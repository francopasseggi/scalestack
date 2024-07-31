from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Book, Review
from .serializers import UserSerializer, MyTokenObtainPairSerializer, ReviewSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    @extend_schema(
        summary="Register a new user",
        description="Create a new user account with username, email, and password.",
        responses={201: UserSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @extend_schema(
        summary="Obtain JWT token",
        description="Authenticate user and return JWT token pair.",
        responses={200: MyTokenObtainPairSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AddReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Add a new book review",
        description="Create a new review for a book. Requires authentication.",
        request=ReviewSerializer,
        responses={201: ReviewSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class GetBookReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get reviews for a book",
        description="Retrieve all reviews for a book by its ISBN. Requires authentication.",
        responses={200: ReviewSerializer(many=True), 404: None},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        isbn = self.kwargs["isbn"]
        return Review.objects.filter(book__isbn=isbn)
