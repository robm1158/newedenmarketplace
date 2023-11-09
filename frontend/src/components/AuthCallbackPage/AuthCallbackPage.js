import React, { useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import AuthContext from '../AuthContext/AuthContext'; // Make sure the path is correct

const AuthCallbackPage = () => {
  const navigate = useNavigate();
  const { setAuth } = useContext(AuthContext); // Destructure the setAuth function from context

  useEffect(() => {
    const code = new URLSearchParams(window.location.search).get('code');
    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

    if (code) {
      axios.post(`${BACKEND_URL}/exchange`, { code })
        .then(response => {
          // Assuming the response contains your tokens and user information
          setAuth(response.data); // Update the auth context with the received data
          navigate('/userprofile'); // Redirect to the dashboard or another page
        })
        .catch(error => {
          console.error('Error exchanging code for tokens:', error);
          navigate('/'); // On error, redirect to home or error page
        });
    }
  }, [navigate, setAuth]); // Include setAuth in the dependency array

  return (
    <div>
      Authenticating...
    </div>
  );
};

export default AuthCallbackPage;
