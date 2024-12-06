# ESGF Python Client Documentation


---
subtitle: Search Concepts
title: Design Concepts
---

The `pyesgf.search` interface to ESGF search reflects the typical workflow of a user navigating through the sets of facets categorising available data.

# Keyword classification

The keyword arguments described in the [ESGF Search API](https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API) have a wide veriety of roles within the search workflow. To reflect this `pyesgf.search` classifies these keywords into system, spatiotemporal and facet keywords. Responsibility for these keywords are distributes across several classes.

## System keywords

| API keyword | class            | Notes                                                                                |
|-------------|------------------|--------------------------------------------------------------------------------------|
| limit       | SearchConnection | Set in `SearchConnection:send_query` method or transparently through `SearchContext` |
| offset      | SearchConnection | Set in `SearchConnection:send_query` method or transparently through `SearchContext` |
| shards      | SearchConnection | Set in constructor                                                                   |
| distrib     | SearchConnection | Set in constructor                                                                   |
| latest      | SearchContext    | Set in constructor                                                                   |
| facets      | SearchContext    | Set in constructor                                                                   |
| fields      | SearchContext    | Set in constructor                                                                   |
| replica     | SearchContext    | Set in constructor                                                                   |
| type        | SearchContext    | Create contexts with the right type using `ResultSet.file_context`, etc.             |
| from        | SearchContext    | Set in constructor. Use "from_timestamp" in the context API.                         |
| to          | SearchContext    | Set in constructor. Use "to_timestamp" in the context API.                           |
| fields      | n/a              | Managed internally                                                                   |
| format      | n/a              | Managed internally                                                                   |
| id          | n/a              | Managed internally                                                                   |

## Temporal keywords

Temporal keywords are supported for Dataset search. The terms "from_timestamp" and "to_timestamp" should be used with values following the format "YYYY-MM-DDThh:mm:ssZ".

## Spatial keywords

Spatial keywords are not yet supported by `pyesgf.search` however the API does have placeholders for these keywords anticipating future implementation:

## Facet keywords

All other keywords are considered to be search facets. The keyword "query" is dealt with specially as a freetext facet.

# Main Classes

## SearchConnection

`SearchConnection` instances represent a connection to an ESGF Search web service. This stores the service URL and also service-level parameters like distrib and shards.

## SearchContext

`SearchContext` represents the constraints on a given search. This includes the type of records you are searching for (File or Dataset), the list of possible facets with or without facet counts (depending on how the instance is created), currently selected facets/search-terms. Instances can return the number of hits and facet-counts associated with the current search.

SearchContext objects can be created in several ways:

> 1.  From a SearchConnection object using the method `SearchConnection.new_context`
> 2.  By further constraining an existing FacetContext object. E.g. new_context = context.constrain(institute='IPSL').
> 3.  From a Result object using one of it's *foo_context()* methods to create a context for searching for results related to the Result.
> 4.  Future development may implement project-specific factory. E.g. CMIP5FacetContext().

## ResultSet

`ResultSet` instances are returned by the `SearchContext.search` method and represent the results from a query. They supports transparent paging of results with a client-side cache.

## Result

`Result` instances represent the result record in the SOLr response. They are subclassed to represent records of different types: `FileResult` and `DatasetResult`. Results have various properties exposing information about the objects they represent. e.g. dataset_id, checksum, filename, size, etc.


---


# ESGF Python Client API Reference


# API Reference


# API ReferenceÂ¶


```python
>>> lm = LogonManager()
>>> lm.is_logged_on()
False
>>> lm.logon(username, password, myproxy_hostname, bootstrap=True)
>>> lm.is_logged_on()
True
```


```python
>>> lm.logoff()
>>> lm.is_logged_on()
False
>>> lm.logon_with_openid(openid, password, bootstrap=True)
>>> lm.is_logged_on()
True
```


> **Warning:**
> Warning
Prior to v0.1.1 the url parameter expected the full URL of the
search endpoint up to the query string.  This has now been changed
to expect url to ommit the final endpoint name,
e.g. https://esgf-node.llnl.gov/esg-search/search should be changed
to https://esgf-node.llnl.gov/esg-search in client code.  The
current implementation detects the presence of /search and
corrects the URL to retain backward compatibility but this feature
may not remain in future versions.


- **class pyesgf.search.connection.SearchConnection(url, distrib=True, cache=None, timeout=120, expire_after=datetime.timedelta(seconds=3600), session=None, verify=True, context_class=None)[source]Â¶** – Variables

url â The URL to the Search API service.  This should be the URL
of the ESGF search service excluding the final endpoint name.
Usually this is http://<hostname>/esg-search
distrib â Boolean stating whether searches through this connection are
distributed.  i.e. whether the Search service distributes the query to
other search peers.  See also the documentation for the facets
argument to pyesgf.search.context.SearchContext in relation to
distributed searches.
cache â Path to sqlite cache file. Cache expires every hours.
timeout â Time (in seconds) before query returns an error.
Default: 120s.
expire_after â Time delta after cache expires. Default: 1 hour.
session â requests.session object. optional.
verify â boolean, determines if query should be sent over a verified
channel.





get_shard_list()[source]Â¶
return the list of all available shards.  A subset of the returned list
can be supplied to âsend_query()â to limit the query to selected
shards.
Shards are described by hostname and mapped to SOLr shard descriptions
internally.

Returns
the list of available shards





new_context(context_class=None, latest=None, facets=None, fields=None, from_timestamp=None, to_timestamp=None, replica=None, shards=None, search_type=None, **constraints)[source]Â¶
Returns a pyesgf.search.context.SearchContext class for
performing faceted searches.
See SearchContext.__init__() for documentation on the
arguments.



send_search(query_dict, limit=None, offset=None, shards=None)[source]Â¶
Send a query to the âsearchâ endpoint.
See send_query() for details.

Returns
The json document for the search results





send_wget(query_dict, shards=None)[source]Â¶
Send a query to the âsearchâ endpoint.
See send_query() for details.

Returns
A string containing the script.

- **Variables** – url â The URL to the Search API service.  This should be the URL
of the ESGF search service excluding the final endpoint name.
Usually this is http://<hostname>/esg-search
distrib â Boolean stating whether searches through this connection are
distributed.  i.e. whether the Search service distributes the query to
other search peers.  See also the documentation for the facets
argument to pyesgf.search.context.SearchContext in relation to
distributed searches.
cache â Path to sqlite cache file. Cache expires every hours.
timeout â Time (in seconds) before query returns an error.
Default: 120s.
expire_after â Time delta after cache expires. Default: 1 hour.
session â requests.session object. optional.
verify â boolean, determines if query should be sent over a verified
channel.

- **get_shard_list()[source]Â¶** – return the list of all available shards.  A subset of the returned list
can be supplied to âsend_query()â to limit the query to selected
shards.
Shards are described by hostname and mapped to SOLr shard descriptions
internally.

Returns
the list of available shards

- **Returns** – the list of available shards

- **new_context(context_class=None, latest=None, facets=None, fields=None, from_timestamp=None, to_timestamp=None, replica=None, shards=None, search_type=None, **constraints)[source]Â¶** – Returns a pyesgf.search.context.SearchContext class for
performing faceted searches.
See SearchContext.__init__() for documentation on the
arguments.

- **send_search(query_dict, limit=None, offset=None, shards=None)[source]Â¶** – Send a query to the âsearchâ endpoint.
See send_query() for details.

Returns
The json document for the search results

- **Returns** – The json document for the search results

- **send_wget(query_dict, shards=None)[source]Â¶** – Send a query to the âsearchâ endpoint.
See send_query() for details.

Returns
A string containing the script.

- **Returns** – A string containing the script.



- **Variables** – url â The URL to the Search API service.  This should be the URL
of the ESGF search service excluding the final endpoint name.
Usually this is http://<hostname>/esg-search
distrib â Boolean stating whether searches through this connection are
distributed.  i.e. whether the Search service distributes the query to
other search peers.  See also the documentation for the facets
argument to pyesgf.search.context.SearchContext in relation to
distributed searches.
cache â Path to sqlite cache file. Cache expires every hours.
timeout â Time (in seconds) before query returns an error.
Default: 120s.
expire_after â Time delta after cache expires. Default: 1 hour.
session â requests.session object. optional.
verify â boolean, determines if query should be sent over a verified
channel.



