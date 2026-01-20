import React from "react";

const Gate = () => {
  return (
    <div className="w-[100%] h-[100%]">
      <div className="shadow-xl rounded-[10px] bg-[#FAFAFA] p-4">
        <div className="text-[26px] font-bold text-[#646464]">Gate</div>
        <div className="flex flex-col gap-2 mt-2">
          <span>
            <span className="font-light">Terminal: </span>
            <span className="font-bold text-[#646464]">1</span>
          </span>
          <span>
            <span className="font-light">Gate: </span>
            <span className="font-bold text-[#646464]">46</span>
          </span>
          <span>
            <span className="font-light">Boarding: </span>
            <span className="font-bold text-[#646464]">18:45</span>
          </span>
        </div>
      </div>
    </div>
  );
};

export default Gate;
