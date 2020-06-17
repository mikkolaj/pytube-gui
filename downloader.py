from PyQt5 import QtWidgets as Widgets
from PyQt5 import QtCore as Core
from PyQt5 import QtGui as Gui
from pytube import YouTube
from pytube import exceptions
import sys
import os
from time import sleep


class MainWindow(Widgets.QMainWindow):
    url1 = None
    url2 = None
    dwnaudio = False
    dwnvideo = False

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Pobierajka")

        mainlay = Widgets.QVBoxLayout()
        stcklay = Widgets.QStackedLayout()
        instcklay1 = Widgets.QVBoxLayout()
        instcklay2 = Widgets.QVBoxLayout()

        btnlay = Widgets.QHBoxLayout()

        btn1 = Widgets.QPushButton("Pobierz osobno")
        btn1.pressed.connect(lambda: stcklay.setCurrentIndex(0))

        btn2 = Widgets.QPushButton("Pobierz razem")
        btn2.pressed.connect(lambda: stcklay.setCurrentIndex(1))

        btn3 = Widgets.QPushButton("?")
        btn3.setFixedWidth(24)
        btn3.setToolTip("YouTube wspiera strumieniowanie wideo razem\nz dżwiękiem wyłącznie do rozdzielczości 720p.\n"
                        "Aby uzyskać lepszą jakość należy pobrać audio\ni wideo oddzielnie, a następnie scalić je w\n"
                        "odpowiednim programie (np. FFmpeg).")
        btn3.setDisabled(True)
        btnlay.addWidget(btn1)
        btnlay.addWidget(btn2)
        btnlay.addWidget(btn3)
        btnlay.setContentsMargins(0, 0, 0, 0)
        btnlay.setSpacing(0)

        label1 = Widgets.QLabel("Podaj URL:")
        fillin = Widgets.QLineEdit()
        fillin.setPlaceholderText("URL:")
        fillin.textChanged.connect(self.zmianaurl)

#       Część do audio
        audiolay = Widgets.QHBoxLayout()
        label3 = Widgets.QLabel("Audio:")
        checkaud = Widgets.QCheckBox()
        checkaud.stateChanged.connect(self.changeaudio)
        audiolay.setContentsMargins(0, 0, 0, 0)
        audiolay.setSpacing(0)
        audiolay.addWidget(label3)
        audiolay.addWidget(checkaud)

#       Część do wideo
        videolay = Widgets.QHBoxLayout()
        label4 = Widgets.QLabel("Wideo:")
        checkvid = Widgets.QCheckBox()
        checkvid.stateChanged.connect(self.changevideo)
        videolay.setContentsMargins(0, 0, 0, 0)
        videolay.setSpacing(0)
        videolay.addWidget(label4)
        videolay.addWidget(checkvid)
        self.lista = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
        self.videolay2 = self.QualSelLay("  - Wybierz docelową rozdzielczość: ", self.lista)
        self.pathwid = self.PathWid()

        self.dwnbtn = Widgets.QPushButton("Pobierz!")

        mainlay.addLayout(btnlay)

        instcklay1.addWidget(label1)
        instcklay1.addWidget(fillin)
        instcklay1.addLayout(audiolay)
        instcklay1.addLayout(videolay)
        instcklay1.addLayout(self.videolay2.videolay)
        instcklay1.addLayout(self.pathwid.filelay)
        instcklay1.addWidget(self.pathwid.pathwid)
        instcklay1.addWidget(self.dwnbtn)
        instcklay1.setContentsMargins(0, 0, 0, 0)
        instcklay1.setSpacing(-1)

