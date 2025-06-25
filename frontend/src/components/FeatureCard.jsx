import React from 'react';
import './FeatureCard.css';

const FeatureCard = ({ icon, title, text }) => {
    return (
        <div className="feature-card">
            <div className="feature-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
    );
};

export default FeatureCard;
