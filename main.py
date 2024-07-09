import math
import sympy

# Dictionary for mapping characters to numbers
cod = {
    '_': 0,
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    'F': 6,
    'G': 7,
    'H': 8,
    'I': 9,
    'J': 10,
    'K': 11,
    'L': 12,
    'M': 13,
    'N': 14,
    'O': 15,
    'P': 16,
    'Q': 17,
    'R': 18,
    'S': 19,
    'T': 20,
    'U': 21,
    'V': 22,
    'W': 23,
    'X': 24,
    'Y': 25,
    'Z': 26
}

# Lists for the values and keys from the cod dictionary
values = list(cod.values())
keys = list(cod.keys())

# Parameters for the RSA algorithm
k = 2
l = 3

# MODIFY HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#random 2 distinct large prime numbers
p = 53
q = 67
# ------------------------------------------------------------

n = p * q
phi = (p - 1) * (q - 1)

# Finding a suitable public key (e)
#1<e<phi(n), smallest prime number  with gdc(e, phi)==1
e = 0
for e in range(1, phi):
    if e % 2 == 1 and sympy.isprime(e):
        #check is e and phi is coprime
        if math.gcd(e, phi) == 1:
            break


#=ax+by
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def modular_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"The modular inverse does not exist for {a} modulo {m}")
    else:
        return x % m


def RSA_encrypt(word):
    # Print RSA parameters
    print("n = ", str(n), "\nphi(n) = ", str(phi), "\ne = ", str(e))

    # Add padding to the input word
    for i in range(len(word) % k + 1):
        word += '_'

    # Divide the padded word into blocks of size k
    blocksK = []
    i = 0
    w = ''
    for c in word:
        if i < k:
            w = w + c
            i = i + 1
        else:
            blocksK.append(w)
            i = 1
            w = c
    print("Blocks K: ", blocksK)

    # Convert each block into its numerical equivalent
    newCodes = []
    for w in blocksK:
        b = 27 * cod[w[0]] + cod[w[1]]
        newCodes.append(b)
    print("Equivalents: ", newCodes)

    # Encrypt each numerical equivalent using RSA

    encryption = []
    for b in newCodes:
        # c=b^e(mod n)
        c = b ** e % n
        encryption.append(c)
    print("Encryption: ", encryption)

    # Convert each encrypted numerical equivalent back to characters
    blocksL = []
    for c in encryption:
        new_cod = ''
        l1 = values.index(c // (27 * 27))
        c = c - l1 * (27 * 27)
        l2 = values.index(c // 27)
        c = c - l2 * 27
        l3 = c
        new_cod = new_cod + keys[l1] + keys[l2] + keys[l3]
        blocksL.append(new_cod)
    print("Blocks L:", blocksL)

    # Combine the decrypted blocks into the final ciphertext
    cyphertext = ''
    for c in blocksL:
        cyphertext = cyphertext + c
    print("Cyphertext: ", cyphertext)


def RSA_decrypt(word):
    # Calculate the private key (d)
    #d=e^(-1)(mod phi)
    d1 = modular_inverse(e, phi)
    # d = 0
    # for i in range(phi-1):
    #     if (e % phi * i % phi) % phi == 1:
    #         d = i
    print("n = ", str(n), "\nphi(n) = ", str(phi), "\ne = ", str(e), "\nd = ", str(d1))

    # Add padding to the input word
    for i in range(len(word) % k + 1):
        word = word + '_'

    # Divide the padded word into blocks of size l
    blocksL = []
    i = 0
    w = ''
    for c in word:
        if i < l:
           w = w + c
           i = i + 1
        else:
            blocksL.append(w)
            i = 1
            w = c
    print("Blocks L: ", blocksL)

    # Convert each block into its numerical equivalent
    newCodes = []
    for w in blocksL:
        b = 27 * 27 * cod[w[0]] + 27 * cod[w[1]] + cod[w[2]]
        newCodes.append(b)
    print("Equivalents: ", newCodes)

    # Decrypt each numerical equivalent using RSA
    decryption = []
    for b in newCodes:
        #c=b^d(mod n)
        c = b ** d1 % n
        decryption.append(c)
    print("Decryption: ", decryption)

    # Convert each decrypted numerical equivalent back to characters
    blocksK = []
    for c in decryption:
        new_cod = ''
        l1 = values.index(c // 27)
        c = c - l1 * 27
        l2 = c
        new_cod = new_cod + keys[l1] + keys[l2]
        blocksK.append(new_cod)
    print("Blocks K:", blocksK)

    # Combine the decrypted blocks into the final plaintext
    plaintext = ''
    for c in blocksK:
        plaintext += c
    print("Plain text: ", plaintext)


def main():
    # User menu
    menu = """0. Exit
1. Encrypt
2. Decrypt
>>>> """

    cmd = input(menu)
    while cmd:
        if cmd == '1':
            word = input("Enter the word you want to encrypt: ")
            RSA_encrypt(word)
            cmd = input(menu)
        elif cmd == '2':
            word = input("Enter the word you want to decrypt: ")
            RSA_decrypt(word)
            cmd = input(menu)
        elif cmd == '0':
            return
        else:
            print("Invalid command!")
            cmd = input(menu)


main()
