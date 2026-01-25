import React from "react";

const Delays = ({ delayTime, delayReason }) => {
  return (
    <div className="w-[100%]">
      <div className="shadow-xl rounded-[10px] bg-[#FAFAFA] p-4">
        <div className="text-[26px] font-bold text-[#646464]">Delays</div>
        <div className="text-[#646464]">
          {!delayTime ? "No delays" : `Plane delayed for ${delayTime} minutes`}
        </div>
        <div className="font-bold text-[#646464]">{delayReason}</div>
      </div>
    </div>
  );
};

export default Delays;
