import streamlit as st
from PIL import Image

from src.util import resize_image, v_spacer

## setup ##
# descriptions
with open("descriptions/app.txt", 'r') as f:
    app_description = f.read()
with open("descriptions/pages.txt", 'r') as f:
    pages_description = f.read()

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
if 'anonymization_type' not in st.session_state:
    st.session_state['anonymization_type'] = "context_preserving"


## page begins ##
_, col2, _ = st.columns([0.5,2,0.5])
col2.image(resize_image(logo, 0.6))
<<<<<<< HEAD
# hide fullscreen option on logo
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

=======
>>>>>>> fb38d397a770cf3903432d8c23683f100e40d134
st.markdown("---")
st.markdown(app_description)
with st.expander("How to use HIanonymizer"):
    st.markdown(pages_description)


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