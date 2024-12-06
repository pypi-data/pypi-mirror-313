from .database import TransactionDatabase

cdef class TransactionTest:
    cdef str sender
    cdef str receiver
    cdef float amount

    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def details(self):
        return f"Transaction from {self.sender} to {self.receiver} of amount {self.amount}"

cdef class Transaction:
    """
    A Cython-optimized transaction class for high-performance cryptocurrency operations.
    
    Attributes:
        sender (str): The transaction initiator
        receiver (str): The transaction recipient
        amount (float): The transaction amount
    
    Methods:
        details(): Returns a formatted transaction summary
    """
    cdef str sender
    cdef str receiver
    cdef float amount
    cdef object db
    
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.db = TransactionDatabase()
    
    def details(self):
        return f"Transaction from {self.sender} to {self.receiver} of amount {self.amount}"
    
    def execute(self):
        # Check if sender has sufficient balance
        current_balance = self.db.get_balance(self.sender)
        if current_balance < self.amount:
            raise ValueError(f"Insufficient balance: {current_balance} < {self.amount}")
        
        # Record the transaction
        transaction_id = self.db.record_transaction(self)
        return transaction_id
    
    def get_sender_balance(self):
        return self.db.get_balance(self.sender)
    
    def get_receiver_balance(self):
        return self.db.get_balance(self.receiver)
