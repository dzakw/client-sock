import socket
import tqdm
import os
from Crypto.Cipher import AES
import io
import PIL.Image
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


SEPARATOR = "<SEPARATOR>"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 8090))


key = input(r'Enter 16 digit key')
iv = input(r'Enter 16 digit iv')

with open("key.key", "wb") as key_file:
        key_file.write(bytes(key, 'utf-8'))
with open("iv.key", "wb") as iv_file:
        iv_file.write(bytes(iv, 'utf-8'))

cwd_original_1=os.getcwd()

cwd_original=os.path.join(cwd_original_1,"Encrypted")
cwd_original_decrypt=os.path.join(cwd_original_1,"Decrypted")
#Encrypting Image
def encrypt_image():
    try:
        os.mkdir(os.path.join(cwd_original_1,"Encrypted"))
    except:
        pass
    global key,iv,filename,root
    file_path=str(filename.get())
    if(file_path=="" or file_path[0]==" "):
        file_path=os.getcwd()
    files=[]
    # r=root, d=directories, f = files
    for r, d, f in os.walk(file_path):
        for file in f:
            file_str=file.lower()
            if((".jpg" in file_str or ".png" in file_str) and ('.enc' not in file_str)):
                direc = os.path.split(r)
                cwd=os.path.join(cwd_original,direc[-1])
                try:
                    os.mkdir(cwd)
                except:
                    pass #Chill
                input_file = open((os.path.join(r,file)),"rb")
                input_data = bytearray(input_file.read())
                input_file.close()
                cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
                enc_data = cfb_cipher.encrypt(input_data)
                enc_file = open(os.path.join(cwd,file)+".enc", "wb")
                enc_file.write(enc_data)
                enc_file.close()
    root.destroy()
    root = Tk()
    root.title("Encryption Successfully Done")
    root.geometry("400x200")
    label = Label(text="Encryption Successfully Done", height=50, width=50, font=(None, 15))
    label.pack(anchor=CENTER, pady=50)
    root.mainloop()
#Decrypting Image
def decrypt_image():
    try:
        os.mkdir(os.path.join(cwd_original_1, "Decrypted"))
    except:
        pass
    global key,iv,filename,root
    file_path = str(filename.get())
    if (file_path == "" or file_path[0] == " "):
        file_path = os.getcwd()
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(file_path):
        for file in f:
            file_str=file.lower()
            if '.enc' in file_str:
                direc = os.path.split(r)
                cwd = os.path.join(cwd_original_decrypt, direc[-1])
                try:
                    os.mkdir(cwd)
                except:
                    pass #Chill
                enc_file2 = open(os.path.join(r,file),"rb")
                enc_data2 = enc_file2.read()
                enc_file2.close()

                cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
                plain_data = (cfb_decipher.decrypt(enc_data2))

                imageStream = io.BytesIO(plain_data)
                imageFile = PIL.Image.open(imageStream)
                file_str=file.lower()
                if(".jpg" in file_str):
                    imageFile.save(((os.path.join(cwd,file))[:-8])+".JPG")
                elif(".png" in file_str):
                    imageFile.save(((os.path.join(cwd, file))[:-8]) + ".png")

    root.destroy()
    root = Tk()
    root.title("Decryption Successfully Done")
    root.geometry("400x200")
    label = Label(text="Decryption Successfully Done",height=50, width=50,font=(None, 15))
    label.pack(anchor=CENTER,pady=50)
    root.mainloop()



#Tkinter Stuff

root=Tk()

root.title("Simple AES Encryption and Decryption of JPG Images")

filename=Entry(root)

def select_file():
    filetypes = (
        ('Image Files', '*.jpg'),
        ('PNG Image Files', '*.png'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )


# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)

##filename.pack()

encrypt=Button(text="Encrypt All",command=encrypt_image)
encrypt.pack()
label=Label(text="Leave Blank for Current Working Directory")
label.pack()
decrypt=Button(text="Decrypt All",command=decrypt_image)
decrypt.pack()

root.mainloop()



# msg_from_server = s.recv(4096)
# print(msg_from_server.decode('utf-8'))

filesize = os.path.getsize(filename)
s.send(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{key}{SEPARATOR}{iv}".encode())
print(f'File {filename} berhasil dikirim ke server!') #debugging

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(4096)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
s.close()