#       layout2
        label5 = Widgets.QLabel("Podaj URL:")
        fillin2 = Widgets.QLineEdit()
        fillin2.setPlaceholderText("URL:")
        fillin2.textChanged.connect(self.zmianaurl2)
        self.videolay3 = self.QualSelLay("Wybierz docelową rozdzielczość: ", self.lista[3:])
        self.pathwid2 = self.PathWid()
        self.dwnbtn2 = Widgets.QPushButton("Pobierz!")

        instcklay2.addWidget(label5)
        instcklay2.addWidget(fillin2)
        instcklay2.addLayout(self.videolay3.videolay)
        instcklay2.addLayout(self.pathwid2.filelay)
        instcklay2.addWidget(self.pathwid2.pathwid)
        instcklay2.addWidget(self.dwnbtn2)
        instcklay2.setContentsMargins(0, 0, 0, 0)
        instcklay2.setSpacing(-1)
        instcklay2.setAlignment(Core.Qt.AlignCenter)

        instck1 = Widgets.QWidget()
        instck1.setLayout(instcklay1)

        instck2 = Widgets.QWidget()
        instck2.setLayout(instcklay2)

        stcklay.addWidget(instck1)
        stcklay.addWidget(instck2)

        mainlay.addLayout(stcklay)

        widget = Widgets.QWidget()
        widget.setLayout(mainlay)
        self.setCentralWidget(widget)

    def zmianaurl(self, s):
        self.url1 = s

    def zmianaurl2(self, s):
        self.url2 = s

    def changevideo(self, s):
        if s == 2:
            self.dwnvideo = True
        else:
            self.dwnvideo = False

    def changeaudio(self, s):
        if s == 2:
            self.dwnaudio = True
        else:
            self.dwnaudio = False

    class QualSelLay:
        resolution = None
        videolay = None

        def __init__(self, message, cmblist):
            self.resolution = cmblist[0]
            self.videolay = Widgets.QHBoxLayout()
            self.label = Widgets.QLabel(message)
            self.cmbvid = Widgets.QComboBox()
            self.cmbvid.addItems(cmblist)
            self.cmbvid.currentIndexChanged[str].connect(self.reschange)
            self.videolay.setContentsMargins(0, 0, 0, 0)
            self.videolay.setSpacing(10)
            self.videolay.addWidget(self.label)
            self.videolay.addWidget(self.cmbvid)

        def reschange(self, s):
            self.resolution = s

    class PathWid:
        path = None
        pathwid = None
        filelay = None

        def __init__(self):
            self.filelay = Widgets.QHBoxLayout()
            label2 = Widgets.QLabel("Wybierz miejsce zapisu:")
            pthbtn = Widgets.QPushButton("Przeglądaj")
            pthbtn.clicked.connect(self.sciezka)
            self.filelay.addWidget(label2)
            self.filelay.addWidget(pthbtn)
            self.filelay.setContentsMargins(0, 0, 0, 0)
            self.filelay.setSpacing(10)
            self.pathwid = Widgets.QLineEdit()
            self.pathwid.setPlaceholderText("Ścieżka:")
            self.pathwid.textChanged.connect(self.sciezka2)

        def sciezka(self):
            self.path = str(Widgets.QFileDialog.getExistingDirectory(caption="Wybierz folder do zapisu"))
            self.pathwid.setText(self.path)

        def sciezka2(self, s):
            self.path = s

    def wrongpathdial(self):
        dialog = CustomDialog(self, Core.Qt.WindowCloseButtonHint)
        dialog.setWindowIcon(Gui.QIcon('warning2'))
        dialog.ustawnapis("Podaj poprawną ścieżkę!")
        dialog.exec_()

    def wrongurlialog(self):
        dialog = CustomDialog(self, Core.Qt.WindowCloseButtonHint)
        dialog.setWindowIcon(Gui.QIcon('warning2'))
        dialog.ustawnapis("Podaj poprawny URL!")
        dialog.exec_()

    def notavaldialog(self):
        dialog = CustomDialog(self, Core.Qt.WindowCloseButtonHint)
        dialog.setWindowIcon(Gui.QIcon('warning2'))
        dialog.ustawnapis("Wideo nie jest dostępne!")
        dialog.exec_()

    def livedialog(self):
        dialog = CustomDialog(self, Core.Qt.WindowCloseButtonHint)
        dialog.setWindowIcon(Gui.QIcon('warning2'))
        dialog.ustawnapis("Nie można pobierać transmisji na żywo!")
        dialog.exec_()


class CustomDialog(Widgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Uwaga!")

        self.label = Widgets.QLabel()
        self.label.setAlignment(Core.Qt.AlignCenter)

        self.la = Widgets.QHBoxLayout()
        self.button = Widgets.QPushButton("Ok")
        self.button.clicked.connect(self.close)
        self.button.setFixedWidth(60)
        self.la.addWidget(self.button)

        self.layout = Widgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.la)
        self.layout.setAlignment(Core.Qt.AlignCenter)
        self.setLayout(self.layout)

    def ustawnapis(self, napis):
        self.label.setText(napis)


