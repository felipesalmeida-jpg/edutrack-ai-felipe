import streamlit as st

# ---> COLE A TRAVA EXATAMENTE AQUI, LOGO NO TOPO <---
if "auth_token" not in st.session_state or not st.session_state.auth_token:
    st.warning("⚠️ Acesso negado. Por favor, faça login na página principal.")
    st.stop()