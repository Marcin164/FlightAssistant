import React, {useState} from "react";
import Text from "../components/Inputs/Text";
import Primary from "../components/Buttons/Primary";
import {useNavigate} from "react-router";

const Home = () => {
  let navigate = useNavigate();
  const [flightDetails, setFlightDetails] = useState({
    flightNumber: "",
    arrivalTime: "",
    departureTime: "",
    arrivalAirport: "",
    departureAirport: "",
  });
  const [chatInput, setChatInput] = useState("");

  const handleFlightDetailsChange = (e) => {
    const {name, value} = e.target;

    setFlightDetails({
      ...flightDetails,
      [name]: value,
    });
  };

  const handleChatInput = (e) => {
    const {value} = e.target;
    setChatInput(value);
  };

  const redirectToDetailsWithSearchData = () => {
    console.log(flightDetails);
    navigate("/details", {state: {...flightDetails}});
  };

  const redirectToChat = () => {
    navigate("/chat", {state: {chatInput}});
  };

  return (
    <div>
      <div className="p-2 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <div className="text-[#646464] text-[24px] font-light">
          Hey, I am your flight assistant
        </div>
        <div className="text-[#3F77D8] text-[30px] font-bold">
          Tell me your flight and I will find everything important
        </div>
        <div className="my-8 w-full">
          <Text
            placeholder="Enter flight number"
            name="flightNumber"
            onChange={handleFlightDetailsChange}
          />
        </div>
        <div className="text-[#646464] text-[24px] font-light">OR</div>
        <div className="my-8 space-y-2 space-x-2">
          <Text
            placeholder="Arrival time"
            name="arrivalTime"
            onChange={handleFlightDetailsChange}
          />
          <Text
            placeholder="Departure time"
            name="departureTime"
            onChange={handleFlightDetailsChange}
          />
          <Text
            placeholder="Arrival airport"
            name="arrivalAirport"
            onChange={handleFlightDetailsChange}
          />
          <Text
            placeholder="Departure airport"
            name="departureAirport"
            onChange={handleFlightDetailsChange}
          />
        </div>
        <Primary
          text="Search"
          className="mt-4 p-2"
          onClick={redirectToDetailsWithSearchData}
        />
        <div className="my-8">
          <Text
            placeholder="Or ask me something about your flight"
            name="chat"
            onChange={handleChatInput}
          />
          <Primary
            text="Ask"
            className="mt-4 p-2"
            onClick={redirectToChat}
          />
        </div>
      </div>
    </div>
  );
};

export default Home;
