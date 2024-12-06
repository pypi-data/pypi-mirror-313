"""


"""
import argparse
from pathlib import Path
from cavd import crystal_structure_analysis
from cavd.batchskeletonstru import batchSkeletonStrufloder_toexcel

def main():
    """
    主函数入口
    """
    # 创建一个参数解析器，用于解析命令行参数
    parser = argparse.ArgumentParser(description='cavd 晶体结构离子输运特征计算分析程序')
    parser.add_argument('-c',
                        '--calculation_type',
                        dest='cal_type',
                        type=str,
                        default='cavd',
                        choices=['cavd', 'batch_skeletonstru'],
                        required=True,
                        help='计算类型选择')
    batch_skeletonstru = parser.add_argument_group('batch_skeletonstru')
    batch_skeletonstru.add_argument('-dir',
                                    '--input_dir',
                                    dest='input_dir',
                                    type=str,
                                    default='./',
                                    help='输入目录')
    
    cavd = parser.add_argument_group('cavd')
    cavd.add_argument('-s',
                        '--structure_file',
                        dest='struct_file',
                        type=str,
                        help='结构文件名(cif格式)')

    # 添加迁移离子类型参数，有默认值
    parser.add_argument('-i',
                        '--move_ion',
                        dest='ion',
                        type=str,
                        default='Li',
                        help='迁移离子类型')

    # 添加计算容限参数，有默认值
    cavd.add_argument('--ntol',
                      dest='ntol',
                      type=float,
                      default=0.02,
                      help='计算容限')

    # 添加几何分析时是否考虑离子半径的参数，有默认值
    cavd.add_argument('--no_radius_flag',
                      dest='no_rad_flag',
                      action='store_false',
                      default=False,
                      help='几何分析时是否考虑离子半径')

    # 添加通道大小下限值参数，有默认值
    cavd.add_argument('-l',
                      '--lower',
                      dest='lower',
                      type=float,
                      default=0.5,
                      help='通道大小下限值(单位埃)')

    # 添加通道大小上限值参数，有默认值
    cavd.add_argument('-u',
                      '--upper',
                      dest='upper',
                      type=float,
                      default=1.0,
                      help='通道大小上限值(单位埃)')

    # 以下代码行被注释掉，因此不需要为其生成注释
    # cavd.add_argument('-rad_dict',
    #                   '--rad_dict',
    #                   type=str,
    #                   default=None,
    #                   dest='rad_dict',
    #                   help='离子半径字典')

    # 解析命令行参数
    args = parser.parse_args()

    # 根据计算类型调用相应的计算函数
    if args.cal_type == 'cavd':
        dims, conn_val = crystal_structure_analysis(args.struct_file,
                              migrant=args.ion,
                              ntol=args.ntol,
                              rad_flag=not args.no_rad_flag,
                              lower=args.lower,
                              upper=args.upper,
                              rad_dict=None)
        print(conn_val)
    if args.cal_type == 'batch_skeletonstru':
        batchSkeletonStrufloder_toexcel(args.input_dir)


if __name__ == "__main__":
    main()
