#For use with python 3.x.
# Program only checks xml files in directory that contains this python file.
# Delete all csv files before running script. Script appends to csv files of 
# the same name if they already exist.

# Program only scrapes epigraphs, epigraph attribution, and file name. Program also notes number of quote entrieis.
# If you want more metadata collected, use attribute_scraper-full.version.py

# libraries
from bs4 import BeautifulSoup            # select XML tags and parse text
from os import walk, getcwd, listdir     # grab all files in directory of script
import os                                
import csv                               # interact with csv files
import re                                # use regular expressions to standardize authors
#import sys                              # take input from command line

# variables & functions
totalEpigraphCount = 0                   #number of epigraphs in xml files in corpus
epigraphlessFileCount = 0                #number of xml files in corpus that do not have epigraphs

def remove_characters(listofstrings, characters_to_be_removed):
    for string in range(0,len(listofstrings)):
        cleaned_text = ""
        for character in listofstrings[string]:
            if character not in characters_to_be_removed:
                cleaned_text += character 
        listofstrings[string] = cleaned_text 
    return listofstrings 


## COLLECTING INFORMATION FROM CORPUS 
allFilesInDirectory = [ filename for filename in listdir(getcwd()) if filename.endswith('.xml')] #get filenames in current directory ending in ".xml"
for document in range(0, len(allFilesInDirectory)):                   # Loop through all files in directory
    root, ext = os.path.splitext(allFilesInDirectory[document])       # Select file extension for particular file "x" in the list "allFilesInDirectory"
    if (ext == '.xml'):                                               # If file ends in ".xml", read file. Skip file otherwise. 
    # open file to be read
        readfile = open(str(allFilesInDirectory[document]))	          # Specify file to be read & open file
        soup = BeautifulSoup(readfile)                                # Make "soup" object of file to search 
    
    # collect novel author, title of novel, pub date, epigraph, epigraph attrib, pub location, publisher, & encoding company from individual file
        author_list = [author.text for author in soup('author')]   # collect text "author" entries
        
        if len(soup('epigraph')) > 0:                                         #collect entries tagged "epigraph" and place it in the list "epigraphlist'
            epigraph_list = [epigraph.text for epigraph in soup('epigraph')]  
            epigraph_attribution = ["No Attribution" if soup('epigraph')[epigraphs].bibl == None \
                                                 else  soup('epigraph')[epigraphs].bibl.text \
                                                 for epigraphs in range(0,len(soup('epigraph')))]
            #see how many quote tags are nested in epigraph tags (for error checking; see line 59)
            quote_tags_in_epigraph = ["No quote tags" if soup('epigraph')[epigraphs].quote == None \
                                                 else soup('epigraph')[epigraphs].quote.text \
                                                 for epigraphs in range(0,len(soup('epigraph')))]
        else: 
            epigraph_list = ['No Epigraphs']
            epigraph_attribution = ['No Epigraphs']
        
    # Checks to identify epigraphs with 'quote' tag & tracking of who did encoding (see also lines 47-50)
        total_epigraph_tags = str(len(soup('epigraph')))        # number of tagged "epigraph"s in file
        total_quote_tags = str(len(soup('quote')))              # number of tagged "quote"s in file

    ## CLEANING INFORMATION COLLECTED FROM CORPUS
    # remove "/n" characters
        epigraph_attribution = remove_characters(epigraph_attribution, '-\n')
        readfile.close() #close file "x"

# Error Checking Print-To-Terminal: print all information collected
        if (len(soup('epigraph')) == 0):                         #check if file has epigraphs                
                epigraphlessFileCount += 1     
        else:
            for i in range(0, len(soup.findAll('epigraph'))):          
                   totalEpigraphCount += 1

#output to a CSV file -- NOTE: need to wrap strings in a list for csvwriter to output properly
        with open('epigraph_metadata.csv', 'a') as csvfile: #output metadata
            epi_meta = csv.writer(csvfile, dialect='excel')
            if (document == 0):
                epi_meta.writerow(['file name' + '|' + 'file number' + '|' + 'epigraph number' + '|' + 'epigraph attribution' + '|' 'total epigraph tags' + '|' + 'total quote tags'])
            for i in range(0,len(soup('epigraph'))):
                    epi_meta.writerow([allFilesInDirectory[document] + '|'+ str(document) + '|' + str(i) + '|' + str(epigraph_attribution[i]) + total_epigraph_tags + '|' + total_quote_tags])
        

        with open('epigraph_list.csv', 'a') as csvfile: #output metadata
            epi_list = csv.writer(csvfile, dialect='excel')
            for i in range(0,len(soup('epigraph'))):
                epi_list.writerow(['Text ' + str(document+1)+ ', epigraph ' + str(i+1)]) 
                epi_list.writerow([epigraph_list[i]])           

       
#Error Checking Print-To-Terminal: Print total number of epigraphs collected  
print("TOTAl NUMBER OF EPIGRAPHS: " + str(totalEpigraphCount))
print("TOTAL NUMBER OF FILES: " + str(len(allFilesInDirectory)))
print("FILES WITHOUT EPIGRAPHS: " + str(epigraphlessFileCount))
