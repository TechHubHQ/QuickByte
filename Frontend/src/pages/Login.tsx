import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import loginIllustration from "../assets/loginIllustration.svg";
import { Lock, User } from "lucide-react";
import { signIn } from "../../services/apiRequestMaker";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleSignIn = async (event: React.FormEvent) => {
    event.preventDefault();
    setErrorMessage("");

    try {
      const signInData = { username, password };
      const response = await signIn(signInData);

      console.log("Sign-in successful:", response);

      navigate("/home");
    } catch (error) {
      console.error("Sign-in failed:", error);
      setErrorMessage("Invalid username or password. Please try again.");
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      <main className="flex-grow w-full px-4 mb-8 mt-8">
        <motion.div
          className="max-w-4xl mx-auto rounded-2xl shadow-[0_0_20px_rgba(0,0,0,0.2)] overflow-hidden bg-gradient-to-r from-orange-500 to-red-600 text-white py-20"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          {/* Login Section */}
          <section>
            <div className="container mx-auto px-4">
              <div className="flex flex-col md:flex-row items-center">
                <motion.div
                  className="md:w-1/2 mb-10 md:mb-0 flex justify-center"
                  initial={{ opacity: 0, x: -50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                >
                  <img
                    src={loginIllustration}
                    alt="Login Illustration"
                    className="rounded-lg shadow-2xl w-3/4"
                  />
                </motion.div>

                {/* Form Section */}
                <motion.div
                  className="md:w-1/2"
                  initial={{ opacity: 0, x: 50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                >
                  <motion.h2
                    className="text-4xl font-bold mb-6"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.4 }}
                  >
                    Welcome Back!
                  </motion.h2>
                  <motion.p
                    className="text-xl mb-6"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.6 }}
                  >
                    Log in to access your account and enjoy our services.
                  </motion.p>

                  {errorMessage && (
                    <motion.p
                      className="text-500 mb-4"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                    >
                      {errorMessage}
                    </motion.p>
                  )}

                  <motion.form
                    className="space-y-4"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.8 }}
                    onSubmit={handleSignIn}
                  >
                    <motion.div
                      className="relative"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.4, delay: 1 }}
                    >
                      <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-orange-500" />
                      <input
                        type="text"
                        placeholder="Username"
                        className="w-full py-3 pl-12 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                      />
                    </motion.div>

                    <motion.div
                      className="relative"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.4, delay: 1.2 }}
                    >
                      <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-orange-500" />
                      <input
                        type="password"
                        placeholder="Password"
                        className="w-full py-3 pl-12 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                      />
                    </motion.div>

                    <motion.button
                      className="bg-white text-orange-600 font-bold py-3 px-6 rounded-lg w-full hover:bg-orange-50 transition duration-300"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      type="submit"
                    >
                      Log In
                    </motion.button>
                  </motion.form>

                  {/* Forgot Password and Sign Up Links */}
                  <motion.div
                    className="mt-4 flex justify-between text-sm"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 1.4 }}
                  >
                    <Link
                      to="/forgot-password"
                      className="text-white hover:underline"
                    >
                      Forgot Password?
                    </Link>
                    <Link to="/signup" className="text-white hover:underline">
                      Sign Up
                    </Link>
                  </motion.div>
                </motion.div>
              </div>
            </div>
          </section>
        </motion.div>
      </main>
    </div>
  );
};

export default LoginPage;
