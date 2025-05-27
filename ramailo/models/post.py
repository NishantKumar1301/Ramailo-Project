from django.db import models
from ramailo.models.base import BaseModel
from ramailo.models.user import User

class Category(BaseModel):
    CHOICES = [
        ('politics', 'Politics'),
        ('sports', 'Sports'),
        ('tech', 'Tech'),
        ('others', 'Others'),
    ]
    name = models.CharField(max_length=30, choices=CHOICES)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Post(BaseModel):
    title = models.CharField(max_length=200)
    content =  models.TextField()
    # created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

class Comment(BaseModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.user.name} commented on {self.post.title}"

class PostImage(BaseModel):
    post = models.OneToOneField(Post,on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f"Image of {self.post.title}"


