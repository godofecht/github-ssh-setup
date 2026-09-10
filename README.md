# github-ssh-setup

Generates a GitHub SSH key, copies it to the clipboard and opens the page where
it gets pasted. One command instead of the four steps in the documentation.

```bash
pip install .
github-ssh-setup
```

What it does, in order:

1. Checks whether a key already exists, and stops if one does.
2. Generates one against the email you give it.
3. Copies the public key to the clipboard. macOS uses `pbcopy`, Linux tries
   `xclip` then `xsel`, and anything else prints the key for you to copy.
4. Opens `github.com/settings/ssh/new` in your browser.

The private key never leaves the machine and is never printed.

If the clipboard step fails, the key is printed instead and the script says so
rather than opening a browser onto an empty paste.
