# ftw-pki-receiver

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL_v2.1-blue.svg)](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
[![Coverage: 93%](https://img.shields.io/badge/coverage-94%25-brightgreen.svg)]

The secure ingestion, validation, and decryption gateway of the **ftw-pki** suite. This repository provides the `ftwpkireceiver` utility.

## 🛠 Why do we need a Receiver?

In high-security PKI environments, signing entities (especially Root and Intermediate CAs) often operate in restricted or offline environments. They should never be directly exposed to raw, unvalidated input from the network.

The **Receiver** acts as a "buffer, filter, and delivery endpoint":

1. **Ingestion & Sanitization:** It collects Certificate Signing Requests (CSRs) and pre-validates them against defined security policies before they ever reach the signing tools.
2. **Security Boundary:** It ensures that only well-formed and authorized requests are passed forward, protecting the sensitive signing infrastructure from malformed data or injection attacks.
3. **Secure Decryption:** Signed certificates are returned encrypted with the sender's public key. The Receiver uses the corresponding private key to decrypt the payload, making the certificate available to the end-user.

## ✨ Features

* **Automated Configuration:** On its first run, the tool automatically initializes the necessary configuration files in the user's config directory (e.g., `~/.config/ftwpki/`).
* **Integrity Checks:** Verifies the cryptographic signatures of incoming CSRs to ensure they haven't been tampered with during transit.
* **Minimalist CLI:** Designed to be as simple as possible to minimize the attack surface, requiring only essential positional arguments.

## 🚀 Quick Start

Since the tool handles its own configuration, you can start processing packages immediately.

```bash
# Usage: ftwpkireceiver <private_key> <received_package>
ftwpkireceiver ./path/to/private_key.pem ./path/to/encrypted_package.bin
```

## 📖 Documentation

* **Technical Manual:** Detailed information on validation rules and security handshakes is available in the `doc/source/` directory.
* **User Config:** If you need to adjust policies, refer to the config file automatically created in your user profile.

## 📄 License

This project is licensed under the **LGPL v2.1 (or later)**.

---
© 2026 ftw-pki Contributors
