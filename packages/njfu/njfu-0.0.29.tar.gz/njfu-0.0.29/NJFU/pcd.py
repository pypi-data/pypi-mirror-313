import numpy as np
import os


def STD_TXT(input_txt_dir, output_txt_dir, del_col_list):
    for filename in os.listdir(input_txt_dir):
        # 检查文件扩展名是否为.txt
        if filename.endswith('.txt'):
            # 构建完整的文件路径
            file_path = os.path.join(input_txt_dir, filename)
            data = np.loadtxt(file_path)
            data = np.delete(data, del_col_list, axis=1)
            output = os.path.join(output_txt_dir, 'new_' + filename)
            np.savetxt(output, data, fmt='%.4f')

