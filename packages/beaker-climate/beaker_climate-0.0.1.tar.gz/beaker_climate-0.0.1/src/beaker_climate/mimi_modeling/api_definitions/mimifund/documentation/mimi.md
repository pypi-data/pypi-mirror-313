Mimi.@defcomp
— Macro

defcomp(comp_name::Symbol, ex::Expr)

Define a Mimi component comp_name with the expressions in ex. The following types of expressions are supported:

    dimension_name = Index() # defines a dimension
    parameter = Parameter(index = [dimension_name], units = "unit_name", default = default_value) # defines a parameter with optional arguments
    variable = Variable(index = [dimension_name], units = "unit_name") # defines a variable with optional arguments
    init(p, v, d) # defines an init function for the component
    run_timestep(p, v, d, t) # defines a run_timestep function for the component

Parses a @defcomp definition, converting it into a series of function calls that create the corresponding ComponentDef instance. At model build time, the ModelDef (including its ComponentDefs) will be converted to a runnable model.
source
Mimi.@defsim
— Macro

defsim(expr::Expr)

Define a Mimi SimulationDef with the expressions in expr.
source
Mimi.@defcomposite
— Macro

defcomposite(cc_name, ex)

Define a Mimi CompositeComponentDef cc_name with the expressions in ex. Expressions are all shorthand for longer-winded API calls, and include the following:

p = Parameter(...)
v = Variable(varname)
local_name = Component(name)
Component(name)  # equivalent to `name = Component(name)`
connect(...)

Variable names are expressed as the component id (which may be prefixed by a module, e.g., Mimi.adder) followed by a . and the variable name in that component. So the form is either modname.compname.varname or compname.varname, which must be known in the current module.

Unlike leaf components, composite components do not have user-defined init or run_timestep functions; these are defined internally to iterate over constituent components and call the associated method on each.
source
Mimi.MarginalModel
— Type

MarginalModel

A Mimi Model whose results are obtained by subtracting results of one base Model from those of another marginal Model that has a difference of delta.
source
Mimi.Model
— Type

Model

A user-facing API containing a ModelInstance (mi) and a ModelDef (md). This Model can be created with the optional keyword argument number_type indicating the default type of number used for the ModelDef. If not specified the Model assumes a number_type of Float64.
source
Mimi.add_comp!
— Function

add_comp!(
    obj::AbstractCompositeComponentDef,
    comp_def::AbstractComponentDef,
    comp_name::Symbol=comp_def.comp_id.comp_name;
    first::NothingInt=nothing,
    last::NothingInt=nothing,
    before::NothingSymbol=nothing,
    after::NothingSymbol=nothing,
    rename::NothingPairList=nothing
)

Add the component comp_def to the composite component indicated by obj. The component is added at the end of the list unless one of the keywords before or after is specified. Note that a copy of comp_id is made in the composite and assigned the give name. The optional argument rename can be a list of pairs indicating original_name => imported_name. The optional arguments first and last indicate the times bounding the run period for the given component, which must be within the bounds of the model and if explicitly set are fixed. These default to flexibly changing with the model's :time dimension.
source

add_comp!(
    obj::AbstractCompositeComponentDef,
    comp_id::ComponentId,
    comp_name::Symbol=comp_id.comp_name;
    first::NothingInt=nothing,
    last::NothingInt=nothing,
    before::NothingSymbol=nothing,
    after::NothingSymbol=nothing,
    rename::NothingPairList=nothing
)

Add the component indicated by comp_id to the composite component indicated by obj. The component is added at the end of the list unless one of the keywords before or after is specified. Note that a copy of comp_id is made in the composite and assigned the give name. The optional arguments first and last indicate the times bounding the run period for the given component, which must be within the bounds of the model and if explicitly set are fixed. These default to flexibly changing with the model's :time dimension.

[Not yet implemented:] The optional argument rename can be a list of pairs indicating original_name => imported_name.
source

add_comp!(obj::AbstractCompositeComponentInstance, ci::AbstractComponentInstance)

