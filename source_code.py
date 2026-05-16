import pandas as pd
import os

# ---------------- SAFE FILE PATH ----------------
BASE_DIR = os.path.dirname(__file__)
USER_FILE = os.path.join(BASE_DIR, "users.csv")

# Create file if not exists
if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_FILE, index=False)

# ---------------- SIGNUP ----------------
def signup():
    st.subheader("📝 Create Account")

    username = st.text_input("Username").strip().lower()
    password = st.text_input("Password", type="password").strip()

    if st.button("Sign Up"):
        if username == "" or password == "":
            st.warning("⚠️ Fields cannot be empty")
            return

        df = pd.read_csv(USER_FILE)

        # Normalize existing data
        df["username"] = df["username"].str.strip().str.lower()

        if username in df["username"].values:
            st.warning("⚠️ User already exists")
        else:
            new_user = pd.DataFrame([[username, password]], columns=["username", "password"])
            df = pd.concat([df, new_user], ignore_index=True)
            df.to_csv(USER_FILE, index=False)
            st.success("✅ Account created! Please login.")

# ---------------- LOGIN ----------------
def login():
    st.subheader("🔐 Login")

    username = st.text_input("Username").strip().lower()
    password = st.text_input("Password", type="password").strip()

    if st.button("Login"):
        df = pd.read_csv(USER_FILE)

        # Normalize stored data
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        username = username_input.strip().lower() if username_input else ""
        password = password_input.strip() if password_input else ""

        # Debug (remove later if you want)
        # st.write(df)

        user_match = df[
            (df["username"] == username) &
            (df["password"] == password)
        ]

        if not user_match.empty:
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")
