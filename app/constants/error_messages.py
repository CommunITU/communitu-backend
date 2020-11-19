""" Common class for the error the messages """

# DATABASE
DB_CONN_ERR = """ 
                Failed to connect database. Please make sure: 
                1) Server is running 
                2) Connection url is valid """

# AUTHENTICATION
AUTH_CREDENTIALS_NOT_CORRECT = """ 
                Authentication failed. Credentials are not correct.
            """

USER_IS_NOT_AUTHENTICATED = """ 
                User is not authenticated.
            """

NO_SUCH_USER_WITH_GIVEN_EMAIL = """ 
                There is not an user with given email.
            """
