import axios from "axios";

export const getFlightDetails = async (flightNumber) => {
  console.log(flightNumber);
  try {
    const result = await axios({
      method: "POST",
      url: `http://127.0.0.1:8000/api/openai/flight-details`,
      headers: {
        "Content-Type": "application/json",
      },
      data: {
        flight_number: flightNumber,
      },
    });

    return result.data;
  } catch (error) {
    return error;
  }
};
