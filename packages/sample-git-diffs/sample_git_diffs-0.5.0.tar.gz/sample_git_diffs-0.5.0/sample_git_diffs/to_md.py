import argparse
import re

FILE_EXP = re.compile("diff.*a/.*b/.*")
DIFF_START_EXP = re.compile("@@.*@@.*")

def main(args):
    current_filepath = None
    diffs = []
    metadata = []
    current_diff_line = None

    with open(args.path) as f:
        s = f.read()

    for l in s.split("\n"):
        file_m = FILE_EXP.search(l)
        if file_m is not None:
            current_filepath = l.split("b/")[-1]
            current_diff_line = None
        
        elif DIFF_START_EXP.search(l) is not None:
            current_diff_line = int(l.split("+")[-1].split(",")[0])
            metadata.append((current_filepath, current_diff_line))
            diffs.append([])
            diffs[-1].append(l)
        elif current_diff_line is not None:
            diffs[-1].append(l)

    print("# Sampled changes")
    print()
    #print(diffs)

    assert len(diffs) == len(metadata)
    current_file = None
    for m, lines in zip(metadata, diffs):
        filename, lineno = m

        if filename != current_file:
            print(f"## {filename}")
            print()
            current_file = filename

        link = f"https://github.com/{args.username}/{args.reponame}/tree/{args.branch}/{filename}#L{lineno}"
        print(f"Diff starting from line [{lineno}]({link})")
        print()
        print("```diff")
        for l in lines:
            print(l)

        print("```")
        print()
        print("- [ ] Correct")
        print("- [ ] Incorrect")
        print()

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--username", default="welfare-state-analytics")
    parser.add_argument("--reponame", default="riksdagen-corpus")
    parser.add_argument("--branch", default="dev")
    args = parser.parse_args()
    main(args)