# Bitcoin Puzzle 160 Solver

## Objective
Find the private key for Bitcoin address: `1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv`

Public Key: `02e0a8b039282faf6fe0fd769cfbc4b6b4cf8758ba68220eac420e32b91ddfa673`

## Known Range
The private key exists within this range:
```
730750818665451459101842416358141509827966271488
```

This is approximately **2^128**, making this a Medium-difficulty puzzle.

## Algorithm: Pollard's Kangaroo

Pollard's Kangaroo algorithm is one of the fastest methods for solving discrete logarithm problems in a known range.

### Time Complexity
- **O(√n)** where n is the range size
- For 2^128 range: ~2^64 operations needed
- Parallelizable across multiple GPUs

### How It Works
1. **Setup Phase**: Define tame and wild kangaroos with pseudo-random jumps
2. **Jumping Phase**: Both kangaroos jump through the elliptic curve
3. **Collision Detection**: When paths collide, solve for the private key
4. **Verification**: Verify the found key matches the public key

## Project Structure

```
puzzle-160-solver/
├── README.md
├── kangaroo.py              # Main Pollard's Kangaroo implementation
├── config.py                # Configuration for Puzzle 160
├── verify.py                # Verification script
├── puzzle_160_solver.ipynb  # Google Colab notebook
├── requirements.txt         # Python dependencies
└── results/                 # Output directory for results
```

## Quick Start

### Option 1: Google Colab (Recommended for GPU)
1. Open `puzzle_160_solver.ipynb` in Google Colab
2. Click "Run All" cells
3. Monitor progress in real-time

### Option 2: Local Installation

```bash
# Clone repository
git clone https://github.com/Olawale20r/puzzle-160-solver.git
cd puzzle-160-solver

# Install dependencies
pip install -r requirements.txt

# Run solver
python kangaroo.py

# Verify result
python verify.py
```

## Expected Output

Once the private key is found:
```
Private Key (HEX): [64 hex characters]
Private Key (DEC): [128-bit integer]
Bitcoin Address: 1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv ✓ VERIFIED
```

## Performance Tips

- **GPU Acceleration**: Use CUDA-enabled GPU for 10-100x speedup
- **Parallelization**: Run multiple instances with different jump tables
- **Memory Optimization**: Adjust table sizes in config.py
- **Google Colab**: Free GPU access, unlimited runtime with pro subscription

## References

- [Pollard's Kangaroo Algorithm](https://en.wikipedia.org/wiki/Pollard%27s_kangaroo_algorithm)
- [ECDLP and Discrete Logarithm](https://cryptodeeptech.ru/kangaroo/)
- [Bitcoin Address Verification](https://www.blockchain.com/btc/address/1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv)

## Status

🔄 In Progress - Solver running

## License

MIT
