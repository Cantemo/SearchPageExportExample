"""
This file defined the URLs (end-points) for the plugin.
"""
from django.conf.urls import url

from . import views

# The plugin handles the request to the URL by responding with the view which is loaded
# from views.py. Inside "views" is a class which responses to the
# request. "name" is a shortcut name for the urls.
urlpatterns = [
    # This is http://<portal_server_url>/search_page_export_example/
    url(r"^$", views.ExportFormView.as_view(), name="form"),
    # This is http://<portal_server_url>/search_page_export_example/csv/
    url(r"^csv/$", views.CsvExportView.as_view(), name="csv"),
]
