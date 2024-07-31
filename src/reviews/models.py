from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return f"{self.title} (ISBN: {self.isbn})"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.book.title} by {self.user.username}"
