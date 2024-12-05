#=
PowerModelsLibrary:
- Julia version: 1.11.1
- Date: 2024-11-21
=#
module PowerModelsLibrary

using PowerModels
using JSON

function solve_power_flow(json_data::String)::String
    data = JSON.parse(json_data)
    result = PowerModels.run_dc_opf(data, PowerModels.run_dc_opf_default)
    return JSON.json(result)
end

export solve_power_flow

end