Add the (leaf or composite) component ci to a composite's list of components.
source

add_comp!(
    m::Model, comp_id::ComponentId, comp_name::Symbol=comp_id.comp_name;
    first::NothingInt=nothing,
    last::NothingInt=nothing,
    before::NothingSymbol=nothing,
    after::NothingSymbol=nothing,
    rename::NothingPairList=nothing
)

Add the component indicated by comp_id to the model indicated by m. The component is added at the end of the list unless one of the keywords before or after is specified. Note that a copy of comp_id is made in the composite and assigned the give name. The optional argument rename can be a list of pairs indicating original_name => imported_name. The optional arguments first and last indicate the times bounding the run period for the given component, which must be within the bounds of the model and if explicitly set are fixed. These default to flexibly changing with the model's :time dimension.
source

add_comp!(
    m::Model, comp_def::AbstractComponentDef, comp_name::Symbol=comp_id.comp_name;
    first::NothingInt=nothing,
    last::NothingInt=nothing,
    before::NothingSymbol=nothing,
    after::NothingSymbol=nothing,
    rename::NothingPairList=nothing
)

Add the component comp_def to the model indicated by m. The component is added at the end of the list unless one of the keywords, first, last, before, after. Note that a copy of comp_id is made in the composite and assigned the give name. The optional argument rename can be a list of pairs indicating original_name => imported_name. The optional arguments first and last indicate the times bounding the run period for the given component, which must be within the bounds of the model and if explicitly set are fixed. These default to flexibly changing with the model's :time dimension.
source
Mimi.add_shared_param!
— Function

add_shared_param!(md::ModelDef, name::Symbol, value::Any; dims::Array{Symbol}=Symbol[])

User-facing API function to add a shared parameter to Model Def md with name name and value value, and an array of dimension names dims which dfaults to an empty vector. The is_shared attribute of the added Model Parameter will be true.

The value can by a scalar, an array, or a NamedAray. Optional keyword argument 'dims' is a list of the dimension names of the provided data, and will be used to check that they match the model's index labels. Optional keyword argument datatype allows user to specify a datatype to use for the shared model parameter.
source

add_shared_param!(m::Model, name::Symbol, value::Any; dims::Array{Symbol}=Symbol[], datatype::DataType=Nothing)

User-facing API function to add a shared parameter to Model m with name name and value value, and an array of dimension names dims which dfaults to an empty vector. The is_shared attribute of the added Model Parameter will be true.

The value can by a scalar, an array, or a NamedAray. Optional keyword argument 'dims' is a list of the dimension names of the provided data, and will be used to check that they match the model's index labels. This must be included if the value is not a scalar, and defaults to an empty vector. Optional keyword argument datatype allows user to specify a datatype to use for the shared model parameter.
source
Mimi.connect_param!
— Function

connect_param!(obj::AbstractCompositeComponentDef, comp_name::Symbol, param_name::Symbol, model_param_name::Symbol;
               check_attributes::Bool=true, ignoreunits::Bool=false))

Connect a parameter param_name in the component comp_name of composite obj to the model parameter model_param_name.
source

connect_param!(obj::AbstractCompositeComponentDef, comp_def::AbstractComponentDef,
                param_name::Symbol, model_param_name::Symbol; check_attributes::Bool=true,
                ignoreunits::Bool = false)

Connect a parameter param_name in the component comp_def of composite obj to the model parameter model_param_name.
source

connect_param!(obj::AbstractCompositeComponentDef,
    dst::Pair{Symbol, Symbol}, src::Pair{Symbol, Symbol},
    backup::Union{Nothing, Array}=nothing;
    ignoreunits::Bool=false, backup_offset::Union{Nothing, Int} = nothing)

Bind the parameter dst[2] of one component dst[1] of composite obj to a variable src[2] in another component src[1] of the same composite using backup to provide default values and the ignoreunits flag to indicate the need to check match units between the two. The backup_offset argument, which is only valid when backup data has been set, indicates that the backup data should be used for a specified number of timesteps after the source component begins. ie. the value would be 1 if the destination componentm parameter should only use the source component data for the second timestep and beyond.
source

