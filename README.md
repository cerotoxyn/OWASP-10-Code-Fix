# OWASP Vulnerability Review

This repository reviews ten vulnerable code samples written in **JavaScript, Python, and Java**. For each example, the security flaw is identified and explained, a secure version of the code is provided, and the fix is described in terms of how it improves security.

---

## Table of Contents

1. [Broken Access Control (JavaScript / Express)](#1-broken-access-control-javascript--express)
2. [Broken Access Control (Python / Flask)](#2-broken-access-control-python--flask)
3. [Cryptographic Failures (Java)](#3-cryptographic-failures-java)
4. [Cryptographic Failures (Python)](#4-cryptographic-failures-python)
5. [Injection - SQL Injection (Java)](#5-injection---sql-injection-java)
6. [Injection - NoSQL Injection (JavaScript / Node.js)](#6-injection---nosql-injection-javascript--nodejs)
7. [Insecure Design (Python / Flask)](#7-insecure-design-python--flask)
8. [Software and Data Integrity Failures (HTML / JavaScript)](#8-software-and-data-integrity-failures-html--javascript)
9. [Server-Side Request Forgery (Python)](#9-server-side-request-forgery-python)
10. [Identification and Authentication Failures (Java)](#10-identification-and-authentication-failures-java)

---

## 1. Broken Access Control (JavaScript / Express)

### Vulnerable Code:
```javascript
app.get('/profile/:userId', (req, res) => {
    User.findById(req.params.userId, (err, user) => {
        if (err) return res.status(500).send(err);
        res.json(user);
    });
});
```

Security Flaw
This route returns any user profile based only on the userId in the URL. There is no authorization check to verify that the requester is actually allowed to view that profile. An attacker could simply change the userId value and access another user's information. This is a classic Broken Access Control issue, often described as an Insecure Direct Object Reference (IDOR). The server is exposing sensitive data because it trusts user-controlled input without verifying permissions.

How the Fix Improves Security
The secure version checks whether the requester is authenticated and whether they are authorized to view the requested profile. Only the account owner or an administrator can access the data. This prevents attackers from changing the ID in the URL to retrieve other users' information.

## 2. Broken Access Control (Python/Flask)

### Vulnerable Code:
@app.route('/account/<user_id>')
def get_account(user_id):
    user = db.query(User).filter_by(id=user_id).first()
    return jsonify(user.to_dict())

Security Flaw
This Flask route has the same problem as the first example. It uses the user_id from the URL to fetch and return account data, but it never checks whether the current user should be allowed to access that account.
An attacker could guess different account IDs and retrieve sensitive information belonging to other users. This is another example of Broken Access Control and IDOR-style behavior.

How the Fix Improves Security
The route now verifies that the requester is logged in and authorized to access the account. Only the owner of the account or an admin can retrieve the data. This prevents unauthorized users from reading other accounts just by changing the URL parameter.

## 3. Cryptographic Failures (Java)

### Vulnerable Code:
public String hashPassword(String password) throws NoSuchAlgorithmException {
    MessageDigest md = MessageDigest.getInstance("MD5");
    md.update(password.getBytes());
    byte[] digest = md.digest();
    return DatatypeConverter.printHexBinary(digest);
}

Security Flaw
This code uses MD5 to hash passwords. MD5 is an outdated and insecure hashing algorithm for password storage because it is extremely fast and easy for attackers to crack using modern hardware.
Passwords should never be stored with weak or fast general-purpose hash functions. Instead, they should be stored using algorithms specifically designed for password hashing.

How the Fix Improves Security
The secure version replaces MD5 with bcrypt, which is designed specifically for password storage. Bcrypt is intentionally slow and uses a work factor, which makes brute-force attacks much harder. This greatly improves password security if the database is compromised.

## 4. Crytopgraphic Failures (Python)

### Vulnerable Code:
import hashlib

def hash_password(password):
    return hashlib.sha1(password.encode()).hexdigest()

Security Flaw
This code uses SHA-1 for password hashing. SHA-1 is not appropriate for storing passwords because it is a fast general-purpose hash function and is vulnerable to cracking attacks.
Just like MD5, SHA-1 should not be used for password storage. Passwords require stronger algorithms designed to slow attackers down.

How the Fix Improves Security
The secure version uses Argon2, a modern password hashing algorithm recommended for password storage. Argon2 is built to resist brute-force attacks by using memory and processing time, making password cracking much more difficult than with SHA-1.

## 5. Injection - SQL Injection (Java)

### Vulnerable Code:
String username = request.getParameter("username");
String query = "SELECT * FROM users WHERE username = '" + username + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);

Security Flaw
This code directly inserts user input into a SQL query. That allows an attacker to supply malicious input that changes the meaning of the query. For example, they could bypass authentication, read unauthorized data, or manipulate the database.
This is a classic SQL Injection vulnerability because the application mixes untrusted data with SQL commands.

How the Fix Improves Security
The secure version uses a PreparedStatement, which separates SQL code from user input. The input is treated only as data, not as executable SQL. This prevents attackers from injecting SQL commands through the username parameter.

## 6. Injection - NoSQL Injection (JavaScript / Node.js)

### Vulnerable Code:
app.get('/user', (req, res) => {
    // Directly trusting query parameters can lead to NoSQL injection
    db.collection('users').findOne({ username: req.query.username }, (err, user) => {
        if (err) throw err;
        res.json(user);
    });
});

Security Flaw
This code directly trusts a query parameter and uses it in a database query. In some cases, attackers can supply specially crafted values or operators that manipulate how the NoSQL query behaves.
This is a NoSQL Injection issue because untrusted input is being passed into the query logic without strong validation.

How the Fix Improves Security
The secure version validates that the input is a normal username string and matches an expected pattern before it is used in the query. This reduces the risk of attackers injecting query operators or malformed input into the database call.

## 7. Insecure Design (Python/Flask)

### Vulnerable Code:
@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form['email']
    new_password = request.form['new_password']
    user = User.query.filter_by(email=email).first()
    user.password = new_password
    db.session.commit()
    return 'Password reset'

Security Flaw
This password reset flow is insecure by design. Anyone who knows a user's email address can submit a new password and reset that user's account. There is no verification step, no reset token, no expiration, and no proof that the requester actually owns the account.
This is an Insecure Design issue because the overall process was designed without proper security controls.

How the Fix Improves Security
The secure version redesigns the password reset process to require a secure reset token. The token is random, time-limited, and must be verified before the password can be changed. The new password is also stored as a hash instead of plain text. This prevents attackers from resetting passwords just by knowing an email address.
    
## 8. Software and Data Integrity Failures (HTML/JavaScript)

### Vulnerable Code:
<script src="https://cdn.example.com/lib.js"></script>

Security Flaw
This code loads a JavaScript file from a third-party CDN without verifying its integrity. If that external file is modified or the CDN is compromised, malicious code could run in the user's browser.
This is a Software and Data Integrity Failures issue because the application is trusting external code without integrity checks.

How the Fix Improves Security
The secure version adds Subresource Integrity (SRI). The browser checks the script's cryptographic hash before executing it. If the file has been changed, it will not run. This helps protect against tampered or compromised third-party scripts.

## 9. Server-Side Request Forgery (Python)

### Vulnerable Code:
url = input("Enter URL: ")
response = requests.get(url)
print(response.text)

Security Flaw
This code accepts any URL from the user and makes a server-side request to it. That means an attacker could make the server access internal systems, cloud metadata services, or private network resources that should not be reachable from the outside.
This is a Server-Side Request Forgery (SSRF) vulnerability because the server is being tricked into making requests on the attacker's behalf.

How the Fix Improves Security
The secure version validates the URL before making the request. It only allows approved hosts, requires HTTPS, blocks private and local IP addresses, and disables redirects. These controls reduce the risk that attackers can use the server to access internal or restricted resources.

## 10. Identification and Authentication Failures (Java)

### Vulnerable Code:
if (inputPassword.equals(user.getPassword())) { 
    // Login success
}

Security Flaw
This code compares the entered password directly with the stored password. That strongly suggests the password is being stored in plaintext or another unsafe reversible form. Storing passwords this way is dangerous because anyone who gains access to the database could read all user passwords immediately.
This is an Identification and Authentication Failures issue because the authentication system is not securely handling passwords.

How the Fix Improves Security
The secure version verifies the entered password against a bcrypt hash instead of comparing plaintext values. This means the real password is never stored directly. If the database is leaked, attackers still have to crack strong password hashes rather than instantly seeing user passwords.
