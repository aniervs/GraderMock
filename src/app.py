from __future__ import annotations

import os

import streamlit as st
import streamlit.components.v1 as components

from streamlit_ace import st_ace

from engine import run_code
from submission import submissions, Submission


if 'theme' not in st.session_state:
    st.session_state['theme'] = 'chrome'


def update_theme():
    components.html("""
    <script>
    const callback = (e) => {
        const theme = e.matches ? "twilight" : "chrome";
        window.parent.postMessage({
            isDarkMode: e.matches,
            theme: theme
        }, "*");
    }
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', callback);
    </script>
    """, height=0, width=0)


update_theme()


def on_theme_change():
    e = st.query_params
    if 'isDarkMode' in e:
        is_dark_mode = e['isDarkMode'][0] == 'true'
        st.session_state['theme'] = 'twilight' if is_dark_mode else 'chrome'


on_theme_change()


def get_Task_names():
    try:
        path = os.path.join(os.getcwd(), 'assets', 'problems')
        elements = os.listdir(path)
        folder_names = [element for element in elements if os.path.isdir(os.path.join(path, element))]

        return folder_names
    except OSError as e:
        print(f"error: {e}")
        return None


def display_verdicts(verdicts: str | list[str]):
    if verdicts == "CE":
        st.error("Compilation Error")
    else:
        for idx, verdict in enumerate(verdicts):
            if verdict == "AC":
                st.success(f"Testcase {idx + 1}: {verdict}")
            else:
                st.error(f"Testcase {idx + 1}: {verdict}")


tasks = get_Task_names()

for title in tasks:
    st.write(title)
    if st.button(f"Open Task {title}"):
        st.write(f"{title}")  # create page with task here

code = st_ace("Your code goes here...",
              language="python",
              font_size=13,
              theme=st.session_state['theme'],
              readonly=False,
              auto_update=True,
              )

if st.button("Submit"):
    st.write("Submitted")
    st.code(code, language='python')

    verdicts = run_code(code, problem_path="example_problem")
    submissions.append(Submission(code, verdicts))
    display_verdicts(verdicts)

if len(submissions) != 0:
    st.write("Submissions")
for i, submission in list(enumerate(submissions))[::-1]:
    with st.expander(f"Submission #{i + 1} -------- {submission.time.strftime('%B %d, %Y, %I:%M:%S')}"):
        st_ace(submission.source_code, key=i, language="python", font_size=11, theme="chrome", readonly=True,
               auto_update=True)
        display_verdicts(submission.verdicts)
