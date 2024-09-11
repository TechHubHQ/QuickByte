import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import deliveryImg from "../assets/delivery-boy.png";
import { RestaurantCard, FeatureCard } from "../components/Cards";
import {
  ArrowRight,
  Clock,
  Utensils,
  Truck,
  Shield,
  CreditCard,
  HeartHandshake,
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
                <div className="md:w-1/2 mb-10 md:mb-0">
                  <h1 className="text-4xl md:text-6xl font-bold mb-4">
                    Delicious Food, Delivered Fast
                  </h1>
                  <p className="text-xl mb-6">
                    Experience the best cuisines from the comfort of your home.
                  </p>
                  <button className="bg-white text-teal-600 font-bold py-2 px-6 rounded-full flex items-center hover:bg-teal-50 transition duration-300">
                    Order Now <ArrowRight className="ml-2" />
                  </button>
                </div>
                <div className="md:w-1/2">
                  <img
                    src={deliveryImg}
                    alt="Delicious food spread"
                    className="rounded-lg shadow-2xl"
                  />
                </div>
              </div>
            </div>
          </section>

          {/* Features Section */}
          <section className="py-20">
            <div className="container mx-auto px-4">
              <h2 className="text-4xl font-bold text-center mb-12 text-gray-800">
                Why Choose QuickByte?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
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
              </div>
            </div>
          </section>

          {/* Popular Dishes Section */}
          <section className="py-20">
            <div className="container mx-auto px-4">
              <h2 className="text-4xl font-bold text-center mb-12 text-gray-800">
                Explore our Culinary Delights
              </h2>
              <div className="relative overflow-hidden">
                <div className="flex overflow-x-auto pb-8 hide-scrollbar">
                  <div className="flex space-x-6">
                    <RestaurantCard
                      name="Chicken Biryani"
                      image={loadedImages.Biryani}
                      rating={4.5}
                      className="w-80 flex-shrink-0"
                    />
                    <RestaurantCard
                      name="Chicken Cheese Pizza"
                      image={loadedImages.Pizza}
                      rating={4.7}
                      className="w-80 flex-shrink-0"
                    />
                    <RestaurantCard
                      name="Chicken Burger"
                      image={loadedImages.Burger}
                      rating={4.6}
                      className="w-80 flex-shrink-0"
                    />
                    <RestaurantCard
                      name="Shawarma"
                      image={loadedImages.Shawarma}
                      rating={4.4}
                      className="w-80 flex-shrink-0"
                    />
                    <RestaurantCard
                      name="Chocolate Cake"
                      image={loadedImages.Cake}
                      rating={4.8}
                      className="w-80 flex-shrink-0"
                    />
                    <RestaurantCard
                      name="Samosa"
                      image={loadedImages.Samosa}
                      rating={4.5}
                      className="w-80 flex-shrink-0"
                    />
                    <RestaurantCard
                      name="Greek Taverna"
                      image="/api/placeholder/400/250"
                      rating={4.6}
                      className="w-80 flex-shrink-0"
                    />
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default LandingPage;
