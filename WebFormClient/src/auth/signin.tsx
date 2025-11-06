import { useState } from 'react';

interface Login {
  email: string;
  password: string;
}

export const SignIn = () => {
  const [loginInfo, setLoginInfo] = useState<Login>({
    email: '',
    password: '',
  });

  const handleLogin = async (
    e: React.MouseEvent<HTMLButtonElement, MouseEvent>
  ) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer token_here`,
        },
        body: JSON.stringify({
          email: loginInfo.email,
          password: loginInfo.password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        console.log(data.message || data.detail || 'Login failed');
        alert('Error Login: ' + data.message || data.detail || 'Login Failed');
        return;
      }

      console.log('Login success:', data);
      alert('User Successfully Logined In!');
    } catch (error) {
      console.log('signin error', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLoginInfo((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0B0F19] px-4">
      <div className="w-full max-w-md bg-[#111827] rounded-xl p-8 shadow-2xl border border-[#1f2937]">
        <h2 className="text-2xl font-bold text-white mb-6 text-center">
          Sign In
        </h2>

        <form className="space-y-5">
          {/* Email */}
          <div>
            <label className="text-gray-300 text-sm">Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              className="w-full mt-1 px-4 py-3 bg-[#0d1320] border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-[#2D3EF7] focus:outline-none"
              onChange={(e) => handleChange(e)}
              required
            />
          </div>

          {/* Password */}
          <div>
            <label className="text-gray-300 text-sm">Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              className="w-full mt-1 px-4 py-3 bg-[#0d1320] border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-[#2D3EF7] focus:outline-none"
              onChange={(e) => handleChange(e)}
              required
            />
          </div>

          {/* Button */}
          <button
            type="submit"
            className="w-full bg-[#2D3EF7] hover:bg-[#1e2acb] transition text-white py-3 rounded-lg font-semibold"
            onClick={(e) => handleLogin(e)}
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
