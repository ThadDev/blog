from django.urls import path
from .views import login,user_detail,send_reset_code

app_name = "accounts"

urlpatterns = [
       path("login/",login,name="login"),
        path("user/<int:id>/",user_detail, name="user_detail"),
        path("send_reset_code/", send_reset_code, name="send_reset_code"),
]