- **get_shard_list()[source]Â¶** – return the list of all available shards.  A subset of the returned list
can be supplied to âsend_query()â to limit the query to selected
shards.
Shards are described by hostname and mapped to SOLr shard descriptions
internally.

Returns
the list of available shards

- **Returns** – the list of available shards



- **Returns** – the list of available shards



- **new_context(context_class=None, latest=None, facets=None, fields=None, from_timestamp=None, to_timestamp=None, replica=None, shards=None, search_type=None, **constraints)[source]Â¶** – Returns a pyesgf.search.context.SearchContext class for
performing faceted searches.
See SearchContext.__init__() for documentation on the
arguments.



- **send_search(query_dict, limit=None, offset=None, shards=None)[source]Â¶** – Send a query to the âsearchâ endpoint.
See send_query() for details.

Returns
The json document for the search results

- **Returns** – The json document for the search results



- **Returns** – The json document for the search results



- **send_wget(query_dict, shards=None)[source]Â¶** – Send a query to the âsearchâ endpoint.
See send_query() for details.

Returns
A string containing the script.

- **Returns** – A string containing the script.



- **Returns** – A string containing the script.



- **pyesgf.search.connection.create_single_session(cache=None, expire_after=datetime.timedelta(seconds=3600), **kwargs)[source]Â¶** – Simple helper function to start a requests or requests_cache session.
cache, if specified is a filename to a threadsafe sqlite database
expire_after specifies how long the cache should be kept



- **pyesgf.search.connection.query_keyword_type(keyword)[source]Â¶** – Returns the keyword type of a search query keyword.
Possible values are âsystemâ, âfreetextâ, âfacetâ, âtemporalâ and
âgeospatialâ.  If the keyword is unknown it is assumed to be a
facet keyword



- **class pyesgf.search.context.AggregationSearchContext(connection, constraints, search_type=None, latest=None, facets=None, fields=None, from_timestamp=None, to_timestamp=None, replica=None, shards=None)[source]Â¶** – 



- **class pyesgf.search.context.DatasetSearchContext(connection, constraints, search_type=None, latest=None, facets=None, fields=None, from_timestamp=None, to_timestamp=None, replica=None, shards=None)[source]Â¶** – 



- **class pyesgf.search.context.FileSearchContext(connection, constraints, search_type=None, latest=None, facets=None, fields=None, from_timestamp=None, to_timestamp=None, replica=None, shards=None)[source]Â¶** – 



- **class pyesgf.search.context.SearchContext(connection, constraints, search_type=None, latest=None, facets=None, fields=None, from_timestamp=None, to_timestamp=None, replica=None, shards=None)[source]Â¶** – Instances of this class represent the state of a current search.
It exposes what facets are available to select and the facet counts
if they are available.
Subclasses of this class can restrict the search options.  For instance
FileSearchContext, DatasetSerachContext or CMIP5SearchContext
SearchContext instances are connected to SearchConnection instances.  You
normally create SearchContext instances via one of:
1. Calling SearchConnection.new_context()
2. Calling SearchContext.constrain()

Variables

constraints â A dictionary of facet constraints currently in effect.
constraint[facet_name] = [value, value, ...]
facets â A string containing a comma-separated list of facets to be
returned (for example 'source_id,ensemble_id'). If set, this will
be used to select which facet counts to include, as returned in the
facet_counts dictionary.  Defaults to including all available
facets, but with distributed searches (where the SearchConnection
instance was created with distrib=True), some results may be
missing for server-side reasons when requesting all facets, so a
warning message will be issued. This contains further details.


Property facet_counts
A dictionary of available hits with each
facet value for the search as currently constrained.
This property returns a dictionary of dictionaries where
facet_counts[facet][facet_value] == hit_count

Property hit_count
The total number of hits available with current
constraints.




constrain(**constraints)[source]Â¶
Return a new instance with the additional constraints.



get_download_script(**constraints)[source]Â¶
Download a script for downloading all files in the set of results.

Parameters
constraints â Further constraints for this query. Equivalent
to calling self.constrain(**constraints).get_download_script()

Returns
A string containing the script





get_facet_options()[source]Â¶
Return a dictionary of facet counts filtered to remove all
facets that are completely constrained.  This method is
similar to the property facet_counts except facet values
which are not relevant for further constraining are removed.



search(batch_size=50, ignore_facet_check=False, **constraints)[source]Â¶
Perform the search with current constraints returning a set of results.

Batch_size
The number of results to get per HTTP request.

Ignore_facet_check
Do not make an extra HTTP request to populate
facet_counts and hit_count.

Parameters
constraints â Further constraints for this query.  Equivalent
to calling self.constrain(**constraints).search()

Returns
A ResultSet for this query

- **Variables** – constraints â A dictionary of facet constraints currently in effect.
constraint[facet_name] = [value, value, ...]
facets â A string containing a comma-separated list of facets to be
returned (for example 'source_id,ensemble_id'). If set, this will
be used to select which facet counts to include, as returned in the
facet_counts dictionary.  Defaults to including all available
facets, but with distributed searches (where the SearchConnection
instance was created with distrib=True), some results may be
missing for server-side reasons when requesting all facets, so a
warning message will be issued. This contains further details.

- **Property facet_counts** – A dictionary of available hits with each
facet value for the search as currently constrained.
This property returns a dictionary of dictionaries where
facet_counts[facet][facet_value] == hit_count

- **Property hit_count** – The total number of hits available with current
constraints.

- **constrain(**constraints)[source]Â¶** – Return a new instance with the additional constraints.

- **get_download_script(**constraints)[source]Â¶** – Download a script for downloading all files in the set of results.

Parameters
constraints â Further constraints for this query. Equivalent
to calling self.constrain(**constraints).get_download_script()

Returns
A string containing the script

- **Parameters** – constraints â Further constraints for this query. Equivalent
to calling self.constrain(**constraints).get_download_script()

- **Returns** – A string containing the script

- **get_facet_options()[source]Â¶** – Return a dictionary of facet counts filtered to remove all
facets that are completely constrained.  This method is
similar to the property facet_counts except facet values
which are not relevant for further constraining are removed.

- **search(batch_size=50, ignore_facet_check=False, **constraints)[source]Â¶** – Perform the search with current constraints returning a set of results.

Batch_size
The number of results to get per HTTP request.

Ignore_facet_check
Do not make an extra HTTP request to populate
facet_counts and hit_count.

Parameters
constraints â Further constraints for this query.  Equivalent
to calling self.constrain(**constraints).search()

Returns
A ResultSet for this query

- **Batch_size** – The number of results to get per HTTP request.

- **Ignore_facet_check** – Do not make an extra HTTP request to populate
facet_counts and hit_count.

- **Parameters** – constraints â Further constraints for this query.  Equivalent
to calling self.constrain(**constraints).search()

- **Returns** – A ResultSet for this query



- **Variables** – constraints â A dictionary of facet constraints currently in effect.
constraint[facet_name] = [value, value, ...]
facets â A string containing a comma-separated list of facets to be
returned (for example 'source_id,ensemble_id'). If set, this will
be used to select which facet counts to include, as returned in the
facet_counts dictionary.  Defaults to including all available
facets, but with distributed searches (where the SearchConnection
instance was created with distrib=True), some results may be
missing for server-side reasons when requesting all facets, so a
warning message will be issued. This contains further details.

- **Property facet_counts** – A dictionary of available hits with each
facet value for the search as currently constrained.
This property returns a dictionary of dictionaries where
facet_counts[facet][facet_value] == hit_count

- **Property hit_count** – The total number of hits available with current
constraints.



- **constrain(**constraints)[source]Â¶** – Return a new instance with the additional constraints.



- **get_download_script(**constraints)[source]Â¶** – Download a script for downloading all files in the set of results.

Parameters
constraints â Further constraints for this query. Equivalent
to calling self.constrain(**constraints).get_download_script()

Returns
A string containing the script

- **Parameters** – constraints â Further constraints for this query. Equivalent
to calling self.constrain(**constraints).get_download_script()

- **Returns** – A string containing the script



- **Parameters** – constraints â Further constraints for this query. Equivalent
to calling self.constrain(**constraints).get_download_script()

- **Returns** – A string containing the script



- **get_facet_options()[source]Â¶** – Return a dictionary of facet counts filtered to remove all
facets that are completely constrained.  This method is
similar to the property facet_counts except facet values
which are not relevant for further constraining are removed.



