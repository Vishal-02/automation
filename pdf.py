from PyPDF2 import PdfReader, PdfWriter
from os import path
from argparse import ArgumentParser

'''
things i need to do before i can complete this program:
- how to split a pdf using the PdfWriter:
    check out the append_pages_from_reader function
    yeah no the above doesn't work you probably gotta use the add_page function, that works way better

- how to make this program a command line argument that i can access any time just by opening my cmd:
    i think i should focus on this after i'm done making the whole program

- the "assert" command in python:
    from what i've gathered, asserts are only for unit tests. they aren't meant to be there in your main program
'''

parser = ArgumentParser(
    description="Parser for parsing commands to manipulate PDF files"
)

# current planned functions -> split a pdf
parser.add_argument(
    "--func",
    nargs="?",
    type=str,
    default="",
    help="Mention the function you would like to perform"
)

# i'm going to assume that if only a file name is provided, it's in the downloads folder
parser.add_argument(
    "-filename",
    type=str,
    default="",
    help="Path of the first PDF file"
)

# this is for the number of pages for splitting
parser.add_argument(
    "--p",
    type=int,
    nargs=2,
    help="Enter the range of pages you would like to split"
)

parser.add_argument(
    "--name",
    nargs="?",
    type=str,
    default="output",
    help="Enter the name you want for the output file"
)

args = parser.parse_args()
func = args.func
path = path.join("C:/Users/visha/Downloads", args.filename)
start, end = args.p[0], args.p[1]
output = args.name

if output.split(".")[-1] != "pdf":
    output += ".pdf"

reader = PdfReader(path)
writer = PdfWriter()

if end <= len(reader.pages):
    for i in range(end):
        writer.add_page(reader.pages[i])
writer.write(output)