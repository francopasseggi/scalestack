from django.contrib.auth.models import User
from rest_framework import generics, permissions
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    inline_serializer,
    OpenApiResponse,
)

from drf_spectacular.types import OpenApiTypes
from .models import Review
from .serializers import (
    BookInformationSerializer,
    UserSerializer,
    ReviewSerializer,
)
from .paginators import StandardResultsSetPagination
from .services import get_book_info
from rest_framework import status
from rest_framework.response import Response
from botocore.exceptions import ClientError


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AddReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class GetBookReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @extend_schema(
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


class GetBookInformationView(generics.RetrieveAPIView):
    serializer_class = BookInformationSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="isbn", description="ISBN of the book", required=True, type=str
            ),
        ],
        responses={
            200: BookInformationSerializer,
            400: OpenApiResponse(description="ISBN is required"),
            404: OpenApiResponse(description="Book not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request, *args, **kwargs):
        isbn = request.query_params.get("isbn")
        if not isbn:
            return Response(
                {"error": "ISBN is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payload = get_book_info(isbn)

            if "statusCode" in payload and payload["statusCode"] != 200:
                return Response(payload["body"], status=payload["statusCode"])

            return Response(payload["body"], status=status.HTTP_200_OK)

        except ClientError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception:
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
