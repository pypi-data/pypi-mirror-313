# Leytonium
Tools for developing git-managed software

## Install
These are generic installation instructions.

### To use, permanently
The quickest way to get started is to install the current release from PyPI:
```
pip3 install --user Leytonium
```

### To use, temporarily
If you prefer to keep .local clean, install to a virtualenv:
```
python3 -m venv venvname
venvname/bin/pip install -U pip
venvname/bin/pip install Leytonium
. venvname/bin/activate
```

## Commands

### abandon
Discard all local changes, with confirmation step.

### agi
Search for identifier in project.

### agil
Edit project files containing identifier.

### autokb
Automatically switch to/from USB keyboard layout.

### autopull
Pull master and releases with automatic stash and switch.

### awslogs
Reconstruct logs from AWS CloudWatch.

### bashrc
To eval in your .bashrc file.

### br
Create given branch with completion and dashes, show menu for parent.

### brown
Satisfy PEP 8 with minimal impact.

### ci
Commit with the given args as message.

### co
Switch to the given branch, with completion.

### d
Show local changes.

### diffuse
Compare an arbitrary number of text files.
If you get this error on startup:
```
gi.repository.GLib.GError: gtk-icon-theme-error-quark: Icon 'document-new' not present in theme Adwaita (0)
```
Install the missing icons:
```
sudo apt-get install adwaita-icon-theme-full
```

### dp
Diff from public branch.

### drclean
Delete Docker assets.

### drop
Drop this branch.

### drst
Show Docker assets.

### dup
Apply the last slammed commit.

### dx
Diff from parent branch or from passed-in commit number.

### dxx
Short diff from parent branch or of passed-in commit number.

### eb
Rebase on the given branch with completion, or parent with confirmation.

### encrypt
Encrypt a secret using gpg for use in aridity config.

### examine
Open a shell in a throwaway container of the given image.

### extractaudio
Extract the audio from the given video files.

### fetchall
Fetch all remotes of projects in directory.

### fixemails
Replace author and committer emails of repo user in history.

### gag
Run ag on all build.gradle files.

### gimports
Stage all imports-only changes and show them.

### git-completion-path
Get path to git completion file, used by scripts.

### git-functions-path
Get path to git functions file, used by scripts.

### gpgedit
Edit gpg-encrypted file.

### gt
Stage all outgoing changes and show them.

### halp
You're looking at it!

### hgcommit
Commit hook to push to central clone of repo on local network.

### imgdiff
Use container-diff to compare Docker images.

### insertshlvl
Insert SHLVL indicator into given prompt.

### isotime
Filter UNIX timestamps to human-readable form.

### ks
Create a kitchen-sink branch.

### mdview
Render Markdown file in browser.

### multimerge
Merge master into all PRs and carrion.

### n
Switch to the next branch and run st.

### next
Go to next step in current git workflow.

### pb
Find parent branch.

### pd
Diff from public branch, the other way.

### prepare
Create a master-based branch from this non-master-based one.

### publish
Publish this branch, accepts push options.

### pullall
Pull all branches of projects in directory.

### pushall
Push (using hgcommit) all branches of projects in directory.

### rd
Run git add on conflicted path(s), with completion.

### rdx
Run git rm on conflicted path, with completion.

### readjust
Set system clock to correct time.

### reks
Rebase on a new kitchen-sink branch.

### ren
Rename current branch.

### resimp
Resolve conflicts in imports and adjacent-line conflicts.

### rol
Move given slammed commit (default top) to the bottom.

### rx
Restore given file to parent branch version.

### scrape85
Extract Adobe Ascii85-encoded images from given file.

### scrub
Remove all untracked items, including the git-ignored.

### setparent
Change declared parent of current branch.

### shove
Update a latest tag in ECR with the given image.

### show
Show a commit that was listed by st.

### showstash
Show stash as patch.

### slam
Reset branch to given commit number.

### spamtrash
Delete spam emails.

### splitpkgs
Show packages that exist in more than one module.

### squash
Semi-interactively squash a most-recent chunk of commits.

### st
Show list of branches and outgoing changes.

### stacks
Compare stack traces across build logs.

### stmulti
Short status of all shallow projects in directory.

### t
Show tree with hidden descendants but not their descendants.
Each hidden directory is annotated with a slash per direct child.
Useful for showing hidden items in a Git repository without also showing the whole `.git` tree.
By default all options are passed to the `tree` command, use `--` to pass (preceding) options to this command.
Use `-v` to show errors that are normally suppressed.

### taskding
Play a sound when a long-running child of shell terminates.

### tempvenv
Activate a writable venv from the pool with the given requires.

### touchb
Give the current branch its own identity.

### unpub
Unpublish this branch.

### unslam
Cherry-pick commits lost in a previous slam.

### upgrade
Upgrade the system and silence the nag.

### vcp
Copy a Docker volume.

### vpn
Start openvpn in background.

### vunzip
Extract a Docker volume.

### watchdesk
Different background for each desktop.
