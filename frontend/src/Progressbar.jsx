import React, { useEffect, useRef } from 'react';
import { ProgressBar } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Fireworks } from '@fireworks-js/react';

function Progressbar({ percentage }) {
    const fireworksRef = useRef(null);

    // Define the emojis for specific percentage milestones
    const getEmoji = () => {
        if (percentage >= 100) {
            return '🏆';
        } else if (percentage >= 90) {
            return '🥇';
        } else if (percentage >= 80) {
            return '🥈';
        } else if (percentage >= 70) {
            return '🥉';
        } else if (percentage >= 60) {
            return '🤩';
        } else if (percentage >= 40) {
            return '😄';
        } else if (percentage >= 30) {
            return '😃';
        } else if (percentage >= 20) {
            return '🙂';
        } else if (percentage >= 10) {
            return '🙂'; // You might want to adjust these to have unique emojis
        } else if (percentage >= 0) {
            return '🏁';
        }
        return '';  // No emoji for less than 10%
    };

    useEffect(() => {
        if (percentage >= 100) {
            if (fireworksRef.current) {
                fireworksRef.current.start();
            }

            const timer = setTimeout(() => {
                if (fireworksRef.current) {
                    fireworksRef.current.stop();
                }
            }, 3000);

            return () => clearTimeout(timer);
        }
    }, [percentage]);

    return (
        <div style={{ width: '100%', margin: '20px auto', position: 'relative' }}>
            <ProgressBar
                animated
                now={percentage}
                label={`${percentage.toFixed(0)}%`}
                style={{
                    width: '400px',
                    height: '30px',
                    fontSize: '15px',
                    backgroundColor: '#f8f9fa',
                    borderColor: '#0081ff'
                }}
            />
            <div style={{ position: 'absolute', top: '0', right: '10px', fontSize: '20px' }}>
                {getEmoji()}
            </div>
            {percentage >= 100 && (
                <Fireworks
                    ref={fireworksRef}
                    options={{ speed: 3 }}
                    style={{
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        position: 'fixed',
                        background: 'transparent',
                        pointerEvents: 'none' // Allow mouse events to pass through
                    }}
                />
            )}
        </div>
    );
}

export default Progressbar;
