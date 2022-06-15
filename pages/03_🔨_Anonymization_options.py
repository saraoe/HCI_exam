import streamlit as st

from src.text_anonymization import anon_text, anonymization_str
from src.util import v_spacer

## setup ##
with open("descriptions/ner_tags.txt", 'r') as f:
    ner_description = f.read()
with open("descriptions/anonymization_types.txt", 'r') as f:
    anon_types_description = f.read()

## page begins ##
st.subheader(":hammer: Anonymization options")
st.markdown("---")
# select enities
entities = st.multiselect("Entities to anonymize", 
                            ["PER", "LOC",  "ORG"], 
                            default=st.session_state['entities'])
st.session_state['entities'] = entities
with st.expander("Explanation of tags"):
    st.markdown(ner_description)

v_spacer(height=2)
# select type of anonymization
anon_options = {
    "Context preserving": "context_preserving", 
    "Non-context preserving": "full_anonymization"}
current_index = list(anon_options.values()).index(st.session_state['anonymization_type'])
anonymization_type = st.selectbox("Type of anonymization",
                                   anon_options.keys(),
                                   index = current_index)
with st.expander("Explanation of type of anonymization"):
    st.markdown(anon_types_description)


st.session_state['anonymization_type'] = anon_options[anonymization_type]

# update previously saved anonymizations
if st.session_state['anon_texts']:
    with st.spinner('Updating saved anonymized documents...'):
        for name, text in st.session_state['uploaded_files'].items():
            if name not in st.session_state['anon_texts'].keys():
                continue
            # check if annotations exists
            self_anno = st.session_state["self_annotate"].get(name, 
                                                                [[],[],[],[]])
            tokens = anon_text(text, 
                                st.session_state['entities'], st.session_state['anonymization_type'],
                                self_anno[0], self_anno[1], self_anno[2], self_anno[3])
            st.session_state['anon_texts'][name] = anonymization_str(tokens)

# sidebar uploaded documents
v_spacer(height=3, sb=True)
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