"""
This module adds a saved search.

Functions:
    _add_saved_search: Adds a saved search.
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _add_saved_search(
    self,
    name: str,
    featured: bool | None,
    bookmarked: bool | None,
    public: bool | None,
    sequence: int | None,
    saved_search_type: int | None,
    query: str | None,
    offset: int | None,
    size: int | None,
    filters: list[dict] | None,
    sort_fields: list[dict] | None,
    search_result_fields: list[dict] | None,
    similar_asset_id: str | None,
    min_score: float | None,
    exclude_total_record_count: bool | None,
    filter_binder: str | None
) -> dict | None:
    """
    Adds a saved search.

    Args:
        name (str): The name of the saved search.
        featured (bool | None): If the saved search is featured.
        bookmarked (bool | None): If the saved search is bookmarked.
        public (bool | None): If the saved search is public.
        sequence (int | None): The sequence of the saved search.
        saved_search_type (int | None): The type of the saved search. 0 = List, 1 = Preview Image, 2 = Header.
        query (str | None): The query of the search.
        offset (int | None): The offset of the search.
        size (int | None): The size of the search.
        filters (list[dict] | None): The filters of the search. [{"fieldName": "string", "operator": "string", "values" : "list of string"} ...]
        sort_fields (list[dict] | None): The sort fields of the search. [{"fieldName": "string", "sortType": ("Ascending" | "Descending")} ...]
        search_result_fields (list[dict] | None): The property fields you want to show in the result. [{"name": "string"} ...]
        similar_asset_id (str | None): When SimilarAssetId has a value, then the search results are a special type of results and bring back the
        items that are the most similar to the item represented here. This search is only enabled when Vector searching has been enabled. When this
        has a value, the SearchQuery value and PageOffset values are ignored.
        min_score (float | None): Specifies the minimum score to match when returning results.
            If omitted, the system default will be used - which is usually .65
        exclude_total_record_count (bool | None): Normally, the total record count is returned but the query can be made faster if this value
            is excluded.
        filter_binder (str | None): The filter binder of the search. 0 = AND, 1 = OR.

    Returns:
        dict: The JSON response from the server if the request is successful.
    None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/portal/savedsearch"

    body: dict = {
        "name": name,
        "featured": featured,
        "bookmarked": bookmarked,
        "public": public,
        "pageSize": size,
        "sequence": sequence,
        "type": saved_search_type,
        "criteria": {}
    }

    if query:
        body["criteria"]["query"] = query
    body["criteria"]["pageOffset"] = offset if offset else 0
    body["criteria"]["pageSize"] = size if size else 10
    if filters:
        body["criteria"]["filters"] = filters
    if sort_fields:
        body["criteria"]["sortFields"] = sort_fields
    if search_result_fields:
        body["criteria"]["searchResultFields"] = search_result_fields
    if similar_asset_id:
        body["criteria"]["similarAssetId"] = similar_asset_id
    if min_score:
        body["criteria"]["minScore"] = min_score
    if exclude_total_record_count:
        body["criteria"]["excludeTotalRecordCount"] = exclude_total_record_count
    if filter_binder:
        body["criteria"]["filterBinder"] = filter_binder

    return _send_request(self, "Add saved search", api_url, "POST", None, body)
