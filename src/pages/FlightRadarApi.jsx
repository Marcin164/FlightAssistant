import SDK from '@flightradar24/fr24sdk'
const FlightRadarApi = async () => {
    const frApiToken = '';
    const client = new SDK.Client({apiToken: frApiToken});
//TODO ADD METHODS FOR FETHCING FLIGHTS AND AIRPORT DATA
    try {
        const summary = await client.flightSummary.getLight({
            flightIds: ['insert here']
        });

        const tracks = await client.flightTracks.get({
            flightId: ''
        });

        console.log(summary, tracks);
    } finally {
        client.close();
    }

}
export default FlightRadarApi