- **search(batch_size=50, ignore_facet_check=False, **constraints)[source]Â¶** – Perform the search with current constraints returning a set of results.

Batch_size
The number of results to get per HTTP request.

Ignore_facet_check
Do not make an extra HTTP request to populate
facet_counts and hit_count.

Parameters
constraints â Further constraints for this query.  Equivalent
to calling self.constrain(**constraints).search()

Returns
A ResultSet for this query

- **Batch_size** – The number of results to get per HTTP request.

- **Ignore_facet_check** – Do not make an extra HTTP request to populate
facet_counts and hit_count.

- **Parameters** – constraints â Further constraints for this query.  Equivalent
to calling self.constrain(**constraints).search()

- **Returns** – A ResultSet for this query



- **Batch_size** – The number of results to get per HTTP request.

- **Ignore_facet_check** – Do not make an extra HTTP request to populate
facet_counts and hit_count.

- **Parameters** – constraints â Further constraints for this query.  Equivalent
to calling self.constrain(**constraints).search()

- **Returns** – A ResultSet for this query



- **class pyesgf.search.results.AggregationResult(json, context)[source]Â¶** – A result object for ESGF aggregations.  Properties from BaseResultare inherited.



Property aggregation_id
The aggregation id

- **A result object for ESGF aggregations.  Properties from BaseResult** – are inherited.

- **Property aggregation_id** – The aggregation id



- **A result object for ESGF aggregations.  Properties from BaseResult** – are inherited.



- **Property aggregation_id** – The aggregation id



- **class pyesgf.search.results.BaseResult(json, context)[source]Â¶** – Base class for results.
Subclasses represent different search types such as File and Dataset.

Variables

json â The original json representation of the result.
context â The SearchContext which generated this result.


Property urls
a dictionary of the form
{service: [(url, mime_type), ...], ...}

Property opendap_url
The url of an OPeNDAP endpoint for this result
if available

Property las_url
The url of an LAS endpoint for this result if available

Property download_url
The url for downloading the result by HTTP
if available

Property gridftp_url
The url for downloading the result by Globus
if available

Property globus_url
The url for downloading the result by Globus
if available (including endpoint)

Property index_node
The index node from where the metadata is stored.
Calls to *_context() will optimise queries to only address this node.

- **Variables** – json â The original json representation of the result.
context â The SearchContext which generated this result.

- **Property urls** – a dictionary of the form
{service: [(url, mime_type), ...], ...}

- **Property opendap_url** – The url of an OPeNDAP endpoint for this result
if available

- **Property las_url** – The url of an LAS endpoint for this result if available

- **Property download_url** – The url for downloading the result by HTTP
if available

- **Property gridftp_url** – The url for downloading the result by Globus
if available

- **Property globus_url** – The url for downloading the result by Globus
if available (including endpoint)

- **Property index_node** – The index node from where the metadata is stored.
Calls to *_context() will optimise queries to only address this node.



- **Variables** – json â The original json representation of the result.
context â The SearchContext which generated this result.

- **Property urls** – a dictionary of the form
{service: [(url, mime_type), ...], ...}

- **Property opendap_url** – The url of an OPeNDAP endpoint for this result
if available

- **Property las_url** – The url of an LAS endpoint for this result if available

- **Property download_url** – The url for downloading the result by HTTP
if available

- **Property gridftp_url** – The url for downloading the result by Globus
if available

- **Property globus_url** – The url for downloading the result by Globus
if available (including endpoint)

- **Property index_node** – The index node from where the metadata is stored.
Calls to *_context() will optimise queries to only address this node.



- **class pyesgf.search.results.DatasetResult(json, context)[source]Â¶** – A result object for ESGF datasets.

Property dataset_id
The solr dataset_id which is unique throughout the
system.




aggregation_context()[source]Â¶
Return a SearchContext for searching for aggregations within this
dataset.



file_context()[source]Â¶
Return a SearchContext for searching for files within this dataset.



property number_of_filesÂ¶
Returns file count as reported by the dataset record.

- **Property dataset_id** – The solr dataset_id which is unique throughout the
system.

- **aggregation_context()[source]Â¶** – Return a SearchContext for searching for aggregations within this
dataset.

- **file_context()[source]Â¶** – Return a SearchContext for searching for files within this dataset.

- **property number_of_filesÂ¶** – Returns file count as reported by the dataset record.



- **Property dataset_id** – The solr dataset_id which is unique throughout the
system.



- **aggregation_context()[source]Â¶** – Return a SearchContext for searching for aggregations within this
dataset.



- **file_context()[source]Â¶** – Return a SearchContext for searching for files within this dataset.



- **property number_of_filesÂ¶** – Returns file count as reported by the dataset record.



- **class pyesgf.search.results.FileResult(json, context)[source]Â¶** – A result object for ESGF files.  Properties from BaseResult areinherited.



Property file_id
The identifier for the file

Property checksum
The checksum of the file

Property checksum_type
The algorithm used for generating the checksum

Property filename
The filename

Property size
The file size in bytes

- **A result object for ESGF files.  Properties from BaseResult are** – inherited.

- **Property file_id** – The identifier for the file

- **Property checksum** – The checksum of the file

- **Property checksum_type** – The algorithm used for generating the checksum

- **Property filename** – The filename

- **Property size** – The file size in bytes



- **A result object for ESGF files.  Properties from BaseResult are** – inherited.



- **Property file_id** – The identifier for the file

- **Property checksum** – The checksum of the file

- **Property checksum_type** – The algorithm used for generating the checksum

- **Property filename** – The filename

- **Property size** – The file size in bytes



- **class pyesgf.search.results.ResultSet(context, batch_size=50, eager=True)[source]Â¶** – Variables
context â The search context object used to generate this resultset

Property batch_size
The number of results that will be requested
from esgf-search as one call.  This must be set on creation and
cannot change.

- **Variables** – context â The search context object used to generate this resultset

- **Property batch_size** – The number of results that will be requested
from esgf-search as one call.  This must be set on creation and
cannot change.



- **Variables** – context â The search context object used to generate this resultset

- **Property batch_size** – The number of results that will be requested
from esgf-search as one call.  This must be set on creation and
cannot change.



- **class pyesgf.logon.LogonManager(esgf_dir='/home/docs/.esg', dap_config='/home/docs/.dodsrc', verify=True)[source]Â¶** – Manages ESGF crendentials and security configuration files.
Also integrates with NetCDFâs secure OPeNDAP configuration.


logoff(clear_trustroots=False)[source]Â¶
Remove any obtained credentials from the ESGF environment.

Parameters
clear_trustroots â If True also remove trustroots.





logon(username=None, password=None, hostname=None, bootstrap=False, update_trustroots=True, interactive=True)[source]Â¶
Obtain ESGF credentials from the specified MyProxy service.
If interactive == True then any missing parameters of password,
username or hostname will be prompted for at the terminal.

Parameters

interactive â Whether to ask for input at the terminal for
any missing information.  I.e. username, password or hostname.
bootstrap â Whether to bootstrap the trustroots for this
MyProxy service.
update_trustroots â Whether to update the trustroots for this
MyProxy service.






logon_with_openid(openid, password=None, bootstrap=False, update_trustroots=True, interactive=True)[source]Â¶
Obtains ESGF credentials by detecting the MyProxy parameters from
the users OpenID.  Some ESGF compatible OpenIDs do not contain enough
information to obtain credentials.  In this case the user is prompted
for missing information if interactive == True, otherwise an
exception is raised.

Parameters
openid â OpenID to login with See logon() for parameters
interactive, bootstrap and update_trustroots.

- **logoff(clear_trustroots=False)[source]Â¶** – Remove any obtained credentials from the ESGF environment.

Parameters
clear_trustroots â If True also remove trustroots.

- **Parameters** – clear_trustroots â If True also remove trustroots.

- **logon(username=None, password=None, hostname=None, bootstrap=False, update_trustroots=True, interactive=True)[source]Â¶** – Obtain ESGF credentials from the specified MyProxy service.
If interactive == True then any missing parameters of password,
username or hostname will be prompted for at the terminal.

Parameters

interactive â Whether to ask for input at the terminal for
any missing information.  I.e. username, password or hostname.
bootstrap â Whether to bootstrap the trustroots for this
MyProxy service.
update_trustroots â Whether to update the trustroots for this
MyProxy service.

