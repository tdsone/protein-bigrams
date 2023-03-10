# Protein Bigrams: a small bigram language model for protein sequences

This repository contains a small bigram language model for protein sequences. The bigram statistics were calculated using UniRef50.

## Usage

1. Install all requirements
2. Download the dataset using the `download_dataset.py` script (approx. 6.8GB download and XXGB unzipped). For convenience, use `tmux` to run the script in the background.
3. Run `main.py` to train the model and generate sequences

Additionally, the notebook visulizes the computed bigram statistics.

Happy coding! In case of ideas, questions or bugs, please reach out at [mail@timonschneider.de](mailto:mail@timonschneider.de)

## Further ideas

- [x] Allow for using a prior distribution over amino acids (allows fine tuning)
- [ ] Provide computed bigram statistics with repo
- [ ] n-gram statistics (n > 2)
- [ ] Compute a bunch of structures and check how they look
- [ ] Phenotype -> Genotype: build function that maps sequence properties (e.g. organism) to a bigram statistic by only using data for which sequence properties apply
  - [ ] Evaluate generated sequences by using a classifier that predicts the sequence properties
- [ ] "token Multi layer bigrams" (?): i.e. tokenize and encode using BPE then do bigram statistics over all tokens

## Acknowledgements

This repository was inspired by adapting [Andrej Kaparthy's makemore](https://github.com/karpathy/makemore) to protein sequences.
