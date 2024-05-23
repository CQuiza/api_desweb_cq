import json
#Django imports
from django.http import JsonResponse
#from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .pycode import connPOO, polygonManage, pointManage, lineManage
from .pycode.libs import general
from django.utils.decorators import method_decorator
#from django.contrib.auth import logout
#from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
#from django.views.decorators.csrf import csrf_exempt
#from django.utils.decorators import method_decorator


class HelloWord(View):
    def get(self, request):
        return JsonResponse({"ok":"true","message": "Hello world", "data":[]})


class HolaClase(View):
    def get(self, request):
        area=request.GET['area']
        return JsonResponse({"ok":"true","message": "Hola clase", "data":[{'area':area}]})


class ConstructionSelectByGid(View):
    def get(self, request):
        gid=request.GET['gid']
        conn=connPOO.Conn()
        b=polygonManage.Constructions(conn)
        r=b.selectAsDict(gid)
        print(r)
        return JsonResponse(r)
    
class ConstructionInsert(LoginRequiredMixin, View):
    def post(self, request):

        #The following does not work with axios
        #descripcion=request.POST['descripcion']
        #geomWkt=request.POST['geomWkt']

        d=general.getPostFormData(request)
        city=d['city']
        days_limit=d['days_limit']
        org_responsible=d['org_responsible']
        geomWkt=d['geomWkt']
        conn=connPOO.Conn()
        b=polygonManage.Constructions(conn)
        r=b.insert(city, days_limit, org_responsible, geomWkt)
        print(r)
        return JsonResponse(r)
    
class ConstructionUpdate(LoginRequiredMixin, View):
    def post(self, request):
        d=general.getPostFormData(request)
        gid=d['gid']
        city=d['city']
        days_limit=d['days_limit']
        org_responsible=d['org_responsible']
        geomWkt=d['geomWkt']
        print(gid,geomWkt)
        conn=connPOO.Conn()
        b=polygonManage.Constructions(conn)
        r=b.update(gid, city, days_limit, org_responsible, geomWkt)
        return JsonResponse(r)


class ConstructionDelete(LoginRequiredMixin, View):
    def post(self, request):
        d=general.getPostFormData(request)
        gid=d['gid']
        print(gid)
        conn=connPOO.Conn()
        b=polygonManage.Constructions(conn)
        r=b.delete(gid)
        return JsonResponse(r)
    def delete(self, request):
        gid=request.POST['gid']
        print(gid)
        conn=connPOO.Conn()
        b=polygonManage.Constructions(conn)
        r=b.delete(gid)
        return JsonResponse(r)
    

'''views para manejar las geometrias de los pozos'''

class WellSelectByGid(View):
    def get(self, request):
        gid=request.GET['gid']
        conn=connPOO.Conn()
        b=pointManage.Wells(conn)
        r=b.selectAsDict(gid)
        return JsonResponse(r)
    
class WellInsert(LoginRequiredMixin, View):
    def post(self, request):

        #The following does not work with axios
        #descripcion=request.POST['descripcion']
        #geomWkt=request.POST['geomWkt']

        d=general.getPostFormData(request)
        descripcion=d['descripcion']
        depth=d['depth']
        geomWkt=d['geomWkt']
        radius=d['radius']
        type = d['type']
        print(geomWkt)
        conn=connPOO.Conn()
        b=pointManage.Wells(conn)
        r=b.insert(descripcion, depth, geomWkt,radius, type)
        return JsonResponse(r)
    
class WellUpdate(LoginRequiredMixin, View):
    def post(self, request):
        d=general.getPostFormData(request)
        gid=d['gid']
        descripcion=d['descripcion']
        depth=d['depth']
        geomWkt=d['geomWkt']
        radius=d['radius']
        type = d['type']
        print(gid,geomWkt)
        conn=connPOO.Conn()
        b=pointManage.Wells(conn)
        r=b.update(descripcion, depth, geomWkt,radius, type, gid)
        return JsonResponse(r)


class WellDelete(LoginRequiredMixin, View):
    def post(self, request):
        d=general.getPostFormData(request)
        gid=d['gid']
        print(gid)
        conn=connPOO.Conn()
        b=pointManage.Wells(conn)
        r=b.delete(gid)
        return JsonResponse(r)
    def delete(self, request):
        gid=request.POST['gid']
        print(gid)
        conn=connPOO.Conn()
        b=pointManage.Wells(conn)
        r=b.delete(gid)
        return JsonResponse(r)
    

