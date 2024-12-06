import os
import base64
import hashlib


def make_salt():
    # 무작위 salt 값 생성
    salt = base64.b64encode(os.urandom(16))
    return salt


def hash_password(plain):
    return hashlib.sha512(plain.encode('utf-8')).hexdigest()


def create_hash(password, salt=None):
    # Generate the salt.
    PBKDF2_COMPAT_SALT_BYTES = 24
    if not salt:
        salt = ''

        if os.path.exists('/dev/urandom'):
            with open('/dev/urandom', 'rb') as f:
                salt = base64.b64encode(f.read(PBKDF2_COMPAT_SALT_BYTES)).decode('utf-8')
        else:
            for i in range(0, PBKDF2_COMPAT_SALT_BYTES, 2):
                salt += chr(os.urandom(2)[1])

            salt = base64.b64encode(salt.encode()).decode('utf-8')

    # Determine the best supported algorithm and iteration count.
    PBKDF2_COMPAT_HASH_ALGORITHM = 'sha256'
    PBKDF2_COMPAT_ITERATIONS = 12000
    PBKDF2_COMPAT_HASH_BYTES = 24

    algo = PBKDF2_COMPAT_HASH_ALGORITHM.lower()
    iterations = PBKDF2_COMPAT_ITERATIONS

    # Return format: algorithm:iterations:salt:hash
    algorithm = 'sha256'
    pbkdf2 = hash_pbkdf2(algorithm, password, salt, iterations, PBKDF2_COMPAT_HASH_BYTES, True)
    # pbkdf2 = hashlib.pbkdf2_hmac(algo, password.encode(), base64.b64decode(salt), iterations, PBKDF2_COMPAT_HASH_BYTES)
    prefix = algo if algo else 'sha1'

    return f"{prefix}:{iterations}:{salt}:{base64.b64encode(pbkdf2).decode('utf-8')}"


def hash_pbkdf2(algo, password, salt, iterations, length=0, binary=False):
    if not binary:
        length = length * 2  # Convert length from bytes to hex representation length
    dk = hashlib.pbkdf2_hmac(algo, password.encode(), salt.encode(), iterations, length)
    if binary:
        return dk
    return dk.hex()


def validate_password(password, hash):
    # Split the hash into 4 parts.
    tokens = hash.split(':')
    algo = tokens[0]
    rounds = tokens[1]
    salt = tokens[2]
    hv = tokens[3]
    return create_hash(password, salt) == hash


def slow_equals(a, b):
    # Compare two byte strings in a time-constant manner.
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0


if __name__ == '__main__':
    # sat = 'SALT'
    p = create_hash('Kch704467!', salt='vOfePPE220ccUcEHe2TOUdX9S7XXVx40')
    print(p)
    salt = 'vOfePPE220ccUcEHe2TOUdX9S7XXVx40'
    iterations = 12000
    hash_length = 24


    # print(len(p))
    # v = validate_password('123456', p)
    # print(v)

    v = validate_password('Kch704467!', 'sha256:12000:vOfePPE220ccUcEHe2TOUdX9S7XXVx40:t6iYQs9YscWr2ck+EFK4MwCNecVAApXc')
    print(v)