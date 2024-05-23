'''
Created on 27 feb. 2024

@author: vagrant
'''
from .connPOO import Conn

"""
{'ok':true,'message':f'Edificios insertados: {n}','data': [[]]}

"""
from .geometryChecks import checkIntersection

class Constructions():
    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert(self, city, days_limit, org_responsible, geomWkt)->int:
        print('Iniciando')
        print(geomWkt)
        r=checkIntersection('c.constructions',geomWkt,25830)
        if r:
            return {'ok':False,'message':'El edificio intersecta con otro','data':[]}

        print('Despues del check')
        q ="insert into c.constructions (city, days_limit, area, org_responsible, geom) values (%s, %s, st_area(st_geometryfromtext(%s,25830)),%s, %s) returning gid, area"
        self.conn.cursor.execute(q,[city, days_limit, geomWkt, org_responsible, geomWkt])
        self.conn.conn.commit()
        r = self.conn.cursor.fetchall()
        print("---",r)
        gid = r[0][0]
        area = r[0][1]
        return {'ok':True,'message':f'Obra insertada. gid: {gid}','data':[{"gid":gid, "area":area}]}
     
     
    def update(self, gid, city, days_limit, org_responsible, geomWkt)->int:
               
        q ="update c.constructions set (city, days_limit, area, org_responsible, geom) = (%s,%s,st_area(st_geometryfromtext(%s,25830)),%s,st_geometryfromtext(%s,25830)) where gid = %s returning area"
        self.conn.cursor.execute(q,[city, days_limit, geomWkt, org_responsible, geomWkt, gid])
        self.conn.conn.commit()
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'ok':False,'message':f'Cero obras actualizadas','data':[[0]]}
        elif n==1:
            area = self.conn.cursor.fetchall()[0][0]
            return {'ok':True,'message':f'Obra actualizada. Filas afectadas: {n}','data':[{"area":area}]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiadas obras actualizadas. Filas afectadas: {n}','data':[[n]]}
        
    def delete(self, gid:int)->int:
        """
        Deletes a building based in the gid
        """
        q="delete from c.constructions where gid = %s"
        self.conn.cursor.execute(q,[gid])
        n= self.conn.cursor.rowcount
        self.conn.conn.commit()
        if n == 0:
            return {'ok':False,'message':f'Cero obras borradas','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'Obra borrado. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiadas obras borradas. Filas afectadas: {n}','data':[[n]]}
    
    def select(self, gid:int)->dict:
        q="select gid, city, days_limit, area, org_responsible, st_astext(geom) from c.constructions where gid = %s"
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'Obras seleccionados: {n}','data':l}
        
    def selectAsDict(self, gid:int)->dict:
        q="""
        SELECT array_to_json(array_agg(registros)) FROM (
            select gid, city, days_limit, area, org_responsible, st_astext(geom), st_asgeojson(geom) 
            from c.constructions where gid = %s
         ) as registros
        """
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        r=l[0][0]
        if r is None:
            return {'ok':True,'message':f'Obras seleccionados: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'Obras seleccionados: {n}','data':r}

    