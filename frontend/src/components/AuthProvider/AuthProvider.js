import React, { useState, useCallback } from 'react';
import AuthContext from '../AuthContext/AuthContext';


// This is a simplified version and should include token refresh, error handling, etc.
const AuthProvider = ({ children }) => {
    const [auth, setAuthState] = useState(null);

    const setAuth = useCallback((authData) => {
        setAuthState(authData);
      }, []);


    // The value provided to the context consumers
    const authContextValue = {
        auth,
        setAuth
      };

    return (
        <AuthContext.Provider value={authContextValue}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;
