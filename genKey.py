from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

# สร้าง private key
private_key = ec.generate_private_key(ec.SECP256R1())
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# สร้าง public key
public_key = private_key.public_key()
public_numbers = public_key.public_numbers()
x = public_numbers.x.to_bytes(32, "big")
y = public_numbers.y.to_bytes(32, "big")
public_key_bytes = b'\x04' + x + y
public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode("utf-8").rstrip("=")

# แสดงผล
print("----- VAPID Key Pair -----")
print("Public Key:\n", public_key_b64)
print("\nPrivate Key (PEM):\n", private_pem.decode("utf-8"))
