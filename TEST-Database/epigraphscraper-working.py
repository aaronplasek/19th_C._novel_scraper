#for use with python 3.x; only gets xml files in current directory

# libraries
from bs4 import BeautifulSoup            #used to select XML tags and parse document
from os import walk, getcwd, listdir     #used to grab all files in directory of script
import os                                
import csv                               #to interact with csv files (not yet working)
import re                                # use regular expressions to standardize authors
#import sys                              #take input from command line

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
        print("TEXT " + str(document+1) + ': ' + allFilesInDirectory[document])  #error check line; uncomment to see progress in terminal
        readfile = open(str(allFilesInDirectory[document]))	        #specify file "x" to be read & open file
        soup = BeautifulSoup(readfile)                           #make "soup" object of file to search 
    # collect author & epigraphs from individual file
        author_list = [author.text for author in soup('author')]          #collect entries tagged "author" and place it in the list "authorlist"
        title_list = [title.text for title in soup('title')]              #collect "title" tag entries
        publication_date = [date.text for date in soup('date')]
        publication_place = [pubplace.text for pubplace in soup('pubplace')]

        if len(soup('publisher')) > 0:         
            publishers = [publisher.text for publisher in soup('publisher')]
        else: 
            publishers = ['Unknown Publisher', 'Unknown Publisher','Unknown Publisher']

        if len(soup('epigraph')) > 0:
            epigraph_list = [epigraph.text for epigraph in soup('epigraph')]  #collect entries tagged "epigraph" and place it in the list "epigraphlist'; note that soup.find_all("tag") == soup("tag")
            epigraph_attribution = ["No Attribution" if soup('epigraph')[epigraphs].bibl == None \
                                                 else soup('epigraph')[epigraphs].bibl.text \
                                                 for epigraphs in range(0,len(soup('epigraph')))]
        else: 
            epigraph_list = ['No Epigraphs']
            epigraph_attribution = ['No Epigraphs']
<<<<<<< HEAD
    # clean out "/n" characters in epigraph attributions
=======
    
    # clean out "/n" characters in attribution
>>>>>>> 47ed28052f2dd71f4e99fb6b65a053be16b366e2
        for attribution in range(0,len(epigraph_attribution)):
            cleaned_text = ""
            for character in epigraph_attribution[attribution]:
                if character not in characters_to_be_removed_from_attribution:
                    cleaned_text += character 
            epigraph_attribution[attribution] = cleaned_text   
    # clean out "\n" characters in author name
        for authorname in range(0, len(author_list)):
            cleaned_text = ""
            for character in author_list[authorname]:
                if character not in characters_to_be_removed_from_attribution:
                    cleaned_text += character
            author_list[authorname] = cleaned_text
     # clean out "\n" characters in titles
        for title in range(0, len(title_list)):
            cleaned_text = ""
            for character in title_list[title]:
                if character not in characters_to_be_removed_from_attribution:
                    cleaned_text += character
            title_list[title] = cleaned_text
        for place in range(0, len(publication_place)):
            cleaned_text = ""
            for character in publication_place[place]:
                if character not in characters_to_be_removed_from_attribution:
                    cleaned_text += character
            publication_place[place] = cleaned_text
    # clean publisher names
        for pubs in range(0, len(publishers)):
            cleaned_text = ""
            for character in publishers[pubs]:
                if character not in characters_to_be_removed_from_attribution:
                    cleaned_text += character
            publishers[pubs] = cleaned_text
    # clean publication years        
        for year in range(0, len(publication_date)):
            cleaned_text = ""
            for character in publication_date[year]:
                if character not in characters_to_be_removed_from_attribution:
                    cleaned_text += character
            publication_date[year] = cleaned_text                                       

<<<<<<< HEAD
    # standardize names in author list
    # generate a dict for first and last names based on corpus entries for XML texts

    reg_ex_for_year = re.compile(r'^(10|11|12|13|14|15|16|17|18|19|20)\d{2}$') #find 4-digit year b/w 1000 & 2999