connect_param!(dst::ComponentReference, dst_name::Symbol, src::ComponentReference, src_name::Symbol)

Connect two components as connect_param!(dst, dst_name, src, src_name).
source

connect_param!(dst::ComponentReference, src::ComponentReference, name::Symbol)

Connect two components with the same name as connect_param!(dst, src, name).
source

connect_param!(m::Model, dst_comp_name::Symbol, dst_par_name::Symbol, 
                src_comp_name::Symbol, src_var_name::Symbol, 
                backup::Union{Nothing, Array}=nothing; ignoreunits::Bool=false, 
                backup_offset::Union{Int, Nothing}=nothing)

Bind the parameter dst_par_name of one component dst_comp_name of model m to a variable src_var_name in another component src_comp_name of the same model using backup to provide default values and the ignoreunits flag to indicate the need to check match units between the two. The backup_offset argument, which is only valid when backup data has been set, indicates that the backup data should be used for a specified number of timesteps after the source component begins. ie. the value would be 1 if the destination componentm parameter should only use the source component data for the second timestep and beyond.
source

connect_param!(m::Model, comp_name::Symbol, param_name::Symbol, model_param_name::Symbol;
               check_attributes::Bool=true, ignoreunits::Bool=false))

Connect a parameter param_name in the component comp_name of composite obj to the model parameter model_param_name.
source

connect_param!(m::Model, dst::Pair{Symbol, Symbol}, src::Pair{Symbol, Symbol}, backup::Array; ignoreunits::Bool=false)

Bind the parameter dst[2] of one component dst[1] of model m to a variable src[2] in another component src[1] of the same model using backup to provide default values and the ignoreunits flag to indicate the need to check match units between the two. The backup_offset argument, which is only valid when backup data has been set, indicates that the backup data should be used for a specified number of timesteps after the source component begins. ie. the value would be 1 if the destination componentm parameter should only use the source component data for the second timestep and beyond.
source
Mimi.create_marginal_model
— Function

create_marginal_model(base::Model, delta::Float64=1.0)

Create a MarginalModel where base is the baseline model and delta is the difference used to create the marginal model. Return the resulting MarginaModel which shares the internal ModelDef between the base and marginal.
source
Mimi.delete_param!
— Function

delete_param!(md::ModelDef, model_param_name::Symbol)

Delete model_param_name from md's list of model parameters, and also remove all external parameters connections that were connected to model_param_name.
source

delete_param!(m::Model, model_param_name::Symbol)

Delete model_param_name from a model m's ModelDef's list of model parameters, and also remove all external parameters connections that were connected to model_param_name.
source
Mimi.dim_count
— Function

dim_count(def::AbstractDatumDef)

Return number of dimensions in def.
source

dim_count(mi::ModelInstance, dim_name::Symbol)

Return the size of index dim_name in model instance mi.
source

dim_count(m::Model, dim_name::Symbol)

Return the size of index dim_name in model m.
source
Mimi.dim_keys
— Function

dim_keys(m::Model, dim_name::Symbol)

Return keys for dimension dim-name in model m.
source

dim_keys(mi::ModelInstance, dim_name::Symbol)

Return keys for dimension dim-name in model instance mi.
source
Mimi.dim_key_dict
— Function

dim_key_dict(m::Model)

Return a dict of dimension keys for all dimensions in model m.
source
Mimi.disconnect_param!
— Function

disconnect_param!(obj::AbstractCompositeComponentDef, comp_def::AbstractComponentDef, param_name::Symbol)

Remove any parameter connections for a given parameter param_name in a given component comp_def which must be a direct subcomponent of composite obj.
source

disconnect_param!(obj::AbstractCompositeComponentDef, comp_name::Symbol, param_name::Symbol)

