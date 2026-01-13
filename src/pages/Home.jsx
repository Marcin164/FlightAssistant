import React from 'react'
import Text from '../components/Inputs/Text'
import Primary from '../components/Buttons/Primary'

const Home = () => {
  return (
    <div>
        <div className="p-2 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <div className="text-[#646464] text-[24px] font-light">Hey, I am your flight assistant</div>
            <div className="text-[#3F77D8] text-[30px] font-bold">Tell me your flight and I will find everything important</div>
            <div className="my-8 w-full">
                <Text placeholder="Enter flight number"/>
            </div>
            <div className="text-[#646464] text-[24px] font-light">OR</div>
            <div className="my-8 space-y-2 space-x-2">
                <Text placeholder="Arrival time"/>
                <Text placeholder="Departure time"/>
                <Text placeholder="Arrival airport"/>
                <Text placeholder="Departure airport"/>
            </div>
            <Primary text="Search" className="mt-4"/>
        </div>
    </div>
  )
}

export default Home