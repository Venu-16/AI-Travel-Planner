import TravelForm from "../components/TravelForm";
import ItineraryResult from "../components/ItineraryResult";
import { useState } from "react";

function Home() {
  const [itinerary, setItinerary] = useState("");

  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Travel Planner ✈️</h1>
      <TravelForm setItinerary={setItinerary} />
      <ItineraryResult itinerary={itinerary} />
    </div>
  );
}

export default Home;
