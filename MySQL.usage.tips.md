*Some Notes To Refer To When Using MySQL Commands*

(1) Structure of the Epi Table:
+----------+--------------+------+-----+---------+-------+
| Field    | Type         | Null | Key | Default | Extra |
+----------+--------------+------+-----+---------+-------+
| No       | int(11)      | NO   | PRI | NULL    |       |
| Filename | varchar(255) | NO   |     | NULL    |       |
| Author   | varchar(255) | YES  |     | NULL    |       |
| Epigraph | text         | YES  |     | NULL    |       |
+----------+--------------+------+-----+---------+-------+


(2) Useful commands & syntax:
  [1] 'mysql -uroot -p' [from terminal] Logon to MySQL as Root to see all DBs
  [2] 'SELECT * FROM EPIDB.Epi'  Output all Data in Table
  [3] 'SELECT No, Filename FROM EPIDB.Epi' Output Epigraph Number & Filename
  [4] 'SELECT Author FROM EPIDB.Epi' Output Hypertext Author & Epigraph
  [5] 'SELECT epigraph FROM Epi WHERE Filename = "brown.xml"' Output all Epigraphs from brown.xml file
