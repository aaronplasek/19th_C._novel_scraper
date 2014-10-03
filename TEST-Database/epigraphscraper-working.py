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
characters_to_be_removed_from_attribution = '\n'          #characters to be removed from epigraph attributions

#get list of files in current directory & put it in an array
allFilesInDirectory = [ filename for filename in listdir(getcwd()) if filename.endswith('.xml')] #get filenames in current directory ending in ".xml"

#scrape epigraphs from all XML files
for document in range(0, len(allFilesInDirectory)):                   #for loop through all files in directory
    root, ext = os.path.splitext(allFilesInDirectory[document])        #select file extension for particular file "x" in the list "allFilesInDirectory"
    if (ext == '.xml'):                                         #if file ends in ".xml", read file 
    # open file to be read
        print("TEXT " + str(document+1) + ': ' + allFilesInDirectory[document])
        readfile = open(str(allFilesInDirectory[document]))	        #specify file "x" to be read & open file
        soup = BeautifulSoup(readfile)                           #make "soup" object of file to search 
    # collect author & epigraphs from individual file
        author_list = [author.text for author in soup('author')]          #collect entries tagged "author" and place it in the list "authorlist"
        print(author_list)

        if len(soup('epigraph')) > 0:
            epigraph_list = [epigraph.text for epigraph in soup('epigraph')]  #collect entries tagged "epigraph" and place it in the list "epigraphlist'; note that soup.find_all("tag") == soup("tag")
            epigraph_attribution = ["No Attribution" if soup('epigraph')[epigraphs].bibl == None \
                                                 else soup('epigraph')[epigraphs].bibl.text \
                                                 for epigraphs in range(0,len(soup('epigraph')))]
        else: 
            epigraph_list = ['No Epigraphs']
            epigraph_attribution = ['No Epigraphs']
    # clean out "/n" characters in attribution
        for attribution in range(0,len(epigraph_attribution)):
            cleaned_text = ""
            for character in epigraph_attribution[attribution]:
                if character not in characters_to_be_removed_from_attribution:
                    cleaned_text += character 
            epigraph_attribution[attribution] = cleaned_text   

# Error Checking Print-To-Terminal: print all information collected
        readfile.close()                                                 #close file "x"
        if (len(soup('epigraph')) == 0):                         #check if file has epigraphs                
            print(allFilesInDirectory[document] + ": No epigraphs found." + '\n')       #Error Test
            epigraphlessFileCount += 1                                    #note file did not have epigraph
        else:
            for i in range(0, len(soup.findAll('epigraph'))):          
                if (len(soup.findAll('author')) == 0):
                    print("Unknown Author" + "\n" + allFilesInDirectory[document] + "\n" + "Text " + str(document+1) \
                         + ", epigraph " + str(i+1) + "\n" + str(epigraph_attribution[i]) + "\n" + str(epigraph_list[i]) + "\n") 
                    totalEpigraphCount += 1
                else:    
                    print(author_list[0] + "\n" + allFilesInDirectory[document] + "\n" + "Text " + str(document+1) \
                         + ", epigraph " + str(i+1) + "\n" + str(epigraph_attribution[i]) + "\n" + str(epigraph_list[i]) + "\n") 
                    totalEpigraphCount += 1
        
#Error Checking Print-To-Terminal: Print total number of epigraphs collected  
print("TOTAl NUMBER OF EPIGRAPHS: " + str(totalEpigraphCount))
print("TOTAL NUMBER OF FILES: " + str(len(allFilesInDirectory)))
print("FILES WITHOUT EPIGRAPHS: " + str(epigraphlessFileCount))


#brown.xml has 15 bibl entries and 25 epigraphs total


#CODE SNIPPETS & USEFUL NOTES ----
#Can directly access individual epigraph as follows:
#soup('author')[0].text
#soup('author')[1].text
#soup('epigraph')[0].text
#soup('epigraph')[1].text
#etc.

#THIS SHOULD WORK FOR OUTPUT TO CSV ----
#out.writerow(authorlist[2] + "    " + allFilesInDirectory[x] + "    " + str(i) + "   " + epigraph[i])
#out = csv.writer(open("epigraph.csv","wb"), delimiter='\t',quoting=csv.QUOTE_MINIMAL) 

#NOTE FOR BEAUTIFUL SOUP: soup('epigraph') == soup.find_all('epigraph')

#CORRECT VALUES FOR TEST DATABASE ----
#TOTAl NUMBER OF EPIGRAPHS: 28
#TOTAL NUMBER OF FILES: 13
#FILES WITHOUT EPIGRAPHS: 6
