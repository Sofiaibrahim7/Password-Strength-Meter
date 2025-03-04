import streamlit as st
import re
import random
import string

# Function to check password strength
def check_password_strength(password):
    strength_score = 0
    feedback = []

    if len(password) >= 8:
        strength_score += 1
    else:
        feedback.append("🔴 Password must be at least 8 characters long.")

    if re.search(r"\d", password):
        strength_score += 1
    else:
        feedback.append("🔴 Add at least one number (0-9).")

    if re.search(r"[A-Z]", password):
        strength_score += 1
    else:
        feedback.append("🔴 Include at least one uppercase letter (A-Z).")

    if re.search(r"[a-z]", password):
        strength_score += 1
    else:
        feedback.append("🔴 Include at least one lowercase letter (a-z).")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength_score += 1
    else:
        feedback.append("🔴 Add at least one special character (!@#$%^&*).")

    # Estimate password crack time
    crack_time = estimate_crack_time(password)

    # Determine password strength level
    if strength_score == 5:
        return "🟢 Strong", "✅ Your password is very secure!", feedback, crack_time
    elif strength_score >= 3:
        return "🟠 Moderate", "⚠️ Your password is okay, but can be improved.", feedback, crack_time
    else:
        return "🔴 Weak", "❌ Your password is too weak. Try making it stronger.", feedback, crack_time

# Function to estimate password crack time
def estimate_crack_time(password):
    length = len(password)
    complexity = len(set(password))  # Count unique characters
    estimated_time = (complexity ** length) / 10**6  # Rough estimate in seconds

    if estimated_time > 31556952 * 100:  # More than 100 years
        return "∞ (Extremely Secure)"
    elif estimated_time > 31556952:  # More than 1 year
        return "💎 More than 1 year"
    elif estimated_time > 86400:  # More than 1 day
        return f"🕒 {int(estimated_time // 86400)} days"
    elif estimated_time > 3600:  # More than 1 hour
        return f"⌛ {int(estimated_time // 3600)} hours"
    else:
        return f"⚡ {int(estimated_time)} seconds"

# Function to generate a strong password
def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()?"
    return "".join(random.choice(chars) for _ in range(12))

# Streamlit UI
st.set_page_config(page_title="Password Strength Checker", page_icon="🔑", layout="centered")

st.title("🔑 Password Strength Meter")
st.write("Check your password strength and get security tips.")

# Password input field
password = st.text_input("Enter a password:", type="password")

# Button to check password strength
if st.button("🔍 Check Password Strength"):
    if password:
        strength, message, feedback, crack_time = check_password_strength(password)

        # Display Password Strength
        st.subheader(f"Password Strength: {strength}")
        st.info(message)

        # Display Password Strength Bar
        strength_percentage = len(password) * 10
        st.progress(min(strength_percentage, 100))

        # Show Crack Time Estimate
        st.write(f"⏳ Estimated Time to Crack: **{crack_time}**")

        # Show Suggestions if Weak or Moderate
        if feedback:
            st.warning("🔍 Here’s how you can improve your password:")
            for tip in feedback:
                st.write(f"- {tip}")

        # Display Strong Password Tips
        st.write("### 🔹 How to Create a Strong Password:")
        st.markdown("""
        - ✅ Use **at least 12 characters**
        - ✅ Include **uppercase (A-Z) & lowercase (a-z) letters**
        - ✅ Add **numbers (0-9)**
        - ✅ Use **special characters (!@#$%^&*)**
        - ✅ Avoid using personal details like **your name or birthdate**
        """)
    else:
        st.error("⚠️ Please enter a password before checking.")

# Generate Strong Password Button
if st.button("🔄 Generate Strong Password"):
    strong_password = generate_password()
    st.success(f"💡 Try this strong password: **{strong_password}**")
