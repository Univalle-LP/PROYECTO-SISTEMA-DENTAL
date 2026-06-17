from django.urls import path
from . import views

urlpatterns = [

    path('ia/', views.ia_caries, name='ia_caries'),

]