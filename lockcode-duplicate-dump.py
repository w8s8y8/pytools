import sqlite3

class Locker:
    def __init__(self, substation_id, name, code, pot):
        self.substation_id = substation_id
        self.name = name
        self.code = code
        self.pot = pot

lockers = {}

substations = {}

cursor = sqlite3.connect('xdb.db').cursor()

for record in cursor.execute('SELECT * FROM SubStation'):
    substations[record[0]] = record[2]

for record in cursor.execute('SELECT * FROM Locker'):
    name = record[2]
    code = record[4]
    if len(name) > 0 and len(code) > 0:
        if code in lockers:
            lockers[code].append(Locker(record[1], name, code, record[6]))
        else:
            lockers[code] = [Locker(record[1], name, code, record[6])]

messages = ''

for vs in lockers.values():
    if len(vs) > 1:
        for lock in vs:
            substation = substations[lock.substation_id]
            messages += f'{substation},{lock.name},{lock.code},{lock.pot}\n'
        messages += ',,,\n'

with open('lockers.csv', 'w',  encoding='gb2312') as fp:
    fp.writelines(messages)
