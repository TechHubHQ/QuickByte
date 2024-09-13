import React, { useState } from "react";
import { motion } from "framer-motion";
import signupIllustration from "../assets/signupIllustration.svg";
import { Mail, Lock, User, MapPin } from "lucide-react";
import { Link } from "react-router-dom"; // Import Link from react-router-dom if you use React Router

const SignUpPage: React.FC = () => {
  const [passwordStrength, setPasswordStrength] = useState("");

  const checkPasswordStrength = (password: string) => {
    const strongPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    const mediumPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{6,}$/;

    if (strongPassword.test(password)) {
      setPasswordStrength("Strong");
    } else if (mediumPassword.test(password)) {
      setPasswordStrength("Medium");
    } else {
      setPasswordStrength("Weak");
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
          {/* Sign Up Section */}
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
                    src={signupIllustration}
                    alt="Sign Up Illustration"
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
                    Create Your Account
                  </motion.h2>
                  <motion.p
                    className="text-xl mb-6"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.6 }}
                  >
                    Sign up to get started and enjoy our services.
                  </motion.p>
                  <motion.form
                    className="space-y-4"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.8 }}
                  >
                    <div className="grid grid-cols-2 gap-4">
                      <motion.div
                        className="relative"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.4, delay: 1 }}
                      >
                        <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-orange-500" />
                        <input
                          type="text"
                          placeholder="First Name"
                          className="w-full py-3 pl-12 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                        />
                      </motion.div>
                      <motion.div
                        className="relative"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.4, delay: 1.2 }}
                      >
                        <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-orange-500" />
                        <input
                          type="text"
                          placeholder="Last Name"
                          className="w-full py-3 pl-12 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                        />
                      </motion.div>
                    </div>
                    <motion.div
                      className="relative"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.4, delay: 1.4 }}
                    >
                      <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-orange-500" />
                      <input
                        type="email"
                        placeholder="Email"
                        className="w-full py-3 pl-12 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                      />
                    </motion.div>
                    <motion.div
                      className="relative"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.4, delay: 1.6 }}
                    >
                      <Lock className="absolute left-3 top-1/3 transform -translate-y-1/2 text-orange-500" />
                      <input
                        type="password"
                        placeholder="Password"
                        className="w-full py-3 pl-12 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                        onChange={(e) => checkPasswordStrength(e.target.value)}
                      />
                      <div className="text-sm mt-1 text-white">
                        Password Strength: {passwordStrength}
                      </div>
                    </motion.div>
                    <motion.div
                      className="relative"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.4, delay: 1.8 }}
                    >
                      <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-orange-500" />
                      <input
                        type="text"
                        placeholder="Street Address"
                        className="w-full py-3 pl-12 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                      />
                    </motion.div>
                    <div className="grid grid-cols-3 gap-4">
                      <motion.div
                        className="relative"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.4, delay: 2 }}
                      >
                        <input
                          type="text"
                          placeholder="City"
                          className="w-full py-3 pl-4 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                        />
                      </motion.div>
                      <motion.div
                        className="relative"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.4, delay: 2.2 }}
                      >
                        <input
                          type="text"
                          placeholder="State"
                          className="w-full py-3 pl-4 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                        />
                      </motion.div>
                      <motion.div
                        className="relative"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.4, delay: 2.4 }}
                      >
                        <input
                          type="text"
                          placeholder="Zip Code"
                          className="w-full py-3 pl-4 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                        />
                      </motion.div>
                    </div>
                    <motion.button
                      className="bg-white text-orange-600 font-bold py-3 px-6 rounded-lg w-full hover:bg-orange-50 transition duration-300"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      Sign Up
                    </motion.button>
                  </motion.form>
                  <motion.div
                    className="mt-4 text-center"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 2.6 }}
                  >
                    <p className="text-white text-sm">
                      Already have an account?{" "}
                      <Link to="/login" className="text-orange-200 hover:underline">
                        Log In
                      </Link>
                    </p>
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

export default SignUpPage;
