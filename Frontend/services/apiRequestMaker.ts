import axiosInstance from "./ApiHandler";
import { SignInFormData, SignUpFormData } from "../types/formTypes";
import { storeAuthToken } from "../security/auth";
import { AuthResponse } from "../types/apiTypeChecker";

export const signUp = async (data: SignUpFormData) => {
  try {
    const response = await axiosInstance.post<AuthResponse>("/v1/signup", data, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    const token: string = response.data.token;
    storeAuthToken(token);
    return response.data;
  } catch (error) {
    console.error("Error during sign-up request:", error);
    throw error;
  }
};

export const signIn = async (data: SignInFormData) => {
  try {
    const response = await axiosInstance.post<AuthResponse>("/v1/login", data, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    const token: string = response.data.token
    storeAuthToken(token);
    return response.data;    
  } catch (error) {
    console.error("Error during sign-in request:", error);
    throw error;
  }
};
