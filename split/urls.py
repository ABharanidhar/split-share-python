from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('create_group/', views.create_group, name='create_group_individual'),

    path('create_groups/', views.create_groups, name='create_group_family'),

    path('delete/<int:group_id>/', views.delete_group, name='delete_group'),

    path('open/<int:group_id>/', views.open_group, name='open_group'),

    path('ajax_share_data_insert/', views.ajax_share_data_insert, name='ajax call'),

    path('<int:group_id>/edit/', views.edit, name='edit_group'),

    path('calculate/<int:group_id>/', views.calculations, name='calculations'),

    path('error/', views.error_view, name='error_view'),

]