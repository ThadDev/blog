from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, PageNotAnInteger
from .models import Post,Like
from django.contrib.auth import authenticate, get_user_model,login,logout
from django.http import HttpResponse
from ..accounts.form import PostForm,SharePostForm,LoginForm
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.urls import reverse
from django.contrib.auth.models import User
# Create your views here.

def post_list(request):
    
    posts = Post.objects.all()
    try:
            paginator = Paginator(posts,2)
            page_number = request.GET.get("page")
            posts = paginator.get_page(page_number)
    except PageNotAnInteger:
            posts = paginator.page(1)
    except Exception as e:
            print(f"An error occurred:{e}")
            posts = paginator.page(1)
    context = {'posts':posts,"paginator":paginator,"page_obj":posts}
    return render(request,
                  "post/post_list.html",context
                  )

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    user_has_liked = False

    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(
            user=request.user,
            post=post
        ).exists()

    return render(
        request,
        "post/post_detail.html",
        {"post": post,"user_has_liked": user_has_liked,}
    )

def post_create(request):
      if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                  form.save()
                  return redirect("post:post_list")

      form = PostForm
      return render(request,"post/post_create.html",{"form":form})


def toggle_like(request, id):
    post = get_object_or_404(Post, id=id)

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    like = Like.objects.filter(
        post=post,
        session_key=session_key
    ).first()

    if like:
        like.delete()
    else:
        Like.objects.create(
            post=post,
            session_key=session_key
        )

    return redirect("post:post_detail", id=post.id)

def share_post(request,id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        form = SharePostForm(request.POST)

        if form.is_valid():
            raw_emails = form.cleaned_data["emails"]

            emails = [
                email.strip()
                for email in raw_emails.split(",")
                if email.strip()
            ]

            valid_emails = []

            for email in emails:
                try:
                    validate_email(email)
                    valid_emails.append(email)
                except ValidationError:
                    pass

            post_url = request.build_absolute_uri(
                reverse("post:post_detail", args=[post.id])
            )

            send_mail(
                subject=f"Check out this post: {post.title}",
                message=f"""
{form.cleaned_data["message"]}

Read the post here:

{post_url}
""",
                from_email=None,
                recipient_list=valid_emails,
            )

            return redirect("post:post_detail", id=post.id)

    else:
        form = SharePostForm()

    return render(request, "post/share.html", {
        "form": form,
        "post": post,
    })

def user_detail(request, id):
    user = get_object_or_404(User,id=id)
    return render(request,"post/user_detail.html",{"user":user})




def Logout(request):
     ...