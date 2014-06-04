# TO DO LIST ---------------------------------------------------------------------
#(1) Need to have script collect additional information besides hypertext author, hypertext title, and
# hypertext epigraph. See "Epigraphs Database" google doc at
# https://docs.google.com/spreadsheet/ccc?key=0ArWRJQdqro24dDVXRmw4NVZXQkttVXp4MzJlUElRZEE&usp=drive_web#gid=0
# --------------------------------------------------------------------------------

# libraries & global variables ----------------------------------------------------
from bs4 import BeautifulSoup            #BeautifulSoup parses XML tags.  http://www.crummy.com/software/BeautifulSoup/
from os import walk, getcwd, listdir     #used to grab all files in directory of script
from os.path import isfile, join         #also used in grabbing all files in directory
import os                                
import csv                               #used to interact with csv files (not yet working)
import re                                #handle escape characters for MySQL 
import sys                               #take input from command line
import sqlite3                           #interact with sqlite database

totalEpigraphCount = 0                   #counts total number of epigraphs in all files in directory
epigraphlessFileCount = 0                #counts total number of files in directory that do not have epigraphs

                                       
# begin "connecting to database" section---- ---- ----
try:
     db = sqlite3.connect("Epigraph.db")
except sqlite3.Error,e:         
     print"Failure to connect the database","\n",e.args[0]

cur = db.cursor() #cursor object to execute sql commands

# If the database table exists, delete, & recreate ----
deleteCommand= "DROP TABLE if exists Epi;"
try:
    cur.execute(deleteCommand)
    print "Pre-existing Epi table found. Table deleted."
except sqlite3.Error,e:
    print "Pre-existing Epi table found. Failure to delete the table." , "\n", e.args[0]
db.commit()

#create table in database with (three) attributes) ----
createCommand = "create table Epi(No int not null, Filename varchar(255) not null, Author varchar(255), Epigraph text, primary key(No,Filename));" #create new table  
try:
    cur.execute(createCommand)
except sqlite3.Error,e:
    print "Failure to create the table." , "\n", e.args[0]
db.commit()
# end "connecting to database" section ---- ---- ---- ----

# begin "collect info from XML files" section ---- ---- ----
allFilesInDirectory = [ i for i in listdir(getcwd()) if isfile(join(getcwd(),i)) ] #get list of files in directory

# scrape information from XML files ----
for x in xrange(0, len(allFilesInDirectory)):             #for loop through all files in directory
    root, ext = os.path.splitext(allFilesInDirectory[x])  #select file extension for particular file "x" in the list "allFilesInDirectory"

   # collect info from text documents ----
   try:
      if (ext == '.xml'):                                                   #if file ends in ".xml", read file 
           readfile = open(str(allFilesInDirectory[x]))                     #specify file "x" to be read & open file
           soup = BeautifulSoup(readfile)                                   #make "soup" object of file to search 
           authorlist = [author.text for author in soup('author')]          #collect "author" tagged content; place in "authorlist[]" list
           epigraphlist = [epigraph.text for epigraph in soup('epigraph')]  #collect "epigraph" tagged content; place in "epigraphlist[]" list
           readfile.close()                                                 #close file "x"
   else:
      print "No XML files in directory. The program will only examine XML files in the same directory as itself and ignores everything else." 
    
   # record information to terminal & database ----
   if (len(soup.findAll('epigraph')) == 0):                                                           #check if file has epigraphs                
      print allFilesInDirectory[x] + ": No epigraphs found! (But XML files were found and scanned.)"  #Error Test
      epigraphlessFileCount += 1                                                                      #note file did not have epigraph
   else:   
      for i in xrange(0, len(soup.findAll('epigraph'))): # output author, text, line, and epigraph to terminal and database          
            if (len(soup.findAll('author')) == 0): # case if no "author" entry exists
              print "Unknown Author" + "    " + allFilesInDirectory[x] + "    " + str(i+1) + "   " + epigraphlist[i] # output to terminal
              insertCommand = "insert into Epi values("+ str(i+1)  +","+"\""+allFilesInDirectory[x] + "\""+"," + "\""+"Unknown Author" + "\""+"," + "\""+ epigraphlist[i] + "\""+");"   # collect info for database
              try:
                 cur.execute(insertCommand) # write to DB
              except sqlite3.Error,e:
                 print "Failure to insert data","\n",e.args[0]
                 db.commit() #save to DB
              totalEpigraphCount += 1
            else:    
               print authorlist[0] + "    " + allFilesInDirectory[x] + "    " + str(i+1) + "   " + epigraphlist[i] #output to terminal
               insertCommand = "insert into Epi values("+ str(i+1) + ", " + "\""+allFilesInDirectory[x] + "\""+"," + "\""+authorlist[0] + "\""+"," + "\""+ epigraphlist[i] + "\""+");" #collect info for database
               try:
                    cur.execute(insertCommand) #write to DB
               except sqlite3.Error,e:
                  print "Failure to insert data.","\n",e.args[0]
                  db.commit() #save to DB
               totalEpigraphCount += 1

# commit data to DB and close ----
db.commit() 
db.close()

#Print total number of epigraphs collected to the terminal ----
print "TOTAl NUMBER OF EPIGRAPHS: " + str(totalEpigraphCount)
print "TOTAL NUMBER OF FILES: " + str(len(allFilesInDirectory))
print "FILES WITHOUT EPIGRAPHS: " + str(epigraphlessFileCount)

#CODE SNIPPETS THAT MAY BE USEFUL FOR FUTURE CHANGES ----
#Can directly access individual epigraph as follows:
#soup('author')[0].text
#soup('author')[1].text
#soup('epigraph')[0].text
#soup('epigraph')[1].text
#THIS SHOULD WORK: out.writerow(authorlist[2] + "    " + allFilesInDirectory[x] + "    "
# + str(i) + "   " + epigraph[i])
#out = csv.writer(open("epigraph.csv","wb"), delimiter='\t',quoting=csv.QUOTE_MINIMAL) 
