import json
import logging
import re
from typing import Optional
import codecs

import pandas
import matplotlib.pyplot as plt
import xarray as xr

from archytas.react import Undefined
from archytas.tool_utils import AgentRef, LoopControllerRef, ReactContextRef, tool

from beaker_kernel.lib import BeakerAgent
from beaker_kernel.lib.context import BaseContext

from pathlib import Path
from adhoc_api.tool import AdhocApi, APISpec

logger = logging.getLogger(__name__)

class MessageLogger():
    def __init__(self, context):
        self.context = context 
    def info(self, message):
        self.context.send_response("iopub",
            "gemini_info", {
                "body": message
            },
        ) 
    def error(self, message):
        self.context.send_response("iopub",
            "gemini_error", {
                "body": message
            },
        ) 

class ClimateDataUtilityAgent(BeakerAgent):

    """
    You are assisting us in modifying geo-temporal datasets.

    The main things you are going to do are regridding spatial datasets, temporally rescaling datasets, and clipping the extent of geo-temporal datasets.

    If you don't have the details necessary to use a tool, you should use the ask_user tool to ask the user for them.

    """
    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        super().__init__(context, tools, **kwargs)
        self.here = Path(__file__).parent  
        self.logger = MessageLogger(self.context)
        try:
            self.esgf_api_adhoc = AdhocApi(apis=[self.get_esgf_api()], 
                                            drafter_config={'model': 'gemini-1.5-pro-001', 'ttl_seconds': 3600},
                                            finalizer_config={'model': 'gpt-4o'},
                                            logger=self.logger,
                                            # run_code=python.run  # don't include so top level agent will run the code itself
                                            )
        except ValueError as e:
            self.esgf_api_adhoc = None     
            
    def get_esgf_api(self) -> APISpec:
        documentation = (self.here/'api_documentation'/'esgf_rest_documentation.md').read_text()
        ESGF_DESCRIPTION = '''\
        The Earth System Grid Federation (ESGF) is a global collaboration that manages and distributes climate and environmental science data. 
        It serves as the primary platform for accessing CMIP (Coupled Model Intercomparison Project) data and other climate model outputs.
        The federation provides a distributed database and delivery system for climate science data, particularly model outputs and observational data.
        Through ESGF, users can search, discover and access climate datasets from major modeling centers and research institutions worldwide.
        The system supports authentication, search capabilities, and data transfer protocols optimized for large scientific datasets.
        '''

        ESGF_ADDITIONAL_INFO_REST = '''\
        For download/OpenDAP URLs, the Thredds catalog URL is now DEPRECATED. If you see a URL like:

        https://aims3.llnl.gov/thredds/catalog/esgcet/306/CMIP6.ScenarioMIP.NCAR.CESM2-WACCM.ssp585.r1i1p1f1.Oday.tos.gr.v20190815.xml#CMIP6.ScenarioMIP.NCAR.CESM2-WACCM.ssp585.r1i1p1f1.Oday.tos.gr.v20190815

        You should reformat it to something like:
        
        http://aims3.llnl.gov/thredds/dodsC/cmip6/ScenarioMIP/NCAR/CESM2-WACCM/ssp585/r1i1p1f1/Oday/tos/gr/v20190815/tos_Oday_CESM2-WACCM_ssp585_r1i1p1f1_gr_20150102-21010101.nc

        Additionally, any data downloaded should be downloaded to the './data/' directory.
        Please ensure the code makes sure this location exists, and all downloaded data is saved to this location.
        '''

        # ESGF_ADDITIONAL_INFO = '''\
        # Be sure to import and instantiate the client for the ESGF API. For example:
        # ```python
        # from pyesgf.search import SearchConnection
        # ```

        # You should always use http://esgf-node.llnl.gov/esg-search as the search node unless it times out.

        # When performing a search, you MUST always specify the facets as its own argument. For example:

        # ```python
        # facets='project,experiment_family'
        # ctx = conn.new_context(project='CMIP5', query='humidity', facets=facets)
        # ctx.hit_count
        # ```

        # In a SEARCH, if the user asks you to find something (e.g. humidity, precipitation, etc.), you should use the query argument.
        # You should NEVER use the variable or experiment_id parameters, they are just way too specific. Stuff as much as you can
        # into the query parameter and work with the user to refine the query over time. Never, EVER print all the results of a search,
        # it could be HUGE. Collect the results into a variable and slice some for presentation to the user. Refer to the search results data
        # model for more information on how to work with it. Note that the only attribute on a search result `DatasetResult`
        # is `dataset_id`, so if you want to capture the results, you can iterate through the results and collect the `dataset_id` of each
        # result. Just note that search results are an iterable, not a list, so you should loop over the first ~10 to 100 results to get a good sample.
        # You can't just slice them! You can check the number of results by calling `ctx.hit_count` which is wise to do before collecting all results.

        # For other things, like getting more detail about a dataset or downloading a dataset you MUST
        # use the instructions available to you in the associated API documentation.

        # Additionally, any data downloaded should be downloaded to the './data/' directory.
        # Please ensure the code makes sure this location exists, and all downloaded data is saved to this location.
        # '''   

        esgf_api_spec: APISpec = {
            'name': "Earth System Grid Federation (ESGF)",
            'cache_key': 'api_assistant_esgf_client',
            'description': ESGF_DESCRIPTION,
            'documentation': documentation,
            'proofread_instructions': ESGF_ADDITIONAL_INFO_REST
        }
        return esgf_api_spec


    @tool()
    async def use_esgf_api(self, goal: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        """
        This tool should be used to submit a request to the ESGF API. This can be used
        for searching for datasets, downloading datasets, etc. This can include climate data such
        as CMIP5, CMIP6, etc.

        Args:
            goal (str): The goal of the interaction with the ESGF API.

        Returns:
            str: The code generated as a result of the ESGF API request.
        """
        name = "Earth System Grid Federation (ESGF)"
        code = self.esgf_api_adhoc.use_api(name, goal)
        self.logger.info(f"running code produced by esgf ad hoc api client: {code}")
        try:
            result = await self.run_code(code, agent=agent, react_context=react_context)
            return result
        except Exception as e:
            self.logger.error(f"error in using ESGF client api: {e}")
            raise e
        
    async def run_code(self, code: str, agent: AgentRef, react_context: ReactContextRef) -> str:
        """
        Executes code in the user's notebook on behalf of the user, but collects the outputs of the run for use by the Agent
        in the ReAct loop, if needed.

        The code runs in a new codecell and the user can watch the execution and will see all of the normal output in the
        Jupyter interface.

        This tool can be used to probe the user's environment or collect information to answer questions, or can be used to
        run code completely on behalf of the user. If a user asks the agent to do something that reasonably should be done
        via code, you should probably default to using this tool.

        This tool can be run more than once in a react loop. All actions and variables created in earlier uses of the tool
        in a particular loop should be assumed to exist for future uses of the tool in the same loop.

        Args:
            code (str): Code to run directly in Jupyter. This should be a string exactly as it would appear in a notebook
                        codecell. No extra escaping of newlines or similar characters is required.
        Returns:
            str: A summary of the run, along with the collected stdout, stderr, returned result, display_data items, and any
                errors that may have occurred.
        """
        self.logger.info(f"used runcode2: {code}")
        def format_execution_context(context) -> str:
            """
            Formats the execution context into a format that is easy for the agent to parse and understand.
            """
            stdout_list = context.get("stdout_list")
            stderr_list = context.get("stderr_list")
            display_data_list = context.get("display_data_list")
            error = context.get("error")
            return_value = context.get("return")

            success = context['done'] and not context['error']
            if context['result']['status'] == 'error':
                success = False
                error = context['result']
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                error['traceback'] = ansi_escape.sub('', error['traceback'])

            output = [
                """Execution report:""",
                f"""Execution id: {context['id']}""",
                f"""Successful?: {success}""",
                f"""Code executed:
    ```
    {context['command']}
    ```\n""",
            ]

            if error:
                output.extend([
                    "The following error was thrown when executing the code",
                    "  Error:",
                    f"    {error['ename']} {error['evalue']}",
                    "  TraceBack:",
                    "\n".join(error['traceback']),
                    "",
                ])


            if stdout_list:
                output.extend([
                    "The execution produced the following stdout output:",
                    "\n".join(["```", *stdout_list, "```\n"]),
                ])
            if stderr_list:
                output.extend([
                    "The execution produced the following stderr output:",
                    "\n".join(["```", *stderr_list, "```\n"]),
                ])
            if display_data_list:
                output.append(
                    "The execution produced the following `display_data` objects to display in the notebook:",
                )
                for idx, display_data in enumerate(display_data_list):
                    output.append(
                        f"display_data item {idx}:"
                    )
                    for mimetype, value in display_data.items():
                        if len(value) > 800:
                            value = f"{value[:400]} ... truncated ... {value[-400:]}"
                        output.append(
                            f"{mimetype}:"
                        )
                        output.append(
                            f"```\n{value}\n```\n"
                        )
            if return_value:
                output.append(
                    "The execution returned the following:",
                )
                if isinstance(return_value, str):
                    output.extend([
                        '```', return_value, '```\n'
                    ])
            output.append("Execution Report Complete")
            return "\n".join(output)

        # TODO: In future, this may become a parameter and we allow the agent to decide if code should be automatically run
        # or just be added.
        autoexecute = True
        message = react_context.get("message", None)
        identities = getattr(message, 'identities', [])
        try:
            execution_task = None
            checkpoint_index, execution_task = await agent.context.subkernel.checkpoint_and_execute(
                code, not autoexecute, parent_header=message.header, identities=identities
            )
            execute_request_msg = {
                name: getattr(execution_task.execute_request_msg, name)
                for name in execution_task.execute_request_msg.json_field_names
            }
            agent.context.send_response(
                "iopub",
                "add_child_codecell",
                {
                    "action": "code_cell",
                    "language": agent.context.subkernel.SLUG,
                    "code": code.strip(),
                    "autoexecute": autoexecute,
                    "execute_request_msg": execute_request_msg,
                    "checkpoint_index": checkpoint_index,
                },
                parent_header=message.header,
                parent_identities=getattr(message, "identities", None),
            )

            execution_context = await execution_task
        except Exception as err:
            logger.error(err, exc_info=err)
            raise
        return format_execution_context(execution_context)        

    @tool()
    async def regrid_dataset(
        self,
        dataset: str,
        target_resolution: tuple,
        agent: AgentRef,
        loop: LoopControllerRef,
        aggregation: Optional[str] = "interp_or_mean",
    ) -> str:
        """
        This tool should be used to show the user code to regrid a netcdf dataset with detectable geo-resolution.

        If a user asks to regrid a dataset, use this tool to return them code to regrid the dataset.

        If you are given a netcdf dataset, use this tool instead of any other regridding tool.

        If you are asked about what is needed to regrid a dataset, please provide information about the arguments of this tool.

        Args:
            dataset (str): The name of the dataset instantiated in the jupyter notebook.
            target_resolution (tuple): The target resolution to regrid to, e.g. (0.5, 0.5). This is in degrees longitude and latitude.
            aggregation (Optional): The aggregation function to be used in the regridding. The options are as follows:
                'conserve'
                'min'
                'max'
                'mean'
                'median'
                'mode'
                'interp_or_mean'
                'nearest_or_mode'

        Returns:
            str: Status of whether or not the dataset has been persisted to the HMI server.
        """

        loop.set_state(loop.STOP_SUCCESS)
        code = agent.context.get_code(
            "flowcast_regridding",
            {
                "dataset": dataset,
                "target_resolution": target_resolution,
                "aggregation": aggregation,
            },
        )

        result = json.dumps(
            {
                "action": "code_cell",
                "language": "python3",
                "content": code.strip(),
            }
        )

        return result

    @tool()
    async def get_netcdf_plot(
        self,
        dataset_variable_name: str,
        agent: AgentRef,
        loop: LoopControllerRef,
        plot_variable_name: Optional[str] = None,
        lat_col: Optional[str] = "lat",
        lon_col: Optional[str] = "lon",
        time_slice_index: Optional[int] = 1,
    ) -> str:
        """
        This function should be used to get a plot of a netcdf dataset.

        This function should also be used to preview any netcdf dataset.

        If the user asks to plot or preview a dataset, use this tool to return plotting code to them.

        You should also ask if the user wants to specify the optional arguments by telling them what each argument does.

        Args:
            dataset_variable_name (str): The name of the dataset instantiated in the jupyter notebook.
            plot_variable_name (Optional): The name of the variable to plot. Defaults to None.
                If None is provided, the first variable in the dataset will be plotted.
            lat_col (Optional): The name of the latitude column. Defaults to 'lat'.
            lon_col (Optional): The name of the longitude column. Defaults to 'lon'.
            time_slice_index (Optional): The index of the time slice to visualize. Defaults to 1.

        Returns:
            str: The code used to plot the netcdf.
        """

        code = agent.context.get_code(
            "get_netcdf_plot",
            {
                "dataset": dataset_variable_name,
                "plot_variable_name": plot_variable_name,
                "lat_col": lat_col,
                "lon_col": lon_col,
                "time_slice_index": time_slice_index,
            },
        )

        result = await agent.context.evaluate(
            code,
            parent_header={},
        )

        output = result.get("return")

        return output