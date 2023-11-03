import requests
# pip install biopython
from Bio import SeqIO

# Function to download a file from a URL
def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

# Function to convert FASTA to GTF or BED12
def convert_fasta_to_gtf(fasta_filename, gtf_filename):
    # This function would need to be implemented using a bioinformatics tool
    pass

# Function to prepare GTF or BED12 files for Gephi and GWAS analysis
def prepare_for_analysis(gtf_filename):
    # Read in the GTF file
    with open(gtf_filename, 'r') as gtf_file:
        gtf_lines = gtf_file.readlines()

    # Extract the relevant information from the GTF file
    nodes = set()
    edges = set()
    for line in gtf_lines:
        if line.startswith('#'):
            continue
        fields = line.strip().split('\t')
        if fields[2] == 'gene':
            node_id = fields[8].split(';')[0].split(' ')[1].strip('"')
            nodes.add(node_id)
        elif fields[2] == 'exon':
            gene_id = fields[8].split(';')[1].split(' ')[2].strip('"')
            edges.add((gene_id, node_id))

    # Write the nodes and edges to a new file
    output_filename = gtf_filename.split('.')[0] + '.txt'
    with open(output_filename, 'w') as output_file:
        output_file.write('Source\tTarget\n')
        for edge in edges:
            output_file.write(f'{edge[0]}\t{edge[1]}\n')

# Get the list of available FASTA files from the Kannapedia API - this would need to be adjusted based on the actual API
response = requests.get('https://kannapedia.net/api/v1/sequences')
fasta_urls = response.json()  # This would need to be adjusted based on the actual API response

# CALLING: Download each FASTA file, convert it to GTF, and prepare it for analysis
for i, url in enumerate(fasta_urls):
    fasta_filename = f'sequence{i}.fasta'
    gtf_filename = f'sequence{i}.gtf'
    
    download_file(url, fasta_filename)
    convert_fasta_to_gtf(fasta_filename, gtf_filename)
    prepare_for_analysis(gtf_filename)

# The GTF files are now ready for Gephi visualization and GWAS analysis

