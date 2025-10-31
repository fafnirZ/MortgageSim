import { Routes } from 'react-router'
import './App.css'
import { BrowserRouter } from 'react-router'
import { Route } from 'react-router'
import { HomePage } from './pages/Homepage'

function App() {

  return (
    <>
      <BrowserRouter>
        <Routes>
         <Route path="/" element={<HomePage/>}/> 
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
