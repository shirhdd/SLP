import React, { useState, useEffect } from 'react';
// import CountUp from 'react-countup';
import axios from 'axios';
import './cssDesign/PointsDisplay.css'; // Import the CSS file

const PointsDisplay = ({ email }) => {
    const [points, setPoints] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPoints = async () => {
            try {
                const response = await axios.get('http://localhost:5000/get_points', { params: { email } });
                setPoints(response.data.points);
            } catch (err) {
                setError(err.response ? err.response.data.error : 'Error fetching points');
            } finally {
                setLoading(false);
            }
        };

        fetchPoints();
    }, [email]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="points-display">
            <h1>Points</h1>
            {/*<CountUp className="count-up" start={0} end={points} duration={4.5} />*/}
        </div>
    );
};

export default PointsDisplay;
