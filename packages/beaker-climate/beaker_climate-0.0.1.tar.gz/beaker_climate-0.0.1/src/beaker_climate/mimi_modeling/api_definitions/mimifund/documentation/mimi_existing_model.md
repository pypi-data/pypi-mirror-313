# Gathering Information About An Existing Model

Start off by importing the Mimi package to your space with

```
using Mimi
```

First of all, you may use the getindex syntax as follows:

```
m[:ComponentName, :VariableName] # returns the whole array of values
m[:ComponentName, :VariableName][100] # returns just the 100th value
```

Indexing into a model with the name of the component and variable will return an array with values from each timestep. You may index into this array to get one value (as in the second line, which returns just the 100th value). Note that if the requested variable is two-dimensional, then a 2-D array will be returned. For example, try taking a look at the income variable of the socioeconomic component of FUND using the code below:

```
m[:socioeconomic, :income]
m[:socioeconomic, :income][100]
```

You may also get data in the form of a dataframe, which will display the corresponding index labels rather than just a raw array. The syntax for this uses getdataframe as follows:

```
getdataframe(m, :ComponentName=>:Variable) # request one variable from one component
getdataframe(m, :ComponentName=>(:Variable1, :Variable2)) # request multiple variables from the same component
getdataframe(m, :Component1=>:Var1, :Component2=>:Var2) # request variables from different components
```

Try doing this for the income variable of the socioeconomic component using:

```
getdataframe(m, :socioeconomic=>:income) # request one variable from one component
getdataframe(m, :socioeconomic=>:income)[1:16,:] # results for all regions in first year (1950)
```

# Access Results: Plots and Graphs

After running the model, you may also explore the results using plots and graphs.

Mimi provides support for plotting using VegaLite and VegaLite.jl within the Mimi Explorer UI.

```
using VegaLite
run(m)
p = Mimi.plot(m, :ComponentName, :ParameterName)
save("figure.svg", p)
```

Do not use `explore()` as mentioned in other documentation.
Always use this style above to plot specific components and parameter names,
otherwise use Plots.
