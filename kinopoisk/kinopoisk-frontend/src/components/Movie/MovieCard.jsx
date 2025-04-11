import React from 'react';
import { Link } from 'react-router-dom';
import './MovieCard.css';

const MovieCard = ({ movie }) => {
  return (
    <div className="movie-card">
      <Link to={`/movie/${movie.id}`}>
        <img
          src={movie.poster?.url || '/placeholder.jpg'}
          alt={movie.name}
          className="movie-poster" // Исправлено с poster на movie-poster
        />
        <div className="movie-info"> {/* Исправлено с info на movie-info */}
          <h3 className="movie-title">{movie.name}</h3> {/* Добавлен класс */}
          <div className="movie-meta"> {/* Обернуто в div с классом */}
            <span>{movie.year}</span>
            {movie.rating?.kp && <span>★ {movie.rating.kp.toFixed(1)}</span>}
          </div>
        </div>
      </Link>
    </div>
  );
};

export default MovieCard;