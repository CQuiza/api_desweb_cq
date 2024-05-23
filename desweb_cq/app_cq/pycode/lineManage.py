'''
Created on 27 feb. 2024

@author: vagrant
'''
from .connPOO import Conn

"""
{'ok':true,'message':f'tuberìas insertados: {n}','data': [[]]}

"""
from .geometryChecks import checkIntersection

class Pipes():
    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert(self, descripcion, geomWkt, material, use)->int:
        print('Iniciando')
        print(geomWkt)
        r=checkIntersection('c.pipes',geomWkt,25830)
        if r:
            return {'ok':False,'message':'El tuberìa intersecta con otra','data':[]}

        print('Despues del check')
        q ="insert into c.pipes (descripcion, length, geom, material, use) values (%s, st_length(%s), st_geometryfromtext(%s,25830), %s, %s) returning gid, length"
        self.conn.cursor.execute(q,[descripcion, geomWkt, geomWkt, material, use])
        self.conn.conn.commit()
        r = self.conn.cursor.fetchall()
        gid = r[0][0]
        length = r[0][1]
        return {'ok':True,'message':f'tuberìa insertada. gid: {gid}','data':[{"gid":gid, "length":length}]}
     
     
    def update(self, descripcion,geomWkt, material, use, gid)->int:
        #r=checkIntersection('c.pipes',geomWkt,25830)
        #if r:
        #    return {'ok':False,'message':'El tuberìa intersecta con otro','data':[]}
        
        q ="update c.pipes set (descripcion, length, geom, material, use) = (%s, st_length(%s), st_geometryfromtext(%s,25830), %s, %s) where gid = %s returning length"
        self.conn.cursor.execute(q,[descripcion,geomWkt, geomWkt, material, use, gid])
        self.conn.conn.commit()
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'ok':False,'message':f'Cero tuberias actualizadas','data':[[0]]}
        elif n==1:
            length = self.conn.cursor.fetchall()[0][0]
            return {'ok':True,'message':f'tuberia actualizada. Filas afectadas: {n}','data':[{"length":length}]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiadas tuberìas actualizadas. Filas afectadas: {n}','data':[[n]]}
        
    def delete(self, gid:int)->int:
        """
        Deletes a building based in the gid
        """
        q="delete from c.pipes where gid = %s"
        self.conn.cursor.execute(q,[gid])
        n= self.conn.cursor.rowcount
        self.conn.conn.commit()
        if n == 0:
            return {'ok':False,'message':f'Cero tuberìas borradas','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'tuberìa borrado. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiadas tuberìas borradas. Filas afectadas: {n}','data':[[n]]}
    
    def select(self, gid:int)->dict:
        q="select gid, descripcion, length, st_astext(geom), material, use from c.pipes where gid = %s"
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'tuberìas seleccionados: {n}','data':l}
        
    def selectAsDict(self, gid:int)->dict:
        q="""
        select array_to_json(array_agg(registros)) from (
            select gid, descripcion, length, st_astext(geom), material, use, st_asgeojson(geom) 
            from c.pipes where gid = %s
            ) as registros
        """
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        r=l[0][0]
        if r is None:
            return {'ok':True,'message':f'tuberìas seleccionados: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'tuberìas seleccionados: {n}','data':r}

    