import json
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from reviews.models import Book, Review
from django.urls import reverse

from unittest.mock import patch, Mock


@pytest.fixture(scope="session")
def test_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = User.objects.create_user(username="testuser", password="testpass123")
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def create_book():
    def _create_book(isbn="1234567890123"):
        return Book.objects.create(isbn=isbn)

    return _create_book


@pytest.mark.django_db
class TestUserAPI:
    def test_user_registration(self, api_client):
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="newuser").exists()

    def test_user_login(self, api_client, test_user):
        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "testpass123"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_user_login_fail(self, api_client):
        url = reverse("token_obtain_pair")
        data = {"username": "wronguser", "password": "wrongpass"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestBookReviewAPI:
    @pytest.fixture
    def review_data(self, create_book):
        book = create_book()
        return {
            "isbn": book.isbn,
            "title": "Great Book",
            "comment": "I really enjoyed reading this book.",
        }

    def test_add_review_authenticated(self, authenticated_client, review_data):
        url = reverse("add_review")
        response = authenticated_client.post(url, review_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Review.objects.filter(book__isbn=review_data["isbn"]).exists()

    def test_add_review_unauthenticated(self, api_client, review_data):
        url = reverse("add_review")
        response = api_client.post(url, review_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize("num_reviews,expected_count", [(0, 0), (2, 2)])
    def test_get_reviews(
        self, authenticated_client, test_user, create_book, num_reviews, expected_count
    ):
        book = create_book()

        for i in range(num_reviews):
            Review.objects.create(
                book=book,
                user=test_user,
                title=f"Review {i+1}",
                comment=f"Comment {i+1}",
            )

        url = reverse("get_book_reviews", kwargs={"isbn": book.isbn})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == expected_count

    def test_get_reviews_unauthenticated(self, api_client, create_book):
        book = create_book()
        url = reverse("get_book_reviews", kwargs={"isbn": book.isbn})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestBookInformationAPI:
    @pytest.fixture
    def mock_lambda_client(self):
        with patch("boto3.client") as mock_client:
            yield mock_client

    def test_get_book_information_success(
        self, authenticated_client, mock_lambda_client
    ):
        mock_lambda_response = {
            "StatusCode": 200,
            "Payload": Mock(
                read=Mock(
                    return_value=json.dumps(
                        {
                            "statusCode": 200,
                            "body": {
                                "title": "Test Book",
                                "author": "Test Author",
                                "publish_date": 2020,
                                "description": "Unknown",
                            },
                        }
                    ).encode("utf-8")
                )
            ),
        }
        mock_lambda_client.return_value.invoke.return_value = mock_lambda_response

        url = reverse("get_book_info")
        response = authenticated_client.get(url, {"isbn": "1234567890"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "title": "Test Book",
            "author": "Test Author",
            "publish_date": 2020,
            "description": "Unknown",
        }

    def test_get_book_information_not_found(
        self, authenticated_client, mock_lambda_client
    ):
        mock_lambda_response = {
            "StatusCode": 200,
            "Payload": Mock(
                read=Mock(
                    return_value=json.dumps(
                        {"statusCode": 404, "body": {"error": "Book not found"}}
                    ).encode("utf-8")
                )
            ),
        }
        mock_lambda_client.return_value.invoke.return_value = mock_lambda_response

        url = reverse("get_book_info")
        response = authenticated_client.get(url, {"isbn": "0000000000"})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {"error": "Book not found"}

    def test_get_book_information_no_isbn(self, authenticated_client):
        url = reverse("get_book_info")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_get_book_information_lambda_error(
        self, authenticated_client, mock_lambda_client
    ):
        mock_lambda_client.return_value.invoke.side_effect = Exception(
            "Lambda invocation failed"
        )

        url = reverse("get_book_info")
        response = authenticated_client.get(url, {"isbn": "1234567890"})

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "error" in response.data
