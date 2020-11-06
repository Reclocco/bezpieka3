class Cryptogram:
    def __init__(self, cipher):
        self.chars = []

        for char in str(cipher).strip().split(' '):
            self.chars.append(chr(int(char, 2)))

    def get_char(self, idx):
        try:
            return self.chars[idx]
        except:
            return '*'


# init
LETTERS_FREQ = {
    'a': 89, 'i': 82, 'o': 78, 'e': 77, 'z': 56, 'n': 55, 'r': 47, 'w': 47, 's': 43, 't': 40, 'c': 40, 'y': 38,
    'k': 35, 'd': 33, 'p': 31, 'm': 28, 'u': 25, 'j': 23, 'l': 21, 'b': 15, 'g': 14, 'h': 11, 'f': 3, 'q': 1,
    'v': 1, 'x': 1, ' ': 100, ',': 16, '.': 10, '-': 10, '"': 10, '!': 10, '?': 10, ':': 10, ';': 10, '(': 10, ')': 10
}

CRYPTOGRAMS = []
key = []

for q in range(65, 91):
    LETTERS_FREQ[chr(q)] = 10

for q in range(48, 58):
    LETTERS_FREQ[chr(q)] = 10


def potential_keys_search(idx):
    potential_keys = {}

    for encrypted in CRYPTOGRAMS:
        if idx >= len(encrypted.chars):
            continue

        for f_char in LETTERS_FREQ.keys():
            potential_key = ord(encrypted.get_char(idx)) ^ ord(f_char)

            potential_keys[potential_key] = potential_keys.get(potential_key, 0) + LETTERS_FREQ[f_char]

    return [i for i in sorted(potential_keys.keys(), key=lambda i: potential_keys[i], reverse=True)]


def best_key_search(keys, idx):
    best_char = ord(' ')
    best_freq = 0

    for char in keys:
        freq = 0

        for encrypted in CRYPTOGRAMS:
            if idx >= len(encrypted.chars):
                continue

            # xor
            if (chr(ord(encrypted.get_char(idx)) ^ char)) in LETTERS_FREQ.keys():
                freq += 1

        if freq > best_freq:
            best_freq = freq
            best_char = char

    return best_char


def learn_and_decrypt():
    global key
    decrypted = ""
    max_len = max(len(encrypted.chars) for encrypted in CRYPTOGRAMS)

    key = [best_key_search(potential_keys_search(idx), idx) for idx in range(max_len)]

    for encrypted in CRYPTOGRAMS:
        for i in range(0, len(encrypted.chars)):
            decrypted += chr(ord(encrypted.get_char(i)) ^ key[i])

        decrypted += '\n'

    return decrypted


def decrypt(file):
    global key
    decrypted = ""
    cryptogram = []

    for char in file.read().strip().split(' '):
        cryptogram.append(chr(int(char, 2)))

    for i in range(0, len(cryptogram)):
        decrypted += chr(ord(cryptogram[i]) ^ key[i])

    decrypted += '\n'

    return decrypted


def main():
    global CRYPTOGRAMS

    with open('encoded.txt', 'r') as f1, open('decoded.txt', 'w') as f2, open('long.txt', 'r') as long,\
            open('short.txt', 'r') as short:
        for line in f1.read().splitlines():
            CRYPTOGRAMS.append(Cryptogram(line))

        learn_and_decrypt()
        f2.write(decrypt(short))


if __name__ == '__main__':
    main()
