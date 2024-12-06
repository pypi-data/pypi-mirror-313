"""
This module contains the search function that is used to search for assets in the Nomad Media Platform.

Functions:
    _search: Searches for assets in the Nomad Media Platform.
"""
from nomad_media_pip.src.helpers.send_request import _send_request


def _search(
    self,
    query: str | None,
    offset: int | None,
    size: int | None,
    filters: list[dict] | None,
    sort_fields: list[dict] | None,
    search_result_fields: list[str] | None,
    similar_asset_id: str | None,
    min_score: int | None,
    exclude_total_record_count: bool | None,
    filter_binder: int | None,
    full_url_field_names: list[str] | None,
    distinct_on_field_name: str | None,
    include_video_clips: bool | None,
    use_llm_search: bool | None,
    include_internal_fields_in_results: bool
) -> dict | None:
    """
    Searches for assets in the Nomad Media Platform.

    Args:
        query (str | None): The query is used for free text searching within all of the text of the records.
        This is typically associated to the values entered into a search bar on a website.
        offset (int | None): The pageOffset is a zero based number offset used for paging purposes.
        If this value is omitted then the marker based paging is used and the return nextPageOffset
        value will specify a string - rather than a number. You can only use either the zero based page
        numbers OR the string based page markers, but not both in a single search query and paging.
        size (int | None): The size is a zero based number that represents how many items
        in the selected page to return
        filters (list[dict] | None): Filters are the primary mechanism for filtering the returned
        records. There is often more than 1 filter. When 2 or more filters are supplied then there is an
        implied "**AND**" between each filter.  The name of each filter must match exactly to the name in
        the output including the appropriate camel-casing.  The operator choices are: (Equals, NotEqual,
        Contains, NotContains, LessThan, GreaterThan, LessThanEquals, snf GreaterThanEquals).
        The value can be either a single value or an array of values. If an array of values is supplied
        then there is an implied "**OR**" between each value in the array. NOTE: When filtering by dates,
        format matters. The appropriate format to use is UTC format such as YYYY-MM-DDTHH:MM:SS.SSSZ.
        List format: [{"fieldName": "string", "operator": "string", "values" : "list | string"} ...]
        sort_fields (list[dict] | None): The sortFields allows the top level results to be sorted
        by one or more of the output result fields. The name represents one of the fields in the output
        and must match exactly including the camel-casing.
        List format: [{"fieldName": "string", "sortType": ("Ascending" | "Descending")} ...]
        search_result_fields (list[dict] | None): The searchResultFields allows you to specify specific
        fields that should be returned in the output as well as any children (or related) records that should
        be also returned. Note that any given searchResultField can contain children also and those fields can
        contain children. There is no limit to the level of related children to return
        List format: [{"name": "string"} ...]
        similar_asset_id (str | None): When SimilarAssetId has a value, then the search
        results are a special type of results and bring back the items that are the most similar to
        the item represented here. This search is only enabled when Vector searching has been enabled.
        When this has a value, the SearchQuery value and PageOffset values are ignored.
        min_score (int | None): Specifies the minimum score to match when returning results.
        If omitted, the system default will be used - which is usually .65
        exclude_total_record_count (bool | None): Normally, the total record count is
        returned but the query can be made faster if this value is excluded.
        filter_binder (int | None): The filter binder of the search. 0 = AND, 1 = OR.
        full_url_field_names (list[str] | None): Gets or sets the list of fields that should have the FullURL
        calculated. The calculations are expensive and greatly slow down the query.
        Use this field to only return the ones that are actually needed.
        distinct_on_field_name (str | None): Gets or sets optional property that will be used to aggregate
        results records to distinct occurances of this field's values.
        include_video_clips (bool | None): Gets or sets a value indicating whether specify if the video
        search results are grouped by include clips of the videos also.
        use_llm_search (bool | None): Gets or sets a value indicating whether gets or Sets a value representing
        if the search engine should try and use the LLM search instead of the standard search.
        include_internal_fields_in_results (bool | None): Gets or sets a value indicating whether
        specify if the internal fields are included in the results.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = (
        f"{self.config["serviceApiUrl"]}/api/admin/search"
        if self.config["apiType"] == "admin"
        else f"{self.config["serviceApiUrl"]}/api/portal/search"
    )

    params: dict = {
        "includeInternalFieldsInResults": include_internal_fields_in_results
    }

    body: dict = {
        "searchQuery": query if query else None,
        "pageOffset": offset if offset else 0,
        "pageSize": size if size else 100,
        "filters": filters if filters else None,
        "sortFields": sort_fields if sort_fields else None,
        "searchResultFields": search_result_fields if search_result_fields else None,
        "fullUrlFieldNames": full_url_field_names if full_url_field_names else None,
        "distinctOnFieldName": distinct_on_field_name if distinct_on_field_name else None,
        "includeVideoClips": include_video_clips if include_video_clips is not None else None,
        "similarAssetId": similar_asset_id if similar_asset_id else None,
        "minScore": min_score if min_score else None,
        "excludeTotalRecordCount": exclude_total_record_count if exclude_total_record_count else None,
        "filterBinder": filter_binder if filter_binder else None,
        "useLLMSearch": use_llm_search if use_llm_search is not None else None
    }

    body: dict = {k: v for k, v in body.items() if v is not None}

    return _send_request(self, "Search", api_url, "POST", params, body)