- **Parameters** – interactive â Whether to ask for input at the terminal for
any missing information.  I.e. username, password or hostname.
bootstrap â Whether to bootstrap the trustroots for this
MyProxy service.
update_trustroots â Whether to update the trustroots for this
MyProxy service.

- **logon_with_openid(openid, password=None, bootstrap=False, update_trustroots=True, interactive=True)[source]Â¶** – Obtains ESGF credentials by detecting the MyProxy parameters from
the users OpenID.  Some ESGF compatible OpenIDs do not contain enough
information to obtain credentials.  In this case the user is prompted
for missing information if interactive == True, otherwise an
exception is raised.

Parameters
openid â OpenID to login with See logon() for parameters
interactive, bootstrap and update_trustroots.

- **Parameters** – openid â OpenID to login with See logon() for parameters
interactive, bootstrap and update_trustroots.



- **logoff(clear_trustroots=False)[source]Â¶** – Remove any obtained credentials from the ESGF environment.

Parameters
clear_trustroots â If True also remove trustroots.

- **Parameters** – clear_trustroots â If True also remove trustroots.



- **Parameters** – clear_trustroots â If True also remove trustroots.



- **logon(username=None, password=None, hostname=None, bootstrap=False, update_trustroots=True, interactive=True)[source]Â¶** – Obtain ESGF credentials from the specified MyProxy service.
If interactive == True then any missing parameters of password,
username or hostname will be prompted for at the terminal.

Parameters

interactive â Whether to ask for input at the terminal for
any missing information.  I.e. username, password or hostname.
bootstrap â Whether to bootstrap the trustroots for this
MyProxy service.
update_trustroots â Whether to update the trustroots for this
MyProxy service.

- **Parameters** – interactive â Whether to ask for input at the terminal for
any missing information.  I.e. username, password or hostname.
bootstrap â Whether to bootstrap the trustroots for this
MyProxy service.
update_trustroots â Whether to update the trustroots for this
MyProxy service.



- **Parameters** – interactive â Whether to ask for input at the terminal for
any missing information.  I.e. username, password or hostname.
bootstrap â Whether to bootstrap the trustroots for this
MyProxy service.
update_trustroots â Whether to update the trustroots for this
MyProxy service.



- **logon_with_openid(openid, password=None, bootstrap=False, update_trustroots=True, interactive=True)[source]Â¶** – Obtains ESGF credentials by detecting the MyProxy parameters from
the users OpenID.  Some ESGF compatible OpenIDs do not contain enough
information to obtain credentials.  In this case the user is prompted
for missing information if interactive == True, otherwise an
exception is raised.

Parameters
openid â OpenID to login with See logon() for parameters
interactive, bootstrap and update_trustroots.

- **Parameters** – openid â OpenID to login with See logon() for parameters
interactive, bootstrap and update_trustroots.



- **Parameters** – openid â OpenID to login with See logon() for parameters
interactive, bootstrap and update_trustroots.




---


# Code Examples from Notebooks



## Demo Notebooks



### subset-cmip5.ipynb

# Subset CMIP5 Datasets with xarray

xarray: http://xarray.pydata.org/en/stable/index.html

## Search CMIP5 Dataset with ESGF pyclient

using: https://esgf-pyclient.readthedocs.io/en/latest/index.html

```python
from pyesgf.search import SearchConnection
conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=True)
```

```python
ctx = conn.new_context(
    project='CMIP5', 
    experiment='rcp45',
    model='HadCM3',
    ensemble='r1i1p1',
    time_frequency='mon',
    realm='atmos',
    data_node='esgf-data1.ceda.ac.uk',
    )
ctx.hit_count
```

```python
result = ctx.search()[0]
result.dataset_id
```

```python
files = result.file_context().search()
for file in files:
    if 'tasmax' in file.opendap_url:
        tasmax_url = file.opendap_url
        print(tasmax_url)
```

## ESGF Logon

```python
from pyesgf.logon import LogonManager
lm = LogonManager()
lm.logoff()
lm.is_logged_on()
```

```python
lm.logon(hostname='esgf-data.dkrz.de', interactive=True, bootstrap=True)
lm.is_logged_on()
```

## Subset single dataset with xarray

Using OpenDAP: http://xarray.pydata.org/en/stable/io.html?highlight=opendap#opendap

```python
import xarray as xr
ds = xr.open_dataset(tasmax_url, chunks={'time': 120})
print(ds)
```

```python
da = ds['tasmax']
da = da.isel(time=slice(0, 1))
da = da.sel(lat=slice(-50, 50), lon=slice(0, 50))

```

```python
%matplotlib inline
da.plot()
```

## Download to NetCDF

```python
da.to_netcdf('tasmax.nc')
```

---


### subset-cmip5.ipynb

# Subset CMIP5 Datasets with xarray

xarray: http://xarray.pydata.org/en/stable/index.html

## Search CMIP5 Dataset with ESGF pyclient

using: https://esgf-pyclient.readthedocs.io/en/latest/index.html

```python
from pyesgf.search import SearchConnection
conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=True)
```

```python
ctx = conn.new_context(
    project='CMIP5', 
    experiment='rcp45',
    model='HadCM3',
    ensemble='r1i1p1',
    time_frequency='mon',
    realm='atmos',
    data_node='esgf-data1.ceda.ac.uk',
    )
ctx.hit_count
```

```python
result = ctx.search()[0]
result.dataset_id
```

```python
files = result.file_context().search()
for file in files:
    if 'tasmax' in file.opendap_url:
        tasmax_url = file.opendap_url
        print(tasmax_url)
```

## ESGF Logon

```python
from pyesgf.logon import LogonManager
lm = LogonManager()
lm.logoff()
lm.is_logged_on()
```

```python
lm.logon(hostname='esgf-data.dkrz.de', interactive=True, bootstrap=True)
lm.is_logged_on()
```

## Subset single dataset with xarray

Using OpenDAP: http://xarray.pydata.org/en/stable/io.html?highlight=opendap#opendap

```python
import xarray as xr
ds = xr.open_dataset(tasmax_url, chunks={'time': 120})
print(ds)
```

```python
da = ds['tasmax']
da = da.isel(time=slice(0, 1))
da = da.sel(lat=slice(-50, 50), lon=slice(0, 50))

```

```python
%matplotlib inline
da.plot()
```

## Download to NetCDF

```python
da.to_netcdf('tasmax.nc')
```

---


### subset-cmip6.ipynb

# Subset CMIP6 Datasets with xarray

xarray: http://xarray.pydata.org/en/stable/index.html

## Search CMIP6 Dataset with ESGF pyclient

using: https://esgf-pyclient.readthedocs.io/en/latest/index.html

```python
from pyesgf.search import SearchConnection
conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=True)
```

```python
ctx = conn.new_context(
    project='CMIP6', 
    source_id='UKESM1-0-LL', 
    experiment_id='historical', 
    variable='tas', 
    frequency='mon', 
    variant_label='r1i1p1f2',
    data_node='esgf-data3.ceda.ac.uk')
ctx.hit_count
```

```python
result = ctx.search()[0]
result.dataset_id
```

```python
files = result.file_context().search()
for file in files:
    print(file.opendap_url)
```

## Subset single dataset with xarray

Using OpenDAP: http://xarray.pydata.org/en/stable/io.html?highlight=opendap#opendap

```python
import xarray as xr
ds = xr.open_dataset(files[0].opendap_url, chunks={'time': 120})
print(ds)
```

```python
da = ds['tas']
da = da.isel(time=slice(0, 1))
da = da.sel(lat=slice(-50, 50), lon=slice(0, 50))

```

```python
%matplotlib inline
da.plot()
```

## Subset over multiple datasets


```python
ds_agg = xr.open_mfdataset([files[0].opendap_url, files[1].opendap_url], chunks={'time': 120}, combine='nested', concat_dim='time')
print(ds_agg)
```

```python
da = ds_agg['tas']
da = da.isel(time=slice(1200, 1201))
da = da.sel(lat=slice(-50, 50), lon=slice(0, 50))
```

```python
da.plot()
```

## Download dataset

```python
da.to_netcdf('tas_africa_19500116.nc')
```

---


### subset-cmip6.ipynb

# Subset CMIP6 Datasets with xarray

xarray: http://xarray.pydata.org/en/stable/index.html

