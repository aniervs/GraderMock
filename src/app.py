from typing_extensions import ReadOnly
import streamlit as st 
from streamlit_ace import st_ace
from engine import run_code
from submission import submissions, Submission
import os

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
            st.write(f"{title}") #create page with task here


code = st_ace( "Your code goes here...",
    language="python",
    font_size=13,
    theme="chrome",
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
        st_ace(submission.source_code, key=i, language="python", font_size=11, theme="chrome", readonly=True, auto_update=True)
        display_verdicts(submission.verdicts)


