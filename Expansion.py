# -*- codeing = utf-8 -*-
# @Time : 2023/6/2 12:32
# @Author : 王赓
# @File : Expansion.py
# @Software : PyCharm

from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.algo.discovery.heuristics import factory as heuristics_miner
from pm4py.algo.conformance.alignments import factory as alignments_factory
from pm4py.objects.petri.exporter import exporter as pnml_exporter
from pm4py.algo.conformance.alignments import algorithm as alignments_algorithm
from pm4py.objects.dfg.exporter import exporter as dfg_exporter
from pm4py.objects.dfg.utils import dfg_utils
from pm4py.objects.dfg.utils import dfg_utils
from pm4py.objects.dfg import factory as dfg_factory
from pm4py.objects.log.util import get_log_trace_attributes

# 读取隐私授权列表
privacy_authorizations = {}
with open("path/to/privacy_authorizations.csv", "r") as f:
    next(f)  # 跳过标题行
    for line in f:
        activity1, activity2, authorization = line.strip().split(",")
        privacy_authorizations[(activity1, activity2)] = authorization

# 读取子组织挖掘出的子日志
log_path = "path/to/sublog.xes"
sublog = xes_import_factory.apply(log_path)

# 进行DFG图挖掘
dfg = dfg_factory.apply(sublog)

# 向中央节点申请访问并进行DFG图扩充
new_dfg = dfg_factory.clone_dfg(dfg)
for activity in dfg:
    predecessors = dfg_utils.get_predecessors_for_activities(dfg, activity)
    successors = dfg_utils.get_successors_for_activities(dfg, activity)
    if (activity, activity) not in privacy_authorizations:
        for predecessor in predecessors:
            if (predecessor, activity) not in privacy_authorizations:
                new_dfg[(predecessor, activity)] += 1
        for successor in successors:
            if (activity, successor) not in privacy_authorizations:
                new_dfg[(activity, successor)] += 1

# 向子节点返回扩充后的DFG图
output_file = "path/to/expanded_dfg.pnml"
pnml_exporter.apply(new_dfg, output_file)

