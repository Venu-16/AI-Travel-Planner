import { useState } from "react";
import { generateItinerary } from "../services/api";

function TravelForm({ setItinerary }) {
  const [destination, setDestination] = useState("");
  const [days, setDays] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const response = await generateItinerary({
      destination,
      days,
    });

    setItinerary(response);
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        placeholder="Destination"
        value={destination}
        onChange={(e) => setDestination(e.target.value)}
        required
      />

      <input
        placeholder="Number of days"
        type="number"
        value={days}
        onChange={(e) => setDays(e.target.value)}
        required
      />

      <button type="submit">
        {loading ? "Planning..." : "Generate Plan"}
      </button>
    </form>
  );
}

export default TravelForm;
