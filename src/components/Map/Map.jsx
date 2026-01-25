import React from "react";
import { MapContainer, Marker, TileLayer } from "react-leaflet";
import L from "leaflet";

const Map = ({
  planeCoordinates,
  arrivalCoordinates,
  departureCoordinates,
}) => {
  const customIcon = L.icon({
    iconUrl: "/plane.png",
    iconSize: [40, 40],
    iconAnchor: [20, 40],
  });

  return (
    <MapContainer
      center={[
        planeCoordinates?.lat || arrivalCoordinates?.lat,
        planeCoordinates?.lon || arrivalCoordinates?.lon,
      ]}
      zoom={10}
      scrollWheelZoom={true}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {/* Plane position marker */}
      <Marker
        position={[
          planeCoordinates?.lat || arrivalCoordinates?.lat,
          planeCoordinates?.lon || arrivalCoordinates?.lon,
        ]}
        icon={customIcon}
      />

      {/* Arrival airport marker */}
      <Marker position={[arrivalCoordinates?.lat, arrivalCoordinates?.lon]} />

      {/* Departure airport marker */}
      <Marker
        position={[departureCoordinates?.lat, departureCoordinates?.lon]}
      />
    </MapContainer>
  );
};

export default Map;
