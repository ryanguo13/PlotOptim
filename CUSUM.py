import numpy as np
import matplotlib.pyplot as plt
import ruptures as rpt
import pandas as pd

# 读取数据
file_path = 'ED-C-01-depth.TXT'

# 读取文件并跳过前面的注释行
df = pd.read_csv(file_path, delimiter='\t', comment='#', skip_blank_lines=False)

# 清理列名
df.columns = df.columns.str.replace(r'\s|\(|\)|\-|\_+', '_', regex=True)

# 忽略 Sputter_Time__s_ 的 400s 及其之后的数据
df = df[df['Sputter_Time__s_'] <= 399]

# 提取需要的列
time = df['Sputter_Time__s_']
intensity = df['Intensity']

# 转换为numpy数组
signal = intensity.to_numpy()

# 检测算法选择，使用动态规划
model = "l2"  # 这里使用 L2 范数模型
algo = rpt.Pelt(model=model).fit(signal)

# 指定要检测的突变点的数量
result = algo.predict(pen=10)  # 调整 pen 参数来控制变化检测的灵敏度
print(result)
# 绘图
plt.figure(figsize=(10, 6))
plt.plot(time, signal, label="Intensity")
rpt.display(signal, result, figsize=(10, 6))
plt.xlabel('Sputter Time')
plt.ylabel('Intensity')
plt.title('Change Point Detection')
plt.legend(['Data 1', 'Data 2'])

plt.legend()
plt.show()
