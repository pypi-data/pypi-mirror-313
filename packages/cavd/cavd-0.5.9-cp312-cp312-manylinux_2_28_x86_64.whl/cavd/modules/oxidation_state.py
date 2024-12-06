import re
import os
from collections import OrderedDict
from mgtoolbox_kernel.kernel.structure import Structure

def get_period_oxistate():
    module_dir = os.path.dirname(os.path.abspath(__file__))
    # 创建一个空字典用于存储元素和化合价
    element_valence = {}

    # 打开文件并逐行读取内容
    with open(os.path.join(module_dir, "bvmparam.dat"), "r") as file:
        next(file)  # 跳过文件的第一行（标题行）
        for line in file:
            line = line.strip()  # 去掉行首行尾的空格或换行符
            elements = line.split("\t")  # 使用制表符分割行中的元素和化合价
            element1 = elements[0].lstrip('#')  # 提取元素
            valence1 = int(elements[1])  # 提取化合价并转换为整数
            element2 = elements[2]  # 提取元素
            valence2 = int(elements[3])  # 提取化合价并转换为整数
            # 将元素和化合价添加到字典中
            if element1 in element_valence:
                if valence1 not in element_valence[element1]:
                    element_valence[element1].append(valence1)
            else:
                element_valence[element1] = [valence1]
            # 将元素和化合价添加到字典中
            if element2 in element_valence:
                if valence2 not in element_valence[element2]:
                    element_valence[element2].append(valence2)
            else:
                element_valence[element2] = [valence2]
    return element_valence


def get_chemdict(chem_sum):
    # 创建一个默认值为0的字典
    element_counts = OrderedDict()

    # 使用正则表达式解析化学式字符串
    pattern = r"([A-Z][a-z]*)(\d*)"
    matches = re.findall(pattern, chem_sum)

    # 遍历匹配结果
    for match in matches:
        element = match[0]
        count = int(match[1]) if match[1] else 1
        element_counts[element] = element_counts.get(element, 0) + count
    return element_counts


def find_combinations(lists, current_index, current_sum, current_combination, results):
    if current_index == len(lists):
        if current_sum == 0:
            results.append(current_combination.copy())
        return

    current_list = lists[current_index]
    for num in current_list:
        current_combination.append(num)
        find_combinations(
            lists, current_index + 1, current_sum + num, current_combination, results
        )
        current_combination.pop()


def find_combination_sum_zero(lists):
    results = []
    find_combinations(lists, 0, 0, [], results)
    return results


def get_oxstate(ciffile):
    struct = Structure.from_file(ciffile)
    element_valences = get_period_oxistate()
    eles_valencelist = []
    chemsum = OrderedDict()
    # 获取化学符号列表和对应的原子个数
    for site in struct.sites:
        symbol = site.atom_symbols[0]
        if symbol not in chemsum:
            chemsum[symbol] = 0
        chemsum[symbol] += 1
    for element, amount in chemsum.items():
        ele_val = [amount * i for i in element_valences[element]]
        eles_valencelist.append(ele_val)
    results = find_combination_sum_zero(eles_valencelist)
    all_posscombination = []
    for oxstatesum in results:
        single_combination = {}
        for i, element in enumerate(chemsum.keys()):
            ele_valance = oxstatesum[i] / chemsum[element]
            single_combination[element] = ele_valance
        all_posscombination.append(single_combination)
    if len(all_posscombination) == 1:
        return all_posscombination[0]

def get_oxstate_from_struct(struct):
    element_valences = get_period_oxistate()
    if struct.is_ordered:
        eles_valencelist = []
        chemsum = OrderedDict()
        # 获取化学符号列表和对应的原子个数
        for site in struct.sites:
            symbol = site.atom_symbols[0]
            if symbol not in chemsum:
                chemsum[symbol] = 0
            chemsum[symbol] += 1
        for element, amount in chemsum.items():
            ele_val = [amount * i for i in element_valences[element]]
            eles_valencelist.append(ele_val)
        results = find_combination_sum_zero(eles_valencelist)
        all_posscombination = []
        for oxstatesum in results:
            single_combination = {}
            for i, element in enumerate(chemsum.keys()):
                ele_valance = oxstatesum[i] / chemsum[element]
                single_combination[element] = ele_valance
            all_posscombination.append(single_combination)
        if len(all_posscombination) == 1:
            return all_posscombination[0]
        # 当晶体结构电荷不平衡时，返回None
        else:
            return None
    else:
        # 无序结构
        return None


if __name__ == "__main__":
    s = get_oxstate(r"D:\warehouses\ciffile\oxidation\icsd_062481.cif")
