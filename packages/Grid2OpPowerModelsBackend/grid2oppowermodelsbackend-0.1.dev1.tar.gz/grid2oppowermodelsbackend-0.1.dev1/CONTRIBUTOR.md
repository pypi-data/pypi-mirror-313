# Contributor Documentation

## Dev Environment Setup

Install [Julia](https://julialang.org/downloads/) as appropriate for your platform (there are also binaries if you scroll down on the linked page).

Once Julia is installed, launch the REPL with `julia` and enter `]` to get into the package manager.

Enter `add PackageCompiler, PowerModels, JSON` to install the dependencies.
- [PackageCompiler.jl](https://julialang.github.io/PackageCompiler.jl/stable/refs.html#PackageCompiler.create_library)
- [PowerModels.jl](https://lanl-ansi.github.io/PowerModels.jl)

Hit `Backspace` (or `delete` on Macbook) to exit the package manager.

## Building the Shared Object

To generate the shared object (.so) `julia compile_library.jl`