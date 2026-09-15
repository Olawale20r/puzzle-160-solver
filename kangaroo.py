#!/usr/bin/env python3
"""
Pollard's Kangaroo Algorithm for ECDLP
Optimized for solving Puzzle 160
"""

import hashlib
import time
import os
from typing import Tuple, Optional
import logging
from config import (
    TARGET_PUBKEY, RANGE_START, RANGE_END, NUM_KANGAROOS,
    DISTINGUISHED_BITS, JUMP_TABLE_SIZE, MAX_ITERATIONS,
    PROGRESS_INTERVAL, OUTPUT_DIR, LOG_FILE, RESULT_FILE,
    P, N, GX, GY, VERBOSE, SAVE_INTERMEDIATE, SAVE_FREQUENCY
)

# Setup logging
os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Point:
    """Elliptic curve point representation"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"Point({hex(self.x)}, {hex(self.y)})"

class KangarooSolver:
    """Pollard's Kangaroo solver for discrete logarithm"""
    
    def __init__(self):
        self.P = P
        self.N = N
        self.G = Point(GX, GY)
        self.target_pubkey = self._parse_pubkey(TARGET_PUBKEY)
        self.range_start = RANGE_START
        self.range_end = RANGE_END
        self.range_size = self.range_end - self.range_start
        
        # Generate jump table
        self.jump_table = self._generate_jump_table()
        
        # Statistics
        self.iterations = 0
        self.start_time = None
        self.collisions = 0
        
        logger.info("="*70)
        logger.info("Bitcoin Puzzle 160 Solver - Pollard's Kangaroo")
        logger.info("="*70)
        logger.info(f"Target Public Key: {TARGET_PUBKEY}")
        logger.info(f"Range: {self.range_start} to {self.range_end}")
        logger.info(f"Range Size: ~2^{self.range_size.bit_length()}")
        logger.info(f"Expected iterations: ~2^{(self.range_size.bit_length()-1)//2}")
        logger.info("="*70)
    
    def _parse_pubkey(self, pubkey_hex: str) -> Point:
        """Parse compressed public key to Point"""
        pubkey_hex = pubkey_hex.lower()
        
        if pubkey_hex.startswith('02') or pubkey_hex.startswith('03'):
            # Compressed format
            prefix = pubkey_hex[:2]
            x = int(pubkey_hex[2:], 16)
            
            # Recover y from x
            y_squared = (pow(x, 3, self.P) + 7) % self.P
            y = pow(y_squared, (self.P + 1) // 4, self.P)
            
            if (y % 2 == 0 and prefix == '02') or (y % 2 == 1 and prefix == '03'):
                return Point(x, y)
            else:
                return Point(x, (self.P - y) % self.P)
        else:
            # Uncompressed format
            x = int(pubkey_hex[2:66], 16)
            y = int(pubkey_hex[66:], 16)
            return Point(x, y)
    
    def _generate_jump_table(self, table_size: int = JUMP_TABLE_SIZE) -> dict:
        """Generate pseudo-random jump distances"""
        jumps = {}
        for i in range(table_size):
            # Hash-based pseudo-random jumps
            h = hashlib.sha256(f"{i}".encode()).digest()
            jump_dist = int.from_bytes(h, 'big') % (self.range_size // 2)
            jump_dist = max(1, jump_dist)  # Ensure non-zero
            jumps[i] = jump_dist
        return jumps
    
    def _point_add(self, p1: Point, p2: Point) -> Point:
        """Add two points on the elliptic curve"""
        if p1.x == p2.x:
            if p1.y == p2.y:
                return self._point_double(p1)
            else:
                return Point(0, 0)  # Point at infinity (simplified)
        
        slope = ((p2.y - p1.y) * pow(p2.x - p1.x, -1, self.P)) % self.P
        x3 = (slope * slope - p1.x - p2.x) % self.P
        y3 = (slope * (p1.x - x3) - p1.y) % self.P
        
        return Point(x3, y3)
    
    def _point_double(self, p: Point) -> Point:
        """Double a point on the elliptic curve"""
        slope = ((3 * p.x * p.x) * pow(2 * p.y, -1, self.P)) % self.P
        x3 = (slope * slope - 2 * p.x) % self.P
        y3 = (slope * (p.x - x3) - p.y) % self.P
        
        return Point(x3, y3)
    
    def _scalar_mult(self, k: int, point: Point) -> Point:
        """Multiply a point by a scalar (binary method)"""
        if k == 0:
            return Point(0, 0)  # Point at infinity
        if k == 1:
            return point
        
        result = Point(0, 0)
        addend = point
        
        while k:
            if k & 1:
                result = self._point_add(result, addend) if result.x != 0 else addend
            addend = self._point_double(addend)
            k >>= 1
        
        return result
    
    def _is_distinguished_point(self, point: Point) -> bool:
        """Check if point is distinguished (leading bits are zero)"""
        x_val = point.x
        return (x_val >> (256 - DISTINGUISHED_BITS)) == 0
    
    def _get_jump_index(self, point: Point) -> int:
        """Get jump table index from point"""
        return (point.x + point.y) % JUMP_TABLE_SIZE
    
    def run_tame_kangaroo(self) -> dict:
        """Run tame kangaroo from known starting point"""
        logger.info("Starting Tame Kangaroo...")
        
        tame_path = {}
        a = self.range_start + self.range_size // 2  # Start at range midpoint
        p = self._scalar_mult(a, self.G)
        
        iteration = 0
        while iteration < MAX_ITERATIONS:
            if self._is_distinguished_point(p):
                tame_path[f"{p.x}:{p.y}"] = a
                if iteration % PROGRESS_INTERVAL == 0 and VERBOSE:
                    logger.info(f"Tame: Found {len(tame_path)} distinguished points, iteration {iteration}")
            
            jump_idx = self._get_jump_index(p)
            jump_dist = self.jump_table[jump_idx]
            a = (a + jump_dist) % self.N
            p = self._scalar_mult(a, self.G)
            iteration += 1
        
        logger.info(f"Tame Kangaroo completed: {len(tame_path)} distinguished points found")
        return tame_path
    
    def run_wild_kangaroo(self, tame_path: dict) -> Optional[int]:
        """Run wild kangaroo and look for collisions"""
        logger.info("Starting Wild Kangaroo...")
        
        b = self.range_start
        p = self.target_pubkey
        
        iteration = 0
        while iteration < MAX_ITERATIONS:
            if self._is_distinguished_point(p):
                key = f"{p.x}:{p.y}"
                if key in tame_path:
                    logger.info(f"\n{'='*70}")
                    logger.info("🎉 COLLISION FOUND!")
                    logger.info(f"{'='*70}\n")
                    
                    # Recover private key
                    a = tame_path[key]
                    private_key = (a - b) % self.N
                    return private_key
            
            jump_idx = self._get_jump_index(p)
            jump_dist = self.jump_table[jump_idx]
            b = (b + jump_dist) % self.N
            p = self._scalar_mult(b, self.G)
            iteration += 1
            
            if iteration % PROGRESS_INTERVAL == 0 and VERBOSE:
                logger.info(f"Wild: iteration {iteration}, b={b}")
        
        logger.info("Wild Kangaroo completed: No solution found")
        return None
    
    def solve(self) -> Optional[int]:
        """Main solver method"""
        self.start_time = time.time()
        
        try:
            # Run tame kangaroo
            tame_path = self.run_tame_kangaroo()
            
            # Run wild kangaroo
            private_key = self.run_wild_kangaroo(tame_path)
            
            if private_key:
                elapsed_time = time.time() - self.start_time
                logger.info(f"\nSolution found in {elapsed_time:.2f} seconds")
                return private_key
            else:
                logger.warning("No solution found. Consider adjusting parameters.")
                return None
        
        except Exception as e:
            logger.error(f"Error during solving: {e}", exc_info=True)
            return None

def main():
    """Main entry point"""
    solver = KangarooSolver()
    private_key = solver.solve()
    
    if private_key:
        logger.info("\n" + "="*70)
        logger.info("SOLUTION FOUND!")
        logger.info("="*70)
        logger.info(f"Private Key (HEX): {hex(private_key)}")
        logger.info(f"Private Key (DEC): {private_key}")
        logger.info("="*70 + "\n")
        
        # Save to file
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(RESULT_FILE, 'w') as f:
            f.write(f"Private Key (HEX): {hex(private_key)}\n")
            f.write(f"Private Key (DEC): {private_key}\n")
        
        logger.info(f"Result saved to {RESULT_FILE}")
    else:
        logger.error("\nFailed to find private key.")

if __name__ == "__main__":
    main()
