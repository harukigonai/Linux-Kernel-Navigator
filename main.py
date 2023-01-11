import os
import re
import subprocess
import sys

def run_bash(cmd):
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s = p.communicate()
    res = p.wait()
    return s

def sys_dirs(arch):
    return [
        f'arch/{arch}/include',
        f'arch/{arch}/include/generated',
        "include",
        f'arch/{arch}/include/uapi',
        f'arch/{arch}/include/generated/uapi',
        "include/uapi",
        "include/generated/uapi",
    ]

def main():
    arch = sys.argv[1]
    cmd = f'make ARCHNAME={arch}'
    s = run_bash(cmd)

    stdout_res = str(s[0])
    li = [x.group() for x in re.finditer(r'gcc (.*?) -c -o \S+ \S+', stdout_res)]
    li = set(["linux-stable/" + x.split()[-1].strip(";'\\") for x in li])

    sys_dirs_li = sys_dirs(arch)

    files_to_process = li
    files_processed = set()
    while len(files_to_process) != 0:
        nxt_files_to_process = set()
        for path in files_to_process:
            if os.path.exists(path):
                f = open(path)
                for line in f:
                    if line.startswith("#include") and ".h" in line:
                        tokens = line.split()
                        filename = tokens[1].strip().strip('"')

                        if "<" in filename and ">" in filename:
                            stripped_file = filename.strip().strip("<>")
                            file_found = False
                            for sys_dir in sys_dirs_li:
                                candidate = f'linux-stable/{sys_dir}/{stripped_file}'
                                if os.path.exists(candidate):
                                    nxt_files_to_process.add(candidate)
                                    file_found = True
                                    break

                            if not file_found:
                                # print("Couldn't find", file)
                                pass
                        else:
                            dirname = os.path.dirname(path)
                            unsimplified_path = dirname + "/" + filename
                            simplified_path = os.path.normpath(unsimplified_path)
                            nxt_files_to_process.add(simplified_path)

        files_processed = files_processed.union(files_to_process)
        files_to_process = nxt_files_to_process - files_processed

    f = open("linux-stable/cscope.files", "w")
    for file in files_processed:
        f.write(file[len("linux-stable")+1:] + "\n")

    os.chdir('linux-stable')

    cmd = f'cscope -b -q -k'
    s = run_bash(cmd)

main()

if __name__ == "main":
    main()
