import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import Converter from './pages/Converter'
import History from './pages/History'

function App() {
  return (
    <Router>
      <div className="flex flex-col h-screen overflow-hidden">
        <Header />
        <main className="flex-grow overflow-auto">
          <Routes>
            <Route path="/" element={<Converter />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App
