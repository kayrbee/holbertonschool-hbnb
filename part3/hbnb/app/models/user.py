import re  # module to implement email format validation check
from app.models.base_class import Base


class User(Base):
    def __init__(self, first_name: str, last_name: str, email: str, is_admin=False):
        """
        Initialise a new User instance

        Args:
            first_name (str): User's first name. Max length 50 characters
            last_name (str): User's last name. Max length 50 characters
            email (str): User's email address. Must be valid email format
            is_admin (bool): admin status (defaults to false)
            created_at: timestamp when the user is created
            updated_at (DateTime):timestamp when the user is last updated
        Raises:
            TypeError: if any argument has incorrect type
            ValueError: if first_name or last_name exceeds 50 characters
                        if email address is invalid
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        # validate1: first_name must be a string and max 50 characters
        if not isinstance(first_name, str):
            raise TypeError("first name must be a string")
        if len(first_name) > 50:
            raise ValueError("first_name cannot exceed 50 characters")
        self.first_name = first_name

        # validate2: last_name must be a string and max 50 characters
        if not isinstance(last_name, str):
            raise TypeError("last name must be a string")
        if len(last_name) > 50:
            raise ValueError("last_name cannot exceed 50 characters")
        self.last_name = last_name

        # validate3: email must be a string and follow standard email format
        if not isinstance(email, str):
            raise TypeError("email must be a string")
        if not self.is_email_valid(email):
            raise ValueError("invalid email format")
        self.email = email

    def is_email_valid(self, email):
        """ Validate format of an email address using a regular expression """
        pattern = (r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
                   r"@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")
        return re.match(pattern, email) is not None

    # todo:
        # validate email address
        # duplicate email address
        # update user
