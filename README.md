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

3. Install the command:

   ```sh
   pip install .
   ```

4. Run it:

   ```sh
   github-ssh-setup
   ```

   If you have no key yet, it asks `Enter your GitHub email:`. Type the email on your GitHub account and press Enter. You should then see:

   ```text
   SSH key generated successfully.
   SSH key copied to clipboard.
   Opened GitHub SSH key settings page. Paste your key there.
   ```

5. In the browser, on the SSH and GPG keys page, choose **New SSH key**, paste into the **Key** box and save.

6. Check that GitHub accepts the key:

   ```sh
   ssh -T git@github.com
   ```

   GitHub replies with a greeting that includes your username.

If you already have a key, the script does not ask for your email. It copies your existing public key and opens the page.

## How it works

The script looks for `~/.ssh/id_ed25519.pub` or `~/.ssh/id_rsa.pub`. If neither exists, it asks for your email, makes the `~/.ssh` folder if it is missing, and runs `ssh-keygen` to make an Ed25519 key (a modern, short and fast kind of key). Then it reads the public key and pipes it into the clipboard tool for your system. If that works, it opens GitHub's key settings page in your browser.

| File | What is in it |
|---|---|
| `github_ssh_setup.py` | The whole program: `ssh_key_exists`, `generate_ssh_key`, `copy_to_clipboard`, `open_github_settings` and `main`. |
| `setup.py` | Package name, version 0.1, and the entry point that turns `github-ssh-setup` into a command. |
| `pyproject.toml` | Tells `pip` to build the package with setuptools. |

## Ideas to try

1. On Linux, when neither `xclip` nor `xsel` works, print the key so the user can copy it by hand. Look at `copy_to_clipboard`.
2. Open `https://github.com/settings/ssh/new` instead, which goes straight to the paste box. Change `open_github_settings`.
3. Ask whether to protect the key with a passphrase. At the moment `generate_ssh_key` passes `-N ""`, which means no passphrase.
4. Run `ssh -T git@github.com` at the end of `main` and report whether it worked.

## Technical details

What `main` does, in order:

1. Checks whether `~/.ssh/id_rsa.pub` or `~/.ssh/id_ed25519.pub` exists. If one does, it skips to step 3.
2. Creates `~/.ssh` (mode 700) if it is missing, then generates `~/.ssh/id_ed25519` with `ssh-keygen -t ed25519 -C <email> -f ~/.ssh/id_ed25519 -N ""`.
3. Copies the public key to the clipboard. macOS uses `pbcopy`, Windows uses `clip`, Linux tries `xclip` then `xsel`. Any other system prints the key for you to copy.
4. If the copy worked, opens `https://github.com/settings/keys` in your browser. If it failed, prints `Manually copy your SSH key and add it to GitHub.` and opens nothing.

The private key never leaves the machine and is never printed. The key is made without a passphrase, so anyone who can read the file can use it.

## Project status

Version 0.1. The flow was run on macOS with Python 3.12, in a fresh virtual environment and an empty test home folder with no `~/.ssh`, with the clipboard and browser calls replaced. It made the folder, generated the key, copied it and opened the settings page. A second run skipped straight to copying.

Known problem: on Linux, a failed clipboard copy does not print the key.

## Licence

You can use, copy and change this code for any purpose, as long as you keep the copyright notice. See [LICENSE](LICENSE) (MIT).

## Credits

Written by Abhishek Shivakumar. Uses OpenSSH's `ssh-keygen`.
