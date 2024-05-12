import React, { useState, useEffect } from 'react';
import { Wheel as RouletteWheel } from 'react-custom-roulette';
import './cssDesign/Wheel.css';
// Import your audio file if using Create React App and static file handling
import spinSound from './assets/sound/spinner-sound.mp3'; // Adjust the path as necessary

function Wheel({ setWord }) {
    const [words, setWords] = useState(["example - 1", "example - 2", "example - 3", "example - 4"]);
    const [mustStartSpinning, setMustStartSpinning] = useState(false);
    const [prizeNumber, setPrizeNumber] = useState(0);
    const [selectedWord, setSelectedWord] = useState('');
    const [shine, setShine] = useState(false);
    const [isInitialLoad, setIsInitialLoad] = useState(true);
    const [spinAudio, setSpinAudio] = useState(new Audio(spinSound)); // Create audio object

    const fetchWords = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/random_words');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setWords(data.words);
            if (!isInitialLoad) {
                continueSpin(data.words);
            }
        } catch (error) {
            console.error('There was a problem retrieving words:', error);
        }
    };

    useEffect(() => {
        fetchWords();
        setIsInitialLoad(false);
    }, []);

    const handleSpinClick = () => {
        setIsInitialLoad(false);
        fetchWords();
        spinAudio.play(); // Play the spin sound when starting the spin
    };

    const continueSpin = (freshWords) => {
        const newPrizeNumber = Math.floor(Math.random() * freshWords.length);
        setPrizeNumber(newPrizeNumber);
        setMustStartSpinning(true);
    };

    const handleSpinStop = () => {
        setMustStartSpinning(false);
        const word = words[prizeNumber];
        setSelectedWord(word);
        setWord(word);
        setShine(true);
        setTimeout(() => setShine(false), 5000); // Ensure comment matches the timeout
        spinAudio.pause(); // Optionally pause or stop the sound when spinning stops
        spinAudio.currentTime = 0; // Reset audio position
    };

    return (
        <div>
            <RouletteWheel
                mustStartSpinning={mustStartSpinning}
                prizeNumber={prizeNumber}
                data={words.map((word, index) => ({
                    option: word,
                    style: { backgroundColor: `hsl(${index * (360 / words.length)}, 70%, 50%)`, textColor: '#fff' }
                }))}
                backgroundColors={words.map((_, index) => `hsl(${index * (360 / words.length)}, 70%, 50%)`)}
                textColors={['#ffffff']}
                textStyle={{ fontFamily: 'Helvetica, Arial', fontSize: '45px' }}
                onStopSpinning={handleSpinStop}
            />
            <button onClick={handleSpinClick}>Spin</button>
            <div style={{ marginTop: '20px', fontSize: '24px' }} className={shine ? 'shine-effect' : ''}>
                {selectedWord ? `You got: ${selectedWord}` : 'Spin the wheel to see what you get!'}
            </div>
        </div>
    );
}

export default Wheel;
