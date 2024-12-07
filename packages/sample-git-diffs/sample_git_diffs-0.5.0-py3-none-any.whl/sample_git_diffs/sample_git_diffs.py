"""
Sample git diffs uniformly wrt. number of changes per file.
The output is formatted as a .diff file.
"""
import pandas as pd
import subprocess
import re
import random
import warnings
from io import StringIO
import argparse
from pathlib import Path

DIFF_EXP = re.compile("@@[ 0-9\.,\-\+]{2,50}@@")

def sample_from_diff(s, n=1, filename=""):
    lines = s.split("\n")
    intro = []
    diffs = []
    for l in lines:
        # Check '@' first for performance reasons
        if "@" in l and DIFF_EXP.search(l) is not None:
            diffs.append(l)
        elif len(diffs) >= 1:
            diffs[-1] += f"\n{l}"
        else:
            intro.append(l)

    intro = "\n".join(intro)
    if n > len(diffs):
        warnings.warn(f"n ({n}) is larger than the number of diffs in the file ({len(diffs)}) {filename}", stacklevel=2)
        diff_sample = diffs
    else:
        diff_sample = random.sample(diffs, n)
    diff = "\n".join(diff_sample)
    return f"{intro}\n{diff}"

def sample_diffs(diffstat="git diff --stat", diffcommand="git diff", n=150):
    diffstat = diffstat.replace("--stat", "--stat=1000")
    call = list(diffstat.split())
    result = subprocess.run(call, capture_output=True)
    csv_data = result.stdout.decode("utf-8")
    df = pd.read_csv(StringIO(csv_data), delimiter="|", names=["filename", "changes"])
    df["changes"] = df["changes"].str.strip().str.split(" ").str[0]
    df = df[df["changes"].notnull()]
    df = df[~df["changes"].str.contains("Bin")]
    df["changes"] = df["changes"].astype(int)
    df["p"] = df["changes"] / df["changes"].sum()
    
    if len(df) == 0:
        warnings.warn(f"No diffs detected", stacklevel=2)
        return ""
    sample = df.sample(n, weights="p", replace=True)
    sample = sample.groupby(['filename'], as_index=False).size()

    output = []
    diffcommand_prime = list(filter(lambda fp: not Path(fp).exists(), diffcommand.split()))
    for _, row in sample.iterrows():
        filename, n_row = row["filename"], row["size"]
        call = diffcommand_prime + [filename.strip()]
        result = subprocess.run(call, capture_output=True)
        s = result.stdout.decode("utf-8")

        diff = sample_from_diff(s, n=n_row, filename=filename.strip())
        output.append(diff)
        
    return "\n".join(output)

def cli():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument("--n", type=int, default=150, help="Total number of diffs to be sampled")
    argparser.add_argument("--diffstat", type=str, default="git diff --stat",
        help="Custom git diff command for the sampling probabilities")
    argparser.add_argument("--diffcommand", type=str, default=None,
        help="Custom git diff command for the actual diff")
    args = argparser.parse_args()
    diffstat, diffcommand = args.diffstat, args.diffcommand
    n = args.n
    if diffcommand is None:
        diffcommand = diffstat.replace("--stat", "")

    output = sample_diffs(diffstat=diffstat, diffcommand=diffcommand, n=n)
    print(output)

    