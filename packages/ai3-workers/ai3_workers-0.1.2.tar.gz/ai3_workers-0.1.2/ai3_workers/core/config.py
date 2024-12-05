import streamlit as st
from typing import Optional
from .components import StreamlitWrapper
from .i18n import get_localized_string


def create_worker(title: Optional[str] = None, description: Optional[str] = None) -> StreamlitWrapper:
    """
    Initialize a worker with all necessary configuration.
    Must be called before any other Streamlit commands.
    """
    # Set page config first
    st.set_page_config(
        page_title=title or get_localized_string("title", "AI3 Worker"),
        page_icon="https://framerusercontent.com/images/VDN0LkS2v1ZuJwy6ZsCdHCNCw.png",
        layout="wide"
    )

    # Create StreamlitWrapper instance
    st_wrapper = StreamlitWrapper()

    with st.container(key="ai3-config"):
        # Apply standard CSS
        st_wrapper.markdown(
            '<link rel="stylesheet" href="https://workers.aiaiai.eu/assets/style.css" />',
            unsafe_allow_html=True
        )

        # Add scripts
        st_wrapper.components.v1.html("""
            <script>
                const hostWindow = window.parent;
                const hostElement = window.parent.document.documentElement;
                
                const postHeight = () => {
                    const hostElementHeight = hostElement.scrollHeight;
                    hostWindow.window.parent.postMessage({ type: 'setHeight', hostElementHeight }, '*');
                }

                const observer = new MutationObserver(postHeight);
                observer.observe(hostElement, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    characterData: true
                });

                window.addEventListener('load', postHeight);
                window.addEventListener('resize', postHeight);
                
                window.top.postMessage({
                    type: 'WORKER_RENDERED',
                    data: 'Worker has successfully rendered'
                }, '*');
            </script>
        """, width=0, height=0)

    # Add description if provided
    st_wrapper.markdown(description or get_localized_string(
        "description", "Description of the worker. You can edit this by adding a description to your i18n.json file."))

    return st_wrapper
