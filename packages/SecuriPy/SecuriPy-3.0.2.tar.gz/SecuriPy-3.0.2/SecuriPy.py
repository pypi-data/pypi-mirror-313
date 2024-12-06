"""Encrypter and Decrypter of Readable Messages Using Python by Anupam Kanoongo"""

class Text:
    @staticmethod    
    def pwd(message, key):
        key = list(key) 
        for i in range(len(key)):
            x = (ord(key[i]) + 100)
            key[i] = chr(x)
            
        if len(message) == len(key):
            return(key) 
        elif len(message) > len(key):
            for i in range(len(message) -len(key)):
                key.append(key[i % len(key)])
            return("" . join(key)) 
        elif len(message) < len(key):
            key = key[:len(message)]
            return("" . join(key))
        
    @staticmethod    
    def encrypt(message,password):
        message = message + " "
        key = Text.pwd(message, password)
        encrypted_text = []
        for i in range(len(message)):
            x = (ord(message[i]) +ord(key[i]) + 500)
            encrypted_text.append(chr(x))
        encrypted_text = ("" . join(encrypted_text))
        key = ("".join(key))
        return encrypted_text + " " + key

    @staticmethod
    def decrypt(text, password):
        orig_text = []
        encrypted_text = text.split(" ")[0]
        key = Text.pwd(encrypted_text, password)
        if type(key) == list:
            key = "".join(key)
        print(encrypted_text, "\n", key)
        if key == text.split(" ")[-1]:
            for i in range(len(encrypted_text)):
                x = (ord(encrypted_text[i]) -ord(key[i]) - 500)
                orig_text.append(chr(x))
            orig_text = ("" . join(orig_text))
            return orig_text[:-1]
        else:
            return "Message is corrupt or Password is incorrect"

class Image:
    @staticmethod
    def Key():
        from cryptography.fernet import Fernet
        
        key_value = Fernet.generate_key()
        
        with open("key.txt","wb") as k:
            k.write(key_value)

        with open("temp","wb") as k:
            k.write(key_value)
            
    @staticmethod
    def Encrypt(key_path, *image_paths):
        from cryptography.fernet import Fernet
        from PIL import Image
        from io import BytesIO

        def encrypt_data(data, key):
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(data)
            return encrypted_data

        def image_to_encrypted_image(image_path, output_path):
            with Image.open(image_path) as img:
                buffer = BytesIO()
                img.save(buffer, format=((image_path.split("."))[1].upper()))
                img_data = buffer.getvalue()
                
            with open(key_path,"rb") as k:
                key = k.read()
                    
            encrypted_data = encrypt_data(img_data, key)
            with open(output_path, 'wb') as f:
                f.write(encrypted_data)

        for path in image_paths:
        	encrypted_image_path = path
        	image_to_encrypted_image(path, encrypted_image_path)
        
    @staticmethod
    def Decrypt(key_path, *encrypted_image_paths):
        from cryptography.fernet import Fernet

        def decrypt_data(encrypted_data, key):
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            return decrypted_data

        def encrypted_image_to_image(image_path, output_path):
            with open(key_path,"rb") as k:
                encryption_key = k.read()
                    
            with open(image_path, 'rb') as f:
                encrypted_data = f.read()
                
            decrypted_data = decrypt_data(encrypted_data, encryption_key)
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)

        for path in encrypted_image_paths:
        	decrypted_image_path = path
        	encrypted_image_to_image(path, decrypted_image_path)

    @staticmethod
    def EncryptAll(key_path):
        import os
        images = os.listdir()

        for image in images:
            try:
                Image.Encrypt(image, key_path)
            except:
                pass

    @staticmethod
    def DecryptAll(key_path):
            import os
            images = os.listdir()

            for image in images:
                try:
                    Image.Decrypt(image, key_path)
                except:
                    pass

class File:
    @staticmethod
    def Key():
        from cryptography.fernet import Fernet
        
        with open("key.txt","wb") as k:
            k.write(Fernet.generate_key())
            
    @staticmethod
    def Encrypt(key_path, *file_paths):
        from cryptography.fernet import Fernet
        from io import BytesIO

        def encrypt_data(data, key):
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(data)
            return encrypted_data

        def file_to_encrypted_file(file_path,output_path):        
            with open(file_path, "rb") as file:
                file_data = file.read()
            with open(key_path,"rb") as k:
                    key = k.read()
            encrypted_data = encrypt_data(file_data, key)
            with open(output_path, 'wb') as f:
                f.write(encrypted_data)

        for path in file_paths: 
        	new_file_path = path
        	encryption_key = file_to_encrypted_file(path, new_file_path)

    @staticmethod
    def Decrypt(key_path, *encrypted_file_paths):
        from cryptography.fernet import Fernet

        def decrypt_data(encrypted_data, key):
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            return decrypted_data

        for path in encrypted_file_paths:
            with open(key_path,"rb") as k:
                encryption_key = k.read()
            with open(path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = decrypt_data(encrypted_data, encryption_key)

            decrypted_file_path = path
            with open(decrypted_file_path, 'wb') as f:
                f.write(decrypted_data)

    @staticmethod
    def EncryptAll(key_path):
        import os
        files = os.listdir()

        for file in files:
            File.Encrypt(file, key_path)
            
    @staticmethod
    def DecryptAll(key_path):
        import os
        files = os.listdir()

        for file in files:
            File.Decrypt(file, key_path)
            
class DNA:
    def encrypt(msg):
        conv = {
            "11": "A",
            "10": "T",
            "01": "C",
            "00": "G"
        }
        code = ""
        for char in msg:
            binary_rep = format(ord(char), '08b')
            code += binary_rep

        result = ""
        for i in range(0, len(code), 2):
            pair = code[i:i+2]
            if pair in conv:
                result += conv[pair]

        return result

    def decrypt(encoded_msg):
        conv = {
            "A": "11",
            "T": "10",
            "C": "01",
            "G": "00"
        }
        binary_code = ""
        for char in encoded_msg:
            if char in conv:
                binary_code += conv[char]

        original_msg = ""
        for i in range(0, len(binary_code), 8):
            byte = binary_code[i:i+8]
            original_msg += chr(int(byte, 2))

        return original_msg