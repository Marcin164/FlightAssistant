import {
  faArrowsLeftRight,
  faArrowsUpDown,
  faClock,
  faGauge,
  faPlane,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { toMinutes } from "../../helpers/time";
import { haversineDistance } from "../../helpers/distance";

const TravelDetails = ({
  departureTime,
  arrivalTime,
  altitude = "0",
  duration = "0",
  distance = "0",
  progress = 0,
  from,
  to,
  status = "Arrived",
  speed = "0",
}) => {
  return (
    <div className="w-[100%] shadow-xl rounded-[10px] bg-[#FAFAFA] p-4">
      <div className="text-[26px] font-bold text-[#646464]">Travel details</div>
      <div className="flex flex-col gap-2 mt-2">
        <span>
          <FontAwesomeIcon icon={faArrowsUpDown} className="text-[#646464]" />
          <span className="ml-2 text-[#646464]">{altitude} ft.</span>
        </span>
        <span>
          <FontAwesomeIcon
            icon={faArrowsLeftRight}
            className="text-[#646464]"
          />
          <span className="ml-2 text-[#646464]">{distance} km</span>
        </span>
        <span>
          <FontAwesomeIcon icon={faClock} className="text-[#646464]" />
          <span className="ml-2 text-[#646464]">{duration}</span>
        </span>
        <span>
          <FontAwesomeIcon icon={faPlane} className="text-[#646464]" />
          <span className="ml-2 text-[#646464]">{status}</span>
        </span>
        <span>
          <FontAwesomeIcon icon={faGauge} className="text-[#646464]" />
          <span className="ml-2 text-[#646464]">{speed}</span>
        </span>
      </div>
      <div>
        <progress
          className="w-full mt-4 h-[10px] rounded-lg"
          value={progress}
          max="100"
        />
        <div className="w-full flex justify-between text-[#646464]">
          <span>{departureTime}</span>
          <span>{arrivalTime}</span>
        </div>
        <div className="w-full flex justify-between text-[#646464]">
          <span>{from}</span>
          <span>➔</span>
          <span>{to}</span>
        </div>
      </div>
    </div>
  );
};

export default TravelDetails;
