import React from 'react'
import Primary from '../components/Buttons/Primary'
import Text from '../components/Inputs/Text'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowsLeftRight, faArrowsUpDown } from '@fortawesome/free-solid-svg-icons'
import { faClock } from '@fortawesome/free-regular-svg-icons'

const Details = () => {
  return (
    <div>
        <div className='flex py-2 px-4'>
            <div className='mr-4'>
                <div className="text-[#646464] text-[14px] font-light">Flight number</div>
                <div className="text-[#3F77D8] text-[30px] font-bold">FR 4897</div>
            </div>
            <div className='flex'>
                <Text placeholder="Flight number"/>
                <Primary text="Search" className="mt-4"/>
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
      A pretty CSS3 popup. <br /> Easily customizable.
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