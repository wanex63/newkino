import React from 'react';
import './ReviewList.css'; // Добавлен импорт стилей

const ReviewList = ({ reviews }) => {
  return (
    <div className="review-list">
      {reviews.length === 0 ? (
        <p className="no-reviews">Пока нет отзывов. Будьте первым!</p>
      ) : (
        reviews.map(review => (
          <div key={review._id} className="review-item">
            <div className="review-header">
              <span className="review-author">{review.author.username}</span>
              <span className="review-rating">★ {review.rating}</span>
              <span className="review-date">
                {new Date(review.createdAt).toLocaleDateString()}
              </span>
            </div>
            <p className="review-text">{review.text}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default ReviewList;