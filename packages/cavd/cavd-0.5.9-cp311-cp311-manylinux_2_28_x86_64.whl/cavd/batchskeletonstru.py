import os
import pandas as pd
from pathlib import Path
from cavd import skeleton_structure_analysis

LOWER_THRESHOLD = {"Li":0.5267, "Na":0.9295, "Mg":0.5513, "Al":0.3447}
UPPER_THRESHOLD = {"Li":0.9857, "Na":1.3961, "Mg":1.0081, "Al":0.7307}
def batchSkeletonStru_toexcel(dir, ions):
    """
    批量处理指定目录下的cif文件,计算并记录相关描述符
    """
    # 检查并创建保存结果的目录
    cifs_path = Path(dir)
    resultsDir = os.path.join(dir, "results")
    os.makedirs(resultsDir, exist_ok=True)
    for i in range(len(ions)):
        ionDir = os.path.join(resultsDir, ions[i])
        os.makedirs(ionDir, exist_ok=True)
        filenames = []
        # 初始化状态和结果存储
        results_list = []

        # 遍历子目录下所有文件，筛选出cif文件
        filenames = list(cifs_path.glob("*.cif"))
        if len(filenames) != 0:
            # 对每个cif文件计算描述符
            for filename in filenames:
                # file_path = os.path.join(dir, filename)
                print(filename)
                try:
                    dims, conn_val = skeleton_structure_analysis(str(filename), ions[i], ionDir,
                    ntol=0.02, rad_flag=True, lower=LOWER_THRESHOLD[ions[i]], upper=UPPER_THRESHOLD[ions[i]], rad_dict=None)
                    Status = "Success!"
                    # 记录结果
                    results_list.append([filename.name, ions[i], dims, conn_val, Status])
                except Exception as e:
                    # 出现异常时，在状态列表中记录异常信息
                    results_list.append((filename.name, ions[i], "None", "None", str(e)))
                    continue
            # 创建Pandas DataFrame并保存为Excel文件
            results_df = pd.DataFrame(results_list, columns=['Filename', 'Migrantion', 'Dimensions', 'Conn_val', 'Status'])
            # 保存到Excel文件
            results_file_path = os.path.join(ionDir, f"com_results_{ions[i]}.xlsx")

            with pd.ExcelWriter(results_file_path) as writer:
                results_df.to_excel(writer, index=False, sheet_name='Results')     

            print(f"{ions[i]} contained file compute completed!")
        else:
            continue
            #print(f"No CIF files found in {cifs_path}")
    
    print("All File compute completed!")
    
def batchSkeletonStrufloder_toexcel(floder_dir, ions = ["Li", "Na", "Mg", "Al"]):
    """
    批量处理指定文件夹下的cif文件,计算并记录相关描述符
    """
    folder_path = Path(floder_dir)
    # 使用 rglob('*') 查找所有文件和文件夹，过滤出文件夹
    subdirectories = [subdir for subdir in folder_path.rglob('*') if subdir.is_dir()]
    if folder_path.is_dir():
        subdirectories.append(folder_path)
    for subdirectory in subdirectories:
        batchSkeletonStru_toexcel(subdirectory, ions)
    return 0

if __name__ == "__main__":
    ions = ["Li", "Na", "Mg", "Al"]
    batchSkeletonStrufloder_toexcel(r"D:\warehouses\ciffile\batchtest\5\4", ions)
    # dir = "./cifs/skeleton"
    # batchSkeletonStru_toexcel(dir, ions)