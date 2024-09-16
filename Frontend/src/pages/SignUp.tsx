import React, { useState } from "react";
import { motion } from "framer-motion";
import signupIllustration from "../assets/signupIllustration.svg";
import { Mail, Lock, User, MapPin, Phone } from "lucide-react";
import { Link } from "react-router-dom";
import { signUp } from "../../services/apiRequestMaker";
import { SignUpFormData } from "../../types/formTypes";

const SignUpPage: React.FC = () => {
  const [formData, setFormData] = useState<SignUpFormData>({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    phone: "",
    street: "",
    city: "",
    state: "",
    zip_code: "",
  });

  const [passwordStrength, setPasswordStrength] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const result = await signUp(formData);
      console.log("Sign up successful:", result);
    } catch (error) {
      setError("Failed to sign up. Please try again.");
    }
  };

  const checkPasswordStrength = (password: string) => {
    const strongPassword =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    const mediumPassword =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{6,}$/;

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
                    onSubmit={handleSubmit}
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
                          name="first_name"
                          placeholder="First Name"
                          value={formData.first_name}
                          onChange={handleChange}
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
                          name="last_name"
                          placeholder="Last Name"
                          value={formData.last_name}
                          onChange={handleChange}
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
                        name="email"
                        placeholder="Email"
                        value={formData.email}
                        onChange={handleChange}
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
                        name="password"
                        placeholder="Password"
                        value={formData.password}
                        onChange={(e) => {
                          handleChange(e);
                          checkPasswordStrength(e.target.value);
                        }}
                        className="w-full py-3 pl-12 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
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
                      <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-orange-500" />
                      <input
                        type="tel"
                        name="phone"
                        placeholder="Phone Number"
                        value={formData.phone}
                        onChange={handleChange}
                        className="w-full py-3 pl-12 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                      />
                    </motion.div>
                    <motion.div
                      className="relative"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.4, delay: 2 }}
                    >
                      <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-orange-500" />
                      <input
                        type="text"
                        name="street"
                        placeholder="Street Address"
                        value={formData.street}
                        onChange={handleChange}
                        className="w-full py-3 pl-12 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                      />
                    </motion.div>
                    <div className="grid grid-cols-3 gap-4">
                      <motion.div
                        className="relative"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.4, delay: 2.2 }}
                      >
                        <input
                          type="text"
                          name="city"
                          placeholder="City"
                          value={formData.city}
                          onChange={handleChange}
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
                          name="state"
                          placeholder="State"
                          value={formData.state}
                          onChange={handleChange}
                          className="w-full py-3 pl-4 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                        />
                      </motion.div>
                      <motion.div
                        className="relative"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.4, delay: 2.6 }}
                      >
                        <input
                          type="text"
                          name="zip_code"
                          placeholder="Zip Code"
                          value={formData.zip_code}
                          onChange={handleChange}
                          className="w-full py-3 pl-4 pr-4 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white/90"
                        />
                      </motion.div>
                    </div>
                    {error && (
                      <motion.div
                        className="text-red-500 text-sm mt-2"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.4 }}
                      >
                        {error}
                      </motion.div>
                    )}
                    <motion.button
                      type="submit"
                      className="w-full py-3 mt-6 rounded-lg bg-orange-600 hover:bg-orange-700 text-white font-bold transition duration-300"
                      whileHover={{ scale: 1.05 }}
                    >
                      Sign Up
                    </motion.button>
                  </motion.form>
                  <motion.p
                    className="text-sm mt-4"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 1 }}
                  >
                    Already have an account?{" "}
                    <Link
                      to="/login"
                      className="text-white hover:underline"
                    >
                      Log in here
                    </Link>
                  </motion.p>
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