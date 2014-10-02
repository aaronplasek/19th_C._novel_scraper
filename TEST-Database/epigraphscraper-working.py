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
        print("Begin LOOP: " + allFilesInDirectory[document])
        readfile = open(str(allFilesInDirectory[document]))	        #specify file "x" to be read & open file
        soup = BeautifulSoup(readfile)                           #make "soup" object of file to search 
    # strip author & epigraphs from individual file
        author_list = [author.text for author in soup('author')]          #collect entries tagged "author" and place it in the list "authorlist"
        epigraph_list = [epigraph.text for epigraph in soup('epigraph')]  #collect entries tagged "epigraph" and place it in the list "epigraphlist'; note that soup.find_all("tag") == soup("tag")
        #epigraph_attribution = [epigraph.bibl.text for epigraph in soup.find_all]
        

        #bibls_in_epigraphs = [epigraph.bibl.text for bibl in soup.find_all('bibl')]
        #print(bibls_in_epigraphs)
        #epigraph_attribution = [epigraph.bibl.text if epigraph.has_attr('bibl') else "No Attribution" for epigraph in soup('epigraph') if len(soup('epigraph')) > 0]
        epigraph_attribution = [soup.findAll('epigraph', {'default' : 'false'}) for epigraph in soup('epigraph')] 
        print(epigraph_attribution)
      #  for link in soup.find_all('a'):
    #print(link.get('href'))


        #if len(soup('epigraph')) > 0:
            #token = 'bibl'
            #for epigraph in range(0, len(epigraph_list)):
                #print("HELLO:" + str(epi.contents))
                #if 'bibl' in soup('epigraph)
                    #print("yes: " + epigraph)
                #if epi.has_attr('bibl'): 
                    #epigraph_attribution.extend(str(soup.epigraph.bibl.text))
                    #print("Attribution: " + str(soup.epigraph.bibl.text))            
                #else:
                    #epigraph_attribution.append("No Attribution")
                    #print("No Attribution")

        #print("soup.epigraph.bibl.string: " + str(soup.epigraph.bibl)
        #epi_attrib = [soup.epigraph.bibl.text for bibl in soup.find('epigraph').find('bibl')]
        #print(epi_attrib)
        #epigraph_attrib = [ ]
        #for epigraph in soup('epigraph'):
        #    epigraph_list.append(epigraph.text)
        #epigraph_attrib.append
        #epi_attrib = [bibl.text for epigraph in soup('epigraph')]
        
# Error Checking Print-To-Terminal: print all information collected
        readfile.close()                                                 #close file "x"
        if (len(soup('epigraph')) == 0):                         #check if file has epigraphs                
            print(allFilesInDirectory[document] + ": No epigraphs found.")       #Error Test
            epigraphlessFileCount += 1                                    #note file did not have epigraph
        else:
            for i in range(0, len(soup.findAll('epigraph'))):          
                if (len(soup.findAll('author')) == 0):
                    print("Unknown Author" + "\n" + allFilesInDirectory[document] + "\n" + str(i+1) + "\n") #+ str(epigraph_attribution[i]) + "\n")# + str(epigraph_list[i]) + "\n") + str(epigraph_attribution[i]) + "\n")
                    totalEpigraphCount += 1
                else:    
                    print(author_list[0] + "\n" + allFilesInDirectory[document] + "\n" + str(i+1) + "\n")# + str(epigraph_attribution[i]) + "\n")#  + str(epigraph_list[i])+"\n")# 
                    totalEpigraphCount += 1
        
#Error Checking Print-To-Terminal: Print total number of epigraphs collected  
print("TOTAl NUMBER OF EPIGRAPHS: " + str(totalEpigraphCount))
print("TOTAL NUMBER OF FILES: " + str(len(allFilesInDirectory)))
print("FILES WITHOUT EPIGRAPHS: " + str(epigraphlessFileCount))
#print("ATTRIBUTIONS: " + epigraph_attribution)

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
