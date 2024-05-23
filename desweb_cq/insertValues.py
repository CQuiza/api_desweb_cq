
from appdesweb.pycode.connPOO import Conn

conn = Conn()
print('Insertando')
conn.cursor.execute('insert into demo (descripcion) values (%s)',['Esto funciona'])
print('Hecho')
conn.conn.commit()