Remove any parameter connections for a given parameter param_name in a given component comp_def which must be a direct subcomponent of composite obj.
source

disconnect_param!(m::Model, comp_name::Symbol, param_name::Symbol)

Remove any parameter connections for a given parameter param_name in a given component comp_def in model m.
source
Mimi.explore
— Function

explore(m::Model)

Produce a UI to explore the parameters and variables of Model m in an independent window.
source

explore(mi::ModelInstance)

Produce a UI to explore the parameters and variables of ModelInstance mi in an independent window.
source

explore(sim_inst::SimulationInstance; title="Electron", model_index::Int = 1, scen_name::Union{Nothing, String} = nothing, results_output_dir::Union{Nothing, String} = nothing)

Produce a UI to explore the output distributions of the saved variables in SimulationInstance sim for results of model model_index and scenario with the name scen_name in a Window with title title. The optional arguments default to a model_index of 1, a scen_name of nothing assuming there is no secenario dimension, and a window with title Electron. The results_output_dir keyword argument refers to the main output directory as provided to run, where all subdirectories are held. If provided, results are assumed to be stored there, otherwise it is assumed that results are held in results.sim and not in an output folder.
source
Mimi.getdataframe
— Function

getdataframe(m::AbstractModel, comp_name::Symbol, pairs::Pair{Symbol, Symbol}...)

Return a DataFrame with values for the given variables or parameters of model m indicated by pairs, where each pair is of the form comp_name => item_name. If more than one pair is provided, all must refer to items with the same dimensions, which are used to join the respective item values.
source

getdataframe(m::AbstractModel, pair::Pair{Symbol, NTuple{N, Symbol}})

Return a DataFrame with values for the given variables or parameters indicated by pairs, where each pair is of the form comp_name => item_name. If more than one pair is provided, all must refer to items with the same dimensions, which are used to join the respective item values.
source

getdataframe(m::AbstractModel, comp_name::Symbol, item_name::Symbol)

Return the values for variable or parameter item_name in comp_name of model m as a DataFrame.
source
Mimi.gettime
— Function

gettime(ts::FixedTimestep)

Return the time (year) represented by Timestep ts
source

gettime(ts::VariableTimestep)

Return the time (year) represented by Timestep ts
source

gettime(c::Clock)

Return the time of the timestep held by the c clock.
source
Mimi.get_param_value
— Function

get_param_value(ci::AbstractComponentInstance, name::Symbol)

Return the value of parameter name in (leaf or composite) component ci.
source
Mimi.get_var_value
— Function

get_var_value(ci::AbstractComponentInstance, name::Symbol)

Return the value of variable name in component ci.
source
Mimi.hasvalue
— Function

hasvalue(arr::TimestepArray, ts::FixedTimestep)

Return true or false, true if the TimestepArray arr contains the Timestep ts.
source

hasvalue(arr::TimestepArray, ts::VariableTimestep)

Return true or false, true if the TimestepArray arr contains the Timestep ts.
source

hasvalue(arr::TimestepArray, ts::FixedTimestep, idxs::Int...)

Return true or false, true if the TimestepArray arr contains the Timestep ts within indices idxs. Used when Array and Timestep have different FIRST, validating all dimensions.
source

hasvalue(arr::TimestepArray, ts::VariableTimestep, idxs::Int...)

Return true or false, true if the TimestepArray arr contains the Timestep ts within indices idxs. Used when Array and Timestep have different TIMES, validating all dimensions.
source
Mimi.is_first
— Function

is_first(ts::AbstractTimestep)

Return true or false, true if ts is the first timestep to be run.
source
Mimi.is_last
— Function

is_last(ts::FixedTimestep)

Return true or false, true if ts is the last timestep to be run.
source

is_last(ts::VariableTimestep)

Return true or false, true if ts is the last timestep to be run. Note that you may run next_timestep on ts, as ths final timestep has not been run through yet.
source
Mimi.is_time
— Function

is_time(ts::AbstractTimestep, t::Int)

