import React from 'react';
import { useLocation } from 'react-router-dom';
import PlaceHolder from "./PlaceHolder.jsx";

const Layout = ({ children }) => {
    const location = useLocation();

    return (
        <>
            {location.pathname !== '/auth' && <PlaceHolder location={location.pathname}/>}
            {children}
        </>
    );
};

export default Layout;
