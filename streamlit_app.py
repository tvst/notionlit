from typing import Dict

import streamlit as st
from htbuilder import a, div, styles
from htbuilder.funcs import var
from htbuilder.units import rem
from notion_client import Client
from notion_client.helpers import get_id

notion = Client(auth=st.secrets.notion.token)


def get_page_blocks():
    blocks = notion.blocks.children.list(get_id(st.secrets.notion.page_url))
    return blocks


def get_pure_text_from_text_dict(text):
    return "".join(token["text"]["content"] for token in text)


def get_markdown_from_text_dict(text):
    out = []
    for token in text:
        markdown = None

        if token["type"] == "text":
            markdown = token["text"]["content"]
            annots = token["annotations"]
            if token["text"]["link"]:
                markdown = f'[{markdown}]({token["text"]["link"]["url"]})'
            if annots["bold"]:
                markdown = f"**{markdown}**"
            if annots["italic"]:
                markdown = f"_{markdown}_"
            if annots["strikethrough"]:
                markdown = f"~~{markdown}~~"

        elif token["type"] == "mention":
            mention = token["mention"]

            if mention["type"] == "date":
                date = mention["date"]
                if "end" in date and date["end"] is not None:
                    markdown = f"{date['start']}–{date['end']}"
                else:
                    markdown = date["start"]
            elif mention["type"] == "user":
                user = mention["user"]
                markdown = f"@{user['name']}"

        if markdown:
            out.append(markdown)

    return "".join(out)


def handle_block(block: Dict):
    if block["type"] == "heading_1":
        md = get_markdown_from_text_dict(block["heading_1"]["rich_text"])
        st.write(f"# {md}")

    elif block["type"] == "heading_2":
        md = get_markdown_from_text_dict(block["heading_2"]["rich_text"])
        st.write(f"## {md}")

    elif block["type"] == "heading_3":
        md = get_markdown_from_text_dict(block["heading_3"]["rich_text"])
        st.write(f"### {md}")

    elif block["type"] == "paragraph":
        md = get_markdown_from_text_dict(block["paragraph"]["rich_text"])
        st.write(md)

    elif block["type"] == "image":
        md = get_markdown_from_text_dict(block["image"]["caption"])
        st.image(block["image"]["file"]["url"], md)

    elif block["type"] == "code":
        txt = get_pure_text_from_text_dict(block["code"]["rich_text"])

        # Treat Python codeblocks differently
        if block["code"]["language"] == "python":
            exec(txt, globals())
        else:
            st.code(txt, language=block["code"]["language"])

    elif block["type"] == "toggle":
        md = get_markdown_from_text_dict(block["toggle"]["rich_text"]).strip().lower()
        content_blocks = notion.blocks.children.list(block["id"])

        if (
            (len(md) == 0 or md == "code")  # Title is empty or equal to "Code"
            and content_blocks
            and len(content_blocks["results"])
            == 1  # Only execute if there's a single code block
        ):
            child_block = content_blocks["results"][0]

            if (
                child_block["type"] == "code"
                and child_block["code"]["language"] == "python"
            ):
                txt = get_pure_text_from_text_dict(child_block["code"]["rich_text"])
                exec(txt, globals())
        else:
            with st.expander(md):
                draw_blocks(content_blocks)

    elif block["type"] == "divider":
        st.write("---")

    elif block["type"] == "bulleted_list_item":
        md = get_markdown_from_text_dict(block["bulleted_list_item"]["rich_text"])
        st.write(f"* {md}")

    elif block["type"] == "numbered_list_item":
        md = get_markdown_from_text_dict(block["numbered_list_item"]["rich_text"])
        st.write(f"1. {md}")


def draw_blocks(blocks):
    for block in blocks["results"]:
        try:
            handle_block(block)
        except Exception as e:
            st.exception(e)
            st.expander("Show problematic block").write(block)


st.write(
    str(
        div(style=styles(position="fixed", top=rem(1), left=rem(1), z_index=2147483647,))(
            a(
                href=st.secrets.notion.page_url,
                target="_blank",
                style=styles(
                    color=var("--text-color"),
                    text_decoration="none",
                ),
            )("✏️ Edit")
        )
    ),
    unsafe_allow_html=True,
)


blocks = get_page_blocks()

draw_blocks(blocks)

# with st.expander("Notionlit debug info"):
#     blocks
