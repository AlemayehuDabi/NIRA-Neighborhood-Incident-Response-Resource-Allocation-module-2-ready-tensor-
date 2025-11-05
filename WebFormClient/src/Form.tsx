import { useState } from 'react';

type categoryEnum =
  | 'Fire'
  | 'Crime'
  | 'Medical'
  | 'Accident'
  | 'Flood'
  | 'Other';
type severityEnum = 'Critical' | 'High' | 'Medium' | 'Low';

interface IncidentForm {
  description: string;
  category: categoryEnum;
  severity: severityEnum;
  location: string;
  uploadedFile?: File;
}

export function IncidentReportForm() {
  const [incident, setIncident] = useState<IncidentForm>({
    description: '',
    category: 'Fire',
    severity: 'Critical',
    location: '',
  });

  const reportIncident = async () => {
    try {
      const res = await fetch('http://localhost:8000/submit_web_incident', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer your_auth_token_here',
        },
        body: JSON.stringify({}),
      });

      const data = await res.json();
      if (!res.ok) {
        console.log(data.message || 'Submit Incident failed');
      }
      console.log('form data', data);
    } catch (error) {
      console.log('form error', error);
    }
  };

  const handleChange = (e: any) => {
    setIncident({
      ...incident,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="flex items-center justify-center min-h-screen p-4">
      <div className="bg-white/70 backdrop-blur-lg shadow-2xl rounded-3xl p-10 w-full max-w-xl space-y-6 border border-white/40">
        <h2 className="text-3xl font-extrabold text-gray-800 text-center drop-shadow-sm">
          Report an Incident
        </h2>
        <p className="text-center text-gray-600 text-sm -mt-3 mb-4">
          Help us verify and respond quickly 🚨
        </p>

        <form className="space-y-5">
          <div>
            <label className="block text-gray-700 font-semibold mb-1">
              Description
            </label>
            <textarea
              className="w-full p-4 rounded-xl border border-gray-300 bg-white/60 focus:ring-2 focus:ring-blue-400 outline-none transition shadow-sm"
              rows={4}
              placeholder="Describe what happened..."
              required
              value={incident.description}
              onChange={handleChange}
              name="description"
            ></textarea>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-700 font-semibold mb-1">
                Category
              </label>
              <select
                className="w-full p-3 rounded-xl border bg-white border-gray-300 focus:ring-2 focus:ring-blue-400 outline-none shadow-sm"
                required
                onChange={handleChange}
                name="category"
              >
                <option>Fire</option>
                <option>Crime</option>
                <option>Medical</option>
                <option>Accident</option>
                <option>Flood</option>
                <option>Other</option>
              </select>
            </div>

            <div>
              <label className="block text-gray-700 font-semibold mb-1">
                Severity
              </label>
              <select
                className="w-full p-3 rounded-xl border bg-white border-gray-300 focus:ring-2 focus:ring-blue-400 outline-none shadow-sm"
                required
                onChange={handleChange}
                name="severity"
              >
                <option>Critical</option>
                <option>High</option>
                <option>Medium</option>
                <option>Low</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-gray-700 font-semibold mb-1">
              Location
            </label>
            <input
              className="w-full p-3 rounded-xl border bg-white/60 border-gray-300 focus:ring-2 focus:ring-blue-400 outline-none shadow-sm"
              placeholder="City, Street, Landmark"
              required
              onChange={handleChange}
              name="location"
            />
          </div>

          <div>
            <label className="block text-gray-700 font-semibold mb-1">
              Upload Image
            </label>
            <input
              type="file"
              className="w-full border rounded-xl p-3 bg-white border-gray-300 shadow-sm cursor-pointer"
              accept="image/*"
              onChange={handleChange}
              name="uploadedFile"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-linear-to-r from-blue-600 to-indigo-600 text-white font-bold p-3 rounded-xl hover:shadow-xl hover:scale-[1.02] transition-all"
            onClick={() => reportIncident()}
          >
            Submit Report
          </button>
        </form>
      </div>
    </div>
  );
}
