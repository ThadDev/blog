from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=255)
    slug = models.SlugField()
    
    def get_absolute_url(self):
        return reverse("post:post_detail", args=[self.id])
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts",null=True,blank=True
    )

    publish = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(default="")

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    session_key = models.CharField(
    max_length=40,
    null=True,
    blank=True
)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "session_key"],
                name="unique_session_post_like"
            )
        ]

    def __str__(self):
        return f"Like on {self.post.title}"