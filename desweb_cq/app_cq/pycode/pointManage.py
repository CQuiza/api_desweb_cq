'''
Created on 27 feb. 2024

@author: vagrant
'''
from .connPOO import Conn

"""
{'ok':true,'message':f'Edificios insertados: {n}','data': [[]]}

"""
from .geometryChecks import checkIntersection

class Wells():
    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert(self, descripcion, depth, geomWkt, radius, type)->int:
        print('Iniciando')
        print(geomWkt)
        r=checkIntersection('c.wells',geomWkt,25830)
        if r:
            return {'ok':False,'message':'El pozo intersecta con otro','data':[]}

        print('Despues del check')
        q ="insert into c.wells (descripcion, depth, geom, radius, type) values (%s, %s,st_geometryfromtext(%s,25830), %s, %s) returning gid"
        self.conn.cursor.execute(q,[descripcion, depth, geomWkt, radius, type])
        self.conn.conn.commit()
        gid = self.conn.cursor.fetchall()[0][0]
        return {'ok':True,'message':f'well insert. gid: {gid}','data':[{"gid":gid}]}
    
     
    def update(self, descripcion, depth, geomWkt, radius, type, gid)->int:
        #r=checkIntersection('c.wells',geomWkt,25830)
        #if r:
        #    return {'ok':False,'message':'El edificio intersecta con otro','data':[]}
        
        q ="update c.wells set (descripcion, depth, geom, radius, type) = (%s, %s, st_geometryfromtext(%s,25830), %s, %s) where gid = %s"
        self.conn.cursor.execute(q,[descripcion, depth, geomWkt, radius, type, gid])
        self.conn.conn.commit()
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'ok':False,'message':f'Cero pozos actualizadas','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'Pozo actualizado. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiados pozos actualizadas. Filas afectadas: {n}','data':[[n]]}
        
    def delete(self, gid:int)->int:
        """
        Deletes a building based in the gid
        """
        q="delete from c.wells where gid = %s"
        self.conn.cursor.execute(q,[gid])
        n= self.conn.cursor.rowcount
        self.conn.conn.commit()
        if n == 0:
            return {'ok':False,'message':f'Cero pozos borradas','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'pozo borrado. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiados pozos borradas. Filas afectadas: {n}','data':[[n]]}
    
    def select(self, gid:int)->dict:
        q="select gid, descripcion, depth, st_astext(geom), radius, type from c.wells where gid = %s"
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'pozos seleccionados: {n}','data':l}
        
    def selectAsDict(self, gid:int)->dict:
        q="""
        select array_to_json(array_agg(registros)) from (
            select gid, descripcion, depth, st_astext(geom), radius, type, st_asgeojson(geom) 
            from c.wells where gid = %s
            ) as registros
        """
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        r=l[0][0]
        if r is None:
            return {'ok':True,'message':f'pozos seleccionados: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'pozos seleccionados: {n}','data':r}

    


