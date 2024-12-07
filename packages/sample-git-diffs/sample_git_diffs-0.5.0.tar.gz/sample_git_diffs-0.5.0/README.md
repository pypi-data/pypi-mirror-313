# sample-git-diffs

```
Sample git diffs uniformly wrt. number of changes per file. The output is formatted as a .diff file.

optional arguments:
  -h, --help            show this help message and exit
  --n N                 Total number of diffs to be sampled
  --diffstat DIFFSTAT   Custom git diff command for the sampling probabilities
  --diffcommand DIFFCOMMAND
                        Custom git diff command for the actual diff
```

For example, if you want to draw a sample of 25 diffs from the folder data/, you run

```
sample-git-diffs --diffstat "git diff --stat data/" --n 25
```

To save this to changes.diff, you run

```
sample-git-diffs --diffstat "git diff --stat data/" --n 25 > changes.diff
```

## diff2markdown

There's also a script that converts the generated .diff / .patch files into markdown.

```
usage: diff2markdown [-h] --path PATH [--username USERNAME] [--reponame REPONAME] [--branch BRANCH]

optional arguments:
  -h, --help           show this help message and exit
  --path PATH
  --username USERNAME
  --reponame REPONAME
  --branch BRANCH
```

For example, if you want to convert the changes.diff file into markdown, assuming that the repo is called 'sample-git-diffs', you're on branch 'main' and the github username is 'testuser', you run

```
diff2markdown --path changes.diff --username testuser --reponame sample-git-diffs --branch main
```
