import streamlit as st

from src.util import v_spacer

## setup ##
with open("descriptions/ner_tags.txt", 'r') as f:
    ner_description = f.read()
with open("descriptions/anonymization_types.txt", 'r') as f:
    anon_types_description = f.read()

if 'anonymization_type' not in st.session_state:
    st.session_state['anonymization_type'] = "context_preserving"

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
st.session_state['anonymization_type'] = anon_options[anonymization_type]
with st.expander("Explanation of type of anonymization"):
    st.markdown(anon_types_description)


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