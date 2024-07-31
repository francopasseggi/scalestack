from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from reviews.views import (
    RegisterView,
    MyTokenObtainPairView,
    AddReviewView,
    GetBookReviewsView,
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
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/reviews/", AddReviewView.as_view(), name="add_review"),
    path(
        "api/reviews/<str:isbn>/", GetBookReviewsView.as_view(), name="get_book_reviews"
    ),
]
