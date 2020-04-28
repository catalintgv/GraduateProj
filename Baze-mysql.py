'''5. Creati o baza de date care sa cuprinda urmatoarele tabele:	--pymysql--  sau --sqlite3--
    Categoria
        - idc INT NOT NULL AUTO_INCREMENT PRIMARY KEY (integer in loc de int in sqlite3)
        - denc VARCHAR(255) (text in loc de varchar in sqlite3)
    Produs
        - idp INT NOT NULL AUTO_INCREMENT PRIMARY KEY
        - idc INT NOT NULL
        - denp VARCHAR(255)
        - pret DECIMAL(8,2) DEFAULT 0 (real in loc de decimal)
        # FOREIGN KEY (idc) REFERENCES Categoria.idc ON UPDATE CASCADE ON DELETE RESTRICT
    Operatiuni
        - ido INT NOT NULL AUTO_INCREMENT PRIMARY KEY
        - idp INT NOT NULL
        - cant DECIMAL(10,3) DEFAULT 0
        - data DATE '''


import mysql.connector
import re

# Credentiale conectare
host = "localhost"
passwd = "cata1234"
port = 3306
user = "root"
dbname = "stoc"

# Creare obiect conectare
db = mysql.connector.connect( host=host, port=port, user=user, passwd=passwd, db=dbname )

# Creare cursor
cursor = db.cursor()

cursor.execute ('USE stoc')

cursor.execute("DROP TABLE IF EXISTS Categoria")
cursor.execute("CREATE TABLE Categoria (idc INT NOT NULL PRIMARY KEY AUTO_INCREMENT, denc VARCHAR(255))")
cursor.execute("INSERT INTO Categoria(denc) VALUES('Legume'),('Fructe'),('Mezeluri')")


cursor.execute("DROP TABLE IF EXISTS Produs")
cursor.execute("CREATE TABLE Produs(idp INT NOT NULL AUTO_INCREMENT PRIMARY KEY,idc INT NOT NULL, denp VARCHAR(255), pret DECIMAL(8,2) DEFAULT 0)")
#cursor.execute("CREATE TABLE Produs(idp INT NOT NULL AUTO_INCREMENT PRIMARY KEY,idc INT NOT NULL, denp VARCHAR(255), pret DECIMAL(8,2) DEFAULT 0, FOREIGN KEY (idc) REFERENCES Categoria (idc) ON UPDATE CASCADE ON DELETE RESTRICT)")
#FOREIGN KEY (idc) REFERENCES Categoria (idc) ON UPDATE CASCADE ON DELETE RESTRICT  - cand aveam aceasta optiune setata, nu mai putem face drop table si nu mai puteam testa

#6. Imlementati o solutie cu ajutorul careia sa populati baza de date cu informatiile adecvate.
# INSERT INTO pentru fiecare tabel

#------------------------idc Legume------------------------
cursor.execute("INSERT INTO Produs (idc, denp, pret )  VALUES (1, 'Morcovi', 3.2)")
cursor.execute("INSERT INTO Produs (idc, denp, pret )  VALUES (1, 'Telina', 3.33)")
cursor.execute("INSERT INTO Produs (idc, denp, pret )  VALUES (1, 'Ridichii', 2.14)")
#------------------------idc Fructe---------------------
cursor.execute("INSERT INTO Produs (idc, denp, pret )  VALUES (2, 'Mere', 4.55)")
cursor.execute("INSERT INTO Produs (idc, denp, pret )  VALUES (2, 'Pere', 6.72)")
cursor.execute("INSERT INTO Produs (idc, denp, pret )  VALUES (2, 'Banane', 4.49)")
#------------------------idc Mezeluri--------------------
cursor.execute("INSERT INTO Produs (idc, denp, pret )  VALUES (3, 'Cabanosi', 16.99)")
cursor.execute("INSERT INTO Produs (idc, denp, pret )  VALUES (3, 'Kaizer', 23.99)")
cursor.execute("INSERT INTO Produs (idc, denp, pret )  VALUES (3, 'Salam Sibiu', 35.49)")


cursor.execute("DROP TABLE IF EXISTS Operatiuni")
cursor.execute("CREATE TABLE Operatiuni (ido INT NOT NULL AUTO_INCREMENT PRIMARY KEY, idp INT NOT NULL, cant DECIMAL(10,3) DEFAULT 0, data DATE)")
cursor.execute("INSERT INTO Operatiuni (idp, cant, data) VALUES (2, 451.25, '2008-11-11')")
cursor.execute("INSERT INTO Operatiuni (idp, cant, data) VALUES (5, 505.233, '2009-10-11')")
cursor.execute("INSERT INTO Operatiuni (idp, cant, data) VALUES (8, 25.3, '2010-11-12')")

#6. Imlementati o solutie cu ajutorul careia sa populati baza de date cu informatiile adecvate.
# INSERT INTO pentru fiecare tabel


#7. Creati cateva view-uri cuprinzand rapoarte standard pe baza informatiilor din baza de date. --pentru avansati--
cursor.execute('CREATE VIEW ProduseAccesibile AS SELECT * FROM Produs WHERE pret < 10')
cursor.execute('CREATE VIEW StocSuficient AS SELECT  idp, data FROM Operatiuni WHERE cant > 100')

db.commit()

##categoria = 'select * from categoria'
##cursor.execute(categoria)

#cursor.execute ('show tables;')
#cursor.execute ('select * from categoria;')
#cursor.execute ('select * from Produs;')
cursor.execute ('select * from Operatiuni;')

rez = cursor.fetchall()
for r in rez:
    print (r)



cursor.close()