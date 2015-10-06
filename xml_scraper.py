#For use with python 3.x.
# Program only checks xml files in the directory that contains this python file.
# Delete all csv files before running script. Script appends to csv files of 
# the same name if they already exist.

# libraries
from bs4 import BeautifulSoup            # select XML tags and parse text
from os import walk, getcwd, listdir     # used to grab all files in directory of script (c.f. line 29)
from lxml import etree                   # using xpath to compare <quote> and <epigraph> tags in order to identify files that may have epigraphs but have not been properly tagged to indicate this
import os                                # used to split off filename root from filename extension (c.f. line 31)
import csv                               # interact with csv files
import re                                # use regular expressions (for parsing author birth/death dates from author names)
#import sys                              # take input from command line (in future versions?)

## GLOBAL VARIABLES & FUNCTIONS
totalEpigraphCount = 0                   #number of epigraphs in xml files in corpus
epigraphlessFileCount = 0                #number of xml files in corpus that do not have epigraphs

def count_tags(path, tag):
    with open(path) as xml:
        xml_parsed = etree.parse(xml)
    epigraph_location = xml_parsed.xpath("//tei:" + tag, namespaces = {"tei" : "http://www.tei-c.org/ns/1.0"})
    return len(epigraph_location) 

def count_nested_tags(path, child_tag, ancestor_tag):
    with open(path) as xml:
        xml_parsed = etree.parse(xml)
    child_in_ancestor = xml_parsed.xpath("//tei:" + child_tag + "/ancestor::tei:" + ancestor_tag, namespaces = {"tei" : "http://www.tei-c.org/ns/1.0"})
    return len(child_in_ancestor)
    
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
        soup = BeautifulSoup(readfile, "lxml")                        # Make "soup" object of file to search 
    
    # collect novel author, title of novel, pub date, epigraph, epigraph attrib, pub location, publisher, & encoding company from individual file
        author_list = [author.text for author in soup('author')]   # (1) collect text "author" entries (&, if present, birth/death year)
        
        # identify author birth & death years by scraping from author name, clean up author name entry
        birthDeathYears = []                                          # years extracted from author_list will be placed here
        authorBirthYear = 'No Birth Year'                             # Birth year OR Year if only a single year is provided                  
        authorDeathYear = 'No Death Year'                             # Death year
        birthDeathYears = re.findall('\d{4}', author_list[0])         # scrape years from author name entry if present
        birthDeathYears = [int(string) for string in birthDeathYears] # convert years from strings to integers 
        if len(birthDeathYears) >= 3:                                 # does file have three or more years in author line?
            print('WARNING: ' + str(len(BirthDeathYears)) + ' years in author line in ' + root)
            authorBirthYear = 'Too many years'                        # too many years, not sure which is birth or death
            authorDeathYear = 'Too many years'
        elif len(birthDeathYears) == 2:                               # or two years?  
            authorBirthYear = str(min(birthDeathYears[0],birthDeathYears[1])) # birth year
            authorDeathYear = str(max(birthDeathYears[0],birthDeathYears[1])) # death year
        elif len(birthDeathYears) == 1:
            authorBirthYear = str(birthDeathYears[0])                 # dump single year into birth year
            authorDeathYear = '????'                                  # remind ourselves that we don't know if this year is birth or death with '????'
        
        # find, extract, and remove birth/death year in parentheses from author name
        inParensToRemove = re.findall(r'\((.+)\)', author_list[0])
        if inParensToRemove:
            toRemove = ' ('+ inParensToRemove[0] + ')'
            author_list[0] = author_list[0].replace(toRemove,"")
        
        # find, extract, and remove birth/death year from author name if no parentheses exist
        noParensToRemove = re.findall('\d{4}-\d{4}', author_list[0])  
        if noParensToRemove:
            toRemove = noParensToRemove[0]
            author_list[0] = author_list[0].replace(toRemove,"")
        
        #remove trailing commas or white space in author name if these symbols are present, starting from *last* symbol in author name
        errorcounter = 0
        while author_list[0][-1:] == ' ' or author_list[0][-1:] == ',' or author_list[0][-1:] == '\n':
            errorcounter = errorcounter + 1
            if errorcounter > 8:
                print('ERROR: ' + root + 'author name cleaning stalled. Check file.')
                break
            author_list[0] = author_list[0][:-1]

        title_list = [title.text for title in soup('title')]       # (2) collect text "title" entries
        
        publication_date = [date.text for date in soup('date')]    # (3) collect text pub year entries
        if "eaf" in root:                                          ### select correct year depending on EAF or Wright corpus. Throw warning if not one of these two corpora.
                pub_year = str(publication_date[1])                ### pick 2nd date tag for EAF corpus
        else:
            if "VAC" in root:
                pub_year = str(publication_date[0])                ### pick 1st date tag for Wright corpus
            else: 
                pub_year = 'Unknown Corpus, see terminal warning'  ### WARNING: user must check pub year entry
                print('WARNING: Check publication year for file ' + root +'.'+ ext + '\n') 
                print('List of publication dates in file: \n')
                print(publication_date)
        
        publication_place = [pubplace.text for pubplace in soup('pubplace')]  #(4) collect text pub location
        if len(soup('epigraph')) > 0:                                         #(5) collect entries tagged "epigraph"
            epigraph_list = [epigraph.text for epigraph in soup('epigraph')]  
            epigraph_attribution = ["No Attribution" if soup('epigraph')[epigraphs].bibl == None \
                                                 else  soup('epigraph')[epigraphs].bibl.text \
                                                 for epigraphs in range(0,len(soup('epigraph')))] #(6) collect epigraph attributions
            
            ##see how many quote tags are nested in epigraph tags (for error checking; c.f. line 111)
            if bool(soup('epigraph')) and bool(soup('quote')) == True :  # don't check if there are zero "epipgraph" and/or "quote" tags
                quote_tags_in_epigraph = [0 if soup('epigraph')[epigraphs].quote == None \
                                         else 1 for epigraphs in range(0,len(soup('epigraph')))] # how often is quote tag appearing in epigraph tag? (used to help hunt for untagged epigraphs in corpus)
            else:
                quote_tags_in_epigraph = [0] # either no "quote" or "epigraph" tags or neither, so no quote-in-epigraph tags                             
        else: 
            epigraph_list = ['No Epigraphs']
            epigraph_attribution = ['No Epigraphs']

        if len(soup('publisher')) > 0:         
            publishers = [publisher.text for publisher in soup('publisher')]
        else: 
            publishers = ['Unknown Publisher', 'Unknown Publisher','Unknown Publisher']

    # (7) identify company/individuals that produced each xml file (for exploring provenance of corpus)
        encoders = []
        encoding_counter = 0

        ## for Early American Fiction corpus ...
        if root[:3] == 'eaf': #Not ideal way to handle this, but encoder always 1st 'name' tag in EAF files
            encoders.append(soup('name')[0].text)
            encoding_counter = 1
        
        ## for Wright American Fiction corpus ...
        if root[:3] == 'VAC':            # Wright American Fiction corpus files begin with "VAC" 
            encoders = [soup('change')[encoder].get('who') for encoder in range(0,len(soup('change')))] #get encoders from 'who' attrs in 'change' tags
            encoding_counter = 1

            ### remove duplicate encoders entries, if present
            duplicate_list = []
            for x in range(len(encoders)): #find duplicates and place in 'duplicate_list'
                    if x != 0:
                        if (encoders[0] == encoders[x]):
                            duplicate_list.append(x)
            for deletions in range(len(duplicate_list)): # mark duplicates by replacing element with 'To Erase'
                encoders[duplicate_list[deletions]] = "To Erase"
            for deletions in range(len(encoders)-1,0,-1): # delete duplicate entries
                if encoders[deletions] == "To Erase":
                    del encoders[deletions]

        if encoding_counter == 0:
            print('WARNING: No case selected for encoder attribution for ' + root + '. Check file.')

        if len(encoders) == 0:
            print('WARNING: no encoder info found for ' + root + '. Check file.')  

    # (8) identify epigraphs with 'quote' tag & tracking of who did encoding (see also lines 47-50)  
        total_epigraph_tags = len(soup('epigraph'))        # number of tagged "epigraph"s in file
        total_quote_tags = len(soup('quote'))              # number of tagged "quote"s in file
        if bool(soup('epigraph')) == True:
        #print(quote_tags_in_epigraph)
            quotes_in_epigraphs = sum(quote_tags_in_epigraph)  # number of "quote"s in "epigraph"s  
        else:
            quotes_in_epigraphs = 0    

    ## CLEANING INFORMATION COLLECTED FROM CORPUS
    # remove "/n" characters
        epigraph_attribution = remove_characters(epigraph_attribution, '-\n')
        author_list = remove_characters(author_list, '\n')
        title_list = remove_characters(title_list, '\n')
        publication_place = remove_characters(publication_place, '\n')
        publishers = remove_characters(publishers, '\n')
        pub_year = remove_characters([pub_year], '\n')[0]
        encoders = str(remove_characters(encoders, '\n'))                                  

        readfile.close() #close file "x"

