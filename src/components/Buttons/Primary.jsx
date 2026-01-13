import React from 'react'

const Primary = ({onClick, text}) => {
  return (
    <button className="bg-[#3F77D8] text-white px-4 py-2 rounded" onClick={onClick}>{text}</button>
  )
}

export default Primary