## Search CMIP6 Dataset with ESGF pyclient

using: https://esgf-pyclient.readthedocs.io/en/latest/index.html

```python
from pyesgf.search import SearchConnection
conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=True)
```

```python
ctx = conn.new_context(
    project='CMIP6', 
    source_id='UKESM1-0-LL', 
    experiment_id='historical', 
    variable='tas', 
    frequency='mon', 
    variant_label='r1i1p1f2',
    data_node='esgf-data3.ceda.ac.uk')
ctx.hit_count
```

```python
result = ctx.search()[0]
result.dataset_id
```

```python
files = result.file_context().search()
for file in files:
    print(file.opendap_url)
```

## Subset single dataset with xarray

Using OpenDAP: http://xarray.pydata.org/en/stable/io.html?highlight=opendap#opendap

```python
import xarray as xr
ds = xr.open_dataset(files[0].opendap_url, chunks={'time': 120})
print(ds)
```

```python
da = ds['tas']
da = da.isel(time=slice(0, 1))
da = da.sel(lat=slice(-50, 50), lon=slice(0, 50))

```

```python
%matplotlib inline
da.plot()
```

## Subset over multiple datasets


```python
ds_agg = xr.open_mfdataset([files[0].opendap_url, files[1].opendap_url], chunks={'time': 120}, combine='nested', concat_dim='time')
print(ds_agg)
```

```python
da = ds_agg['tas']
da = da.isel(time=slice(1200, 1201))
da = da.sel(lat=slice(-50, 50), lon=slice(0, 50))
```

```python
da.plot()
```

## Download dataset

```python
da.to_netcdf('tas_africa_19500116.nc')
```

---


## Examples Notebooks



# General Information about the ESGF API


<div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">

<div itemprop="articleBody">

<div id="the-esgf-search-restful-api" class="section">

# The ESGF Search RESTful API<a href="#the-esgf-search-restful-api" class="headerlink" title="Permalink to this headline">¶</a>

The ESGF search service exposes a RESTful URL that can be used by clients (browsers and desktop clients) to query the contents of the underlying search index, and return results matching the given constraints. Because of the distributed capabilities of the ESGF search, the URL at any Index Node can be used to query that Node only, or all Nodes in the ESGF system.

<div id="syntax" class="section">

## Syntax<a href="#syntax" class="headerlink" title="Permalink to this headline">¶</a>

The general syntax of the ESGF search service URL is:

<div class="highlight-console notranslate">

<div class="highlight">

    http://<index-node>/esg-search/search?[keyword parameters as (name, value) pairs][facet parameters as (name,value) pairs]

</div>

</div>

where “” is the base URL of the search service at a given Index Node.

All parameters (keyword and facet) are optional. Also, the value of all parameters must be URL-encoded, so that the complete search URL is well formed.

</div>

<div id="keywords" class="section">

## Keywords<a href="#keywords" class="headerlink" title="Permalink to this headline">¶</a>

Keyword parameters are query parameters that have reserved names, and are interpreted by the search service to control the fundamental nature of a search request: where to issue the request to, how many results to return, etc.

The following keywords are currently used by the system - see later for usage examples:

- facets= to return facet values and counts

- offset= , limit= to paginate through the available results (default: offset=0, limit=10)

- fields= to return only specific metadata fields for each matching result (default: fields=\*)

- format= to specify the response document output format

- type= (searches record of the specified type: Dataset, File or Aggregation)

- replica=false/true (searches for all records, or records that are NOT replicas)

- latest=true/false (searches for just the latest version, or all versions)

- distrib=true/false (searches across all nodes, or the target node only)

- shards= (searches the specified shards only)

- bbox=\[west, south, east, north\] (searches within a geo-spatial box)

- start=, end= (select records based on their nominal data coverage, i.e. their datetime_start, datetime_stop values )

- from=, to= (select records based on when the data was marked as last modified, i.e. their nominal “timestamp” value)

</div>

<div id="default-query" class="section">

## Default Query<a href="#default-query" class="headerlink" title="Permalink to this headline">¶</a>

If no parameters at all are specified, the search service will execute a query using all the default values, specifically:

- query=\* (query all records)

- distrib=true (execute a distributed search)

- type=Dataset (return results of type “Dataset”)

Example:

- <a href="http://esgf-node.llnl.gov/esg-search/search" class="reference external">http://esgf-node.llnl.gov/esg-search/search</a>

</div>

<div id="free-text-queries" class="section">

## Free Text Queries<a href="#free-text-queries" class="headerlink" title="Permalink to this headline">¶</a>

The keyword parameter query= can be specified to execute a query that matches the given text \_ anywhere \_ in the records metadata fields. The parameter value can be any expression following the Apache Lucene query syntax (because it is passed “as-is” to the back-end Solr query), and must be URL- encoded. When using the CoG user interface at any ESGF node and project, the “query=” parameter value must be entered in the text field at the top of the page.

Examples:

- Search for any text, anywhere: <a href="http://esgf-node.llnl.gov/esg-search/search?query=*" class="reference external">http://esgf-node.llnl.gov/esg-search/search?query=*</a> (the default value of the query parameter)

- Search for “humidity” in all metadata fields: <a href="http://esgf-node.llnl.gov/esg-search/search?query=humidity" class="reference external">http://esgf-node.llnl.gov/esg-search/search?query=humidity</a>

- Search for the exact sentence “specific humidity” in all metadata fields (the sentence must be surrounded by quotes and URL-encoded): <a href="http://esgf-node.llnl.gov/esg-search/search?query=%22specific%20humidity%22" class="reference external">http://esgf-node.llnl.gov/esg-search/search?query=%22specific%20humidity%22</a>

- Search for both words “specific” and “humidity”, but not necessarily in an exact sequence (must use a space between the two words = this is the same as executing a query with the logical OR): <a href="http://esgf-node.llnl.gov/esg-search/search?query=specific%20humidity" class="reference external">http://esgf-node.llnl.gov/esg-search/search?query=specific%20humidity</a>

- Search for the word “observations” ONLY in the metadata field “product” : <a href="http://esgf-node.llnl.gov/esg-search/search?query=product:observations" class="reference external">http://esgf-node.llnl.gov/esg-search/search?query=product:observations</a>

- Using logical AND: <a href="http://esgf-node.llnl.gov/esg-search/search?query=airs%20AND%20humidity" class="reference external">http://esgf-node.llnl.gov/esg-search/search?query=airs%20AND%20humidity</a> (must use upper case “AND”)

- Using logical OR: <a href="http://esgf-node.llnl.gov/esg-search/search?query=airs%20OR%20humidity" class="reference external">http://esgf-node.llnl.gov/esg-search/search?query=airs%20OR%20humidity</a> (must use upper case “OR”). This is the same as using simply a blank space: <a href="http://esgf-node.llnl.gov/esg-search/search?query=airs%20humidity" class="reference external">http://esgf-node.llnl.gov/esg-search/search?query=airs%20humidity</a> )

- Search for a dataset with a specific id: <a href="http://esgf-node.llnl.gov/esg-search/search?query=id:obs4MIPs.NASA-JPL.AIRS.hus.mon" class="reference external">http://esgf-node.llnl.gov/esg-search/search?query=id:obs4MIPs.NASA-JPL.AIRS.hus.mon</a>.v20110608\|esgf-data.llnl.gov

- Search for all datasets that match an id pattern: <a href="http://esgf-node.llnl.gov/esg-search/search?query=id:obs4MIPs.NASA-JPL.AIRS.*" class="reference external">http://esgf-node.llnl.gov/esg-search/search?query=id:obs4MIPs.NASA-JPL.AIRS.*</a>

</div>

<div id="facet-queries" class="section">

## Facet Queries<a href="#facet-queries" class="headerlink" title="Permalink to this headline">¶</a>

A request to the search service can be constrained to return only those records that match specific values for one or more facets. Specifically, a facet constraint is expressed through the general form: =, where is chosen from the controlled vocabulary of facet names configured at each site, and must match exactly one of the possible values for that particular facet.

When specifying more than one facet constraint in the request, multiple values for the same facet are combined with a logical OR, while multiple values for different facets are combined with a logical AND. Also, multiple possible values for teh same facets can be expressed as a comma-separated list. For example:

- experiment=decadal2000&variable=hus : will return all records that match experiment=decadal2000 AND variable=hus

