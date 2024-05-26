// ProfilePage.jsx
import React from 'react';
import { useLocation } from 'react-router-dom';

const ProfilePage = () => {
    const location = useLocation();
    // Fetch user data if needed

    return (
        <div>
            <h1>User Profile</h1>
            {/* Display user profile details here */}
        </div>
    );
}

export default ProfilePage;
