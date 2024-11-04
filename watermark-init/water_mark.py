def add_watermark(code, watermark="LABORATORIA"):
    watermark_binary = ''.join(
        ['\t' if bit == '1' else ' ' for bit in ''.join(format(ord(c), '08b') for c in watermark)])
    print("Watermark binary:" + watermark_binary)
    print('Dlugosc watermarku: ' + str(len(watermark)))
    print('Dlugosc binarna watermarku: ' + str(len(watermark_binary)))
    lines = code.splitlines()

    for i in range(1, len(lines), 2):
        if i // 2 < len(watermark_binary):
            lines[i] += watermark_binary[i // 2]

    return '\n'.join(lines)


def extract_watermark(code):
    lines = code.splitlines()

    binary_pattern = []
    for i in range(1, len(lines), 2):
        if lines[i].endswith(" ") or lines[i].endswith("\t"):
            last_char = lines[i][-1]
            binary_pattern.append('1' if last_char == '\t' else '0')

    watermark_text = ''
    for i in range(0, len(binary_pattern), 8):
        byte = ''.join(binary_pattern[i:i + 8])
        if len(byte) == 8:
            watermark_text += chr(int(byte, 2))

    return watermark_text if watermark_text else "Brak znaku wodnego"


code_example = """
def sample_function():
    print("Hello, World!")
    return 42

def sample_function2():
    print("Hello, World!")

def sample_function():
    print("Hello, World!")
    return 42

def sample_function2():
    print("Hello, World!")

def sample_function():
    print("Hello, World!")
    return 42

def sample_function2():
    print("Hello, World!")

def sample_function():
    print("Hello, World!")
    return 42

def sample_function2():
    print("Hello, World!")

def sample_function():
    print("Hello, World!")
    return 42

def sample_function2():
    print("Hello, World!")

def sample_function():
    print("Hello, World!")
    return 42

def sample_function2():
    print("Hello, World!")

def sample_function():
    print("Hello, World!")
    return 42

def sample_function2():
    print("Hello, World!")

def sample_function():
    print("Hello, World!")
    return 42
"""

watermarked_code = add_watermark(code_example)
print("Watermarkowany kod:" + watermarked_code)

detected_watermark = extract_watermark(watermarked_code)
print("Odczytany przykladowy kod:", code_example)

detected_watermark_2 = extract_watermark(watermarked_code)
print("Odczytany watermark:", detected_watermark_2)
