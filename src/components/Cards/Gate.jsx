import React from "react";

const Gate = ({ gate, departureTime, terminal }) => {
  return (
    <div className="w-[100%] h-[100%]">
      <div className="shadow-xl rounded-[10px] bg-[#FAFAFA] p-4">
        <div className="text-[26px] font-bold text-[#646464]">
          Departure Airport
        </div>
        <div>
          <span className="font-light">Terminal: </span>
          <span className="font-bold text-[#646464]">{terminal}</span>
        </div>
        <div>
          <span className="font-light">Gate: </span>
          <span className="font-bold text-[#646464]">{gate}</span>
        </div>
        <div>
          <span className="font-light">Boarding: </span>
          <span className="font-bold text-[#646464]">{departureTime - 30}</span>
        </div>
      </div>
    </div>
  );
};

export default Gate;
