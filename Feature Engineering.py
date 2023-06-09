# -*- codeing = utf-8 -*-
# @Time : 2023/6/2 12:29
# @Author : 王赓
# @File : Feature Engineering.py
# @Software : PyCharm

import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer
from category_encoders import OrdinalEncoder

# 导入事件日志
log = xes_importer.apply("path_to_your_log_file.xes")

# 提取活动
activities = set()
for trace in log:
    for event in trace:
        activities.add(event["concept:name"])

# 创建混淆编码器
encoder = OrdinalEncoder(cols=["activity"])
encoder.fit(pd.DataFrame({"activity": list(activities)}))

# 初始化频率矩阵和时间矩阵
frequency_matrix = pd.DataFrame(index=activities, columns=activities).fillna(0)
time_matrix = pd.DataFrame(index=activities, columns=activities).fillna(0)

# 遍历日志并更新频率矩阵和时间矩阵
for trace in log:
    previous_event = None
    for event in trace:
        activity = event["concept:name"]
        encoded_activity = encoder.transform(pd.DataFrame({"activity": [activity]}))["activity"].values[0]

        if previous_event is not None:
            previous_activity = previous_event["concept:name"]
            encoded_previous_activity = encoder.transform(pd.DataFrame({"activity": [previous_activity]}))["activity"].values[0]

            # 更新频率矩阵
            frequency_matrix.at[encoded_previous_activity, encoded_activity] += 1

            # 更新时间矩阵
            time_diff = event["time:timestamp"] - previous_event["time:timestamp"]
            time_matrix.at[encoded_previous_activity, encoded_activity] += time_diff.total_seconds()

        previous_event = event

# 打印频率矩阵和时间矩阵
print("Frequency Matrix:")
print(frequency_matrix)
print("\nTime Matrix:")
print(time_matrix)