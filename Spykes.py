import numpy as np
from spykes.plot.neurovis import NeuroVis

# 假设您已有尖峰数据和事件
spike_times = np.random.uniform(0, 400, size=100)  # 模拟尖峰时间
events = np.array([50, 150, 250, 350])  # 假设的一些事件时间

# 创建 NeuroVis 对象
nv = NeuroVis(spike_times, name='Neuron 1')

# 绘制围绕事件的 PSTH（每事件时间直方图）
nv.plot_event_centers(events, window=(-50, 50))
