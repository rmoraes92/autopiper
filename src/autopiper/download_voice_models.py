import requests


def download_file(url, filename):
    """Downloads a file from a given URL and saves it to the specified filename."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Successfully downloaded file from {url} to {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    download_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ar/ar_JO/kareem/low/ar_JO-kareem-low.onnx?download=true"
    output_filename = "ar_JO-kareem-low.onnx"

    download_file(download_url, output_filename)
