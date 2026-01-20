import React, { useState } from "react";
import OpenAI from "openai";
import { useParams } from "react-router";
import DetailsTopbar from "../components/Topbars/DetailsTopbar";
import TravelDetails from "../components/Cards/TravelDetails";
import Map from "../components/Map/Map";
import PlaneState from "../components/Cards/PlaneState";
import Delays from "../components/Cards/Delays";
import Gate from "../components/Cards/Gate";

const client = new OpenAI({
  apiKey: "", // Vite
  dangerouslyAllowBrowser: true, // ⚠️ wymagane w przeglądarce
});

const SYSTEM_PROMPT = `
Jesteś systemem informacji lotniskowej.

Użytkownik podaje numer lotu (np. "LO123", "FR4567").
Twoim zadaniem jest zwrócić szczegółowe informacje o locie.

ZASADY:
- Jeśli numer lotu wygląda poprawnie, ZAWSZE zwróć dane
- Dane mogą być symulowane, ale muszą być realistyczne
- Odpowiadaj WYŁĄCZNIE w formacie JSON
- Nie dodawaj żadnego tekstu poza JSON

TODO CHANGE HERE RESPONSE AND ENABLE MODEL TO CALL API
FORMAT JSON:
{
  "flightNumber": string,
  "airline": string,
  "from": string,
  "to": string,
  "departureTime": string,
  "arrivalTime": string,
  "gate": string,
  "terminal": string,
  "status": "On Time" | "Delayed" | "Boarding" | "Cancelled",
  "delayMinutes": number | null
}
`;

const flightRadarApiDesc = [
  {
    type: "function",
    name: "get_flight_detials_from_flight_radar",
    description:
      "Pobiera dane z serwisu flightradar24. Pozwla pobrac informacje o aktualnych lotach " +
      "TODO HERE OTHER METHODS CALLS " +
      "Args: table_type (str): " +
      "Typ tabeli (np. 'A', 'B'). " +
      "date (str): Data w formacie 'YYYY-MM-DD'." +
      " Returns: dict or None: Słownik z danymi o kursach walut lub None w przypadku błędu.",
    strict: false,
    parameters: {
      type: "object",
      properties: {
        table_type: {
          type: "string",
          description: "Typ tabeli (np. 'A', 'B').",
        },
        date: {
          type: "string",
          description: "Data w formacie 'YYYY-MM-DD'.",
        },
      },
      required: ["table_type", "date"],
    },
  },
];

const Details = () => {
  const params = useParams();
  const [flight, setFlight] = useState("FR 99");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const findFlightDetails = async () => {
    setLoading(true);
    setData(null);

    const response = await client.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user", content: flight },
      ],
      tools: flightRadarApiDesc,
    });

    try {
      //TODO add call to FlightRADARaPI
      console.log(response);
      const json = JSON.parse(response.choices[0].message.content);

      console.log(json);
      setData(json);
      console.log(data);
      //TODO ADD A WAY TO DISPLAY DATA TO USER
    } catch (e) {
      alert("Błąd parsowania odpowiedzi AI");
    }

    setLoading(false);
  };

  return (
    <div>
      <DetailsTopbar
        flight={flight}
        setFlight={setFlight}
        findFlightDetails={findFlightDetails}
      />
      <div className="flex">
        <div className="w-[50%] h-[calc(100vh-50px)] p-4">
          <Map />
        </div>
        <div className="w-[50%] p-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-4">
              <TravelDetails />
              <Delays />
            </div>
            <div className="flex flex-col gap-4">
              <PlaneState />
              <Gate />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Details;