class SeparateDownloadWorker(Core.QObject):
    finished = Core.pyqtSignal()
    inprogress = Core.pyqtSignal()
    updated = Core.pyqtSignal()
    wrongpath = Core.pyqtSignal()
    wrongurl = Core.pyqtSignal()
    notaval = Core.pyqtSignal()
    live = Core.pyqtSignal()

    def __init__(self, path, url, dwnvideo, dwnaudio, frmat, resolution):
        super(SeparateDownloadWorker, self).__init__()
        self.path = path
        self.url = url
        self.dwnvideo = dwnvideo
        self.dwnaudio = dwnaudio
        self.format = frmat
        self.resolution = resolution

    def update(self, path, url, dwnvideo, dwnaudio, frmat, resolution):
        self.path = path
        self.url = url
        self.dwnvideo = dwnvideo
        self.dwnaudio = dwnaudio
        self.format = frmat
        self.resolution = resolution
        self.updated.emit()

    def pobieranie(self):
        if self.path is not None and self.url is not None:
            if not os.path.exists(self.path):
                self.wrongpath.emit()
                return

            if self.dwnvideo or self.dwnaudio:
                try:
                    yt = YouTube(self.url)
                except exceptions.RegexMatchError:
                    self.wrongurl.emit()
                    return
                except exceptions.VideoUnavailable:
                    self.notaval.emit()
                    return
                except exceptions.LiveStreamError:
                    self.live.emit()
                    return
                self.inprogress.emit()

            else:
                return
            strms = yt.streams

            if self.dwnvideo:
                if strms.filter(resolution=self.resolution, subtype="mp4", progressive=False). \
                        order_by("fps").desc().first() is None:

                    if strms.filter(resolution=self.resolution, progressive=False). \
                            order_by("fps").desc().first() is not None:

                        self.format = strms.filter(resolution=self.resolution, progressive=False). \
                            order_by("fps").desc().first().subtype

                        strms.filter(resolution=self.resolution, progressive=False).order_by("fps").desc(). \
                            first().download(self.path, filename_prefix="video_")

                    else:

                        self.format = strms.filter(subtype="mp4", progressive=False).order_by("resolution").desc(). \
                            first().subtype

                        strms.filter(subtype="mp4", progressive=False).order_by("resolution").desc(). \
                            first().download(self.path, filename_prefix="video_")
                else:

                    strms.filter(resolution=self.resolution, subtype="mp4", progressive=False). \
                        order_by("fps").desc().first().download(self.path, filename_prefix="video_")

            if self.dwnaudio:
                prefix = "audio_"
                if not self.dwnvideo:
                    prefix = ""
                strms.filter(only_audio=True, subtype=self.format).order_by("abr").desc().first(). \
                    download(self.path, filename_prefix=prefix)

            self.finished.emit()


class ConnectedDownloadWorker(Core.QObject):
    finished = Core.pyqtSignal()
    inprogress = Core.pyqtSignal()
    updated = Core.pyqtSignal()
    wrongpath = Core.pyqtSignal()
    wrongurl = Core.pyqtSignal()
    notaval = Core.pyqtSignal()
    live = Core.pyqtSignal()

    def __init__(self, path, url, resolution):
        super(ConnectedDownloadWorker, self).__init__()
        self.path = path
        self.url = url
        self.resolution = resolution

    def update(self, path, url, resolution):
        self.path = path
        self.url = url
        self.resolution = resolution
        self.updated.emit()

    def pobieranie(self):
        if self.path is not None and self.url is not None:
            if not os.path.exists(self.path):
                self.wrongpath.emit()
                return

            try:
                yt = YouTube(self.url)
            except exceptions.RegexMatchError:
                self.wrongurl.emit()
                return
            except exceptions.VideoUnavailable:
                self.notaval.emit()
                return
            except exceptions.LiveStreamError:
                self.live.emit()
                return
            self.inprogress.emit()

            strms = yt.streams
            if strms.filter(resolution=self.resolution, progressive=True).first() is not None:
                strms.filter(resolution=self.resolution, progressive=True).first(). \
                    download(self.path)
            else:
                strms.filter(progressive=True).order_by("resolution").desc().first().download(self.path)
        self.finished.emit()


