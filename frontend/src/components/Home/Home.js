import React, { useState, useEffect } from 'react';
import axios from 'axios';
import image from '../../assets/images/Artboard_1_copy.png'
import './Home.css';

function Home() {
    const [, setHomeData] = useState(null);
    
    useEffect(() => {
        async function fetchHomeData() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/');
                setHomeData(response.data);
                
            } catch (error) {
                console.error("Error fetching home data:", error);
            }
        }

        fetchHomeData();
    }, []);

    return (
        <div className="centered-container">
            <h1><img src={image} alt="Character Portrait"/></h1>
            <div className="overview-section">
                <h2>Overview</h2>
                <p className="stylish-text">
                    This project is an ambitious undertaking aimed at significantly enhancing the decision-making process of market traders in identifying lucrative investments. 
                    By integrating advanced Machine Learning (ML) models and comprehensive data analytics presented through various graphical representations, 
                    this tool seeks to empower users with deeper insights and predictive analytics. 
                    It is a testament to ongoing innovation and dedication to continuous improvement in EvE's financial technology space.<br /><br />
                    
                    While the tool is in active development and shows great promise, it's important to recognize that it is not a silver bullet. 
                    No system can guarantee absolute success, and this platform is no exception. It is not 100% foolproof and should be used as an augmentative tool to support, 
                    not replace, the nuanced judgement of savvy traders. The project's evolution is continuous, with enhancements and refinements being made regularly. 
                    Users are invited to be part of this journey, as the tool evolves and adapts to the ever-changing landscape of the market, 
                    always with the aim of providing valuable, actionable intelligence for the discerning trader.
                </p>
            </div>
        </div>
    );    
    
}

export default Home;
