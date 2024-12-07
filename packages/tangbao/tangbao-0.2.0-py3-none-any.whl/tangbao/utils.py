from contextlib import contextmanager
from io import StringIO
from streamlit.runtime.scriptrunner.script_run_context import SCRIPT_RUN_CONTEXT_ATTR_NAME
from threading import current_thread
import sys
import pandas as pd
import streamlit as st
import os
from typing import Dict, Any

def extract_code_from_log(file_path):
    """
    Extracts code snippets from a log file.

    Args:
        file_path (str): The path to the log file.

    Returns:
        str: The extracted code snippet.

    Example:
        code_snippet = extract_code_from_log('path/to/log.txt')
        print(code_snippet)
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    indices_code_running = [i for i, line in enumerate(lines) if "Code running:" in line]
    if len(indices_code_running) < 1:
        return "No code in the log"
    start_index = indices_code_running[-1]

    indices_triple_backtick = [i for i, line in enumerate(lines) if "```" in line]
    if not indices_triple_backtick:
        raise ValueError("The phrase '```' does not occur in the file.")
    end_index = indices_triple_backtick[-1]

    extracted_lines = lines[start_index+2:end_index]

    return ''.join(extracted_lines)

@contextmanager
def st_redirect(src, dst):
    """
    Context manager to redirect streamlit output.

    Args:
        src (stream): Source stream.
        dst (callable): Destination callable.

    Yields:
        None

    Example:
        with st_redirect(sys.stdout, st.write):
            print("This will be redirected to Streamlit")
    """
    old_write = src.write
    with StringIO() as buffer:
        def new_write(b):
            if getattr(current_thread(), SCRIPT_RUN_CONTEXT_ATTR_NAME, None):
                buffer.write(b)
                dst(buffer.getvalue())
            else:
                old_write(b)
        try:
            src.write = new_write
            yield
        finally:
            src.write = old_write

@contextmanager
def st_stdout(dst):
    """
    Context manager to redirect stdout to Streamlit.

    Args:
        dst (callable): Destination callable.

    Yields:
        None

    Example:
        with st_stdout(st.write):
            print("This will be redirected to Streamlit")
    """
    with st_redirect(sys.stdout, dst):
        yield

def get_file_ext(x):
    """
    Returns the file extension of a given filename.

    Args:
        x (str): The filename.

    Returns:
        str: The file extension.

    Example:
        ext = get_file_ext("example.png")
        print(ext)  # Output: .png
    """
    assert isinstance(x, str)
    return os.path.splitext(x)[1].lower()

def parse_response(response):
    """
    Parses the response and displays it using Streamlit.

    Args:
        response: The response to parse and display.

    Returns:
        None

    Example:
        parse_response("Hello, World!")
    """
    if isinstance(response, int):
        st.markdown(response)
    elif isinstance(response, pd.DataFrame):
        st.table(response)
    elif isinstance(response, str):
        if get_file_ext(response) == ".png":
            st.image(response)
        else:
            st.markdown(response)
    else:
        raise NotImplementedError("Returned an output that we don't yet know how to handle")

def extract_source(rag_output: Dict[str, Any]) -> str:
    text = ""
    titles = []
    for i, context in enumerate(rag_output["docs"], start=1):
        titles.append(context['metadata']['Source'])
        text += (
            f"<b>Chunk {i}:</b>"
            f"<br>"
            f"<u>Document name</u>: {context['metadata']['Source']}"
            f"<br>"
            f"<u>Page</u>: {context['metadata']['Page']}"
            f"<br>"
            f"<u>Content</u>: <em>{context['text']}</em>"
            f"<br><br>"
        )
    return text, titles