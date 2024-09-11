import React from "react";
import { FeatureCardProps, RestaurantCardProps } from "../../types/cardTypes";
import { Star, StarHalf } from "lucide-react";

const FeatureCard: React.FC<FeatureCardProps> = ({
  icon,
  title,
  description,
}) => (
  <div className="bg-white rounded-lg shadow-md p-6 flex flex-col items-center text-center">
    <div className="mb-4">{icon}</div>
    <h3 className="text-xl font-semibold mb-2">{title}</h3>
    <p className="text-gray-600">{description}</p>
  </div>
);

const RestaurantCard: React.FC<RestaurantCardProps> = ({
  name,
  image,
  rating,
  cuisine,
  className,
}) => {
  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;

    for (let i = 1; i <= 5; i++) {
      if (i <= fullStars) {
        stars.push(
          <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />
        );
      } else if (i === fullStars + 1 && hasHalfStar) {
        stars.push(
          <StarHalf
            key={i}
            className="w-5 h-5 fill-yellow-400 text-yellow-400"
          />
        );
      } else {
        stars.push(<Star key={i} className="w-5 h-5 text-gray-300" />);
      }
    }

    return stars;
  };

  return (
    <div
      className={`bg-white rounded-lg shadow-md overflow-hidden ${className}`}
    >
      <div className="h-52 overflow-hidden flex justify-center items-center">
        <img src={image} alt={name} className="w-56 h-full object-cover" />
      </div>
      <div className="p-4">
        <h3 className="text-black font-semibold mb-1">{name}</h3>
        <p className="text-gray-600 mb-2">{cuisine}</p>
        <div className="flex items-center">
          <div className="flex mr-2">{renderStars(rating)}</div>
          <span className="text-sm text-gray-600">{rating.toFixed(1)}</span>
        </div>
      </div>
    </div>
  );
};

export { FeatureCard, RestaurantCard };
