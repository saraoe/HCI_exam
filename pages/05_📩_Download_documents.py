import streamlit as st

<<<<<<< HEAD
from src.text_anonymization import anon_text, anonymization_str
from src.util import v_spacer, create_zip, remove_files

## setup ##
ex_text = "My neighbor Laura is moving because she got a job at Apple in California."
=======
from src.util import v_spacer, create_zip, remove_files

>>>>>>> fb38d397a770cf3903432d8c23683f100e40d134

## page begins ##
st.subheader(":inbox_tray: Download documents")
st.markdown("---")

if not st.session_state['anon_texts']:
    st.error("You need to upload and assess the documents before you can download them.")
else:
<<<<<<< HEAD
    st.write(f'You have anonymized {len(st.session_state["anon_texts"])} document(s).')
    # example of anonymized text
    with st.expander('See example of anonymized texts'):
        st.write('Initial text:')
        st.write(f'<i>{ex_text}</i>', 
                    unsafe_allow_html=True)
        st.write('Anomymized text:')
        tokens = anon_text(ex_text, 
                           st.session_state['entities'], st.session_state['anonymization_type'])
        anon_ex = anonymization_str(tokens)
        st.write(f'<i>{anon_ex}</i>', 
                    unsafe_allow_html=True)

    # options for download
    v_spacer(height=2)
=======
    # settings
    st.write(f'You have anonymized {len(st.session_state["anon_texts"])} document(s).')
>>>>>>> fb38d397a770cf3903432d8c23683f100e40d134
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