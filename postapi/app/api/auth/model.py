from ...extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from flask_bcrypt import Bcrypt

bycrypt = Bcrypt()

class User(db.Model):
    """User entity
    """

    __tablename__ = "user"
    __asbtract__ = False
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[String] = mapped_column(String(90), nullable=False)
    password_hash: Mapped[String] = mapped_column(String(180), nullable=False)

    def set_password(self, password):
        self.password_hash = bycrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bycrypt.check_password_hash(self.password_hash, password)
 