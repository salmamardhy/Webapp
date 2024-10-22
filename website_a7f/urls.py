from django.contrib import admin
from django.urls import path
from website_a7f import views  
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'), 
    path('member', views.index, name='index'),  
    path('regis',views.regis, name='regis'),   
    path('edit/<str:memberid>/', views.edit, name='edit'),
    path('update/<str:memberid>/', views.update, name='update'),
    path('delete/<str:memberid>/',views.destroy,name="destroy")
]