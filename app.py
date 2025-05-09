import streamlit as st
from PIL import Image
import pytesseract
import re

st.set_page_config(page_title="Offer Checker", layout="centered")

st.title("OFFER CHECKER")
st.markdown("**Upload your Uber Eats offer screenshot below:**")

uploaded_file = st.file_uploader(" ", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Screenshot', use_column_width=True)

    with st.spinner("Extracting data..."):
        text = pytesseract.image_to_string(image)

    st.subheader("Detected Text:")
    st.code(text)

    offer_match = re.findall(r"£\s?(\d+(?:\.\d{1,2})?)", text)
    miles_match = re.findall(r"(\d+(?:\.\d+)?)\s?mi", text, re.IGNORECASE)
    mins_match = re.findall(r"(\d+)\s?min", text, re.IGNORECASE)

    try:
        offer = float(offer_match[0])
        miles = float(miles_match[0])
        minutes = float(mins_match[0])

        fuel_cost = miles * 0.15
        hours = minutes / 60
        insurance_cost = hours * 1.5
        profit = offer - fuel_cost - insurance_cost
        hourly_profit = profit / hours if hours > 0 else 0

        st.markdown(f"**Offer:** £{offer}")
        st.markdown(f"**Miles:** {miles}")
        st.markdown(f"**Time:** {minutes} mins")
        st.markdown(f"**Net Hourly Profit:** £{hourly_profit:.2f}")

        if hourly_profit >= 15:
            st.success("ACCEPT")
        else:
            st.error("REJECT")

    except Exception as e:
        st.warning("Could not detect all required values (amount, miles, or minutes).")