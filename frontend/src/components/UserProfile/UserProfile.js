import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import AuthContext from '../AuthContext/AuthContext';

const UserProfile = () => {
  const { auth } = useContext(AuthContext);
  const [orders, setOrders] = useState(null);
  const [wallet, setWallet] = useState(null);
  const [characterInfo, setCharacterInfo] = useState({ id: null, name: null });
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    const fetchCharacterId = async () => {
      if (auth && auth.access_token) {
        try {
          const response = await axios.get(`${BACKEND_URL}/get_character_id`, {
            headers: {
              Authorization: `Bearer ${auth.access_token}`,
            },
          });
          setCharacterInfo({ 
            id: response.data.CharacterID,
            name: response.data.CharacterName
          });
        } catch (error) {
          console.error('Error fetching character ID:', error);
          // Handle error, e.g. redirect to login if the token is invalid
        }
      }
    };

    // Call the function to fetch character information
    fetchCharacterId();
  }, [auth, BACKEND_URL]); 

  useEffect(() => {
    // Function to get current orders
    const getCurrentOrders = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/get_current_orders`, {
          headers: {
            Authorization: `Bearer ${auth.access_token}`,  // Use the access token from auth
          },
        });
        setOrders(response.data);
      } catch (error) {
        console.error('Error fetching current orders:', error);
        // Handle error, e.g. redirect to login if the token is invalid
      }
    };

    // Function to get wallet
    const getWallet = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/get_wallet_balance`, {
          headers: {
            Authorization: `Bearer ${auth.access_token}`,  // Use the access token from auth
          },
        });
        setWallet(response.data);
      } catch (error) {
        console.error('Error fetching wallet:', error);
        // Handle error, e.g. redirect to login if the token is invalid
      }
    };

    // Call both functions if the user is authenticated
    if (auth && auth.access_token) {
      getCurrentOrders();
      getWallet();
    }
  }, [auth, BACKEND_URL]);  // Depend on auth to re-run when it changes

  // Render your dashboard structure with the data received
  return (
    <div>
      {/* Render orders and wallet data */}
      <h1>{characterInfo.name}</h1>
      <div>
        <h2>Character ID</h2>
        <p>ID: {characterInfo.id}</p>
      </div>
      <div>
        <h2>Current Orders</h2>
        {/* Render orders here */}
      </div>
      <div>
        <h2>Wallet</h2>
        <p>wallet: {wallet}</p>
      </div>
    </div>
  );
};

export default UserProfile;
