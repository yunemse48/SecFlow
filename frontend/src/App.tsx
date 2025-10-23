import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Shield } from 'lucide-react'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  )
}

function LandingPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="text-center">
        <div className="flex justify-center mb-6">
          <Shield className="w-20 h-20 text-indigo-600" />
        </div>
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          AppSec Management Dashboard
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          API-first Application Security Orchestration Platform
        </p>
        <div className="space-y-4">
          <div className="bg-white rounded-lg shadow-md p-6 max-w-2xl mx-auto">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              🚀 Project Setup Complete!
            </h2>
            <div className="text-left space-y-2 text-gray-700">
              <p>✅ Django backend configured</p>
              <p>✅ React frontend initialized</p>
              <p>✅ Docker setup ready</p>
              <p>✅ Plugin system architecture in place</p>
              <p>✅ All Django apps created</p>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 max-w-2xl mx-auto">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Next Steps:
            </h3>
            <ol className="text-left list-decimal list-inside space-y-1 text-gray-700">
              <li>Set up your environment variables</li>
              <li>Run migrations: <code className="bg-gray-100 px-2 py-1 rounded">python manage.py migrate</code></li>
              <li>Create a superuser: <code className="bg-gray-100 px-2 py-1 rounded">python manage.py createsuperuser</code></li>
              <li>Start building your features!</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
