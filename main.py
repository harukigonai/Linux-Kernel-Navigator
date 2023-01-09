import os
import re
import subprocess
import sys

def filter_files(li):
    files = set()
    for filename in li:
        if ".o" in filename or ".c" in filename:
            res = os.path.splitext(filename)[0]
            files.add(res)
    return files

def main():
    bashCommand = f'make ARCHNAME={sys.argv[1]}'
    p = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s = p.communicate()
    res = p.wait()

    stdout_res = str(s[0])
    li = [x.group() for x in re.finditer(r'gcc (.*?) -c -o \S+ \S+', stdout_res)]
    li = sorted(list(set([x.split()[-1].strip(";'\\") for x in li])))
    print("\n".join(li))

main()

if __name__ == "main":
    main()
