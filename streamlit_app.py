import streamlit as st
from notion_client import Client
from notion_client.helpers import get_id
from collections import namedtuple, defaultdict
import datetime
import pandas as pd
import calendar

PAGE_URL = 'https://www.notion.so/streamlit/NotionLit-d500932b258b43298b509eb6dd3db230'
the_token = st.secrets.notion.token

TTL = 0 #12*60*60

@st.cache(allow_output_mutation=True, ttl=TTL)
def _get_blocks():
    notion = Client(auth=the_token)
    blocks = notion.blocks.children.list(get_id(PAGE_URL))
    return blocks

def get_pure_text_from_text_dict(text):
    return ''.join(token['text']['content'] for token in text)

def get_markdown_from_text_dict(text):
    out = []
    for token in text:
        if token['type'] == 'text':
            markdown = token['text']['content']
            annots = token['annotations']
            if token['text']['link']:
                markdown = f'[{markdown}]({token["text"]["link"]})'
            if annots['bold']:
                markdown = f'**{markdown}**'
            if annots['italic']:
                markdown = f'_{markdown}_'
            if annots['strikethrough']:
                markdown = f'~~{markdown}~~'
            out.append(markdown)

    return ''.join(out)

blocks = _get_blocks()

#blocks

for block in blocks['results']:
    if block['type'] == 'heading_1':
        md = get_markdown_from_text_dict(block['heading_1']['text'])
        st.write(f'# {md}')

    if block['type'] == 'heading_2':
        md = get_markdown_from_text_dict(block['heading_2']['text'])
        st.write(f'## {md}')

    if block['type'] == 'heading_3':
        md = get_markdown_from_text_dict(block['heading_3']['text'])
        st.write(f'### {md}')

    if block['type'] == 'paragraph':
        md = get_markdown_from_text_dict(block['paragraph']['text'])
        st.write(md)

    if block['type'] == 'image':
        md = get_markdown_from_text_dict(block['image']['caption'])
        st.image(block['image']['file']['url'], md)

    if block['type'] == 'code':
        txt = get_pure_text_from_text_dict(block['code']['text'])
        if block['code']['language'] == 'python':
            exec(txt)
        else:
            st.code(txt, language=block['code']['language'])
