import streamlit as st
from annotated_text import annotated_text

from src.text_anonymization import *
from src.util import v_spacer

## setup ##
assess_description = """Assess the annotations made by the model 
and change annotations that are incorrect by selecting the tokens
in the expander below."""

st.markdown("""
            <style>
            div.stButton > button:first-child {
                height: 2em; 
                width: 8em;
            }
            </style>""", unsafe_allow_html=True)


## page begins ##
st.subheader(":eyes: Assess documents")
st.markdown("---")
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
    with st.expander('Manual annotation'):
        self_anno = st.session_state["self_annotate"].get(name, 
                                                            [[],[],[],[]])
        col1, col2 = st.columns(2)
        per_tokens = col1.multiselect("Add name annotation:",
                                        get_non_entity_tokens(text, []),
                                        default = self_anno[0],
                                        disabled=("PER" not in st.session_state['entities']))
        loc_tokens = col2.multiselect("Add location annotation:",
                                        get_non_entity_tokens(text, []),
                                        default = self_anno[1],
                                        disabled=("LOC" not in st.session_state['entities']))
        org_tokens = col1.multiselect("Add organization annotation:",
                                        get_non_entity_tokens(text, []),
                                        default = self_anno[2],
                                        disabled=("ORG" not in st.session_state['entities']))
        non_entity_tokens = col2.multiselect("Remove annotation:",
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
    tokens = anon_text(text, 
                    st.session_state['entities'], 
                    st.session_state['anonymization_type'],
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
    _, col2, _, = st.columns([1.2, 1, 1.2])
    if col2.button('Save current', kwargs={'n_buttons': 2}):
        st.session_state['anon_texts'][name] = anonymization_str(tokens)
    # save all annotations
    # _, col2, _, = st.columns([2, 1, 2])
    if col2.button("Save all"):
        for name, text in st.session_state['uploaded_files'].items():
            if name not in st.session_state['anon_texts'].keys():
                # check if annotations exists
                self_anno = st.session_state["self_annotate"].get(name, 
                                                                    [[],[],[],[]])
                tokens = anon_text(text, 
                                    st.session_state['entities'], st.session_state['anonymization_type'],
                                    self_anno[0], self_anno[1], self_anno[2], self_anno[3])
                st.session_state['anon_texts'][name] = anonymization_str(tokens)
    
    # buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button('Previous text', disabled = (i == 0)):
        st.session_state['n_file'] -= 1
        st.experimental_rerun()
    if col5.button('Next text', disabled = (i == len(names_texts)-1)):
        st.session_state['n_file'] += 1
        st.experimental_rerun()
    col3.write(f'text {i+1} of {len(names_texts)}')

    # status
    v_spacer(height=2)
    _, col2, _ = st.columns([1.4, 1, 1.4])
    if name in st.session_state['anon_texts']:
        if anonymization_str(tokens) != st.session_state['anon_texts'][name]:
            status = '<font color="orange"> Unsaved changes</font>'
        else:
            status = '<font color="green"> Saved</font> :heavy_check_mark:'
    else:
        status = '<font color="red"> Unsaved</font> :heavy_multiplication_x:'
    col2.markdown(f'Status: {status}', unsafe_allow_html=True)


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
