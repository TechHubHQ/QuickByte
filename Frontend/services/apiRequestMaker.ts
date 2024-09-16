import axiosInstance from "./apiHandler";
import { SignInFormData, SignUpFormData } from "../types/formTypes";

export const signUp = async (data: SignUpFormData) => {
  try {
    const response = await axiosInstance.post("/v1/signup", data, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error during sign-up request:", error);
    throw error;
  }
};

export const signIn = async (data: SignInFormData) => {
  try {
    const response = await axiosInstance.post("/v1/signin", data, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error during sign-in request:", error);
    throw error;
  }
};
