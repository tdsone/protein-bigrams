# example showing how the model can be fine tuned

import torch
from main import _calc_bigram_counts, get_probs_from_counts, get_entries_from_fasta, get_token_idx_map, TOKENS, generate_proteins

# prior weight determines how much influence the prior has on the posterior
# valid values: [0,inf)
# e.g.: 
# 0 means ignore prior completely (equivalent to from scratch model training)
# 1.0 is equivally weighting the prior and the fine tune
PRIOR_WEIGHT = 1.0

# load prior (bigram counts from general training)
prior = torch.load("example_prior.pt") * PRIOR_WEIGHT

# read fine tuned samples from fasta
entries = get_entries_from_fasta(path='data/fine_tune.fasta')

# build index maps for tokens
ttoi, itot = get_token_idx_map(TOKENS)

# build fine tuned bigram
bigram_counts = _calc_bigram_counts(entries, ttoi, prior)
bigram_probs = get_probs_from_counts(bigram_counts)

sequences = generate_proteins(ttoi, itot, bigram_probs, count=100)

with open(f'generations/fine_tuned.fasta', "w+") as f:
    for idx, s in enumerate(sequences):
        f.write(f">seq{idx}\n{s}\n")
