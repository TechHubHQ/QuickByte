import React from "react";

export interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}


export interface DishCardProps {
  name: string;
  image: string;
  rating: number;
  className?: string;
}