import React from "react";

const Primary = ({ onClick, text, className = "" }) => {
  return (
    <button
      className={`bg-[#3F77D8] text-white px-4 rounded ${className}`}
      onClick={onClick}
    >
      {text}
    </button>
  );
};

export default Primary;
