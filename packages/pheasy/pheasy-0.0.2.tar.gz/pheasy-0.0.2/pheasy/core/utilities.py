"""Miscellaneous useful functions."""
# -*- coding: utf-8 -*-
# Copyright (C) 2021-2023 Changpeng Lin
# All rights reserved.

__all__ = [
    "kron_product",
    "kron_product_einsum",
    "kron_product_sparse",
    "rref_dense",
    "null_space_dense",
    "block_diag_sparse",
    "get_permutation_matrix",
    "get_permutation_tensor",
    "get_rotation_cartesian",
    "get_exclude_set",
    "generate_uniform_grid",
]

import numbers
import itertools
from copy import deepcopy
from collections import deque

import numpy as np
from scipy.sparse import coo_matrix, issparse, kron


def kron_product(mat, times=2):
    """A wrapper of multiple-time Kronecker product.

    If the input 'times' is smaller than 5, 'kron_product_einsum' will
    be called to calculate the result; Otherwise, 'kron_product_sparse'
    will be used to compute the result.

    Parameters
    ----------
    mat : numpy.ndarray
        Input matrix.
    times : int
        The number of times of Kronecker product to be performed.

    Returns:
    -------
    scipy.sparse.coo_matrixs
        The resulting Kronecker product in COO sparse form.

    """
    if times < 5:
        result = kron_product_einsum(mat, times)
        return coo_matrix(result.reshape(3 ** times, 3 ** times))
    else:
        return kron_product_sparse(mat, times)


def kron_product_einsum(mat, times=2):
    """Perform multiple-time Kronecker product using einsum.

    Parameters
    ----------
    mat : numpy.ndarray
        Input matrix.
    times : int
        The number of times of Kronecker product to be performed.

    Returns:
    -------
    np.ndarray
        The resulting Kronecker product as a tensor.

    """
    input = []
    for i in range(times):
        input.append(mat)
        input.append([i, times + i])

    return np.einsum(*input)


def kron_product_sparse(mat, times=2):
    """Sparse version of multiple-time Kronecker product.

    Parameters
    ----------
    mat : numpy.ndarray
        Input matrix.
    times : int
        The number of times of Kronecker product to be performed.

    Returns:
    -------
    scipy.sparse.coo_matrixs
        The resulting Kronecker product in COO sparse form.

    """
    result = kron(mat, mat)
    for n in range(times - 2):
        result = kron(result, mat)

    return result.tocoo()


def block_diag_sparse(mats, order, format=None, dtype=None):
    """Build a block diagonal sparse matrix from provided matrices.

    This function is originally defined in scipy.sparse.block_diag
    which has been modified here to tackle with the special case of
    making a block diagonal sparse matrix from a list of sub-null-space
    for each representative clusters, i.e. a sub-null-space having zero
    vectors.

    https://github.com/scipy/scipy/blob/v1.8.0/scipy/sparse/_construct.py

    Parameters
    ----------
    mats : sequence of matrices
        Input matrices.
    order : int
        The order of IFCs or cluster.
    format : str, optional
        The sparse format of the result (e.g., "csr"). If not given, the matrix
        is returned in "coo" format.
    dtype : dtype specifier, optional
        The data-type of the output matrix. If not given, the dtype is
        determined from that of `blocks`.

    Returns
    -------
    res : sparse matrix

    """
    row = []
    col = []
    data = []
    r_idx = 0
    c_idx = 0
    fc_row = np.power(3, order)
    for a in mats:
        if isinstance(a, (list, numbers.Number)):
            a = coo_matrix(a)
        if a.shape == (1, 0) or a.shape == (0,):
            nrows, ncols = fc_row, 0
        else:
            nrows, ncols = a.shape
        if issparse(a):
            a = a.tocoo()
            row.append(a.row + r_idx)
            col.append(a.col + c_idx)
            data.append(a.data)
        else:
            if a.shape != (1, 0) or a.shape != (0,):
                a_row, a_col = np.divmod(np.arange(nrows * ncols), ncols)
                row.append(a_row + r_idx)
                col.append(a_col + c_idx)
                data.append(a.ravel())
        r_idx += nrows
        c_idx += ncols
    row = np.concatenate(row)
    col = np.concatenate(col)
    data = np.concatenate(data)
    return coo_matrix((data, (row, col)), shape=(r_idx, c_idx), dtype=dtype).asformat(
        format
    )


def get_permutation_matrix(index_orginal, index_permuted):
    """Compute permutation matrix according to input atom index.

    This function generates matrix representation R of permutation
    symmetry for IFCs, i.e. R \Phi(index) = \Phi(index_permuted)
    (old implementation).

    Parameters
    ----------
    index_original : list or numpy.ndarray
        Original atom index from the input. If it is not given,
        the original atom index will be taken from object itself.
    index_permuted : list or numpy.ndarray
        Atom index of the cluster after permutation.

    Returns:
    -------
    scypy.sparse.coo_matrix
        The permutation matrx with the shape (ifc_num, ifc_num).

    """
    order = len(index_orginal)
    ifc_num = np.power(3, order)
    if index_orginal == index_permuted:
        Rmat = np.identity(ifc_num)
    else:
        Rmat = np.zeros((ifc_num, ifc_num))
        components = list(itertools.product(["x", "y", "z"], repeat=order))
        idx_before = list(
            zip(range(ifc_num), np.tile(index_orginal, (ifc_num, 1)), components)
        )
        idx_after = list(
            zip(range(ifc_num), np.tile(index_permuted, (ifc_num, 1)), components)
        )
        for row in idx_after:
            for i, col in enumerate(idx_before):
                if sorted(list(zip(row[1], row[2]))) == sorted(
                    list(zip(col[1], col[2]))
                ):
                    Rmat[row[0], col[0]] = 1.0
                    idx_before.pop(i)
                    break

    return coo_matrix(Rmat)


