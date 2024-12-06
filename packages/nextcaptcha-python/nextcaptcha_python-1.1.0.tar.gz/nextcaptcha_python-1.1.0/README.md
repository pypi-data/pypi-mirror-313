# NextCaptcha Python SDK
NextCaptcha is a powerful captcha solving service that supports various types of captchas including reCAPTCHA v2,
reCAPTCHA v2 Enterprise, reCAPTCHA v3, reCAPTCHA Mobile, hCaptcha, and FunCaptcha. With NextCaptcha, you can easily
solve a variety of captcha challenges in your automation scripts and programs.

This SDK provides a simple and easy-to-use Python interface for interacting with the NextCaptcha API. It supports all
available captcha types and offers intuitive methods for solving different types of captchas.

## Installation

You can install the NextCaptcha Python SDK using pip:

```shell
pip install nextcaptcha-python
```

## Usage

To start using the NextCaptcha Python SDK, you first need to obtain your API key (clientKey) from the 
[NextCaptcha](https://dashboard.nextcaptcha.com) Dashboard. Then, you can create a NextCaptchaAPI instance:

```python
from nextcaptcha import NextCaptchaAPI

api = NextCaptchaAPI(client_key="YOUR_CLIENT_KEY")
```

Now, you can use the api object to solve various types of captchas.
To solve reCAPTCHA v2 challenges, use the recaptchav2 method:

```python
result = api.recaptchav2(website_url="https://example.com", website_key="SITE_KEY")
```

Solving reCAPTCHA v2 Enterprise
To solve reCAPTCHA v2 Enterprise challenges, use the recaptchav2enterprise method:

```python
result = api.recaptchav2enterprise(website_url="https://example.com", website_key="SITE_KEY")
```

Solving reCAPTCHA v3
To solve reCAPTCHA v3 challenges, use the recaptchav3 method:

```python
result = api.recaptchav3(website_url="https://example.com", website_key="SITE_KEY")
```

Solving reCAPTCHA Mobile
To solve reCAPTCHA Mobile challenges, use the recaptcha_mobile method:

```python
result = api.recaptcha_mobile(app_key="APP_KEY")
```

Solving hCaptcha
To solve hCaptcha challenges, use the hcaptcha method:

```python
result = api.hcaptcha(website_url="https://example.com", website_key="SITE_KEY")
```

Solving hCaptcha Enterprise
To solve hCaptcha Enterprise challenges, use the hcaptcha_enterprise method:

```python
result = api.hcaptcha_enterprise(website_url="https://example.com", website_key="SITE_KEY")
```


Checking Account Balance
To check your NextCaptcha account balance, use the get_balance method:

```python
balance = api.get_balance()
print(f"Account balance: {balance}")
```

Here is a complete example of using the NextCaptcha Python SDK to solve a reCAPTCHA v2 challenge:

```python
from nextcaptcha import NextCaptchaAPI

CLIENT_KEY = "YOUR_CLIENT_KEY"
WEBSITE_URL = "https://example.com"
WEBSITE_KEY = "SITE_KEY"

api = NextCaptchaAPI(client_key=CLIENT_KEY)
result = api.recaptchav2(website_url=WEBSITE_URL, website_key=WEBSITE_KEY)

if result["status"] == "ready":
    print(f"reCAPTCHA solved: {result['solution']}")
else:
    print(f"Failed to solve reCAPTCHA: {result['error']}")
```

## Error Handling

If an error occurs while solving a captcha, the SDK will return a dictionary containing the error information. You can
check the status field to determine if the request was successful. If the status is "ready", the captcha has been
successfully solved and the solution will be provided in the solution field. If the status is "failed", the error field
will contain a description of the error.

## Contributing

If you find any bugs or have suggestions for improvement, please feel free to submit an issue or send a pull request. We
welcome all contributions!

## License

This project is licensed under the MIT License. For more information, please see the LICENSE file.


