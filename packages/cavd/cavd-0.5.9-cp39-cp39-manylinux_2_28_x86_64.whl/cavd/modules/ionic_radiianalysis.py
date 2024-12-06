# -*- encoding: utf-8 -*-
"""
    @File    :   ionic_radius.py
    @Time    :   2022/5/14
    @Author  :   赖智聪
    @Version :   0.1
    @Email   :   3338910983@qq.com
    @Desc    :   获得离子半径。
"""
import numpy as np
import math
import re
import os
import json
from bisect import bisect_left

from cavd.modules.oxidation_state import get_oxstate_from_struct
from mgtoolbox_kernel.kernel.structure import Structure


def getlattic_matrix(a, b, c, alpha, beta, gamma):
    lattic_matrix = np.zeros((3, 3))
    cosgamma = math.cos(math.radians(gamma))
    singamma = math.sin(math.radians(gamma))
    cosbeta = math.cos(math.radians(beta))
    cosalpha = math.cos(math.radians(alpha))
    lattic_matrix[0, 0] = a
    lattic_matrix[1, 0] = 0.0
    lattic_matrix[2, 0] = 0.0
    lattic_matrix[0, 1] = b * cosgamma
    lattic_matrix[1, 1] = b * singamma
    lattic_matrix[2, 1] = 0.0
    lattic_matrix[0, 2] = c * cosbeta
    lattic_matrix[1, 2] = (c * (cosalpha - cosgamma * cosbeta)) / singamma
    lattic_matrix[2, 2] = c * math.sqrt(1 - cosbeta**2 - (lattic_matrix[1, 2] / c) ** 2)
    return lattic_matrix.T


period_list = [
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0],
    [0.0, 0.0, -1.0],
    [0.0, 1.0, 0.0],
    [0.0, -1.0, 0.0],
    [1.0, 0.0, 0.0],
    [-1.0, 0.0, 0.0],
    [0.0, 1.0, 1.0],
    [0.0, 1.0, -1.0],
    [0.0, -1.0, 1.0],
    [0.0, -1.0, -1.0],
    [1.0, 0.0, 1.0],
    [1.0, 0.0, -1.0],
    [-1.0, 0.0, 1.0],
    [-1.0, 0.0, -1.0],
    [1.0, 1.0, 0.0],
    [1.0, -1.0, 0.0],
    [-1.0, 1.0, 0.0],
    [-1.0, -1.0, 0.0],
    [1.0, 1.0, 1.0],
    [1.0, 1.0, -1.0],
    [1.0, -1.0, 1.0],
    [1.0, -1.0, -1.0],
    [-1.0, 1.0, 1.0],
    [-1.0, 1.0, -1.0],
    [-1.0, -1.0, 1.0],
    [-1.0, -1.0, -1.0],
]


def get_period_dis(frac_site1, frac_site2, lattice_matrix):
    """
    Considering the periodicity of crystals to obtain the distance
    between two points within the crystal.
    :param frac_site1: fractional coordinates of site frac_site1,such as[0.5, 0.5, 0.5]
    :param frac_site2: fractional coordinates of site frac_site2
    :param lattice_matrix: lattice_matrix
    :return: the shortest distance between two sites and
    the number of ions with the shortest distance between them
    """
    actual_site1 = np.dot(frac_site1, lattice_matrix)
    frac_site2 = np.array(frac_site2)
    dis_list = []
    for i in period_list:
        period_i = np.array(i)
        temp_frac_site2 = period_i + frac_site2
        temp_actual_site2 = np.dot(temp_frac_site2, lattice_matrix)
        temp_dis = np.linalg.norm(temp_actual_site2 - actual_site1)
        dis_list.append(temp_dis)
    sorted_list = sorted(dis_list)
    min_dis = sorted_list[0]
    max_value = min_dis + 0.03
    cout = 0
    for num in sorted_list:
        if min_dis <= num <= max_value:
            cout += 1
    return min_dis, cout


def different_sign(num1, num2):
    if (num1 > 0 and num2 > 0) or (num1 < 0 and num2 < 0):
        return False
    else:
        return True


def get_r0_b(element1, valence1, element2, valence2, file_path):
    """
    Obtain r0 and b of the target element from the file
    """
    file_dir = os.path.dirname(__file__)
    file = os.path.join(file_dir, file_path)
    with open(file, "r") as f:
        for line in f:
            # 将每行按空格切割成列表
            params = line.strip().split()
            if valence1 < 0:
                [element1, element2] = [element2, element1]
                [valence1, valence2] = [valence2, valence1]
            if (
                params[0] == element1
                and int(params[1]) == valence1
                and params[2] == element2
                and int(params[3]) == valence2
            ):
                r0 = float(params[4])
                b = float(params[5])
                return r0, b
    # 如果未找到匹配行，则返回None
    return None, None

