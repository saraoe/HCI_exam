'''
Streamlit app for the anonymization tool
'''
import streamlit as st
from io import StringIO 
from annotated_text import annotated_text

from src.text_anonymization import anon_text, get_entity_tokens, get_non_entity_tokens
from src.util import create_zip

st.title("Text Anonymization")

# st.text("Insert description of app")

texts = []
uploaded_files = st.sidebar.file_uploader("Choose a one or multiple files", 
                                          accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        name = uploaded_file.name
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        string_data = stringio.read()
        texts.append((name, string_data))

    # view the file
    if 'n_file' not in st.session_state:
        st.session_state['n_file'] = 0

    i = st.session_state['n_file']
    name, text = texts[i]

    # self annotated tokens
    st.write('Select tokens that are not annotated correctly')
    col1, col2, col3 = st.columns(3)
    per_tokens = col1.multiselect("Name tokens:",
                                     get_non_entity_tokens(text))
    loc_tokens = col2.multiselect("Location tokens:",
                                     get_non_entity_tokens(text))
    org_tokens = col3.multiselect("Organization tokens:",
                                     get_non_entity_tokens(text))
    non_entity_tokens = st.multiselect("Non entity tokens:",
                                        get_entity_tokens(text))

    # annotated text
    tokens = anon_text(text, ["LOC", "PER", "ORG"], per_tokens)
    annotated_text(*tokens)
    # text name
    st.markdown(f"<h1 style='text-align:right;color:grey; font-size:12px;'><i>Text: {name}</i></h1>", 
                unsafe_allow_html=True)
    
    # buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button('Previous text'):#, disabled = (i == 0)):
        if st.session_state['n_file'] == 0:
            st.session_state['n_file'] = len(texts)
        st.session_state['n_file'] -= 1
    if col5.button('Next text'):#, disabled = (i == len(texts)-1)):
        if st.session_state['n_file'] == len(texts)-1:
            st.session_state['n_file'] = -1
        st.session_state['n_file'] += 1
    col3.write(f'text {i+1} of {len(texts)}')

    # save the anonymized texts
    anonymized = []
    for token in tokens:
        if isinstance(token, tuple):
            anonymized.append(token[0])
        else:
            anonymized.append(token)

    with open(f'anonymized_texts/anon_{name}', 'w') as f:
        f.write(' '.join(anonymized))


anon_zip = create_zip()
st.sidebar.download_button("Download anonymized texts", 
                            anon_zip, 
                            file_name="anonymized_texts.zip")