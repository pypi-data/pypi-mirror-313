#=
compile_library:
- Julia version: 
- Author: krachwal
- Date: 2024-11-21
=#
using PackageCompiler

# Path to the project directory
project_path = pwd()

# Create the shared library
create_library(
    project_path,                # Source project
    "libpowermodels",            # Name of the library
    lib_name = "libpowermodels", # Name of the shared library
    incremental = false,         # Full build for portability
    include_transitive_dependencies = true,
    include_lazy_artifacts = true,
    force = true # facilitate rebuild
)
