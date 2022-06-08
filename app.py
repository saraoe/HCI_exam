'''
Streamlit app for the anonymization tool
'''
import streamlit as st
from io import StringIO 
from PIL import Image
from annotated_text import annotated_text

from src.text_anonymization import *
from src.util import *

# descriptions
with open("descriptions/app.txt", 'r') as f:
    app_description = f.read()
with open("descriptions/pages.txt", 'r') as f:
    pages_description = f.read()
with open("descriptions/ner_tags.txt", 'r') as f:
    ner_description = f.read()
assess_description = """Assess the annotations made by the model 
and change annotations that are incorrect by selecting the tokens
in the expander below."""

logo = Image.open('fig/logo-removebg.png')
logo_size = logo.size

# session states
if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = {}
if "entities" not in st.session_state:
        st.session_state['entities'] = ["PER", "LOC", "ORG"]
if "anon_texts" not in st.session_state:
    st.session_state['anon_texts'] = {}
if "self_annotate" not in st.session_state:
    st.session_state['self_annotate'] = {}

# menu
st.sidebar.image(resize_image(logo, 0.25))
st.sidebar.subheader('Navigation')
menu = st.sidebar.radio("Go to", ["Getting started", 
                             "Upload documents",
                             "Anonymization options", 
                             "Assess documents",
                             "Download documents"])
    
if menu == "Getting started":
    _, col2, _ = st.columns([0.5,2,0.5])
    col2.image(resize_image(logo, 0.6))
    st.markdown("---")
    st.markdown(app_description)
    with st.expander("How to use HIanonymizer"):
        st.markdown(pages_description)

if menu == "Upload documents":
    st.subheader(":file_folder: Upload documents")
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
            if i % 2 == 0:
                col1.write('')
                col2.write('')
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
    
if menu == "Anonymization options":
    st.subheader(":hammer: Anonymization options")
    # select enities
    entities = st.multiselect("Entities to anonymize", 
                              ["PER", "LOC",  "ORG"], 
                              default=st.session_state['entities'])
    st.session_state['entities'] = entities
    with st.expander("Explanation of tags"):
        st.markdown(ner_description)

if menu == "Assess documents":
    st.subheader(":eyes: Assess documents")
    if not st.session_state['uploaded_files']:
        st.error("You need to upload documents to assess the anonymization")
    else:
        st.write(assess_description)
        names_texts=[]
        for elem in st.session_state["uploaded_files"].items():
            names_texts.append(elem)
        # view the file
        if 'n_file' not in st.session_state:
            st.session_state['n_file'] = 0
        if names_texts and st.session_state['n_file'] >= len(names_texts):
            st.session_state['n_file'] = len(names_texts)-1
        i = st.session_state['n_file']
        name, text = names_texts[i]

        # self annotated tokens
        with st.expander('Select tokens that are not annotated correctly'):
            self_anno = st.session_state["self_annotate"].get(name, 
                                                              [[],[],[],[]])
            col1, col2 = st.columns(2)
            per_tokens = col1.multiselect("Name tokens:",
                                          get_non_entity_tokens(text, []),
                                          default = self_anno[0],
                                          disabled=("PER" not in st.session_state['entities']))
            loc_tokens = col2.multiselect("Location tokens:",
                                          get_non_entity_tokens(text, []),
                                          default = self_anno[1],
                                          disabled=("LOC" not in st.session_state['entities']))
            org_tokens = col1.multiselect("Organization tokens:",
                                          get_non_entity_tokens(text, []),
                                          default = self_anno[2],
                                          disabled=("ORG" not in st.session_state['entities']))
            non_entity_tokens = col2.multiselect("Not entity tokens:",
                                                 get_entity_tokens(text, 
                                                        st.session_state['entities']),
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
        
        v_spacer(height=3)
        # save the anonymized texts
        _, col2, _, = st.columns([1.5, 1, 1.5])
        if col2.button('Save current'):
            st.session_state['anon_texts'][name] = anonymization_str(tokens)
        # save all annotations
        _, col2, _, = st.columns([2, 1, 2])
        if col2.button("Save all"):
            for name, text in st.session_state['uploaded_files'].items():
                if name not in st.session_state['anon_texts'].keys():
                    # check if annotations exists
                    self_anno = st.session_state["self_annotate"].get(name, 
                                                                      [[],[],[],[]])
                    tokens = anon_text(text, st.session_state['entities'],
                                        self_anno[0], self_anno[1], self_anno[2], self_anno[3])
                    st.session_state['anon_texts'][name] = anonymization_str(tokens)
        
        # buttons
        col1, col2, col3, col4, col5 = st.columns(5)
        if col1.button('Previous text', disabled = (i == 0)):
            # if st.session_state['n_file'] == 0:
            #     st.session_state['n_file'] = len(texts)
            st.session_state['n_file'] -= 1
            st.experimental_rerun()
        if col5.button('Next text', disabled = (i == len(names_texts)-1)):
            # if st.session_state['n_file'] == len(texts)-1:
            #     st.session_state['n_file'] = -1
            st.session_state['n_file'] += 1
            st.experimental_rerun()
        col3.write(f'text {i+1} of {len(names_texts)}')

if menu == "Download documents":
    st.subheader(":inbox_tray: Download documents")

    if not st.session_state['anon_texts']:
        st.error("You need to upload and assess the documents before you can download them.")
    else:
        # settings
        st.write(f'You have anonymized {len(st.session_state["anon_texts"])} document(s).')
        st.write("You can chose the file type you want the downloaded files in and the prefix of the anonymized files.")
        file_type = st.selectbox("File type", [".txt", ".pdf", ".docx"])
        prefix = st.text_input("Prefix", "anon")

        # download files
        remove_files("anonymized_texts")
        for name, text in st.session_state['anon_texts'].items():
            with open(f'anonymized_texts/{prefix}_{name}', 'w', encoding="utf-8") as f:
                f.write(text)
        anon_zip = create_zip()
        v_spacer(height = 2)
        _, col2, _ = st.columns(3)
        col2.download_button("Download anonymized texts", 
                            anon_zip, 
                            file_name="anonymized_texts.zip")

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