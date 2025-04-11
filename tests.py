from django.test import TestCase
from django.contrib.auth.models import User
from .models import Genre, Movie, Review

class MovieModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.genre = Genre.objects.create(name='Драма')
        cls.movie = Movie.objects.create(
            title='Тестовый фильм',
            description='Тестовое описание',
            release_year=2020
        )
        cls.movie.genres.add(cls.genre)

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, 'Тестовый фильм')
        self.assertEqual(self.movie.genres.count(), 1)
        self.assertEqual(self.movie.rating, 0.0)

    def test_review_creation(self):
        review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            text='Хороший фильм',
            rating=8
        )
        self.assertEqual(review.rating, 8)
        self.assertEqual(self.movie.reviews.count(), 1)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.rating, 8.0)

    def test_unique_review_constraint(self):
        Review.objects.create(
            movie=self.movie,
            user=self.user,
            text='Первый отзыв',
            rating=8
        )
        with self.assertRaises(Exception):
            Review.objects.create(
                movie=self.movie,
                user=self.user,
                text='Второй отзыв',
                rating=9
            )