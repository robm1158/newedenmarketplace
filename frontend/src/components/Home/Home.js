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
                <div>{homeData.content}</div>
            ) : (
                <div>Loading...</div>
            )}
        </div>
    );
}

export default Home;
