import uuid,os,qrcode,tempfile
from dotenv import load_dotenv
from models import URL
from database import get_db
from sqlalchemy.orm import Session
load_dotenv()

from supabase import create_client, Client

# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")
# bucket_name = os.environ.get("BUCKET_NAME")
# supabase: Client = create_client(url, key)

def generate_short_url():
    # Generate a UUID
    unique_id = uuid.uuid4()
    # Convert UUID to a short string
    short_url = base_convert(int(unique_id), 10, 62)
    # Ensure short URL is 6 characters long
    short_url = short_url.zfill(6)[:6]
    return short_url

def base_convert(number, base_from, base_to):
    if number < 0 or base_from < 2 or base_to < 2:
        raise ValueError("Invalid input")

    digits = []
    while number > 0:
        number, remainder = divmod(number, base_to)
        digits.append(str(remainder))

    return ''.join(digits[::-1])



# future implementation
# def generate_qr_code(url, short_url):
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(url)
#     qr.make(fit=True)

#     img = qr.make_image(fill_color="black", back_color="white")
    
#     img.save(f"static/{short_url}.png")


#     filename = f"static/{short_url}.png"
#     temp_file = tempfile.NamedTemporaryFile(delete=False)

#     with open(f"static/{short_url}.png", "rb") as image_file:
#         qr_code = image_file.read()


def check_short_url_exists(short_url, db: Session):
    existing_url = db.query(URL).filter(URL.short_url == short_url).first()
    return existing_url is not None

def check_long_url_exists(long_url,db:Session):
    long_code = db.query(URL).filter(URL.url == long_url).first()
    if long_code:
        return long_code
    return None
    




    
    



