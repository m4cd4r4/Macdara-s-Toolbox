# Website Mirroring Script with HTTrack

This Python script is designed to automate the process of mirroring websites using HTTrack, a free, open-source website copier that allows for offline browsing. The script enables users to specify the URL of the website they wish to mirror, the depth of the mirror (i.e., how many levels deep to follow links from the initial page), and the output directory where the mirrored website will be saved.

## Features
- **Customizable Mirroring Depth**: Users can define how deep the script should go into the website's link structure. The default depth is 1, which means it mirrors the main page and one level of linked pages.
- **Configurable Output Directory**: The location where the mirrored website is stored can be easily set, with a default directory named `mirrored_site`.
- **User-Agent Customization**: The script includes a user-agent string to mimic a real browser, reducing the chance of being blocked by the website's server.
- **Robust Error Handling**: Incorporates error checking to ensure the mirroring process completes successfully or provides a meaningful error message if it fails.

## Usage

### Installation Requirement
Ensure HTTrack is installed on your system and accessible from the specified path in the script (`C:\Program Files\WinHTTrack\httrack.exe`). Modify the path as necessary to match your installation.

### Script Configuration
Before running the script, set the `WEBSITE_URL` variable to the URL of the website you wish to mirror. Optionally, adjust the `depth` and `output_directory` parameters in the `mirror_website` function call to suit your needs.

### Execution
Run the script in a Python environment. It requires Python 3.x.

## Important Notes

- **Windows Only**: The script is designed for Windows environments, given the path to HTTrack. For other operating systems, adjust the `httrack_path` accordingly.
- **Legal and Ethical Considerations**: Always ensure you have permission to mirror a website and are compliant with the website's `robots.txt` file and terms of service.

## Error Handling

If the mirroring process fails, the script will catch a `subprocess.CalledProcessError` and raise a `RuntimeError` with details about the failure. This feature aids in debugging and ensures users are aware of any issues encountered during execution.

