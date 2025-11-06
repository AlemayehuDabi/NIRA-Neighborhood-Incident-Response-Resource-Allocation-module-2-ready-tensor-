import { useState } from 'react';

interface Login {
  name: string;
  email: string;
  password: string;
}

export const Register = () => {
  const [loginInfo, setLoginInfo] = useState<Login>({
    name: '',
    email: '',
    password: '',
  });

  const handleRegister = async (
    e: React.MouseEvent<HTMLButtonElement, MouseEvent>
  ) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer token_here`,
        },
        body: JSON.stringify({
          name: loginInfo.name,
          email: loginInfo.email,
          password: loginInfo.password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        console.log(data.message || data.detail || 'Register failed');
        alert(
          'Error Register: ' + data.message || data.detail || 'Register Failed'
        );
        return;
      }

      console.log('Register success:', data);
      alert('User Successfully Register In!');
    } catch (error) {
      console.log('register error', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLoginInfo((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md rounded-xl p-8 shadow-2xl">
        <h2 className="text-2xl font-bold mb-6 text-center">Sign Up</h2>

        <form className="space-y-5">
          {/* name */}
          <div>
            <label className="text-gray-600 text-sm">Name</label>
            <input
              type="name"
              placeholder="Enter your full name"
              className="w-full mt-1 px-4 py-3 border border-gray-700 rounded-lg focus:ring-2 focus:ring-[#2D3EF7] focus:outline-none"
              onChange={(e) => handleChange(e)}
              required
            />
          </div>
          {/* Email */}
          <div>
            <label className="text-gray-600 text-sm">Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              className="w-full mt-1 px-4 py-3 border border-gray-700 rounded-lg focus:ring-2 focus:ring-[#2D3EF7] focus:outline-none"
              onChange={(e) => handleChange(e)}
              required
            />
          </div>

          {/* Password */}
          <div>
            <label className="text-gray-600 text-sm">Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              className="w-full mt-1 px-4 py-3 border rounded-lg focus:ring-2 focus:ring-[#2D3EF7] focus:outline-none"
              onChange={(e) => handleChange(e)}
              required
            />
          </div>

          {/* Button */}
          <button
            type="submit"
            className="w-full bg-[#2D3EF7] hover:bg-[#1e2acb] transition text-white py-3 rounded-lg font-semibold"
            onClick={(e) => handleRegister(e)}
          >
            Sign In
          </button>
        </form>

        {/* Footer */}
        <p className="text-gray-400 text-sm mt-6 text-center">
          Don’t have an account?{' '}
          <a href="#" className="text-[#2D3EF7] hover:underline">
            Create one
          </a>
        </p>
      </div>
    </div>
  );
};
