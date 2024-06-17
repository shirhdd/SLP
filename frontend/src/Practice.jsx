import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DragAndDrop from "./DragAndDrop.jsx";
import Progressbar from "./Progressbar.jsx";
import ArtificialAudio from "./ArtificialAudio.jsx";
import Demo from "./Demo.jsx";
// import ArtficalUser from "./ArtficalUser.jsx";
import Wheel from "./Wheel.jsx";
import "./cssDesign/Practice.css"
import {useAuth} from "./AuthContext.jsx";

function Practice() {
    const [score, setScore] = useState(0);
    const [response, setResponse] = useState(null);
    const maxScore = 100;
    const [percentage, setPercentage] = useState(0);
    const [word, setWord] = useState(null);
    const [imageUrl, setImageUrl] = useState('');
    const { state } = useAuth(); // Get the email from AuthContext

    useEffect(() => {

        const updatePoints = async () => {
            try {
                const response = await axios.post('http://127.0.0.1:5000/update_points', {
                    email: state.email,
                    points: 10
                });
                console.log(response.data); // Handle the response as needed
            } catch (error) {
                console.error('Error updating points:', error); // Handle the error as needed
            }
        };
        const updatePercentage = () => {
            const newPercentage = (score / maxScore) * 100;
            setPercentage(newPercentage); // Update percentage state
            if(newPercentage >= 100){
                updatePoints(); // Call the function to update points

            }
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
                <Wheel setWord={setWord} setResponse={setResponse}/>
                <DragAndDrop setScore={setScore} word={word} setResponse={setResponse} />
                <Progressbar percentage={percentage} />
                {/*{imageUrl && <img src={imageUrl} alt="Word visual representation" />}*/}
                <div>{response}</div>
                {/*<ArtficalUser word={"sing"}/>*/}
            </div>
        </>
    );
}

export default Practice;