file_dir = os.path.dirname(__file__)
rad_file = os.path.join(file_dir, "ionic_radii.json")
with open(rad_file, "r") as fp:
    _ion_radii = json.load(fp)


def nearest_key(sorted_vals, key):
    """
    Returns the key of the sorted list element closest to the target key
    :param sorted_vals:sorted list
    :param key:valence
    :return:the key of the sorted list element closest to the target key
    """
    i = bisect_left(sorted_vals, key)
    if i == len(sorted_vals):
        return sorted_vals[-1]
    if i == 0:
        return sorted_vals[0]
    before = sorted_vals[i - 1]
    after = sorted_vals[i]
    if after - key < key - before:
        return after
    else:
        return before

def get_ionic_radius(elem, oxi_state, coord_no):
    """
    Query Shannon table according to element, valence, and coordination number to get ionic radius
    :param elem:
    :param oxi_state:valence
    :param coord_no:ion coordination number
    :return:ionic radius
    """
    # 检查元素是否在香农表中
    if elem not in _ion_radii:
        # raise ValueError(f"Element '{elem}' not found in the Query Shannon table(ionic_radii.json).")
        return 0.0
    try:
        # 根据香农表对元素的价态进行排序，找到最接近的价态
        tab_oxi_states = sorted(map(int, _ion_radii[elem].keys()))
        oxi_state = nearest_key(tab_oxi_states, oxi_state)
        tab_coord_noes = sorted(map(int, _ion_radii[elem][str(oxi_state)].keys()))
        return _ion_radii[elem][str(oxi_state)][str(coord_no)]
    except KeyError:
        # 如果配位数未找到，调整配位数
        if coord_no not in tab_coord_noes:
            for adjustment in [-1, 1]:
                new_coord_no = coord_no + adjustment
                if new_coord_no in tab_coord_noes:
                    return _ion_radii[elem][str(oxi_state)][str(new_coord_no)]
        # 如果仍为找到，在两个最近的配位数之间进行差值
        return iterpolate_radius(tab_coord_noes, elem, oxi_state, coord_no)
    
def iterpolate_radius(tab_coords, elem, oxi_state, coord_no):
    """
    根据给定的配位数列表和元素信息，插值计算离子半径。
    
    参数:
    tab_coords (list): 有效配位数的列表。
    elem (str): 元素符号。
    oxi_state (str): 氧化态。
    coord_no (int): 待插值的配位数。
    
    返回:
    float: 插值计算得到的离子半径。
    """
    i = 0
    # 找到第一个大于或等于coord_no的有效配位数
    while i < len(tab_coords) and coord_no > int(tab_coords[i]):
        i += 1
    # 如果coord_no大于所有有效配位数
    if i == len(tab_coords):
        # 返回与最大配位数对应的离子半径
        return _ion_radii[elem][str(oxi_state)][str(tab_coords[-1])]
    # 如果coord_no小于所有有效配位数
    if i == 0:
        # 返回与最小配位数对应的离子半径
        return _ion_radii[elem][str(oxi_state)][str(tab_coords[0])]
    # 获取两个邻近的配位数对应的离子半径
    radius1 = _ion_radii[elem][oxi_state][tab_coords[i - 1]]
    radius2 = _ion_radii[elem][oxi_state][tab_coords[i]]

    # 计算并返回这两个离子半径的平均值
    return (radius1 + radius2) / 2

def get_ionicradius(structs):
    """
    Get ionic radius
    :param structs:by CifFile get structs
    :return:eg:{'Li0': 0.9, 'Sc1': 0.885, 'Ge2': 0.53, 'O3': 1.24, 'O4': 1.24, 'O5': 1.24}
    """
    radii = {}
    type_index_dict = {}  # 保存每个type值第一次出现的索引
    for i, item in enumerate(structs.sites):
        if item.label not in type_index_dict:
            type_index_dict[item.type] = i
    target_sites = []  # 保存结果
    for i, item in enumerate(structs.sites):
        if i == type_index_dict.get(item.type):  # 该type值第一次出现，保存到结果中
            target_sites.append(item)
    for target_site in structs.sites:
        new_target_site_label = target_site.label
        # new_target_site_label = target_site.label[: target_site.label.rfind("_")]
        coord = 0
        for periodsite in structs.sites:
            new_periodsite_label = periodsite.label
            # new_periodsite_label = periodsite.label[: periodsite.label.rfind("_")]
            if new_target_site_label != new_periodsite_label and different_sign(
                periodsite.atom_valences[0], target_site.atom_valences[0]
            ):
                dis, amount = get_period_dis(
                    target_site.coord,
                    periodsite.coord,
                    structs.cell.cell_basis_vectors
                )
                # if dis < 2.0:
                #     coord += amount
                ele1 = extract_element_symbol(new_target_site_label)
                ele2 = extract_element_symbol(new_periodsite_label)
                # ele1 = re.sub("\d+", "", new_target_site_label)
                # ele2 = re.sub("\d+", "", new_periodsite_label)
                r0, b = get_r0_b(
                    ele1,
                    int(target_site.atom_valences[0]),
                    ele2,
                    int(periodsite.atom_valences[0]),
                    "bvmparam.dat",
                )
                if r0 == None:
                    continue
                e = math.e
                bv = e ** ((r0 - dis) / b)
                if bv > 1 / 12:
                    coord += amount
        ele = extract_element_symbol(new_target_site_label)
        rad = get_ionic_radius(ele, target_site.atom_valences[0], coord)
        radii[new_target_site_label] = rad
    return radii

