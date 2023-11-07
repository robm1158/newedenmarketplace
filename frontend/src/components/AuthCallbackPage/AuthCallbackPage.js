import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AuthCallbackPage = () => {
  const navigate = useNavigate();
  useEffect(() => {
    const code = new URLSearchParams(window.location.search).get('code');
    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

    if (code) {
      // Replace with your Flask API endpoint that handles the OAuth exchange
      axios.post(`${BACKEND_URL}/exchange`, { code })
        .then(response => {
          // Process the response, store the tokens, manage login state, etc.
          navigate('/dashboard'); // Redirect to the dashboard or another page
        })
        .catch(error => {
          console.error('Error exchanging code for tokens:', error);
          navigate('/'); // On error, redirect to home or error page
        });
    }
  }, [navigate]);

  return (
    <div>
      Authenticating...
    </div>
  );
};

export default AuthCallbackPage;
