import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Buku Tamu Digital", layout="centered")

# Google Sheets authorization
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

# Google Sheet ID
SHEET_ID = "1vTCOg7uD6bX7PwYrclBNOBbR3TU3no_sSRzRYOXilq0"
sheet = client.open_by_key(SHEET_ID).sheet1


# Sidebar menu
menu = st.sidebar.radio("Menu", ["Isi Buku Tamu", "Lihat Data Tamu"])


# ==========================
# Form Input Tamu
# ==========================
if menu == "Isi Buku Tamu":
    st.title("📘 Buku Tamu Digital")

    with st.form("form_bukutamu"):
        nama = st.text_input("Nama")
        email = st.text_input("Email")
        instansi = st.text_input("Instansi / Perusahaan")
        pesan = st.text_area("Pesan / Keperluan")

        submit = st.form_submit_button("Kirim")

    if submit:
        if nama == "":
            st.warning("Nama wajib diisi!")
        else:
            sheet.append_row([nama, email, instansi, pesan, str(datetime.now())])
            st.success("Terima kasih! Data berhasil disimpan!")


# ==========================
# Halaman Admin Data Tamu
# ==========================
elif menu == "Lihat Data Tamu":
    st.title("📄 Data Tamu Masuk")

    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if df.empty:
        st.info("Belum ada data.")
    else:
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "buku_tamu.csv", "text/csv")
