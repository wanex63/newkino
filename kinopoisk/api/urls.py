from django.urls import path
from .views import (
    LoginView, LogoutView,
    MovieListCreateView, MovieDetailView,
    ReviewCreateView, MovieReviewsListView
)
from api.views import LoginView, LogoutView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='api_login'),
    path('auth/logout/', LogoutView.as_view(), name='api_logout'),
    path('movies/', MovieListCreateView.as_view(), name='api_movies'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='api_movie_detail'),
    path('movies/<int:movie_id>/reviews/', MovieReviewsListView.as_view(), name='api_movie_reviews'),
    path('reviews/', ReviewCreateView.as_view(), name='api_create_review'),
]