- variable=hus&variable=ta : will return all records that match variable=hus OR variable=ta

- variable=hus,ta : will also return all records that match variable=hus OR variable=ta

A facet constraint can be negated by using the != operator. For example, model!=CCSM searches for all items that do NOT match the CCSM model. Note that all negative facets are combined in logical AND, for example, model!=CCSM&model!=HadCAM searches for all items that do not match CCSM, and do not match HadCAM.

By default, no facet counts are returned in the output document. Facet counts must be explicitly requested by specifying the facet names individually (for example: facets=experiment,model) or via the special notation facets=\*. The facets list must be comma-separated, and white spaces are ignored.

If facet counts is requested, facet values are sorted alphabetically (facet.sort=lex), and all facet values are returned (facet.limit=-1), provided they match one or more records (facet.mincount=1)

The “type” facet must be always specified as part of any request to the ESGF search services, so that the appropriate records can be searched and returned. If not specified explicitly, the default value is type=Dataset .

Examples:

- Single facet query: <a href="http://esgf-node.llnl.gov/esg-search/search?cf_standard_name=air_temperature" class="reference external">http://esgf-node.llnl.gov/esg-search/search?cf_standard_name=air_temperature</a>

- Query with two different facet constraints: <a href="http://esgf-node.llnl.gov/esg-search/search?cf_standard_name=air_temperature&amp;project=obs4MIPs" class="reference external">http://esgf-node.llnl.gov/esg-search/search?cf_standard_name=air_temperature&amp;project=obs4MIPs</a>

- Combining two values of the same facet with a logical OR: <a href="http://esgf-node.llnl.gov/esg-search/search?project=obs4MIPs&amp;variable=hus&amp;variable=ta" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=obs4MIPs&amp;variable=hus&amp;variable=ta</a> (search for all obs4MIPs files that have variable “ta” OR variable “hus”)

- Using a negative facet:

  - <a href="http://esgf-node.llnl.gov/esg-search/search?project=obs4MIPs&amp;variable=hus&amp;variable=ta&amp;model!=Obs-AIRS" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=obs4MIPs&amp;variable=hus&amp;variable=ta&amp;model!=Obs-AIRS</a> (search for all obs4MIPs datasets that have variable ta OR hus, excluding those produced by AIRS)

  - <a href="http://esgf-node.llnl.gov/esg-search/search?project=obs4MIPs&amp;variable!=ta&amp;variable!=huss" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=obs4MIPs&amp;variable!=ta&amp;variable!=huss</a> (search for all obs4MIPs datasets that do not contain neither variable ta nor variable huss)

- Search a file by its tracking id: <a href="http://esgf-node.llnl.gov/esg-search/search?type=File&amp;tracking_id=2209a0d0-9b77-4ecb-b2ab-b7ae412e7a3f" class="reference external">http://esgf-node.llnl.gov/esg-search/search?type=File&amp;tracking_id=2209a0d0-9b77-4ecb-b2ab-b7ae412e7a3f</a>

- Search a file by its checksum: <a href="http://esgf-node.llnl.gov/esg-search/search?type=File&amp;checksum=83df8ae93e85e26df797d5f770449470987a4ecd8f2d405159995b5cac9a410c" class="reference external">http://esgf-node.llnl.gov/esg-search/search?type=File&amp;checksum=83df8ae93e85e26df797d5f770449470987a4ecd8f2d405159995b5cac9a410c</a>

- Issue a query for all supported facets and their values at one site, while returning no results (note that only facets with one or more values are returned): <a href="http://esgf-node.llnl.gov/esg-search/search?facets=*&amp;limit=0&amp;distrib=false" class="reference external">http://esgf-node.llnl.gov/esg-search/search?facets=*&amp;limit=0&amp;distrib=false</a>

</div>

<div id="facet-listings" class="section">

## Facet Listings<a href="#facet-listings" class="headerlink" title="Permalink to this headline">¶</a>

The available facet names and values for searching data within a specific project can be listed with a query of the form …project=&facets=\*&limit=0 (i.e. return no results). Only facet values that match one or more records will be returned.

Examples:

- List all obs4MIPs facet names and values: <a href="http://esgf-node.llnl.gov/esg-search/search?project=obs4MIPs&amp;facets=*&amp;limit=0" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=obs4MIPs&amp;facets=*&amp;limit=0</a>

- List all CMIP5 facet names and values: <a href="http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;facets=*&amp;limit=0" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;facets=*&amp;limit=0</a>

The same query with no project constraint will return all facet names and values for ALL data across the federation:

- List ALL facet names and values: <a href="http://esgf-node.llnl.gov/esg-search/search?facets=*&amp;limit=0" class="reference external">http://esgf-node.llnl.gov/esg-search/search?facets=*&amp;limit=0</a>

To retrieve a listing of available values for only a few facets, simply specify a comma-separated list of facet names:

- List all values of model, experiment and project throughout the federation: <a href="http://esgf-node.llnl.gov/esg-search/search?facets=model,experiment,project&amp;limit=0" class="reference external">http://esgf-node.llnl.gov/esg-search/search?facets=model,experiment,project&amp;limit=0</a>

- List all values of model, experiment for CMIP5 data: <a href="http://esgf-node.llnl.gov/esg-search/search?facets=model,experiment&amp;project=CMIP5&amp;limit=0" class="reference external">http://esgf-node.llnl.gov/esg-search/search?facets=model,experiment&amp;project=CMIP5&amp;limit=0</a>

</div>

<div id="temporal-coverage-queries" class="section">

## Temporal Coverage Queries<a href="#temporal-coverage-queries" class="headerlink" title="Permalink to this headline">¶</a>

The keyword parameters start= and/or end= can be used to query for data with temporal coverage that overlaps the specified range. The parameter values can either be date-times in the format “YYYY-MM-DDTHH:MM:SSZ” (UTC ISO 8601 format), or special values supported by the Solr DateMath syntax.

Examples:

- Search for data in the past year: <a href="http://esgf-node.llnl.gov/esg-search/search?start=NOW-1YEAR" class="reference external">http://esgf-node.llnl.gov/esg-search/search?start=NOW-1YEAR</a> (translates into the constraint datetime_stop:\[NOW-1YEAR TO \*\] or datetime_stop \> NOW-1YEAR)

- Search for data before the year 2000: <a href="http://esgf-node.llnl.gov/esg-search/search?end=2000-01-01T00:00:00Z" class="reference external">http://esgf-node.llnl.gov/esg-search/search?end=2000-01-01T00:00:00Z</a> (translates into the constraint datetime_start:\[\* TO 2000-01-01T00:00:00Z\] or datetime_start \< 2000-01-01)

</div>

<div id="spatial-coverage-queries" class="section">

## Spatial Coverage Queries<a href="#spatial-coverage-queries" class="headerlink" title="Permalink to this headline">¶</a>

The keyword parameter bbox=\[west, south, east, north\] can be used to query for data with spatial coverage that overlaps the given bounding box. As usual, the parameter value must be URL-encoded.

Examples:

- <a href="http://esgf-node.llnl.gov/esg-search/search?bbox=%5B-10,-10,+10,+10%5D" class="reference external">http://esgf-node.llnl.gov/esg-search/search?bbox=%5B-10,-10,+10,+10%5D</a> ( translates to: east_degrees:\[-10 TO \*\] AND north_degrees:\[-10 TO \*\] AND west_degrees:\[\* TO 10\] AND south_degrees:\[\* TO 10\] )

Please note though that NOT all ESGF records contain geo-spatial information, and therefore will not be returned by a geo-spatial search.

</div>

<div id="distributed-queries" class="section">

## Distributed Queries<a href="#distributed-queries" class="headerlink" title="Permalink to this headline">¶</a>

The keyword parameter distrib= can be used to control whether the query is executed versus the local Index Node only, or distributed to all other Nodes in the federation. If not specified, the default value distrib=true is assumed.

Examples:

- Search for all datasets in the federation: <a href="http://esgf-node.llnl.gov/esg-search/search?distrib=true" class="reference external">http://esgf-node.llnl.gov/esg-search/search?distrib=true</a>

- Search for all datasets at one Node only: <a href="http://esgf-node.llnl.gov/esg-search/search?distrib=false" class="reference external">http://esgf-node.llnl.gov/esg-search/search?distrib=false</a>

</div>

<div id="shard-queries" class="section">

