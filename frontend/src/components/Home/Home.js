import React, { useState, useEffect } from 'react';
import axios from 'axios';
import image from '../../assets/images/Artboard_1_copy.png'

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
        <div>
                
                    
            <h1><img src={image} alt="Character Portrait"/></h1>
            {/* Other content of your homepage */}
                
    
        </div>
    );
}

export default Home;
