'''

Symmetry analysis.

Created on 2018.7.2

@author: YeAnjiang
'''
import re
import spglib
import numpy as np
import pandas as pd
from mgtoolbox_kernel.util.base import parse_sitesym
from scipy.spatial.ckdtree import cKDTree
from monty.io import zopen

# Using spglib to analyze the space group in .vasp file
def get_symmetry_spglib(filename, symprec=0.00001):
    with zopen(filename, "rt") as f:
        contents = f.read()
    poscar = Poscar_new.from_string(contents, False, read_velocities=False)
    positions = poscar.coords
    lattice = poscar.lattice
    atomic_symbols = poscar.atomic_symbols
    numbers = [] 
    a = ""
    j = 0
    for i in atomic_symbols:
        if i != a:
            a = i
            j = j+1
        numbers.append(j)

    cell = (lattice, positions, numbers)
    dataset = spglib.get_symmetry_dataset(cell, symprec)
    print("space group: ", dataset['international'],dataset['number'])
    print("rotations: ", dataset['rotations'])
    print("translations: ", dataset['translations'])
    print("equivalent atoms: ", dataset['equivalent_atoms'])
    print("sites wyckoffs: ", dataset['wyckoffs'])
    sym_independ = np.unique(dataset['equivalent_atoms'])
    print("independent atoms: ", sym_independ)
    for i in sym_independ:
        print("coordinates of independent atoms")
        print(positions[i])

"""
    Return the symmetry number of input positions in unitcell.
    Input:
        lattice
        positions
    Output:
        symmetry number or zero.
"""
def get_symnum_sites(lattice, positions, symprec=0.01, angle_tolerance=5):
    numbers = [1,]*len(positions)
    cell = (lattice, positions, numbers)
    dataset = spglib.get_symmetry_dataset(cell, symprec, angle_tolerance)
    if dataset:
        return dataset['number']
    else:
        return 0

"""
Function:
    Get the symmetry equivalent sites for input site.
"""
def get_equivalent_VorNodes(pos, sitesym):
    rot, trans = parse_sitesym(sitesym)
    sympos = np.dot(rot, pos) + trans
    return sympos

"""
    Analyzing the symmetry of Voronoi Network by spglib.
"""
def get_equivalent_vornet(vornet, symprec=1e-5, angle_tolerance=5):
    positions = []
    lattice = vornet.lattice
    for i in vornet.nodes:
        positions.append(i[2])
    numbers = [1,]*len(vornet.nodes)
    cell = (lattice, positions, numbers)

    dataset = spglib.get_symmetry_dataset(cell, symprec, angle_tolerance)
    print(dataset['number'])
    voids = []
    if dataset:
        symm_label = dataset['equivalent_atoms']
        vornet_uni_symm = vornet.parse_symmetry(symm_label)
        sym_independ = np.unique(dataset['equivalent_atoms'])
        print("symm_label", symm_label)
        print("sym_independ", sym_independ)
        print("The number of symmetry distinct voids: ",len(sym_independ))
        for i in sym_independ:
            voids.append(positions[i])
        return vornet_uni_symm,voids
    else:
        return vornet,voids

"""
    Analyzing the symmetry of Voronoi Network by ourself code.
"""
def get_labeled_vornet(vornet, sitesym, symprec=1e-3):
    positions = []
    for i in vornet.nodes:
        positions.append(i[2])

    tags,tagdis = tag_sites(sitesym, positions,symprec)
    voids = []

    vornet_uni_symm = vornet.parse_symmetry(tags)
    sym_independ = np.unique(tags)
    # print("The number of symmetry distinct voids: ",len(sym_independ))
    for i in sym_independ:
         voids.append(positions[i])
    return vornet_uni_symm,voids

"""
    Get unique sites from .vasp file.
"""
def get_unique_sites(filename, sitesym, symprec=1e-3):
    with zopen(filename, "rt") as f:
        contents = f.read()
    poscar = Poscar_new.from_string(contents, False, read_velocities=False)
    positions = poscar.coords
    tags,tagdis = tag_sites(sitesym, positions, symprec)
    print(tags)
    print(tagdis)
    print(np.unique(tags))
    frame = pd.Series(tags)
    print(frame.value_counts())   

"""
    Get symmetry equivalent sites of provided scaled_positions 
    based on provided symmetry operations. This function will 
    return a mapping table of sites to symmetrically independent 
    sites.This is used to find symmetrically equivalent atoms. 
    The numbers contained are the indices of sites starting from 0, 
    i.e., the first atom is numbered as 0, and then 1, 2, 3, … 
    np.unique(equivalent_sites) gives representative symmetrically 
    independent sites.
"""
def tag_sites(sitesym, scaled_positions, symprec=1e-3):
    scaled = np.around(np.array(scaled_positions, ndmin=2),8)
    scaled %= 1.0
    scaled %= 1.0
    np.set_printoptions(suppress=True)
    tags = -np.ones((len(scaled), ), dtype=int)
    tagdis = 100*np.ones((len(scaled), ), dtype=float)
    rot, trans = parse_sitesym(sitesym)

    siteskdTree = cKDTree(scaled)
    for i in range(len(scaled)):
        if tags[i] == -1:
            curpos = scaled[i]
            sympos = np.dot(rot, curpos) + trans
            sympos %= 1.0
            sympos %= 1.0
            sympos = np.unique(np.around(sympos,8), axis=0)
            min_dis,min_ids = siteskdTree.query(sympos,k=1)
            # print(i,len(min_dis))
            # print(min_dis)

            select = min_dis <= symprec
            select_ids = min_ids[select]
            tags[select_ids] = i
            tagdis[select_ids] = min_dis[select]
    return tags,tagdis

def get_vornet_labeled(vornet, symm_ops, symprec=1e-3):
    positions = []
    for i in vornet.nodes:
        positions.append(i[2])

    tags,tagdis = sites_tag(symm_ops, positions,symprec)
    voids = []

    vornet_uni_symm = vornet.parse_symmetry(tags)
    sym_independ = np.unique(tags)
    # print("The number of symmetry distinct voids: ",len(sym_independ))
    for i in sym_independ:
         voids.append(positions[i])
    return vornet_uni_symm,voids

def sites_tag(symm_ops, scaled_positions, symprec=1e-3):
    scaled = np.around(np.array(scaled_positions, ndmin=2),8)
    scaled %= 1.0
    scaled %= 1.0
    np.set_printoptions(suppress=True)
    tags = -np.ones((len(scaled), ), dtype=int)
    tagdis = 100*np.ones((len(scaled), ), dtype=float)
    rot, trans = symm_ops

    siteskdTree = cKDTree(scaled)
    for i in range(len(scaled)):
        if tags[i] == -1:
            curpos = scaled[i]
            sympos = np.dot(rot, curpos) + trans
            sympos %= 1.0
            sympos %= 1.0
            sympos = np.unique(np.around(sympos,8), axis=0)
            min_dis,min_ids = siteskdTree.query(sympos,k=1)
            # print(i,len(min_dis))
            # print(min_dis)

            select = min_dis <= symprec
            select_ids = min_ids[select]
            tags[select_ids] = i
            tagdis[select_ids] = min_dis[select]
    return tags,tagdis