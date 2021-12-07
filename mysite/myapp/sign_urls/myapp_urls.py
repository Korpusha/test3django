from django.urls import path
from myapp.views import MyLogin, MyRegister, MyLogOut


urlpatterns = [
    path('login/', MyLogin.as_view(), name='login'),
    path('register/', MyRegister.as_view(), name='register'),
    path('logout/', MyLogOut.as_view(), name='logout'),
]
