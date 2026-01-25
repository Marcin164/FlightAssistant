import React, { useEffect, useState } from "react";
import { useLocation } from "react-router";
import DetailsTopbar from "../components/Topbars/DetailsTopbar";
import TravelDetails from "../components/Cards/TravelDetails";
import Map from "../components/Map/Map";
import PlaneState from "../components/Cards/PlaneState";
import Delays from "../components/Cards/Delays";
import Gate from "../components/Cards/Gate";
import { getFlightDetails } from "../services/openai";

const Details = () => {
  const location = useLocation();
  const [flight, setFlight] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    getFlightDetails(location.state.flightNumber)
      .then((result) => {
        setFlight(result);
      })
      .catch((error) => {
        console.error("Error fetching flight details:", error);
        setError("Nie udało się pobrać szczegółów lotu.");
        setFlight(null);
      });
  }, [location.state]);

  console.log(flight);

  if (!flight || error) return <div>Loading</div>;

  return (
    <div>
      <DetailsTopbar
        flight={location.state.flightNumber || ""}
        setFlight={setFlight}
        // findFlightDetails={findFlightDetails}
      />
      <div className="flex">
        <div className="w-[50%] h-[calc(100vh-50px)] p-4">
          <Map />
        </div>
        <div className="w-[50%] p-4">
          {loading && <div className="text-center py-4">Ładowanie...</div>}
          {error && <div className="text-red-500 py-4">Błąd: {error}</div>}
          {flight && (
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-4">
                <TravelDetails data={flight} />
                <Delays data={flight} />
              </div>
              <div className="flex flex-col gap-4">
                <PlaneState data={flight} />
                <Gate data={flight} />
              </div>
            </div>
          )}
          {!loading && !error && flight && (
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
