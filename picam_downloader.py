import os
import paramiko
import getpass

# Remote server details
remote_user = "icrucrob"
remote_host = "192.168.24.25"
remote_dir = "/home/username/picam/high_street/"

# Local download directory
local_dir = "./picam_downloads/"

# Log file to record downloaded files
log_file = "downloaded_files.log"

# Ensure the local directory exists
os.makedirs(local_dir, exist_ok=True)

# Function to check if a file exists in the local directory
def file_exists_locally(file):
    return os.path.exists(os.path.join(local_dir, file))

# Replace '~/.ssh/id_rsa' with the actual path to your private key file
private_key_path = os.path.expanduser("~/.ssh/id_rsa")

# Prompt the user for the passphrase
passphrase = getpass.getpass("Enter passphrase for the private key: ")

# Initialize SSH client
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()

try:
    ssh.connect(
        remote_host,
        username=remote_user,
        key_filename=private_key_path,
        passphrase=passphrase
    )

    # List remote files
    with ssh.open_sftp() as sftp:
        remote_files = sftp.listdir(remote_dir)

    # Process remote files
    for remote_file in remote_files:
        if remote_file.endswith(".jpg"):
            local_file = os.path.basename(remote_file)
            if not file_exists_locally(local_file):
                print("Downloading {}...".format(local_file))
                with ssh.open_sftp() as sftp:
                    sftp.get(os.path.join(remote_dir, remote_file), os.path.join(local_dir, local_file))
                with open(os.path.join(local_dir, log_file), "a") as log:
                    log.write(local_file + "\n")
            else:
                print("Skipping {} (already exists locally)".format(local_file))

finally:
    ssh.close()
