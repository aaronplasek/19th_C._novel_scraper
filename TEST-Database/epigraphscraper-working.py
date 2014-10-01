#for use with python 3.x; only gets xml files in current directory

# libraries
from bs4 import BeautifulSoup            
from os import walk, getcwd, listdir     #used to grab all files in directory of script
import os                                
import csv                               #used to interact with csv files (not yet working)
import re                                #handle escape characters for MySQL 
import sys                               #take input from command line

# variables
totalEpigraphCount = 0                   #number of epigraphs in all files in directory
epigraphlessFileCount = 0                #number of files in directory that do not have epigraphs


#get list of files in current directory & put it in an array
allFilesInDirectory = [ filename for filename in listdir(getcwd()) if filename.endswith('.xml')] #get filenames in current directory ending in ".xml"

#scrape epigraphs from all XML files
for document in range(0, len(allFilesInDirectory)):                   #for loop through all files in directory
    root, ext = os.path.splitext(allFilesInDirectory[document])        #select file extension for particular file "x" in the list "allFilesInDirectory"
    if (ext == '.xml'):                                         #if file ends in ".xml", read file 
    # open file to be read
        readfile = open(str(allFilesInDirectory[document]))	        #specify file "x" to be read & open file
        soup = BeautifulSoup(readfile)                           #make "soup" object of file to search 
    # strip author & epigraphs from individual file
        author_list = [author.text for author in soup('author')]          #collect entries tagged "author" and place it in the list "authorlist"
        epigraph_list = [epigraph.text for epigraph in soup('epigraph')]  #collect entries tagged "epigraph" and place it in the list "epigraphlist'; note that soup.find_all("tag") == soup("tag")
        epigraph_attribution = []
        for epi in soup('epigraph'):
            if epi.has_key('bibl'): 
                epigraph_attribution[epi].extend(soup.epigraph.bibl.text)
            else:
                epigraph_attribution[epi].extend("No Attribution")


        print("NUM of soup('epigraph'): " + str(len(soup('epigraph'))))
        print("NUM OF soup('bibl')" + str(len(soup('bibl'))))
        #print("soup.epigraph.bibl.string: " + str(soup.epigraph.bibl)
        #epi_attrib = [soup.epigraph.bibl.text for bibl in soup.find('epigraph').find('bibl')]
        #print(epi_attrib)
        #epigraph_attrib = [ ]
        #for epigraph in soup('epigraph'):
        #    epigraph_list.append(epigraph.text)
        #epigraph_attrib.append
        #epi_attrib = [bibl.text for epigraph in soup('epigraph')]
        readfile.close()                                                 #close file "x"
        if (len(soup.findAll('epigraph')) == 0):                         #check if file has epigraphs                
            print(allFilesInDirectory[document] + ": No epigraphs found.")       #Error Test
            epigraphlessFileCount += 1                                    #note file did not have epigraph
        else:
            for i in range(0, len(soup.findAll('epigraph'))):          
                if (len(soup.findAll('author')) == 0):
                    print("Unknown Author" + "\n" + allFilesInDirectory[document] + "\n" + str(i+1) + "\n" + epigraph_list[i] + "\n" + epigraph_attribution[i] + "\n")
                    totalEpigraphCount += 1
                else:    
                    print(author_list[0] + "\n" + allFilesInDirectory[document] + "\n" + str(i+1) + "\n" + str(epigraph_list[i])+"\n" + epigraph_attribution[i] + "\n")
                    totalEpigraphCount += 1
        
#Print total number of epigraphs collected to the terminal -------------------------
print("TOTAl NUMBER OF EPIGRAPHS: " + str(totalEpigraphCount))
print("TOTAL NUMBER OF FILES: " + str(len(allFilesInDirectory)))
print("FILES WITHOUT EPIGRAPHS: " + str(epigraphlessFileCount))

#CODE SNIPPETS THAT MAY BE USEFUL FOR FUTURE CHANGES ------------------------------
#Can directly access individual epigraph as follows:
#soup('author')[0].text
#soup('author')[1].text
#soup('epigraph')[0].text
#soup('epigraph')[1].text
#THIS SHOULD WORK: out.writerow(authorlist[2] + "    " + allFilesInDirectory[x] + "    "
# + str(i) + "   " + epigraph[i])
#out = csv.writer(open("epigraph.csv","wb"), delimiter='\t',quoting=csv.QUOTE_MINIMAL) 

#TOTAl NUMBER OF EPIGRAPHS: 28
#TOTAL NUMBER OF FILES: 13
#FILES WITHOUT EPIGRAPHS: 6
