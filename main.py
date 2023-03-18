from fastapi import FastAPI, Depends, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import UserSignUpModel, UserSignInModel, UserResponseModel, PokemonResponseModel
import models
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session, subqueryload
import helpers
import fileuploads


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

Base.metadata.create_all(bind=engine)

# @app.get("/")
# def printHelloWorld():
#     return {"message": "Hello Code"}


# @app.get("/test")
# def printHelloWorld():
#     return {"message": "Hello Code Test"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup", response_model=UserResponseModel)
def signup(user: UserSignUpModel, db: Session = Depends(get_db)):
    registeredUser = helpers.register(user, db)
    # print(registeredUser)
    return registeredUser

@app.post("/signin", response_model=UserResponseModel)
def signin(user: UserSignInModel, db: Session = Depends(get_db)):
    loggedInUser = helpers.login(user,db)
    return loggedInUser

#  this is a one time process.
# a route to upload file and extract data from it and add it to pokemons table
# we are expecting a file which is uploadable and thus we are using UploadFile from fastapi (see line 1 above)
@app.post("/pokemon")
def uploadPokemon(pokemonCSVFile: UploadFile, db : Session = Depends(get_db)):
    fileuploads.uploadCSVFileToPokemonDatabase(pokemonCSVFile, db)
    return {"message": "File uploaded successfully"}

#  this is a one time process.
# a route to upload file and extract data from it and add it to pokemon_stats table
# we are expecting a file which is uploadable and thus we are using UploadFile from fastapi (see line 1 above)
@app.post("/pokemon_stats")
def uploadPokemonStats(pokemonStatsCSVFile: UploadFile, db : Session = Depends(get_db)):
    fileuploads.uploadCSVFileToPokemonStatsDatabase(pokemonStatsCSVFile, db)
    return {"message": "File uploaded successfully"}



@app.get("/pokemon", response_model=list[PokemonResponseModel])
def getAllPokemons(db: Session = Depends(get_db)):
    # avoid n+1 problem with eager loading using subqueryload (will be discussed in the session remind me if I forget please :))
    pokemons  = db.query(models.Pokemon).options(subqueryload(models.Pokemon.stats)).all()
    return pokemons


# @app.put("/pokemon/{pokemon_name}")    
# def updatePokemon(pokemon_name : str):
#     return {"pokemon": pokemon_name}


@app.get("/pokemon/{pokemon_name}", response_model=PokemonResponseModel)
def getPokemon(pokemon_name : str, db: Session = Depends(get_db)):
    #  case insensitive search. We use ilike which is only supported by postgresql
    # if you are using mysql or sqlite then you need to use like and convert the pokemon_name to lower case before passing it to the query
    # also need to write raw sql query to convert column string to lower case. 
    # That's the power of postgresql. It's a lot easier to use it than to use other databases in some cases.
    pokemon = db.query(models.Pokemon).filter(models.Pokemon.name.ilike(pokemon_name)).first()
    if not pokemon:
        raise HTTPException(404, "Pokemon not found")
    return pokemon

