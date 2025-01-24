# csrf-payload-generator
CSRF Payload Generator A powerful and flexible Cross-Site Request Forgery (CSRF) Payload Generator designed for security enthusiasts and penetration testers. This tool automates the generation of CSRF attack payloads based on HTTP requests.

Features
* Supports Multiple Payload Methods:
    - iframe: Generates a hidden iframe to execute CSRF requests.
    - fetch: Uses the Fetch API to execute CSRF requests programmatically.
    - onerror: Leverages the onerror event of an empty image tag for CSRF execution.
    - form: Auto-submitting HTML forms for CSRF attacks.

* HTML Output:
    - Generates an easy-to-use HTML file containing all the CSRF payloads for testing.

* How It Works
    - Input: Supply a raw HTTP request 
    - Process: The tool parses the HTTP request, extracts relevant data, and generates payloads.
    - Output: Produces an HTML file containing the generated payloads for execution.

* Usage
    1- Clone the repository:
  
---
  ```
git clone https://github.com/Abutalib-Zarban/csrf-payload-generator.git

```
