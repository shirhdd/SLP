import React from 'react';
import { useNavigate } from 'react-router-dom';
import characterImage from './assets/button/Donald_Duck_Iconic.webp';
import './cssDesign/MainMenu.css';
import PointsDisplay from "./PointsDisplay.jsx";
import { useAuth } from './AuthContext'; // Import the useAuth hook

function MainMenu() {
    const navigate = useNavigate();
    const { state } = useAuth(); // Use the useAuth hook to get the state from the context
    const { email } = state; // Extract the email from the state



    return (
        <div className="menu-container">

            <img src={characterImage} alt="Character" className="character-image" />
            <PointsDisplay email={email}/>
            <div className="button-container">
                <button className="menu-button" onClick={() => navigate('/info')}>Info</button>
                <button className="menu-button" onClick={() => navigate('/practice')}>Start Practice</button>
                <button className="menu-button" onClick={() => navigate('/scores')}>Scores</button>
            </div>
        </div>
    );
}

export default MainMenu;
