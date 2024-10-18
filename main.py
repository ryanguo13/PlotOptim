import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
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
skipe_intervals = []
for idx in spike_indices:
    start_idx = max(0, idx - 1)
    end_idx = min(len(time) - 1, idx + 5) # 根据需要调整区间长度
    if skipe_intervals and skipe_intervals[-1][1] >= start_idx:
        skipe_intervals[-1] = (skipe_intervals[-1][0], end_idx)
    else:
        skipe_intervals.append((start_idx, end_idx))

skip_indices = [i for interval in skipe_intervals for i in range(interval[0], interval[1])]


slices = []
last_index = 0

for start, end in skipe_intervals:
    slices.append(df.iloc[last_index:start])
    last_index = end

slices.append(df.iloc[last_index:])

mapped_data = slices[0]

for i in range(1,len(slices)):
    last = mapped_data.iloc[-1]
    current = slices[i].iloc[0]
    
    diff_rate = last['Intensity'] - current['Intensity']
    diff_rate = diff_rate - (threshold * 0.3 * diff_rate / abs(diff_rate))
    print(diff_rate)

    mapped = slices[i] + diff_rate
    mapped['Sputter_Time__s_'] = slices[i]['Sputter_Time__s_']

    mapped_data = pd.concat([mapped_data, mapped])

print(mapped_data)


# 创建 Plotly 图形对象
fig = go.Figure()

# 添加强度曲线 
fig.add_trace(go.Scatter(x=mapped_data['Sputter_Time__s_'], y=mapped_data['Intensity'], mode='lines+markers', name='Intensity mapped', line=dict(color='blue'), marker=dict(size=0.5)))
fig.add_trace(go.Scatter(x=df['Sputter_Time__s_'], y=intensity, mode='lines+markers', name='Intensity', line=dict(color='green'), marker=dict(size=0.5)))

# # 标记突变区间
# for (start, end) in spike_intervals:
#     fig.add_shape(
#         type='rect',
#         x0=time[start], x1=time[end],
#         y0=min(intensity), y1=max(intensity),
#         fillcolor='red', opacity=0.3, line_width=0
#     )

# 图形设置
fig.update_layout(
    title='Intensity with Detected Spikes',
    xaxis_title='Sputter Time (s)',
    yaxis_title='Intensity',
    showlegend=True
)

# 显示图形
fig.show()

# 输出突变的区间
print("Detected spike intervals:")
for (start, end) in skipe_intervals:
    print(f"Start: {time[start]}, End: {time[end]}")