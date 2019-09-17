#!~/.pyvenvs/elliptic_curve
# -*- coding: utf-8 -*-

"""A simple implementation of Diffie Hellman Elliptic Curve Crypto 

Functions
-----------
f(str, int): finds the int in the str and returns the index
"""

import os
import sys
import secrets
import time

# Curve constants
secp256k1_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
secp256k1_A = 0x0
secp256k1_B = 0x7
secp256k1_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
secp256k1_Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
secp256k1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
secp256k1_H = 0x1


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


class CurveParams(object):
    """This class defines the public parameters for the curve"""

    def __init__(self, p, a, b, Gx, Gy, n, h):
        self.p = p
        self.a = a
        self.b = b
        self.G = Point(Gx, Gy)
        self.n = n
        self.h = h
        self.O = "Origin"


def valid(P, params):
    if P == params.O:
        return True
    else:
        return (
            (P.y ** 2 - (P.x ** 3 + params.a * P.x + params.b)) % params.p == 0
            and 0 <= P.x < params.p
            and 0 <= P.y < params.p
        )


def inv_mod(x, params):
    assert x % params.p != 0

    # This is the inverse by Fermat's Little Theorem
    return pow(x, params.p - 2, params.p)


def ec_add(P, Q, params):
    assert valid(P, params) and valid(Q, params)

    if P == params.O:
        result = Q
    elif Q == params.O:
        result = P
    elif Q.x == P.x and Q.y != P.y:
        result = params.O
    else:
        dydx = (Q.y - P.y) * inv_mod(Q.x - P.x, params)

        x = (dydx ** 2 - P.x - Q.x) % params.p
        y = (dydx * (P.x - x) - P.y) % params.p

        result = Point(x, y)

    assert valid(result, params)
    return result


def ec_double(P, params):
    assert valid(P, params)

    if P == params.O:
        result = P
    else:
        dydx = (3 * P.x ** 2 + params.a) * inv_mod(2 * P.y, params)
        x = (dydx ** 2 - P.x - P.x) % params.p
        y = (dydx * (P.x - x) - P.y) % params.p

        result = Point(x, y)

    assert valid(result, params)
    return result


# using double and add method for log_2(k) complexity
def ec_mult(P, k, params):
    if not (valid(P, params)):
        raise ValueError("Invalid Point")

    bits = f"{k:b}"[::-1]

    Q = params.O
    N = P
    for bit in bits:
        if bit == "1":
            Q = ec_add(Q, N, params)
        N = ec_double(N, params)

    return Q


def get_priv_key(params):
    return secrets.randbelow(params.n)


def pp(P):
    try:
        print(f"({P.x}, {P.y})")
    except:
        print(P)


# Calculate the value to be sent
def dh_phase_1(priv_key, params):
    return ec_mult(params.G, priv_key, params)


# Calculate shared secret with recieved value
def dh_phase_2(priv_key, P, params):
    return ec_mult(P, priv_key, params)


# def main(args):

# 	params = CurveParams(30, secp256k1_A,
# 		secp256k1_B, secp256k1_Gx, secp256k1_Gy, secp256k1_N, secp256k1_H)

# 	# Alice
# 	alice_priv_key = get_priv_key(params)
# 	send_to_bob = dh_phase_1(alice_priv_key, params)

# 	# Bob
# 	bobs_priv_key = get_priv_key(params)
# 	send_to_alice = dh_phase_1(bobs_priv_key, params)

# 	# Alice
# 	shared_secret_alice = dh_phase_2(alice_priv_key, send_to_alice, params)

# 	# Bob
# 	shared_secret_bob = dh_phase_2(bobs_priv_key, send_to_bob, params)

# 	assert (shared_secret_bob == shared_secret_alice)


# 	# pp(shared_secret_alice)
# 	print(inv_mod(2, params))


# if __name__ == '__main__':
# 	sys.exit(main(sys.argv))
