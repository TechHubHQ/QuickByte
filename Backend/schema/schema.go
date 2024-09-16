package schema

type LoginRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type SignupRequest struct {
	FirstName string `json:"first_name"`
	LastName  string `json:"last_name"`
	Password  string `json:"password"`
	Phone     string `json:"phone"`
	Email     string `json:"email"`
	Street    string `json:"street"`
	City      string `json:"city"`
	State     string `json:"state"`
	ZipCode   string `json:"zip_code"`
}
