from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
from .models import Post,Like
from .form import PostForm
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

@login_required
def toggle_like(request, id):
    post = get_object_or_404(Post, id=id)

    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    if like:
        like.delete()
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect("post:post_detail", id=post.id)