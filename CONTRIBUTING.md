# Guidelines for Contributing to This Repo
## SETTING UP LOCAL ENVIRONMENT
Follow these guidelines to set up your local development environment. If you have already set it up, move on to [Contributing to the project](https://github.com/FAUSWE-GROUP11/Rokku/blob/master/CONTRIBUTING.md#contributing-to-the-project).

### 1. Fork this repo into your own GitHub account
Click the "Fork" button on the upper-right hand corner.

### 2. Clone your fork and add upstream
Your git should have two remotes: origin (pointing to your fork) and upstream (pointing to the master you have forked from). Always pull from upstream to sync your local repo and push to your origin.

```
# Make sure you're in desired directory for your local repository
git clone <url of your fork>
cd Rokku
git remote add upstream https://github.com/FAUSWE-GROUP11/Rokku.git
```

### 3. Create a virtual environment
Virtual environment is crucial for any Python projects to manage dependencies. We recommend the built-in `venv` command to create virtual environment (see [doc](https://docs.python.org/3/tutorial/venv.html)). You can, of course, use `virtualenv` (see [guides](https://python-guide-kr.readthedocs.io/ko/latest/dev/virtualenvs.html)) for the same purpose. We do not recommend using `pipenv` as it might create hassel unjustified for this project.

The following command creates a virtual environment inside a directory called `venv` inside the main project folder.

Note: These commands also assume you have adjusted your file path to include python.exe and python scripts.

```
# inside Rokku directory
python3 -m venv venv/
```
```
# if you're on Windows
python -m venv c:venv\
```

### 4. Activate virtual environment and install dependencies
```
# inside Rokku directory
source venv/bin/activate
pip3 install -r requirements.txt
```
The first command activate the virtual environment, so that all your python dependencies come from within the virtual environment (i.e. within the `venv` directory), instead of your system python site-packages folder.

The second command installs the dependencies required (listed in `requirements.txt`) by the project.

Note: If you're on Windows replace `bin` with `Scripts`.

### 5. Install pre-commit git hook
The `pre-commit` CLI tool is downloaded already as part of the dependencies for this project. We use `pre-commit` to check for PEP8 violation (via [`flake8`](http://flake8.pycqa.org/en/latest/index.html)) and automatically format python code (via ['black'](https://github.com/psf/black)) to comply with PEP8, before allowing `git commit` to take effect. Run the following command to install `pre-commit` git hook.

`pre-commit install`

## CONTRIBUTING TO PROJECT
Proceed only if you have already set up local development environment.

### 1. Sync your fork with upstream master branch
`git pull upstream master`

### 2. Check out a new branch to work on
`git checkout -b fanchen/fix_bug`

### 3. Make changes

### 4. Commit to your branch
Due to the existence of `pre-commit` git hook, your python code will be subject to testing from `flake8` checker and `black` formatter. If either of these two checks fail, your commit will not be fulfilled. You must fix your code's formatting according to the error message shown on the console. Note that, if `flake8` is triggered before `black`, some of the formatting issue reported from `flake8` could be already fixed by `black`, despite both checks show failure. We recommend that you run `git commit` multiple times until `black` passes, and then fix any remaining issues (i.e. issues unfixable by `black`). Once all issues are fixed, your commit will come through.

If you add new dependencies to the project (i.e. you have run `pip3 install <package_name>`), you must update `requirements.txt`. To update, run the following command:

```
pip3 freeze > requirements.txt
git commit -am "Update requirements"
```

### 5. Push commit to your remote branch
Since you have been working on branch "fanchen/fix_bug", you have to push your changes to the same branch of your fork on GitHub. Note: always push to origin (your folk); never push to upstream.

Example:

`git push origin fanchen/fix_bug`

### 6. Create new pull request (PR)
From your fork or upstream, open a new PR to merge your new branch to upstream/master. Wait for one of the codeowners (go to CODEOWNER file to see who are codeowners of this project) to approve of your PR. Upon approval, your contribution can be merged to upstream/master.

### 7. Delete your branch and sync with upstream
After your PR is merged to upstream/master, delete your local branch and the branch on your fork. This is to make sure that all branches currently living on the remote repo are unmerged. Note that, before you can delete the branch, you have to go to your local master and sync with upstream first.

```
git checkout master
git pull upstream master
git push origin master
git branch -d fanchen/fix_bug
git push -d origin fanchen/fix_bug
```
