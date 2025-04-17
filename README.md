# 🛡️ Secure Data Encryption System

A Streamlit-based secure data storage and retrieval system. Users can store data with a unique passkey and decrypt it only with the correct passkey. The system enforces security by limiting failed attempts and requiring reauthorization.

## 🚀 Features
- **In-memory secure data storage** (no external database required)
- **Fernet encryption** for data security
- **SHA-256 hashed passkeys**
- **Three failed attempts** lockout with forced login
- **Simple login mechanism** for reauthorization
- **User-friendly Streamlit UI**

## 🛠️ Setup
1. **Clone this repository:**
   ```sh
   git clone https://github.com/huzzy12/Secure-Data-Encryption-System.git
   cd Secure-Data-Encryption-System
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```sh
   streamlit run app.py
   ```

## 🔑 Usage
- **Store Data:** Enter your data and a passkey. You’ll receive encrypted text.
- **Retrieve Data:** Paste your encrypted text and enter the same passkey to decrypt.
- **Security:** After three failed attempts, you must log in with the master password.
- **Master Password:** `admin123`

## 📂 Project Structure
- `app.py` — Main Streamlit app
- `requirements.txt` — Python dependencies
- `README.md` — Project documentation

## 📝 Notes
- All data is stored in memory and will be lost when the app stops.
- For production, use more secure authentication and persistent storage.

---

Made with ❤️ using Streamlit and Python.
