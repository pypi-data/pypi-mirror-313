"""
    Analyze the recovery rate of target ions.

    Update date：20191120
    Author：YAJ
    School of Computer Engineering and Science, ShangHai University 

"""
import numpy as np
from scipy.spatial.ckdtree import cKDTree

period_list = [[0.0, 0.0, 0.0],
       [0.0, 0.0, 1.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0], [0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0],
       [0.0, 1.0, 1.0], [0.0, 1.0, -1.0], [0.0, -1.0, 1.0], [0.0, -1.0, -1.0],
       [1.0, 0.0, 1.0], [1.0, 0.0, -1.0], [-1.0, 0.0, 1.0], [-1.0, 0.0, -1.0],
       [1.0, 1.0, 0.0], [1.0, -1.0, 0.0], [-1.0, 1.0, 0.0], [-1.0, -1.0, 0.0],
       [1.0, 1.0, 1.0], [1.0, 1.0, -1.0], [1.0, -1.0, 1.0], [1.0, -1.0, -1.0],
       [-1.0, 1.0, 1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0], [-1.0, -1.0, -1.0]]


def get_period_dis(frac_site1, frac_site2, lattice):
    """
    Considering the periodicity of crystals to obtain the distance
    between two points within the crystal.
    :param frac_site1: fractional coordinates of site frac_site1,such as[0.5, 0.5, 0.5]
    :param frac_site2: fractional coordinates of site frac_site2
    :param lattice: lattice parameters of crystals
    :return: the shortest distance between two sites and
    the number of ions with the shortest distance between them
    """
    lattice_matrix = np.array([[lattice[0], 0.0, 0.0],
                               [0.0, lattice[1], 0.0],
                               [0.0, 0.0, lattice[2]]])
    actual_site1 = np.dot(lattice_matrix, frac_site1)
    frac_site2 = np.array(frac_site2)
    dis_list = []
    for i in period_list:
        period_i = np.array(i)
        temp_frac_site2 = period_i + frac_site2
        temp_actual_site2 = np.dot(lattice_matrix, temp_frac_site2)
        temp_dis = np.linalg.norm(temp_actual_site2 - actual_site1)
        dis_list.append(temp_dis)
    sorted_list = sorted(dis_list)
    min_dis = sorted_list[0]
    return min_dis, sorted_list.count(min_dis)

# Return the site type.
def get_point_tag(id, pts_len):
    vexs_len = pts_len[0]
    bts_len = pts_len[1]
    fcs_len = pts_len[2]

    if id < vexs_len:
        return "It" + str(id)
    elif id < vexs_len + bts_len:
        return "Bn" + str(id - vexs_len)
    elif id < vexs_len + bts_len + fcs_len:
        return "Fc" + str(id - vexs_len - bts_len)
    else:
        raise IndexError

def get_point_tag_onlyVertex(id, pts_len):
    vexs_len = pts_len[0]
    if id < vexs_len:
        return "It" + str(id)
    else:
        raise IndexError

# Calculate the recovery rates of the lattice sites of mobile ions by KD-Tree.
def rediscovery_kdTree(stru, migrate, vorosites, threshold = 0.5):
    recover_labels = []
    recover_state = {}
    migrate_mindis = {}
    
    migrate_pos_frac = np.around(np.array([site.coord for site in stru.sites if migrate in site.atom_symbols[0]], ndmin=2), 3)
    migrate_pos_frac %= 1.0
    migrate_pos_frac %= 1.0
    labels = [site.label[:site.label.rfind('_')] for site in stru.sites if migrate in site.atom_symbols[0]]

    points = np.around(np.array(vorosites[0] + vorosites[1] + vorosites[2], ndmin=2), 3)
    points %= 1.0
    points %= 1.0
    vorositesKdTree = cKDTree(points)
    min_dis,min_ids = vorositesKdTree.query(migrate_pos_frac,k=1)

    for idx in range(len(min_ids)):
        if labels[idx] in recover_labels:
            continue
        dis_st1_st2, amout = get_period_dis(migrate_pos_frac[idx], points[min_ids[idx]], stru.cell.abc)
        pts_len = [len(vorosites[0]), len(vorosites[1]), len(vorosites[2])]
        pt_tag = get_point_tag(min_ids[idx], pts_len)
        migrate_mindis[str(labels[idx])] = (pt_tag, dis_st1_st2)
        if dis_st1_st2 <= threshold:
            recover_state[str(labels[idx])] = pt_tag
            recover_labels.append(labels[idx])
        else:
            recover_state[str(labels[idx])] = None

    recover_rate = len(recover_labels) / len(np.unique(labels))
    return recover_rate, recover_state, migrate_mindis