# Error Checking Print-To-Terminal: print all information collected
        if (len(soup('epigraph')) == 0):                         #check if file has epigraphs                
            if (len(soup('author')) > 0):
                epigraphlessFileCount += 1     
            else:
                if (len(soup('author')) == 0):
                    author_list = ['NO AUTHOR TAG IN FILE. CHECK XML FILE!']
                    epigraphlessFileCount += 1 
        else:
            for i in range(0, len(soup.findAll('epigraph'))):          
                if (len(soup.findAll('author')) == 0):
                   totalEpigraphCount += 1
                else:    
                    totalEpigraphCount += 1

#output to a CSV file -- NOTE: need to wrap strings in a list for csvwriter to output properly
        with open('epigraph_metadata.csv', 'a') as csvfile: #output metadata
            epi_meta = csv.writer(csvfile, dialect='excel')
            for i in range(0,len(soup('epigraph'))):
                if (len(soup('author')) ==0):
                    epi_meta.writerow(['junkrow | ' + str(i) + ' | ' + allFilesInDirectory[document] + ' | '+ str(document) + ' | ' +  'Unknown Author' + ' | ' + authorBirthYear + ' | ' + authorDeathYear + ' | ' + str(title_list[0])+ ' | ' + str(epigraph_attribution[i])+ ' | ' + str(publishers[1]) + ' | ' + str(publication_place[1])+ ' | ' + pub_year + ' | junkrow'])           
                else:
                    epi_meta.writerow(['junkrow | ' + str(i) + ' | ' + allFilesInDirectory[document] + ' | '+ str(document) + ' | ' +  author_list[0] + ' | ' + authorBirthYear + ' | ' + authorDeathYear + ' | ' +  str(title_list[0])+ ' | ' + str(epigraph_attribution[i])+ ' | ' +  str(publishers[1]) + ' | ' + str(publication_place[1])+ ' | ' + pub_year + ' | junkrow'])

        with open('epigraph_list.csv', 'a') as csvfile: #output metadata
            epi_list = csv.writer(csvfile, dialect='excel')
            for i in range(0,len(soup('epigraph'))):
                epi_list.writerow([allFilesInDirectory[document] + " | " + str(document+1)+ ', epigraph ' + str(i+1)]) 
                epi_list.writerow([epigraph_list[i]])           

        #output ratio of epigraphs-to-quotes for each file, warnings, & error checks
        with open('epigraph_to_quotes.csv', 'a') as csvfile: 
            epi_to_quote = csv.writer(csvfile, dialect='excel')
            if (document == 0):
                epi_to_quote.writerow(['junkrow | file number | check? | file name | encoding credit | total epigraph tags | total quote tags | quote pairs in epigraphs | junkrow'])
            
            author_error_check = 'Field Empty -- ERROR'
            if len(soup('author')) == 0:
                author_error_check = 'No Author Tags!'
            else:
                author_error_check = str(len(soup('author')))
            
            checkFile = 'yes'   #indicator to inspect novel page image
            checkFile_count = 0 #how many texts do we need to inspect with our eyes
            if count_tags(allFilesInDirectory[document], "epigraph") >= count_nested_tags(allFilesInDirectory[document], "quote", "epigraph") \
               and  count_tags(allFilesInDirectory[document], "epigraph") >= count_tags(allFilesInDirectory[document], "quote") \
               or count_tags(allFilesInDirectory[document], "epigraph") >= 0 and count_tags(allFilesInDirectory[document], "quote") == 0:
               checkFile = 'no'
            else:
               checkFile_count += 1

            epi_to_quote.writerow(['junkrow | ' + str(document) + ' | ' + checkFile + ' | '+ str(allFilesInDirectory[document]) + ' | ' +  encoders + ' | ' + str(total_epigraph_tags) + ' | ' + str(total_quote_tags) + ' | ' + str(quotes_in_epigraphs) + ' | junkrow'])
       
#Error Checking Print-To-Terminal: Print total number of epigraphs collected  
print("TOTAl NUMBER OF EPIGRAPHS: " + str(totalEpigraphCount))
print("TOTAL NUMBER OF FILES: " + str(len(allFilesInDirectory)))
print("FILES WITHOUT EPIGRAPHS: " + str(epigraphlessFileCount))
print("TOTAL NUMBER OF FILES TO INSPECT: " + str(checkFile_count))

#NOTE FOR BS4: soup('epigraph') == soup.find_all('epigraph') == soup.findAll('epigraph')
