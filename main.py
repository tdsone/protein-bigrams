import torch

AMINO_ACIDS = ['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','O','S','U','T','W','Y','V','B','Z','X','J']
END_TOKEN = ['.']
TOKENS = END_TOKEN + AMINO_ACIDS


# read entries from fasta file and return as array
def get_entries_from_fasta(path):
    from Bio import SeqIO
    return list(SeqIO.parse(path, "fasta"))

# build map to swap easily between chars and idxs
def get_token_idx_map(tokens): 
    """returns two dicts that map from tokens to idx and reverse

    Args:
        tokens (list[str]): tokens to make bigram statistics over

    Returns:
        ttoi, itot: dicts
    """
    ttoi = {char: idx for idx, char in enumerate(tokens)}
    itot = {value: key for key, value in ttoi.items()}
    return ttoi, itot

# calculate bigram counts
def calc_bigram_counts(entries, token_to_idx, tokens) -> torch.tensor:
    bigram_counts = torch.zeros(len(tokens), len(tokens))

    for record in entries:
        seq = "." + record.seq + "."
        for idx in range(len(seq) - 1):
            bigram = seq[idx : idx + 2]
            i, j = [token_to_idx[token] for token in bigram]
            bigram_counts[i, j] += 1

    return bigram_counts


def get_probs_from_counts(counts: torch.tensor):
    # transform into probabilities by normalizing them row wise
    bigram_probs = counts.float() / counts.sum(keepdim=True, dim=1)
    # if no count exists we assume uniform probability distribution
    bigram_probs = torch.nan_to_num(bigram_probs, 1 / 27)

    return bigram_probs


def generate_proteins(ttoi, itot, bigram_probs, count):
    g = torch.Generator().manual_seed(328923)
    sequences = []
    
    for i in range(count):
        sequence = "."
        last_token = ""

        # random number gen

        # draw new aas from bigram statistics until stop token
        while last_token != ".":
            curr_token_idx = ttoi[last_token] if last_token != "" else ttoi["."]
            # draw from bigram
            next_token_idx = torch.multinomial(
                bigram_probs[curr_token_idx], num_samples=1, replacement=True, generator=g
            ).item()
            next_token = itot[next_token_idx]
            sequence += next_token
            last_token = next_token

        sequences.append(sequence[1:-1])
    
    return sequences

def run_pipeline(count=100):
    # read all uniref entries into array
    entries = get_entries_from_fasta(path='data/example.fasta')
    
    # build index maps for tokens
    ttoi, itot = get_token_idx_map(TOKENS)
    
    # build bigram
    bigram_counts = calc_bigram_counts(entries, ttoi, TOKENS)
    bigram_probs = get_probs_from_counts(bigram_counts)
    
    return generate_proteins(ttoi, itot, bigram_probs, count), bigram_probs

if __name__ == '__main__':
    # run pipeline to generate 100 proteins
    proteins, bigram_probs = run_pipeline(count=100)
    
    from pprint import pprint
    pprint(proteins)
    
