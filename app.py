#!/usr/bin/env python3
"""
Streamlit Playground for AI Experiments
"""

__author__ = "Brian Koech"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import streamlit as st

# Setup storage
root_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(root_dir, "images")
data_dir = os.path.join(root_dir, "data")

st.set_page_config(
    page_title="Hello",
    page_icon="🤖",
)
hide_menu = """
<style>
    #MainMenu {
        visibility: hidden;
        }
    footer {
        visibility: visible;
        }
    footer:after {
        content: "Copyright © 2023 - @LibranTechie | All rights reserved | Powered by Python | ";
        display: block;
        position: relative;
        color: tomato;
        align-items: center;
    }
</style>
"""

st.markdown(hide_menu, unsafe_allow_html=True)
st.write("# Hello 👋, Welcome to My Streamlit & AI 🤖 Playground.")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects. I have utilised to build a test bed and portfolio of my AI and Data Science projects.

    **👈 Select a demo from the sidebar** to see some examples.
    ### Want to see more?
    - 🖥️ My Github profile is [@brightmaraba](https://github.com/brightmaraba)
    - 📫 Contact me: [Click here](mailto:brightkoech@libranconsult.com) to send me an email.

    """
)
st.divider()
(
    col1,
    col2,
) = st.columns(2)
with col1:
    image_file = os.path.join(images_dir, "brian.jpg")
    st.image(image_file, use_column_width=True)

with col2:
    st.markdown(
        """
        * Bachelor of Science - Computer Science
            * Maseno University
        * Master of Science - Information Technology
            * Murdoch University
        * Certified Python Developer
            * Python Institute
        """
    )
st.divider()
st.markdown(
    """
### About Me

#### Hi there 👋

1. 👋 Hi, I’m Brian Koech.

2. 👀 My interests are:
    * Software Engineering [Python - Django, DjangoRest, FastAPI, Flask].
    * Data Science/ ML / AI/ NLP [Python - Pandas, Numpy, Scikit-Learn, Matplotlib, Seaborn, Plotly, Streamlit, Dash, PyTorch, TensorFlow, Keras and others].

3. 🌱 I’m working on all the above and learning more technologies.

4. 🌱 Experienced in DevOps and ICT Project Management.

5. 🌱 I love Technical writing and sharing my passion for ICT.
        *My Blog is on [Hashnode]('https://librantechie.tech')*

6. 💞️ I’m looking to collaborate on Software Engineering and Data Science / ML / AI Projects - Applications in Open Data, Education, Agriculture, Water, Climate Change & other Humanitarian centred fields.
7. 🐦 I am on Twitter [@LibranTechie](https://twitter.com/LibranTechie)
8. 📺 Check out my  Youtube Channel [Libran Techie](https://www.youtube.com/c/librantechie)
"""
)
st.divider()
st.markdown(
    """
        | Perpetual Learner | Teacher | Bibliophile | ICT | Python | Data Scientist | ML | AI | NLP | LabEveryday | LibranTechie | Kenya | AU | Motto: Be Teachable |
        """
)
# Add a Image and a link to a blog post in the sidebar
with st.sidebar:
    logo_name = os.path.join(images_dir, "logo.png")
    st.image(logo_name, use_column_width=True)
