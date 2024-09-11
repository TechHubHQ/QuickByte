import React from "react";

export interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}


export interface RestaurantCardProps {
  name: string;
  image: string;
  rating: number;
  cuisine: string;
  className?: string;
}