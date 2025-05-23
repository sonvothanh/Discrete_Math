import sympy
from sympy.ntheory import sqrt_mod

def rabin_generate_keys():
    p = sympy.nextprime(100)
    while p % 4 != 3:
        p = sympy.nextprime(p)
    
    q = sympy.nextprime(p + 1)
    while q % 4 != 3:
        q = sympy.nextprime(q)
    
    n = p * q
    return n, (p, q)

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

# --- CHUYỂN ĐỔI GIỮA CHUỖI VÀ SỐ ---
def string_to_ascii_blocks(s):
    return [ord(char) for char in s]

def ascii_blocks_to_string(lst):
    return ''.join([chr(x) for x in lst])

# --- MÃ HÓA VÀ GIẢI MÃ CHUỖI ---
def encrypt_string(message, n):
    blocks = string_to_ascii_blocks(message)
    encrypted_blocks = [rabin_encrypt(m, n) for m in blocks]
    return encrypted_blocks

def decrypt_string(cipher_blocks, p, q):
    decrypted_candidates = [rabin_decrypt(c, p, q) for c in cipher_blocks]

    # Lọc đúng ký tự ASCII (0-127) - thường chỉ có 1 ứng viên hợp lệ
    decrypted_blocks = []
    for cands in decrypted_candidates:
        valid = [x for x in cands if 0 <= x <= 127]
        if valid:
            decrypted_blocks.append(valid[0])
        else:
            decrypted_blocks.append(ord('?'))  # fallback
    return ascii_blocks_to_string(decrypted_blocks)

# --- DEMO ---
n, (p, q) = rabin_generate_keys()
print(f"Public key (n): {n}")
print(f"Private key (p, q): {p}, {q}")

original_text = "Hi!"
print(f"Original text: {original_text}")

cipher_blocks = encrypt_string(original_text, n)
print(f"Encrypted blocks: {cipher_blocks}")

decrypted_text = decrypt_string(cipher_blocks, p, q)
print(f"Decrypted text: {decrypted_text}")
