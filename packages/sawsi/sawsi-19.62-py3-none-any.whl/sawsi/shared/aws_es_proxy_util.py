import os
import subprocess
import platform


def install_aws_es_proxy():
    """
    Detect the operating system and install aws-es-proxy along with its dependencies.
    This function will install Homebrew (if needed), Go, and aws-es-proxy based on the OS.
    It also sets up the required environment variables.
    """
    os_name = platform.system()

    if os_name == "Darwin":  # macOS
        install_brew()  # Install Homebrew if not installed
        install_go_mac()  # Install Go on macOS using Homebrew
        set_environment_variable_mac_linux()  # Set environment variables
        install_aws_es_proxy_command()  # Install aws-es-proxy
    elif os_name == "Linux":
        install_go_linux()  # Install Go on Linux
        set_environment_variable_mac_linux()  # Set environment variables
        install_aws_es_proxy_command()  # Install aws-es-proxy
    elif os_name == "Windows":
        install_go_windows()  # Install Go on Windows
        set_environment_variable_windows()  # Set environment variables
        install_aws_es_proxy_command_windows()  # Install aws-es-proxy on Windows
    else:
        print(f"Unsupported OS: {os_name}")
        return

    print("Installation of aws-es-proxy completed!")


def install_brew():
    """
    Check if Homebrew is installed on macOS. If not, install Homebrew.
    Homebrew is a package manager for macOS that makes it easy to install software.
    """
    try:
        subprocess.check_call(["brew", "--version"])
        print("Homebrew is already installed.")
    except subprocess.CalledProcessError:
        print("Homebrew not found. Installing Homebrew...")
        try:
            subprocess.check_call(
                ['/bin/bash', '-c',
                 '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"']
            )
            print("Homebrew installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Homebrew: {e}")


def install_go_mac():
    """
    Install Go programming language on macOS using Homebrew.
    Go is required to install aws-es-proxy.
    """
    try:
        subprocess.check_call(["brew", "install", "go"])
        print("Go installed successfully on macOS.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Go on macOS: {e}")


def install_go_linux():
    """
    Install Go programming language on Linux using apt package manager.
    Go is required to install aws-es-proxy.
    """
    try:
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "install", "-y", "golang-go"])
        print("Go installed successfully on Linux.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Go on Linux: {e}")


def install_go_windows():
    """
    Install Go programming language on Windows.
    This function downloads the Go installer and runs it.
    Go is required to install aws-es-proxy.
    """
    go_url = "https://golang.org/dl/go1.16.6.windows-amd64.msi"  # URL for the Go installer MSI file
    msi_path = "go-installer.msi"  # Local path to save the downloaded MSI file

    try:
        subprocess.check_call(["curl", "-o", msi_path, go_url])
        subprocess.check_call(["msiexec", "/i", msi_path, "/quiet", "/norestart"])
        print("Go installed successfully on Windows.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Go on Windows: {e}")
    finally:
        if os.path.exists(msi_path):
            os.remove(msi_path)  # Clean up the MSI installer file after installation


def set_environment_variable_mac_linux():
    """
    Set the environment variables for Go and aws-es-proxy on macOS and Linux.
    This function updates the PATH environment variable to include the Go bin directory.
    """
    go_path = os.path.expanduser("~/go/bin")

    shell_config_file = os.path.expanduser("~/.bashrc")  # Default shell config file for bash
    if 'zsh' in os.environ.get('SHELL', ''):
        shell_config_file = os.path.expanduser("~/.zshrc")  # zsh shell config file

    export_command = f'\nexport PATH=$PATH:{go_path}\n'

    try:
        with open(shell_config_file, 'a') as f:
            f.write(export_command)
        print(f"Environment variables set successfully on macOS/Linux. Added {go_path} to PATH.")
        print(f"Please run 'source {shell_config_file}' or open a new terminal session to apply the changes.")
    except Exception as e:
        print(f"Failed to set environment variables on macOS/Linux: {e}")


def set_environment_variable_windows():
    """
    Set the environment variables for Go and aws-es-proxy on Windows.
    This function updates the PATH environment variable to include the Go bin directory.
    """
    go_path = os.path.join(os.environ['USERPROFILE'], 'go', 'bin')

    try:
        subprocess.check_call(f'setx PATH "%PATH%;{go_path}"', shell=True)
        print(f"Environment variables set successfully on Windows. Added {go_path} to PATH.")
        print("Please restart your command prompt or open a new one to apply the changes.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set environment variables on Windows: {e}")


def install_aws_es_proxy_command():
    """
    Install aws-es-proxy using Go's package management.
    This command works for both macOS and Linux.
    """
    try:
        subprocess.check_call(["go", "install", "github.com/abutaha/aws-es-proxy@latest"])
        print("aws-es-proxy installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install aws-es-proxy: {e}")


def install_aws_es_proxy_command_windows():
    """
    Install aws-es-proxy on Windows using Go's package management.
    """
    try:
        subprocess.check_call(["go", "install", "github.com/abutaha/aws-es-proxy@latest"], shell=True)
        print("aws-es-proxy installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install aws-es-proxy: {e}")


if __name__ == "__main__":
    install_aws_es_proxy()
