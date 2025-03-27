import hashlib
import json
import datetime
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(block_dict):
        return Block(
            block_dict["index"],
            block_dict["previous_hash"],
            block_dict["timestamp"],
            block_dict["data"],
            block_dict["hash"]
        )


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Crea il blocco di genesi"""
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.calculate_hash(0, "0", time.time(), "Genesis Block"))
        self.chain.append(genesis_block)

    def calculate_hash(self, index, previous_hash, timestamp, data):
        """Calcola l'hash del blocco"""
        block_string = f"{index}{previous_hash}{timestamp}{data}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def add_block(self, data):
        """Aggiungi un nuovo blocco alla blockchain"""
        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = time.time()
        previous_hash = previous_block.hash
        hash = self.calculate_hash(index, previous_hash, timestamp, data)

        new_block = Block(index, previous_hash, timestamp, data, hash)
        self.chain.append(new_block)

    def format_timestamp(self, timestamp):
        """Formatta il timestamp in un formato leggibile"""
        return datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')

    def get_chain(self):
        """Restituisce l'intera blockchain come lista di dizionari"""
        return [block.to_dict() for block in self.chain]

    def save_to_file(self, filename):
        """Salva la blockchain su un file JSON"""
        with open(filename, 'w') as file:
            json.dump([block.to_dict() for block in self.chain], file, indent=4)

    def load_from_file(self, filename):
        """Carica la blockchain da un file JSON"""
        try:
            with open(filename, 'r') as file:
                blockchain_data = json.load(file)
                self.chain = [Block.from_dict(block) for block in blockchain_data]
        except FileNotFoundError:
            print("File non trovato. Creando una nuova blockchain.")
        except json.JSONDecodeError:
            print("Errore nel formato del file JSON. Creando una nuova blockchain.")


def main():
    blockchain = Blockchain()

    # Carica la blockchain dal file, se esiste
    blockchain.load_from_file("blockchain.json")

    while True:
        print("\nMenu:")
        print("1. Visualizza la blockchain")
        print("2. Aggiungi un nuovo blocco")
        print("3. Salva la blockchain su file")
        print("4. Esci")

        choice = input("Scegli un'opzione: ")

        if choice == '1':
            # Visualizzare la blockchain
            print("\nBlockchain attuale:")
            for block in blockchain.get_chain():
                formatted_timestamp = blockchain.format_timestamp(block["timestamp"])  # Formatta il timestamp
                print(f"Indice: {block['index']}, \nData: {block['data']}, \nTimestamp: {formatted_timestamp}, \nHash: {block['hash']}")
                print("\n")
        elif choice == '2':
            # Aggiungere un nuovo blocco
            data = input("Inserisci i dati per il nuovo blocco: ")
            blockchain.add_block(data)
            print("Nuovo blocco aggiunto!")

        elif choice == '3':
            # Salvare la blockchain su file
            blockchain.save_to_file("blockchain.json")
            print("Blockchain salvata su blockchain.json")

        elif choice == '4':
            # Esci
            print("Uscendo...")
            break

        else:
            print("Opzione non valida. Riprova.")

if __name__ == "__main__":
    main()