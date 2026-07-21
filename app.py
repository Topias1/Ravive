import os
import sys

# Add Homebrew to PATH on macOS to ensure ffmpeg/ffprobe are found when run as an App bundle
if sys.platform == "darwin":
    for path in ("/opt/homebrew/bin", "/usr/local/bin"):
        if path not in os.environ.get("PATH", ""):
            os.environ["PATH"] = path + os.path.pathsep + os.environ.get("PATH", "")

try:
    sys.stdout.reconfigure(write_through=True, line_buffering=True)
    sys.stderr.reconfigure(write_through=True, line_buffering=True)
except Exception:
    pass

def main():
    import threading
    import time
    import webview
    from gui import main as start_server
    
    class Api:
        def __init__(self):
            self.window = None

        def select_file(self):
            if not self.window:
                return ""
            result = self.window.create_file_dialog(
                webview.OPEN_DIALOG,
                file_types=('Video files (*.mp4;*.mkv;*.mov;*.avi;*.webm)', 'All files (*.*)')
            )
            return result[0] if result else ""

        def select_folder(self):
            if not self.window:
                return ""
            result = self.window.create_file_dialog(webview.FOLDER_DIALOG)
            return result[0] if result else ""

    def on_closed():
        from gui import active_process
        if active_process:
            try:
                active_process.terminate()
            except Exception:
                pass
        sys.exit(0)

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait a bit for server to start
    time.sleep(0.8)
    
    # Instantiate the exposed Javascript API
    api = Api()
    
    # Create webview window
    port = int(os.environ.get("RAVIVE_GUI_PORT", "8080"))
    window = webview.create_window(
        title="Ravive",
        url=f"http://127.0.0.1:{port}",
        width=900,
        height=750,
        min_size=(800, 650),
        resizable=True,
        js_api=api
    )
    api.window = window
    
    # Register closing callback
    window.events.closed += on_closed
    
    # Start the webview loop
    webview.start()

if __name__ == "__main__":
    # In a frozen bundle sys.executable is this app, so anything asking Python
    # for a helper process re-launches it — multiprocessing does exactly that
    # ("<app> -c 'from multiprocessing.resource_tracker import main;main(5)'"),
    # and the CLI branch below then read that code string as a file to upscale.
    # freeze_support hands those re-launches back to multiprocessing before any
    # argument parsing sees them.
    import multiprocessing
    multiprocessing.freeze_support()

    # freeze_support only claims the "--multiprocessing-fork" form. The
    # resource tracker uses "-c <code>" instead, which slips past it, so act
    # as the interpreter it expects. Restricted to multiprocessing's own
    # bootstrap rather than running any -c payload handed to the app.
    if len(sys.argv) >= 3 and sys.argv[1] == "-c" and "multiprocessing" in sys.argv[2]:
        bootstrap = sys.argv[2]
        sys.argv = sys.argv[2:]
        exec(bootstrap, {"__name__": "__main__"})
        sys.exit(0)

    if os.environ.get("VIDEO_UPSCALER_CLI") == "1":
        # Run as the CLI upscaler helper
        import upscale
        sys.exit(upscale.main())
    else:
        # Run as the native GUI app
        main()
