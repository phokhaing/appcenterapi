from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64

class IdEncryption:
    # Define a secret key for AES encryption (should be 16, 24, or 32 bytes)
    secret_key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10'

    @classmethod
    def encrypt_id(cls, id, prefix='ASS'):
        # Convert the ID to bytes
        id_bytes = str(f"{id}{prefix}").encode()

        # Pad the data to the block size
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(id_bytes) + padder.finalize()

        # Create an AES cipher object
        cipher = Cipher(algorithms.AES(cls.secret_key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()

        # Encrypt the data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Encode the result in base64 (URL-safe variant) to get a string
        encrypted_id_string = base64.urlsafe_b64encode(encrypted_data).decode()

        return encrypted_id_string

    @classmethod
    def decrypt_id(cls, encrypted_id, prefix='ASS'):
        # Decode the base64 (URL-safe variant) string
        encrypted_data = base64.urlsafe_b64decode(encrypted_id)

        # Create an AES cipher object
        cipher = Cipher(algorithms.AES(cls.secret_key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the data
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Unpad the decrypted data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        id_bytes = unpadder.update(decrypted_data) + unpadder.finalize()

        # Convert bytes back to a string
        decrypted_id = id_bytes.decode()

        # Remove the prefix
        decrypted_id = decrypted_id.replace(prefix, '', 1)
           
        return decrypted_id
    
# # Example usage
# original_id = 1
# with prefix = "Ass" or other 

# # Create an instance of IdEncryption
# id_encryptor = IdEncryption()

# encrypted_id = id_encryptor.encrypt_id(original_id)
# print("Encrypted ID:", encrypted_id)

# decrypted_id = id_encryptor.decrypt_id(encrypted_id)
# print("Decrypted ID:", decrypted_id)
