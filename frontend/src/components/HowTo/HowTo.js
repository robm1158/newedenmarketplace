import image from '../../assets/images/Artboard_1_copy.png';
import paypalQR from '../../assets/images/paypal_qr.jpg'; // Make sure the path is correct
import './HowTo.css';

function HowTo() {
    return (
        <div className="centered-container">
            <h1><img src={image} alt="Page Header"/></h1>
            <div className="overview-section">
                <h2>How To Use The Website</h2>
                <p className="stylish-text">
                    This will be a basic overview on how to use the website. Some of the tools will be blocked behind a pay wall such as the predictive market tool, some industry options, etc.
                    The subscription cost is 1bil ISK per month. If you are interested in subscribing, please send ISk in-game to XiT StatiK Daphiti. The server caches every hour so
                    it may take up to an hour for your subscription to be active. If you have any questions, please contact me in-game or on Discord (xit_statik)
                    <br /><br />
                    {/* Additional content */}
                </p>
                <h2>Please Reference The Video Below</h2>
            </div>
            <div className="payment-container">
                <a href="https://venmo.com/u/Rob-Mullins-3" target="_blank" rel="noopener noreferrer">
                    <img src={paypalQR} alt="PayPal QR Code" className="paypal-qr" />
                </a>
                <p>If you find the tools useful, consider supporting the project:</p>
                <a href="https://venmo.com/u/Rob-Mullins-3" className="venmo-link" target="_blank" rel="noopener noreferrer">
                    Venmo: @Rob-Mullins-3
                </a>
            </div>
        </div>
    );
}

export default HowTo;
