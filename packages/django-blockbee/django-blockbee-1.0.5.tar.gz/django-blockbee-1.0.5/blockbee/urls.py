from django.urls import include, path
from blockbee import views

app_name = 'blockbee'

urlpatterns = [
    path('callback/', views.callback, name='callback'),
    path('status/', views.status, name='status'),
]
