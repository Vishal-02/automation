import os
import argparse

# custom exception class
class EmptyValueError(Exception):
    def __init__(self, var="", *args) -> None:
        self.var = var
        print(f"The {var} parameter cannot be left blank.")

        super(EmptyValueError, self).__init__(var, *args)

parser = argparse.ArgumentParser(
    description="Test parser"
)

# add 'path' argument
parser.add_argument(
    "--path",
    type=str,
    default=".",
    help="Directory of the folder with files to be renamed"
)

# add 'search' argument
parser.add_argument(
    "--s",
    type=str,
    default="",
    help="Enter the word to be replaced"
)

# add 'replace' argument
parser.add_argument(
    "--r",
    type=str,
    default="",
    help="Enter the word to do the replacing"
)

# add 'type' argument
parser.add_argument(
    "--type",
    type=str,
    default=".txt",
    help="Enter the file extension of the target file. Default value is .txt"
)

args = parser.parse_args()
search = args.s
replace = args.r
type_filter = args.type
path = os.path.join(os.getcwd(), args.path)

# make sure you get valid string values for 'search' and 'replace'
while True:
    flag = False
    try:
        if search == "":
            raise EmptyValueError("search")
        if replace == "":
            raise EmptyValueError("replace")
        flag = True
    except EmptyValueError as e:
        if str(e) == "search":
            search = input("Enter a value for search: ")
        elif str(e) == "replace":
            replace = input("Enter a value for replace: ")

    if flag:
        break

docs = os.listdir(path)
renamed = 0

# loop for name replacement
for doc in docs:
    # check if it's a file or not, check the type of file
    new_path = os.path.join(path, doc)
    _, _type = os.path.splitext(doc)
    if not os.path.isfile(new_path) or _type != type_filter:
        continue
    
    # change to 'replace' if search is in the name of the file
    if search in _:
        new_name = doc.replace(search, replace)
        os.rename(new_path, os.path.join(path, new_name))
        renamed += 1

print(f"A total of {renamed} files were renamed!")

