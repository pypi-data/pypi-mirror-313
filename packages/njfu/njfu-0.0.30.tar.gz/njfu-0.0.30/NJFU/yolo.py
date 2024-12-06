import os
import random
import cv2
import argparse
import xml.etree.ElementTree as ET
import numpy as np
from .utils import DataAugmentForObjectDetection, ToolHelper, show_pic
import shutil


def TXT2XML(input_txt_dir, output_xml_dir, image_dir, class_txt, pic_type):
    if not os.path.exists(output_xml_dir):
        os.makedirs(output_xml_dir)
    # 获取txt文件的目录列表
    txt_files = os.listdir(input_txt_dir)
    # 获取图像的目录列表
    image_files = os.listdir(image_dir)
    image_infos = []
    for txt_file in txt_files:
        flag = 0
        file_name, file_ext = os.path.splitext(txt_file)
        for image_file in image_files:
            images = []
            image_name, image_ext = os.path.splitext(image_file)
            if image_ext == pic_type:
                # 判断图像名是否与txt文件名相同
                if image_name == file_name:
                    flag = 1
                    images.append(image_file)
                    # 读取txt文件中的标注信息
                    with open(os.path.join(input_txt_dir, txt_file), 'r') as f:
                        bboxes = []
                        for line in f.readlines():
                            bbox_id, x_center, y_center, width, height = line.strip().split()
                            x_center = float(x_center)  # 相对坐标
                            y_center = float(y_center)  # 相对坐标
                            width = float(width)  # 相对坐标
                            height = float(height)  # 相对坐标

                            bbox = (bbox_id, x_center, y_center, width, height)
                            bboxes.append(bbox)
                        images.append(bboxes)
                    image_infos.append(images)

            else:
                print('The image type is not correct')

        if flag == 0:
            print(file_name, ' not found files')

    # 获取标注框的类别列表
    class_names = []
    with open(class_txt, 'r') as classes:
        for class_name in classes.readlines():
            class_names.append(class_name.strip())

    # 遍历每个图像文件，获取图像的高度和宽度，并将标注信息写入XML文件
    for image_info in image_infos:
        image_file = image_info[0]
        image_name, image_ext = os.path.splitext(image_file)
        image_path = os.path.join(image_dir, image_file)
        img = cv2.imread(image_path)
        image_height, image_width, num_channels = img.shape[:3]  # 获取图片的高度、宽度和通道数

        # 创建XML文件并写入标注信息
        with open(os.path.join(output_xml_dir, image_name + '.xml'), 'a') as f:
            f.write('<annotation>\n')
            # 图像位置信息
            f.write('\t<filename>{}</filename>\n'.format(image_file))
            f.write('\t<path>{}</path>\n'.format(image_path))
            # 图像尺寸信息
            f.write('\t<size>\n')
            f.write('\t\t<width>{}</width>\n\t\t<height>{}</height>\n\t\t<depth>{}</depth>\n'.format(image_width, image_height, num_channels))
            f.write('\t</size>\n')
            # 图像类别、坐标信息
            bboxes = image_info[1]
            for bbox in bboxes:
                bbox_id, x_center, y_center, width, height = bbox
                xmin = (x_center * image_width) - (width * image_width) / 2  # 计算标注框左上角x坐标值
                ymin = (y_center * image_height) - (height * image_height) / 2  # 计算标注框左上角y坐标值
                xmax = (x_center * image_width) + (width * image_width) / 2  # 计算标注框右下角x坐标值
                ymax = (y_center * image_height) + (height * image_height) / 2  # 计算标注框右下角y坐标值

                f.write('\t<object>\n')
                f.write('\t\t<name>{}</name>\n'.format(class_names[int(bbox_id)].strip()))
                f.write('\t\t<pose>Unspecified</pose>\n')
                f.write('\t\t<truncated>0</truncated>\n')
                f.write('\t\t<difficult>0</difficult>\n')
                f.write('\t\t<bndbox>\n')
                f.write('\t\t\t<xmin>{}</xmin>\n\t\t\t<ymin>{}</ymin>\n\t\t\t<xmax>{}</xmax>\n\t\t\t<ymax>{}</ymax>\n'.format(int(xmin), int(ymin),
                                                                                                                              int(xmax), int(ymax)))
                f.write('\t\t</bndbox>\n')

                f.write('\t</object>\n')
            f.write('</annotation>')


