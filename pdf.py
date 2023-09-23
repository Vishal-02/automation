from os import path
from argparse import ArgumentParser
from PyPDF2 import PdfReader, PdfWriter

'''
TODO:
- finish the merge_pdf function

- how to make this program a command line argument that i can access any time just by opening my cmd:
    i think i should focus on this after i'm done making the whole program
'''

def check_valid_file(org_dir):
    while True:
        if not path.isfile(org_dir):
            path = input(f"{org_dir} is not a valid file. Enter a valid file path: ")
        else:
            break

    location = ""
    if len(args.path.split("/")) == 1:
        return path.join("C:/Users/visha/Downloads", org_dir)
    else:
        return org_dir

def split_pdf(args: ArgumentParser.parse_args):
    '''
    function that splits the pdf and writes the new pdf at cwd.
    '''

    location = check_valid_file(args.path)
    start, end = pages[0], pages[1]
    reader = PdfReader(location)

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

    output = args.name
    if output.split(".")[-1] != "pdf":
        output += ".pdf"

    writer = PdfWriter()
    for i in range(start - 1, end):
        writer.add_page(reader.pages[i])
    
    writer.write(output)
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

    other.insert(first, 0)

    for pdf in other:
        merger.append(pdf)
    
    if args.name.split(".")[-1] != "pdf":
        args.name += ".pdf"

    merger.write(args.name)
    merger.close()

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

args = parser.parse_args()
args.func(args)
