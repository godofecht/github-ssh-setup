# github-ssh-setup

Sets up GitHub SSH keys so you never enter a password again.

## What this is

SSH (Secure Shell) is a way for your computer to prove who it is to another computer. It uses a key pair: two linked files. The private key stays on your computer. The public key goes to GitHub. Once GitHub has your public key, `git push` and `git pull` work without a password.

This is a small Python command, `github-ssh-setup`. It generates a GitHub SSH key, copies it to the clipboard and opens the page where it gets pasted. One command replaces the four steps in GitHub's documentation.

## What you can learn from it

Computer Science:

- Public-key cryptography in practice: a private key you keep and a public key you share.
- Calling other programs from Python with `subprocess` (here `ssh-keygen` and the clipboard tools).
- Writing code that behaves differently on macOS, Windows and Linux with `platform.system()`.
- Packaging a Python script as a command you can type, through an entry point in `setup.py`.

## Run it

### On your own computer

**You will need:**

- [Python](https://www.python.org/downloads/) 3.
- [Git](https://git-scm.com/downloads), to download the code.
- `ssh-keygen`. It comes with macOS, with most Linux systems, and with Windows 10 and later.
- On Linux, `xclip` or `xsel` for the clipboard step.
- A GitHub account.

Tested on macOS with Python 3.12.

1. Download the code:

   ```sh
   git clone https://github.com/godofecht/github-ssh-setup.git
   cd github-ssh-setup
   ```

2. Make a virtual environment (a private folder of Python packages for this project) and turn it on:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the command together with `setuptools`, which the script imports when it starts. New virtual environments no longer include it:

   ```sh
   pip install setuptools .
   ```

4. If you have never used SSH on this computer, make the folder the key will live in. The script stops with an error if it is missing:

   ```sh
   mkdir -p ~/.ssh
   ```

5. Run it:

   ```sh
   github-ssh-setup
   ```

   If you have no key yet, it asks `Enter your GitHub email:`. Type the email on your GitHub account and press Enter. You should then see:

   ```text
   SSH key generated successfully.
   SSH key copied to clipboard.
   Opened GitHub SSH key settings page. Paste your key there.
   ```

6. In the browser, on the SSH and GPG keys page, choose **New SSH key**, paste into the **Key** box and save.

7. Check that GitHub accepts the key:

   ```sh
   ssh -T git@github.com
   ```

   GitHub replies with a greeting that includes your username.

If you already have a key, the script does not ask for your email. It copies your existing public key and opens the page.

## How it works

The script looks for `~/.ssh/id_ed25519.pub` or `~/.ssh/id_rsa.pub`. If neither exists, it asks for your email and runs `ssh-keygen` to make an Ed25519 key (a modern, short and fast kind of key). Then it reads the public key and pipes it into the clipboard tool for your system. If that works, it opens GitHub's key settings page in your browser.

| File | What is in it |
|---|---|
| `github_ssh_setup.py` | The whole program: `ssh_key_exists`, `generate_ssh_key`, `copy_to_clipboard`, `open_github_settings` and `main`. |
| `setup.py` | Package name, version 0.1, and the entry point that turns `github-ssh-setup` into a command. |
| `pyproject.toml` | Tells `pip` to build the package with setuptools. |
| `build/lib/github_ssh_setup.py` | A leftover build copy of the script. It is not used. |

## Ideas to try

1. Make the `~/.ssh` folder for the user. In `generate_ssh_key` in `github_ssh_setup.py`, call `os.makedirs` with `exist_ok=True` before running `ssh-keygen`.
2. Remove `from setuptools import setup` from the top of `github_ssh_setup.py`. Nothing uses it. Then step 3 of Run it only needs `pip install .`.
3. On Linux, when neither `xclip` nor `xsel` works, print the key so the user can copy it by hand. Look at `copy_to_clipboard`.
4. Open `https://github.com/settings/ssh/new` instead, which goes straight to the paste box. Change `open_github_settings`.
5. Ask whether to protect the key with a passphrase. At the moment `generate_ssh_key` passes `-N ""`, which means no passphrase.
6. Run `ssh -T git@github.com` at the end of `main` and report whether it worked.

## Technical details

What `main` does, in order:

1. Checks whether `~/.ssh/id_rsa.pub` or `~/.ssh/id_ed25519.pub` exists. If one does, it skips to step 3.
2. Generates `~/.ssh/id_ed25519` with `ssh-keygen -t ed25519 -C <email> -f ~/.ssh/id_ed25519 -N ""`.
3. Copies the public key to the clipboard. macOS uses `pbcopy`, Windows uses `clip`, Linux tries `xclip` then `xsel`. Any other system prints the key for you to copy.
4. If the copy worked, opens `https://github.com/settings/keys` in your browser. If it failed, prints `Manually copy your SSH key and add it to GitHub.` and opens nothing.

The private key never leaves the machine and is never printed. The key is made without a passphrase, so anyone who can read the file can use it.

## Project status

Version 0.1. The flow was run on macOS in a test home folder with the clipboard and browser calls replaced, and it generated the key and reached the last step. Known problems:

- The script imports `setuptools` without needing it, and does not list it as a dependency. In a fresh Python 3.12 virtual environment, `github-ssh-setup` stops with `ModuleNotFoundError: No module named 'setuptools'`. Step 3 works around this.
- If `~/.ssh` does not exist, `ssh-keygen` fails and the script stops with a `CalledProcessError`. Step 4 works around this.
- On Linux, a failed clipboard copy does not print the key.

## Licence

You can use, copy and change this code for any purpose, as long as you keep the copyright notice. See [LICENSE](LICENSE) (MIT).

## Credits

Written by Abhishek Shivakumar. Uses OpenSSH's `ssh-keygen`.
