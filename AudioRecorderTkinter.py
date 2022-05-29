import threading
import urllib.request
import datetime
import sqlite3
from tkinter import *
import faker






def record():
    # Öffnen die URL

    # Working link : http://stream.antennethueringen.de/live/mp3-128/

    filename= name.get()
    web= url.get()
    daur= dauer.get()
    size = 200
    stream = urllib.request.urlopen(web)
    start = datetime.datetime.now()
    file = open(filename+ '.mp3', 'wb')

    while (datetime.datetime.now() - start).seconds < int(daur):
        file.write(stream.read(int(size)))
    file.close()


def create_table(co):
    c = co.cursor()
    c.execute('''
                CREATE TABLE IF NOT EXISTS radio1(
                    name varchar (50),
                    dauer int DEFAULT '22',
                    size int DEFAULT '200',
                    help text
                );

            ''')
    co.commit()


def insert_wert_data(co):
    c = co.cursor()
    f = faker.Faker()
    sql = '''
    INSERT INTO radio1(name, help) VALUES (?,?);
    '''

    c.execute(sql,(f.name(), f.text()[:40]))

    co.commit()


def print_list(co):
    c = co.cursor()
    c.execute('SELECT * FROM radio1;')
    r = c.fetchall()

    for row in r:
        name, dauer, size, help = row
        print(f'{name:>50} {dauer} {size} {help}')



# Tkinter


master = Tk()

master.geometry("450x300")
master.title('Voice Recoder')


w =  Label(master, text = "Url")
w.pack()
url=Entry(master)
url.pack()


y = Label(master, text = "filename")
y.pack()
name=Entry(master)
name.pack()

x = Label(master, text = "dauer")
x.pack()
dauer = Entry(master)
dauer.pack()



b = Button(master, text="Start", command=record)
b.pack()


if __name__ == '__main__':
    co = sqlite3.connect('music1.sqlite')
    create_table(co)
    insert_wert_data(co)
    print_list(co)
    master.mainloop()

