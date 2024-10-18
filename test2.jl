using CSV
using DataFrames
using Plots

# 假设数据存储在一个名为 "data.txt" 的文件中
file_path = "ED-C-01-depth.txt"

# 读取文件并跳过前面的注释行
df = CSV.File(file_path, delim='\t', ignorerepeated=true, comment="#") |> DataFrame

# 清理列名
rename!(df, Symbol.(replace.(names(df), r"\s|\(|\)|\-|\_+" => "_")))

# 忽略 Sputter_Time__s_的 400s 及其之后的数据
df = df[df.Sputter_Time__s_ .<= 399, :]

# 使用滑动窗口平滑数据
function moving_average(v, w)
    return [mean(v[i:i+w-1]) for i in 1:length(v)-w+1]
end

data = DataFrame(SputterTime=df.Sputter_Time__s_[3:end-4], Intensity=moving_average(df.Intensity, 7))

# Task 1: 判断突变的区域
threshold = 100.0
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
let
    keep_indices = collect(1:nrow(data))

    for (start, stop) in zip(mutation_start, mutation_end)
        keep_indices = setdiff(keep_indices, start:stop)
    end

    filtered_data = data[keep_indices, :]
    new_intensity = copy(filtered_data.Intensity)

    # Task 3: 连接突变的区域头尾
    for i in eachindex(mutation_start)
        if mutation_start[i] > 1 && mutation_end[i] < nrow(data)
            before_index = mutation_start[i] - 1
            after_index = mutation_end[i] + 1
            if before_index > 0 && after_index <= nrow(data)
                average_value = (data.Intensity[before_index] + data.Intensity[after_index]) / 2
                push!(new_intensity, average_value)
            end
        end
    end
    @assert length(filtered_data.Intensity) == length(new_intensity) "Lengths of filtered_data.Intensity and new_intensity do not match"
    filtered_data[:, :Intensity] .= new_intensity


    # 绘制原始数据和过滤后的数据进行对比
    plot(data.SputterTime, data.Intensity, label="Original", xlabel="Sputter Time (s)", ylabel="Intensity", lw=2)
    plot!(filtered_data.SputterTime, filtered_data.Intensity, label="Filtered and Connected", lw=2, linestyle=:dash)

    display(plot)
end