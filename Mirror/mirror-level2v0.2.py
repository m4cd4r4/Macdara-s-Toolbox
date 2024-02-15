import os
import subprocess

def mirror_website(url: str, depth: int = 1, output_directory: str = "mirrored_site"):
    """
    Uses WinHTTrack to mirror the main pages of a website and one level down into each link on each page.

    Args:
    - url (str): The URL of the website to mirror.
    - depth (int): The depth of the mirroring process. Default is 1, which mirrors the main pages and one level down.
    - output_directory (str): The directory where the mirrored website will be saved. Default is 'mirrored_site'.

    """
    httrack_path = r"C:\Program Files\WinHTTrack\httrack.exe"  # Ensure this is the correct path to httrack.exe

    # Ensure the httrack executable exists
    if not os.path.exists(httrack_path):
        raise FileNotFoundError(f"httrack executable not found at specified path: {httrack_path}")

    # Prepare WinHTTrack command as a list
    command = [
        httrack_path,
        url,
        "-O", output_directory,
        "--depth={}".format(depth),
        "--ext-depth={}".format(depth),
        "-r2",
        "--mirror",
        "-N100",
        "--robots=0",
        "--timeout=60",
        "--retries=3",
        "--sockets=10",
        "--connection-per-second=1",
        "--keep-alive",
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "--display"  # Display URLs as they're mirrored
    ]

    # Execute the WinHTTrack command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"WinHTTrack mirroring failed: {e}")

if __name__ == "__main__":
    WEBSITE_URL = "https://www.whitewashnews.com"
    mirror_website(WEBSITE_URL)
