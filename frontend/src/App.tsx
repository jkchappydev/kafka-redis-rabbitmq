import { useEffect, useState } from 'react'
import './App.css'

export default function App() {
  const [status, setStatus] = useState('연결 확인 중…')
  useEffect(() => {
    const controller = new AbortController()
    fetch('/api/health', { signal: controller.signal })
      .then(async (response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const data: unknown = await response.json()
        if (!data || typeof data !== 'object' || !('status' in data) || data.status !== 'UP') {
          throw new Error('Unexpected response')
        }
        setStatus('Spring Boot 연결 완료')
      })
      .catch(() => {
        if (!controller.signal.aborted) setStatus('백엔드 연결 실패 — 서버 실행 후 새로고침하세요.')
      })
    return () => controller.abort()
  }, [])
  return (
    <main>
      <p>PROJECT STARTER</p>
      <h1>React + Spring Boot</h1>
      <p role="status">{status}</p>
    </main>
  )
}
