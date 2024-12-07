"""Scripts for running Pheasy"""
# -*- coding: utf-8 -*-
# Copyright (C) 2021-2023 Changpeng Lin
# All rights reserved.

import os
import datetime
from collections import deque

import numpy as np
import scipy.sparse as spmat
import pickle
import pheasy.structure.io as io
from pheasy.version import get_logo_version
from pheasy.basic_io import InputParser, logger
from pheasy.structure.atoms import NeighborList, create_supercell
from pheasy.structure.symmetry import get_spacegroup, get_symmetry
from pheasy.structure.force_constants import ForceConstants
from pheasy.core.cluster_orbit import CSGenerator, ClusterSpace
from pheasy.core.symmetry_constraints import SymmetryConstraints
from pheasy.core.utilities import get_exclude_set
from pheasy.core.optimizer import Optimizer
from pheasy.core.displacements import (
    move_atoms_simple,
    generate_displacements_from_file,
    generate_displacements_from_aimd,
    build_sensing_matrix,
)
from pheasy.core.forces import read_interatomic_forces, read_interatomic_forces_aimd


class WorkFlow(object):
    """Class defining a complete workflow of calculations.

    The workflow consists of mandatory and optional tasks.
    Each task has a method that runs the calculation. To 
    add a new calculation, the corresponding run method 
    should be implemented here.
    manatory :
        welcome
        run_cell
        run_neighborlist_cutoff
    optional :
        run_cluster_expansion
        run_symmetry_constraints
        run_sensing_matrix
        run_fit_force_constants

    """

    def __init__(self, parser):
        """Initialize with an input parser and set default filenames.

        Parameters
        ----------
        parser : InputParser
            An instance of class InputParser.

        """
        self.settings = parser.settings

        self.NeighborListFile = "neighbor_list.pkl"
        self.ClusterSpaceFile = "cs.pkl"
        self.ConstraintsFile = "constraints.pkl"
        self.SensingMatrixFile = "sm_prime.npz"
        self.ForceArrayFile = "fm1d.npz"
        self.ForceMatrixFile = "fm2d.npz"
        self.ForceConstantArrayFile = "phi.npz"
        self.AForceConstantArrayFile = "phi_anharm.npz"

    def welcome(self):
        """Print welcome information.
        """
        logo_list = get_logo_version()
        logo = logo_list[np.random.randint(len(logo_list))]
        logger.info("Start Pheasy." + logo)

    def run_cell(self):
        """Parse primitive cell and create supercell.

        Returns:
        -------
        pcell : pheasy.Atoms
            Primitive unit cell structure.
        scell : pheasy.Atoms
            Supercell structure.

        """
        settings = self.settings

        """Read primitive unit cell and check settings"""
        pcell = io.read_cell(settings.PCELL_FILENAME, settings=settings)
        natom = pcell.get_global_number_of_atoms()
        InputParser.check_args(settings, natom)
        ndim = np.prod(settings.DIM)
        natoms = ndim * natom

        """Set magmom in case of magnetic materials."""
        if settings.IS_MAGNETIC:
            if len(settings.MAGMOM) == 3 * natom:  # collinear case
                settings.MAGMOM = np.reshape(settings.MAGMOM, (natom, 3))
            else:
                settings.MAGMOM = np.array(settings.MAGMOM)
            self.settings = settings
            pcell.set_initial_magnetic_moments(settings.MAGMOM)

        """Print crystal system information."""
        space_group = get_spacegroup(pcell, symprec=settings.SYMPREC)
        pcell.symops = get_symmetry(
            pcell, symprec=settings.SYMPREC, is_magnetic=settings.IS_MAGNETIC
        )
        io.write_symops(pcell.symops, "pcell.symops")
        nsym = pcell.get_number_of_symmetries()
        logger.info("System: %s" % pcell.get_chemical_formula())
        logger.info(
            "Space group: %s, %i symmetry operations found." % (space_group, nsym)
        )

        """Create supercell or read supercell from file.
           In case of reading supercell from file, check if DIM is
           consistent with total numbe of atoms in the supercell."""
        if settings.READ_SCELL:  # read supercell
            logger.info(
                "Read {0[0]:d} x {0[1]:d} x {0[2]:d} supercell from file ({1:d} atoms).".format(
                    settings.DIM, natoms
                )
            )
            scell = io.read_cell(
                settings.SCELL_FILENAME, settings=settings, supercell=True
            )
            if (ndim * natom) != scell.get_global_number_of_atoms():
                logger.error(
                    "Number of atoms in supercell inconsistent with argument DIM."
                )
                raise ValueError
            scell.set_supercell(settings.DIM)
            if settings.IS_MAGNEIC:  # in case of magnetic materials
                if len(settings.MAGMOM.shape) == 1:
                    smagmom = np.repeat(settings.MAGMOM, ndim)
                else:
                    smagmom = np.repeat(settings.MAGMOM, ndim, axis=0)
                scell.set_initial_magnetic_moments(smagmom)
        else:  # create supercell
            logger.info(
                "Creating {0[0]:d} x {0[1]:d} x {0[2]:d} supercell ({1:d} atoms).".format(
                    settings.DIM, natoms
                )
            )
            scell = create_supercell(pcell, settings.DIM, settings.IS_MAGNETIC)
            io.write_cell(scell, settings=settings)
        if settings.QE:
            if os.path.isfile(settings.PW_HEADER_FILE):
                scell.read_pw_header(settings.PW_HEADER_FILE)

        """Set dielectric tensor and Born effective charges."""
        if settings.NAC != 0:
            born_info = io.read_dielectrics(settings.BORN_FILE)
            if np.reshape(born_info[1])[0] != natom:
                logger.error("Shape of Born effective charge tensor is wrong.")
                raise ValueError
            pcell.set_dielectrics(born_info[0], born_info[1])
            scell.set_dielectrics(born_info[0], born_info[1])

        """Set mapping between primitive and supercell atomic indices."""
        scell.set_smap()
        scell.set_pmap()

        """Analyze supercell symmetry."""
        scell.symops = get_symmetry(
            scell, symprec=settings.SYMPREC, is_magnetic=settings.IS_MAGNETIC
        )
        io.write_symops(scell.symops, "scell.symops")

        self.pcell = pcell
        self.scell = scell

    def run_neighborlist_cutoff(self):
        """Analyze neighbor list and cutoffs.

        Generate a neighbor list or read it from pickle file.
        Config cutoff distance for interatomic force constants.

        Returns:
        -------
        nn_list : NeighborList
            An instance of class NeighborList created for 
            supercell structure.
        cutoffs : dict
            A dictionary for cutoffs at different orders.

        """
        settings = self.settings

        if os.path.isfile(self.NeighborListFile):
            nn_list = NeighborList.read(self.NeighborListFile)
            if list(nn_list.supercell) != settings.DIM:
                logger.warning(
                    "System dimension defined in neighbor list file"
                    + " is not consistent with DIM."
                )
                nn_list = NeighborList(
                    self.scell, self.pcell.symops["equivalent_atoms"]
                )
                nn_list.write(self.NeighborListFile)
        else:
            nn_list = NeighborList(self.scell, self.pcell.symops["equivalent_atoms"])
            nn_list.write(self.NeighborListFile)
        self.scell.set_wigner_seitz_offsets(nn_list.ws_offsets)

        cutoffs = {}
        for n in range(2, settings.MAX_ORDER + 1):
            cutoff = getattr(settings, "CUT" + str(n))
            if cutoff is None:
                cutoffs[n] = np.inf
            elif cutoff > 0:
                cutoffs[n] = cutoff
            else:
                nth = int(abs(cutoff))
                cutoffs[n] = nn_list.get_neighbor_cutoff_distance(nth)

        self.cutoffs = cutoffs
        self.nn_list = nn_list

    def run_cluster_expansion(self):
        """Generate cluster-orbit space CS_full."""
        settings = self.settings

        if settings.SPG_CLUS:
            start_time_sub = datetime.datetime.now()

            logger.info(
                "Starting to generate cluster space up to {}-order.".format(
                    settings.MAX_ORDER
                )
            )
            CS_generator = CSGenerator(
                self.nn_list,
                self.scell.symops,
                settings.MAX_ORDER,
                self.cutoffs,
                settings.NBODY,
            )
            CS_full = CS_generator.generate_represent_clusters_with_orbit()
            CS_full.write(self.ClusterSpaceFile)
            end_time_sub = datetime.datetime.now()
            time_cost = end_time_sub - start_time_sub
            logger.info(
                "Cluster space generation finished, time cost: {}.".format(time_cost)
            )
        else:
            """Read cluster space from file and print related information."""
            if os.path.isfile(self.ClusterSpaceFile):
                logger.info(
                    "Reading and generating cluster space from file, "
                    + f"up to {settings.MAX_ORDER}-order."
                )
                CS_full = ClusterSpace.read(self.ClusterSpaceFile)
                CS_full.print_cluster_space_info()

        self.CS_full = CS_full

    def run_symmetry_constraints(self):
        """Apply symmetry constraints and construct null space."""
        settings = self.settings

        if settings.NULL_SPACE:
            start_time_sub = datetime.datetime.now()
            logger.info("Starting to construct symmetry constraints and null space.")
            if settings.CRYS_BASIS:
                logger.info("Symmmetry constraints are imposed in crystal coordinate.")
            else:
                logger.info(
                    "Symmmetry constraints are imposed in Cartesian coordinate."
                )

            symmetry_constraints = SymmetryConstraints(
                self.scell,
                settings.CRYS_BASIS,
                rasr=settings.RASR,
                do_rasr=settings.DO_RASR,
                nac=settings.NAC,
                eps=settings.EPS,
            )
            self.NS_full = symmetry_constraints.impose_symmtery_constaints(self.CS_full)
            if settings.WRITE_SYM_CONS:
                symmetry_constraints.write(self.ConstraintsFile)

            end_time_sub = datetime.datetime.now()
            time_cost = end_time_sub - start_time_sub
            logger.info(
                "Construction of symmetry constraints finished, time cost: {}.".format(
                    time_cost
                )
            )
        else:
            if settings.FIT_IFC or settings.MODE.upper() == "PP":
                logger.info(
                    "Reconstructing null space of symmetry constraints from file."
                )
                self.NS_full = SymmetryConstraints.construct_null_space_restart(
                    settings.MAX_ORDER
                )

    def run_sensing_matrix(self):
        """Create displaced configurations and construct sensing matrix."""
        settings = self.settings

        if settings.SENSING_MAT:
            start_time_sub = datetime.datetime.now()
            logger.info("Starting to construct sensing (displacement) matrix.")

            if settings.QE:
                file_format = "qe"
                filename_pattern = "DISP.in.{{0:0{0}d}}".format(3)
            else:
                file_format = "vasp"
                filename_pattern = "DISP.POSCAR.{{0:0{0}d}}".format(3)

            sensing_mat_list = deque()

            if settings.MODE.upper() == "RANDOM":
                if settings.DISP_FILE:
                    logger.info("Reading displaced configurations from file.")
                    with open("disp_matrix.pkl", "rb") as file:
                         u_matrix = pickle.load(file)
                    for n in range(settings.NDATA):
                        u_vecs = u_matrix[n,:,:]
                        #filename = filename_pattern.format(n + 1)
                        #disp_scell = generate_displacements_from_file(
                         #   self.scell, filename, file_format
                        #)
                        #u_vecs = disp_scell.get_atomic_displacements()
                        #u_max = np.amax(np.linalg.norm(u_vecs, axis=1))
                        #logger.info(
                         #   "- Reading {} of {}, max u: {:.4f} A.".format(
                         #       n + 1, settings.NDATA, u_max
                          #  )
                        #)
                        sensing_mat = build_sensing_matrix(self.CS_full, u_vecs)
                        sensing_mat_list.append(sensing_mat)
                else:
                    logger.info(
                        "Displacing atoms randomly by {} A.".format(settings.U_VAL)
                    )
                    for n in range(settings.NDATA):
                        filename = filename_pattern.format(n + 1)
                        disp_scell = move_atoms_simple(self.scell, settings.U_VAL)
                        disp_scell.automatic_write(filename, file_format)
                        u_vecs = disp_scell.get_atomic_displacements()
                        logger.info(
                            "- Generating displaced configuration {} of {}.".format(
                                n + 1, settings.NDATA
                            )
                        )
                        sensing_mat = build_sensing_matrix(self.CS_full, u_vecs)
                        sensing_mat_list.append(sensing_mat)

            elif settings.MODE.upper() == "AIMD":
                logger.info("Reading displaced configurations from AIMD trajectories.")
                if settings.NSKIP is not None:
                    logger.info(
                        "- The first {} steps of AIMD are skipped.".format(
                            settings.NSKIP
                        )
                    )
                logger.info(
                    "- Number of sampled structures: {}.".format(settings.NDATA)
                )
                logger.info("- Sampling interval: {}.".format(settings.NSTEP))
                disp_scell_list = generate_displacements_from_aimd(
                    self.scell,
                    settings.NDATA,
                    settings.NSKIP,
                    settings.NSTEP,
                    file_format,
                )
                u_vecs_list = deque(
                    map(lambda x: x.get_atomic_displacements(), disp_scell_list)
                )
                for u_vecs in u_vecs_list:
                    sensing_mat = build_sensing_matrix(self.CS_full, u_vecs)
                    sensing_mat_list.append(sensing_mat)

                F_mean = deque()
                force_list = deque(map(lambda x: x.get_forces(), disp_scell_list))
                for forces in force_list:
                    F_mean.append(forces.mean(axis=0))
                F_mat = np.vstack(force_list)
                np.savez_compressed(
                    self.ForceMatrixFile, F=F_mat, mean=np.array(F_mean)
                )

            self.SM_prime = spmat.coo_matrix(np.vstack(sensing_mat_list))
            spmat.save_npz(self.SensingMatrixFile, self.SM_prime)

            end_time_sub = datetime.datetime.now()
            time_cost = end_time_sub - start_time_sub
            logger.info(
                "Construction of sensing (displacement) matrix finished, time cost: {}.".format(
                    time_cost
                )
            )
        else:
            if settings.FIT_IFC:
                logger.info("Reconstructing sensing (displacement) matrix from file.")
                self.SM_prime = spmat.load_npz(self.SensingMatrixFile)

    def run_fit_force_constants(self):
        """Fit interatomic force constants."""
        settings = self.settings
        natoms = self.scell.get_global_number_of_atoms()

        if settings.FIT_IFC:
            start_time_sub = datetime.datetime.now()
            logger.info("Starting to fit interatomic force constants.")

            # Create ForceConstants instance.
            FC_model = ForceConstants(self.scell, self.CS_full)

            # Pre-processing sensing matrix
            SM_prime = self.SM_prime.toarray()[: 3 * natoms * settings.NDATA, :]

            if settings.QE:
                file_format = "qe"
                rforce_file = "rforce.out"
                filename_pattern = "DISP.out.{{0:0{0}d}}".format(3)
            else:
                file_format = "vasp"
                rforce_file = "rforce.xml"
                filename_pattern = "vasprun.xml.{{0:0{0}d}}".format(3)

            if settings.RFORCE:
                logger.info("Residual forces of perfect structure will be removed.")
                rforces = read_interatomic_forces(rforce_file, format=file_format)
            else:
                rforces = np.zeros((natoms, 3))

            if settings.EXCLUDE is not None:
                ex_set = get_exclude_set(settings.EXCLUDE)
                logger.info(
                    "Training samples to be excluded: {}".format(
                        settings.EXCLUDE.replace(" ", "")
                    )
                )
            else:
                ex_set = set()

            if settings.MODE == "RANDOM":
                logger.info(
                    "Reading interatomic forces, {} configurations.".format(
                        settings.NDATA
                    )
                )
                force_list = deque()
                #for n in range(settings.NDATA):
                #    filename = filename_pattern.format(n + 1)
                #    if (n + 1) in ex_set:
                #        continue
                #    forces = read_interatomic_forces(filename, format=file_format)
                 #   res = forces.mean(axis=0)
                  #  force_list.append(forces - rforces)
                  #  logger.info("- {}, average force per atom:".format(filename))
                  #  logger.info("\t {} eV / A".format(res))
                with open("force_matrix.pkl", "rb") as file:
                     f_matrix = pickle.load(file)
                     f_matrix_use = []
                     for n in range(settings.NDATA):
                        f_matrix_new = f_matrix[n,:,:]
                        f_matrix_use.append(f_matrix_new)
                FM = np.vstack(f_matrix_use).flatten()
                if settings.EXCLUDE is not None:
                    sensing_mat_list = deque()
                    for n in range(settings.NDATA):
                        if (n + 1) in ex_set:
                            continue
                        sensing_mat_list.append(
                            SM_prime[3 * natoms * n : 3 * natoms * (n + 1), :]
                        )
                    SM_prime = np.vstack(sensing_mat_list)

            elif settings.MODE == "AIMD":
                logger.info(
                    "Reading interatomic forces from AIMD, {} trajectories.".format(
                        settings.NDATA
                    )
                )
                logger.info("- AIMD average force per atom:")
                if os.path.isfile(self.ForceMatrixFile):
                    F_tmp = np.load(self.ForceMatrixFile)
                    F_mat = F_tmp["F"]
                    F_mean = F_tmp["mean"]
                    if F_mean.shape[0] != settings.NDATA:
                        logger.error(
                            "Wrong dimension of AIMD force database, {} trajectories".format(
                                F_mean.shape[0]
                            )
                        )
                    for n in range(F_mean.shape[0]):
                        logger.info("\t {} eV / A".format(F_mean[n]))
                        F_mat[3 * natoms * n : 3 * natoms * (n + 1), :] -= rforces
                    FM = F_mat.flatten()
                else:
                    force_list = read_interatomic_forces_aimd(
                        settings.NDATA, settings.NSKIP, settings.NSTEP, file_format
                    )
                    for n, forces in enumerate(force_list):
                        res = forces.mean(axis=0)
                        force_list[n] = forces - rforces
                        logger.info("\t {} eV / A".format(res))
                    FM = np.vstack(force_list).flatten()

            np.savez_compressed(self.ForceArrayFile, F=FM)

            if settings.FIX_FC2:
                if settings.MAX_ORDER == 2:
                    logger.info(
                        "No force constants left for fitting "
                        + "when MAX_ORDER is 2 and FIX_FC2 is True."
                    )
                    raise RuntimeError
                else:
                    logger.info("Fix second-order IFCs during fitting.")
                    fc2_fmt = settings.FC2_FMT.upper()
                    NS_harm = spmat.load_npz("ns_harm.npz").toarray()
                    NS_anharm = self.NS_full.toarray()[
                        NS_harm.shape[0] :, NS_harm.shape[1] :
                    ]
                    if fc2_fmt == "PHONOPY":
                        if os.path.isfile("FORCE_CONSTANTS"):
                            fc2_filename = "FORCE_CONSTANTS"
                        else:
                            fc2_filename = "fc.hdf5"
                    elif fc2_fmt == "Q2R":
                        fc2_filename = "espresso.fc"
                    elif fc2_fmt == "NDARRAY":
                        fc2_filename = "Phi2.npz"
                    logger.info(
                        "Reading second-order IFCs from {}.".format(fc2_filename)
                    )
                    Phi2 = FC_model.read_force_constants(
                        self.CS_full, fc2_filename, order=2, format=fc2_fmt, full=False
                    )
                    if isinstance(Phi2, tuple):
                        Phi2 = Phi2[0].flatten()
                    else:
                        Phi2 = Phi2.flatten()
                    if settings.REMOVE_LR and settings.NAC != 0:
                        # TODO
                        pass
                ifc2_num = self.CS_full.get_number_of_ifcs_each_order()[2]
                SM2_prime = SM_prime[:, :ifc2_num]
                SM3_prime = SM_prime[:, ifc2_num:]
                FM -= np.dot(SM2_prime, Phi2)
                SM = np.dot(SM3_prime, NS_anharm)
            else:
                if settings.REMOVE_LR and settings.NAC != 0:
                    pass
                # SM = SM_prime.dot(self.NS_full)
                SM = SM_prime.dot(self.NS_full.toarray())

            # Train interatomic force constants
            optimizer = Optimizer(
                settings.MODEL,
                nalpha=settings.NALPHA,
                alpha_min=settings.ALPHA_MIN,
                alpha_max=settings.ALPHA_MAX,
                cv=settings.CV,
                tol=settings.TOL,
                max_iter=settings.MAX_ITER,
                rand_seed=settings.RAND_SEED,
                standardize=settings.STANDARDIZE,
            )
            if settings.MODEL.upper() == "LASSO":
                logger.info("Fitting force constants via the coordinate descent LASSO.")
            elif settings.MODEL.upper() == "OLS":
                logger.info("Fitting force constants via the ordinary least-square.")
            else:
                logger.error(
                    "Unknown linear model for fitting force constants, {}".format(
                        settings.MODEL
                    )
                )
                raise ValueError
            rank = np.linalg.matrix_rank(SM)
            optimizer.fit(SM, FM)
            fit_results = optimizer.results
            fit_metrics = optimizer.metrics
            FC_model.set_force_constant_metrics(fit_metrics)

            logger.info("Summary of force constants fitting:")
            if settings.MODEL.upper() == "LASSO":
                logger.info(
                    "- Reaching the specified tolerance for the optimal "
                    + "alpha after {} iterations.".format(fit_results["n_iter"])
                )
                logger.info("- alpha_min: 1e{}".format(settings.ALPHA_MIN))
                logger.info("- alpha_max: 1e{}".format(settings.ALPHA_MAX))
                logger.info("- alpha_opt: {}".format(fit_results["alpha"]))
                logger.info("- RMSE_CV: {} eV/A".format(fit_metrics["rmse_path_mean"]))
            logger.info("- RMSE: {} eV/A".format(fit_metrics["rmse"]))
            logger.info("- Relative error: {}".format(optimizer.metrics["re"]))
            logger.info("- Rank of coefficient matrix: {}".format(rank))
            logger.info("- Free IFC terms: {}".format(fit_results["coef"].shape[0]))
            logger.info(
                "- Non-zero IFC terms: {}".format(np.count_nonzero(fit_results["coef"]))
            )

            if settings.FIX_FC2:
                APhi = NS_anharm.dot(fit_results["coef"])
                np.savez_compressed(self.AForceConstantArrayFile, Phi=APhi)
                Phi = np.hstack([Phi2, APhi])
                np.savez_compressed(self.ForceConstantArrayFile, Phi=Phi)
                FC_model.set_force_constants(Phi)
            else:
                Phi = self.NS_full.dot(fit_results["coef"])
                np.savez_compressed(self.ForceConstantArrayFile, Phi=Phi)
                FC_model.set_force_constants(Phi)
                FC_model.write_force_constants(settings, self.CS_full, order=2)
                logger.info("Writing second-order force constants into file.")

            if settings.MAX_ORDER > 2:
                FC_model.write_force_constants(settings, self.CS_full, order=3)
                logger.info("Writing third-order force constants into file.")

            if settings.MAX_ORDER > 3:
                FC_model.write_force_constants(settings, self.CS_full, order=4)
                logger.info("Writing fourth-order force constants into file.")

            end_time_sub = datetime.datetime.now()
            time_cost = end_time_sub - start_time_sub
            logger.info(
                "Force constant fitting finished, time cost: {}.".format(time_cost)
            )

    def run_post_processing(self):
        """Post-process interatomic force constants by adding correct symmetries."""
        from sklearn.linear_model import LinearRegression

        settings = self.settings

        if settings.MODE.upper() == "PP":
            start_time_sub = datetime.datetime.now()
            logger.info("Post-process harmonic interatomic force constants.")
            if settings.MAX_ORDER != 2:
                logger.error(
                    "Force constant post-processing currently only "
                    + "implemented for the second order. Please set MAX_ORDER to 2."
                )
                raise ValueError

            # Create ForceConstants instance.
            FC_model = ForceConstants(self.scell, self.CS_full)

            # Read harmonic force constants
            fc2_fmt = settings.FC2_FMT.upper()
            if fc2_fmt == "PHONOPY":
                if os.path.isfile("FORCE_CONSTANTS"):
                    fc2_filename = "FORCE_CONSTANTS"
                else:
                    fc2_filename = "fc.hdf5"
            elif fc2_fmt == "Q2R":
                fc2_filename = "espresso.fc"
            elif fc2_fmt == "NDARRAY":
                fc2_filename = "Phi2.npz"
            logger.info("Reading second-order IFCs from {}.".format(fc2_filename))
            Phi2 = FC_model.read_force_constants(
                self.CS_full, fc2_filename, order=2, format=fc2_fmt, full=False
            )
            if isinstance(Phi2, tuple):
                Phi2 = Phi2[0].flatten()
            else:
                Phi2 = Phi2.flatten()

            # Read null space for harmonic force constants
            NS_harm = spmat.load_npz("ns_harm.npz").toarray()

            # Symmetrize harmonic force constants
            logger.info("Symmetrizing harmonic force constants.")
            linear_model = LinearRegression(fit_intercept=False).fit(NS_harm, Phi2)
            Phi2_reduced = linear_model.coef_
            Phi2_sym = np.dot(NS_harm, Phi2_reduced)
            FC_model.set_force_constants(Phi2_sym)
            FC_model.write_force_constants(settings, self.CS_full, order=2)
            logger.info("Writing harmonic force constants into file.")

            end_time_sub = datetime.datetime.now()
            time_cost = end_time_sub - start_time_sub
            logger.info(
                "Post-processing force constants finished, time cost: {}.".format(
                    time_cost
                )
            )


def main():
    # TODO: create a base CalTask class and put the realization of calculation
    #       into a class with a run method inheriting from CalTask class.
    """Pheasy Main Routine"""
    start_time = datetime.datetime.now()

    parser = InputParser()  # instantiate an input parser
    parser.read()  # config user settings via command-line and settings.nml

    logger.config(parser.settings.LOG_FILE)  # set logging outstream, console or file

    workflow = WorkFlow(parser)  # instantiate a workflow

    workflow.welcome()  # print pheasy version and logo

    workflow.run_cell()  # read primitive cell and create supercell

    workflow.run_neighborlist_cutoff()  # analyze neighbor list and cutoffs

    workflow.run_cluster_expansion()  # analyze supercell symmetry and generate cluster-orbit space

    workflow.run_symmetry_constraints()  # apply symmetry constraints and calculate null space

    workflow.run_sensing_matrix()  # create displaced configurations and construct sensing matrix

    workflow.run_fit_force_constants()  # fit interatomic force constants

    workflow.run_post_processing()  # post-process interatomic force constants

    """Finalize and estimate time cost"""
    end_time = datetime.datetime.now()
    total_time = end_time - start_time
    logger.info("Finalize Pheasy, total time cost: {}.".format(total_time))
