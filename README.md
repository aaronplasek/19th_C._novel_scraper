*TEI/XML Epigraph Scraper*
================
This script pulls XML-tagged text and metadata from all the XML files in a directory and outputs this information into a csv file (to be viewed in Excel, OpenOffice, or your preferred spreedsheet of choice). Presently the script grabs (1) author name, (2) novel title, (3) publication date, (4) publication location, (5) epigraph text, (6) epigraph attribution, (7) author birth and death years, and (8) file creation attribution from XML files in Early American Fiction and [Wright American Fiction](https://github.com/iulibdcs/tei_text) collections. 

The script also scrapes the *number* of "quote" and "epigraph" tags in each XML file. This is done because it has been discovered that some files have epigraphs that have not been correctly tagged as such. Examining the number and placement of "quote" and "epigraph" tags, in combination with other methods, can be used to guide systematic checking of novels for epigraphs in cases where they have not been properly labeled.

If you want to use this scraper to examine different XML-encoded corpora, it will be necessary to make minor changes to the code. Please feel free to fork to your heart's satisfaction. 

*Usage*
=============
Just place the script in the directory with your XML texts to be scraped, and then run script in the terminal by typing
`python3 xml_scraper.py`.

The csv files generated will be placed in the same directory containing xml_scraper.py. 

*Testing*
==========
This script was tested on a 2012 Macbook Pro and a 2013 iMac (both using OS 10.9.x) using python 3.4. (Please note that this script will not work with python 2.x.) You will need Beautiful Soup 4. 

*Code Provenance*
=============
The first version of this code was written in a weekend in November 2013 by Aaron Plasek in collaboration with the [NYU Digital Experiments Working Group](http://nyudigitalexperiments.com/) for the (now defunct) Epigraph Project. (This initial version was also the first program Aaron wrote in python, and the present version of the code bears many of the scars from that initial effort.) This initial version only collected novel author names and novel epigraphs. During this time Jonathan Reeve also wrote an [epigraph scraper](https://github.com/DigitalExperiments/epi-project) for the Epigraph Project that uses XPath exclusively.  

Working in conversation with Collin Jennings and Robby Koehler from 2013-2015, Aaron added functionality to collect more information about novels being examined. During the NYU Spring 2015 semester Chancy Zhang, in collaboration with Colling Jennings and Aaron Plasek, also forked a [version of this scraper](https://github.com/yangchen506) that uses SQLite instead of python lists. 

During the 2015 European Summer School in the Digital Humanities at Leipzig, the two functions "count tags" and "count nested tags" (used to facilitate checking of novels for epigraphs in cases where the epigraphs have been mislabeled or unlabeled) were collaboratively written by Ariane Pinche, Ana Migowski, Mark Moll, and Aaron Plasek.
