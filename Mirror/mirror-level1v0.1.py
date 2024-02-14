import os
import subprocess

def mirror_website(url: str, depth: int = 1, output_directory: str = "mirrored_site"):
    """
    Uses WinHTTrack to mirror the main pages of a website and one level down into each link on each page.

    Args:
    - url (str): The URL of the website to mirror.
    - depth (int): The depth of the mirroring process. Default is 1, which mirrors the main pages and one level down.
    - output_directory (str): The directory where the mirrored website will be saved. Default is 'mirrored_site'.

    Note: This function assumes WinHTTrack is installed and accessible from the command line.
    """
    # Ensure WinHTTrack is installed by checking its presence in the PATH
    try:
        subprocess.run(["httrack", "--version"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise RuntimeError("WinHTTrack is not installed or not found in PATH.")

    # Prepare WinHTTrack command
    command = [
        "httrack",
        url,  # The website to mirror
        f"-O {"C:/Users/Administrator/Documents/Mirrors"}",  # Output directory
        "--depth={2}".format(depth),  # Mirroring depth
        "--ext-depth={}".format(depth),  # External depth
        "-r2",  # Mirror one level down of external links
        "--mirror",  # Ensure it's a mirror operation
        "-N100",  # Naming convention for mirrored files
        "--robots=0",  # Ignore robots.txt rules
        "--timeout=60",  # Timeout after 60 seconds of inactivity
        "--retries=3",  # Retry 3 times on failure
        "--sockets=10",  # Use up to 10 sockets (parallel connections)
        "--connection-per-second=1",  # Limit to 1 connection per second to avoid server overload
        "--keep-alive",  # Use HTTP Keep-Alive
        "--no-catchurl",  # Do not catch URLs
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)",  # Use a common user-agent string
    ]

    # Execute the WinHTTrack command
    try:
        subprocess.run(" ".join(command), check=True, shell=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"WinHTTrack mirroring failed: {e}")

if __name__ == "__main__":
    WEBSITE_URL = "https://www.whitewashnews.com"
    mirror_website(WEBSITE_URL)
