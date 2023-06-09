# -*- codeing = utf-8 -*-
# @Time : 2023/6/2 12:32
# @Author : 王赓
# @File : Privacy Authorization.py
# @Software : PyCharm

from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_export_factory
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.petri.exporter import exporter as pnml_exporter
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.objects.log.util import get_log_trace_attributes

# 读取事件日志
log_path = "path/to/your/log.xes"
log = xes_import_factory.apply(log_path)

# 定义敏感属性
sensitive_attribute = "your_sensitive_attribute"

# 提取敏感活动
sensitive_activities = set()
for trace in log:
    if sensitive_attribute in trace.attributes:
        sensitive_activities.add(trace.attributes[sensitive_attribute])

net, initial_marking, final_marking = inductive_miner.apply(log)

# 遍历所有敏感活动的前继和后继节点
privacy_authorizations = {}
for activity in sensitive_activities:
    predecessors = net.predecessors(activity)
    successors = net.successors(activity)
    for predecessor in predecessors:
        if predecessor != activity:
            if not net.get_place(predecessor).name.startswith("org"):
                privacy_authorizations[(predecessor, activity)] = "禁止访问"
    for successor in successors:
        if successor != activity:
            if not net.get_place(successor).name.startswith("org"):
                privacy_authorizations[(activity, successor)] = "禁止访问"

# 制作隐私授权列表
for activity in net.nodes:
    if not net.get_place(activity).name.startswith("org"):
        privacy_authorizations[(activity, activity)] = "允许访问"

# 输出隐私授权列表
output_file = "path/to/privacy_authorizations.csv"
with open(output_file, "w") as f:
    f.write("活动1,活动2,授权\n")
    for (activity1, activity2), authorization in privacy_authorizations.items():
        f.write(f"{activity1},{activity2},{authorization}\n")
