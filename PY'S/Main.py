import webview



height = 1080
width = 1920
wtitle = 'Sky Launcher'
Launcher_GUI = '../Assets/index.html'  # Change to your HTML file path

webview.create_window(title=wtitle, url=Launcher_GUI, width=width, height=height)
webview.start()
