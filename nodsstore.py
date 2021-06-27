import os, sys


def match_file(basename: str) -> bool:
    return basename.startswith("._") or basename == ".DS_Store"


class termcolor:
    FAIL = "\033[91m"
    OKGREEN = "\033[92m"
    ENDC = "\033[0m"


paths_to_execute = sys.argv[1:]
files_to_remove = []

for path in paths_to_execute:
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for i in filenames:
                paths_to_execute.append(dirpath + "/" + i)
    elif os.path.isfile(path):
        normalized_path = os.path.abspath(path)
        basename = os.path.basename(normalized_path)
        dirname = os.path.dirname(normalized_path)
        if match_file(basename):
            files_to_remove.append({"dirname": dirname, "basename": basename})

if len(files_to_remove) == 0:
    print("Cannot find files to remove. Directory Clean.")
    exit()

from math import ceil, log

offset = ceil(log(len(files_to_remove), 10))

print()
for count, value in enumerate(files_to_remove):
    print(
        termcolor.OKGREEN
        + str(count + 1).zfill(offset)
        + termcolor.ENDC
        + ". "
        + value["dirname"]
        + "/"
        + termcolor.OKGREEN
        + value["basename"]
        + termcolor.ENDC
    )

print()
print(
    f"Found { termcolor.OKGREEN + str(len(files_to_remove)) + termcolor.ENDC } file{('s') if len(files_to_remove) > 1 else ''}."
)
if input("Delete all? (y/n) : ").lower() == "y":
    for file in files_to_remove:
        try:
            os.remove(file["dirname"] + "/" + file["basename"])
        except:
            print(
                termcolor.FAIL
                + "× "
                + termcolor.ENDC
                + file["dirname"]
                + "/"
                + termcolor.FAIL
                + file["basename"]
                + termcolor.ENDC
            )
else:
    print("Aborted.")
