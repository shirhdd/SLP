import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import MainMenu from "./MainMenu";
import Practice from "./Practice"; // Make sure this component is created

function App() {
    return (
        <div className="app-container"> {/* Added class here */}
            <Router>
                <Routes>
                    <Route path="/" element={<MainMenu />} />
                    <Route path="/practice" element={<Practice />} />
                </Routes>
            </Router>
        </div>
    );
}

export default App;