=======
        readfile.close() #close file "x"
>>>>>>> 47ed28052f2dd71f4e99fb6b65a053be16b366e2
# Error Checking Print-To-Terminal: print all information collected
        if (len(soup('epigraph')) == 0):                         #check if file has epigraphs                
<<<<<<< HEAD
            print('Author: ' + author_list[0] + '\n' + "No epigraphs found." + '\n')       #Error Test
=======
#            print(allFilesInDirectory[document] + ": No epigraphs found." + '\n')       #Error Test
>>>>>>> 47ed28052f2dd71f4e99fb6b65a053be16b366e2
            epigraphlessFileCount += 1                                    #note file did not have epigraph
        else:
            for i in range(0, len(soup.findAll('epigraph'))):          
                if (len(soup.findAll('author')) == 0):
#                    print("Unknown Author" + "\n" +title_list[i]+ "\n" +allFilesInDirectory[document] + "\n" + "Text " + str(document+1) \
#                         + ", epigraph " + str(i+1) + "\n" + str(epigraph_attribution[i]) + "\n" + str(epigraph_list[i]) + "\n") 
                    totalEpigraphCount += 1
                else:    
#                    print(author_list[0] + "\n" + title_list[i]+ "\n" +allFilesInDirectory[document] + "\n" + "Text " + str(document+1) \
#                         + ", epigraph " + str(i+1) + "\n" + str(epigraph_attribution[i]) + "\n" + str(epigraph_list[i]) + "\n") 
                    totalEpigraphCount += 1

#output to a CSV file -- NOTE: need to wrap strings in a list for csvwriter to output properly
       
        with open('epigraph_metadata.csv', 'a') as csvfile: #output metadata
            epi_meta = csv.writer(csvfile, dialect='excel')
            #epi_meta.writerow('epigraph ID' + '  |  ' + 'File Name' + '  |  ' +'File ID' + '  |  ' +'Hypotext Author' + '  |  ' + '  |  '+ 'Title'+ 'Epigraph Attribution') 
            for i in range(0,len(soup('epigraph'))):
                if (len(soup('author')) ==0):
                    epi_meta.writerow([str(i) + '|' + allFilesInDirectory[document] + '|'+ str(document) + '|' +  'Unknown Author' + '|' + str(title_list[0])+ '|' + str(epigraph_attribution[i]) + '|' + str(publishers[1])+ '|' + str(publication_place[1]) + '|' + str(publication_date[1])])           
                else:
                    epi_meta.writerow([str(i) + '|' + allFilesInDirectory[document] + '|'+ str(document) + '|' +  author_list[0] + '|' + str(title_list[0])+ '|' + str(epigraph_attribution[i])+ '|' +  str(publishers[1])+ '|' + str(publication_place[1]) + '|' + str(publication_date[1])])

        with open('epigraph_list.csv', 'a') as csvfile: #output metadata
            epi_list = csv.writer(csvfile, dialect='excel')
            for i in range(0,len(soup('epigraph'))):
                epi_list.writerow(['Text ' + str(document+1)+ ', epigraph ' + str(i+1)]) 
                epi_list.writerow([epigraph_list[i]])           


        
#Error Checking Print-To-Terminal: Print total number of epigraphs collected  
print("TOTAl NUMBER OF EPIGRAPHS: " + str(totalEpigraphCount))
print("TOTAL NUMBER OF FILES: " + str(len(allFilesInDirectory)))
print("FILES WITHOUT EPIGRAPHS: " + str(epigraphlessFileCount))

#CODE SNIPPETS & USEFUL NOTES ----
#Can directly access individual epigraph as follows:
#soup('author')[0].text
#soup('author')[1].text
#etc. 

#NOTE FOR BEAUTIFUL SOUP: soup('epigraph') == soup.find_all('epigraph')
