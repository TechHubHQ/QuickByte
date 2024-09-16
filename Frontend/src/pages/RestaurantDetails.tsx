import React from 'react';
import { useParams } from 'react-router-dom';
import { Star } from 'lucide-react';

//restaurant data
const restaurants = [
    { id: 1, name: 'Spice Delight', cuisine: 'North Indian', rating: 4.2, deliveryTime: '30 min', price: '₹₹' },
    { id: 2, name: 'Dosa House', cuisine: 'South Indian', rating: 4.5, deliveryTime: '25 min', price: '₹' },
    { id: 3, name: 'Tandoori Nights', cuisine: 'Mughlai', rating: 4.0, deliveryTime: '35 min', price: '₹₹' },
    { id: 4, name: 'Chaat Corner', cuisine: 'Street Food', rating: 4.7, deliveryTime: '20 min', price: '₹' },
    { id: 5, name: 'Biryani Bazaar', cuisine: 'Biryani', rating: 4.3, deliveryTime: '40 min', price: '₹₹' },
    { id: 6, name: 'Veggie Paradise', cuisine: 'Vegetarian', rating: 4.1, deliveryTime: '30 min', price: '₹₹' },
  ];

const RestaurantDetails: React.FC = () => {
  const { id } = useParams();
  const restaurant = restaurants.find((rest) => rest.id === Number(id));

  if (!restaurant) {
    return <div>Restaurant not found</div>;
  }

  return (
    <div className="container mx-auto mt-8 px-4">
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-2xl font-bold mb-4">{restaurant.name}</h2>
        <p className="text-gray-600 mb-2">{restaurant.cuisine}</p>
        <div className="flex items-center mb-4">
          <Star className="text-yellow-400 mr-1" size={24} />
          <span>{restaurant.rating}</span>
        </div>
        <p className="text-gray-600 mb-2">Delivery Time: {restaurant.deliveryTime}</p>
        <p className="text-gray-600">Price: {restaurant.price}</p>
      </div>
    </div>
  );
};

export default RestaurantDetails;
