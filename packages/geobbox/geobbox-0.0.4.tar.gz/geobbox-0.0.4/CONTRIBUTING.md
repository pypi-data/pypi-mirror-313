# Contributing guidelines

## Contributing code

1. (optional) Set up a Python development environment
   (advice: use [venv](https://docs.python.org/3/library/venv.html),
   [virtualenv](https://virtualenv.pypa.io/), or [miniconda](https://docs.conda.io/en/latest/miniconda.html))
2. Clone the repository and install `geobbox`
   ```bash
   git clone https://github.com/gbelouze/geobbox.git
   cd geobbox
   pip install -e .
   ```
3. Start a new branch off the main branch: `git switch -c my-new-branch main`
4. Make your code changes
5. It's nice to have common formatting options. We use `ruff`. Use the nice `pre-commit` tool to adhere to the repository formatting guidelines.
```bash
   pip install pre-commit # install pre-commit
   pre-commit install   # install the hooks for the geobbox project
   # this will prevent you from committing unformatted code
   ```
   You can then optionally use the code checking tools by hand or run them all at once with
   ```bash
   pre-commit run --all-files
   ```
6. Commit, push, and open a pull request!
   ```bash
   git add file1 file2 file3  # add the modified files
   git commit -m "Short message to explain your changes"  # commit your changes
   git push -u origin my-new-branch  # change the branch name to the one you created in step 3.
   ```
   Use the link in the output, which should look something like `https://github.com/gbelouze/geobbox/compare/my-new-branch`, and create a *pull request*.
   Someone else will review your code and merge it to the repository !
