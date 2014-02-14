*TEI/XML Epigraph Scraper*
================
This script pulls XML-tagged content (including epigraphs specifically) from all the XML files in a directory and outputs this information to both the terminal and to a MySQL database. This script was written and tested on a Macbook Pro (OS 10.9.1) using python 2.7.1. It should also work on Linux/Unix. You will need to install Beautiful Soup.

*Instructions*
=============
(1) Install Beautiful Soup. http://www.crummy.com/software/BeautifulSoup/

(2) The script should be placed in the same directory as all the files to be scraping.

(3) The current "working directory" of your terminal needs to be the same directory in which you are running your script! 

*Future Features*
================
(1) Will add other attribute-grabbing features, including title, publication date, epigraph author, and more.

(2) Will add the ability to include part-of-speech information for epigraphs and titles. 

(3) Will add the ability to output to a csv file.
