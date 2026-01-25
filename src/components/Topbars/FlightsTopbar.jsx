import React from "react";

const FlightsTopbar = ({ from = "", to = "" }) => {
  return (
    <div className="h-[50px] flex items-center px-4">
      <div className="text-[22px] text-[#646464]">
        Search different flights from:{" "}
        <span className="text-[#3F77D8] font-bold">{from}</span> to{" "}
        <span className="text-[#3F77D8] font-bold">{to}</span>
      </div>
    </div>
  );
};

export default FlightsTopbar;
