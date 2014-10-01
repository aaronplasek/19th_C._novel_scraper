# libraries
from bs4 import BeautifulSoup            
from os import walk, getcwd, listdir     #used to grab all files in directory of script
from os.path import isfile, join         #also used in grabbing all files in directory
import os                                
import csv                               #used to interact with csv files (not yet working)
import re                                #handle escape characters for MySQL 
import sys                               #take input from command line
import sqlite3                           #interact with sqlite database

# variables
totalEpigraphCount = 0                   #number of epigraphs in all files in directory
epigraphlessFileCount = 0                #number of files in directory that do not have epigraphs

                                       
#connect to database --------------------------------------------------------------
try:
     db = sqlite3.connect("Epigraph.db")
except sqlite3.Error, e:         
     print"Failure to connect the database","\n",e.args[0]

cur = db.cursor() #cursor object will let you execute sql commands

# If the table exists, delete [KEEP FOR TESTING; COMMENT OUT FOR DISTRIBUTION] ---
deleteCommand= "DROP TABLE if exists Epi;"
try:
    cur.execute(deleteCommand)
except sqlite3.Error,e:
    print "Failure to delete the table." , "\n", e.args[0]
db.commit()


#create table in database with three elements --------------------------------------
createCommand = "create table Epi(No int not null, Filename varchar(255) not null, Author varchar(255), Epigraph text, primary key(No,Filename));"  
try:
    cur.execute(createCommand)
except sqlite3.Error,e:
    print "Failure to create the table." , "\n", e.args[0]
db.commit()

#get list of files in current directory & put it in an array ---------------------
allFilesInDirectory = [ i for i in listdir(getcwd()) if isfile(join(getcwd(),i)) ]

#scrape epigraphs from all XML files ---------------------------------------------
for x in xrange(0, len(allFilesInDirectory)):                   #for loop through all files in directory
    root, ext = os.path.splitext(allFilesInDirectory[x])        #select file extension for particular file "x" in the list "allFilesInDirectory"
    if (ext == '.xml'):                                         #if file ends in ".xml", read file 
       
    # open file "x" to be read ---------------------------------------------------
       readfile = open(str(allFilesInDirectory[x]))	        #specify file "x" to be read & open file
       soup = BeautifulSoup(readfile)                           #make "soup" object of file to search 
       
    # strip author & epigraphs from individual file -------------------------------
       authorlist = [author.text for author in soup('author')]          #collect entries tagged "author" and place it in the list "authorlist"
       epigraphlist = [epigraph.text for epigraph in soup('epigraph')]  #collect entries tagged "epigraph" and place it in the list "epigraphlist" 

    # close file -----------------------------------------------------------------
       readfile.close()                                                 #close file "x"
    
    # record information to terminal & database ----------------------------------
       if (len(soup.findAll('epigraph')) == 0):                         #check if file has epigraphs                
          # print allFilesInDirectory[x] + ": No epigraphs found."      #Error Test
          epigraphlessFileCount += 1                                    #note file did not have epigraph
       else:
          # output author, text, line, and epigraph to terminal and database   
          for i in xrange(0, len(soup.findAll('epigraph'))):          
             if (len(soup.findAll('author')) == 0):
                 print "Unknown Author" + "    " + allFilesInDirectory[x] + "    " + str(i+1) + "   " + epigraphlist[i]
                 # output to database 
                 insertCommand = "insert into Epi values("+ str(i+1)  +","+"\""+allFilesInDirectory[x] + "\""+"," + "\""+"Unknown Author" + "\""+"," + "\""+ epigraphlist[i] + "\""+");"
                 try:
                     cur.execute(insertCommand)
                 except sqlite3.Error,e:
                     print "Failure to insert data","\n",e.args[0]
                 db.commit()
                 totalEpigraphCount += 1
             else:    
                 print authorlist[0] + "    " + allFilesInDirectory[x] + "    " + str(i+1) + "   " + epigraphlist[i]
                 # output to database
                 insertCommand = "insert into Epi values("+ str(i+1) + ", " + "\""+allFilesInDirectory[x] + "\""+"," + "\""+authorlist[0] + "\""+"," + "\""+ epigraphlist[i] + "\""+");"
                 try:
                     cur.execute(insertCommand)
                 except sqlite3.Error,e:
                     print "Failure to insert data.","\n",e.args[0]
                 db.commit()
                 totalEpigraphCount += 1

# commit data to DB and close -----------------------------------------------------
db.commit() 
db.close()

#Print total number of epigraphs collected to the terminal -------------------------
print "TOTAl NUMBER OF EPIGRAPHS: " + str(totalEpigraphCount)
print "TOTAL NUMBER OF FILES: " + str(len(allFilesInDirectory))
print "FILES WITHOUT EPIGRAPHS: " + str(epigraphlessFileCount)

#CODE SNIPPETS THAT MAY BE USEFUL FOR FUTURE CHANGES ------------------------------
#Can directly access individual epigraph as follows:
#soup('author')[0].text
#soup('author')[1].text
#soup('epigraph')[0].text
#soup('epigraph')[1].text
#THIS SHOULD WORK: out.writerow(authorlist[2] + "    " + allFilesInDirectory[x] + "    "
# + str(i) + "   " + epigraph[i])
#out = csv.writer(open("epigraph.csv","wb"), delimiter='\t',quoting=csv.QUOTE_MINIMAL) 