Deprecated function to return true or false, true if the current time (year) for ts is t
source
Mimi.is_timestep
— Function

is_timestep(ts::AbstractTimestep, t::Int)

Deprecated function to return true or false, true if ts timestep is step t.
source
Mimi.modeldef
— Function

modeldef(mi)

Return the ModelDef contained by ModelInstance mi.
source

modeldef(m)

Return the ModelDef contained by Model m.
source
Base.nameof
— Function

nameof(obj::NamedDef) = obj.name

Return the name of def. NamedDefs include DatumDef, ComponentDef, and CompositeComponentDef
source
Mimi.parameter_dimensions
— Function

parameter_dimensions(obj::AbstractComponentDef, param_name::Symbol)

Return the names of the dimensions of parameter param_name exposed in the component definition indicated by obj.
source

parameter_dimensions(obj::AbstractComponentDef, comp_name::Symbol, param_name::Symbol)

Return the names of the dimensions of parameter param_name in component comp_name, which is exposed in composite component definition indicated byobj.
source
Mimi.parameter_names
— Function

parameter_names(md::ModelDef, comp_name::Symbol)

Return a list of all parameter names for a given component comp_name in a model def md.
source
Base.replace!
— Function

replace!(
    m::Model,
    old_new::Pair{Symbol, ComponentDef},
    before::NothingSymbol=nothing,
    after::NothingSymbol=nothing,
    reconnect::Bool=true
)

For the pair comp_name => comp_def in old_new, replace the component with name comp_name in the model m with the new component specified by comp_def. The new component is added in the same position as the old component, unless one of the keywords before or after is specified for a different position. The optional boolean argument reconnect with default value true indicates whether the existing parameter connections should be maintained in the new component. Returns a ComponentReference for the added component.
source
Mimi.replace_comp!
— Function

replace_comp!(
    m::Model, comp_def::ComponentDef, comp_name::Symbol=comp_id.comp_name;
    before::NothingSymbol=nothing,
    after::NothingSymbol=nothing,
    reconnect::Bool=true
)

Deprecated function for replacing the component with name comp_name in model m with the new component specified by comp_def. Use the following syntax instead:

replace!(m, comp_name => comp_def; kwargs...)

See docstring for replace! for further description of available functionality.
source

replace_comp!(
    m::Model, comp_id::ComponentId, comp_name::Symbol=comp_id.comp_name;
    before::NothingSymbol=nothing,
    after::NothingSymbol=nothing,
    reconnect::Bool=true
)

Deprecated function for replacing the component with name comp_name in model m with the new component specified by comp_id. Use the following syntax instead:

replace!(m, comp_name => Mimi.compdef(comp_id); kwargs...)

See docstring for replace! for further description of available functionality.
source
Base.run
— Function

Base.run(mm::MarginalModel; ntimesteps::Int=typemax(Int))

Run the marginal model mm once with ntimesteps.
source

Base.run(mi::ModelInstance, ntimesteps::Int=typemax(Int),
        dimkeys::Union{Nothing, Dict{Symbol, Vector{T} where T <: DimensionKeyTypes}}=nothing)

Run the ModelInstance mi once with ntimesteps and dimension keys dimkeys.
source

Base.run(m::Model; ntimesteps::Int=typemax(Int), rebuild::Bool=false,
        dim_keys::Union{Nothing, Dict{Symbol, Vector{T} where T <: DimensionKeyTypes}}=nothing)

Run model m once.
source

Base.run(sim_def::SimulationDef{T}, 
        models::Union{Vector{M}, AbstractModel}, 
        samplesize::Int;
        ntimesteps::Int=typemax(Int), 
        trials_output_filename::Union{Nothing, AbstractString}=nothing, 
        results_output_dir::Union{Nothing, AbstractString}=nothing, 
        pre_trial_func::Union{Nothing, Function}=nothing, 
        post_trial_func::Union{Nothing, Function}=nothing,
        scenario_func::Union{Nothing, Function}=nothing,
        scenario_placement::ScenarioLoopPlacement=OUTER,
        scenario_args=nothing,
        results_in_memory::Bool=true) where {T <: AbstractSimulationData, M <: AbstractModel}

