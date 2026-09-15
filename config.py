#!/usr/bin/env python3
"""
Configuration for Puzzle 160 Solver
Defines all parameters for Pollard's Kangaroo algorithm
"""

# ============================================================================
# PUZZLE 160 PARAMETERS
# ============================================================================

# Target Bitcoin Address
TARGET_ADDRESS = "1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv"

# Target Public Key (Compressed)
TARGET_PUBKEY = "02e0a8b039282faf6fe0fd769cfbc4b6b4cf8758ba68220eac420e32b91ddfa673"

# Known Range (Private Key exists in this range)
# Approximately 2^128
RANGE_START = 730750818665451459101842416358141509827966271488
RANGE_END = 1461501637330902918203685753292512604949051373824  # ~2x range start

# Range size (for calculation)
RANGE_SIZE = RANGE_END - RANGE_START

# ============================================================================
# ALGORITHM PARAMETERS
# ============================================================================

# Number of kangaroos (tame + wild)
NUM_KANGAROOS = 4  # Adjust based on available memory

# Distinguished point prefix (probability 2^-16)
DISTINGUISHED_BITS = 16

# Jump table size (affects memory usage)
JUMP_TABLE_SIZE = 256

# Maximum iterations before restart
MAX_ITERATIONS = 10_000_000

# Update interval for progress reporting (iterations)
PROGRESS_INTERVAL = 100_000

# ============================================================================
# EXECUTION PARAMETERS
# ============================================================================

# Enable GPU acceleration (CUDA)
USE_GPU = True

# Number of parallel processes
PARALLEL_PROCESSES = 4

# Output directory
OUTPUT_DIR = "results"

# Log file
LOG_FILE = f"{OUTPUT_DIR}/puzzle_160.log"

# Result file
RESULT_FILE = f"{OUTPUT_DIR}/PRIVATEKEY.txt"

# ============================================================================
# SECP256K1 CURVE PARAMETERS
# ============================================================================

# Prime field modulus
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

# Curve order (total number of valid private keys)
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Generator point coordinates
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

# ============================================================================
# VERBOSITY & DEBUGGING
# ============================================================================

# Print detailed progress
VERBOSE = True

# Save intermediate results
SAVE_INTERMEDIATE = True

# Save frequency (every N iterations)
SAVE_FREQUENCY = 1_000_000
