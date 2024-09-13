import React, { useEffect, useState } from "react";
import deliveryBoy from "../assets/delivery-boy-scooter.png";
import { LoadingAnimationProps } from "../../types/cardTypes";

const LoadingAnimation: React.FC<LoadingAnimationProps> = ({ duration }) => {
  const [loadingProgress, setLoadingProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setLoadingProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 1;
      });
    }, duration / 100);

    return () => clearInterval(interval);
  }, [duration]);

  return (
    <div className="flex flex-col items-center justify-center h-screen w-full">
      {/* Loading Road Container */}
      <div className="relative w-3/4 h-6 bg-gray-700 rounded-full">
        {/* Road Markings */}
        <div className="absolute top-1/2 left-0 w-full h-1 flex justify-between items-center">
          {[...Array(20)].map((_, i) => (
            <div key={i} className="w-8 h-1 bg-white"></div>
          ))}
        </div>

        {/* Progress Road */}
        <div
          className="absolute top-0 left-0 h-full bg-gray-500 transition-all duration-300 ease-out"
          style={{ width: `${loadingProgress}%` }}
        ></div>
      </div>

      {/* Delivery Boy */}
      <div
        className="absolute transition-all duration-300 ease-out"
        style={{
          top: "calc(50% - 13rem)",
          left: `${loadingProgress}%`,
          transform: `translateX(-50%)`,
        }}
      >
        <img
          src={deliveryBoy}
          alt="Delivery Boy"
          className="h-52 w-52 object-contain"
        />
      </div>

      {/* Loading Text */}
      <p className="text-xl mt-4 font-semibold text-gray-700">
        Loading... {Math.floor(loadingProgress)}%
      </p>
    </div>
  );
};

export default LoadingAnimation;
