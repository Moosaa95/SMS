import random
import string
import hashlib
import binascii
import smtplib
import random
from django.utils.crypto import get_random_string




# def generate_random_code():
#     return 'school_name'.join(random.choice(string.ascii_lowercase + string.digits, k=4))
RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
def generate_user_id(length,account_type, allowed_chars="1234567890"):
    result = None
    if account_type == "teacher":
        result = "tch"
    if account_type == "student":
        result = "stud"
    if account_type == "parent":
        result = "prt"
    
    return (f"{result}{get_random_string(length, allowed_chars)}")


 
def hash_password(ppt):
    bppt = ppt.encode()
    pct = hashlib.pbkdf2_hmac("sha256", bppt, b"m@ssa", 10000)
    dehex = binascii.hexlify(pct)
    hash_pass = dehex.decode()
    return hash_pass