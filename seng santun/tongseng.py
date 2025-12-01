from PIL import Image
from PIL.PngImagePlugin import PngInfo
import zipfile 
import os

img = Image.open("c:\Users\falan\Downloads\tongseng.jpg")

if img.mode != 'RGB':
    img = img.convert('RGB')

metadata = PngInfo()
metadata.add_text("comment", "ada udang dibalik batu :D")
metadata.add_text("author", "Bu soleh")
metadata.add_text("flag_part1", "W92{T0ng_")
img.save("challenge.png", pnginfo=metadata)

print("✅ Part 1 disimpan di metadata")

with open("challenge.png", "ab") as f:
    f.write(b"\n\n")
    f.write(b"flag_part2: S33ng_seN9\n")
    f.write(b"\n")
print("✅ Part 2 disimpan di akhir file")

part3_content = """
ini adalah bagian akhir dari sebuah pengakhiran yang tiada henti :D
flag_part3: _S4NtUn}
"""

def xor_encrypt(data, key):
    return bytes([b ^ key for b in data.encode('utf-8')])

XOR_KEY = 0x42
encrypted_data = xor_encrypt(part3_content, XOR_KEY)

with open("flag_part3.txt", "wb") as f:
    f.write(encrypted_data)

with zipfile.ZipFile("hidden.zip", "w") as zf:
    zf.write("flag_part3.txt")

with open("challenge.png", "ab") as img_file:
    with open("hidden.zip", "rb") as zip_file:
        img_file.write(zip_file.read())

print("✅ Part 3 tersembunyi di flag_part3.txt (XOR encrypted)")

os.remove("flag_part3.txt")
os.remove("hidden.zip") 

print("\n" + "="*50)
print("🎉 CHALLENGE CREATED!")
print("="*50)
print("📍 Cara Solve:")
print("├─ Part 1: exiftool challenge.png | grep flag")
print("├─ Part 2: strings challenge.png | grep flag")
print("└─ Part 3: binwalk -e challenge.png --> decrypt flag_part3.txt")
print("\n🚩 Full Flag: W92{T0ng_S33ng_seN9_S4NtUn}")
print("\n💡 Cara decrypt Part 3 (setelah binwalk):")
print("   python3 -c 'data=open(\"flag_part3.txt\",\"rb\").read(); print(bytes([b^0x42 for b in data]).decode())'")
print("="*50)