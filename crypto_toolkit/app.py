from flask import Flask, render_template_string, request
from ciphers import (
    CaesarCipher,
    MonoalphabeticCipher,
    PlayfairCipher,
    HillCipher,
    VigenereCipher,
    OneTimePad,
    RailFenceCipher,
    ColumnarCipher,
)
from utils.validators import (
    validate_integer,
    validate_rails,
    validate_alpha_key,
    validate_mono_key,
    validate_hill_matrix_string,
)

app = Flask(__name__)

CIPHERS = {
    "Caesar": CaesarCipher(),
    "Monoalphabetic": MonoalphabeticCipher(),
    "Playfair": PlayfairCipher(),
    "Hill": HillCipher(),
    "Vigenere": VigenereCipher(),
    "One-Time Pad": OneTimePad(),
    "Rail Fence": RailFenceCipher(),
    "Columnar": ColumnarCipher(),
}

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Crypto Toolkit</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#0b1020;color:#eef2ff;
font:16px Arial,sans-serif;padding:25px}
main{max-width:850px;margin:35px auto}
h1{font-size:42px;margin-bottom:8px;color:#c4b5fd}
p{color:#b9c4dc;line-height:1.6}
.card{background:#151e32;border:1px solid #35425d;
padding:24px;border-radius:16px}
label{display:block;margin:15px 0 8px;font-weight:bold}
input,select,textarea{width:100%;padding:12px;
border:1px solid #455571;border-radius:8px;
background:#0b1223;color:white;font-size:16px}
textarea{min-height:150px;resize:vertical}
button{margin-top:18px;padding:12px 22px;border:0;
border-radius:8px;background:#8b5cf6;color:white;
font-size:16px;font-weight:bold;cursor:pointer}
.result{margin-top:22px;padding:16px;
background:#10192a;border-radius:10px;overflow-wrap:anywhere}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}
.error{color:#fca5a5}
small{color:#a9b6d0}
</style>
</head>
<body>
<main>
<h1>Crypto Toolkit</h1>
<p>Encrypt and decrypt messages using eight classical
cryptography algorithms.</p>
<section class="card">
<form method="POST">
<label for="cipher">Choose Cipher</label>
<select name="cipher" id="cipher">
{% for c in ciphers %}
<option value="{{c}}" {% if c == selected %}selected{% endif %}>
{{c}}</option>
{% endfor %}
</select>

<label for="operation">Operation</label>
<select name="operation" id="operation">
<option value="encrypt" {% if operation == 'encrypt' %}selected{% endif %}>Encrypt</option>
<option value="decrypt" {% if operation == 'decrypt' %}selected{% endif %}>Decrypt</option>
</select>

<label for="key">Key</label>
<input name="key" id="key" value="{{key}}"
placeholder="Enter the cipher key">
<small>Caesar/Rail Fence: number. Hill: matrix key.
Other ciphers: use the appropriate key.</small>

<label for="message">Message</label>
<textarea name="message" id="message" required
placeholder="Enter your message">{{message}}</textarea>

<button type="submit">Process Message</button>
</form>

{% if result is not none %}
<div class="result">
<h3>{% if error %}Error{% else %}Result{% endif %}</h3>
<pre class="{% if error %}error{% endif %}">{{result}}</pre>
</div>
{% endif %}
</section>
<p><small>Educational use only. Classical ciphers are not
suitable for securing sensitive real-world information.</small></p>
</main>
</body>
</html>
"""


def process_message(cipher_name, operation, message, raw_key):
    if not message:
        raise ValueError("Enter a message first.")

    cipher = CIPHERS[cipher_name]
    key_text = raw_key.strip()
    generated_key_message = ""

    if cipher_name == "Caesar":
        key = validate_integer(key_text, "Caesar key")

    elif cipher_name == "Rail Fence":
        key = validate_rails(key_text)

    elif cipher_name == "Hill":
        key = validate_hill_matrix_string(key_text)

    elif cipher_name == "Monoalphabetic":
        if not key_text and operation == "encrypt":
            key = cipher.generate_key()
            generated_key_message = f"Generated key: {key}\\n\\n"
        elif not key_text:
            raise ValueError("Enter the key used for encryption.")
        else:
            key = validate_mono_key(key_text)

    elif cipher_name == "One-Time Pad":
        if not key_text:
            if operation == "decrypt":
                raise ValueError("Enter the original OTP key.")
            key = cipher.generate_key(message)
            generated_key_message = (
                f"Generated key (save this): {key}\\n\\n"
            )
        else:
            key = key_text.upper()

    elif cipher_name in ("Vigenere", "Columnar"):
        key = validate_alpha_key(key_text, f"{cipher_name} key")

    elif cipher_name == "Playfair":
        if not key_text:
            raise ValueError("Enter a Playfair keyword.")
        key = key_text

    else:
        key = key_text

    method = cipher.encrypt if operation == "encrypt" else cipher.decrypt
    return generated_key_message + str(method(message, key))


@app.route("/", methods=["GET", "POST"])
def home():
    selected = request.form.get("cipher", "Caesar")
    operation = request.form.get("operation", "encrypt")
    message = request.form.get("message", "")
    key = request.form.get("key", "")
    result = None
    error = False

    if request.method == "POST":
        try:
            if selected not in CIPHERS:
                raise ValueError("Select a valid cipher.")
            if operation not in ("encrypt", "decrypt"):
                raise ValueError("Select a valid operation.")
            result = process_message(selected, operation, message, key)
        except Exception as exc:
            result = str(exc) or "Unable to process this message."
            error = True

    return render_template_string(
        PAGE,
        ciphers=list(CIPHERS.keys()),
        selected=selected,
        operation=operation,
        message=message,
        key=key,
        result=result,
        error=error,
    )


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
```