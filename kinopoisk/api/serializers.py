from rest_framework import serializers
from movies.models import Movie, Review
from datetime import date


class MovieSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'rating', 'created_at']
        read_only_fields = ('rating', 'created_at')

    def get_rating(self, obj):
        return obj.average_rating()

    def validate_release_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Дата релиза не может быть в будущем.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'content', 'rating', 'created_at']
        read_only_fields = ('created_at', 'user')

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value