from django.urls import path

from . import views

app_name = 'money_data'
urlpatterns = [
    path('', views.index, name='index'),
    path('moneylogs/', views.money, name='moneylogs'),
    path('edit_log/<int:log_id>/', views.edit_log, name="edit_log"),
    path('delete/<int:log_id>/', views.delete_log, name="delete_log"),
]