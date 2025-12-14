function ItineraryResult({ itinerary }) {
  if (!itinerary) return null;

  return (
    <div>
      <h2>Your Travel Plan 🧭</h2>
      <pre style={{ whiteSpace: "pre-wrap" }}>{itinerary}</pre>
    </div>
  );
}

export default ItineraryResult;
