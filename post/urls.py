from django.urls import path
from .views import post_list, post_detail, post_create,toggle_like,share_post

app_name = "post"

urlpatterns = [
    path("", post_list, name="post_list"),
    path("<int:id>/", post_detail, name="post_detail"),
    path("create", post_create, name="post_create"),
    path("<int:id>/like/", toggle_like, name="toggle_like"),
    path("<int:id>/share/", share_post, name="share_post"),
]

