import subprocess

from .core.streamlit_app import OmniAIChatApp
import time


def claude_server():
    print("🚀 Starting OmniAI Chat App...")
    print("🔧 Initializing...")
    app = OmniAIChatApp()
    print("🌐 Starting Streamlit server...")
    app.run()


if __name__ == '__main__':
    claude_server()