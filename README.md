# Streamlit + Notion test app

Write Streamlit apps using Notion!

☠️ **IMPORTANT:** This is just a little prototype I made to play with some ideas. Not meant for production!

* Example app: https://share.streamlit.io/tvst/notionlit/main
* Notion page with source code: https://www.notion.so/streamlit/NotionLit-d500932b258b43298b509eb6dd3db230

  👉 **Try editing the Notion page, then going to the app and pressing `R` to refresh!**

# Forking instructions

1. Fork this app into your own repo
   (or just copy `streamlit_app.py`. It's fully self-contained!)

1. Create [a new integration in Notion](https://www.notion.so/my-integrations).
   When you're done, grab the secret token as you'll need it later.

1. Create a page in Notion, then:
   1. Share it with your integration
   1. Grab the page URL as you'llneed it later.

1. Deploy your app with [share.streamlit.io](https://share.streamlit.io/).

1. [Set up your app's secrets](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management),
   adding in the secret token and page URL from the steps above.
   ```
   [notion]
   token = "YOUR_NOTION_SECRET"
   page_url = "YOUR_NOTION_PAGE_URL"
   ```

**🥳 Done!**

Now any time you edit your Notion page, go into your Streamlit app and press `R` to rerun it
(thereby fetching the latest content from Notion).


# But wait, there's more!

If you add a code block in Notion **and mark it as a Python block,** it will actually get executed
when you load your app!

So try adding a Python block with this into your Notion page:

```
import streamlit as st
import numpy as np

num_rows = st.slider("Number of rows", 1, 500, 100)
data = np.random.randn(num_rows, 5)

st.write(data)
st.line_chart(data)
```

(If you need other Python packages, add them to your `requirements.txt`)

One more thing: let's say you want to execute Python code, but don't want to
polute your Notion page with too much ugly code. There's a hack for that.
Just put the code inside an expander **without a title.**


# What's supported

* Headers
* Paragraphs (with bold/italic/strikethrough/links)
* Images
* Code blocks
* Expanders

And that's all ☹️

Again, this is just a proof-of-concept / prototype. So I didn't implement a bunch of other stuff,
like underline, @page_mentions, columns, etc.

Also note that not everything in Streamlit is supported either. I
don't have an exhaustive list but, for example,
[magic](https://docs.streamlit.io/library/api-reference/write-magic/magic) doesn't work.
