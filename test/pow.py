import hashlib

def proof_of_work(last_hash, difficulty):
    """
    Simple Proof of Work Algorithm:
    - Find a nonce such that hash(last_hash + nonce) has a certain number of leading zeroes (difficulty)
    """
    nonce = 0
    prefix = '0' * difficulty
    while True:
        text = f"{last_hash}{nonce}"
        hash_result = hashlib.sha256(text.encode()).hexdigest()
        if hash_result.startswith(prefix):
            return nonce, hash_result
        nonce += 1