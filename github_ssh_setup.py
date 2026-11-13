import os
import subprocess
import platform
import webbrowser


def ssh_key_exists():
    return os.path.exists(os.path.expanduser("~/.ssh/id_rsa.pub")) or os.path.exists(os.path.expanduser("~/.ssh/id_ed25519.pub"))


def generate_ssh_key(email):
    ssh_dir = os.path.expanduser("~/.ssh")
    # ssh-keygen cannot create this folder itself, and a new machine may not have it.
    os.makedirs(ssh_dir, mode=0o700, exist_ok=True)
    key_path = os.path.join(ssh_dir, "id_ed25519")
    subprocess.run(["ssh-keygen", "-t", "ed25519", "-C", email, "-f", key_path, "-N", ""], check=True)
    print("SSH key generated successfully.")


def copy_to_clipboard():
    ssh_key_path = os.path.expanduser("~/.ssh/id_ed25519.pub")
    if not os.path.exists(ssh_key_path):
        ssh_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
    
    if not os.path.exists(ssh_key_path):
        print("No SSH key found.")
        return False
    
    with open(ssh_key_path, "r") as key_file:
        ssh_key = key_file.read()
    
    system = platform.system()
    if system == "Darwin":
        subprocess.run("pbcopy", text=True, input=ssh_key)
    elif system == "Windows":
        subprocess.run("clip", text=True, input=ssh_key)
    elif system == "Linux":
        try:
            subprocess.run("xclip -selection clipboard", shell=True, text=True, input=ssh_key, check=True)
        except subprocess.CalledProcessError:
            try:
                subprocess.run("xsel --clipboard --input", shell=True, text=True, input=ssh_key, check=True)
            except subprocess.CalledProcessError:
                print("Clipboard copy failed. Install xclip or xsel, or manually copy the key.")
                return False
    else:
        print("Unsupported OS. Copy the key manually:")
        print(ssh_key)
        return False
    
    print("SSH key copied to clipboard.")
    return True


def open_github_settings():
    github_url = "https://github.com/settings/keys"
    webbrowser.open(github_url)
    print("Opened GitHub SSH key settings page. Paste your key there.")


def main():
    if not ssh_key_exists():
        email = input("Enter your GitHub email: ")
        generate_ssh_key(email)
    
    if copy_to_clipboard():
        open_github_settings()
    else:
        print("Manually copy your SSH key and add it to GitHub.")


if __name__ == "__main__":
    main()
