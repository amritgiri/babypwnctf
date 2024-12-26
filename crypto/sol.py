from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import unpad
from hashlib import sha256
import math

# Optimized Discrete Logarithm: Baby-Step Giant-Step
def discrete_log(target, base, modulus):
    """Baby-Step Giant-Step algorithm for discrete logarithms."""
    m = math.isqrt(modulus) + 1
    base_powers = {}
    current = 1

    # Baby step: Precompute base^j % modulus for all j in [0, m)
    for j in range(m):
        base_powers[current] = j
        current = (current * base) % modulus

    # Giant step: Compute target * base^(-i*m) % modulus
    factor = pow(base, -m, modulus)  # base^(-m) mod modulus
    current = target

    for i in range(m):
        if current in base_powers:
            return i * m + base_powers[current]
        current = (current * factor) % modulus

    raise ValueError("Discrete log not found")

# Inputs
p = 0xdd6cc28d  # Prime modulus
g = 0x83e21c05  # Generator
A = 0xcfabb6dd  # Public key A
B = 0xc4a21ba9  # Public key B
ciphertext = b'\xff\x01n\xc6^\xb0\xdf%\xa7\xae\xee\xa4>\xb6\xb5\x17\xefjx\x97\x99\xb9\x95!\x16\x8a:\x08M\x82\xef\xf8'

# Calculate the private key `a` and shared secret `C`
a = discrete_log(A, g, p)  # Find `a` such that g^a ≡ A (mod p)
C = pow(B, a, p)          # Calculate shared secret: C = B^a (mod p)

# Derive AES key from shared secret `C`
hash = sha256()
hash.update(long_to_bytes(C))
key = hash.digest()[:16]

# Decrypt the ciphertext using AES-CBC
iv = b'\xc1V2\xe7\xed\xc7@8\xf9\\\xef\x80\xd7\x80L*'
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(ciphertext)

# Unpad and print the plaintext (flag)
try:
    flag = unpad(decrypted, 16)
    print(flag.decode('utf-8'))
except ValueError:
    print("Decryption failed: Incorrect padding or key.")
