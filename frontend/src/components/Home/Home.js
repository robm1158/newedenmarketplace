import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Home() {
    const [homeData, setHomeData] = useState(null);

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
            {homeData ? (
                <div>
                    {homeData.message}
                    <h1>Welcome to the Homepage</h1>
                    <img src="https://images.evetech.net/characters/95383397/portrait?tenant=tranquility&size=256" alt="Character Portrait" />
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
