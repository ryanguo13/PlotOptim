import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# 强制在浏览器中显示
pio.renderers.default = 'browser'

# 读取数据
file_path = 'ED-C-01-depth.TXT'
df = pd.read_csv(file_path, delimiter='\t', comment='#', skip_blank_lines=False)

# 清理列名
df.columns = df.columns.str.replace(r'\s|\(|\)|\-|\_+', '_', regex=True)

# 过滤时间 >= 400s 的数据
df = df[df['Sputter_Time__s_'] <= 399]

# 提取时间和强度数据
time = df['Sputter_Time__s_'].values
intensity = df['Intensity'].values

# 计算变化率（差分）
diff_intensity = np.diff(intensity)

# 设定阈值（可以调整）
threshold = np.percentile(np.abs(diff_intensity), 99)  # 设置 99% 百分位数作为突变的阈值

# 找到突变的索引
spike_indices = np.where(np.abs(diff_intensity) > threshold)[0]

# 确定突变的区间
spike_intervals = []
for idx in spike_indices:
    start_idx = max(0, idx - 1)
    end_idx = min(len(time) - 1, idx + 2)
    spike_intervals.append((start_idx, end_idx))

# 创建新的时间和强度列表，用于存储去除突变区间后的数据
filtered_time = []
filtered_intensity = []

# 记录上一次的结束索引
prev_end_idx = 0

# 遍历所有突变区间，删除突变数据，并对突变后的数据进行平移
for (start, end) in spike_intervals:
    # 将上一个突变区间之前的数据保存
    filtered_time.extend(time[prev_end_idx:start])
    filtered_intensity.extend(intensity[prev_end_idx:start])

    # 计算平移量：突变前的最后一个点和突变后第一个点的强度差
    if end < len(intensity):
        shift_value = intensity[start - 1] - intensity[end]

        # 将突变区间后的所有数据平移
        adjusted_intensity = intensity[end:] + shift_value
        filtered_time.extend(time[end:])
        filtered_intensity.extend(adjusted_intensity)

    # 更新上一个区间的结束索引
    prev_end_idx = end

# 转换为 NumPy 数组
filtered_time = np.array(filtered_time)
filtered_intensity = np.array(filtered_intensity)

# 创建 Plotly 图形对象
fig = go.Figure()

# 添加强度曲线 (经过过滤和平移后的数据)
fig.add_trace(go.Scatter(x=filtered_time, y=filtered_intensity, mode='lines+markers', name='Filtered Intensity',
                         line=dict(color='blue')))

# 图形设置
fig.update_layout(
    title='Intensity with Spikes Removed and Adjusted',
    xaxis_title='Sputter Time (s)',
    yaxis_title='Intensity',
    showlegend=True
)

# 显示图形
fig.show()

# 输出处理后的结果
print("Filtered spike intervals:")
for (start, end) in spike_intervals:
    print(f"Start: {time[start]}, End: {time[end]}")