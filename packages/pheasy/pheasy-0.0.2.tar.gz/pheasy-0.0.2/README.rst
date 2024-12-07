Pheasy: a calculator for high-order anharmonicity and phonon quasiparticles
===========================================================================

* Free software: GNU General Public License v3
* Please note this is a prerelease version to be compatible with the atomate2_ 
  package and used for the high-througput phonon calculations of `Materials Project`_.
  The official release will be available soon.

Authors:
--------

*  Changpeng Lin (changpeng.lin@epfl.ch), École Polytechnique Fédérale
   de Lausanne

*  Jian Han (thu-hanjian@qq.com), Tsinghua University

*  Nicola Marzari (nicola.marzari@epfl.ch), École Polytechnique Fédérale
   de Lausanne

*  Ben Xu (bxu@gscaep.ac.cn), Graduate School of China Academy of
   Engineering Physics

Features
--------

*  Efficient extraction of interatomic force constants up to
   sixth-order with the separate treatment of long-range Coulomb
   interactions for infrared-active solids;

*  Temperature renormalization of phonon quasiparticles via
   temperature-dependent effective potential, self-consistent *ab
   initio* lattice dynamics and self-consistent phonons via 
   statistical perturbation-operator renormalization;

*  Complete invariance and equilibrium conditions for lattice dynamics
   including the exact treatment for infrared-active solids;

*  Interfaced to VASP_ and `Quantum ESPRESSO`_ as force and total energy
   calculators;

*  Interfaced to MATDYN_, Phonopy_, Phono3py_, ShengBTE_ and GPU_PBTE_ for
   lattice dynamics and thermal transport calculations.

Installation via pip
--------------------

#. Git clone from our `GitLab repository <https://gitlab.com/cplin/pheasy>`_::

    git clone https://gitlab.com/cplin/pheasy.git

#. Move into **pheasy** directory::

    cd ./pheasy

#. Install via *pip* tool in developing mode::

    pip install -e .

.. _VASP: https://www.vasp.at/
.. _`Quantum ESPRESSO`: https://www.quantum-espresso.org/
.. _MATDYN: https://www.quantum-espresso.org/Doc/INPUT_MATDYN.html
.. _Phonopy: https://phonopy.github.io/phonopy/
.. _Phono3py: https://phonopy.github.io/phono3py/
.. _ShengBTE: https://www.shengbte.org/home
.. _GPU_PBTE: https://gitlab.com/xiaokun.gu/
.. _atomate2: https://materialsproject.github.io/atomate2/
.. _`Materials Project`: https://materialsproject.org/
