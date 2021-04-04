from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    sequence = models.IntegerField()

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100) # varchar(50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, blank=False)
    image = models.ImageField(default='blank.png', blank=True)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' -' + self.get_created_date()
    
    def get_created_date(self):
        return str(self.created_at)[:19]
    def get_text(self):
        return self.text[:200] + '...'
    
class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    def serialize(self):
        return {
            "id": self.id,
            "CommentCreator": self.user.username,
            "CommentText": self.text,
        }
    
    def get_created_date(self):
        return str(self.created_at)[:19]