def get_permutation_tensor(index_orginal, index_permuted):
    """Compute permutation tensor according to input atom index.

    This function is similar to 'get_permutation_matrix'. However,
    it uses tensor notation and the resulting permutation for IFCs
    is returned as a multi-dimension tensor by using numpy.einsum.

    Parameters
    ----------
    index_original : list or numpy.ndarray
        Original atom index from the input. If it is not given,
        the original atom index will be taken from object itself.
    index_permuted : list or numpy.ndarray
        Atom index of the cluster after permutation.

    Returns:
    -------
    numpy.ndarray
        The permutation tensor with the IFC-order related shape.

    """
    order = len(index_orginal)
    Rmat = kron_product_einsum(np.identity(3), order)
    if index_orginal == index_permuted:
        return Rmat
    else:
        input = list(range(order * 2))
        input_org = list(range(order * 2))
        index_tmp = deepcopy(index_permuted)
        for i, idx in enumerate(index_orginal):
            j = index_tmp.index(idx)
            input[order + j] = input_org[order + i]
            index_tmp[j] = -1
        return np.einsum(Rmat, input)


def get_rotation_cartesian(rotmat, cell, eps=1e-4):
    """Convert rotation matrix from crystal to Cartesian coordinate.

    Parameters
    ----------
    rotmat : numpy.ndarray
        (3,3) Rotation matrix in crystal coordinate.
    cell : numpy.ndarray
        (3,3) Lattice vectors of supercell.

    Returns:
    -------
    numpy.ndarray
        (3,3) Rotation matrix in Cartesian coordinate.
    
    """
    crotmat = np.linalg.multi_dot((cell.T, rotmat, np.linalg.inv(cell.T)))
    crotmat = np.where(abs(crotmat) < eps, 0.0, crotmat)
    return crotmat


def get_exclude_set(exclude):
    """Return a set of excluded training samples.

    Parameters
    ----------
    exclude : str
        Index of excluded training samples given by
        a string. For instance, 'exclude=2-4,7,9'
        means the samples from 2 to 4, 7 and 9 
        are excluded in force constant fitting.
        
    Returns:
    -------
    set
        A set of excluded training samples.

    """
    ex_set = []
    item_list = [i.strip() for i in exclude.split(",")]
    for item in item_list:
        if "-" in item:
            low, high = [int(i) for i in item.split("-")]
            ex_set += list(range(low, high + 1))
        else:
            ex_set.append(int(item))

    return set(ex_set)


def generate_uniform_grid(grid_size):
    """Generate a uniform grid for the given grid size.

    Parameters
    ----------
    grid_size : list or numpy.array
        Input uniform grid where irreducible k/q-points is searched.
        All of elements should be integer.

    Returns:
        grid : numpy.array
            An array of scaled grid points in the range [-0.5, 0.5),
            in the shape (npts, 3).

    """
    trans = [x[::-1] for x in np.ndindex(*grid_size[::-1])]
    grid = trans / grid_size
    grid = np.where(grid >= 0.5, grid - 1.0, grid)

    return grid


def rref_dense(mat, eps=1e-4):
    """A dense version of full-pivot Gauss-Jordan elimination.

    mat : numpy.ndarray
        Input matrix.
    eps : float
        Numeric tolerance.

    Returns:
    -------
    mat : numpy.ndarray
        Input matrix in reduced row echelon form.
    pivots : list
        A list of pivots for the reduced row echelon matrix.

    """
    shape = mat.shape
    pivots = deque()

    while True:
        mat[np.where(np.linalg.norm(mat, axis=1) < eps)] = 0
        mat_zero = mat.copy()
        if pivots:
            pivot_tmp = np.array(pivots)
            mat_zero[pivot_tmp[:, 0]] = 0
            mat_zero[:, pivot_tmp[:, 1]] = 0
        if np.max(np.absolute(mat_zero)) == 0:
            break
        idx = np.unravel_index(np.absolute(mat_zero).argmax(), shape)
        pivots.append(idx)

        povit = mat[idx]
        mat_idx = mat[idx[0]] / povit
        mat = mat - np.outer(mat[:, idx[1]], mat[idx[0]]) / povit
        mat[idx[0]] = mat_idx

    return (mat, pivots)


def null_space_dense(mat, eps=1e-4):
    """Calculate the null space of the input matrix.

    Parameters
    ----------
    mat : numpy.ndarray
        Input matrix.
    eps : float
        Numeric tolerance.

    Returns:
    -------
    numpy.ndarray
        Null space of the input matrix.

    """
    rref, pivots = rref_dense(mat, eps)
    shape = rref.shape
    if pivots == deque():
        null_space = np.eye(shape[1])
    else:
        pivots = np.array(pivots)
        col = np.arange(shape[1], dtype="int")
        col = col[np.isin(col, pivots[:, 1], invert=True)]
        if col.shape == (0,):
            null_space = np.array([])
        else:
            null_space = np.zeros((shape[1], col.shape[0]))
            null_space[col, range(col.shape[0])] = 1.0
            null_space[pivots[:, 1, None], range(col.shape[0])] = -rref[
                pivots[:, 0, None], col
            ]

    return null_space
