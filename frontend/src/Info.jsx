import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './cssDesign/Info.css';  // Import the CSS file

const Info = () => {
    const [info, setInfo] = useState({});
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchInfo = async () => {
            try {
                const response = await axios.get('http://localhost:5000/info');
                setInfo(response.data);
            } catch (error) {
                console.error('Error fetching info', error);
                setError('Failed to load project information.');
            }
        };

        fetchInfo();
    }, []);

    return (
        <div className="info-container">
            <h1 className="info-title">{info.title}</h1>
            <p className="description">{info.description}</p>
            <h2 className="developers-title">Developers</h2>
            {info.developers ? (
                <ul className="developers-list">
                    {info.developers.map((developer, index) => (
                        <li key={index} className="developer-name">{developer.name}</li>
                    ))}
                </ul>
            ) : (
                <p className="error">{error}</p>
            )}
        </div>
    );
};

export default Info;
