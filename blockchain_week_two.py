import hashlib
import json
from time import time
from flask import Flask
from uuid import uuid4
from flask.json import jsonify
from django.http import request





class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        
        block = {

            'index': len(self.chain) + 1,

            'timestamp': time(),

            'proof': proof,


            previous_hash:  previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []

        self.chain.append(block)

        return block




        
        
        
        
        self.current_transactions = []




    @property
    def last_block(self):
        """
        calls and returns the last block of the chain
        """
        return self.chain[-1]


    def new_transaction(self, sender, recipient, amount):
        #This function adds a new transaction to already existing transactions

        '''This will create a new transaction which will be sent to the next block. It will contain

        three variables including sender, recipient and amount
        '''

        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        # Return the index of the block to which our new transaction will be added.
        return self.last_block['index'] + 1


    @staticmethod
    def hash(self, block):
       #Used for hashing a block
        '''The follow code will create a SHA-256 block hash and also ensure that the dictionary is ordered'''
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0

        while self.valid_proof(last_proof, proof) is False:

            proof += 1

        return proof


    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
 
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == '0000'



app = Flask(__name__)



blockchain = Blockchain()

node_identifier = str(uuid4()).replace('-','')

if __name__ == '__main__':

   app.run(host="0.0.0.0", port=5000)



@app.route('/mine', methods=['GET'])
def mine():
    # return "Mining a new Block"

    last_block = blockchain.last_block()


    last_proof = last_block['proof']

    proof = blockchain.proof_of_work[last_proof]



    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )


    previous_hash = blockchain.hash(last_block)

    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': 'The new block has been forged',

        'index': block['index'],

        'transactions': block['transactions'],

        'proof': block['proof'],

        'previous_hash': block['previous_hash']
        
    }

    return jsonify(response, 200)



@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # return "Adding a new transaction"

    values = request.get_json()

    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return "Missing Values", 400


    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction is scheduled to be added to Block No.{index}'}

    return jsonify(response), 201



@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200






# blockchain = Blockchain()
# t1 = blockchain.new_transaction("Satoshi", "Mike", '5 BTC')
# t2 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
# t3 = blockchain.new_transaction("Satoshi", "Hal", '5 BTC')
# blockchain.new_block(12345)


# t4 = blockchain.new_transaction("Mike", "Alice", '1 BTC')
# t5 = blockchain.new_transaction("Alice", "Bob", '0.5 BTC')
# t6 = blockchain.new_transaction("Bob", "Mike", '0.5 BTC')
# blockchain.new_block(6789)


# print("Genesis block: ", blockchain.chain)