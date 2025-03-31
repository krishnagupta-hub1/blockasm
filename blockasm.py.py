import time

# Custom hash function using basic mathematical operations
def custom_hash(data):
    # Simple hash: sum of ASCII values of characters, multiplied by a constant
    return str(sum(ord(char) for char in data) * 2654435761 % (2**32))  # Converted to string

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        # Combine block attributes into a string
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return custom_hash(block_string)  # Returning as string

    def proof_of_work(self, difficulty):
        # Proof of Work: find a hash with a specific number of leading zeros
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), data, previous_block.hash)
        new_block.proof_of_work(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.compute_hash():
                print(f"Hash mismatch at block {i}")
                return False

            if current_block.previous_hash != previous_block.hash:
                print(f"Previous hash mismatch at block {i}")
                return False

        return True

# Example usage
if __name__ == "__main__":
    my_blockchain = Blockchain(difficulty=3)

    my_blockchain.add_block("First block after genesis")
    my_blockchain.add_block("Second block after genesis")

    for block in my_blockchain.chain:
        print(f"Block {block.index} Hash: {block.hash}")

    print("Is blockchain valid?", my_blockchain.is_chain_valid())