def XML2TXT(input_dir, output_dir, class_txt):
    # 获取所有XML文件列表
    xml_files = os.listdir(input_dir)
    # 获取标注框的类别列表
    class_names = []
    with open(class_txt, 'r') as classes:
        for class_name in classes.readlines():
            class_names.append(class_name.split())

    # 遍历每个XML文件
    for xml_file in xml_files:
        # 获取文件名和扩展名
        file_name, file_ext = os.path.splitext(xml_file)
        # 确保是XML文件
        if file_ext == '.xml':
            # 解析XML文件并获取标注信息
            tree = ET.parse(os.path.join(input_dir, xml_file))
            root = tree.getroot()

            # 获取图像的最大宽度和高度
            max_width = float(root.find('size').find('width').text)
            max_height = float(root.find('size').find('height').text)

            # 获取标注框的坐标信息
            bndbox_coords = []
            for obj in root.findall('object'):
                bbox_type = obj.find('name').text
                type_id = class_name.index(bbox_type)
                bndbox = obj.find('bndbox')
                xmin = float(bndbox.find('xmin').text)
                ymin = float(bndbox.find('ymin').text)
                xmax = float(bndbox.find('xmax').text)
                ymax = float(bndbox.find('ymax').text)
                bndbox_coords.append((type_id, xmin, ymin, xmax, ymax))

            # 计算YOLO所需的格式并写入输出文件
            with open(os.path.join(output_dir, file_name + '.txt'), 'w') as f:
                for coords in bndbox_coords:
                    type_id, xmin, ymin, xmax, ymax = coords
                    x_center = (xmin + xmax) / 2 / max_width  # x_center字段计算，相对坐标
                    y_center = (ymin + ymax) / 2 / max_height  # y_center字段计算，相对坐标
                    width = (xmax - xmin) / max_width  # width字段（相对宽）计算
                    height = (ymax - ymin) / max_height  # height字段（相对高）计算
                    f.write('{} {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(type_id, x_center, y_center, width, height))


def extend(num, source_img_path, source_xml_path, save_img_path, save_xml_path):

    need_aug_num = num  # 每张图片需要增强的次数

    is_endwidth_dot = True  # 文件是否以.jpg或者png结尾

    dataAug = DataAugmentForObjectDetection()  # 数据增强工具类

    toolhelper = ToolHelper()  # 工具

    # 获取相关参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_img_path', type=str, default=source_img_path)
    parser.add_argument('--source_xml_path', type=str, default=source_xml_path)
    parser.add_argument('--save_img_path', type=str, default=save_img_path)
    parser.add_argument('--save_xml_path', type=str, default=save_xml_path)
    args = parser.parse_args()
    source_img_path = args.source_img_path  # 图片原始位置
    source_xml_path = args.source_xml_path  # xml的原始位置

    save_img_path = args.save_img_path  # 图片增强结果保存文件
    save_xml_path = args.save_xml_path  # xml增强结果保存文件

    # 如果保存文件夹不存在就创建
    if not os.path.exists(save_img_path):
        os.mkdir(save_img_path)

    if not os.path.exists(save_xml_path):
        os.mkdir(save_xml_path)

    for parent, _, files in os.walk(source_img_path):
        files.sort()
        for file in files:
            cnt = 0
            pic_path = os.path.join(parent, file)
            xml_path = os.path.join(source_xml_path, file[:-4] + '.xml')
            values = toolhelper.parse_xml(xml_path)  # 解析得到box信息，格式为[[x_min,y_min,x_max,y_max,name]]
            coords = [v[:4] for v in values]  # 得到框
            labels = [v[-1] for v in values]  # 对象的标签

            # 如果图片是有后缀的
            if is_endwidth_dot:
                # 找到文件的最后名字
                dot_index = file.rfind('.')
                _file_prefix = file[:dot_index]  # 文件名的前缀
                _file_suffix = file[dot_index:]  # 文件名的后缀
            img = cv2.imread(pic_path)

            # show_pic(img, coords)  # 显示原图
            while cnt < need_aug_num:  # 继续增强
                auged_img, auged_bboxes = dataAug.dataAugment(img, coords)
                auged_bboxes_int = np.array(auged_bboxes).astype(np.int32)
                height, width, channel = auged_img.shape  # 得到图片的属性
                img_name = '{}_{}{}'.format(_file_prefix, cnt + 1, _file_suffix)  # 图片保存的信息
                toolhelper.save_img(img_name, save_img_path,
                                    auged_img)  # 保存增强图片

                toolhelper.save_xml('{}_{}.xml'.format(_file_prefix, cnt + 1),
                                    save_xml_path, (save_img_path, img_name), height, width, channel,
                                    (labels, auged_bboxes_int))  # 保存xml文件
                # show_pic(auged_img, auged_bboxes)  # 强化后的图
                # print(img_name)
                cnt += 1  # 继续增强下一张

    print('Augmentation completed!')


def SplitDataset(train_per, val_per, test_per, img_path, img_type, xml_path, txt_save_path):

    total_xml = os.listdir(xml_path)

    num = len(total_xml)
    ID = range(num)
    train = random.sample(ID, int(num * train_per))
    val = random.sample(ID, int(num * val_per))

    train_file = open(txt_save_path + '/train.txt', 'w')
    val_file = open(txt_save_path + '/val.txt', 'w')
    test_file = open(txt_save_path + '/test.txt', 'w')

    for i in ID:
        name = total_xml[i][:-4]
        if i in train:
            train_file.write(img_path + '/%s' % name + img_type + '\n')

        elif i in val:
            val_file.write(img_path + '/%s' % name + img_type + '\n')

        else:
            test_file.write(img_path + '/%s' % name + img_type + '\n')

    train_file.close()
    val_file.close()
    test_file.close()

    print('Split completed!')


def copy_files(src_dir, dst_dir, filenames, extension):
    os.makedirs(dst_dir, exist_ok=True)
    missing_files = 0
    for filename in filenames:
        src_path = os.path.join(src_dir, filename + extension)
        dst_path = os.path.join(dst_dir, filename + extension)

        # Check if the file exists before copying
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
        else:
            print(f"Warning: File not found for {filename}")
            missing_files += 1

    return missing_files


def split_and_copy_dataset(image_dir, label_dir, output_dir, img_type, train_ratio=0.7, valid_ratio=0.15, test_ratio=0.15):
    # 获取所有图像文件的文件名（不包括文件扩展名）
    image_filenames = [os.path.splitext(f)[0] for f in os.listdir(image_dir)]

    # 随机打乱文件名列表
    random.shuffle(image_filenames)

    # 计算训练集、验证集和测试集的数量
    total_count = len(image_filenames)
    train_count = int(total_count * train_ratio)
    valid_count = int(total_count * valid_ratio)
    test_count = total_count - train_count - valid_count

    # 定义输出文件夹路径
    train_image_dir = os.path.join(output_dir, 'train', 'images')
    train_label_dir = os.path.join(output_dir, 'train', 'labels')
    valid_image_dir = os.path.join(output_dir, 'valid', 'images')
    valid_label_dir = os.path.join(output_dir, 'valid', 'labels')
    test_image_dir = os.path.join(output_dir, 'test', 'images')
    test_label_dir = os.path.join(output_dir, 'test', 'labels')

    # 复制图像和标签文件到对应的文件夹
    train_missing_files = copy_files(image_dir, train_image_dir, image_filenames[:train_count], img_type)
    train_missing_files += copy_files(label_dir, train_label_dir, image_filenames[:train_count], '.txt')

    valid_missing_files = copy_files(image_dir, valid_image_dir, image_filenames[train_count:train_count + valid_count], img_type)
    valid_missing_files += copy_files(label_dir, valid_label_dir, image_filenames[train_count:train_count + valid_count], '.txt')

    test_missing_files = copy_files(image_dir, test_image_dir, image_filenames[train_count + valid_count:], img_type)
    test_missing_files += copy_files(label_dir, test_label_dir, image_filenames[train_count + valid_count:], '.txt')

    # Print the count of each dataset
    print(f"Train dataset count: {train_count}, Missing files: {train_missing_files}")
    print(f"Validation dataset count: {valid_count}, Missing files: {valid_missing_files}")
    print(f"Test dataset count: {test_count}, Missing files: {test_missing_files}")

