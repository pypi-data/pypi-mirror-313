import re


def camel_to_snake(name):
    """将 camelCase 字符串转换为 snake_case"""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def dict_keys_to_snake_case(data):
    """递归地将字典中的所有键从 camelCase 转换为 snake_case"""
    if isinstance(data, dict):
        return {camel_to_snake(k): dict_keys_to_snake_case(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [dict_keys_to_snake_case(item) for item in data]
    else:
        return data


if __name__ == "__main__":
    # 示例用法
    sample_dict = {
        "taskId": 123,
        "metricName": "accuracy",
        "metricType": "SCALAR",
        "histogramRecordList": [
            {"step": 1, "walltime": 162134, "minValue": 0.1, "maxValue": 0.9},
            {"step": 2, "walltime": 162135, "minValue": 0.2, "maxValue": 0.8}
        ]
    }

    converted_dict = dict_keys_to_snake_case(sample_dict)
    print(converted_dict)
    # {'task_id': 123, 'metric_name': 'accuracy', 'metric_type': 'SCALAR', 'histogram_record_list': [{'step': 1, 'walltime': 162134, 'min_value': 0.1, 'max_value': 0.9}, {'step': 2, 'walltime': 162135, 'min_value': 0.2, 'max_value': 0.8}]}