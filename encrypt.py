import random


def to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2: ]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def encrypt(text, key):
    output = ""
    index = 0
    key = str(key)
    while len(text) > len(key): # Увеличиваем ключ, пока не станет больше текста
        key += key
    for char_text in text:
        output += str(int(to_bits(key[index])) - int(to_bits(char_text)))
        # Добавляем нестандартный дефис и рандомное число
        num = random.randint(0, 9)
        output += "–" + str(num)
        index += 1
    return output


def decrypt(text, key):
    outputs = []
    index = 0
    key = str(key)
    out = ""
    for char_text in text:
        if char_text == "–":
            outputs.append(out)
            out = ""
        elif text[index - 1] != "–":
            out += char_text
            index += 1
    output = ""
    while len(outputs) > len(key):
        key += key
    for i in outputs:
        output += from_bits(str(int(to_bits(key[outputs.index(i)])) - int(outputs[outputs.index(i)])))
    return output