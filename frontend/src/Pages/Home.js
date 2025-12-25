import TravelForm from "../components/TravelForm";
import ItineraryResult from "../components/ItineraryResult";
import Auth from "../components/Auth";
import { useState, useEffect } from "react";
import { logout, getCurrentToken } from "../services/api";

function Home() {
  const [itinerary, setItinerary] = useState("");
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    setAuthenticated(Boolean(getCurrentToken()));
  }, []);

  const handleLogout = () => {
    logout();
    setAuthenticated(false);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Travel Planner ✈️</h1>
      {!authenticated ? (
        <Auth onAuth={() => setAuthenticated(true)} />
      ) : (
        <div>
          <div style={{ marginBottom: 12 }}>
            <button onClick={handleLogout}>Log out</button>
          </div>
          <TravelForm setItinerary={setItinerary} />
          <ItineraryResult itinerary={itinerary} />
        </div>
      )}
    </div>
  );
}

export default Home;
