<!-- SPONSOR-START -->
---

<div align="center">

### 🌐 Need Proxies? Check out my services

<a href="https://vaultproxies.com" target="_blank" rel="noopener noreferrer">
  <img src="https://i.imgur.com/TF165pP.gif" alt="VaultProxies">
</a>
<p></p>

<table>
  <tr>
    <th>Service</th>
    <th>Pricing</th>
    <th>Features</th>
  </tr>
  <tr>
    <td><b><a href="https://vaultproxies.com" target="_blank" rel="noopener noreferrer">🔮 VaultProxies</a></b></td>
    <td><code>$1.00/GB</code> residential</td>
    <td>Residential · IPv6 · Residential Unlimited · Datacenter</td>
  </tr>
  <tr>
    <td><b><a href="https://nullproxies.com" target="_blank" rel="noopener noreferrer">🌑 NullProxies</a></b></td>
    <td><code>$0.75/GB</code> residential</td>
    <td>Residential · Residential Unlimited · DC Unlimited · Mobile Proxies</td>
  </tr>
  <tr>
    <td><b><a href="https://strikeproxy.net" target="_blank" rel="noopener noreferrer">⚡ StrikeProxy</a></b></td>
    <td><code>$0.75/GB</code> residential</td>
    <td>Residential · Residential Unlimited · DC Unlimited · Mobile Proxies</td>
  </tr>
</table>
</div>

<!-- SPONSOR-END -->

<div align="center">
  <h2 align="center">Duolingo Account Generator</h2>
  <p align="center">
   This script helps you create Duolingo accounts automatically. It can make three types of accounts: unclaimed (just created), claimed (with email and password), and verified (fully activated). The tool uses proxies, random device settings, and fake emails to look like a real user. It’s fast, works with multiple threads, and saves the account info in neat files.
    <br />
    <br />
    <a href="https://discord.cyberious.xyz">💬 Discord</a>
    ·
    <a href="https://github.com/sexfrance/Duolingo-Account-Creator#-changelog">📜 ChangeLog</a>
    ·
    <a href="https://github.com/sexfrance/Duolingo-Account-Creator/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/sexfrance/Duolingo-Account-Creator/issues">💡 Request Feature</a>
  </p>
</div>

---

### ⚙️ Installation

- Requires: `Python 3.7+`
- Make a python virtual environment: `python3 -m venv venv`
- Source the environment: `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (macOS, Linux)
- Install the requirements: `pip install -r requirements.txt`

---

### 🔥 Features

- Automatically generates Duolingo accounts in three modes: Unclaimed, Claimed, Verified.
- Supports customizable proxy integration for account creation.
- Randomized user-agents to mimic real device behavior.
- Handles temporary email generation and verification.
- Multi-threaded support for fast account generation.

---

### ⭐ Milestones
**15 stars**: Adding humanization

---
### 📝 Usage

1. **Preparation**:

   - Place your proxy list in `input/proxies.txt` (optional for proxy-based usage).
   - Configure settings in `config.toml`.

2. **Running the script**:

   ```bash
   python main.py
   ```

3. **Output**:
   - Unclaimed accounts: `output/unclaimed/accounts.txt`
   - Claimed accounts: `output/claimed/accounts.txt`
   - Verified accounts: `output/verified/accounts.txt`
   - Full account capture (verified): `output/verified/full_account_capture.txt`

---

### 📹 Preview

![Preview](https://i.imgur.com/KvNyObg.gif)

---

### ❗ Disclaimers

- This project is for educational purposes **only**. Its goal is to understand Duolingo's API better. Do not use it to mass-generate accounts as this is against their terms of service.
- The author is not responsible for any consequences, such as API blocking, IP bans, or account suspension.
- This is a fun and experimental project. For further updates, star the repo & create an "issue" [here](https://github.com/sexfrance/Duolingo-Account-Creator/issues).

---

### 📜 ChangeLog

```diff
v0.0.1 ⋮ 12/07/2024
! Initial release with Duolingo account generation feature
```

<p align="center">
  <img src="https://img.shields.io/github/license/sexfrance/Duolingo-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/sexfrance/Duolingo-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/sexfrance/Duolingo-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python"/>
</p>
