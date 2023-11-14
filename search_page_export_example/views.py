"""
This file implements the views (end-points) for the application.
"""
import csv
import logging

from django.http import HttpResponse
from rest_framework.response import Response

from portal.generic.baseviews import CView
from portal.generic.decorators import HasAnyRole
from portal.utils.general import get_item_ids_from_request
from portal.vidispine.iitem import ItemHelper

log = logging.getLogger(__name__)


class ExportFormView(CView):
    """
    This view returns a HTML form that is rendered in a popup, called from
    templates/search_page_export_example/search_page_javascript.html
    """

    template_name = "search_page_export_example/form.html"

    # User accessing this view must have the "portal_items_read" role.
    #
    # A custom role for our plugin could also be used - see
    #    Help > System API Reference > groups > API for creating custom portal roles
    # ... on your Cantemo system on how those can be created.
    permission_classes = [HasAnyRole]
    roles = ["portal_items_read"]

    def get(self, request):
        log.info(f"{request.user} viewing ExportFormView")
        # The form is loaded with user item selection as query parameters, for example:
        #
        #   /search_page_export_example/?selected_objects=VX-2&selected_objects=VX-1
        #
        # or
        #
        #   /search_page_export_example/?search_id=1
        #
        # We want to pass that on into the form as a variable (see form.html),
        # but replace the URL to point to CsvExportView
        ctx = {
            "csv_export_link": request.get_full_path().replace(
                "/search_page_export_example/", "/search_page_export_example/csv/"
            )
        }
        return Response(ctx)


class CsvExportView(CView):
    """
    This view handles the request to get the CSV data based on user selection in the UI.
    """

    # Use the same role requirement as in ExportFormView
    permission_classes = [HasAnyRole]
    roles = ["portal_items_read"]

    def post(self, request):
        log.info(f"{request.user} posting to CsvExportView")

        # We want to respond with a file of type CSV - see
        # https://docs.djangoproject.com/en/1.11/howto/outputting-csv/

        # HttpResponse instead of the Django Rest Framework Response as this makes
        # it easier to return the raw CSV data.
        response = HttpResponse(content_type="text/csv")
        # This defines the filename the user gets
        response["Content-Disposition"] = 'attachment; filename="search_page_export_example.csv.txt"'

        # request.data gives access to the data user selected from the form -
        # any non-empty value in export_item_id means we include that data
        export_item_id = request.data.get("export_item_id")
        export_item_title = request.data.get("export_item_title")
        export_item_created = request.data.get("export_item_created")

        # This writer allows us to write values as CSV
        writer = csv.writer(response)

        # We add a header row to the CSV
        header_row = []
        if export_item_id:
            header_row.append("Item ID")
        if export_item_title:
            header_row.append("Title")
        if export_item_created:
            header_row.append("Creation date")
        writer.writerow(header_row)

        # We get the list of item IDs the user has selected - based on the query parameters in the URL.
        # This can be a long one in case a search_id is selected
        item_ids = get_item_ids_from_request(request)

        # ItemHelper is used to access item data from Vidispine
        item_helper = ItemHelper(runas=request.user)
        items = item_helper.getItems(item_ids)

        # Export the data of each item
        for item in items:
            item_row = []
            if export_item_id:
                item_row.append(item.getId())
            if export_item_title:
                item_row.append(item.getTitle())
            if export_item_created:
                item_row.append(item.getMetadataFieldValueByName("created"))
            writer.writerow(item_row)

        # Note: Above loop writes the CSV data in memory for simplicity - for large datasets
        # streaming output would be more effcient:
        # https://docs.djangoproject.com/en/1.11/howto/outputting-csv/#streaming-large-csv-files

        return response