class AppWrap(Core.QObject):

    def __init__(self, parent=None):
        super(AppWrap, self).__init__(parent)
        self.window = MainWindow()
        self._connectsignals()

        self.window.setFixedHeight(self.window.sizeHint().height())
        self.window.setMaximumWidth(600)
        self.window.setWindowIcon(Gui.QIcon('icon'))

        self.window.show()

        self.CDThread = None
        self.SDThread = None
        self.CDLoop = False
        self.SDLoop = False

    def _connectsignals(self):
        self.window.dwnbtn.clicked.connect(self.createSDWorker)
        self.window.dwnbtn2.clicked.connect(self.createCDWorker)
        self.parent().aboutToQuit.connect(self.forceQuitWorker)

    def createSDWorker(self):
        self.SDWorker = SeparateDownloadWorker(self.window.pathwid.path, self.window.url1, self.window.dwnvideo,
                                               self.window.dwnaudio, "mp4", self.window.videolay2.resolution)
        self.SDThread = Core.QThread()
        self.SDWorker.moveToThread(self.SDThread)
        self.SDThread.started.connect(self.SDWorker.pobieranie)

        self.window.dwnbtn.clicked.disconnect(self.createSDWorker)
        self.window.dwnbtn.clicked.connect(self.reuseSDWorker)

        self.SDWorker.inprogress.connect(self.loopingSD)
        self.SDWorker.finished.connect(self.breakSDloop)
        self.SDWorker.updated.connect(self.SDWorker.pobieranie)

        self.SDWorker.wrongpath.connect(self.window.wrongpathdial)
        self.SDWorker.wrongurl.connect(self.window.wrongurlialog)
        self.SDWorker.notaval.connect(self.window.notavaldialog)
        self.SDWorker.live.connect(self.window.livedialog)

        self.SDThread.start()

    def createCDWorker(self):
        self.CDWorker = ConnectedDownloadWorker(self.window.pathwid2.path, self.window.url2,
                                                self.window.videolay3.resolution)
        self.CDThread = Core.QThread()
        self.CDWorker.moveToThread(self.CDThread)
        self.CDThread.started.connect(self.CDWorker.pobieranie)

        self.window.dwnbtn2.clicked.disconnect(self.createCDWorker)
        self.window.dwnbtn2.clicked.connect(self.reuseCDWorker)

        self.CDWorker.inprogress.connect(self.loopingCD)
        self.CDWorker.finished.connect(self.breakCDloop)
        self.CDWorker.updated.connect(self.CDWorker.pobieranie)

        self.CDWorker.wrongpath.connect(self.window.wrongpathdial)
        self.CDWorker.wrongurl.connect(self.window.wrongurlialog)
        self.CDWorker.notaval.connect(self.window.notavaldialog)
        self.CDWorker.live.connect(self.window.livedialog)

        self.CDThread.start()

    def reuseSDWorker(self):
        self.SDWorker.update(self.window.pathwid.path, self.window.url1, self.window.dwnvideo,
                             self.window.dwnaudio, "mp4", self.window.videolay2.resolution)

    def reuseCDWorker(self):
        self.CDWorker.update(self.window.pathwid2.path, self.window.url2,
                             self.window.videolay3.resolution)

    def loopingCD(self):
        self.CDLoop = True
        self.window.dwnbtn2.setDisabled(True)
        Widgets.QApplication.processEvents()
        while self.CDLoop:
            self.window.dwnbtn2.setText("Pobieranie.")
            for i in range(100):
                sleep(0.002)
                Widgets.QApplication.processEvents()
            if not self.CDLoop:
                break
            self.window.dwnbtn2.setText("Pobieranie..")
            for i in range(100):
                sleep(0.002)
                Widgets.QApplication.processEvents()
            if not self.CDLoop:
                break
            self.window.dwnbtn2.setText("Pobieranie...")
            for i in range(100):
                sleep(0.002)
                Widgets.QApplication.processEvents()
        self.window.dwnbtn2.setEnabled(True)
        self.window.dwnbtn2.setText("Pobierz!")

    def breakCDloop(self):
        self.CDLoop = False

    def loopingSD(self):
        self.SDLoop = True
        self.window.dwnbtn.setDisabled(True)
        Widgets.QApplication.processEvents()
        while self.SDLoop:
            self.window.dwnbtn.setText("Pobieranie.")
            for i in range(100):
                sleep(0.002)
                Widgets.QApplication.processEvents()
            if not self.SDLoop:
                break
            self.window.dwnbtn.setText("Pobieranie..")
            for i in range(100):
                sleep(0.002)
                Widgets.QApplication.processEvents()
            if not self.SDLoop:
                break
            self.window.dwnbtn.setText("Pobieranie...")
            for i in range(100):
                sleep(0.002)
                Widgets.QApplication.processEvents()
        self.window.dwnbtn.setEnabled(True)
        self.window.dwnbtn.setText("Pobierz!")

    def breakSDloop(self):
        self.SDLoop = False

    def forceQuitWorker(self):
        if self.SDThread is not None and self.SDThread.isRunning():
            self.SDThread.terminate()
            self.SDThread.wait()
        if self.CDThread is not None and self.CDThread.isRunning():
            self.CDThread.terminate()
            self.CDThread.wait()


app = Widgets.QApplication([])
wrapped = AppWrap(app)
sys.exit(app.exec_())

