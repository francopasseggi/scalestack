from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from drf_spectacular.types import OpenApiTypes
from .models import Review
from .serializers import UserSerializer, MyTokenObtainPairSerializer, ReviewSerializer
from .paginators import StandardResultsSetPagination


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
        responses={
            201: ReviewSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class GetBookReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @extend_schema(
        summary="Get reviews for a book",
        description="Retrieve all reviews for a book by its ISBN. Requires authentication. Results are paginated.",
        parameters=[
            OpenApiParameter(
                name="page", description="Page number", required=False, type=int
            ),
            OpenApiParameter(
                name="page_size",
                description="Number of results per page",
                required=False,
                type=int,
            ),
        ],
        responses={
            200: inline_serializer(
                name="PaginatedReviewResponse",
                fields={
                    "count": OpenApiTypes.INT,
                    "next": OpenApiTypes.URI,
                    "previous": OpenApiTypes.URI,
                    "results": ReviewSerializer(many=True),
                },
            )
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        isbn = self.kwargs["isbn"]
        return Review.objects.filter(book__isbn=isbn)
