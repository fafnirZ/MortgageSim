import { Routes } from 'react-router'
import './App.css'
import { BrowserRouter } from 'react-router'
import { Route } from 'react-router'
import { AppPage } from './pages/AppPage'

function App() {

  return (
    <>
      <BrowserRouter>
        <Routes>
         <Route path="/" element={<AppPage/>}/> 
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
