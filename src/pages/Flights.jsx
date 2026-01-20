import React from "react";
import DetailsTopbar from "../components/Topbars/DetailsTopbar";
import FlightListItem from "../components/Lists/FlightListItem";

const Flights = () => {
  return (
    <div>
      <DetailsTopbar
      // flight={flight}
      // setFlight={setFlight}
      // findFlightDetails={findFlightDetails}
      />
      <div className="flex">
        <FlightListItem
          departureTime="15:10"
          departureDate="10.01.2026"
          arrivalTime="23:55"
          arrivalDate="10.01.2026"
          stopovers="1 przesiadka"
          airline="LOT, Wizzair"
          departureAirport="CIA"
          stopoverAirport="BER"
          arrivalAirport="WRO"
          price="832 zł"
        />
      </div>
    </div>
  );
};

export default Flights;
