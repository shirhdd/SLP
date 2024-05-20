import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import MainMenu from "./MainMenu";
import Practice from "./Practice";
import Demo from "./Demo.jsx"

function App() {
    return (
        <div className="app-container">
            <Router>
                <Routes>
                    <Route path="/" element={<MainMenu />} />
                    <Route path="/practice" element={<Practice />} />
                    <Route path="/demo" element={<Demo word={"sing"}/>} />
                </Routes>
            </Router>
        </div>
    );
}

export default App;
