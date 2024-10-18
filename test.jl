using CSV
using DataFrames
using Statistics
using Plots
using Dates

# 假设数据存储在一个名为 "data.txt" 的文件中
file_path = "ED-C-01-depth.txt"

# 读取文件并跳过前面的注释行
df = CSV.File(file_path, delim='\t', ignorerepeated=true, comment="#") |> DataFrame

# 显示数据的前几行
# println(first(df, 5))
rename!(df, Symbol.(replace.(names(df), r"\s|\(|\)|\-|\_+" => "_")))

# 打印清理后的列名
# println(names(df))

# 忽略 Sputter_Time__s_的 400s 及其之后的数据
df = df[df.Sputter_Time__s_ .<= 399, :]

# 绘制数据，画出 Sputter Time 和 Intensity 的关系图
# plot(df.Sputter_Time__s_, df.Intensity, label="Intensity", xlabel="Sputter Time", ylabel="Intensity", marker=:circle, markersize=2, legend=:topleft)

# plot!(df.Sputter_Time__s_, df.Intensity_Background_Corrected__, label="Intensity", xlabel="Sputter Time", ylabel="Intensity", marker=:circle, markersize=2, legend=:topleft)
# savefig("intensity_vs_time.png")

# 示例数据（在实际情况下，应替换为实际数据）
data = df
# data = DataFrame(
#     SputterTime = 1:100,
#     Intensity = vcat(ones(25), 50 .* ones(5), ones(70)) + 0.1 * randn(100)
# )

# Task 1: 判断突变（突然变大）的区域
# 使用滑动窗口方法来检测突变
window_size = 20
threshold = 20

# 创建一个布尔数组来标记突变点
mutations = Bool.(abs.(diff(data.Intensity)) .> threshold * std(data.Intensity))

# 创建一个布尔数组来标记突变点
connected_mutations = Bool.(diff(mutations) .!= 0)

# 创建一个布尔数组来标记突变点
connected_mutations = vcat(false, connected_mutations)

# 创建一个布尔数组来标记突变点
connected_mutations = connected_mutations[1:end-1]

# 打印突变点
println("Mutations: ", mutations)
println("Connected Mutations: ", connected_mutations)

# Task 2: 过滤掉突变点
filtered_data = data[.!connected_mutations, :]

# Task 3: 连接突变点
connected_data = data[connected_mutations, :]






# 绘制原始数据和过滤后的数据进行对比
plot(data.SputterTime, data.Intensity, label="Original", xlabel="Sputter Time (s)", ylabel="Intensity", lw=2)
plot!(filtered_data.SputterTime, filtered_data.Intensity, label="Filtered and Connected", lw=2, linestyle=:dash)

display(plot)