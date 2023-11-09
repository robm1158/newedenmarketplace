import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import AuthContext from '../AuthContext/AuthContext';
import { useNavigate } from 'react-router-dom';

const AuthProvider = ({ children }) => {
  const [auth, setAuthState] = useState(null);
  const navigate = useNavigate(); // useNavigate hook for navigation
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  const refreshToken = useCallback(async () => {
    try {
      console.log('Refreshing token');
      const response = await axios.post(`${BACKEND_URL}/refresh_token`, {
        refresh_token: auth.refresh_token,
      });
      const newAuthData = response.data;
      setAuthState(prevAuth => ({
        ...prevAuth,
        access_token: newAuthData.access_token,
        expires_in: newAuthData.expires_in,
        refresh_token: newAuthData.refresh_token || prevAuth.refresh_token,
      }));
    } catch (error) {
      console.error('Error refreshing token:', error);
      navigate('/'); // Redirect to the home page
    }
  }, [auth?.refresh_token, BACKEND_URL, navigate]); // Add navigate to the dependency array

  useEffect(() => {
    if (auth && auth.expires_in) {
      const timeout = setTimeout(() => {
        refreshToken();
      }, (auth.expires_in - 300) * 1000); // 300 seconds before expiry

      return () => clearTimeout(timeout);
    }
  }, [auth, refreshToken]);

  const setAuth = (authData) => {
    setAuthState(authData);
  };

  const authContextValue = {
    auth,
    setAuth,
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
