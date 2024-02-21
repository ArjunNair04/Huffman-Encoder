import numpy as np
from collections import Counter, defaultdict
import heapq

# Huffman Tree Node class
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Function to build the Huffman tree
def build_huffman_tree(data):
    frequency = Counter(data)
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)
    
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    
    return priority_queue[0]

# Function to generate Huffman codes from the tree
def generate_codes(node, prefix="", codebook=defaultdict()):
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

# Function to calculate total and average bits required for Huffman encoded data
def calculate_huffman_data(data, codes):
    total_bits = sum(len(codes[char]) * freq for char, freq in Counter(data).items())
    average_bits = total_bits / len(data)
    return total_bits, average_bits

# Read text from a file and calculate Huffman encoding
file = open('huffmantext.txt', 'r')
data = file.read()
file.close()

# Build Huffman Tree
root = build_huffman_tree(data)

# Generate Huffman codes
huffman_codes = generate_codes(root)

# Calculate total and average bits for the encoded data
total_bits, average_bits = calculate_huffman_data(data, huffman_codes)

# Print out the results
print(f"Total number of characters: {len(data)}")
print(f"Distinct number of characters: {len(set(data))}")
print(f"Total number of bits: {total_bits}")
print(f"Average number of bits: {average_bits:.2f}")

# Print Huffman codes
print("\nHuffman Codes:")
for char, code in huffman_codes.items():
    print(f"Character: {char} | Code: {code}")

# Write the encoded data to a file
encoded_data = ''.join(huffman_codes[char] for char in data)
with open('encoded_huffmantext.txt', 'w') as encoded_file:
    encoded_file.write(encoded_data)