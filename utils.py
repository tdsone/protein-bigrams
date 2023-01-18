import string 
import numpy as np
import random

# random sequence generator
def get_random_string(length: int, alphabet: list):
    # choose from all lowercase letter
    result_str = ''.join(random.choice(alphabet) for i in range(length))
    return result_str

# pick a number from a normal distribution of a specified range of numbers
def pick_length_from_distribution(mean, std, min, max):
    # pick a number from a normal distribution of a specified range of numbers

    length = round(np.random.normal(mean, std))

    if length < min:
        length = min
    if length > max:
        length = max

    return length

if __name__ == "__main__":
    random_seqs = []
    for i in range(10000):
        length = pick_length_from_distribution(150, 30, 5, 267)
        amino_acid_alphabet = ['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','O','S','U','T','W','Y','V','B','Z','X','J']
        seq = get_random_string(length=length, alphabet=amino_acid_alphabet)
        random_seqs.append(seq)

    # write to data folder as fasta file with name random_seqs.fasta
    with open("data/random_seqs.fasta", "w") as f:
        for i, seq in enumerate(random_seqs):
            f.write(f">random_seq_{i}\n{seq}\n")

