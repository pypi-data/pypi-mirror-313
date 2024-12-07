"""
This module provides the ability to update a saved search.

Functions:
    _update_saved_search: Updates a saved search.
"""

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.portal.saved_search.get_saved_search import _get_saved_search


def _update_saved_search(
    self,
    saved_search_id: str,
    name: str | None,
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
    Updates a saved search.

    Args:
        saved_search_id (str): The ID of the saved search.
        name (str | None): The name of the saved search.
        featured (bool | None): If the saved search is featured.
        bookmarked (bool | None): If the saved search is bookmarked.
        public (bool | None): If the saved search is public.
        sequence (int | None): The sequence of the saved search.
        saved_search_type (int | None): The type of the saved search. 0 = List, 1 = Preview Image, 2 = Header.
        query (str | None): The query of the search.
        offset (int | None): The offset of the search.
        size (int | None): The size of the search.
        filters (list[dict] | None): The filters of the search.
            dict format: {"fieldName": "string", "operator": "string", "values" : "array<string>" | "string"}
        sort_fields (list[dict] | None): The sort fields of the search.
            dict format: {"fieldName": "string", "sortType": ("Ascending" | "Descending")}
        search_result_fields (list[dict] | None): The property fields you want to show in the result.
            dict format: {"name": "string"}
        similar_asset_id (str | None): When SimilarAssetId has a value, then the search results are a special type
            of results and bring back the items that are the most similar to the item represented here.
            This search is only enabled when Vector searching has been enabled.
            When this has a value, the SearchQuery value and PageOffset values are ignored.
        min_score (float | None): Specifies the minimum score to match when returning results.
            If omitted, the system default will be used - which is usually .65
        exclude_total_record_count (bool | None): Normally, the total record count is returned but the query
            can be made faster if this value is excluded.
        filter_binder (str | None): The filter binder of the search. 0 = AND, 1 = OR.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/portal/savedsearch/{saved_search_id}"

    saved_search_info: dict = _get_saved_search(self, saved_search_id)

    body: dict = {
        key: value for key, value in {
            "id": saved_search_id,
            "name": name or saved_search_info.get("name"),
            "featured": featured or saved_search_info.get("featured"),
            "bookmarked": bookmarked or saved_search_info.get("bookmarked"),
            "public": public or saved_search_info.get("public"),
            "pageSize": size or saved_search_info.get("pageSize"),
            "sequence": sequence or saved_search_info.get("sequence"),
            "type": saved_search_type or saved_search_info.get("type"),
            "user": saved_search_info.get("user"),
            "criteria": {
                key: value for key, value in {
                    "query": query or saved_search_info.get("criteria").get("query"),
                    "pageOffset": offset or saved_search_info.get("criteria").get("pageOffset"),
                    "pageSize": size or saved_search_info.get("criteria").get("pageSize"),
                    "filters": filters or saved_search_info.get("criteria").get("filters"),
                    "sortFields": sort_fields or saved_search_info.get("criteria").get("sortFields"),
                    "searchResultFields": search_result_fields or saved_search_info.get("criteria").get("searchResultFields"),
                    "similarAssetId": similar_asset_id or saved_search_info.get("criteria").get("similarAssetId"),
                    "minScore": min_score or saved_search_info.get("criteria").get("minScore"),
                    "excludeTotalRecordCount": exclude_total_record_count or saved_search_info.get("criteria").get("excludeTotalRecordCount"),
                    "filterBinder": filter_binder or saved_search_info.get("criteria").get("filterBinder")
                }.items() if value is not None
            }
        }.items() if value is not None
    }

    return _send_request(self, "Update saved search", api_url, "PUT", None, body)
