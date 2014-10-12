*TEI/XML Epigraph Scraper*
================
This script pulls XML-tagged content from all the XML files in a directory and outputs this information into a csv file (that can be viewed in Excel or OpenOffice). Presently the script collects author name, novel title, publication date, publication location, epigraph text, and epigraph attribution from XML files in Early American Fiction and Wright American Fiction collections. 

This script was tested on a Macbook Pro and an iMac (both using OS 10.9) using python 3.4. (Please note that this script will not work with python 2.x.) You will need to install Beautiful Soup 4. 

*Usage*
=============
Just place the script in the directory with your XML texts to be scraped, and then run script in the terminal by typing
`python3 epigraphscraper.py`.

