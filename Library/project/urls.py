from django.urls import path,include
from .import views
from django.contrib.auth.views import LoginView
from .views import CustomLogoutView


urlpatterns = [
    path('home',views.home_view,name='home'),
    path('adminclick',views.adminclick_view),
    path('studentclick',views.studentclick_view),
    path('adminsignup',views.adminsignup_view),
    path('studentsignup',views.studentsignup_view),
    path('adminlogin',LoginView.as_view(template_name='adminlogin.html')),
    path('studentlogin',LoginView.as_view(template_name='studentlogin.html')),
    path('afterlogin',views.afterlogin_view,name='afterlogin'),
    path('addbook',views.addbook_view),
    path('logout/',CustomLogoutView.as_view(),name='logout'),
    path('viewbook',views.viewbook_view),
    path('issuebook',views.issuebook_view),
    path('viewissuedbook',views.viewissuedbook_view),
    path('viewstudent',views.viewstudent_view),
    path('viewissuedbookbystudent',views.viewissuedbookbystudent_view),
    path('aboutus',views.aboutus_view),
    path('contactus',views.contactus_view),

]
