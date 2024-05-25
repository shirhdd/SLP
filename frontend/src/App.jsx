import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MainMenu from './MainMenu';
import Practice from './Practice';
import Demo from './Demo';
import Scores from './Scores';
import AuthForm from './AuthForm';
import './App.css';

function App() {
    const [loggedIn, setLoggedIn] = useState(false);

    return (
        <div className="app-container">
            <Router>
                <Routes>
                    <Route path="/" element={loggedIn ? <MainMenu/> : <Navigate to="/auth"/>}/>
                    <Route path="/practice" element={loggedIn ? <Practice/> : <Navigate to="/auth"/>}/>
                    <Route path="/demo" element={loggedIn ? <Demo word={"sing"}/> : <Navigate to="/auth"/>}/>
                    <Route path="/auth" element={<AuthForm setLoggedIn={setLoggedIn}/>}/>
                    <Route path="/scores" element={ <Scores/>}/>
                </Routes>
            </Router>
        </div>
    );
}

export default App;
