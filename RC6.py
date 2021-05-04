import math
def ROR(x, n, bits = 32):
    mask = (2**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))

def ROL(x, n, bits = 32):
    return ROR(x, bits - n,bits)

def blockConverter(sentence):
    encoded = []
    res = ""
    for i in range(0,len(sentence)):
        if i%4==0 and i!=0 :
            encoded.append(res)
            res = ""
        temp = bin(ord(sentence[i]))[2:]
        if len(temp) <8:
            temp = "0"*(8-len(temp)) + temp
        res = res + temp
    print(encoded)
    encoded.append(res)
    return encoded

def deBlocker(blocks):
    s = ""
    for ele in blocks:
        temp =bin(ele)[2:]
        if len(temp) <32:
            temp = "0"*(32-len(temp)) + temp
        for i in range(0,4):
            s=s+chr(int(temp[i*8:(i+1)*8],2))
    return s

# w - nr bits pentru cheie
# r - nr de runde
class RC6():
    def __init__(self, key, w = 32, r = 12):
        self.w = w
        self.r = r
        self.b = len(key)
        self.key = key

    def generate_s(self):
        modulo = 2**32
        s=(2*self.r+4)*[0]
        s[0]=0xB7E15163
        for i in range(1,2*self.r+4):
            s[i]=(s[i-1]+0x9E3779B9)%(2**self.w)
        encoded = blockConverter(self.key)
        enlength = len(encoded)
        l = enlength*[0]
        for i in range(1,enlength+1):
            l[enlength-i]=int(encoded[i-1],2)
        v = 3*max(enlength,2*self.r+4)
        A=B=i=j=0
        for index in range(0,v):
            A = s[i] = ROL((s[i] + A + B)%modulo,3,32)
            B = l[j] = ROL((l[j] + A + B)%modulo,(A+B)%32,32) 
            i = (i + 1) % (2*self.r + 4)
            j = (j + 1) % enlength
        return s

    def encrypt(self, msg):
        idx = 0
        sub_msgs = []
        while idx < len(msg):
            sub_msgs.append(msg[idx:idx+16])
            idx += 16
        cipher_rez = ""
        s = self.generate_s()
        for msg in sub_msgs:
            if len(msg) < 16:
                msg = msg + " "*(16-len(msg))
            msg = msg[:16]
            encoded = blockConverter(msg)
            enlength = len(encoded)
            A = int(encoded[0],2)
            B = int(encoded[1],2)
            C = int(encoded[2],2)
            D = int(encoded[3],2)
            orgi = []
            orgi.append(A)
            orgi.append(B)
            orgi.append(C)
            orgi.append(D)
            modulo = 2**32
            lgw = 5
            B = (B + s[0])%modulo
            D = (D + s[1])%modulo
            for i in range(1,self.r+1):
                t_temp = (B*(2*B + 1))%modulo
                t = ROL(t_temp,lgw,32)
                u_temp = (D*(2*D + 1))%modulo
                u = ROL(u_temp,lgw,32)
                tmod=t%32
                umod=u%32
                A = (ROL(A^t,umod,32) + s[2*i])%modulo
                C = (ROL(C^u,tmod,32) + s[2*i+ 1])%modulo
                (A, B, C, D)  =  (B, C, D, A)
            A = (A + s[2*self.r + 2])%modulo
            C = (C + s[2*self.r + 3])%modulo
            cipher = []
            cipher.append(A)
            cipher.append(B)
            cipher.append(C)
            cipher.append(D)
            cipher = deBlocker(cipher)
            cipher_rez += cipher
        return cipher_rez

    def decrypt(self, msg_cyph):
        s = self.generate_s()
        idx = 0
        sub_msgs = []
        while idx < len(msg_cyph):
            sub_msgs.append(msg_cyph[idx:idx+16])
            idx += 16
        msg_rez = ""
        for msg in sub_msgs:
            encoded = blockConverter(msg)
            enlength = len(encoded)
            A = int(encoded[0],2)
            B = int(encoded[1],2)
            C = int(encoded[2],2)
            D = int(encoded[3],2)
            modulo = 2**32
            lgw = 5
            C = (C - s[2*self.r+3])%modulo
            A = (A - s[2*self.r+2])%modulo
            for j in range(1,self.r+1):
                i = self.r+1-j
                (A, B, C, D) = (D, A, B, C)
                u_temp = (D*(2*D + 1))%modulo
                u = ROL(u_temp,lgw,32)
                t_temp = (B*(2*B + 1))%modulo
                t = ROL(t_temp,lgw,32)
                tmod=t%32
                umod=u%32
                C = (ROR((C-s[2*i+1])%modulo,tmod,32)^u)
                A = (ROR((A-s[2*i])%modulo,umod,32)^t)
            D = (D - s[1])%modulo
            B = (B - s[0])%modulo
            orgi = []
            orgi.append(A)
            orgi.append(B)
            orgi.append(C)
            orgi.append(D)
            msg_rez += deBlocker(orgi)
        return msg_rez

if __name__ == "__main__":
    key = "A WORD IS A WORD"
    msg = "Fqweqweqweqwdsdfsdfsdfsf"
    rc6 = RC6(key)
    cipher = rc6.encrypt(msg)
    msg = rc6.decrypt(cipher)