import base64
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QPoint, QAbstractAnimation, QParallelAnimationGroup

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout
toggle_switch_ui = base64.b64encode(b"""from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QPoint, QAbstractAnimation, QParallelAnimationGroup

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout


class PyQtSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()
        self.__state = True

    def __initVal(self):
        self.__circle_diameter = 25
        self.__animationEnabledFlag = True
        self.__pointAnimation = ''
        self.__colorAnimation = ''
        # Define default background colors for toggled states
        self.__bgColorOn = 'rgb(200, 200, 250)'  # Light blue when toggled on
        self.__bgColorOff = 'rgb(255, 255, 255)'  # Light red when toggled off
    def isChecked(self):
        return self.__state
    def __initUi(self):
        self.__circle = QPushButton()
        self.__circle.setCheckable(True)
        self.__circle.setChecked(True)
        self.__circle.toggled.connect(self.__toggled)

        self.__layForBtnAlign = QHBoxLayout()
        self.__layForBtnAlign.setAlignment(Qt.AlignRight)
        self.__layForBtnAlign.addWidget(self.__circle)
        self.__layForBtnAlign.setContentsMargins(0, 0, 0, 0)

        innerWidgetForStyle = QWidget()
        innerWidgetForStyle.setLayout(self.__layForBtnAlign)

        lay = QGridLayout()
        lay.addWidget(innerWidgetForStyle)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

        self.__setStyle()
        self.__updateStyle(True)

    def __setStyle(self):
        self.__circle.setFixedSize(self.__circle_diameter, self.__circle_diameter)
        self.setStyleSheet(
            f'QWidget {{'
            f'  border: {self.__circle_diameter // 20}px solid #AAAAAA; '
            f'  border-radius: {self.__circle_diameter // 4}px; '
            f'  background-color: rgb(240, 240, 240);'  # Light grey background
            f'}}'
            f'QPushButton {{'
            f'  background-color: rgb(113, 95, 207);'  # Button color as previously defined
            f'}}')
        self.setFixedSize(self.__circle_diameter * 2, self.__circle_diameter)
    def __updateStyle(self, toggled):
        # Update the circle button and widget background color based on the toggle state
        bgColor = self.__bgColorOn if toggled else self.__bgColorOff
        self.setStyleSheet(
            f'QWidget {{'
            f'  border: {self.__circle_diameter // 20}px solid #AAAAAA; '
            f'  border-radius: {self.__circle_diameter // 2}px; '
            f'  background-color: {bgColor};'  # Dynamic background color
            f'}}'
            f'QPushButton {{'
            f'  background-color: rgb(113, 95, 207);'  # Toggle button color
            f'}}')
        self.setFixedSize(self.__circle_diameter * 2, self.__circle_diameter)

    def setAnimation(self, f: bool):
        self.__animationEnabledFlag = f
        if self.__animationEnabledFlag:
            self.__colorAnimation = QPropertyAnimation(self, b'point')
            self.__colorAnimation.valueChanged.connect(self.__circle.move)
            self.__colorAnimation.setDuration(100)
            self.__colorAnimation.setStartValue(QPoint(0, 0))
            self.__colorAnimation.setEndValue(QPoint(self.__circle_diameter, 0))

            self.__pointAnimation = QPropertyAnimation(self, b'color')
            self.__pointAnimation.valueChanged.connect(self.__setColor)
            self.__pointAnimation.setDuration(100)
            self.__pointAnimation.setStartValue(255)
            self.__pointAnimation.setEndValue(200)

            self.__animationGroup = QParallelAnimationGroup()
            self.__animationGroup.addAnimation(self.__colorAnimation)
            self.__animationGroup.addAnimation(self.__pointAnimation)

    def mousePressEvent(self, e):
        self.__circle.toggle()
        return super().mousePressEvent(e)

    def __toggled(self, f):
        self.__state = f
        if self.__animationEnabledFlag:
            if f:
                self.__animationGroup.setDirection(QAbstractAnimation.Forward)
                self.__animationGroup.start()
            else:
                self.__animationGroup.setDirection(QAbstractAnimation.Backward)
                self.__animationGroup.start()
        else:
            if f:
                self.__circle.move(self.__circle_diameter, 0)
                self.__layForBtnAlign.setAlignment(Qt.AlignRight)
            else:
                self.__circle.move(0, 0)
                self.__layForBtnAlign.setAlignment(Qt.AlignLeft)
        self.__updateStyle(f)  # Update the style based on the toggle state
        self.toggled.emit(f)

    def __setColor(self):
    # Set the color to RGB(113, 95, 207)
        self.__circle.setStyleSheet('QPushButton { background-color: rgb(113, 95, 207); }')

    def setCircleDiameter(self, diameter: int):
        self.__circle_diameter = diameter
        self.__setStyle()
        self.__colorAnimation.setEndValue(QPoint(self.__circle_diameter, 0))""")

run_toggle_switch_ui = exec(base64.b64decode(toggle_switch_ui))