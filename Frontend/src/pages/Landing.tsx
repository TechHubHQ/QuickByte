import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import Header from "../components/Header";
import Footer from "../components/Footer";
import deliveryImg from "../assets/delivery-boy.png";
import { DishCard, FeatureCard } from "../components/Cards";
import {
  ArrowRight,
  Clock,
  Utensils,
  Truck,
  Shield,
  CreditCard,
  HeartHandshake,
  ArrowRightCircle,
} from "lucide-react";

const images = import.meta.glob("../assets/img/*.png");

const LandingPage: React.FC = () => {
  const [loadedImages, setLoadedImages] = useState<{ [key: string]: string }>(
    {}
  );

  useEffect(() => {
    const loadImages = async () => {
      const entries = Object.entries(images);
      const loaded = await Promise.all(
        entries.map(async ([key, importFn]) => {
          const module = (await importFn()) as { default: string };
          return [
            key.replace("../assets/img/", "").replace(".png", ""),
            module.default,
          ] as [string, string];
        })
      );

      setLoadedImages(Object.fromEntries(loaded));
    };

    loadImages();
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow w-full px-4 mb-8 mt-8">
        <div className="max-w-7xl mx-auto rounded-2xl shadow-[0_0_20px_rgba(0,0,0,0.2)] overflow-hidden bg-gradient-to-r from-orange-500 to-red-600 text-white py-20">
          {/* Hero Section */}
          <section>
            <div className="container mx-auto px-4">
              <div className="flex flex-col md:flex-row items-center">
                <motion.div
                  className="md:w-1/2 mb-10 md:mb-0"
                  initial={{ opacity: 0, y: -50 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8 }}
                >
                  <motion.h1
                    className="text-4xl md:text-6xl font-bold mb-4"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2, duration: 0.6 }}
                  >
                    Delicious Food, Delivered Fast
                  </motion.h1>
                  <motion.p
                    className="text-xl mb-6"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4, duration: 0.6 }}
                  >
                    Experience the best cuisines from the comfort of your home.
                  </motion.p>
                  <motion.div
                    className="flex justify-start"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6, duration: 0.6 }}
                  >
                    <Link
                      to="/login"
                      className="bg-white text-teal-600 font-bold py-2 px-6 rounded-full inline-flex items-center hover:bg-teal-50 transition duration-300"
                    >
                      Order Now <ArrowRight className="ml-2" />
                    </Link>
                  </motion.div>
                </motion.div>
                <motion.div
                  className="md:w-1/2"
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8 }}
                >
                  <img
                    src={deliveryImg}
                    alt="Delicious food spread"
                    className="rounded-lg shadow-2xl"
                  />
                </motion.div>
              </div>
            </div>
          </section>

          {/* Features Section */}
          <section className="py-20">
            <div className="container mx-auto px-4">
              <motion.h2
                className="text-4xl font-bold text-center mb-12 text-gray-800"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                Why Choose QuickByte?
              </motion.h2>
              <motion.div
                className="grid grid-cols-1 md:grid-cols-3 gap-8"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2, duration: 0.6 }}
              >
                <FeatureCard
                  icon={<Clock className="w-12 h-12 text-teal-500" />}
                  title="Lightning-Fast Delivery"
                  description="Experience the thrill of our 30-minute delivery guarantee or your next order is on us!"
                />
                <FeatureCard
                  icon={<Utensils className="w-12 h-12 text-teal-500" />}
                  title="Culinary Adventure"
                  description="Embark on a gastronomic journey with our curated selection of 1000+ local and international cuisines."
                />
                <FeatureCard
                  icon={<Truck className="w-12 h-12 text-teal-500" />}
                  title="Real-Time Tracking"
                  description="Watch your order's journey in real-time with our state-of-the-art GPS tracking system."
                />
                <FeatureCard
                  icon={<Shield className="w-12 h-12 text-teal-500" />}
                  title="Safety First"
                  description="Rest easy with our contactless delivery and stringent food safety protocols."
                />
                <FeatureCard
                  icon={<CreditCard className="w-12 h-12 text-teal-500" />}
                  title="Exclusive Deals"
                  description="Enjoy daily promotions and loyalty rewards that make every order a steal!"
                />
                <FeatureCard
                  icon={<HeartHandshake className="w-12 h-12 text-teal-500" />}
                  title="Community Impact"
                  description="Every order contributes to our local food bank initiative, feeding those in need."
                />
              </motion.div>
            </div>
          </section>

          {/* Popular Dishes Section */}
          <section className="py-20">
            <div className="container mx-auto px-4">
              <motion.h2
                className="text-4xl font-bold text-center mb-12 text-gray-800"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                Explore our Culinary Delights
              </motion.h2>
              <motion.div
                className="relative overflow-hidden"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2, duration: 0.6 }}
              >
                <div className="flex overflow-x-auto pb-8 hide-scrollbar">
                  <div className="flex space-x-6">
                    <DishCard
                      name="Chicken Biryani"
                      image={loadedImages.Biryani}
                      rating={4.5}
                      className="w-80 flex-shrink-0"
                    />
                    <DishCard
                      name="Chicken Cheese Pizza"
                      image={loadedImages.Pizza}
                      rating={4.7}
                      className="w-80 flex-shrink-0"
                    />
                    <DishCard
                      name="Chicken Burger"
                      image={loadedImages.Burger}
                      rating={4.6}
                      className="w-80 flex-shrink-0"
                    />
                    <DishCard
                      name="Shawarma"
                      image={loadedImages.Shawarma}
                      rating={4.4}
                      className="w-80 flex-shrink-0"
                    />
                    <DishCard
                      name="Chocolate Cake"
                      image={loadedImages.Cake}
                      rating={4.8}
                      className="w-80 flex-shrink-0"
                    />
                    <DishCard
                      name="Samosa"
                      image={loadedImages.Samosa}
                      rating={4.5}
                      className="w-80 flex-shrink-0"
                    />
                    <DishCard
                      name="Dosa"
                      image={loadedImages.Dosa}
                      rating={4.6}
                      className="w-80 flex-shrink-0"
                    />
                    {/* Explore More Card */}
                    <Link to="/login" className="w-80 flex-shrink-0">
                      <div className="cursor-pointer flex flex-col items-center justify-center bg-gray-100 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 p-6 text-center h-full">
                        <ArrowRightCircle className="w-12 h-12 text-teal-500 mb-4" />
                        <h3 className="text-xl font-bold text-gray-800">
                          Explore More
                        </h3>
                      </div>
                    </Link>
                  </div>
                </div>
              </motion.div>
            </div>
          </section>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default LandingPage;
