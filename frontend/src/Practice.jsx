import React, { useState, useEffect } from 'react';
import axios from 'axios';
import RandomWord from "./RandomWord.jsx";
import DragAndDrop from "./DragAndDrop.jsx";
import Progressbar from "./Progressbar.jsx";
import ArtificialAudio from "./ArtificialAudio.jsx";
import Demo from "./Demo.jsx";
// import ArtficalUser from "./ArtficalUser.jsx";
import Wheel from "./Wheel.jsx";
import "./cssDesign/Practice.css"

function Practice() {
    const [score, setScore] = useState(0);
    const [response, setResponse] = useState(null);
    const maxScore = 100;
    const [percentage, setPercentage] = useState(0);
    const [word, setWord] = useState(null);
    const [imageUrl, setImageUrl] = useState('');

    useEffect(() => {
        const updatePercentage = () => {
            const newPercentage = (score / maxScore) * 100;
            setPercentage(newPercentage); // Update percentage state
        };

        updatePercentage();
    }, [score]);

    useEffect(() => {
        if (word) {
            // fetchImage(word);
            console.log("should fetch image")
        }
    }, [word]);

    const fetchImage = async (word) => {
        try {
            const response = await axios.get(`http://localhost:5000/get_image?name=${word}`);
            setImageUrl(response.config.url); // Assuming your backend sends the direct URL or handles redirection to the image
        } catch (error) {
            console.error('Error fetching image:', error);
            setImageUrl(''); // Reset image URL on error
        }
    };

    return (
        <>
            <div>
                <ArtificialAudio word={word}/>
                {word && <div>Word: {word}</div>}
                <Wheel setWord={setWord}/>
                <DragAndDrop setScore={setScore} word={word} setResponse={setResponse} />
                <Progressbar percentage={percentage} />
                {/*{imageUrl && <img src={imageUrl} alt="Word visual representation" />}*/}
                {response && <div>{response.message}</div>}
                {response && <div>{response.phonemes}</div>}
                {/*<ArtficalUser word={"sing"}/>*/}
            </div>
        </>
    );
}

export default Practice;
