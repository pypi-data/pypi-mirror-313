"""
Wrapper for the curl command to request an API endpoint.
The Quizlet API requires TLS Fingerprinting to be bypassed, so this script uses curl to request the API by impersonating a browser.
"""

import subprocess


def curl_api(endpoint: str) -> str:
    """
    Requests and endpoint using curl (due to TLS Fingerprinting) and returns the response as a string.

    Args:
        endpoint (str): The endpoint of the API to request.

    Returns:
        str: The raw response from the API.
    """

    cmd = f"""curl "{endpoint}" \
    -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
    -H 'accept-language: en-US,en;q=0.9' \
    -H 'cache-control: max-age=0' \
    -H 'dnt: 1' \
    -H 'priority: u=0, i' \
    -H 'sec-ch-ua: "Chromium";v="131", "Not_A Brand";v="24"' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'sec-ch-ua-platform: "macOS"' \
    -H 'sec-fetch-dest: document' \
    -H 'sec-fetch-mode: navigate' \
    -H 'sec-fetch-site: none' \
    -H 'sec-fetch-user: ?1' \
    -H 'upgrade-insecure-requests: 1' \
    -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    """

    result = subprocess.run(cmd, shell=True, capture_output=True)

    raw = result.stdout.decode("utf-8")

    return raw
