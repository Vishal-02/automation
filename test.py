from os import path
from argparse import ArgumentParser

parser = ArgumentParser()
sub = parser.add_subparsers()
split = sub.add_parser("split")

print(type(parser))
print(type(sub))
print(type(split))