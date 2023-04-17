from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from extract import *
import os
import subprocess
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from fastapi.middleware.cors import CORSMiddleware

cred = credentials.Certificate('genius-bot-b8355-firebase-adminsdk-bookx-2d49ab4b27.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserSearch(BaseModel):
    artistName: str

@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to ScrapeAPI!"}

@app.post("/artists/")
async def create_artist(data: UserSearch):
    artist_name = data.artistName
    print(data)
    print('Artist name: {}'.format(artist_name))
    doc_ref = db.collection('artists').document(artist_name)
    doc = doc_ref.get()
    collab_ref = doc_ref.collection('collaborators')
    if doc.exists:
        print('Artist found in database, returning data...')
        print(doc.to_dict())
        return jsonify(doc.to_dict())
    else:
        print('Artist not found in database, scraping...')
        scraper_thread = threading.Thread(target=run_scraper, args=(artist_name,))
        scraper_thread.start()
        return jsonify({'message': 'Scraping artist...'})

def run_scraper(artist):
    cmd = ['python3', 'newtrst.py', artist]
    subprocess.run(cmd)

#@app.get("/homepage")
#async def demo_get():
    #driver=createDriver()

    #homepage = getGoogleHomepage(driver)
    #driver.close()
    #return homepage



