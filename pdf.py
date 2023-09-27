from os import path
from argparse import ArgumentParser
from PyPDF2 import PdfReader, PdfWriter

'''
TODO:
- how to make it so that i can access this script from anywhere on my laptop

- encrypt and decrypt functions?:
    - encrypt
    - decrypt
'''

# adds the '.pdf' at the end of the file if the user doesn't mention it themselves
add_extension = lambda x: x if x.split(".")[-1] == "pdf" else x + ".pdf"

def check_valid_file(org_dir):
    org_dir = add_extension(org_dir)

    if len(org_dir.split("/")) == 1:
        org_dir = path.join("C:/Users/visha/Downloads", org_dir).replace("/", "\\") 
    
    while True:
        if not path.isfile(org_dir):
            org_dir = input(f"{org_dir} is not a valid file. Enter a valid file path: ")
        else:
            break

    return org_dir

def split_pdf(args: ArgumentParser.parse_args):
    '''
    function that splits the pdf and writes the new pdf at cwd.
    '''

    start, end = args.pages[0], args.pages[1]
    reader = PdfReader(check_valid_file(args.path))

    # need to make sure that the start and end values aren't negative fucking integers
    while True:
        if start <= 0:
            start = int(input("First page cannot be a negative integer or zero. Enter the page to begin the split from: "))
        elif start > len(reader.pages):
            start = int(input("First page cannot be greater than length of document, enter the first page number again: "))
        elif end < 0:
            end = int(input("Invalid value for last page of split. Enter the page to end split operation: "))
        else:
            break
    
    # if you have a 10 page doc and choose to split at 100, f*ck you
    if end > len(reader.pages):
        end = len(reader.pages)


    writer = PdfWriter()
    for i in range(start - 1, end):
        writer.add_page(reader.pages[i])
    
    writer.write(add_extension(args.name))
    writer.close()

def merge_pdf(args: ArgumentParser.parse_args):
    '''
    function that merges pdf files and writes the output pdf at cwd.
    '''

    merger = PdfWriter()
    first = check_valid_file(args.first)
    other = []

    for pdfs in args.other:
        other.append(check_valid_file(pdfs))

    other.insert(0, first)

    for pdf in other:
        merger.append(pdf)

    merger.write(add_extension(args.name))
    merger.close()

def encrypt(args: ArgumentParser.parse_args):
    reader = PdfReader(check_valid_file(args.path))
    writer = PdfWriter()

    for page in len(reader.pages):
        writer.add_page(page)

    if args.type != "":
        writer.encrypt(args.pwd, args.type)
    else: writer.encrypt(args.pwd)

    # this is what's written in the documentation, but the one below should work as well
    # with open(add_extension(args.name), "wb") as f:
    #     writer.write(f)

    writer.write(add_extension(args.name))
    writer.close()

def decrypt(args: ArgumentParser.parse_args):
    reader = PdfReader(check_valid_file(args.path))
    writer = PdfWriter()


    while reader.is_encrypted:
        reader.decrpyt(args.pwd)

        if reader.is_encrypted:
            args.pwd = input("The password entered was incorrect, re-enter the password for decryption: ")

    for page in reader.pages:
        writer.add_page(page)

    # you could do this too, this is what's written in the documentation
    # with open("decrypted-pdf.pdf", "wb") as f:
    #     writer.write(f)

    writer.write(add_extension(args.name))
    writer.close()

parser = ArgumentParser(description="Parser for parsing commands to manipulate PDF files")
subparsers = parser.add_subparsers()

#subparser for split
split_parser = subparsers.add_parser("split", help="split parser")
split_parser.add_argument("--path", type=str)
split_parser.add_argument("--pages", type=int, nargs=2)
split_parser.add_argument("--name", type=str, default = "split")
split_parser.set_defaults(func=split_pdf)

# subparser for merge
merge_parser = subparsers.add_parser("merge", help="merge parser")
merge_parser.add_argument("--first", type=str, required=True)
merge_parser.add_argument("--other", type=str, required=True, nargs="+")
merge_parser.add_argument("--name", type=str, default="merged")
merge_parser.set_defaults(func=merge_pdf)

# subparser for encryption
enc_parser = subparsers.add_parser("encrypt", help="encrypt parser")
enc_parser.add_argument("--path", type=str, required=True)
enc_parser.add_argument("--pwd", type=str, required=True)
enc_parser.add_argument("--type", type=str, nargs="?", default="")
merge_parser.add_argument("--name", type=str, default="encrypted_file")
enc_parser.set_defaults(func=encrypt)

# subparser for decryption
dec_parser = subparsers.add_parser("decrpyt", help="decrypt parser")
dec_parser.add_argument("--path", type=str, required=True)
dec_parser.add_argument("--pwd", type=str, required=True)
dec_parser.add_argument("--name", type=str, default="decrypted_file")
dec_parser.set_defaults(func=decrypt)

args = parser.parse_args()
args.func(args)
