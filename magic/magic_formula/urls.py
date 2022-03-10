from django.urls import path

from .views.company import index,refreshcompanies

urlpatterns = [
  path('',index,name='index'),
  path('refreshcompanies/',refreshcompanies,name='refreshcompanies'),
]