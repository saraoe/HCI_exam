'''
Streamlit app for the anonymization tool
'''
import streamlit as st
from io import StringIO 
from annotated_text import annotated_text

from src.text_anonymization import anon_text, get_entity_tokens, get_non_entity_tokens
from src.util import create_zip, v_spacer, remove_files

st.title("Text Anonymization")
app_description = "Insert description of app"

# session states
if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = None
if "entities" not in st.session_state:
        st.session_state['entities'] = ["LOC", "PER", "ORG"]
if "anon_texts" not in st.session_state:
    st.session_state['anon_texts'] = {}
if "self_annotate" not in st.session_state:
    st.session_state['self_annotate'] = {}

# menu
menu = st.sidebar.radio("", ["Welcome page", 
                             "Upload documents and anonymization options", 
                             "Assess documents",
                             "Download documents"])
    
if menu == "Welcome page":
    st.write(app_description)

if menu == "Upload documents and anonymization options":
    st.subheader(":file_folder: Upload documents")
    uploaded_files = st.file_uploader("You can choose one or multiple files", 
                                        accept_multiple_files=True,
                                        key = "1")
    if uploaded_files:
        # make list of texts
        texts = []
        for uploaded_file in uploaded_files:
            name = uploaded_file.name
            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            # To read file as string:
            string_data = stringio.read()
            texts.append((name, string_data))
        st.session_state["uploaded_files"] = texts
    # else:
    #     st.session_state["uploaded_files"] = None
    
    v_spacer(height=2)
    st.subheader(":hammer: Anonymization options")
    # select enities
    entities = st.multiselect("Entities to anonymize", 
                              ["LOC", "PER", "ORG"], 
                              default=st.session_state['entities'])
    st.session_state['entities'] = entities

if menu == "Assess documents":
    st.subheader(":eyes: Assess documents")
    if not st.session_state['uploaded_files']:
        st.write("You need to upload documents to assess the anonymization")
    else:
        texts = st.session_state["uploaded_files"]
        # view the file
        if 'n_file' not in st.session_state:
            st.session_state['n_file'] = 0

        i = st.session_state['n_file']
        name, text = texts[i]

        # self annotated tokens
        with st.expander('Select tokens that are not annotated correctly'):
            self_anno = st.session_state["self_annotate"].get(name, 
                                                              [[],[],[],[]])
            col1, col2 = st.columns(2)
            per_tokens = col1.multiselect("Name tokens:",
                                          get_non_entity_tokens(text, []),
                                          default = self_anno[0])
            loc_tokens = col2.multiselect("Location tokens:",
                                          get_non_entity_tokens(text, []),
                                          default = self_anno[1])
            org_tokens = col1.multiselect("Organization tokens:",
                                          get_non_entity_tokens(text, []),
                                          default = self_anno[2])
            non_entity_tokens = col2.multiselect("Not entity tokens:",
                                                  get_entity_tokens(text),
                                                  default = self_anno[3])
            st.session_state["self_annotate"][name] = [
                per_tokens,
                loc_tokens,
                org_tokens,
                non_entity_tokens
            ]

        # annotated text
        v_spacer(height=3)
        tokens = anon_text(text, st.session_state['entities'], 
                        per_tokens,
                        loc_tokens,
                        org_tokens,
                        non_entity_tokens)
        annotated_text(*tokens)
        # text name
        st.markdown(f"<h1 style='text-align:right;color:grey; font-size:12px;'><i>Filename: {name}</i></h1>", 
                    unsafe_allow_html=True)
        
        # buttons
        v_spacer(height=3)
        col1, col2, col3, col4, col5 = st.columns(5)
        if col1.button('Previous text', disabled = (i == 0)):
            # if st.session_state['n_file'] == 0:
            #     st.session_state['n_file'] = len(texts)
            st.session_state['n_file'] -= 1
            st.experimental_rerun()
        if col5.button('Next text', disabled = (i == len(texts)-1)):
            # if st.session_state['n_file'] == len(texts)-1:
            #     st.session_state['n_file'] = -1
            st.session_state['n_file'] += 1
            st.experimental_rerun()
        col3.write(f'text {i+1} of {len(texts)}')

        # save the anonymized texts
        anonymized = []
        for token in tokens:
            if isinstance(token, tuple):
                anonymized.append(token[0])
            else:
                anonymized.append(token)
        st.session_state['anon_texts'][name] = ' '.join(anonymized)

if menu == "Download documents":
    st.subheader(":inbox_tray: Download documents")

    if not st.session_state['uploaded_files']:
        st.write("You need to upload and assess the documents, before you can download them.")
    else:
        # settings
        st.write("You can chose the file format you want the downloaded files in, and the prefix of the files.")
        file_type = st.selectbox("File type", [".txt", ".pdf", ".docx"])
        prefix = st.text_input("Prefix", "anon")

        # download files
        remove_files("anonymized_texts")
        for name, text in st.session_state['anon_texts'].items():
            with open(f'anonymized_texts/{prefix}_{name}', 'w') as f:
                f.write(text)
        anon_zip = create_zip()
        v_spacer(height = 2)
        _, col2, _ = st.columns(3)
        col2.download_button("Download anonymized texts", 
                            anon_zip, 
                            file_name="anonymized_texts.zip")