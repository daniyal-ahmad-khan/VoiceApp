import base64
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFileSystemWatcher
# from PySide6.QtCore import Slot
from ui import MainWindow
import qdarktheme
import pyqtgraph as pg
from PyQt5.QtGui import QFont
code  = base64.b64encode(b"""import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFileSystemWatcher
# from PySide6.QtCore import Slot
from ui import MainWindow
import qdarktheme
import pyqtgraph as pg
from PyQt5.QtGui import QFont

class Reloader(QFileSystemWatcher):
    def __init__(self, application):
        super(Reloader, self).__init__()
        self.application = application

    def on_file_changed(self, path):
        print(f"Change detected in file: {path}")
        self.application.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)

def main():
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    # app.setFont("Arial", 10)
    global_font = QFont("Arial")
    app.setFont(global_font)
    qdarktheme.setup_theme(theme="dark", additional_qss="QWidget {border-radius: 10px;}")
    reloader = Reloader(app)
    # plot_widget = pg.PlotWidget()

    # Add the files you want to watch for changes
    # Typically, you'd watch the main script and other frequently changed files
    reloader.addPath('ui.py')
    reloader.addPath('sidebar.py')
    reloader.addPath('apisidebar.py')
    reloader.addPath('voice_generator.py')
    reloader.addPath('styles.py')
    reloader.addPath('app.py')
    reloader.addPath('toggle_switch.py')
    # ... add other paths as needed ...

    reloader.fileChanged.connect(reloader.on_file_changed)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()""")

exec(base64.b64decode(code))