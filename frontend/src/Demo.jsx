import React, { useState } from 'react';
import axios from 'axios';

function Demo({word}) {
    const [audioUrl, setAudioUrl] = useState('');

    const handleClick = () => {
        axios.get('http://localhost:5000/speech_inpainting', {
            params: { word: word },
            responseType: 'blob'
        })
            .then(response => {
                const url = window.URL.createObjectURL(new Blob([response.data], { type: 'audio/wav' }));
                setAudioUrl(url);
            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    };

    return (
        <div>
            <button onClick={handleClick}>Generate Speech</button>
            {audioUrl && <audio controls src={audioUrl} />}
        </div>
    );
}

export default Demo;
