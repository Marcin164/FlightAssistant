import axios from "axios";

const OpenAIflights = [
  {
    flightNumber: "MU262",
    airline: "China Eastern Airlines",
    from: "MAD",
    to: "WNZ",
    departureTime: "06:15",
    arrivalTime: "08:35",
    gate: "A3",
    terminal: "1",
    status: "On Time",
    delayMinutes: null,
  },
  {
    flightNumber: "FR8123",
    airline: "Ryanair",
    from: "KRK",
    to: "STN",
    departureTime: "09:40",
    arrivalTime: "11:20",
    gate: "B7",
    terminal: "2",
    status: "Delayed",
    delayMinutes: 25,
  },
  {
    flightNumber: "LH1347",
    airline: "Lufthansa",
    from: "FRA",
    to: "WAW",
    departureTime: "12:10",
    arrivalTime: "13:55",
    gate: "C2",
    terminal: "1",
    status: "On Time",
    delayMinutes: null,
  },
  {
    flightNumber: "AF1982",
    airline: "Air France",
    from: "CDG",
    to: "AMS",
    departureTime: "07:30",
    arrivalTime: "08:55",
    gate: "D5",
    terminal: "2",
    status: "On Time",
    delayMinutes: null,
  },
  {
    flightNumber: "BA879",
    airline: "British Airways",
    from: "LHR",
    to: "MAD",
    departureTime: "15:20",
    arrivalTime: "18:05",
    gate: "E11",
    terminal: "3",
    status: "Delayed",
    delayMinutes: 40,
  },
  {
    flightNumber: "EK180",
    airline: "Emirates",
    from: "DXB",
    to: "FCO",
    departureTime: "02:45",
    arrivalTime: "07:10",
    gate: "F1",
    terminal: "3",
    status: "On Time",
    delayMinutes: null,
  },
  {
    flightNumber: "KL1023",
    airline: "KLM",
    from: "AMS",
    to: "OSL",
    departureTime: "10:05",
    arrivalTime: "11:45",
    gate: "C9",
    terminal: "2",
    status: "On Time",
    delayMinutes: null,
  },
  {
    flightNumber: "W62215",
    airline: "Wizz Air",
    from: "KTW",
    to: "BCN",
    departureTime: "18:30",
    arrivalTime: "21:15",
    gate: "A18",
    terminal: "1",
    status: "Delayed",
    delayMinutes: 15,
  },
  {
    flightNumber: "SK751",
    airline: "Scandinavian Airlines",
    from: "ARN",
    to: "CPH",
    departureTime: "13:00",
    arrivalTime: "14:10",
    gate: "B4",
    terminal: "5",
    status: "On Time",
    delayMinutes: null,
  },
  {
    flightNumber: "IB3209",
    airline: "Iberia",
    from: "MAD",
    to: "LIS",
    departureTime: "20:10",
    arrivalTime: "21:35",
    gate: "D12",
    terminal: "4",
    status: "On Time",
    delayMinutes: null,
  },
];

export const getFlightDetails = async (flightNumber) => {
  try {
    // const result = await axios({
    //   method: "POST",
    //   url: `http://127.0.0.1:8000/api/openai/flight-details`,
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   data: {
    //     flight_number: flightNumber,
    //   },
    // });

    // return result.data;

    const flightRadarAPI = await axios({
      method: "GET",
      url: `https://aerodatabox.p.rapidapi.com/flights/number/${flightNumber}`,
      params: {
        withAircraftImage: false,
        withLocation: true,
        withFlightPlan: false,
      },
      headers: {
        "x-rapidapi-key": "",
        "x-rapidapi-host": "aerodatabox.p.rapidapi.com",
      },
    });

    const OpenAIFlight = OpenAIflights.find(
      (flight) => flight.flightNumber === flightNumber,
    );

    return {
      ...OpenAIFlight,
      ...flightRadarAPI.data[0],
    };
  } catch (error) {
    return error;
  }


};

export const getAirPortInformation = async (airportName) => {
  try {
    console.log("Calling airports API with name:", airportName);

    const result = await axios.get(
      "http://127.0.0.1:8000/api/openai/airports",
      {
        params: {
          airport_name: airportName, // MUST match FastAPI param name
        },
      }
    );

    console.log(`Airports API response for ${airportName}:`, result.data);
    return result.data;
  } catch (error) {
    console.error("Error calling airports API:", error);
    throw error;
  }
  // returns example response
  /*airpotrts: [{
  "iata": "PBN",
  "lon": "13.75",
  "iso": "AO",
  "status": 1,
  "name": "Porto Amboim Airport",
  "continent": "AF",
  "type": "airport",
  "lat": "-10.7",
  "size": "medium"
  }]
*/
};


export const getChatResponse = async (chatInput) => {
  try {
    console.log("Calling chat API with input:", chatInput);
    const result = await axios({
      method: "POST",
      url: `http://127.0.0.1:8000/api/openai/chat`,
      headers: {
        "Content-Type": "application/json",
      },
      data: {
        messages: [{"role": "user", "content": chatInput}],
      },
    });

    return result.data;
  } catch (error) {
    console.error("Error calling chat API:", error);
    throw error;
  }

};

export const getNearestFlights = async (from, to) => {
  try {
    // const result = await axios({
    //   method: "POST",
    //   url: `http://127.0.0.1:8000/api/openai/nearest-flights`,
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   data: {
    //     from: from,
    //     to: to,
    //   },
    // });
    // return result.data;
  } catch (error) {
    return error;
  }
};
