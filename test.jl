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

# Task 1: 判断突变的区域
threshold = 50.0  # 定义用于检测突变的阈值
intensity_diff = abs.(diff(data.Intensity))
mutation_indices = findall(x -> x > threshold, intensity_diff)

# 确保只找起始和结束位置
mutation_start = Int[]
mutation_end = Int[]

for idx in mutation_indices
    if isempty(mutation_start) || idx > mutation_end[end] + 1
        push!(mutation_start, idx + 1)
        push!(mutation_end, idx + 1)
    else
        mutation_end[end] = idx + 1
    end
end

println("突变区域开始索引: $mutation_start")
println("突变区域结束索引: $mutation_end")

# Task 2: 过滤掉突变的区域, 并保留合适的索引
global keep_indices
keep_indices = collect(1:nrow(data))

for (start, stop) in zip(mutation_start, mutation_end)
    keep_indices = setdiff(keep_indices, start:stop)
end

filtered_data = data[keep_indices, :]

# Task 3: 连接突变的区域头尾
new_intensity = copy(filtered_data.Intensity)
for i in eachindex(mutation_start)
    if mutation_start[i] > 1 && mutation_end[i] < nrow(data)
        before_index = findfirst(==(mutation_start[i]-1), keep_indices)
        after_index = findfirst(==(mutation_end[i]+1), keep_indices)
        if !isnothing(before_index) && !isnothing(after_index)
            average_value = (data.Intensity[mutation_start[i]-1] + data.Intensity[mutation_end[i]+1]) / 2
            insert!(new_intensity, before_index + 1, average_value)
        end
    end
end

filtered_data[:, :Intensity] .= new_intensity

# 绘制原始数据和过滤后的数据进行对比
plot(data.SputterTime, data.Intensity, label="Original", xlabel="Sputter Time (s)", ylabel="Intensity", lw=2)
plot!(filtered_data.SputterTime, filtered_data.Intensity, label="Filtered and Connected", lw=2, linestyle=:dash)

display(plot)