Run the simulation definition sim_def for the models using samplesize samples.

Optionally run the models for ntimesteps, if specified, else to the maximum defined time period. Note that trial data are applied to all the associated models even when running only a portion of them.

If provided, the generated trials and results will be saved in the indicated trials_output_filename and results_output_dir respectively. If results_in_memory is set to false, then results will be cleared from memory and only stored in the results_output_dir.

If pre_trial_func or post_trial_func are defined, the designated functions are called just before or after (respectively) running a trial. The functions must have the signature:

fn(sim_inst::SimulationInstance, trialnum::Int, ntimesteps::Int, tup::Tuple)

where tup is a tuple of scenario arguments representing one element in the cross-product of all scenario value vectors. In situations in which you want the simulation loop to run only some of the models, the remainder of the runs can be handled using a pre_trial_func or post_trial_func.

If provided, scenario_args must be a Vector{Pair}, where each Pair is a symbol and a Vector of arbitrary values that will be meaningful to scenario_func, which must have the signature:

scenario_func(sim_inst::SimulationInstance, tup::Tuple)

By default, the scenario loop encloses the simulation loop, but the scenario loop can be placed inside the simulation loop by specifying scenario_placement=INNER. When INNER is specified, the scenario_func is called after any pre_trial_func but before the model is run.

Returns the type SimulationInstance that contains a copy of the original SimulationDef, along with mutated information about trials, in addition to the model list and results information.
source
Mimi.set_dimension!
— Function

set_dimension!(ccd::CompositeComponentDef, name::Symbol, keys::Union{Int, Vector, Tuple, AbstractRange})

Set the values of ccd dimension name to integers 1 through count, if keys is an integer; or to the values in the vector or range if keys is either of those types.
source

set_dimension!(obj::AbstractComponentDef, name::Symbol, dim::Dimension)

Set the dimension name in obj to dim.
source

set_dimension!(m::Model, name::Symbol, keys::Union{Vector, Tuple, AbstractRange})

Set the values of m dimension name to integers 1 through count, if keysis an integer; or to the values in the vector or range ifkeys`` is either of those types.
source
Mimi.set_leftover_params!
— Function

set_leftover_params!(md::ModelDef, parameters::Dict)

Set all of the parameters in ModelDef md that don't have a value and are not connected to some other component to a value from a dictionary parameters. This method assumes the dictionary keys are Symbols (or convertible into Symbols ie. Strings) that match the names of unset parameters in the model. All resulting connected model parameters will be shared model parameters.

Note that this function set_leftover_params! has been deprecated, and uses should be transitioned to usingupdateleftoverparams!` with keys specific to component-parameter pairs i.e. (compname, paramname) => value in the dictionary.
source

set_leftover_params!(m::Model, parameters::Dict)

Set all of the parameters in Model m that don't have a value and are not connected to some other component to a value from a dictionary parameters. This method assumes the dictionary keys are strings (or convertible into Strings ie. Symbols) that match the names of unset parameters in the model, and all resulting new model parameters will be shared parameters.

Note that this function set_leftover_params! has been deprecated, and uses should be transitioned to usingupdateleftoverparams!` with keys specific to component-parameter pairs i.e. (compname, paramname) => value in the dictionary.
source
Mimi.set_param!
— Function

set_param!(md::ModelDef, comp_name::Symbol,
           value_dict::Dict{Symbol, Any}, param_names)

Call set_param!() for each name in param_names, retrieving the corresponding value from value_dict[param_name].
source

set_param!(md::ModelDef, comp_name::Symbol, param_name::Symbol, value; dims=nothing)

Set the value of parameter param_name in component comp_name of Model Def md to value. This will create a shared model parameter with name param_name and connect comp_name's parameter param_name to it.

