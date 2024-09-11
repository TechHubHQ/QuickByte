package database

func CreateDBUser(username string, password string) error {
	db, err := ConnectDB()
	if err != nil {
		return err
	}
	defer db.Close()

	// Create the new user
	_, err = db.Exec("CREATE ROLE " + username + " WITH PASSWORD '" + password + "';")
	if err != nil {
		return err
	}

	// Grant privileges (optional)
	_, err = db.Exec("GRANT CONNECT ON DATABASE quickdb TO " + username + ";")
	if err != nil {
		return err
	}

	// Grant privileges on specific tables (optional)
	_, err = db.Exec("GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE qb_user TO " + username + ";")
	if err != nil {
		return err
	}

	return nil
}
