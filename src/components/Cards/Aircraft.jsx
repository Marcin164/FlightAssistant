import React from "react";

const Aircarft = ({ company = "M/A", model = "N/A", reg = "N/A" }) => {
  return (
    <div className="w-[100%]">
      <div className="shadow-xl rounded-[10px] bg-[#FAFAFA] p-4">
        <div className="text-[26px] font-bold text-[#646464]">Aircraft</div>
        <div>
          <span className="font-light">Company: </span>
          <span className="font-bold text-[#646464]">{company}</span>
        </div>
        <div>
          <span className="font-light">Model: </span>
          <span className="font-bold text-[#646464]">{model}</span>
        </div>
        <div>
          <span className="font-light">Registration: </span>
          <span className="font-bold text-[#646464]">{reg}</span>
        </div>
      </div>
    </div>
  );
};

export default Aircarft;
