import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import Details from './pages/Details'
import Flights from './pages/Flights'
import Airport from './pages/Airport'
import Chat from "./pages/Chat.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/details" element={<Details/>}/>
        <Route path="/flights" element={<Flights/>}/>
        <Route path="/airport" element={<Airport/>}/>
        <Route path="/chat" element={<Chat/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
