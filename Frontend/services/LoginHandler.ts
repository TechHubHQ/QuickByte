import axiosInsatnce from "./ApiHandler";

export const signIn = async (email: string, password: string) => {
  try {
    const response = await axiosInsatnce.post(`/signin`, {
      email,
      password,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const signUp = async (email: string, password: string) => {
  try {
    const response = await axios.post(`/signup`, {
      email,
      password,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};
