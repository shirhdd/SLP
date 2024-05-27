import React from 'react';
import { useNavigate } from 'react-router-dom';
import characterImage from './assets/button/Donald_Duck_Iconic.webp';
import './cssDesign/MainMenu.css';
import PointsDisplay from "./PointsDisplay.jsx";
function MainMenu() {
    const navigate = useNavigate();




    return (
        <div className="menu-container">

            <img src={characterImage} alt="Character" className="character-image" />
            <PointsDisplay email={"email@email.com"}/>
            <div className="button-container">
                <button className="menu-button" onClick={() => navigate('/info')}>Info</button>
                <button className="menu-button" onClick={() => navigate('/practice')}>Start Practice</button>
                <button className="menu-button" onClick={() => navigate('/scores')}>Scores</button>
            </div>
        </div>
    );
}

export default MainMenu;
