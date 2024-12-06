from certifi import where
from pwn import *
# from LibcSearcher import LibcSearcher
# import tqdm
# from time import *
from ctypes import *
class Pwn:
    p = file_name = elf = libc_name = libc = libclib_name = libclib = ld_name = ld = ip = port = None

    @staticmethod
    def init(File=None,Libc=None,LibcLib=None,Ld=None,Url=None,arch="amd64",os='linux',log_level='debug'):
        context(arch = arch,os=os,log_level=log_level)
        global file_name,elf,libc_name,libc,libclib_name,libclib,ld_name,ld,ip,port

        Pwn.file_name = File; Pwn.libc_name = Libc; Pwn.libclib_name = LibcLib; Pwn.ld_name = Ld
        Pwn.ip,Pwn.port = (None,None) if not Url else (Url[:Url.find(':')].strip(), Url[Url.find(':') + 1:].strip())

        if Pwn.file_name: Pwn.elf = ELF(Pwn.file_name)
        if Pwn.libc_name: Pwn.libc = ELF(Pwn.libc_name)
        if Pwn.libclib_name: Pwn.libclib = cdll.LoadLibrary(Pwn.libclib_name)
        if Pwn.ld_name: Pwn.ld = ELF(Pwn.ld_name)

    @staticmethod
    def connect(local=0):
        if local: Pwn.p = process(Pwn.file_name)
        else: Pwn.p = remote(Pwn.ip,Pwn.port)

    @staticmethod
    def db():
        gdb.attach(Pwn.p)

    libc_base = elf_base = 0

    @staticmethod
    def get_libc(model,*names): #model 0:symbols[] 1:dump()
        model = 0 if model == "symbols" else 1
        ans = []
        for name in names: ans.append(Pwn.libc_base + (Pwn.libc.dump(name) if model else Pwn.libc.symbols[name]))
        return ans

    @staticmethod
    def leak_libc(name,addr,model=0): #model 0:symbols[] 1:dump()
        Pwn.libc_base = addr - (Pwn.libc.dump(name) if model else Pwn.libc.symbols[name])
        return Pwn.libc_base

    @staticmethod
    def get_elf(*names):
        ans = []
        for i in range(0,len(names),2):
            if names[i] == 'symbols': ans += [Pwn.elf.symbols[names[i+1]]]
            elif names[i] == 'plt': ans += [Pwn.elf.plt[names[i+1]]]
            elif names[i] == 'got': ans += [Pwn.elf.got[names[i+1]]]
        return ans

    @staticmethod
    def fmt(arch,mode,base,pre,aim_addr,where_addr):
        if arch == '32' : size = 4; this_p = p32
        else : size = 8; this_p = p64
        n = 0
        aim_addr = [int(pre)] + aim_addr
        for i in range(1,len(aim_addr)):
            if mode == "hhn": # %256c%13$hhn
                n += 12
            elif mode == 'hn':  # %65536c%13$hn
                n += 8 + len(str(int((aim_addr[i]-aim_addr[i-1]+65536)%65536)))
        offset = (n-1)//size+1
        payload = ""
        for i in range(1,len(aim_addr)):
            if mode == "hhn":
                payload += f'%{(aim_addr[i]-aim_addr[i-1]+256)%256}c%{base+offset+i-1}$hhn'
            elif mode =='hn':
                payload += f'%{(aim_addr[i]-aim_addr[i-1]+65536)%65536}c%{base+offset+i-1}$hn'
        payload = payload.ljust(offset*size,'A').encode()
        for x in where_addr: payload += this_p(x)
        return payload

s       = lambda data               :Pwn.p.send(data)
sl      = lambda data               :Pwn.p.sendline(data)
sa      = lambda x,data             :Pwn.p.sendafter(x, data)
sla     = lambda x,data             :Pwn.p.sendlineafter(x, data)
r       = lambda n                  :Pwn.p.recv(n)
rl      = lambda n                  :Pwn.p.recvline(n)
ru      = lambda x                  :Pwn.p.recvuntil(x)
rud     = lambda x                  :Pwn.p.recvuntil(x, drop = True)
uu32    = lambda                    :u32(Pwn.p.recvuntil(b'\xf7')[-4:].ljust(4,b'\x00'))
uu64    = lambda                    :u64(Pwn.p.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))
pad32   = lambda *data              :b''.join([p32(x) for x in data])
pad64   = lambda *data              :b''.join([p64(x) for x in data])
leak    = lambda name,addr          :log.success('{} = {:#x}'.format(name, addr))
lg      = lambda address,data       :log.success('%s: '%(address)+hex(data))
shut    = lambda direction          :Pwn.p.shutdown(direction)
ita     = lambda                    :Pwn.p.interactive()