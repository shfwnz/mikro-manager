import paramiko

# Server details
hostname = '192.168.126.129'
port = 22  # Default SSH port
username = 'admin'
password = '12345'  # Consider using key-based authentication for security

# Command to execute
command = 'ip address print'

try:
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    # Automatically add host keys from the server if not already known
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the server
    ssh_client.connect(hostname, port, username, password)

    # Execute a command
    stdin, stdout, stder = ssh_client.exec_command(command)
    
    # Read and print the command output
    print("Output:")
    for line in stdout:
        print(line.strip())
    
    # Read and print any error messages
    print("Errors:")
    for line in stder:
        print(line.strip())

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the SSH connection
    ssh_client.close()
