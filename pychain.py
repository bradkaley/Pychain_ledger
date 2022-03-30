# PyChain Ledger

#This script includes the creation of a blockchain based ledger system of transactions 
# for deployment via Streamlit.

################################################################################
# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

# Create a Record Data Class that consists of the `sender`, `receiver`, and
# `amount` attributes
@dataclass
class Record:
    sender: str
    receiver: str
    amount: float

@dataclass
class Block:

    # Rename the `data` attribute to `record`, and set the data type to `Record`
    record: Record

    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()

@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

################################################################################
# Streamlit Code

# Adds the cache decorator for Streamlit
@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])

st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()

# Add other relevant input areas for the user interface of the Streamlit
# application. Create these input areas to capture the sender, receiver, and
# amount for each transaction that is stored in the `Block` record.

# Add an input area where to get a value for `sender` from the user.
input_sender = st.text_area("Sender")

# Add an input area to get a value for `receiver` from the user.
input_receiver = st.text_area("Receiver")

# Add an input area to get a value for `amount` from the user.
input_amount = st.text_area("Amount")

if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    # Update `new_block` so that `Block` consists of an attribute named `record`
    # which is set equal to a `Record` that contains the `sender`, `receiver`,
    # and `amount` values
    new_block = Block(
        Record(
            sender = input_sender,
            receiver = input_receiver,
            amount=input_amount
        ),
        creator_id = 100, #Arbitray creator id set here - can make it an input later
        prev_hash = prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()

st.markdown("## The PyChain Ledger")

pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(pychain.is_valid())

################################################################################
# Test the completed `PyChain` ledger and user interface by running the
# Streamlit application using `streamlit run pychain.py` (after navigating to the 
# project folder where the code is stored). Then, store some mined blocks in the 
# `PyChain` ledger and test the validation process.

# Once in the application, enter values for the sender, receiver, and amount, and 
# then click the "Add Block" button. Do this several times to store several blocks
# in the ledger.

# Test the blockchain validation process by using the web interface. The streamlit 
# application page should indicate the validity of the blockchain.