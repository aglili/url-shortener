from fastapi import FastAPI,BackgroundTasks,Depends,Request,HTTPException,Response
from starlette.responses import RedirectResponse
from schema import LongURL,ShortenURLResponse
from funcs import generate_short_url,check_short_url_exists,check_long_url_exists,is_valid_url
from models import URL
from sqlalchemy.orm import Session
from database import get_db,Base,engine
from redis_config import RedisConfig
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

redis = RedisConfig().get_redis()
Base.metadata.create_all(bind=engine)
    


@app.post("/shorten-link", response_model=ShortenURLResponse, status_code=201)
def shorten_link(url: LongURL, request: Request, db: Session = Depends(get_db)):
    if not is_valid_url(url.url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    long_url = check_long_url_exists(url.url, db)
    if long_url:
        return ShortenURLResponse(**long_url.__dict__)

    max_attempts = 5  # Maximum number of attempts to generate a unique short URL
    attempt = 0
    while attempt < max_attempts:
        short_code = generate_short_url()
        if not check_short_url_exists(short_code, db):
            break  # Exit the loop if the short URL is unique
        attempt += 1

    if attempt >= max_attempts:
        raise HTTPException(status_code=500, detail="Failed to generate a unique short URL")

    key = f"short_url:{short_code}"
    redis.setex(key, 3600, url.url)

    base_url = str(request.base_url)
    short_url = f"{base_url}{short_code}"
    
    
    whatsapp_url = f"https://api.whatsapp.com/send?text={short_url}"
    facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={short_url}"
    gmail_url = f"mailto:?subject=Check%20out%20this%20short%20URL&body={short_url}"


    db_url = URL(url=url.url, short_url=short_url, whatsapp=whatsapp_url, facebook=facebook_url,gmail=gmail_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return ShortenURLResponse(short_url=short_url, url=url.url, whatsapp=db_url.whatsapp, facebook=db_url.facebook,gmail=db_url.gmail)



@app.get("/{short_url}")
def redirect_to_url(short_url: str, db: Session = Depends(get_db)):
    url = redis.get(f"short_url:{short_url}")
    if url:
        return RedirectResponse(url.decode("utf-8"), status_code=301)
    else:
        db_url = check_short_url_exists(short_url, db)
        if db_url:

            return RedirectResponse(db_url.url, status_code=301)
        else:
            print("")
            raise HTTPException(status_code=404, detail="URL not found")
        





    




    


    