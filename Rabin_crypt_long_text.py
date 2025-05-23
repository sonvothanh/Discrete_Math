
import sympy
from sympy.ntheory import sqrt_mod
from math import ceil

# --- KHỞI TẠO KHÓA ---
def rabin_generate_keys():
    p = sympy.nextprime(50000)
    while p % 4 != 3:
        p = sympy.nextprime(p)
    q = sympy.nextprime(p + 1)
    while q % 4 != 3:
        q = sympy.nextprime(q)
    n = p * q
    return n, (p, q)

# --- MÃ HÓA / GIẢI MÃ ---
def rabin_encrypt(m, n):
    return pow(m, 2, n)

def rabin_decrypt(c, p, q):
    n = p * q
    r = sqrt_mod(c, p, all_roots=True)
    s = sqrt_mod(c, q, all_roots=True)
    roots = []
    for rp in r:
        for sq in s:
            x = sympy.crt([p, q], [rp, sq])
            if x is not None:
                roots.append(x % n)
    return list(set(roots))

# --- HỖ TRỢ CHUỖI DÀI ---
def split_blocks(s: str, block_size: int) -> list[int]:
    byte_data = s.encode('utf-8')
    blocks = [int.from_bytes(byte_data[i:i + block_size], 'big')
              for i in range(0, len(byte_data), block_size)]
    return blocks

def combine_blocks(blocks: list[int], block_size: int) -> str:
    byte_data = b''.join([b.to_bytes(block_size, 'big') for b in blocks])
    return byte_data.decode('utf-8', errors='ignore')

def encrypt_long_text(text, n, block_size):
    blocks = split_blocks(text, block_size)
    encrypted_blocks = [rabin_encrypt(b, n) for b in blocks]
    return encrypted_blocks

def decrypt_long_text(encrypted_blocks, p, q, block_size):
    decrypted_blocks = []
    for c in encrypted_blocks:
        candidates = rabin_decrypt(c, p, q)
        # Chọn ứng viên có thể convert lại đúng số byte
        found = False
        for m in candidates:
            try:
                m.to_bytes(block_size, 'big').decode('utf-8')
                decrypted_blocks.append(m)
                found = True
                break
            except:
                continue
        if not found:
            decrypted_blocks.append(int.from_bytes(b'?', 'big') * block_size)
    return combine_blocks(decrypted_blocks, block_size)

# --- DEMO ---
n, (p, q) = rabin_generate_keys()
block_size = 2  # 2 byte = 16 bit = số < 65536, an toàn với n > 100000

text = "Xin chào, đây là hệ mã Rabin với padding!"
print("Original:", text)

cipher_blocks = encrypt_long_text(text, n, block_size)
print("Encrypted:", cipher_blocks)

recovered = decrypt_long_text(cipher_blocks, p, q, block_size)
print("Decrypted:", recovered)
