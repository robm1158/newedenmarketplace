
import image from '../../assets/images/portrait.jpg'
import './Aboutme.css';

function Aboutme() {

    return (
        <div className="centered-container">
            <h1><img src={image} alt="Character Portrait"/></h1>
            <div className="overview-section">
                <h2>About Me</h2>
                <p className="stylish-text">

                Hello, fellow space enthusiasts and market strategists! I'm Xit Statik Daphiti (just like it sounds: "exit static daphiti"), 
                your guide through the cosmic ventures of EvE Online. My journey began not in the vast reaches of virtual space, but with a 
                fascination for the real stars above us. With a Bachelor’s degree in Astrophysics and the start of a Masters in Machine Learning 
                and Artificial Intelligence, I've always been drawn to the unknown. My career took flight in the space industry, where I’ve 
                spent over six years creating software that breathes life into satellites and crafts that venture into the great expanse.
                <br /><br />
                My most memorable work includes my time at Johns Hopkins Applied Physics Lab, where I contributed to the Dragonfly mission to Titan. 
                It’s this blend of space and technology that fuels my passion and leads me to where I am today – a software developer with a zeal for 
                data analytics and machine learning, applying these skills to both terrestrial and extraterrestrial projects.<br /><br />

                In the universe of EvE Online, I'm not just a starship commander but also a ten-year veteran, a testament to my dedication to this digital cosmos. 
                My in-game feats range from running a nullsec corporation and commanding fleets in monumental battles, to being an active participant in the 
                Alliance Tournament with TEST Alliance.<br /><br />

                The creation of this market tool is the fusion of my real-world expertise and my virtual space escapades. 
                It’s been a dream in the making, born from a desire to give traders like you the edge in the ever-thrilling economic warfare of EvE. 
                This project, meticulously crafted in the margins of my personal time over recent months, is my way of contributing to a community that 
                thrives on strategy, intelligence, and, of course, a bit of luck.
                <br /><br />
                Enjoy the journey, and may your trades be as prosperous as the stars are numerous!
          
                </p>
            </div>
        </div>
    );    
    
}

export default Aboutme;
