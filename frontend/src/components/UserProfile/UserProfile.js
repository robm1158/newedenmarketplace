import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import AuthContext from '../AuthContext/AuthContext';
import './UserProfile.css';

const UserProfile = () => {
  const { auth } = useContext(AuthContext);
  const [orders, setOrders] = useState(null);
  const [wallet, setWallet] = useState(null);
  const [paid, setPaid] = useState(false);
  const [characterInfo, setCharacterInfo] = useState({ id: null, name: null, alliance_id: null, corporation_id: null });
  const [corpInfo, setCorpInfo] = useState({ id: null, name: null, alliance_id: null, ticker: null, member_count: null});
  const [Alliancename, setAllianceName] = useState(null);
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    const fetchCharacterId = async () => {
      if (auth && auth.access_token) {
        try {
          const response = await axios.get(`${BACKEND_URL}/get_character_id`, {
            headers: {
              Authorization: `Bearer ${auth.access_token}`,
            },
            
          } );
          setCharacterInfo({
            id: response.data.character_id,
            name: response.data.name,
            alliance_id: response.data.alliance_id,
            corporation_id: response.data.corporation_id
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
    const getPaidStatus = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/get_wallet_log`, {
          headers: {
            Authorization: `Bearer ${auth.access_token}`,  // Use the access token from auth
          },
        });
        setPaid(response.data);
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
    //   getCurrentOrders();
      getWallet();
      getPaidStatus();
    }
  }, [auth, BACKEND_URL]);  // Depend on auth to re-run when it changes

  useEffect(() => {
    // Function to get corporation info
    const getCorpInfo = async () => {
      // Check if corporation_id is available before making the call
      if (characterInfo && characterInfo.corporation_id && auth && auth.access_token) {
        try {
          const response = await axios.get(`${BACKEND_URL}/get_corp_info/${characterInfo.corporation_id}`, {
            headers: {
              Authorization: `Bearer ${auth.access_token}`
            },
          });
          setCorpInfo({ 
              id: characterInfo.corporation_id, 
              name: response.data.name,
              alliance_id: response.data.alliance_id,
              ticker: response.data.ticker, 
              member_count: response.data.member_count
          });
        } catch (error) {
          console.error('Error fetching corporation info:', error);
          // Handle error, e.g. redirect to login if the token is invalid
        }
      }
    };
  
    getCorpInfo();
  }, [characterInfo, auth, BACKEND_URL]); 
  
  // Render your dashboar.payment_receiveded
  return (
    <div className="dashboard-container">
        <div className="profile-container">
            <div className="character-profile">
                <img src={`https://images.evetech.net/characters/${characterInfo.id}/portrait?tenant=tranquility&size=128`} alt="Character Portrait" />
                <div>
                    <h1 className="character-name">{characterInfo.name}</h1>
                    <p className={`payment-status ${paid.payment_received ? "paid" : "unpaid"}`}>
                        {paid.payment_received ? "Active: Paid" : "Inactive: Un-paid"}
                    </p>
                    <p className="wallet-balance">Current Wallet: {new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(wallet)} ISK</p>
                </div>
            </div>
            <div className="corporation-logo-container">
                <div>
                    <h1 className="corp-name">{corpInfo.name}</h1>
                    <p className='corp-ticker'>{corpInfo.ticker}</p>
                    <p className='corp-member-count'>Members:{corpInfo.member_count}</p>
                </div>
                <img src={`https://images.evetech.net/corporations/${characterInfo.corporation_id}/logo?tenant=tranquility&size=128`} alt="Corporation Logo" />
            </div>
        </div>
        <div className="orders-container">
            <h2>Current Orders</h2>
            {/* Render orders here */}
        </div>
    </div>
  );
};

export default UserProfile;
