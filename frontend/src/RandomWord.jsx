import React, { useState } from 'react';

function RandomWord() {
    const [word, setWord] = useState('');

    const fetchWord = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/random_word');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setWord(data.word);
        } catch (error) {
            console.error('There was a problem retrieving the word:', error);
        }
    };

    return (
        <div>
            <button onClick={fetchWord}>Get Random Word</button>
            {word && <p>{word}</p>}
        </div>
    );
}

export default RandomWord;
