// src/components/Placeholder.jsx

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './cssDesign/PlaceHolder.css';
import { useAuth } from './AuthContext.jsx';

const Placeholder = ({location}) => {
    const navigate = useNavigate();
    const { state } = useAuth();
    const { email } = state;
    const [avatar, setAvatar] = useState('');
    const locationToTitle = {
        '/': '',
        '/practice': 'Game Time',
        '/info': 'Information',
        '/profile': 'Profile',
        '/scores': '',
    };
    useEffect(() => {
        const fetchAvatar = async () => {
            try {
                const response = await fetch('http://localhost:5000/get_avatar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email }),
                });

                const data = await response.json();

                if (response.ok) {
                    setAvatar(data.avatar);
                } else {
                    console.error(data.message);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        };

        if (email) {
            fetchAvatar();
        }
    }, [email]);

    const handleNavigation = () => {
        navigate('/');
    };

    return (
        <div className="placeholder">
            <button className="left-button" onClick={handleNavigation}>
                <img
                    src={`./src/assets/house.webp`} // Replace with your asset path
                    alt="Home"
                    className={`avatar-option ${avatar ? 'selected' : ''}`}
                />
            </button>
            <div className="title">{locationToTitle[location]}</div>
            <button className="right-button" onClick={handleNavigation}>
                {avatar && (
                    <img
                        src={`./src/assets/${avatar}`}
                        alt="Avatar"
                        className={`avatar-option ${avatar ? 'selected' : ''}`}
                    />
                )}
            </button>
        </div>
    );
};

export default Placeholder;
