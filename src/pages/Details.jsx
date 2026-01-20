import React, { useEffect, useState } from "react";
import Primary from "../components/Buttons/Primary";
import Text from "../components/Inputs/Text";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faArrowsLeftRight,
  faArrowsUpDown,
} from "@fortawesome/free-solid-svg-icons";
import { faClock } from "@fortawesome/free-regular-svg-icons";
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
    });

    try {
      const json = JSON.parse(response.choices[0].message.content);

      setData(json);
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
