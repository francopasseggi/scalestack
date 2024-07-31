from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.views import (
    RegisterView,
    AddReviewView,
    GetBookReviewsView,
    GetBookInformationView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/reviews/", AddReviewView.as_view(), name="add_review"),
    path(
        "api/reviews/<str:isbn>/", GetBookReviewsView.as_view(), name="get_book_reviews"
    ),
    path("api/book-info/", GetBookInformationView.as_view(), name="get_book_info"),
]
