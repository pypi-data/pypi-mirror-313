# beaker-climate

[![PyPI - Version](https://img.shields.io/pypi/v/beaker-climate.svg)](https://pypi.org/project/beaker-climate)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/beaker-climate.svg)](https://pypi.org/project/beaker-climate)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)
- [Usage](#usage)
    - [Mimi](#mimi) 

## Installation 

### Docker

```docker-compose up```

This will run Beaker with the contexts installed.
Ensure `.env` is created in the working directory with the correct keys.

### Existing Beaker Installation

```
pip install -e climate-python
pip install -e mimi-api
```

### Manual

```console
# Install Julia
curl -fsSL https://install.julialang.org | sh -s -- -y
export PATH="/root/.julialup/bin:${PATH}"

# Set up Julia environment
julia -e ' \
    packages = [ \
        "DataSets", "XLSX", "Plots", "Downloads", "DataFrames", "ImageShow", "FileIO", "Mimi", "JSON3", "DisplayAs"  \
    ]; \
    using Pkg; \
    Pkg.add(packages);'

# Install MimiFUND Julia library
julia -e 'using Pkg; Pkg.add(url="https://github.com/fund-model/MimiFUND.jl.git"); using MimiFUND'

# install beaker-climate contexts
pip install -e climate-python
pip install -e mimi-julia

export OPENAI_API_KEY=your key here
export GEMINI_API_KEY=your key here
```

Run with `beaker notebook`

## Usage

### Mimi

Inside the `mimi_api` context, Mimi integrated assessment models can be used.

**MimiFUND**:  

Example questions for the agent:

> "What is a FUND model?"

> "How do FUND models calculate social cost?"

> "What parameters matter in calculating the social cost of CO2?"

> "Can you calculate the social cost of CH4 starting at the year 1995?"

> "Can you calculate the social cost of CO2 with n = 5 monte carlo simulations and plot the result?"

## License

`beaker-climate` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
