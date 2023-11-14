"""
This code registers the plugins requires by this example application.

Another example can be generated on a Portal system by running the command:

    /opt/cantemo/portal/manage.py start_portal_app <name_of_app>
"""
import logging

from portal.generic.plugin_interfaces import IAppRegister
from portal.generic.plugin_interfaces import IPluginBlock
from portal.generic.plugin_interfaces import IPluginURL
from portal.pluginbase.core import Plugin
from portal.pluginbase.core import implements

log = logging.getLogger(__name__)


class SearchPageExportExamplePluginURL(Plugin):
    """
    Adds a plugin which creates url handler for the URLs defined in urls.py
    """

    implements(IPluginURL)

    def __init__(self):
        self.name = "SearchPageExportExample App"
        self.urls = "portal.plugins.search_page_export_example.urls"
        # All the end-points for this plugin are defined under the URL
        # /search_page_export_example/
        self.urlpattern = r"^search_page_export_example/"
        # Name space for the views - when "name" from urls.py is used
        self.namespace = r"search_page_export_example"
        self.plugin_guid = "abd25951-159c-4342-99f1-d8ce88e42aac"
        log.debug("Initiated SearchPageExportExample App")


SearchPageExportExamplePluginURL()


class SearchPageExportExampleRegister(Plugin):
    """
    This plugin adds the app to the list of registered apps.
    """

    implements(IAppRegister)

    def __init__(self):
        self.name = "SearchPageExportExample Registration App"
        self.plugin_guid = "b48c7d2f-3373-48c3-90e9-c3baf3b4bf8f"
        log.debug("Register the App")

    def __call__(self):
        # This has to be imported in the method call to prevent a circular dependency
        from .__init__ import __version__ as versionnumber

        _app_dict = {
            "name": "SearchPageExportExample",
            "version": versionnumber,
            "author": "",
            "author_url": "https://www.cantemo.com/",
            "notes": "Add your Copyright notice here.",
        }
        return _app_dict


SearchPageExportExampleRegister()


class SearchPageExportExampleExportSearchPlugin(Plugin):
    """
    Add an action to the search page gear menu
    """

    implements(IPluginBlock)

    def __init__(self):
        # The name of the plugin defines where the HTML gets rendered. This is in the large gear menu of the
        # search page, intended for actions on selection so disabled when no items are selected.
        # See
        # https://doc.cantemo.com/latest/DevelopmentGuide/modules/search_results.html
        # and https://doc.cantemo.com/latest/DevelopmentGuide/search.html?q=pluginblock
        # for more examples.
        self.name = "vs_collection_view_dropdown"
        self.plugin_guid = "50D46B4F-E993-4795-B1D3-7CCF5C308F02"

    def return_string(self, tagname, *args):
        """
        This function returns
        :param tagname: The plugin name where this is rendered - in this example always "vs_collection_view_dropdown"
        :param args: Arguments from the rendering - not needed in this example
        :return:
        """
        return {"guid": self.plugin_guid, "template": "search_page_export_example/menu_item.html"}


SearchPageExportExampleExportSearchPlugin()


class SearchPageExportExampleSearchPageJavascriptPlugin(Plugin):
    """
    Add javascript code to the search page
    """

    implements(IPluginBlock)

    def __init__(self):
        # This plugin block is meant for custom scripting on the search page. It is defined in the HTML template
        # /opt/cantemo/portal/portal_themes/core/templates/search/new-search-page.html
        # See
        #    grep -r pluginblock /opt/cantemo/portal/portal_themes/core/templates/
        # for more examples.
        self.name = "new_search_view_script"
        self.plugin_guid = "7D48595A-1E11-42D0-9ACB-A2B7288D348B"

    def return_string(self, tagname, *args):
        return {"guid": self.plugin_guid, "template": "search_page_export_example/search_page_javascript.html"}


SearchPageExportExampleSearchPageJavascriptPlugin()
