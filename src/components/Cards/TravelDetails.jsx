import {
  faArrowsLeftRight,
  faArrowsUpDown,
  faClock,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

const TravelDetails = () => {
  return (
    <div className="w-[100%]">
      <div className="shadow-xl rounded-[10px] bg-[#FAFAFA] p-4">
        <div className="text-[26px] font-bold text-[#646464]">
          Travel details
        </div>
        <div className="flex flex-col gap-2 mt-2">
          <span>
            <FontAwesomeIcon icon={faArrowsUpDown} className="text-[#646464]" />
            <span className="ml-2 text-[#646464]">30000 ft.</span>
          </span>
          <span>
            <FontAwesomeIcon
              icon={faArrowsLeftRight}
              className="text-[#646464]"
            />
            <span className="ml-2 text-[#646464]">114 km</span>
          </span>
          <span>
            <FontAwesomeIcon icon={faClock} className="text-[#646464]" />
            <span className="ml-2 text-[#646464]">0:45</span>
          </span>
        </div>
      </div>
    </div>
  );
};

export default TravelDetails;
