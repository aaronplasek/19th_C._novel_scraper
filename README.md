*TEI/XML Scraper*
================
This script pulls XML-tagged text and metadata from all the XML files in a directory and outputs this information into a csv file (to be viewed in Excel, OpenOffice, or your preferred spreedsheet of choice). Presently the script scrapes (1) author name, (2) novel title, (3) publication date, (4) publication location, (5) epigraph text, (6) epigraph attribution, (7) author birth and death years, and (8) file creation attribution from XML files in Early American Fiction and [Wright American Fiction](https://github.com/iulibdcs/tei_text) collections. 

The script also scrapes the *number* of "quote" and "epigraph" tags in each XML file. This is done because it has been discovered that some files have epigraphs that have not been correctly tagged as such. (See [this video](http://videostreaming.gc.cuny.edu/videos/video/3502/?live=true) at time 51:07 for a quick 5-minute talk about the problem.) Examining the number and placement of "quote" and "epigraph" tags, in combination with other methods, can be used to guide systematic checking of novels for epigraphs in cases where they have not been properly labeled.


If you want to use this scraper to examine different XML-encoded corpora, it will be necessary to make minor changes to the code. (Please feel free to fork to your heart's satisfaction.) 

This script was tested on a Macbook Pro and an iMac (both using OS 10.9.x) using python 3.4. (Please note that this script will not work with python 2.x.) You will need to install Beautiful Soup 4. 

*Usage*
=============
Just place the script in the directory with your XML texts to be scraped, and then run script in the terminal by typing
`python3 xml_scraper.py`.

The csv files generated will be placed in the same directory as xml_scraper.py. 
