import re  # module to implement email format validation check
from app.models.base_class import Base
from app import db, bcrypt
from sqlalchemy.orm import validates
from .base_class import Base


class User(Base):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='user', lazy=True)  # relationship w Place
    reviews = db.relationship('Review', backref='user', lazy=True)  # relationship w Review

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        is_admin=False
    ):
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
        self.password = self.hash_password(password)
        self.is_admin = is_admin

    # --- Validations start here ----
    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value:
            raise TypeError("First name must be provided")
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        if len(value) > 50:
            raise ValueError("First name cannot exceed 50 characters")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value:
            raise TypeError("Last name must be provided")
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        if len(value) > 50:
            raise ValueError("Last name cannot exceed 50 characters")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not value:
            raise TypeError("Email must be provided")
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not self.is_email_valid(value):
            raise ValueError("Invalid email format")
        return value

    def is_email_valid(self, email):
        """ Validate format of an email address using a regular expression """
        pattern = (r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
                   r"@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")
        return re.match(pattern, email) is not None

    def hash_password(self, password):
        """Hashes the password before storing it."""
        if not password:
            raise TypeError("Password must be provided")
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        # todo: add more validations (missing pw if not pw, raise error "pw must be included")
        return bcrypt.generate_password_hash(
            password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Return a dictionary representation of the User."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
