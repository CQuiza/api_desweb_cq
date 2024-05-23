'''
Created on 21 mar. 2024

@author: vagrant
'''
from django.urls import path
from app_cq import views, viewsUsers

urlpatterns = [
    path('not_logged_in/',viewsUsers.notLoggedIn),
    path('app_login/',viewsUsers.AppLogin.as_view()),
    path('app_logout/',viewsUsers.AppLogout.as_view()),
    path('hello_world/',views.HelloWord.as_view()),
    path('hola_clase/',views.HolaClase.as_view()),
    path('construction_select_by_gid/',views.ConstructionSelectByGid.as_view()),
    path('construction_insert/',views.ConstructionInsert.as_view()),
    path('construction_update/',views.ConstructionUpdate.as_view()),
    path('construction_delete/',views.ConstructionDelete.as_view()),
    path('well_select_by_gid/',views.WellSelectByGid.as_view()),
    path('well_insert/',views.WellInsert.as_view()),
    path('well_update/',views.WellUpdate.as_view()),
    path('well_delete/',views.WellDelete.as_view()),
    path('pipe_select_by_gid/',views.PipeSelectByGid.as_view()),
    path('pipe_insert/',views.PipeInsert.as_view()),
    path('pipe_update/',views.PipeUpdate.as_view()),
    path('pipe_delete/',views.PipeDelete.as_view()),
    path('h/',views.HelloWord.as_view()),
    #path('construction/',views.Construction.as_view()),
    #path('construction_select_by_gid2/<date>/',views.ConstructionSelectByGid2.as_view()),
    #path('construction_select_by_area/',views.ConstructionSelectByArea.as_view()),

]
