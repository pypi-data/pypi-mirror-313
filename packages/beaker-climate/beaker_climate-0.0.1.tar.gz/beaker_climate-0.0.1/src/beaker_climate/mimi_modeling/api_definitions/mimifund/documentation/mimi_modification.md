# Altering Parameters

In the case that you wish to alter an parameter retrieving an exogenously set value from a model parameter, you may use the update_param! function. Per usual, you will start by importing the Mimi package to your space with

```
using Mimi
```

For example, in DICE the parameter fco22x is the forcings of equilibrium CO2 doubling in watts per square meter, and is a shared model parameter (named fco22x) and connected to component parameters with the same name, fco22x, in components climatedynamics and radiativeforcing. We can change this value from its default value of 3.200 to 3.000 in both components, using the following code:

```
update_param!(m, :fco22x, 3.000)
run(m)
```

A more complex example may be a situation where you want to update several parameters, including some with a :time dimension, in conjunction with altering the time index of the model itself. DICE uses a default time horizon of 2005 to 2595 with 10 year increment timesteps. If you wish to change this, say, to 1995 to 2505 by 10 year increment timesteps and use parameters that match this time, you could use the following code:

First you update the time dimension of the model as follows:

```
const ts = 10
const years = collect(1995:ts:2505)
nyears = length(years)
set_dimension!(m, :time, years)
```

At this point all parameters with a :time dimension have been slightly modified under the hood, but the original values are still tied to their original years. In this case, for example, the model parameter has been shorted by 9 values (end from 2595 –> 2505) and padded at the front with a value of missing (start from 2005 –> 1995). Since some values, especially initializing values, are not time-agnostic, we maintain the relationship between values and time labels. If you wish to attach new values, you can use update_param! as below. In this case this is probably necessary, since having a missing in the first spot of a parameter with a :time dimension will likely cause an error when this value is accessed.

Updating the :time dimension can be tricky, depending on your use case, so we recommend reading How-to Guide 6: Update the Time Dimension if you plan to do this often in your work.

To batch update shared model parameters, create a dictionary params with one entry (k, v) per model parameter you want to update by name k to value v. Each key k must be a symbol or convert to a symbol matching the name of a shared model parameter that already exists in the model definition. Part of this dictionary may look like:

```
params = Dict{Any, Any}()
params[:a1]         = 0.00008162
params[:a2]         = 0.00204626
...
params[:S]          = repeat([0.23], nyears)
...
```

To batch update unshared model parameters, follow a similar pattern but use tuples (:compname, :paramname) as your dictionary keys, which might look like:

```
params = Dict{Any, Any}()
params[(:comp1, :a1)]         = 0.00008162
params[(:comp1, :a2)]         = 0.00204626
...
params[(:comp2, :S)]          = repeat([0.23], nyears)
...
```

Finally, you can combine these two dictionaries and Mimi will recognize and resolve the two different key types under the hood.

Now you simply update the parameters listen in params and re-run the model with

```
update_params!(m, params)
run(m)
```

Component and Structural Modifications: The API

Most model modifications will include not only parametric updates, but also structural changes and component modification, addition, replacement, and deletion along with the required re-wiring of parameters etc.

We recommend trying to use the user-facing API to modify existing models by importing the model (and with it its various components) as demonstrated in examples such as MimiFUND-MimiFAIR-Flat.jl from Tutorial 7. When this API is not satisfactory, you may wish to make changes directly to the model repository, which for many completed models is configured as a julia Package. In this case, the use of environments and package versioning may become one level more complicated, so please do not hesitate to reach out on the forum for up-front help on workflow ... pausing for a moment to get that straight will save you a lot of time. We will work on getting standard videos and tutorials up as resources as well.

The most useful functions of the common API, in these cases are likely `replace!`, `add_comp! `along with delete! and the requisite functions for parameter setting and connecting. For detail on the public API functions look at the API reference.

If you wish to modify the component structure we recommend you also look into the built-in helper components adder, multiplier,ConnectorCompVector, and ConnectorCompMatrix in the src/components folder, as these can prove quite useful.

adder.jl – Defines Mimi.adder, which simply adds two parameters, input and add and stores the result in output.

multiplier.jl – Defines Mimi.multiplier, which simply multiplies two parameters, input and multiply and stores the result in output.

connector.jl – Defines a pair of components, Mimi.ConnectorCompVector and Mimi.ConnectorCompMatrix. These copy the value of parameter input1, if available, to the variable output, otherwise the value of parameter input2 is used. It is an error if neither has a value.
