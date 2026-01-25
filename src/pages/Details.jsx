import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router";
import DetailsTopbar from "../components/Topbars/DetailsTopbar";
import TravelDetails from "../components/Cards/TravelDetails";
import Map from "../components/Map/Map";
import Aircraft from "../components/Cards/Aircraft";
import Delays from "../components/Cards/Delays";
import Gate from "../components/Cards/Gate";
import { getFlightDetails } from "../services/openai";
import { haversineDistance } from "../helpers/distance";
import Primary from "../components/Buttons/Primary";

const Details = () => {
  let navigate = useNavigate();
  const location = useLocation();
  const [flight, setFlight] = useState(null);

  useEffect(() => {
    getFlightDetails(location.state.flightNumber)
      .then((result) => {
        setFlight(result);
      })
      .catch((error) => {
        console.error("Error fetching flight details:", error);
        setFlight(null);
      });
  }, [location.state]);

  const redirectToNearestFlightsWithSearchData = () => {
    navigate("/flights", {
      state: { to: flight?.to || "", from: flight?.from },
    });
  };

  if (!flight) return null;

  return (
    <div>
      <DetailsTopbar flightNumber={location.state.flightNumber} />
      <div className="flex">
        <div className="w-[50%] h-[calc(100vh-50px)] p-4">
          <Map
            arrivalCoordinates={flight?.arrival?.airport?.location}
            planeCoordinates={flight?.location}
            departureCoordinates={flight?.departure?.airport?.location}
          />
        </div>
        <div className="w-[50%] p-4">
          {flight && (
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-4">
                <TravelDetails
                  departureTime={flight?.departureTime}
                  arrivalTime={flight?.arrivalTime}
                  altitude={flight?.location?.altitude?.feet}
                  distance={haversineDistance(
                    flight?.location?.lat ||
                      flight?.arrival?.airport?.location?.lat,
                    flight?.location?.lon ||
                      flight?.arrival?.airport?.location?.lon,
                    flight?.arrival?.airport?.location?.lat,
                    flight?.arrival?.airport?.location?.lon,
                  )}
                  duration={flight?.duration}
                  progress={flight?.progress}
                  from={flight?.from}
                  to={flight?.to}
                  status={flight?.status}
                  speed={flight?.location?.groundSpeed?.kmPerHour}
                />
                <Delays
                  delayTime={flight?.delayMinutes}
                  delayReason={flight?.delayReason}
                />
              </div>
              <div className="flex flex-col gap-4">
                <Aircraft
                  model={flight?.aircraft?.model}
                  reg={flight?.aircraft?.reg}
                  company={flight?.airline?.name}
                />
                <Gate
                  gate={flight?.gate}
                  departureTime={flight?.departureTime}
                  terminal={flight?.terminal}
                />
              </div>
              <div>
                <Primary
                  className="p-2"
                  text="Find other connections"
                  onClick={redirectToNearestFlightsWithSearchData}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Details;
