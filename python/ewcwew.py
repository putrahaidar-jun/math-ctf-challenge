from scapy.all import *

def create_icmp_challenge():
    """
    Membuat PCAP dengan flag tersembunyi di ICMP payload
    """
    

    flag = "flag{p1ng_h1dd3n_m3ss4g3}"
    
    print("[+] Generating ICMP Steganography Challenge")
    print(f"[+] Hidden flag: {flag}")
    
    packets = []
    

    for i in range(5):
        pkt = IP(dst="8.8.8.8")/ICMP()/Raw(load="abcdefghijklmnopqrstuvwxyz")
        packets.append(pkt)
    
   
    for char in flag:
        pkt = IP(dst="8.8.8.8")/ICMP()/Raw(load=char * 32) 
        packets.append(pkt)
    

    for i in range(5):
        pkt = IP(dst="8.8.8.8")/ICMP()/Raw(load="0123456789abcdef")
        packets.append(pkt)
    
 
    wrpcap("ping_secret.pcap", packets)
    print("[+] PCAP created: ping_secret.pcap")
    print(f"[+] Total packets: {len(packets)}")
    print("\n[*] Challenge: Find the hidden message in ICMP packets!")
    print("[*] Hint: Look at the ICMP payload data")

def solve_icmp_challenge():
    """
    Solution script untuk challenge
    """
    print("\n[+] Solving ICMP Challenge...")
    
    packets = rdpcap("ping_secret.pcap")
    hidden_message = ""
    
    for pkt in packets:
        if ICMP in pkt and Raw in pkt:
            payload = pkt[Raw].load.decode('utf-8', errors='ignore')
            if payload and payload[0].isprintable():
                if len(set(payload[:10])) == 1:
                    hidden_message += payload[0]
    
    print(f"[+] Hidden message found: {hidden_message}")

if __name__ == "__main__":
    print("=" * 60)
    print("CTF Network Steganography Challenge Generator")
    print("Soal 1: ICMP Hidden Message (Easy)")
    print("=" * 60)
    
    create_icmp_challenge()
 