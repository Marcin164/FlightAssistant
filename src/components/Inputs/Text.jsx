import React from 'react'

const Text = ({placeholder, onChange}) => {
  return (
    <input className="border border-[#3F77D8] rounded px-4 py-2 w-full" placeholder={placeholder} onChange={onChange}/>
  )
}

export default Text