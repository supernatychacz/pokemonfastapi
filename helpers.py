from models import User
from passlib.context import CryptContext
from fastapi import HTTPException

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
def register(user, db):

    userDetails = getUserByEmail(user.email, db)
    if userDetails:
        raise HTTPException(400, "User already exists")
    hashedPassword = passwordContext.hash(user.password)
    
    newUser = User(name=user.name, email=user.email, password=hashedPassword)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser    


def login(user, db):
    userDetails = getUserByEmail(user.email, db)

    if not userDetails:
        raise HTTPException(404, "Email not found")
    
    passwordCheck = passwordContext.verify(user.password, userDetails.password)

    if not passwordCheck:
        raise HTTPException(401,"Incorrect credentials")

    return userDetails

        

# select * from users where email = email limit 1
def getUserByEmail(email, db):
    return db.query(User).filter(User.email == email).first()
    