from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Review, Book


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("isbn",)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    book = BookSerializer(read_only=True)
    isbn = serializers.CharField(write_only=True)

    class Meta:
        model = Review
        fields = ("id", "user", "book", "title", "comment", "created_at", "isbn")
        read_only_fields = ("id", "user", "book", "created_at")

    def create(self, validated_data):
        isbn = validated_data.pop("isbn")
        book, _ = Book.objects.get_or_create(isbn=isbn)
        user = self.context["request"].user
        review = Review.objects.create(user=user, book=book, **validated_data)
        return review
