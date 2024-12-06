import json
import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


def visdom_json_to_csv(input_json_path, output_csv_path, id_list=['reward', 'repeat', 'step', 'dangerous', 'loss', 'repeat_ratio', 'cover_ratio']):
    if not os.path.exists(output_csv_path):
        os.makedirs(output_csv_path)

    for file_name in os.listdir(input_json_path):
        if not file_name.endswith('.json'):
            continue

        input_file = os.path.join(input_json_path, file_name)
        output_file = os.path.join(output_csv_path, file_name.replace('json', 'csv'))

        try:
            with open(input_file, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            logging.error(f"无法解析JSON文件: {file_name}")
            continue

        all_data = {}
        x_data = None

        for window_id, window_data in data.items():
            for id in id_list:
                if id not in window_data:
                    logging.warning(f"{file_name} {window_id}中没有找到 {id} 数据")
                    continue

                content = window_data[id].get('content', {})
                if 'data' not in content:
                    logging.warning(f"{file_name} {window_id}中没有找到 {id} 的data数据")
                    continue

                data_content = content['data'][0]

                # 只读取一次x数据
                if x_data is None and 'x' in data_content:
                    x_data = pd.DataFrame(data_content['x'], columns=['x'])

                if 'y' in data_content:
                    y = pd.DataFrame(data_content['y'], columns=[id])
                    all_data[id] = y

        if all_data and x_data is not None:
            # 将x数据添加到结果的开始
            result = pd.concat([x_data] + list(all_data.values()), axis=1)

            # 确保所有的id都在结果中，如果缺少某个id，添加一列NaN
            for id in id_list:
                if id not in result.columns:
                    result[id] = pd.NA

            # 重新排列列以匹配id_list的顺序
            result = result[['x'] + id_list]

            # 保存CSV，包含表头
            result.to_csv(output_file, index=False)
            logging.info(f"数据已成功保存到 {output_file}")
        else:
            logging.warning(f"没有找到可以保存的数据: {file_name}")
