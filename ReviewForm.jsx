import React, { useState } from 'react';
import axios from 'axios';
import './ReviewForm.css';

const ReviewForm = ({ movieId, onReviewAdded }) => {
  const [text, setText] = useState('');
  const [rating, setRating] = useState(5);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) {
      setError('Отзыв не может быть пустым');
      return;
    }

    try {
      const response = await axios.post('/api/reviews', {
        movieId,
        text,
        rating: Number(rating) // Убедимся, что rating это число
      });
      onReviewAdded(response.data.review);
      setText('');
      setRating(5);
      setError('');
    } catch (err) {
      setError(err.response?.data?.message || 'Ошибка при отправке отзыва');
    }
  };

  return (
    <form className="review-form" onSubmit={handleSubmit}>
      <h3>Оставить отзыв</h3>
      {error && <div className="error-message">{error}</div>}
      <div className="form-group">
        <label>Оценка:</label>
        <select
          value={rating}
          onChange={(e) => setRating(e.target.value)}
          className="rating-select"
        >
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
            <option key={num} value={num}>{num}</option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Ваш отзыв..."
          rows="5"
          className="review-textarea"
        />
      </div>
      <button type="submit" className="submit-button">Отправить</button>
    </form>
  );
};

export default ReviewForm;