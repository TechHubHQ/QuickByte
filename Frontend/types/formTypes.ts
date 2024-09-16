export interface SignUpFormData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  phone: string;
  street: string;
  city: string;
  state: string;
  zip_code: string;
}

export interface SignInFormData {
  username: string;
  password: string;
}
