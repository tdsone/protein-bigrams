# download uniref50 dataset in fasta format via ftp from ftp.uniprot.org/pub/databases/uniprot/uniref/uniref50


def download_file_ftp(address):
    from ftplib import FTP
    from tqdm import tqdm

    domain = address.split("/")[0]
    path = "/".join(address.split("/")[1:])
    folder = "/".join(path.split("/")[:-1])
    filename = path.split("/")[-1]

    print(f"{domain=}")
    print(f"{path=}")
    print(f"{folder=}")
    print(f"{filename=}")

    # establish connection to ftp server
    client = FTP(domain)
    client.login()

    # change working directory
    client.cwd(folder)

    with open(f"data/{filename}", "wb") as fd:
        total = client.size(filename)

        with tqdm(total=total) as pbar:

            def callback_(data):
                l = len(data)
                pbar.update(l)
                fd.write(data)

            client.retrbinary("RETR {}".format(filename), callback_)

    client.quit()


def download_uniref50():
    download_file_ftp(
        "ftp.uniprot.org/pub/databases/uniprot/uniref/uniref50/uniref50.fasta.gz"
    )


if __name__ == "__main__":
    import gzip
    import os

    # set local working directory
    os.chdir(os.getcwd())

    # downloads a single zipped fasta file with all entries
    download_uniref50()

    # unzip file and write to new file
    import gzip
    import shutil

    with gzip.open("data/uniref50.fasta.gz", "rb") as f_in:
        with open("data/uniref50.fasta", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
