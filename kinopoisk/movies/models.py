from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название жанра")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    release_year = models.IntegerField(
        verbose_name="Год выпуска",
        validators=[MinValueValidator(1895), MaxValueValidator(2025)]
    )
    genres = models.ManyToManyField(Genre, related_name='movies', verbose_name="Жанры")
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="Рейтинг",
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = round(sum([r.rating for r in reviews]) / reviews.count(), 1)
            self.save(update_fields=['rating', 'updated_at'])

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        indexes = [
            models.Index(fields=['release_year']),
            models.Index(fields=['rating']),
        ]
        ordering = ['-rating', 'title']

    def __str__(self):
        return f"{self.title} ({self.release_year})"

class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Фильм"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Пользователь"
    )
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=['movie', 'user'],
                name='unique_user_movie_review'
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}/10)"

    def clean(self):
        if self.rating < 1 or self.rating > 10:
            raise ValidationError("Оценка должна быть от 1 до 10")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.movie.update_rating()