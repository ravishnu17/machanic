from passlib.context import CryptContext

pwd= CryptContext(schemes=['bcrypt'], deprecated='auto')

def encrypt(plaintext):
    return pwd.hash(plaintext)

def verify(plainText, encryptedText):
    return pwd.verify(plainText,encryptedText)