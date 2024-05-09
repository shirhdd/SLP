import {useState} from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';
import DragAndDrop from "./DragAndDrop.jsx";
import RandomWord from "./RandomWord.jsx";

function App() {
    return (
        <>
            <RandomWord/>
            <DragAndDrop/>
        </>
    );
}

export default App;