## Shard Queries<a href="#shard-queries" class="headerlink" title="Permalink to this headline">¶</a>

By default, a distributed query (distrib=true) targets all ESGF Nodes in the current peer group, i.e. all nodes that are listed in the local configuration file /esg/config/esgf_shards.xml , which is continuously updated by the local node manager to reflect the latest state of the federation. It is possible to execute a distributed search that targets only one or more specific nodes, by specifying them in the “shards” parameter, as such: shards=hostname1:port1/solr,hostname2:port2/solr,…. . Note that the explicit shards value is ignored if distrib=false (but distrib=true by default if not otherwise specified).

Examples:

- Query for CMIP5 data at the PCMDI and CEDA sites only: <a href="http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;shards=pcmdi.llnl.gov/solr,esgf-index1.ceda.ac.uk/solr" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;shards=pcmdi.llnl.gov/solr,esgf-index1.ceda.ac.uk/solr</a>

- Query for all files belonging to a given dataset at one site only: <a href="http://esgf-node.llnl.gov/esg-search/search?type=File&amp;shards=esgf-node.llnl.gov/solr&amp;dataset_id=obs4MIPs.NASA-JPL.TES.tro3.mon" class="reference external">http://esgf-node.llnl.gov/esg-search/search?type=File&amp;shards=esgf-node.llnl.gov/solr&amp;dataset_id=obs4MIPs.NASA-JPL.TES.tro3.mon</a>.v20110608\|esgf-data.llnl.gov

</div>

<div id="replica-queries" class="section">

## Replica Queries<a href="#replica-queries" class="headerlink" title="Permalink to this headline">¶</a>

Replicas (Datasets and Files) are distinguished from the original record (a.k.a. the “master”) in the Solr index by the value of two special keywords:

- replica: a flag that is set to false for master records, true for replica records.

- master_id: a string that is identical for the master and all replicas of a given logical record (Dataset or File).

By default, a query returns all records (masters and replicas) matching the search criteria, i.e. no replica=… constraint is used. To return only master records, use replica=false, to return only replicas, use replica=true. To search for all identical Datasets or Files (i.e. for the master AND replicas of a Dataset or File), use master_id=….

Examples:

- Search for all datasets in the system (masters and replicas): <a href="http://esgf-node.llnl.gov/esg-search/search" class="reference external">http://esgf-node.llnl.gov/esg-search/search</a>

- Search for just master datasets, no replicas: <a href="http://esgf-node.llnl.gov/esg-search/search?replica=false" class="reference external">http://esgf-node.llnl.gov/esg-search/search?replica=false</a>

- Search for just replica datasets, no masters: <a href="http://esgf-node.llnl.gov/esg-search/search?replica=true" class="reference external">http://esgf-node.llnl.gov/esg-search/search?replica=true</a>

- Search for the master AND replicas of a given dataset: <a href="http://esgf-node.llnl.gov/esg-search/search?master_id=cmip5.output1.LASG-CESS.FGOALS-g2.midHolocene.3hr.land.3hr.r1i1p1" class="reference external">http://esgf-node.llnl.gov/esg-search/search?master_id=cmip5.output1.LASG-CESS.FGOALS-g2.midHolocene.3hr.land.3hr.r1i1p1</a>

- Search for the master and replicas of a given file: <a href="http://esgf-node.llnl.gov/esg-search/search?type=File&amp;master_id=cmip5.output1.MIROC.MIROC5.decadal1978.mon.ocean.Omon.r4i1p1.wfo_Omon_MIROC5_decadal1978_r4i1p1_197901-198812.nc" class="reference external">http://esgf-node.llnl.gov/esg-search/search?type=File&amp;master_id=cmip5.output1.MIROC.MIROC5.decadal1978.mon.ocean.Omon.r4i1p1.wfo_Omon_MIROC5_decadal1978_r4i1p1_197901-198812.nc</a>

</div>

<div id="latest-and-version-queries" class="section">

## Latest and Version Queries<a href="#latest-and-version-queries" class="headerlink" title="Permalink to this headline">¶</a>

By default, a query to the ESGF search services will return all versions of the matching records (Datasets or Files). To only return the very last, up-to-date version include latest=true . To return a specific version, use version=… . Using latest=false will return only datasets that were superseded by newer versions.

Examples:

- Search for all latest CMIP5 datasets: <a href="http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;latest=true" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;latest=true</a>

- Search for all versions of a given dataset: <a href="http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;master_id=cmip5.output1.MOHC.HadCM3.decadal1972.day.atmos.day.r10i2p1&amp;facets=version" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;master_id=cmip5.output1.MOHC.HadCM3.decadal1972.day.atmos.day.r10i2p1&amp;facets=version</a>

- Search for a specific version of a given dataset: <a href="http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;master_id=cmip5.output1.NSF-DOE-NCAR.CESM1-CAM5-1-FV2.historical.mon.atmos.Amon.r1i1p1&amp;version=20120712" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;master_id=cmip5.output1.NSF-DOE-NCAR.CESM1-CAM5-1-FV2.historical.mon.atmos.Amon.r1i1p1&amp;version=20120712</a>

</div>

<div id="retracted-queries" class="section">

## Retracted Queries<a href="#retracted-queries" class="headerlink" title="Permalink to this headline">¶</a>

NOTE: this feature is NOT yet released

Retracted datasets are marked by “retracted=true”, and also have the flag “latest=false” set. Consequently, retracted datasets are automatically NOT included in any search for the latest version data (“latest=true”), while they are automatically included in searches the span all versions (no “latest” constraint). To search specifically for only retracted datasets, use the constraint “retracted=true”.

Example:

- Search for all retracted datasets in the CMIP5 project, across all nodes: <a href="https://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;retracted=true" class="reference external">https://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;retracted=true</a>

</div>

<div id="minimum-and-maximum-version-queries" class="section">

## Minimum and Maximum Version Queries<a href="#minimum-and-maximum-version-queries" class="headerlink" title="Permalink to this headline">¶</a>

NOTE: this feature is NOT yet released

The special keywords “min_version” and “max_version” can be used to query for all records that have a version greater or equal, or less or equal, of a given numerical value. Because often in ESGF versions are expressed as dates of the format YYYYMMDD, it is possible to query for all records that have a version greater/less or equal of a certain date. The two constraints can be combined with each other to specify a version (aka date) range, and can also be combined with other constraints.

Examples:

- All datasets with version less than a given date: <a href="https://esgf-node.llnl.gov/esg-search/search?max_version=20150101" class="reference external">https://esgf-node.llnl.gov/esg-search/search?max_version=20150101</a>

- All Obs4MIPs datasets with version between two dates: <a href="http://esgf-node.llnl.gov/esg-search/search?min_version=20120101&amp;max_version=20131231&amp;project=obs4MIPs" class="reference external">http://esgf-node.llnl.gov/esg-search/search?min_version=20120101&amp;max_version=20131231&amp;project=obs4MIPs</a>

</div>

<div id="results-pagination" class="section">

## Results Pagination<a href="#results-pagination" class="headerlink" title="Permalink to this headline">¶</a>

By default, a query to the search service will return the first 10 records matching the given constraints. The offset into the returned results, and the total number of returned results, can be changed through the keyword parameters limit= and offset= . The system imposes a maximum value of limit \<= 10,000.

Examples:

- Query for 100 CMIP5 datasets in the system: <a href="http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;limit=100" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;limit=100</a>

- Query for the next 100 CMIP5 datasets in the system: <a href="http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;limit=100&amp;offset=100" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;limit=100&amp;offset=100</a>

</div>

<div id="output-format" class="section">

## Output Format<a href="#output-format" class="headerlink" title="Permalink to this headline">¶</a>

The keyword parameter output= can be used to request results in a specific output format. Currently the only available options are Solr/XML (the default) and Solr/JSON.

Examples:

- Request results in Solr XML format: <a href="http://esgf-node.llnl.gov/esg-search/search?format=application%2Fsolr%2Bxml" class="reference external">http://esgf-node.llnl.gov/esg-search/search?format=application%2Fsolr%2Bxml</a>

- Request results in Solr JSON format: <a href="http://esgf-node.llnl.gov/esg-search/search?format=application%2Fsolr%2Bjson" class="reference external">http://esgf-node.llnl.gov/esg-search/search?format=application%2Fsolr%2Bjson</a>

</div>

