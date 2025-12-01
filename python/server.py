import socketserver
import random
import time

ANGKA_KE_KATA = {
    0: "nol", 1: "satu", 2: "dua", 3: "tiga", 4: "empat",
    5: "lima", 6: "enam", 7: "tujuh", 8: "delapan", 9: "sembilan",
    10: "sepuluh", 11: "sebelas", 12: "duabelas", 13: "tigabelas",
    14: "empatbelas", 15: "limabelas", 16: "enambelas", 17: "tujuhbelas",
    18: "delapanbelas", 19: "sembilanbelas", 20: "duapuluh",
    25: "duapuluhlima", 30: "tigapuluh", 40: "empatpuluh", 50: "limapuluh",
    60: "enampuluh", 70: "tujuhpuluh", 80: "delapanpuluh", 90: "sembilanpuluh",
    100: "seratus", 200: "duaratus", 250: "duaratuslimapuluh",
    300: "tigaratus", 400: "empatratus", 500: "limaratus",
    600: "enamratus", 700: "tujuhratus", 800: "delapanratus", 900: "sembilanratus",
    1000: "seribu", 2000: "duaribu", 3000: "tigaribu", 4000: "empatribu", 5000: "limaribu"
}

def angka_ke_kata(angka):
    if angka in ANGKA_KE_KATA:
        return ANGKA_KE_KATA[angka]
    if 20 < angka < 100:
        puluhan = (angka // 10) * 10
        satuan = angka % 10
        nama_puluhan = {20: "duapuluh", 30: "tigapuluh", 40: "empatpuluh",
                       50: "limapuluh", 60: "enampuluh", 70: "tujuhpuluh",
                       80: "delapanpuluh", 90: "sembilanpuluh"}
        return f"{nama_puluhan[puluhan]}{ANGKA_KE_KATA[satuan]}"
    if 100 < angka < 1000:
        ratusan = (angka // 100) * 100
        sisa = angka % 100
        if sisa == 0:
            return ANGKA_KE_KATA.get(ratusan, f"{ANGKA_KE_KATA[angka//100]}ratus")
        else:
            nama_ratus = ANGKA_KE_KATA.get(ratusan, f"{ANGKA_KE_KATA[angka//100]}ratus")
            return f"{nama_ratus}{angka_ke_kata(sisa)}"
    if 1000 < angka < 10000:
        ribuan = angka // 1000
        sisa = angka % 1000
        if ribuan == 1:
            nama_ribu = "seribu"
        else:
            nama_ribu = f"{ANGKA_KE_KATA[ribuan]}ribu"
        if sisa == 0:
            return nama_ribu
        else:
            return f"{nama_ribu}{angka_ke_kata(sisa)}"
    return str(angka)

class MathChallengeHandler(socketserver.BaseRequestHandler):
    def send(self, message):
        try:
            self.request.sendall(message.encode('utf-8') + b'\n')
        except Exception as e:
            print(f"Send error: {e}")
            raise
    
    def receive(self):
        try:
            data = self.request.recv(1024).strip()
            if not data:
                return None
            return data.decode('utf-8')
        except Exception as e:
            print(f"Receive error: {e}")
            return None
    
    def generate_question(self, level):
        if level <= 10:
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            operator = '+'
            answer = a + b
        elif level <= 25:
            a = random.randint(10, 100)
            b = random.randint(1, 50)
            operator = random.choice(['+', '-'])
            answer = a + b if operator == '+' else a - b
        elif level <= 40:
            a = random.randint(5, 30)
            b = random.randint(2, 20)
            operator = '*'
            answer = a * b
        elif level <= 60:
            a = random.randint(50, 200)
            b = random.randint(10, 50)
            operator = random.choice(['+', '-', '*'])
            if operator == '+':
                answer = a + b
            elif operator == '-':
                answer = a - b
            else:
                answer = a * b
        elif level <= 80:
            a = random.randint(100, 500)
            b = random.randint(20, 100)
            operator = random.choice(['+', '-', '*'])
            if operator == '+':
                answer = a + b
            elif operator == '-':
                answer = a - b
            else:
                answer = a * b
        else:
            a = random.randint(500, 2000)
            b = random.randint(50, 500)
            operator = random.choice(['+', '-', '*'])
            if operator == '+':
                answer = a + b
            elif operator == '-':
                answer = a - b
            else:
                answer = a * b
        
        kata_a = angka_ke_kata(a)
        kata_b = angka_ke_kata(b)
        op_text = {'+': 'tambah', '-': 'kurang', '*': 'kali'}
        question = f"{kata_a} {op_text[operator]} {kata_b}"
        return question, answer
    
    def handle(self):
        try:
            self.send("=" * 50)
            self.send("    MATH CHALLENGE CTF - belajarmatematika")
            self.send("=" * 50)
            self.send("")
            self.send("Selesaikan 100 level untuk mendapatkan flag!")
            self.send("Ketik jawaban dalam angka (contoh: 25)")
            self.send("")
            self.send("    Level makin tinggi, soal makin susah!")
            self.send("    Mama ku suka emteka ")
            self.send("    tapi di aku emteka bikin ngantuk xixixi")
            self.send("")
            self.send("Contoh gerakan:")
            for angka, kata in list(ANGKA_KE_KATA.items())[:10]:
                self.send(f"  • {angka} = {kata}")
            self.send("")
            time.sleep(0.5)
            
            level = 1
            max_level = 100
            
            while level <= max_level:
                self.send(f"[Level {level}/{max_level}]")
                question, correct_answer = self.generate_question(level)
                self.send(f"Soal: {question} = ?")
                self.send("Jawaban: ")
                
                try:
                    user_answer = int(self.receive())
                except:
                    self.send("❌ Jawaban harus angka!")
                    self.send("")
                    continue
                
                if user_answer == correct_answer:
                    self.send("✓ Benar!")
                    self.send("")
                    level += 1
                    time.sleep(0.3)
                else:
                    self.send(f"❌ Salah! Jawaban yang benar: {correct_answer}")
                    self.send("Game Over! Coba lagi dari awal.")
                    return
            
            self.send("")
            self.send("=" * 50)
            self.send("🎉 SELAMAT! Kamu berhasil menyelesaikan semua level!")
            self.send("=" * 50)
            self.send("")
            self.send("Flag kamu:")
            self.send("W92{cuman_emteka_biasa_dan_pasti_seru}")
            self.send("")
            self.send("Terima kasih sudah bermain!")
            self.send("=" * 50)
            
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.request.close()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 12567
    
    print("[*] Math Challenge CTF Server")
    print(f"[*] Starting server on {HOST}:{PORT}")
    print(f"[*] Connect with: nc localhost {PORT}")
    print("[*] Press Ctrl+C to stop")
    print()
    
    try:
        with ThreadedTCPServer((HOST, PORT), MathChallengeHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped by user")
    except Exception as e:
        print(f"[!] Error: {e}")
