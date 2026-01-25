import React, { useState } from "react";
import Text from "../Inputs/Text";
import Primary from "../Buttons/Primary";
import { useNavigate } from "react-router";

const DetailsTopbar = ({ flightNumber }) => {
  let navigate = useNavigate();
  const [flightDetails, setFlightDetails] = useState({
    flightNumber: "",
    arrivalTime: "",
    departureTime: "",
    arrivalAirport: "",
    departureAirport: "",
  });

  const handleFlightDetailsChange = (e) => {
    const { name, value } = e.target;

    setFlightDetails({
      ...flightDetails,
      [name]: value,
    });
  };

  const findFlightDetails = () => {
    navigate("/details", {
      state: { ...flightDetails },
    });
  };

  return (
    <div className="h-[50px] flex items-center px-4">
      <div className="mr-4">
        <div className="text-[#3F77D8] text-[22px] font-bold">
          {flightNumber}
        </div>
      </div>
      <div className="flex justify-around">
        <Text
          placeholder="Flight number"
          onChange={handleFlightDetailsChange}
          className="w-[200px]"
        />
      </div>
      <div className="mx-4 text-[24px] text-[#646464] font-bold">OR</div>
      <div className=" flex justify-around">
        <Text
          placeholder="Departure airport"
          onChange={handleFlightDetailsChange}
          className="w-[200px] mr-2"
        />
        <Text
          placeholder="Arrival airport"
          onChange={handleFlightDetailsChange}
          className="w-[200px] mr-2"
        />
        <Text
          placeholder="Departure date"
          onChange={handleFlightDetailsChange}
          className="w-[200px] mr-2"
        />
        <Text
          placeholder="Arrival date"
          onChange={handleFlightDetailsChange}
          className="w-[200px] mr-2"
        />
        <Primary text="Search" onClick={findFlightDetails} />
      </div>
    </div>
  );
};

export default DetailsTopbar;
