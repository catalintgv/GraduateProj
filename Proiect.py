"""
    Avem aplicatia care tine stocul unui depozit (Cap 5-6). Efectuati urmatoarele imbunatatiri:

	Este necesar rezolvati minim 3 din punctele de mai jos:

1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
anumita perioada, pentru un anumit produs;	--pygal--

2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o
limita minima, predefinita per produs. Limita sa poata fi variabila (per produs). Preferabil sa
transmita automat un email de avertizare;

3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii(
de exemplu fisa produsului) ; 	--SMTP--

4. Utilizati Regex pentru a cauta :
    - un produs introdus de utilizator;
    - o tranzactie cu o anumita valoare introdusa de utilizator;	--re--

5. Creati o baza de date care sa cuprinda urmatoarele tabele:	--pymysql--  sau --sqlite3--
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
        - data DATE

6. Imlementati o solutie cu ajutorul careia sa populati baza de date cu informatiile adecvate.

7. Creati cateva view-uri cuprinzand rapoarte standard pe baza informatiilor din baza de date. --pentru avansati--

8. Completati aplicatia astfel incat sa permita introducerea pretului la fiecare intrare si iesire.
Pretul de iesire va fi pretul mediu ponderat (la fiecare tranzactie de intrare se va face o medie intre
pretul produselor din stoc si al celor intrate ceea ce va deveni noul pret al produselor stocate).
Pretul de iesire va fi pretul din acel moment; --pentru avansati--

9. Creati doua metode noi, testatile si asigurativa ca functioneaza cu succes;


""" #


from datetime import datetime
from prettytable import PrettyTable
import pygal
import os
import smtplib
import pftp #parola mail
import re
import mysql

class Stoc():


    def __init__(self,numeP ,categP, um='Buc', sold=0 , soldminProd=0): #la initializarea obiectului setam soldul minim
        self.numeP = numeP
        self.categP = categP
        self.um = um
        self.sold = sold
        self.dop = {}
        self.dint = {}
        self.dout = {}
        self.soldminProd = soldminProd # variabila soldminProd cu care comparam sold
        self.warning = '' # mesaj atentionare limita stoc, pe care sa il poti folosi in email.


    def intrari(self, cantit, data = str(datetime.now().strftime('%Y%m%d'))):
        self.cantit = cantit
        self.data = data
        if self.dop.keys():
            cheie = len(self.dop.keys())+1
        else:
            cheie = 1

        self.dop[cheie]=self.data
        self.dint[cheie]=self.cantit
        self.sold += self.cantit


    def iesiri(self, cant, data = str ( datetime.now ( ).strftime ( '%Y%m%d' ) )):
        self.cant = cant
        self.data = data
        if self.dop.keys():
            cheie = len(self.dop.keys()) + 1
        else:
            cheie = 1
        self.dop[cheie] = self.data
        self.dout[cheie] = self.cant
        self.sold -= self.cant

    def fisaP(self):
        print('Fisa produsului:', self.numeP, 'unitatea de masura:',self.um)
        listeaza = PrettyTable()
        listeaza.field_names = ['Nrc', 'Data', 'Intrare', 'Iesire']

        for elem in self.dop.keys():
            if elem in self.dint.keys():
                listeaza.add_row([elem, self.dop[elem], self.dint[elem], str(0)])

            else:
                listeaza.add_row([elem, self.dop[elem], str(0), self.dout[elem]])

        listeaza.add_row(['---------','--------','------','----'])
        listeaza.add_row(['Sold final', self.categP, self.numeP, self.sold])
        print(listeaza)


#2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o
#limita minima, predefinita per produs. Limita sa poata fi variabila (per produs). Preferabil sa
#transmita automat un email de avertizare;

        if self.sold < self.soldminProd:
            self.warning = 'ATENTIE !!!  Stocul de ' + self.numeP  + ' se afla sub limita minima de ' + str(self.soldminProd) + ' unitati!'
            print (self.warning)
            self.sendMail()  #trimite mail numai daca soldul se afla sub limita impusa