"""
    Find the Interstice, Bottleneck or Face Center that corresponding to the lattice position of mobile ions.
    Algorithm:
        1. Use KD-tree to find the nearest sites (Interstice, Bottleneck or Face Center) of 
        the specified lattice sites of mobile ion.
        2. Record the distance between them. If the distance is smaller than the size of 
        the nearest sites (Interstice, Bottleneck or Face Center), current mobile ions position is considered to be recoveried.
    Return:
        Recovery rate, recovery status of mobile ions, nearest sites (Interstice, Bottleneck or Face Center) and the  distance between them.
"""
def rediscovery_byRad_kdTree(stru, migrate, vorosites, vororad, threshold = 0.5):
    """
    使用kd树算法和半径信息来识别和恢复结构中的特定迁移状态。

    :param stru: 晶体结构。
    :param migrate: 迁移离子的类型。
    :param vorosites: 间隙位点列表。
    :param vororad: 间隙位点对应的半径。
    :param threshold: 判断两个点是否接近的阈值。
    :return: 恢复率，恢复状态字典，和离迁移离子的最近间隙点标签和距离信息。
    """
    recover_labels = []
    recover_state = {}
    migrate_mindis = {}

    migrate_pos_frac = np.around(np.array([site.coord for site in stru.sites if migrate in site.atom_symbols[0]], ndmin=2), 3)
    migrate_pos_frac %= 1.0
    migrate_pos_frac %= 1.0

    migrate_labels = [site.label[:site.label.rfind('_')] for site in stru.sites if migrate in site.atom_symbols[0]]

    points = np.around(np.array(vorosites[0] + vorosites[1] + vorosites[2], ndmin=2), 3)
    points_rad = np.array(vororad[0] + vororad[1] + vororad[2])

    points %= 1.0
    points %= 1.0

    vorositesKdTree = cKDTree(points)
    min_dis,min_ids = vorositesKdTree.query(migrate_pos_frac,k=1)

    pts_len = [len(vorosites[0]), len(vorosites[1]), len(vorosites[2])]
    for idx in range(len(migrate_labels)):
        if migrate_labels[idx] in recover_labels:
            continue
        dis_st1_st2, amout = get_period_dis(migrate_pos_frac[idx], points[min_ids[idx]], stru.cell.abc)
        pt_tag = get_point_tag(min_ids[idx], pts_len)
        pt_rad = points_rad[min_ids[idx]]
        migrate_mindis[str(migrate_labels[idx])] = (pt_tag, pt_rad, dis_st1_st2)

        # if dis_st1_st2 <= threshold or dis_st1_st2 <= pt_rad:
        if dis_st1_st2 <= threshold:
            recover_state[str(migrate_labels[idx])] = pt_tag
            recover_labels.append(migrate_labels[idx])
        else:
            recover_state[str(migrate_labels[idx])] = None

    recover_rate = len(recover_labels) / len(np.unique(migrate_labels))
    return recover_rate, recover_state, migrate_mindis

def rediscovery_byRad_kdTree_onlyVertex(stru, migrate, vorosites, vororad, threshold = 0.5):
    recover_labels = []
    recover_state = {}
    migrate_mindis = {}

    migrate_pos_frac = np.around(np.array([site.coord for site in stru.sites if migrate in site.atom_symbols[0]], ndmin=2), 3)
    migrate_pos_frac %= 1.0
    migrate_pos_frac %= 1.0
    expand_pos_frac = migrate_pos_frac
    
    # expand the migrant sites to 3*3*3
    for a in range(-1, 2):
        for b in range(-1, 2):
            for c in range(-1, 2):
                if a==b==c==0:
                    continue
                else:
                    expand_pos_frac = np.concatenate((expand_pos_frac,migrate_pos_frac+np.array([a,b,c])),axis=0)

    migrate_labels = [site.label[:site.label.rfind('_')] for site in stru.sites if migrate in site.atom_symbols[0]]
    
    points = np.around(np.array(vorosites[0], ndmin=2), 3)
    points_rad = np.array(vororad[0])
    
    points %= 1.0
    points %= 1.0

    vorositesKdTree = cKDTree(points)
    min_dis,min_ids = vorositesKdTree.query(migrate_pos_frac,k=1)

    pts_len = [len(vorosites[0])]
    for idx in range(len(migrate_labels)):
        if migrate_labels[idx] in recover_labels:
            continue
        dis_st1_st2, amout = get_period_dis(migrate_pos_frac[idx], points[min_ids[idx]], stru.cell.abc)
        pt_tag = get_point_tag_onlyVertex(min_ids[idx], pts_len)
        pt_rad = points_rad[min_ids[idx]]
        migrate_mindis[str(migrate_labels[idx])] = (pt_tag, pt_rad, dis_st1_st2)
        
        # if dis_st1_st2 <= threshold or dis_st1_st2 <= pt_rad:
        if dis_st1_st2 <= threshold:
            recover_state[str(migrate_labels[idx])] = pt_tag
            recover_labels.append(migrate_labels[idx])
        else:
            recover_state[str(migrate_labels[idx])] = None

    recover_rate = len(recover_labels) / len(np.unique(migrate_labels))
    return recover_rate, recover_state, migrate_mindis