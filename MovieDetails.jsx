import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './MovieDetail.css';
import LoadingSpinner from '../Common/LoadingSpinner'; // Добавлен импорт спиннера

const MovieDetail = () => {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const response = await axios.get(`https://api.kinopoisk.dev/v1.3/movie/${id}`, {
          headers: {
            'X-API-KEY': process.env.REACT_APP_API_KEY
          }
        });
        setMovie(response.data);
      } catch (error) {
        console.error('Error fetching movie:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMovie();
  }, [id]);

  if (loading) return <LoadingSpinner />; // Использование компонента спиннера
  if (!movie) return <div className="error">Фильм не найден</div>;

  return (
    <div className="movie-detail-container"> {/* Исправлено название класса */}
      <div className="movie-detail-header"> {/* Исправлено название класса */}
        <img
          src={movie.poster?.url || '/placeholder.jpg'}
          alt={movie.name}
          className="movie-poster"
        />
        <div className="movie-info">
          <h1 className="movie-detail-title">{movie.name} ({movie.year})</h1>
          <div className="rating">★ {movie.rating?.kp?.toFixed(1) || 'Н/Д'}</div>
          <p className="movie-detail-description">{movie.description || 'Описание отсутствует'}</p>
          <div className="movie-detail-genres">
            {movie.genres?.map(g => g.name).join(', ') || '-'}
          </div>
        </div>
      </div>

      <div className="movie-content">
        <section>
          <h2>О фильме</h2>
          <div className="details">
            <p><strong>Страна:</strong> {movie.countries?.map(c => c.name).join(', ') || '-'}</p>
            <p><strong>Длительность:</strong> {movie.movieLength || '?'} мин</p>
          </div>
        </section>
      </div>
    </div>
  );
};

export default MovieDetail;