import React from "react";
import Text from "../Inputs/Text";
import Primary from "../Buttons/Primary";

const DetailsTopbar = ({ flight, setFlight, findFlightDetails }) => {
  return (
    <div className="h-[50px] flex items-center px-4">
      <div className="mr-4">
        <div className="text-[#3F77D8] text-[22px] font-bold">{flight}</div>
      </div>
      <div className="flex justify-around">
        <Text
          placeholder="Flight number"
          onChange={(e) => setFlight(e.target.value)}
          className="w-[200px]"
        />
      </div>
      <div className="mx-4 text-[24px] text-[#646464] font-bold">OR</div>
      <div className=" flex justify-around">
        <Text
          placeholder="Departure airport"
          onChange={(e) => setFlight(e.target.value)}
          className="w-[200px] mr-2"
        />
        <Text
          placeholder="Arrival airport"
          onChange={(e) => setFlight(e.target.value)}
          className="w-[200px] mr-2"
        />
        <Text
          placeholder="Departure date"
          onChange={(e) => setFlight(e.target.value)}
          className="w-[200px] mr-2"
        />
        <Text
          placeholder="Arrival date"
          onChange={(e) => setFlight(e.target.value)}
          className="w-[200px] mr-2"
        />
        {/* <Primary text="Search" className="mt-4" onClick={findFlightDetails} /> */}
      </div>
    </div>
  );
};

export default DetailsTopbar;