<div id="returned-metadata-fields" class="section">

## Returned Metadata Fields<a href="#returned-metadata-fields" class="headerlink" title="Permalink to this headline">¶</a>

By default, all available metadata fields are returned for each result. The keyword parameter fields= can be used to limit the number of fields returned in the response document, for each matching result. The list must be comma-separated, and white spaces are ignored. Use fields=\* to return all fields (same as not specifiying it, since it is the default). Note that the pseudo field “score” is always appended to any fields list.

Examples:

- Return all available metadata fields for CMIP5 datasets: <a href="http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;fields=*" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;fields=*</a>

- Return only the “model” and “experiment” fields for CMIP5 datasets: <a href="http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;fields=model,experiment" class="reference external">http://esgf-node.llnl.gov/esg-search/search?project=CMIP5&amp;fields=model,experiment</a>

</div>

<div id="identifiers" class="section">

## Identifiers<a href="#identifiers" class="headerlink" title="Permalink to this headline">¶</a>

Each search record in the system is assigned the following identifiers (all of type string):

- id : universally unique for each record across the federation, i.e. specific to each Dataset or File, version and replica (and the data node storing the data). It is intended to be “opaque”, i.e. it should not be parsed by clients to extract any information.

  - Dataset example: id=obs4MIPs.NASA-JPL.TES.tro3.mon.v20110608\|esgf-data.llnl.gov

  - File example: id=obs4MIPs.NASA-JPL.TES.tro3.mon.v20110608.tro3Stderr_TES_L3_tbd_200507-200912.nc\|esgf-data.llnl.gov

- master_id : same for all replicas and versions across the federation. When parsing THREDDS catalogs, it is extracted from the properties “dataset_id” or “file_id”.

  - Dataset example: obs4MIPs.NASA-JPL.TES.tro3.mon (for a Dataset)

  - File example: obs4MIPs.NASA-JPL.TES.tro3.mon.tro3Stderr_TES_L3_tbd_200507-200912.nc

- instance_id : same for all replicas across federation, but specific to each version. When parsing THREDDS catalogs, it is extracted from the ID attribute of the corresponding THREDDS catalog element (for both Datasets and Files).

  - Dataset example: obs4MIPs.NASA-JPL.TES.tro3.mon.v20110608

  - File example: obs4MIPs.NASA-JPL.TES.tro3.mon.v20110608.tro3Stderr_TES_L3_tbd_200507-200912.nc

Note also that the record version is the same for all replicas of that record, but different across versions. Examples:

- Dataset example: version=20110608

- File example: version=1

</div>

<div id="access-urls" class="section">

## Access URLs<a href="#access-urls" class="headerlink" title="Permalink to this headline">¶</a>

In the Solr output document returned by a search, URLs that are access points for Datasets and Files are encoded as 3-tuple of the form “url\|mime type\|service name”, where the fields are separated by the “pipe (”\|“) character, and the”mime type” and “service name” are chosen from the ESGF controlled vocabulary.

Example of Dataset access URLs:

- THREDDS catalog: <a href="http://esgf-data.llnl.gov/thredds/catalog/esgcet/1/obs4MIPs.NASA-JPL.TES.tro3.mon.v20110608.xml#obs4MIPs.NASA-JPL.TES.tro3.mon" class="reference external">http://esgf-data.llnl.gov/thredds/catalog/esgcet/1/obs4MIPs.NASA-JPL.TES.tro3.mon.v20110608.xml#obs4MIPs.NASA-JPL.TES.tro3.mon</a>.v20110608\|application/xml+thredds\|THREDDS

- LAS server: <a href="http://esgf-node.llnl.gov/las/getUI.do?catid=0C5410C250379F2D139F978F7BF48BB9_ns_obs4MIPs.NASA-JPL.TES.tro3.mon" class="reference external">http://esgf-node.llnl.gov/las/getUI.do?catid=0C5410C250379F2D139F978F7BF48BB9_ns_obs4MIPs.NASA-JPL.TES.tro3.mon</a>.v20110608\|application/las\|LAS

Example of File access URLs:

- HTTP download: <a href="http://esgf-data.llnl.gov/thredds/fileServer/esg_dataroot/obs4MIPs/observations/atmos/tro3Stderr/mon/grid/NASA-JPL/TES/v20110608/tro3Stderr_TES_L3_tbd_200507-200912" class="reference external">http://esgf-data.llnl.gov/thredds/fileServer/esg_dataroot/obs4MIPs/observations/atmos/tro3Stderr/mon/grid/NASA-JPL/TES/v20110608/tro3Stderr_TES_L3_tbd_200507-200912</a>.nc\|application/netcdf\|HTTPServer

- GridFTP download: gsiftp://esgf-data.llnl.gov:2811//esg_dataroot/obs4MIPs/observations/atmos/tro3Stderr/mon/grid/NASA-JPL/TES/v20110608/tro3Stderr_TES_L3_tbd_200507-200912.nc\|application/gridftp\|GridFTP

- OpenDAP download: <a href="http://esgf-data.llnl.gov/thredds/dodsC/esg_dataroot/obs4MIPs/observations/atmos/tro3Stderr/mon/grid/NASA-JPL/TES/v20110608/tro3Stderr_TES_L3_tbd_200507-200912.nc" class="reference external">http://esgf-data.llnl.gov/thredds/dodsC/esg_dataroot/obs4MIPs/observations/atmos/tro3Stderr/mon/grid/NASA-JPL/TES/v20110608/tro3Stderr_TES_L3_tbd_200507-200912.nc</a>.html\|application/opendap-html\|OPENDAP

- Globus As-A-Service download: globus:e3f6216e-063e-11e6-a732-22000bf2d559/esg_dataroot/obs4MIPs/observations/atmos/tro3Stderr/mon/grid/NASA-JPL/TES/v20110608/tro3Stderr_TES_L3_tbd_200507-200912.nc\|Globus\|Globus

</div>

<div id="wget-scripting" class="section">

## Wget scripting<a href="#wget-scripting" class="headerlink" title="Permalink to this headline">¶</a>

The same RESTful API that is used to query the ESGF search services can also be used, with minor modifications, to generate a Wget script to download all files matching the given constraints. Specifically, each ESGF Index Node exposes the following URL for generating Wget scripts:

<div class="highlight-console notranslate">

<div class="highlight">

    http:///wget?[keyword parameters as (name, value) pairs][facet parameters as (name,value) pairs]

</div>

</div>

where again“” is the base URL of the search service at a given Index Node. As for searching, all parameters (keyword and facet) are optional, and the value of all parameters must be URL-encoded, so that the complete search URL is well formed.

The only syntax differences with respect to the search URL are:

- The keyword parameter type= is not allowed, as the wget URL always assumes type=File .

- The keyword parameter format= is not allowed, as the wget URL always returns a shell script as response document.

- The keyword parameter limit= is assigned a default value of limit=1000 (and must still be limit \< 10,000).

- The keyword parameter download_structure= is used for defining a relative directory structure for the download by using the facets value (i.e. of Files and not Datasets).

- The keyword parameter download_emptypath= is used to define what to do when download_structure is set and the facet returned has no value (for example, when mixing files from CMIP5 and obs4MIP and selecting instrument as a facet value will result in all CMIP5 files returning an empty value)

A typical workflow pattern consists in first identifying all datasets or files matching some scientific criteria, then changing the request URL from “/search?” to “/wget?” to generate the corresponding shell scripts for bulk download of files.

Examples:

- Download all obs4MIPs files from the JPL node with variable “hus” : <a href="http://esgf-node.llnl.gov/esg-search/wget?variable=hus&amp;project=obs4MIPs&amp;distrib=false" class="reference external">http://esgf-node.llnl.gov/esg-search/wget?variable=hus&amp;project=obs4MIPs&amp;distrib=false</a>

- Download the files as in the previous examples, and organize them in a directory structure such as project/product/institute/time_frequency : <a href="http://esgf-node.llnl.gov/esg-search/wget?variable=hus&amp;project=obs4MIPs&amp;distrib=false&amp;download_structure=project,product,institute,time_frequency" class="reference external">http://esgf-node.llnl.gov/esg-search/wget?variable=hus&amp;project=obs4MIPs&amp;distrib=false&amp;download_structure=project,product,institute,time_frequency</a>

For more information, see also the Wget FAQ

</div>

</div>

</div>

</div>
