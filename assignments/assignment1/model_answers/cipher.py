import random

test_text = "The number Pi is a mathematical constant. Originally defined as the ratio of a circle's circumference to its diameter, it now has various equivalent definitions and appears in many formulas in all areas of mathematics and physics."

# convert a string to uppercase and remove all the spaces, punctuation, numbers, etc
def to_upper_no_spaces(str):
    result = ""
    for char in str.upper():
        if char >= 'A' and char <= 'Z':
            result += char
    return result

# encrypt a string using a caesar cipher and a random key
def encrypt(str):
    key = random.randint(1,25)
    print("Encrypting with key", key)
    #reverse the key, so encryption and decryption keys are the same
    key = 26 - key
    result = ""
    return decrypt_with_key(str, key)

# decrypt a string using a caesar cipher and a specific key
def decrypt_with_key(str, key):
    result = ""
    for char in str:
        #shift each character key places later in the alphabet,
        #wrapping from Z back to A if necessary
        newchar = chr(((ord(char) - ord('A') + key) % 26) + ord('A'))
        result += newchar
    return result

#text a possible decrypt against english language letter frequencies
def score_result(str):
    # english language letter frequencies
    frequencies = [8.12, 1.49, 2.71, 4.32, 12.02, 2.30, 2.03, 5.92, 7.31, 0.10,
                   0.69, 3.98, 2.61, 6.95, 7.68, 1.82, 0.11, 6.02, 6.28, 9.10,
                   2.88, 1.11, 2.09, 0.17, 2.11, 0.07]
    score = 0.0
    for char in str:
        index = ord(char) - ord('A')
        score += frequencies[index]
    return score
        

# decrypt a string using a caesar cipher
def decrypt(str):
    bestkey = -1
    bestscore = -1
    # just try all the keys.
    for key in range(0,26):
        teststr = decrypt_with_key(str, key)
        score = score_result(teststr)
        print("Testing key", key, "score is", score)
        if score > bestscore:
            bestscore = score
            bestkey = key
    return decrypt_with_key(str, bestkey)


plain_text = to_upper_no_spaces(test_text)
print("Original text:")
print(plain_text)

cipher_text = encrypt(plain_text)
print("\nCipher text:")     
print(cipher_text)

decrypted_text = decrypt(cipher_text)
print("\nDecrypt:")     
print(decrypted_text)

