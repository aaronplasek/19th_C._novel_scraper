#see readme file before using!

#libraries & Global variables ----------------------------------------------------
from bs4 import BeautifulSoup
from os import walk, getcwd, listdir
from os.path import isfile, join
import os
import csv
import re
import sqlite3
import sys


totalEpigraphCount = 0
epigraphlessFileCount = 0
#out = csv.writer(open("epigraph.csv","wb"), delimiter='\t',quoting=csv.QUOTE_MINIMAL)

#connect to database -------------------------------------------------------------
try:
    db = sqlite3.connect("Epigraph.db")
except sqlite3.Error,e:
    print"Failure to connect the database","\n",e.args[0]

# Name of the data base
# If exists, then open the database; if not, then create it and open it.

# The Cursor object will let you execute the sql commands
cur = db.cursor()

# crete a table with attributes---------------------------------------------------
# If the table exists, delete it and recreate it.
deleteCommand= "DROP TABLE if exists Epi;"
try:
    cur.execute(deleteCommand)
except sqlite3.Error,e:
    print "Failure to delete the talbe." , "\n", e.args[0]

db.commit()


createCommand = "create table Epi(No integer not null, Filename varchar(255) not null, Author varchar(255), Epigraph text, HypertextAttribute varchar(255), primary key(No,Filename)) ;"
try:
    cur.execute(createCommand)
except sqlite3.Error,e:
    print "Failure to create the talbe." , "\n", e.args[0]

db.commit()

#get only files from directory & loop through each file --------------------------
allFilesInDirectory = [ i for i in listdir(getcwd()) if isfile(join(getcwd(),i)) ]

for x in xrange(0, len(allFilesInDirectory)):
    root, ext = os.path.splitext(allFilesInDirectory[x])
    if (ext == '.xml'):
        
        # open file to be read -------------------------------------------------------
        readfile = open(str(allFilesInDirectory[x]))	#specific file to be examined
        soup = BeautifulSoup(readfile) #make file "soup" object for easy searching
        
        # strip author & epigraphs from individual file-------------------------------
        authorlist = [author.text for author in soup('author')]  #collect author entries
        epigraphlist = [epigraph.text for epigraph in soup('epigraph')]  #collect epigraphs
        
        # close file------------------------------------------------------------------
        readfile.close()
        
        # print out contents to terminal and database---------------------------------
        if (len(soup.findAll('epigraph')) == 0):
            #print allFilesInDirectory[x] + ": No epigraphs found." #Error Test
            epigraphlessFileCount += 1
        else:
            for i in xrange(0, len(soup.findAll('epigraph'))):
                # save the every sentence in epigraph and save the last sentense into database as epigraph author
                TheEpigraph=epigraphlist[i].split('\n')
                NewEpigraph=[]
                for sentence in TheEpigraph:
                    if len(sentence)!=0:
                        NewEpigraph.append(sentence)
            
                if len(NewEpigraph)>1:
                    if u'\u201d' not in NewEpigraph[len(NewEpigraph)-1]:
                        EpigraphAuthor=NewEpigraph[len(NewEpigraph)-1];
                    else:
                        EpigraphAuthor="Unknown Hypertext Attribute"
                else:
                    EpigraphAuthor="Unknown Hypertext Attribute"

                if (len(soup.findAll('author')) == 0):
                    print "Unknown Author" + "    " + allFilesInDirectory[x] + "    " + str(i+1) + "   " +EpigraphAuthor+"   "+ epigraphlist[i]
                    totalEpigraphCount += 1
                    
                    # insert into database
                    insertCommand = "insert into Epi values (?,?,?,?,?)"
                    #print insertCommand
                    try:
                        cur.execute(insertCommand,(str(i+1),allFilesInDirectory[x],"Unknown Author",epigraphlist[i],EpigraphAuthor))
                    except sqlite3.Error,e:
                        print "Failure to insert data.","\n",e.args[0]
                    
                    db.commit()
                
                
                else:
                    print authorlist[0] + "    " + allFilesInDirectory[x] + "    " + str(i+1) + "   " +EpigraphAuthor+"   "+ epigraphlist[i]
                    totalEpigraphCount += 1
                    
                    # insert into database
                    insertCommand = "insert into Epi values (?,?,?,?,?)"
                    #print insertCommand
                    try:
                        cur.execute(insertCommand,(str(i+1),allFilesInDirectory[x],authorlist[0],epigraphlist[i],EpigraphAuthor))
                    except sqlite3.Error,e:
                        print "Failure to insert data.","\n",e.args[0]
                    
                    db.commit()




print "TOTAl NUMBER OF EPIGRAPHS: " + str(totalEpigraphCount)
print "TOTAL NUMBER OF FILES: " + str(len(allFilesInDirectory))
print "FILES WITHOUT EPIGRAPHS: " + str(epigraphlessFileCount),"\n\n"

# Select everyting from xml files in database---------------------------------------------------------------------------------

print "Which file do you want to read?" ,"\n","Please type the numbers of the files and then press Enter : " ,"\n"

# Show all filenames in database
selectFile = "SELECT distinct Filename FROM Epi;"
cur.execute(selectFile)

FileNumber=0
FileList=[]
for filenames in cur:
    FileNumber+=1
    FileList.append(filenames[0])
    print str(FileNumber)+str(' ')+str(filenames),"\n"



# Read input from user

line = sys.stdin.readline()
line=line.split()

# Select everyting from the xml files that user want
for FileIndex in line:
    
    if (int(FileIndex)>0 and int(FileIndex)<FileNumber+1):
        TheFilename=FileList[int(FileIndex)-1]
        print str(TheFilename)
        selectCommand = "SELECT * FROM Epi where Filename='"+str(TheFilename)+"';"
        cur.execute(selectCommand)
        k=0;
        for row in cur:
            k+=1;
            print row ,"\n"
        print "TOTAl NUMBER OF ROWS: " + str(k)+"\n"
    
    else:
        print "No such file number: " + str(FileIndex),"\n"


db.close()
#Notes for future changes--------------------------
#Can directly access individual epigraph as follows:
#soup('author')[0].text
#soup('author')[1].text
#soup('epigraph')[0].text
#soup('epigraph')[1].text
#THIS SHOULD WORK: out.writerow(authorlist[2] + "    " + allFilesInDirectory[x] + "    "
# + str(i) + "   " + epigraph[i])
