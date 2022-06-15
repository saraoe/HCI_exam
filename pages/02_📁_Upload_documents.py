import streamlit as st
from io import StringIO 

from src.util import v_spacer


st.subheader(":file_folder: Upload documents")
st.markdown("---")
st.write('**Upload new documents:**')
uploaded_files = st.file_uploader("You can choose one or multiple files", 
                                    accept_multiple_files=True)

v_spacer(height=2)
st.write('**Already uploaded documents:**')
if st.session_state['uploaded_files']:
    # with st.expander('Already uploaded documents'):
    col1, col2, col3 = st.columns(3)
    for i, (name, _) in enumerate(st.session_state["uploaded_files"].items()):
        col1.write(name)
        if name in st.session_state['anon_texts']:
            anno_symbol = ":heavy_check_mark:"  
        else:
            anno_symbol = ':heavy_multiplication_x:'
        col2.write(f'Anonymized: {anno_symbol}')

        m = st.markdown("""
            <style>
            div.stButton > button:first-child {
                height: 1.5em; 
            }
            </style>""", unsafe_allow_html=True)
        if col3.button('remove', key=f'{i}'):
            st.session_state["uploaded_files"].pop(name)
            if name in st.session_state['anon_texts'].keys():
                st.session_state['anon_texts'].pop(name)
            st.experimental_rerun()

if uploaded_files:
    # make dict of texts
    for uploaded_file in uploaded_files:
        name = uploaded_file.name
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        string_data = stringio.read()
        st.session_state["uploaded_files"][name] = string_data


# sidebar uploaded documents
v_spacer(height=2, sb=True)
st.sidebar.write("**Uploaded documents**")
if st.session_state["uploaded_files"]:
    col1, col2 = st.sidebar.columns(2)
    for i, (name, _) in enumerate(st.session_state["uploaded_files"].items()):
        col1.write(name)
        if name in st.session_state['anon_texts']:
            anno_symbol = ":heavy_check_mark:"  
        else:
            anno_symbol = ':heavy_multiplication_x:'
        col2.write(f'Anonymized: {anno_symbol}')
else:
    st.sidebar.write('*None*')