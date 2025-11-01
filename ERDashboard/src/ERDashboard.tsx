import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { motion } from 'framer-motion';

// ✅ Type-safe incident
export interface Incident {
  id: string;
  description: string;
  category: string;
  severity: string;
  location: string;
  latitude: number;
  longitude: number;
  timestamp: string;
}

const socketUrl = import.meta.env.VITE_SOCKET_URL || 'http://localhost:5000';
let socket: Socket;

export default function App() {
  const [incidents, setIncidents] = useState<Incident[]>([]);

  useEffect(() => {
    socket = io(socketUrl);

    socket.on('connect', () => {
      console.log('✅ Connected to incident socket server');
    });

    socket.on('new_incident', (data: Incident) => {
      console.log('🚨 New incident received', data);
      setIncidents((prev) => [data, ...prev]);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const dispatchResponder = (id: string) => {
    socket.emit('dispatch_responder', { incidentId: id });
    alert(`🚑 Responder dispatched for incident ${id}`);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6">Emergency Response Admin</h1>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {incidents.map((incident) => (
          <motion.div
            key={incident.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gray-800 rounded-xl p-5 space-y-2 border border-gray-700 shadow-lg"
          >
            <h2 className="text-xl font-semibold">{incident.category}</h2>
            <p className="text-gray-300 text-sm">{incident.description}</p>
            <p className="text-sm">📍 {incident.location}</p>
            <p className="text-sm">⚠️ Severity: {incident.severity}</p>
            <p className="text-xs text-gray-400">🕒 {incident.timestamp}</p>

            <button
              onClick={() => dispatchResponder(incident.id)}
              className="mt-3 w-full bg-red-500 hover:bg-red-600 transition text-white px-4 py-2 rounded-lg font-semibold"
            >
              Dispatch Responder
            </button>
          </motion.div>
        ))}
      </div>

      {incidents.length === 0 && (
        <p className="text-gray-400 mt-10 text-center">No incidents yet...</p>
      )}
    </div>
  );
}
