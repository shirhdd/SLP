import React from 'react';
import { useNavigate } from 'react-router-dom';
import characterImage from './assets/button/Donald_Duck_Iconic.webp';
import './cssDesign/MainMenu.css';

function MainMenu() {
    const navigate = useNavigate();

    return (
        <div className="menu-container">
            <img src={characterImage} alt="Character" className="character-image" />
            <div className="button-container">
                <button className="menu-button">Button 1</button>
                <button className="menu-button" onClick={() => navigate('/practice')}>Start Practice</button>
                <button className="menu-button">Button 3</button>
            </div>
        </div>
    );
}

export default MainMenu;
