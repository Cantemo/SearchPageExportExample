"""
Implementation of a utility function that is available in core Portal 4.2.0
"""

try:
    # We try to import from Portal core ...
    from portal.utils.general import get_item_ids_from_request
except ImportError:
    # ... if that fails use the function defined here:
    def get_item_ids_from_request(request):
        """
        Get the actually selected item IDs from a request. This can be a generator in case
        of search_id selection, or plain list if user has only selected some items.

        If the caller wants to distinguish between these, they can call len() on the results,
        this will raise with TypeError in case of the generator.

        :param request: A request
        :type request: rest_framework.request.Request  or django.core.handlers.wsgi.WSGIRequest
        :return: item IDs
        :rtype: list(str) or collections.Iterable[str]
        """
        from portal.vidispine.tasks import get_item_ids_from_search_id

        search_id = request.GET.get("search_id")
        ignore_list = request.GET.getlist("ignore_list")
        if search_id:
            # This is a generator
            return get_item_ids_from_search_id(search_id, ignore_list, request.user.username)
        else:
            # A plain list of IDs
            return request.GET.getlist("selected_objects")
