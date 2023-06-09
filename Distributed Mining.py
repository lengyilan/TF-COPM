# -*- codeing = utf-8 -*-
# @Time : 2023/6/2 12:31
# @Author : 王赓
# @File : Distributed Mining.py
# @Software : PyCharm

from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.objects.dfg.exporter import exporter as dfg_exporter
from pm4py.objects.dfg.utils import dfg_utils
import syft as sy

# 初始化可信环境
hook = sy.TorchHook(torch)
bob = sy.VirtualWorker(hook, id="bob")  # 子组织1
alice = sy.VirtualWorker(hook, id="alice")  # 子组织2
charlie = sy.VirtualWorker(hook, id="charlie")  # 子组织3

# 读取子日志
log_path = "path/to/sublog.xes"
sublog = xes_import_factory.apply(log_path)

# 进行DFG图挖掘
dfg = dfg_factory.apply(sublog)

# 提取活动信息
activities = list(dfg.keys())

# 提取频率矩阵F
F = dfg_utils.convert_to_matrix(dfg)

# 提取时间矩阵T（示例中假设T矩阵为全0矩阵）
T = [[0] * len(activities)] * len(activities)

# 将数据转换为PySyft张量
activities_tensor = torch.tensor(activities)
F_tensor = torch.tensor(F)
T_tensor = torch.tensor(T)

# 加密参数信息
encrypted_activities = activities_tensor.encrypt(crypto_provider=bob)
encrypted_F = F_tensor.encrypt(crypto_provider=bob)
encrypted_T = T_tensor.encrypt(crypto_provider=bob)

# 发送加密后的参数信息到中央节点
encrypted_activities.send(bob)
encrypted_F.send(bob)
encrypted_T.send(bob)

'''
import syft as sy
import torch
from pm4py.objects.dfg import factory as dfg_factory
from pm4py.objects.dfg.utils import dfg_utils

# 初始化可信环境
hook = sy.TorchHook(torch)
bob = sy.VirtualWorker(hook, id="bob")  # 子组织1
alice = sy.VirtualWorker(hook, id="alice")  # 子组织2
charlie = sy.VirtualWorker(hook, id="charlie")  # 子组织3

# 接收加密的参数信息
encrypted_activities = torch.Tensor().fix_prec().get()
encrypted_F = torch.Tensor().fix_prec().get()
encrypted_T = torch.Tensor().fix_prec().get()

# 解密参数信息
activities = encrypted_activities.decrypt()
F = encrypted_F.decrypt()
T = encrypted_T.decrypt()

# 构建全局DFG图
dfg = dfg_factory.apply(activities, F, T)

# 打印全局DFG图
print(dfg)

'''

