import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './cssDesign/Scores.css';  // Import the CSS file

const Scores = () => {
    const [users, setUsers] = useState([]);  // Initialize as an empty array
    const [error, setError] = useState(null); // For error handling

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await axios.get('http://localhost:5000/get_users');
                console.log('API response:', response.data);  // Debug: Log the response
                if (Array.isArray(response.data)) {
                    setUsers(response.data);
                } else {
                    throw new Error('Data is not an array');
                }
            } catch (error) {
                console.error('Error fetching users', error);
                setError('Failed to load scores.');
            }
        };

        fetchUsers();
    }, []);

    return (
        <div className="scores-container">
            <h1 className="title">Scores</h1>
            {error ? (
                <p className="error">{error}</p>
            ) : (
                <table className="score-table">
                    <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Username</th>
                        <th>Points</th>
                    </tr>
                    </thead>
                    <tbody>
                    {users
                        .slice() // create a shallow copy of the users array to avoid mutating the original array
                        .sort((a, b) => b.points - a.points) // sort users by points in descending order
                        .map((user, index) => (
                            <tr key={index}>
                                <td>{index + 1}</td>
                                {/* Rank based on index */}
                                <td>{user.username}</td>
                                <td>{user.points}</td>
                            </tr>
                        ))}
                    </tbody>

                </table>
            )}
        </div>
    );
};

export default Scores;
