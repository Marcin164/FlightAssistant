import React from "react";
import { twMerge } from "tailwind-merge";

const Text = ({ placeholder, onChange, className }) => {
  return (
    <input
      className={twMerge(
        `border border-[#3F77D8] rounded px-4 py-2 w-full`,
        className,
      )}
      placeholder={placeholder}
      onChange={onChange}
    />
  );
};

export default Text;
