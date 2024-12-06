FROM python:3.11.5
RUN useradd -m jupyter
EXPOSE 8888

RUN apt update && apt-get install -y lsof build-essential make gcc g++ git gfortran npm \
        gdal-bin libgdal-dev python3-all-dev libspatialindex-dev
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install Julia
RUN wget --no-verbose -O julia.tar.gz "https://julialang-s3.julialang.org/bin/linux/$(uname -m|sed 's/86_//')/1.10/julia-1.10.1-linux-$(uname -m).tar.gz"
RUN tar -xzf "julia.tar.gz" && mv julia-1.10.1 /opt/julia && \
    ln -s /opt/julia/bin/julia /usr/local/bin/julia && rm "julia.tar.gz"

# Add Julia to Jupyter
USER 1000
RUN julia -e 'using Pkg; Pkg.add("IJulia");'

# Install Julia requirements
RUN julia -e ' \
    packages = [ \
        "DataSets", "XLSX", "Plots", "Downloads", "DataFrames", "ImageShow", "FileIO", "Mimi", "JSON3", "DisplayAs"  \
    ]; \
    using Pkg; \
    Pkg.add(packages);'

# Back to root for Python package install
USER root

# Copy project files
COPY --chown=1000:1000 . /jupyter/
RUN chown -R 1000:1000 /jupyter

# Install Python requirements
RUN pip install --upgrade --no-cache-dir hatch pip
RUN pip install -e /jupyter/

# Switch to jupyter user and install Julia packages
USER jupyter
WORKDIR /jupyter

RUN julia -e 'using Pkg; Pkg.add("IJulia");'

# Install required Julia packages (these are used in the procedures/*.jl files)
RUN julia -e 'using Pkg; Pkg.add(["Mimi", "JSON3", "DisplayAs"]); using Mimi'

# Install LLMConvenience from GitHub
RUN julia -e 'using Pkg; Pkg.add(url="https://github.com/fund-model/MimiFUND.jl.git"); using MimiFUND'

# Service
CMD ["python", "-m", "beaker_kernel.server.main", "--ip", "0.0.0.0"]
