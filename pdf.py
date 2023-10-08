from argparse import ArgumentParser
from pdf_functions import *

'''
TODO:
- how to make it so that i can access this script from anywhere on my laptop

- encrypt and decrypt functions?:
    - encrypt
    - decrypt
'''

parser = ArgumentParser(description="Parser for parsing commands to manipulate PDF files")
subparsers = parser.add_subparsers()

#subparser for split
split_parser = subparsers.add_parser("split", 
                    help="split --path --pages --name")
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
enc_parser.add_argument("--name", type=str, default="encrypted_file")
enc_parser.set_defaults(func=encrypt)

# subparser for decryption
dec_parser = subparsers.add_parser("decrpyt", help="decrypt parser")
dec_parser.add_argument("--path", type=str, required=True)
dec_parser.add_argument("--pwd", type=str, required=True)
dec_parser.add_argument("--name", type=str, default="decrypted_file")
dec_parser.set_defaults(func=decrypt)

args = parser.parse_args()
args.func(args)
