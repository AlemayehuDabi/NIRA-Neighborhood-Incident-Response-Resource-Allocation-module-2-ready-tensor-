import type { ReportMessage } from '../../Form';

interface ModalProps {
  data: ReportMessage;
  isOpen: boolean;
  onClose: () => void;
}

export const ReportModal = ({ data, isOpen, onClose }: ModalProps) => {
  if (!isOpen) return null;

  const token = localStorage.getItem('token');

  return (
    <div className="fixed inset-0 bg-black/30 flex justify-center items-center z-50">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 relative">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-blue-500 font-bold text-xl hover:text-blue-700"
        >
          &times;
        </button>

        <h2 className="text-2xl font-bold text-center text-blue-600 mb-4">
          Incident Report
        </h2>

        <div className="space-y-3">
          <div>
            <label className="block font-semibold text-gray-700">
              Report Id
            </label>
            <p className="bg-blue-50 rounded-lg p-3 text-gray-800">
              {data.report_id}
            </p>
          </div>

          <div>
            <label className="block font-semibold text-gray-700">Message</label>
            <p className="bg-blue-50 rounded-lg p-3 text-gray-800">
              {data.message}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold text-gray-700">
                Recieved Message Type
              </label>
              <p className="bg-blue-50 rounded-lg p-3 text-gray-800">
                {data.recevied_message}
              </p>
            </div>
          </div>

          <div>
            <label className="block font-semibold text-gray-700">Status</label>
            <p className="bg-blue-50 rounded-lg p-3 text-gray-800">
              {data.status}
            </p>
          </div>
        </div>

        <div className="mt-6 text-center space-y-4">
          <button
            onClick={onClose}
            className="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition"
          >
            Close
          </button>
          {!token && (
            <div className="w-full border-2 border-red-600 bg-red-300 py-1">
              <div className="flex justify-center items-center">
                <p>
                  If you want to track the progress of the incident{' '}
                  <a
                    href="/login"
                    className="text-gray-700 hover:border-b-2 hover:border-red-500 hover:text-gray-500"
                  >
                    sign in
                  </a>{' '}
                  and submit the incident again
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
