import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

console.log('🚀 main.jsx is loading')
console.log('📦 React:', React)
console.log('📦 ReactDOM:', ReactDOM)
console.log('📦 App:', App)

const rootElement = document.getElementById('root')
console.log('🎯 Root element:', rootElement)

if (rootElement) {
  console.log('✅ Root element found, creating React root')
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  )
  console.log('✅ React render called')
} else {
  console.error('❌ Root element not found!')
}
