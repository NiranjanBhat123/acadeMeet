from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path("login/",views.loginPage,name="login"),
    path("register/",views.RegisterUser,name="register"),
    path("logout/",views.logoutUser,name="logout"),
    path("",views.home,name="home"),
    path("room/<str:pk>",views.rooms,name="room"),
    path("profile/<str:pk>",views.userProfile,name="user_profile"),
    path("create_room/",views.createRoom,name="create_room"),
    path("update_room/<str:pk>",views.updateRoom,name="update_room"),
    path("delete_room/<str:pk>",views.deleteRoom,name="delete_room"),
    path("delete_message/<str:pk>",views.deleteMessage,name="delete_message"),
    path("update-user/",views.updateUser,name="update-user"),
    path("topics/",views.topicsPage,name="topics"),
    path("activity/",views.activitiyPage,name="activity"),
]
