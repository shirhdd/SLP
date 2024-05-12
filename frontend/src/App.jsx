import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import MainMenu from "./MainMenu";
import Practice from "./Practice";
import Wheel from "./Wheel.jsx";

function App() {
    return (
        <div className="app-container">
            <Router>
                <Routes>
                    <Route path="/" element={<MainMenu />} />
                    <Route path="/practice" element={<Practice />} />
                    <Route path="/wheel" element={<Wheel words={["example - 1","example - 2","example - 3","example - 4"]}/>} />
                </Routes>
            </Router>
        </div>
    );
}

export default App;
