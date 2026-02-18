import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    business_name: str
    location: str



@app.post("/scrape")
def scrape(query: ScrapeRequest):
    query = str(query.business_name) + " in " + str(query.location)
    resp = requests.get(
        "https://maps.googleapis.com/maps/api/place/textsearch/json",
        params={"query": query, "key": os.getenv("API_KEY")}
    )
    ret = []
    response_results = resp.json()['results']
    for result in response_results:
        types = ""
        for type in result['types']:
            types +=  str(type) + ", "
        types = types[0:len(types) - 2]
        ret.append([result['name'], result['formatted_address'], types])

    return {"results": ret}