def extract_element_symbol(input_string):
    # 正则表达式模式，匹配元素符号
    pattern = r'([A-Z][a-z]?)'
    match = re.match(pattern, input_string)
    # 如果找到了匹配项，返回该项；否则返回 None
    return match.group(1) if match else None

def get_ioniccoord(structs):
    """
    Get ionic cooordination number,radius,the ion label and distance closest to the ion
    :param structs:by CifFile get structs
    :return:eg:{'Li0': [6, 0.9, ('O5', 2.1058564567272255)],
                'Sc1': [6, 0.885, ('O4', 2.0788469530862503)],
                'Ge2': [4, 0.53, ('O5', 1.7434166083225153)],
                'O3': [4, 1.24, ('Ge2', 1.8066217103408058)],
                'O4': [4, 1.24, ('Ge2', 1.7634523150010546)],
                'O5': [4, 1.24, ('Ge2', 1.7434166083225153)]}
    """
    ioniccoord = {}
    lattice = structs.cell.abc
    type_index_dict = {}  # 保存每个type值第一次出现的索引
    for i, item in enumerate(structs.sites):
        if item.type not in type_index_dict:
            type_index_dict[item.type] = i
    target_sites = []  # 保存结果
    for i, item in enumerate(structs.sites):
        if i == type_index_dict.get(item.type):  # 该type值第一次出现，保存到结果中
            target_sites.append(item)
    for target_site in target_sites:
        new_target_site_label = target_site.label[: target_site.label.rfind("_")]
        coord = 0
        near_ionic = {}
        for i, periodsite in enumerate(structs.sites):
            new_periodsite_label = periodsite.label[: periodsite.label.rfind("_")]
            if new_target_site_label != new_periodsite_label and different_sign(
                periodsite.atom_valences[0], target_site.atom_valences[0]
            ):
                dis, amount = get_period_dis(
                    target_site.coord,
                    periodsite.coord,
                    structs.cell.cell_basis_vectors
                )
                # if dis < 2.0:
                #     coord += amount
                ele1 = re.sub("\d+", "", new_target_site_label)
                ele2 = re.sub("\d+", "", new_periodsite_label)
                r0, b = get_r0_b(
                    ele1,
                    int(target_site.atom_valences[0]),
                    ele2,
                    int(periodsite.atom_valences[0]),
                    "bvmparam.dat",
                )
                e = math.e
                bv = e ** ((r0 - dis) / b)
                if bv > 1 / 12:
                    coord += amount
                    near_ionic[new_periodsite_label] = dis
        nearest_ionic = min(near_ionic.items(), key=lambda x: x[1])
        ele = re.sub("\d+", "", new_target_site_label)
        rad = get_ionic_radius(ele, target_site.atom_valences[0], coord)
        para = [coord, rad, nearest_ionic]
        ioniccoord[new_target_site_label] = para
    return ioniccoord

def get_default_radius(symbol):
    if symbol in _ion_radii:
        first_key = next(iter(_ion_radii[symbol].keys()))  # 获取第一个键
        first_value = _ion_radii[symbol][first_key]         # 获取该键对应的值
        first_subkey = next(iter(first_value.keys()))  # 获取第一个子键
        desired_value = first_value[first_subkey]    # 获取该子键对应的值
        return desired_value
    # 当元素不在香农表中默认半径为1.0
    else:
        return 1.0


if __name__ == "__main__":
    structs = Structure.from_file(
        r"C:\Users\33389\Desktop\materials\LiScGeO4file\LiScGeO4.cif"
    )
    mobiles = [
        (idx, structs.sites[idx])
        for idx in range(len(structs.sites))
        if "Li" in structs.sites[idx].atom_symbols[0]
    ]
    print(mobiles[0][1].coord)
    structs.sites.append(structs.sites[0])
    # type_index_dict = {} # 保存每个type值第一次出现的索引
    # for i, item in enumerate(structs.sites):
    #     if item.type not in type_index_dict:
    #         type_index_dict[item.type] = i
    # target_sites = [] # 保存结果
    # for i, item in enumerate(structs.sites):
    #     if i == type_index_dict.get(item.type): # 该type值第一次出现，保存到结果中
    #         target_sites.append(item)
    # print(target_sites)
    # print(structs.sites[1].coord)
    radius = get_ioniccoord(structs)
    print(radius)
