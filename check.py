import os

path = "C:\Projects\langchain"

# Check if the file or directory exists
if os.path.exists(path):
    # Check permissions for the file or directory
    permissions = os.stat(path).st_mode

    # Check if the file or directory is readable
    is_readable = bool(permissions & 0o400)  # Read permission bit
    if is_readable:
        print("File or directory is readable")
    else:
        print("File or directory is not readable")

    # Check if the file or directory is writable
    is_writable = bool(permissions & 0o200)  # Write permission bit
    if is_writable:
        print("File or directory is writable")
    else:
        print("File or directory is not writable")

    # Check if the file or directory is executable
    is_executable = bool(permissions & 0o100)  # Execute permission bit
    if is_executable:
        print("File or directory is executable")
    else:
        print("File or directory is not executable")

else:
    print("File or directory does not exist")
