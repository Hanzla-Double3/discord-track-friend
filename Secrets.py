import json

class Secret:
    def __init__(self , filename = "secrets.json") -> None:
        self.filename = filename
        try:
            file = open(filename)
            self.data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"{filename} not found")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Invalid JSON in {filename}")
        
    def __getitem__(self, key: str) -> str:
        try:
            return self.data[key]
        except KeyError:
            raise KeyError(f"{key} not found in {self.filename}")
        
    def listSecrets(self):
        return self.data.keys()