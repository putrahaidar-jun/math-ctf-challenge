from PIL import Image

def quick_check(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    width, height = img.size
    
    # Ambil 1000 bit pertama
    binary = ''
    count = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary += str(r & 1)
            count += 1
            if count >= 1000:
                break
        if count >= 1000:
            break
    
    # Convert ke text
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    
    print("[*] First 100 characters extracted:")
    print(repr(text[:100]))
    
    if "FLAG" in text or "|||" in text:
        print("✅ Flag detected!")
    else:
        print("❌ No flag detected in first 1000 bits")

# Check
quick_check('challenge.png')