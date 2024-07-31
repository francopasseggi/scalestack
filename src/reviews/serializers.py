from rest_framework import serializers, exceptions
from django.contrib.auth.models import User
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


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("isbn",)


class BookInformationSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    isbn = serializers.CharField()
    first_publish_year = serializers.IntegerField()
    first_sentence = serializers.CharField()


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    book = BookSerializer(read_only=True)
    isbn = serializers.CharField(write_only=True)

    class Meta:
        model = Review
        fields = ("id", "user", "book", "title", "comment", "created_at", "isbn")
        read_only_fields = ("id", "user", "book", "created_at")

    def create(self, validated_data):
        try:
            isbn = validated_data.pop("isbn")
            book = Book.objects.get(isbn=isbn)
            user = self.context["request"].user
            review = Review.objects.create(user=user, book=book, **validated_data)
            return review
        except Book.DoesNotExist:
            raise exceptions.ValidationError(
                {"isbn": f"Book with ISBN {isbn} does not exist in our database."}
            )
