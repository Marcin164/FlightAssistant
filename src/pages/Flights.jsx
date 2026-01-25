import React, { useEffect, useState } from "react";
import FlightsTopbar from "../components/Topbars/FlightsTopbar";
import FlightListItem from "../components/Lists/FlightListItem";
import { getNearestFlights } from "../services/openai";
import { useLocation } from "react-router";

const Flights = () => {
  const location = useLocation();
  const [flights, setFlights] = useState(null);

  useEffect(() => {
    getNearestFlights(location.state.from, location.state.to)
      .then((result) => {
        setFlights(result);
      })
      .catch((error) => {
        console.error("Error fetching flight details:", error);
        setFlights(null);
      });
  }, [location.state]);

  return (
    <div>
      <FlightsTopbar from={location.state.from} to={location.state.to} />
      <div className="flex justify-center mt-4">
        {flights &&
          flights?.length > 0 &&
          flights.map((flight) => <FlightListItem {...flight} />)}
      </div>
      {!flights && (
        <div className="text-center text-[#646464] text-[18px]">
          No flights found.
        </div>
      )}
    </div>
  );
};

export default Flights;
