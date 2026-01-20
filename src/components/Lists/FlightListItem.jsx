import {
  faArrowsLeftRight,
  faGauge,
  faHandHoldingDollar,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

const FlightListItem = ({
  departureTime,
  departureDate,
  arrivalTime,
  arrivalDate,
  stopovers,
  airline,
  departureAirport,
  stopoverAirport,
  arrivalAirport,
  price,
}) => {
  return (
    <div className="w-[35vw] bg-white rounded-lg shadow-xl p-4 flex items-center justify-between hover:shadow-lg transition-shadow">
      {/* Departure Time */}
      <div className="text-center">
        <div className="text-2xl font-bold text-gray-800">{departureTime}</div>
        <div className="text-xs text-gray-500">{departureDate}</div>
      </div>

      {/* Arrow Connector */}
      <div className="w-[200px] flex-1 mx-4 flex flex-col items-center">
        <div className="border-t-2 border-gray-300 w-12"></div>
        <div className="text-xs text-gray-600 font-semibold mt-1">
          {stopovers}
        </div>
      </div>

      {/* Arrival Time */}
      <div className="text-center">
        <div className="text-2xl font-bold text-gray-800">{arrivalTime}</div>
        <div className="text-xs text-gray-500">{arrivalDate}</div>
      </div>

      {/* Airline & Route Info */}
      <div className="flex-1 mx-6">
        <div className="flex items-center gap-2 mb-2">
          <div className="text-xs font-semibold text-gray-700">{airline}</div>
        </div>
        <div className="flex gap-2 text-xs text-gray-600">
          <span>{departureAirport}</span>
          <span>•</span>
          <span>{stopoverAirport}</span>
          <span>•</span>
          <span>{arrivalAirport}</span>
        </div>
      </div>

      <div className="flex gap-2 mr-4">
        <span className="inline-flex items-center justify-center w-6 h-6 bg-green-500 rounded-full text-white text-xs">
          <FontAwesomeIcon icon={faGauge} />
        </span>
        <span className="inline-flex items-center justify-center w-6 h-6 bg-green-500 rounded-full text-white text-xs">
          <FontAwesomeIcon icon={faHandHoldingDollar} />
        </span>
        <span className="inline-flex items-center justify-center w-6 h-6 bg-yellow-400 rounded-full text-white text-xs">
          <FontAwesomeIcon icon={faArrowsLeftRight} />
        </span>
      </div>

      {/* Price */}
      <div className="text-right">
        <div className="text-2xl font-bold text-gray-800">{price}</div>
        <div className="text-xs text-gray-500">cena za osobę</div>
      </div>
    </div>
  );
};

export default FlightListItem;
