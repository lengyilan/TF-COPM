# -*- codeing = utf-8 -*-
# @Time : 2023/6/2 14:56
# @Author : 王赓
# @File : Log Partitioning.py
# @Software : PyCharm

from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_export_factory

# 读取事件日志
log_path = "path/to/your/log.xes"
log = xes_import_factory.apply(log_path)

# 切片方式划分子日志
sorted_log = sorted(log, key=lambda x: x["time:timestamp"])  # 按时间戳排序
log_length = len(sorted_log)
split_index = log_length // 3  # 划分索引位置

sub_logs = []
sub_logs.append(sorted_log[:split_index])  # 第一个子日志
sub_logs.append(sorted_log[split_index:2*split_index])  # 第二个子日志
sub_logs.append(sorted_log[2*split_index:])  # 第三个子日志

# 输出子日志
for i, sub_log in enumerate(sub_logs):
    sub_log_path = f"path/to/output/sub_log_{i+1}.xes"
    xes_export_factory.apply(sub_log, sub_log_path)

'''
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_export_factory

# 读取事件日志
log_path = "path/to/your/log.xes"
log = xes_import_factory.apply(log_path)

# 按时间戳排序
sorted_log = sorted(log, key=lambda x: x["time:timestamp"])

# 循环分配给三个组织
org1_log = []
org2_log = []
org3_log = []

for i, event in enumerate(sorted_log):
    if i % 3 == 0:
        org1_log.append(event)  # 组织1
    elif i % 3 == 1:
        org2_log.append(event)  # 组织2
    else:
        org3_log.append(event)  # 组织3

# 输出子日志
xes_export_factory.apply(org1_log, "path/to/output/org1_log.xes")
xes_export_factory.apply(org2_log, "path/to/output/org2_log.xes")
xes_export_factory.apply(org3_log, "path/to/output/org3_log.xes")

'''
