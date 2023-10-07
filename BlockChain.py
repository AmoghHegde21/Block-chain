import csv
import datetime
import hashlib
import json


class BlockChain:
    def __init__(self):
        self.chain = []
        self.index = -1
        self.chain.append(self.new_block(proof=100, previous_hash=None, transactions=None))

    def new_block(self, proof, previous_hash, transactions=None):
        self.index = self.index + 1
        block = {
            'index': self.index,
            'timestamp': str(datetime.datetime.now()),
            'proof': str(proof),
            'previous_hash': previous_hash,
            'transactions': json.dumps(transactions).encode() if transactions != None else None,
            'current_hash': hashlib.sha256(json.dumps(transactions).encode()).hexdigest() if transactions != None else None
        }
        return block

    def new_transaction(self, transaction):
        proof = self.proof_of_work(self.chain[-1]['proof'])
        self.chain.append(self.new_block(proof, self.chain[-1]['current_hash'], transaction))

    def proof_of_work(self, last_proof):
        new_proof = 0
        while self.valid_proof(last_proof, str(new_proof)) is False:
            new_proof += 1
        return str(new_proof)

    def valid_proof(self, last_proof, new_proof):
        guess = last_proof.encode() + new_proof.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:2] == "00"

    def get_chain(self):
        return self.chain

my_block_chain = BlockChain()
with open('dataset.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        my_block_chain.new_transaction(row)

transaction_history = my_block_chain.get_chain()
for transaction in transaction_history:
    print(transaction)