'''views para manejar las geometrias de los tuberìa'''

class PipeSelectByGid(View):
    def get(self, request):
        gid=request.GET['gid']
        conn=connPOO.Conn()
        b=lineManage.Pipes(conn)
        r=b.selectAsDict(gid)
        return JsonResponse(r)

class PipeInsert(LoginRequiredMixin, View):
    def post(self, request):

        #The following does not work with axios
        #descripcion=request.POST['descripcion']
        #geomWkt=request.POST['geomWkt']

        d=general.getPostFormData(request)
        descripcion=d['descripcion']
        geomWkt=d['geomWkt']
        material=d['material']
        use = d['use']
        print(geomWkt)
        conn=connPOO.Conn()
        b=lineManage.Pipes(conn)
        r=b.insert(descripcion, geomWkt, material, use)
        return JsonResponse(r)
    
class PipeUpdate(LoginRequiredMixin, View):
    def post(self, request):
        d=general.getPostFormData(request)
        gid=d['gid']
        descripcion=d['descripcion']
        geomWkt=d['geomWkt']
        material=d['material']
        use = d['use']
        print(gid,geomWkt)
        conn=connPOO.Conn()
        b=lineManage.Pipes(conn)
        r=b.update(descripcion, geomWkt, material, use, gid)
        return JsonResponse(r)
    
class PipeDelete(LoginRequiredMixin, View):
    def post(self, request):
        d=general.getPostFormData(request)
        gid=d['gid']
        print(gid)
        conn=connPOO.Conn()
        b=lineManage.Pipes(conn)
        r=b.delete(gid)
        return JsonResponse(r)
    def delete(self, request):
        gid=request.POST['gid']
        print(gid)
        conn=connPOO.Conn()
        b=lineManage.Pipes(conn)
        r=b.delete(gid)
        return JsonResponse(r)
    

        
'''class ConstructionSelectByGid2(View):
    def get(self, request,gid):
        #gid=request.GET['gid']
        conn=connPOO.Conn()
        b=polygonManage.Constructions(conn)
        r=b.selectAsDict(gid)
        return JsonResponse(r)

class ConstructionSelectByArea(View):
    def get(self, request):
        area=request.GET['area']
        conn=connPOO.Conn()
        b=polygonManage.Constructions(conn)
        r=b.selectAsDictByArea(area=area)
        return JsonResponse(r)
    

class ConstructionGet(View):
    def get(self, request):
        gid=request.GET['gid']
        conn=connPOO.Conn()
        b=polygonManage.Constructions(conn)
        r=b.selectAsDict(gid)
        return JsonResponse(r)
        #return JsonResponse({'mens':'Metodo get para seleccionar'})

class ConstructionPost(LoginRequiredMixin,View):
    def post(self, request):
        d=general.getPostFormData(request)
        city=d['city']
        days_limit=d['days_limit']
        org_responsible=d['org_responsible']
        geomWkt=d['geomWkt']
        print(geomWkt)
        conn=connPOO.Conn()
        b=polygonManage.Constructions(conn)
        r=b.insert(city, days_limit, org_responsible, geomWkt)
        return JsonResponse(r)
        #return JsonResponse({'mens':'Metodo post para insertar'})

    def put(self, request):
        d=general.getPostFormData(request)
        gid=d['gid']
        city=d['city']
        days_limit=d['days_limit']
        org_responsible=d['org_responsible']
        geomWkt=d['geomWkt']
        print(gid,geomWkt)
        conn=connPOO.Conn()
        b=polygonManage.Constructions(conn)
        r=b.update(gid, city, days_limit, org_responsible, geomWkt)
        return JsonResponse(r)
        #return JsonResponse({'mens':'Metodo put para update'})
    
    def delete(self, request):
        gid=request.POST['gid']
        print(gid)
        conn=connPOO.Conn()
        b=polygonManage.Constructions(conn)
        r=b.delete(gid)
        return JsonResponse(r)
        #return JsonResponse({'mens':'Metodo delete para borrar'})


    

#    def get(self, request):
#        return JsonResponse({'message':'soy el método get'})'''


