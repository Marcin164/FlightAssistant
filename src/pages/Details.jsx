import React, { useState } from "react";
import { useParams } from "react-router";
import DetailsTopbar from "../components/Topbars/DetailsTopbar";
import TravelDetails from "../components/Cards/TravelDetails";
import Map from "../components/Map/Map";
import PlaneState from "../components/Cards/PlaneState";
import Delays from "../components/Cards/Delays";
import Gate from "../components/Cards/Gate";

const API_BASE_URL = "http://localhost:8000/api/openai";

const Details = () => {
  const params = useParams();
  const [flight, setFlight] = useState("FR 99");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const findFlightDetails = async () => {
    setLoading(true);
    setData(null);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/flight-details`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          flight_number: flight,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const flightData = await response.json();
      console.log("Flight data received:", flightData);
      setData(flightData);
    } catch (e) {
      console.error("Error fetching flight details:", e);
      setError(e.message || "Błąd podczas pobierania detali lotu");
    }

    setLoading(false);
  };

  return (
    <div>
      <DetailsTopbar
        flight={flight}
        setFlight={setFlight}
        findFlightDetails={findFlightDetails}
      />
      <div className="flex">
        <div className="w-[50%] h-[calc(100vh-50px)] p-4">
          <Map />
        </div>
        <div className="w-[50%] p-4">
          {loading && <div className="text-center py-4">Ładowanie...</div>}
          {error && <div className="text-red-500 py-4">Błąd: {error}</div>}
          {data && (
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-4">
                <TravelDetails data={data} />
                <Delays data={data} />
              </div>
              <div className="flex flex-col gap-4">
                <PlaneState data={data} />
                <Gate data={data} />
              </div>
            </div>
          )}
          {!loading && !error && !data && (
            <div className="text-center py-4 text-gray-500">
              Wyszukaj lot aby zobaczyć szczegóły
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Details;
