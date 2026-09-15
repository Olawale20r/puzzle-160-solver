#!/usr/bin/env python3
"""
Verification script for found private key
Verifies that the found key matches the target public key
"""

import sys
import os
from config import TARGET_PUBKEY, TARGET_ADDRESS, RESULT_FILE, P, N, GX, GY
import hashlib
import binascii

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class PrivateKeyVerifier:
    """Verify private key against target public key"""
    
    def __init__(self):
        self.P = P
        self.N = N
        self.G = Point(GX, GY)
        self.target_pubkey = TARGET_PUBKEY
        self.target_address = TARGET_ADDRESS
    
    def point_add(self, p1: Point, p2: Point) -> Point:
        """Add two points on elliptic curve"""
        if p1.x == p2.x:
            if p1.y == p2.y:
                return self.point_double(p1)
            else:
                return Point(0, 0)
        
        slope = ((p2.y - p1.y) * pow(p2.x - p1.x, -1, self.P)) % self.P
        x3 = (slope * slope - p1.x - p2.x) % self.P
        y3 = (slope * (p1.x - x3) - p1.y) % self.P
        
        return Point(x3, y3)
    
    def point_double(self, p: Point) -> Point:
        """Double a point on elliptic curve"""
        slope = ((3 * p.x * p.x) * pow(2 * p.y, -1, self.P)) % self.P
        x3 = (slope * slope - 2 * p.x) % self.P
        y3 = (slope * (p.x - x3) - p.y) % self.P
        
        return Point(x3, y3)
    
    def scalar_mult(self, k: int, point: Point) -> Point:
        """Multiply point by scalar"""
        if k == 0:
            return Point(0, 0)
        if k == 1:
            return point
        
        result = Point(0, 0)
        addend = point
        
        while k:
            if k & 1:
                result = self.point_add(result, addend) if result.x != 0 else addend
            addend = self.point_double(addend)
            k >>= 1
        
        return result
    
    def private_key_to_pubkey(self, private_key: int) -> str:
        """Convert private key to compressed public key"""
        point = self.scalar_mult(private_key, self.G)
        
        # Determine prefix
        prefix = '02' if point.y % 2 == 0 else '03'
        pubkey = prefix + format(point.x, '064x')
        
        return pubkey
    
    def pubkey_to_address(self, pubkey: str) -> str:
        """Convert public key to Bitcoin address"""
        # This is simplified - real implementation needs proper Bitcoin encoding
        pubkey_bytes = binascii.unhexlify(pubkey)
        
        # SHA256
        s = hashlib.sha256(pubkey_bytes).digest()
        
        # RIPEMD160
        import hashlib
        h = hashlib.new('ripemd160')
        h.update(s)
        h = h.digest()
        
        # Add version byte
        h = b'\x00' + h
        
        # Add checksum
        checksum = hashlib.sha256(hashlib.sha256(h).digest()).digest()[:4]
        address_bytes = h + checksum
        
        # Base58 encode
        return self._base58_encode(address_bytes)
    
    def _base58_encode(self, v: bytes) -> str:
        """Base58 encode"""
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        p, acc = 1, 0
        for c in reversed(v):
            acc += p * c
            p = p * 256
        result = ''
        while acc:
            acc, mod = divmod(acc, 58)
            result = alphabet[mod] + result
        return result
    
    def verify(self, private_key: int) -> bool:
        """Verify private key"""
        print("\n" + "="*70)
        print("VERIFICATION SCRIPT - Puzzle 160")
        print("="*70 + "\n")
        
        print(f"Private Key (DEC): {private_key}")
        print(f"Private Key (HEX): {hex(private_key)}\n")
        
        # Generate public key from private key
        generated_pubkey = self.private_key_to_pubkey(private_key)
        print(f"Generated Public Key: {generated_pubkey}")
        print(f"Target Public Key:   {self.target_pubkey}")
        
        # Check match
        if generated_pubkey == self.target_pubkey:
            print("\n✅ PUBLIC KEY MATCH! ✅\n")
            return True
        else:
            print("\n❌ PUBLIC KEY MISMATCH ❌\n")
            return False

def main():
    """Main verification"""
    
    # Check if result file exists
    if not os.path.exists(RESULT_FILE):
        print(f"\nError: Result file '{RESULT_FILE}' not found.")
        print("Run kangaroo.py first to generate results.\n")
        return False
    
    # Read private key from result file
    with open(RESULT_FILE, 'r') as f:
        content = f.read()
        if 'HEX' in content:
            for line in content.split('\n'):
                if 'HEX' in line:
                    private_key_hex = line.split(':')[-1].strip()
                    private_key = int(private_key_hex, 16)
                    break
        else:
            private_key = int(content.strip())
    
    # Verify
    verifier = PrivateKeyVerifier()
    is_valid = verifier.verify(private_key)
    
    if is_valid:
        print("="*70)
        print("✨ PUZZLE 160 SOLVED! ✨")
        print("="*70)
        print(f"Bitcoin Address: {TARGET_ADDRESS}")
        print("="*70 + "\n")
    
    return is_valid

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
