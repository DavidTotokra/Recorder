import urllib.request
import datetime
import sqlite3
import faker
from docopt import docopt

# CLI

usage = '''


Usage:  
    audioR2.py -l | --list
    audioR2.py <url> [--filename=<audioname>] [--duration=<dauer>] 
    audioR2.py -h | --help

Options:
    -h --help                 Show this screen.
    --filename=<filename>     Name of recording [default: myradio.mp3].
    --duration=<duration>     Duration of recording in seconds [default: 22].
    -l --list                 List all recordings.
'''


# Musik

def record(url, dauer, name):
    
    
    # Öffnen die URL
    # Working link : http://stream.antennethueringen.de/live/mp3-128/
    

    size = 200

    # Sample rate
    # fs = 44100

    stream = urllib.request.urlopen(url)
    start = datetime.datetime.now()

    with open(name, 'wb') as f:
        while (datetime.datetime.now() - start).seconds < dauer:
            f.write(stream.read(size))


# Datenbank

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





if __name__ == '__main__':
    
    co = sqlite3.connect('music_db.sqlite')
    arguments = docopt(usage)
    create_table(co)


    if arguments['--list']:
        print_list(co)
    else:
        record(arguments['<url>'], dauer=int(arguments['--duration']), name=arguments['--filename'])
        insert_wert_data(co)
        