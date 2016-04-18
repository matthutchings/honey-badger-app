import sqlite3

conn = sqlite3.connect('data.db')
conn.text_factory = str
curs = conn.cursor()


insertRow = 'INSERT INTO %s SELECT * FROM CharList WHERE Name = (?)'
deleteRow = 'DELETE FROM %s WHERE Name = (?)'


def changeScore(newscore, name):
    curs.execute('UPDATE Market SET Score = (?) WHERE Name = (?)', (newscore, name,))
    curs.execute('UPDATE Roster SET Score = (?) WHERE Name = (?)', (newscore, name,))    
    curs.execute('UPDATE Subs SET Score = (?) WHERE Name = (?)', (newscore, name,))
    curs.execute('UPDATE Team SET Score = (?) WHERE Name = (?)', (newscore, name,))
    conn.commit()


def add(name, table):
    curs.execute('INSERT INTO %s SELECT * FROM CharList WHERE Name = (?)'
 % table, (name,))
    conn.commit()


def remove(name, table):
    curs.execute('DELETE FROM %s WHERE Name = (?)'
 % table, (name,))
    conn.commit()


def buy(name):
    # name: MARKET -> ROSTER + SUBS
    add(name, 'Roster')
    add(name, 'Subs')
    remove(name, 'Market')


def sell(name):
    # name: ROSTER + SUBS -> MARKET
    add(name, 'Market')
    remove(name, 'Roster')
    remove(name, 'Subs')
                
   
def subChar(nameOff, nameOn):
    # nameOff: TEAM -> SUBS
    # nameOn: SUBS -> TEAM
    add(nameOff, 'Subs')
    remove(nameOff, 'Team')
    add(nameOn, 'Team')
    remove(nameOn, 'Subs')


def syncTables():
    curs.execute('SELECT Count(*) FROM Market')
    count = int(curs.fetchone()[0])
    print count

    for i in range(count):
        curs.execute('SELECT Name FROM Market LIMIT 1 OFFSET (?)', (i,))
        name = str(curs.fetchone()[0])
        curs.execute('SELECT Score FROM CharList WHERE Name = (?)', (name,))
        newscore = int(curs.fetchone()[0])
        curs.execute('SELECT Score FROM Market WHERE Name = (?)', (name,))
        currentscore = int(curs.fetchone()[0])

        if currentscore != newscore:
            changeScore(newscore, name)

conn.close()
