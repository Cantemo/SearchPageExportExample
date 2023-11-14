Portal plugin that implements an action based on user selection on the search page.

## Prerequisites

This plugin requires Cantemo 6.0.0 or later.

For Cantemo 5.x or 4.x, please see [this version](https://github.com/Cantemo/SearchPageExportExample/tree/cantemo5)


## Installation

To install this plugin, copy the contents of this directory to `/opt/cantemo/portal/portal/plugins/`,
make sure the directory is readable by the Portal web-workers (default `www-data`).

For example - on a Portal system:

```
curl -L https://github.com/Cantemo/SearchPageExportExample/archive/master.zip > SearchPageExportExample-master.zip 
unzip SearchPageExportExample-master.zip 
mv SearchPageExportExample-master/search_page_export_example /opt/cantemo/portal/portal/plugins/
chown -R www-data:www-data /opt/cantemo/portal/portal/plugins/search_page_export_example
sudo service portal-web restart
```

## Usage

The plugins adds an "Export CSV" action to the search page gear box, it is active when some items are selected:

![Plugin in search page menu](menu.png?raw=true)

Selecting the action shows a popup where user can select the data to export. Export produces a
CSV file that the browser downloads:

![Export popup](export_popup.png?raw=true)

Example CSV output:

    Item ID,Title,Creation date
    VX-2,test2,2019-09-12T10:49:43.183Z
    VX-1,test1,2019-09-12T10:49:34.498Z
