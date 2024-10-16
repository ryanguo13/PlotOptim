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
spike_intervals = []
for idx in spike_indices:
    start_idx = max(0, idx - 1)
    end_idx = min(len(time) - 1, idx + 2)
    spike_intervals.append((start_idx, end_idx))

# 创建 Plotly 图形对象
fig = go.Figure()

# 添加强度曲线
fig.add_trace(go.Scatter(x=time, y=intensity, mode='lines+markers', name='Intensity', line=dict(color='blue'), marker=dict(size=0.5)))

# 标记突变区间
for (start, end) in spike_intervals:
    fig.add_shape(
        type='rect',
        x0=time[start], x1=time[end],
        y0=min(intensity), y1=max(intensity),
        fillcolor='red', opacity=0.3, line_width=0
    )

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
for (start, end) in spike_intervals:
    print(f"Start: {time[start]}, End: {time[end]}")