The value can by a scalar, an array, or a NamedAray. Optional keyword argument 'dims' is a list of the dimension names of the provided data, and will be used to check that they match the model's index labels.
source

set_param!(md::ModelDef, comp_name::Symbol, param_name::Symbol, model_param_name::Symbol, 
            value; dims=nothing)

Set the value of parameter param_name in component comp_name of Model Def md to value. This will create a shared model parameter with name model_param_name and connect comp_name's parameter param_name to it.

The value can by a scalar, an array, or a NamedAray. Optional keyword argument 'dims' is a list of the dimension names of the provided data, and will be used to check that they match the model's index labels.
source

set_param!(md::ModelDef, comp_def::AbstractComponentDef, param_name::Symbol, 
            model_param_name::Symbol, value; dims=nothing)

Set the value of parameter param_name in component comp_def of Model Def md to value. This will create a shared model parameter with name model_param_name and connect comp_name's parameter param_name to it.

The value can by a scalar, an array, or a NamedAray. Optional keyword argument 'dims' is a list of the dimension names of the provided data, and will be used to check that they match the model's index labels.
source

set_param!(md::ModelDef, param_name::Symbol, value; dims=nothing)

Set the value of parameter param_name in all components of the Model Defmdthat have a parameter of the specified name tovalue. This will create a shared model parameter with nameparam_name` and connect all component parameters with that name to it.

The value can by a scalar, an array, or a NamedAray. Optional keyword argument 'dims' is a list of the dimension names of the provided data, and will be used to check that they match the model's index labels.
source

set_param!(ref::ComponentReference, name::Symbol, value)

Set a component parameter as set_param!(reference, name, value). This creates a unique name :compname_paramname in the model's model parameter list, and sets the parameter only in the referenced component to that value.
source

set_param!(m::Model, comp_name::Symbol, param_name::Symbol, value; dims=nothing)

Set the parameter of a component comp_name in a model m to a given value. The value can by a scalar, an array, or a NamedAray. Optional keyword argument 'dims' is a list of the dimension names of the provided data, and will be used to check that they match the model's index labels.
source

set_param!(m::Model, comp_name::Symbol, param_name::Symbol, model_param_name::Symbol, value; dims=nothing)

Set the parameter param_name of a component comp_name in a model m to a given value, storing the value in the model's parameter list by the provided name model_param_name. The value can by a scalar, an array, or a NamedAray. Optional keyword argument 'dims' is a list of the dimension names of the provided data, and will be used to check that they match the model's index labels.
source

set_param!(m::Model, param_name::Symbol, value; dims=nothing)

Set the value of a parameter in all components of the model that have a parameter of the specified name.
source
Mimi.TimestepIndex
— Type

TimestepIndex

A user-facing type used to index into a TimestepArray in run_timestep functions, containing an Int index that indicates the position in the array in terms of timesteps.
source
Mimi.TimestepValue
— Type

TimestepValue

A user-facing type used to index into a TimestepArray in run_timestep functions, containing a value of the same Type as the times in the TimstepArray which is used to index into the array at that position, with an optional Int offset in terms of timesteps.
source
Mimi.update_param!
— Function

update_param!(obj::AbstractCompositeComponentDef, name::Symbol, value; update_timesteps = nothing)

Update the value of a model parameter in composite obj, referenced by name. The update_timesteps keyword argument is deprecated, we keep it here just to provide warnings.
source

update_param!(mi::ModelInstance, name::Symbol, value)

Update the value of a model parameter in ModelInstance mi, referenced by name. This is an UNSAFE update as it does not dirty the model, and should be used carefully and specifically for things like our MCS work.
source

update_param!(mi::ModelInstance, comp_name::Symbol, param_name::Symbol, value)

Update the value of a model parameter in ModelInstance mi, connected to component comp_name's parameter param_name. This is an UNSAFE updat as it does not dirty the model, and should be used carefully and specifically for things like our MCS work.
source

update_param!(md::ModelDef, comp_name::Symbol, param_name::Symbol, value)

Update the value of the unshared model parameter in Model Def md connected to component comp_name's parameter param_name.
source

update_param!(ref::ComponentReference, name::Symbol, value)

Update a component parameter as update_param!(reference, name, value). This uses the unique name :compname_paramname in the model's model parameter list, and updates the parameter only in the referenced component to that value.
source

update_param!(m::Model, name::Symbol, value; update_timesteps = nothing)

Update the value of an model parameter in model m, referenced by name. The update_timesteps keyword argument is deprecated, we keep it here just to provide warnings.
source

update_param!(m::Model, comp_name::Symbol, param_name::Symbol, value)

Update the value of the unshared model parameter in Model m's Model Def connected to component comp_name's parameter param_name.
source
Mimi.update_params!
— Function

update_params!(obj::AbstractCompositeComponentDef, parameters::Dict; update_timesteps = nothing)

For each (k, v) in the provided parameters dictionary, update_param! is called to update the model parameter identified by k to value v.

For updating unshared parameters, each key k must be a Tuple matching the name of a component in obj and the name of an parameter in that component.

For updating shared parameters, each key k must be a symbol or convert to a symbol matching the name of a shared model parameter that already exists in the model.
source

update_params!(m::Model, parameters::Dict; update_timesteps = nothing)

For each (k, v) in the provided parameters dictionary, update_param! is called to update the model parameter identified by k to value v.

For updating unshared parameters, each key k must be a Tuple matching the name of a component in obj and the name of an parameter in that component.

For updating shared parameters, each key k must be a symbol or convert to a symbol matching the name of a shared model parameter that already exists in the model.
source
Mimi.update_leftover_params!
— Function

update_leftover_params!(md::ModelDef, parameters::Dict)

Update all of the parameters in ModelDef md that don't have a value and are not connected to some other component to a value from a dictionary parameters. This method assumes the dictionary keys are Tuples of Symbols (or convertible to Symbols ie. Strings) of (compname, paramname) that match the component-parameter pair of unset parameters in the model. All resulting connected model parameters will be unshared model parameters.
source

update_leftover_params!(m::Model, parameters::Dict)

Update all of the parameters in Model m that don't have a value and are not connected to some other component to a value from a dictionary parameters. This method assumes the dictionary keys are Tuples of Symbols (or convertible to Symbols ie. Strings) of (compname, paramname) that match the component-parameter pair of unset parameters in the model. All resulting connected model parameters will be unshared model parameters.
source
Mimi.variable_dimensions
— Function

variable_dimensions(obj::AbstractCompositeComponentDef, comp_path::ComponentPath, var_name::Symbol)

Return the names of the dimensions of variable var_name exposed in the composite component definition indicated byobj along the component path comp_path. The comp_path is of type Mimi.ComponentPath with the single field being an NTuple of symbols describing the relative (to a composite) or absolute (relative to ModelDef) path through composite nodes to specific composite or leaf node.
source

variable_dimensions(obj::AbstractCompositeComponentDef, comp::Symbol, var_name::Symbol)

Return the names of the dimensions of variable var_name exposed in the composite component definition indicated by obj for the component comp, which exists in a flat model.
source

variable_dimensions(obj::AbstractCompositeComponentDef, comp::Symbol, var_name::Symbol)

Return the names of the dimensions of variable var_name exposed in the composite component definition indicated by obj along the component path comp_path. The comp_path is a tuple of symbols describing the relative (to a composite) or absolute (relative to ModelDef) path through composite nodes to specific composite or leaf node.
source

variable_dimensions(obj::AbstractComponentDef, name::Symbol)

Return the names of the dimensions of variable name exposed in the component definition indicated by obj.
source
Mimi.variable_names
— Function

variable_names(md::AbstractCompositeComponentDef, comp_name::Symbol)

Return a list of all variable names for a given component comp_name in a model def md.
source

variable_names(comp_def::AbstractComponentDef)

Return a list of all variable names for a given component comp_def.
source
« Reference Guides Intro
Structures: Classes.jl and Types »
