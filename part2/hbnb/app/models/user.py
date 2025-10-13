from app.models.base_class import Base

class User(Base):
    def __init__(self, first_name: str, last_name: str, email: str, is_admin=False): # todo: add password
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    # todo:
        # validate email address
            # duplicate email address
        # update user

        

