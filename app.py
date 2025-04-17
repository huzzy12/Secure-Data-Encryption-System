import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# Streamlit session state initialization
if 'stored_data' not in st.session_state:
    st.session_state['stored_data'] = {}  # {encrypted_text: {"encrypted_text":..., "passkey":...}}
if 'failed_attempts' not in st.session_state:
    st.session_state['failed_attempts'] = 0
if 'reauth' not in st.session_state:
    st.session_state['reauth'] = False

# Generate a key (should be stored securely in production)
if 'fernet_key' not in st.session_state:
    st.session_state['fernet_key'] = Fernet.generate_key()
cipher = Fernet(st.session_state['fernet_key'])

# Function to hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Function to encrypt data
def encrypt_data(text, passkey):
    return cipher.encrypt(text.encode()).decode()

# Function to decrypt data
# Returns decrypted_text if correct, None if not
# Increments failed_attempts if incorrect
# Resets failed_attempts if correct
# Returns 'locked' if too many failed attempts

def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)
    stored_data = st.session_state['stored_data']
    for key, value in stored_data.items():
        if value["encrypted_text"] == encrypted_text and value["passkey"] == hashed_passkey:
            st.session_state['failed_attempts'] = 0
            return cipher.decrypt(encrypted_text.encode()).decode()
    st.session_state['failed_attempts'] += 1
    if st.session_state['failed_attempts'] >= 3:
        st.session_state['reauth'] = True
        return 'locked'
    return None

# --- Streamlit UI ---
st.set_page_config(page_title="Secure Data Encryption System", page_icon="🔒")
st.title("🔒 Secure Data Encryption System")

# Navigation logic
menu = ["Home", "Store Data", "Retrieve Data", "Login"]

# If forced reauth, only allow Login page
if st.session_state['reauth']:
    menu = ["Login"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")

elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")
    if st.button("Encrypt & Save"):
        if user_data and passkey:
            hashed_passkey = hash_passkey(passkey)
            encrypted_text = encrypt_data(user_data, passkey)
            st.session_state['stored_data'][encrypted_text] = {"encrypted_text": encrypted_text, "passkey": hashed_passkey}
            st.success(f"✅ Data stored securely!\nEncrypted Data: {encrypted_text}")
        else:
            st.error("⚠️ Both fields are required!")

elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    encrypted_text = st.text_area("Enter Encrypted Data:")
    passkey = st.text_input("Enter Passkey:", type="password")
    if st.button("Decrypt"):
        if encrypted_text and passkey:
            result = decrypt_data(encrypted_text, passkey)
            if result == 'locked':
                st.warning("🔒 Too many failed attempts! Redirecting to Login Page.")
                st.rerun()
            elif result:
                st.success(f"✅ Decrypted Data: {result}")
            else:
                attempts_left = 3 - st.session_state['failed_attempts']
                st.error(f"❌ Incorrect passkey! Attempts remaining: {attempts_left}")
        else:
            st.error("⚠️ Both fields are required!")
    st.info(f"Failed attempts: {st.session_state['failed_attempts']} (Max 3)")

elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_pass = st.text_input("Enter Master Password:", type="password")
    if st.button("Login"):
        if login_pass == "admin123":  # Hardcoded for demo
            st.session_state['failed_attempts'] = 0
            st.session_state['reauth'] = False
            st.success("✅ Reauthorized successfully! Redirecting to Retrieve Data...")
            st.rerun()
        else:
            st.error("❌ Incorrect password!")