#'''1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
#anumita perioada, pentru un anumit produs;	--pygal-- '''
# 9. Creati doua metode noi, testatile si asigurativa ca functioneaza cu succes;

    def listeazaPy(self):
        bar_chart = pygal.Bar()
        bar_chart.title = 'Stoc produs'
        bar_chart.human_readable = True
        operatiuni = []
        for o in self.dop.values():
            operatiuni.append(o)

        bar_chart.x_title = 'Data operatiune'

        bar_chart.x_labels = [*operatiuni] # valori dop
        #operatiuniSet = set(operatiuni)
        #bar_chart.x_labels = [*operatiuniSet] # valori dop
        bar_chart.y_title = 'Operatiuni - Intrari/Iesiri'

        intrari= list()
        for kin in self.dint.keys():
            if kin in self.dop.keys():
                intrari.append(self.dint.get(kin))
                intrari.append(0)


        iesiri = []
        for kout in self.dout.keys():
            if kout in self.dop.keys():
                iesiri.append(0)
                iesiri.append(self.dout.get(kout))

        bar_chart.add ( 'Intrari', [*intrari] )
        bar_chart.add ( 'Iesiri', [*iesiri] )



        bar_chart.render_to_file ('Stoc.svg')
        os.system('Stoc.svg')




#2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o
#limita minima, predefinita per produs. Limita sa poata fi variabila (per produs). Preferabil sa
#transmita automat un email de avertizare;


    def sendMail(self):

        expeditor = 'cp@gmail.ro'  #conturile de mail sunt fictive din motive protectie dar functioneaza cu cont real
        destinatar = 'cpd@gmail.ro'
        username = 'cp@gmail.ro'
        parola = pftp.parola
        mesaj = """From: Catalin <cp@gmail.ro>
To: Dumitru <cpd@gmail.ro>
Subject: Atentionare stoc

Salut Ionel,

{}

Catalin,""".format(self.warning)

        try:
            smtp_ob = smtplib.SMTP('gmail.ro:25')
            smtp_ob.login(username, parola)
            smtp_ob.sendmail(expeditor, destinatar, mesaj)
            print('Mesaj expediat cu succes!')
        except:
            print('Mesajul nu a putut fi expediat!')


#3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii(
#de exemplu fisa produsului) ; 	--SMTP--

    def fisaPsendMail(self):
        print('test sendmail')#
        expeditor = 'cp@gmail.ro'
        destinatar = 'cpd@gmail.ro'
        username = 'cp@gmail.ro'
        parola = pftp.parola
        body = PrettyTable()
        body.field_names = ['Nrc', 'Data', 'Intrare', 'Iesire']

        for elem in self.dop.keys():
            if elem in self.dint.keys():
                body.add_row([elem, self.dop[elem], self.dint[elem], str(0)])

            else:
                body.add_row([elem, self.dop[elem], str(0), self.dout[elem]])

        body.add_row(['---------','--------','------','----'])
        body.add_row(['Sold final', self.categP, self.numeP, self.sold])
        mesaj = """From: Catalin <cp@gmail.ro>
To: Dumitru <cpd@gmail.ro>
Subject: Fisa produsului {0} !


Salut Daniel, in mail gasesti fisa produsului {0}, in unitatea de masura: {1}

{2}


Catalin,


""".format(self.numeP, self.um, body)

        try:
            smtp_ob = smtplib.SMTP('gmail.ro')
            smtp_ob.login(username, parola)
            smtp_ob.sendmail(expeditor, destinatar, mesaj)
            print('Mesaj expediat cu succes!')
        except:
            print('Mesajul nu a putut fi expediat!')


#4. Utilizati Regex pentru a cauta :
#    - un produs introdus de utilizator;
#    - o tranzactie cu o anumita valoare introdusa de utilizator;	--re--










rosii = Stoc('Rosii','Legume','Kg', 0 ,5)
rosii.intrari(23,'20200120')
rosii.iesiri(18 , '20200121')
rosii.intrari(23 , '20200121')
rosii.iesiri(15, '20200201')
rosii.intrari(12, '20200203')
rosii.iesiri(2,'20200204')


bere = Stoc('Ursus', 'Alcool','Navete',0,5)  #limita stoc este 5
bere.intrari(3, '20200118')
bere.iesiri(1,'20200119' )
bere.intrari(4, '20200120')
bere.iesiri(3, '20200122' )



#rosii.fisaP()
#rosii.listeazaPy()
#bere.fisaP()  #aici se poate testa warning send mail
#rosii.fisaPsendMail()