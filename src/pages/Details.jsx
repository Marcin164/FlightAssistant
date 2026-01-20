import React, {useState} from 'react'
import Primary from '../components/Buttons/Primary'
import Text from '../components/Inputs/Text'
import {MapContainer, Marker, Popup, TileLayer} from 'react-leaflet'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faArrowsLeftRight, faArrowsUpDown} from '@fortawesome/free-solid-svg-icons'
import {faClock} from '@fortawesome/free-regular-svg-icons'
import OpenAI from "openai";
import {useParams} from 'react-router'

const client = new OpenAI({
    apiKey: '', // Vite
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

const flightRadarApiDesc = [{
    type: "function",
    name: "get_flight_detials_from_flight_radar",
    description: "Pobiera dane z serwisu flightradar24. Pozwla pobrac informacje o aktualnych lotach " +
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
                description: "Typ tabeli (np. 'A', 'B')."
            },
            date: {
                type: "string",
                description: "Data w formacie 'YYYY-MM-DD'."
            }
        },
        required: ["table_type", "date"]
    }
}]

const Details = () => {
    const params = useParams()
    const [flight, setFlight] = useState("FR 99");
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);

    const findFlightDetails = async () => {
        setLoading(true);
        setData(null);

        const response = await client.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [
                {role: "system", content: SYSTEM_PROMPT},
                {role: "user", content: flight},
            ],
            tools: flightRadarApiDesc
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
            <div className='flex py-2 px-4'>
                <div className='mr-4'>
                    <div className="text-[#646464] text-[14px] font-light">Flight number</div>
                    <div className="text-[#3F77D8] text-[30px] font-bold">FR 4897</div>
                </div>
                <div className='flex'>
                    <Text placeholder="Flight number" onChange={(e) => setFlight(e.target.value)}/>
                    <Primary text="Search" className="mt-4" onClick={findFlightDetails}/>
                </div>
            </div>
            <div className='flex'>
                <div className="w-[50%]">
                    <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={false}>
                        <TileLayer
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        />
                        <Marker position={[51.505, -0.09]}>
                            <Popup>
                                A pretty CSS3 popup. <br/> Easily customizable.
                            </Popup>
                        </Marker>
                    </MapContainer>
                </div>
                <div className="w-[50%]">
                    <div className="shadow-xl bg-[#FAFAFA] p-4">
                        <div className="text-[26px] font-bold">Travel details</div>
                        <div className="flex flex-col gap-2 mt-2">
                            <span><FontAwesomeIcon icon={faArrowsUpDown}/><span className="ml-2">30000 ft.</span></span>
                            <span><FontAwesomeIcon icon={faArrowsLeftRight}/><span className="ml-2">114 km</span></span>
                            <span><FontAwesomeIcon icon={faClock}/><span className="ml-2">0:45</span></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Details