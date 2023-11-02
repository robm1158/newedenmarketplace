import React, { useState, useEffect } from 'react';
import axios from 'axios';
import image from '../../assets/images/portrait.jpg'

function Home() {
    const [homeData, setHomeData] = useState(null);
    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
    useEffect(() => {
        async function fetchHomeData() {
            try {
                const response = await axios.get(`${BACKEND_URL}/`);
                setHomeData(response.data);
            } catch (error) {
                console.error("Error fetching home data:", error);
            }
        }

        fetchHomeData();
    }, []);

    return (
        <div>
            {homeData ? (
                <div>
                    
                    <h1>Welcome to the Homepage</h1>
                    <img src={image} alt="Character Portrait" />
                    {/* Other content of your homepage */}
                
                </div>
        //         <div>
        //             <video width="100%" height="auto" controls>
        //         <source src={videoSource} type="video/mp4" />
        //         Your browser does not support the video tag.
        //     </video>
        // </div>
            ) : (
                <div>Loading...</div>
            )}
        </div>
    );
}

export default Home;
