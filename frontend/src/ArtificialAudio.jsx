import React, { useState } from 'react';

function ArtificialAudio({ word }) {
    const [audio, setAudio] = useState(null);

    const handleAudio = async () => {
        if (audio) {
            audio.pause();  // Pause the current audio if it's playing
        }

        try {
            const response = await fetch(`http://localhost:5000/get_correct_pronunciation?word=${word}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const newAudio = new Audio(url);
            setAudio(newAudio);
            newAudio.play();
        } catch (error) {
            console.error('Error fetching and playing audio:', error);
        }
    };

    return (
        <div>
            <button onClick={handleAudio}>Play Pronunciation</button>
        </div>
    );
}

export default ArtificialAudio;
