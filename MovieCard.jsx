import React from 'react';

const MovieCard = ({ movie }) => (
    <div className="movie-card">
        <h3>{movie.title}</h3>
        <p>{movie.description}</p>
    </div>
);

export default MovieCard;
