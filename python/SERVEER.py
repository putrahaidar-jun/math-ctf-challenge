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

KATA_KE_ANGKA = {v: k for k, v in ANGKA_KE_KATA.items()}


def kata_ke_angka(kata):
    """Convert kata bahasa Indonesia ke angka"""
    kata = kata.lower().strip().replace(" ", "").replace("-", "")
    
    if kata in KATA_KE_ANGKA:
        return KATA_KE_ANGKA[kata]
    
    if kata.startswith("min") or kata.startswith("minus"):
        kata_positif = kata.replace("min", "").replace("minus", "")
        angka_positif = kata_ke_angka(kata_positif)
        return -angka_positif if angka_positif is not None else None
    
    try:
        if "ribu" in kata:
            parts = kata.split("ribu")
            ribuan_kata = parts[0]
            sisa_kata = parts[1] if len(parts) > 1 else ""
            
            if ribuan_kata == "se":
                ribuan = 1000
            else:
                ribuan = KATA_KE_ANGKA.get(ribuan_kata, 0) * 1000
            
            sisa = kata_ke_angka(sisa_kata) if sisa_kata else 0
            return ribuan + sisa
        
        if "ratus" in kata:
            parts = kata.split("ratus")
            ratusan_kata = parts[0]
            sisa_kata = parts[1] if len(parts) > 1 else ""
            
            if ratusan_kata == "se":
                ratusan = 100
            else:
                ratusan = KATA_KE_ANGKA.get(ratusan_kata, 0) * 100
            
            sisa = kata_ke_angka(sisa_kata) if sisa_kata else 0
            return ratusan + sisa
        
        puluhan_map = {
            "duapuluh": 20, "tigapuluh": 30, "empatpuluh": 40,
            "limapuluh": 50, "enampuluh": 60, "tujuhpuluh": 70,
            "delapanpuluh": 80, "sembilanpuluh": 90
        }
        
        for puluhan_kata, nilai in puluhan_map.items():
            if kata.startswith(puluhan_kata):
                sisa_kata = kata.replace(puluhan_kata, "", 1)
                sisa = KATA_KE_ANGKA.get(sisa_kata, 0) if sisa_kata else 0
                return nilai + sisa
        
        return int(kata)
    except:
        return None


def angka_ke_kata(angka):
    """Convert angka ke kata bahasa Indonesia"""
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
    """Handler untuk setiap client yang connect"""
    
    def send(self, message):
        """Kirim message ke client"""
        try:
            self.request.sendall(message.encode('utf-8') + b'\n')
        except Exception as e:
            print(f"Send error: {e}")
            raise
    
    def receive(self):
        """Terima input dari client"""
        try:
            data = self.request.recv(1024).strip()
            if not data:
                return None
            return data.decode('utf-8')
        except Exception as e:
            print(f"Receive error: {e}")
            return None
    
    def generate_question(self, level):
        """Generate soal matematika berdasarkan level"""
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
        """Main logic untuk handle client"""
        try:
            self.send("=" * 70)
            self.send("  SELAMAT DATANG DI PERMAINAN MATEMATIKA")
            self.send("=" * 70)
            self.send("")
            self.send("ATURAN PERMAINAN:")
            self.send("• Selesaikan soal matematika untuk maju ke level yang lebih susah xixixi")
            self.send("• Soal semakin sulit seiring bertambahnya level")
            self.send("• Capai level untuk mendapatkan flag!")
            self.send("• Jawab salah dan permainan berakhir")
            self.send("")
            self.send("CARA MENJAWAB:")
            self.send("• Jawab dengan KATA-KATA dalam bahasa Indonesia")
            self.send("  Contoh: 5 = lima, 12 = duabelas, 25 = duapuluhlima")
            self.send("  Contoh: 100 = seratus, 250 = duaratuslimapuluh")
            self.send("  PENTING: Tulis dalam satu kalimat tanpa spasi!")
            self.send("")
            self.send("=" * 70)
            self.send("")
            self.send("Tekan ENTER untuk memulai...")
            
            self.receive()
            self.send("")
            
            level = 1
            max_level = 100
            
            while level <= max_level:
                self.send(f"[Level {level}/{max_level}]")
                question, correct_answer = self.generate_question(level)
                self.send(f"Soal: {question} = ?")
                self.send("Jawaban: ")
                
                try:
                    user_answer = self.receive()
                    
                    if user_answer is None or not user_answer:
                        self.send("Disconnected.")
                        return
                    
                    user_answer_angka = kata_ke_angka(user_answer)
                    
                    if user_answer_angka is None:
                        self.send("Jawaban tidak valid! Gunakan kata-kata Indonesia.")
                        self.send("Contoh: duapuluhlima, seratus, tigapuluh")
                        self.send("")
                        continue
                    
                    if user_answer_angka == correct_answer:
                        self.send("Benar!")
                        
                        if level == 10:
                            self.send("")
                            self.send("=" * 50)
                            self.send("Wow! Quarter done! Here's your flag:")
                            self.send("W92{flag_palsu_yahaha_coba_itung_lagi}")
                            self.send("=" * 50)
                        elif level == 30:
                            self.send("")
                            self.send("=" * 50)
                            self.send("Halfway there! Your flag:")
                            self.send("W92{flag_palsu_lagi_coba_lagi}")
                            self.send("=" * 50)
                        elif level == 75:
                            self.send("")
                            self.send("=" * 50)
                            self.send("Almost there! Flag unlocked:")
                            self.send("W92{hampir_mendapatkan_flagnya_zzzz}")
                            self.send("=" * 50)
                        elif level == 90:
                            self.send("")
                            self.send("=" * 50)
                            self.send("90% Complete! Your reward:")
                            self.send("W92{sangat_dekat_dengan_flagnya}")
                            self.send("=" * 50)
                        
                        self.send("")
                        level += 1
                        time.sleep(0.2)
                    else:
                        self.send(f"Salah! Jawaban yang benar: {angka_ke_kata(correct_answer)}")
                        self.send("Game Over! Coba lagi dari awal.")
                        return
                
                except Exception as e:
                    self.send(f"Error: {str(e)}")
                    return
            
            self.send("")
            self.send("=" * 50)
            self.send("SELAMAT! Kamu berhasil menyelesaikan semua level!")
            self.send("=" * 50)
            self.send("")
            self.send("THE REAL FLAG:")
            self.send("W92{emteka_enak_bukan_semangat}")
            self.send("")
            self.send("(ini, bare real bukan fake-fake)")
            self.send("selamat kamu udah bisa belajar emteka!")
            self.send("=" * 50)
            
        except ConnectionResetError:
            print(f"Client disconnected abruptly from {self.client_address}")
        except BrokenPipeError:
            print(f"Broken pipe from {self.client_address}")
        except Exception as e:
            print(f"Error handling client {self.client_address}: {e}")
        finally:
            try:
                self.request.close()
            except:
                pass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Server yang bisa handle multiple clients dengan threading"""
    allow_reuse_address = True


if __name__ == "__main__":
    HOST = "0.0.0.0"  
    PORT = 12567       
    
    print(f"[*] Math Challenge CTF Server")
    print(f"[*] Starting server on {HOST}:{PORT}")
    print(f"[*] Connect with: nc localhost {PORT}")
    print(f"[*] Press Ctrl+C to stop")
    print()
    
    try:
        with ThreadedTCPServer((HOST, PORT), MathChallengeHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped by user")
    except Exception as e:
        print(f"[!] Error: {e}")