import React, { createContext, useReducer, useContext } from 'react';

const AuthContext = createContext();

const initialState = {
    email: null,
};

const authReducer = (state, action) => {
    switch (action.type) {
        case 'LOGIN':
            return { ...state, email: action.payload.email };
        case 'LOGOUT':
            return { ...state, email: null };
        default:
            return state;
    }
};

export const AuthProvider = ({ children }) => {
    const [state, dispatch] = useReducer(authReducer, initialState);

    return (
        <AuthContext.Provider value={{ state, dispatch }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
