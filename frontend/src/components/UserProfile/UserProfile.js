import React, { useContext, useEffect, useState, useCallback } from "react";
import axios from "axios";
import AuthContext from "../AuthContext/AuthContext";
import PaidContext from "../PaidContext/PaidContext";
import DonutChart from "../DonutChart/DonutChart";
import "./UserProfile.css";
import PagedTable from "../PagedTable/PagedTable";
import { LocationEnum } from "../../constants/locationEnum";
import { ItemEnum } from "../../constants/ItemEnum";


const REVERSED_ITEM_ENUM = Object.keys(ItemEnum).reduce((obj, key) => {
  obj[ItemEnum[key]] = key;
  return obj;
}, {});


const isRomanNumeral = (word) => {
  // Regex to match a Roman numeral
  const romanRegex =
    /^(?=[MDCLXVI])(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))$/i;
  return romanRegex.test(word);
};

const formatItemName = (itemName) => {
  if (!itemName) return "";
  return itemName
    .toLowerCase()
    .split("_")
    .map((word) => {
      return isRomanNumeral(word)
        ? word.toUpperCase()
        : word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
};

const UserProfile = () => {
  const { auth } = useContext(AuthContext);
  const { isPaid, setPaid } = useContext(PaidContext);
  const [wallet, setWallet] = useState(null);
  const [characterInfo, setCharacterInfo] = useState({
    id: null,
    name: null,
    alliance_id: null,
    corporation_id: null,
  });
  const [corpInfo, setCorpInfo] = useState({
    id: null,
    name: null,
    alliance_id: null,
    ticker: null,
    member_count: null,
  });
  const [orders, setOrders] = useState([]); // State to hold orders
  const [orderHistory, setOrderHistory] = useState([]); // State to hold order history
  const [chartData, setChartData] = useState([]);
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;



  function transformDataWithLocation(data) {
    return data.map((row) => {
      const locationName = LocationEnum[row.location_id] || row.location_id;
      return {
        ...row,
        location_id: locationName,
      };
    });
  }

  const transformDataWithType = useCallback((data) => {
    return data.map((row) => {
      const rawItemName =
        REVERSED_ITEM_ENUM[row.type_id] || `Unknown Item (${row.type_id})`;
      const formattedItemName = formatItemName(rawItemName);

      return {
        ...row,
        type_id: formattedItemName, // Replace type_id with the formatted item name
      };
    });
  }, [  ]);

  const transformOrderHistory = useCallback((data) => {
    return data.map((row) => {
      const rawItemName =
        REVERSED_ITEM_ENUM[row.type_id] || `Unknown Item (${row.type_id})`;
      const formattedItemName = formatItemName(rawItemName);

      // Check if state is 'Expired' and volume_remain is 0, then change state to 'Complete'
      const updatedState =
        row.state === "expired" && row.volume_remain === 0
          ? "Completed"
          : "Expired";
      const updatedIsBuyOrder = row.is_buy_order === true ? "Buy" : "Sell";

      return {
        ...row,
        type_id: formattedItemName, // Replace type_id with the formatted item name
        state: updatedState, // Update the state conditionally
        is_buy_order: updatedIsBuyOrder,
      };
    });
  }, [ ]);

  // Fetch character ID
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
            id: response.data.character_id,
            name: response.data.name,
            alliance_id: response.data.alliance_id,
            corporation_id: response.data.corporation_id,
          });
        } catch (error) {
          console.error("Error fetching character ID:", error);
        }
      }
    };

    fetchCharacterId();
  }, [auth, BACKEND_URL]);

  // Fetch wallet and paid status
  useEffect(() => {
    const getWallet = async () => {
      if (auth && auth.access_token) {
        try {
          const response = await axios.get(
            `${BACKEND_URL}/get_wallet_balance`,
            {
              headers: {
                Authorization: `Bearer ${auth.access_token}`,
              },
            }
          );
          setWallet(response.data);
        } catch (error) {
          console.error("Error fetching wallet:", error);
        }
      }
    };

    const getPaidStatus = async () => {
      if (auth && auth.access_token) {
        try {
          const response = await axios.get(`${BACKEND_URL}/get_paid_status`, {
            headers: {
              Authorization: `Bearer ${auth.access_token}`,
            },
          });
          setPaid(response.data.payment_received); // Update the paid status in the context
        } catch (error) {
          console.error("Error fetching paid status:", error);
        }
      }
    };

    getWallet();
    getPaidStatus();
  }, [auth, BACKEND_URL, setPaid]);

  // Fetch corporation info
  useEffect(() => {
    const getCorpInfo = async () => {
      if (
        characterInfo &&
        characterInfo.corporation_id &&
        auth &&
        auth.access_token
      ) {
        try {
          const response = await axios.get(
            `${BACKEND_URL}/get_corp_info/${characterInfo.corporation_id}`,
            {
              headers: {
                Authorization: `Bearer ${auth.access_token}`,
              },
            }
          );
          setCorpInfo({
            id: characterInfo.corporation_id,
            name: response.data.name,
            alliance_id: response.data.alliance_id,
            ticker: response.data.ticker,
            member_count: response.data.member_count,
          });
        } catch (error) {
          console.error("Error fetching corporation info:", error);
        }
      }
    };

    getCorpInfo();
  }, [characterInfo, auth, BACKEND_URL]);

  useEffect(() => {
    const fetchOrders = async () => {
      if (characterInfo && characterInfo.id && auth && auth.access_token) {
        try {
          const response = await axios.get(
            `${BACKEND_URL}/get_character_orders/${characterInfo.id}`,
            {
              headers: {
                Authorization: `Bearer ${auth.access_token}`,
              },
            }
          );
          // First, transform the data with type information
          const transformedWithType = transformDataWithType(response.data);

          // Then, if needed, transform the data with location
          const transformedWithLocation =
            transformDataWithLocation(transformedWithType);

          // Finally, set the transformed data to the orders state
          setOrders(transformedWithLocation);
        } catch (error) {
          console.error("Error fetching orders:", error);
        }
      }
    };

    fetchOrders();
  }, [characterInfo, auth, BACKEND_URL, transformDataWithType]);

  useEffect(() => {
    const fetchOrderHistory = async () => {
      if (characterInfo && characterInfo.id && auth && auth.access_token) {
        try {
          const response = await axios.get(
            `${BACKEND_URL}/get_character_order_history/${characterInfo.id}`,
            {
              headers: {
                Authorization: `Bearer ${auth.access_token}`,
              },
            }
          );
          const transformedWithLocation = transformDataWithLocation(
            response.data
          );
          const transformedOrderHistory = transformOrderHistory(
            transformedWithLocation
          );
          setOrderHistory(transformedOrderHistory);
        } catch (error) {
          console.error("Error fetching orders:", error);
        }
      }
    };

    fetchOrderHistory();
  }, [characterInfo, auth, BACKEND_URL, transformOrderHistory]);

  useEffect(() => {
    const fetchData = async () => {
      if (characterInfo && characterInfo.id && auth && auth.access_token) {
        try {
          const response = await axios.get(
            `${BACKEND_URL}/get_character_wallet_journal/${characterInfo.id}`,
            {
              headers: { Authorization: `Bearer ${auth.access_token}` },
            }
          );

          setChartData(response.data);
        } catch (error) {
          console.error("Error fetching wallet journal data:", error);
        }
      }
    };

    fetchData();
  }, [characterInfo, auth, BACKEND_URL]);

  const orderheaders = [
    { displayName: "Location", dataKey: "location_id" },
    { displayName: "Item", dataKey: "type_id" },
    { displayName: "Price Per Unit", dataKey: "price" },
    { displayName: "Volume Remain", dataKey: "volume_remain" },
    { displayName: "Volume Total", dataKey: "volume_total" },
    { displayName: "Issued", dataKey: "issued" },
  ];

  const orderhistoryheaders = [
    { displayName: "Status", dataKey: "state" },
    { displayName: "Buy/Sell", dataKey: "is_buy_order" },
    { displayName: "Location", dataKey: "location_id" },
    { displayName: "Item", dataKey: "type_id" },
    { displayName: "Price Per Unit", dataKey: "price" },
    { displayName: "Volume Remain", dataKey: "volume_remain" },
    { displayName: "Volume Total", dataKey: "volume_total" },
  ];

  const buyOrders = orders.filter((order) => order.is_buy_order);
  const sellOrders = orders.filter((order) => !order.is_buy_order);

  // Render the component
  return (
    <div className="dashboard-container">
      <div className="profile-container">
        <div className="character-profile">
          <img
            src={`https://images.evetech.net/characters/${characterInfo.id}/portrait?tenant=tranquility&size=128`}
            alt="Character Portrait"
          />
          <div>
            <h1 className="character-name">{characterInfo.name}</h1>
            <p className={`payment-status ${isPaid ? "paid" : "unpaid"}`}>
              {isPaid ? "Subscription: Active" : "Subscription: Inactive"}
            </p>
            <p className="wallet-balance">
              Current Wallet:{" "}
              {new Intl.NumberFormat("en-US", {
                style: "decimal",
                maximumFractionDigits: 2,
              }).format(wallet)}{" "}
              ISK
            </p>
          </div>
        </div>
        <div className="corporation-logo-container">
          <div>
            <h1 className="corp-name">{corpInfo.name}</h1>
            <p className="corp-ticker">{corpInfo.ticker}</p>
            <p className="corp-member-count">Members:{corpInfo.member_count}</p>
          </div>
          <img
            src={`https://images.evetech.net/corporations/${characterInfo.corporation_id}/logo?tenant=tranquility&size=128`}
            alt="Corporation Logo"
          />
        </div>
      </div>
      {isPaid ? (
        <>
          <div className="orders-container">
            <h2 className="orders-header">Current Orders</h2>
            <div className="tables-container">
              <div className="buy-table-container">
                <h2 className="buy-orders-header">Buy Orders</h2>
                <PagedTable data={buyOrders} headers={orderheaders} />
              </div>

              <div className="sell-table-container">
                <h2 className="sell-orders-header">Sell Orders</h2>
                <PagedTable data={sellOrders} headers={orderheaders} />
              </div>
            </div>
          </div>
          <div className="donut-chart-container">
            <h2 className="chart-header">Wallet Journal Analysis</h2>
            <DonutChart data={chartData} />
          </div>
            <div className="orders-history-container">
              <h2 className="orders-header">Order History</h2>
              <PagedTable data={orderHistory} headers={orderhistoryheaders} />
            </div>
        </>
      ) : (
        <div className="inactive-overlay">
          <div className="inactive-subscription">
            <h2 className="inactive-message">Subscription: Inactive</h2>
          </div>
          <div className="orders-container blurred">
            {/* ... Repeat the orders and order history containers but with a blurred class ... */}
          </div>
          <div className="orders-history-container blurred">
            {/* ... Repeat the orders and order history containers but with a blurred class ... */}
          </div>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
