import json
import os
from cryptography.fernet import Fernet
from getpass import getpass

class PassVault:
    def __init__(self, file="vault.json", keyfile="key.key"):
        self.file = file
        self.keyfile = keyfile
        self.key = self._load_key()
        self.fernet = Fernet(self.key)
        self.vault = self._load_vault()

    def _load_key(self):
        if not os.path.exists(self.keyfile):
            key = Fernet.generate_key()
            with open(self.keyfile, "wb") as f:
                f.write(key)
            return key
        with open(self.keyfile, "rb") as f:
            return f.read()

    def _load_vault(self):
        if not os.path.exists(self.file):
            return {}
        with open(self.file, "rb") as f:
            encrypted = f.read()
            try:
                decrypted = self.fernet.decrypt(encrypted)
                return json.loads(decrypted)
            except:
                return {}

    def _save_vault(self):
        encrypted = self.fernet.encrypt(json.dumps(self.vault).encode())
        with open(self.file, "wb") as f:
            f.write(encrypted)

    def add_password(self, site, username, password):
        self.vault[site] = {"username": username, "password": password}
        self._save_vault()

    def get_password(self, site):
        return self.vault.get(site, None)

    def delete_password(self, site):
        if site in self.vault:
            del self.vault[site]
            self._save_vault()

# Example usage
if __name__ == "__main__":
    pv = PassVault()
    pv.add_password("github.com", "user123", "securepass!")
    print(pv.get_password("github.com"))
