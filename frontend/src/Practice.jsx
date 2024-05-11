import React, { useState, useEffect } from 'react';
import RandomWord from "./RandomWord.jsx";
import DragAndDrop from "./DragAndDrop.jsx";
import Progressbar from "./Progressbar.jsx";

function Practice() {
    const [score, setScore] = useState(0);
    const maxScore = 100;
    const [percentage, setPercentage] = useState(0);

    useEffect(() => {
        const updatePercentage = () => {
            const newPercentage = (score / maxScore) * 100;
            setPercentage(newPercentage); // Update percentage state
        };

        updatePercentage();
    }, [score]);

    return (
        <div>
            <h1>Practice Area</h1>
            <RandomWord />
            <DragAndDrop score={score} setScore={setScore} />
            <Progressbar percentage={percentage} />
        </div>
    );
}

export default Practice;
