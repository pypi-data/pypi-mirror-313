from .core.streamlit_app import OmniAIChatApp
import streamlit.web.server.server as server
import threading
import time


def claude_server():
    print("🚀 Starting OmniAI Chat App...")
    print("🔧 Initializing...")

    # Create an instance of the OmniAIChatApp
    app = OmniAIChatApp()

    # Define a function to run the Streamlit app
    def run_streamlit():
        server.start_server(
            "app",
            command_line=None,
            args=None,
            flag_options=None,
            config_options=None
        )

    # Start the Streamlit app in a separate thread
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()

    # Wait a moment to ensure the server is up
    time.sleep(2)

    print("🌐 Starting Streamlit server...")
    app.run()


if __name__ == '__main__':
    claude_server()