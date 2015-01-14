# -*- coding: latin-1 -*-

from PyQt4 import QtCore, QtGui

import Code.QT.Iconos as Iconos
import Code.QT.Colocacion as Colocacion
import Code.QT.WBase as WBase
import Code.QT.WInformacion as WInformacion
import Code.QT.QTUtil as QTUtil
import Code.QT.QTVarios as QTVarios

class EstadoWindow:
    def __init__(self, x):
        self.noEstado = x == QtCore.Qt.WindowNoState
        self.minimizado = x == QtCore.Qt.WindowMinimized
        self.maximizado = x == QtCore.Qt.WindowMaximized
        self.fullscreen = x == QtCore.Qt.WindowFullScreen
        self.active = x == QtCore.Qt.WindowActive

class Pantalla(QTVarios.WDialogo):
    def __init__(self, gestor, owner=None):

        self.gestor = gestor

        titulo = ""
        icono = Iconos.Aplicacion64()
        extparam = "main"
        QTVarios.WDialogo.__init__(self, owner, titulo, icono, extparam)

        self.setBackgroundRole(QtGui.QPalette.Light)
        # self.setStyleSheet( "QToolButton { padding: 2px;}" )
        # self.setStyleSheet( "QWidget { background-color: yellow; }")

        # self.setMaximumWidth(QTUtil.anchoEscritorio()) # NO ya que elimina maximize

        self.base = WBase.WBase(self, gestor)

        self.capturas = self.base.capturas
        self.capturas.hide()
        self.siCapturas = False
        self.capturas.hide()
        self.informacionPGN = WInformacion.InformacionPGN(self)
        self.siInformacionPGN = False
        self.informacionPGN.hide()

        self.timer = None
        self.siTrabajando = False

        self.onTop = False

        self.tablero = self.base.tablero
        self.tablero.dispatchSize(self.ajustaTam)
        self.tablero.permitidoResizeExterno(True)
        self.anchoAntesMaxim = None

        self.splitter = splitter = QtGui.QSplitter(self)
        splitter.addWidget(self.base)
        splitter.addWidget(self.informacionPGN)

        ly = Colocacion.H().control(splitter).margen(0)

        self.setLayout(ly)

        ctrl1 = QtGui.QShortcut(self)
        ctrl1.setKey("Ctrl+1")
        self.connect(ctrl1, QtCore.SIGNAL("activated()"), self.pulsadoShortcutCtrl1)

        ctrlF10 = QtGui.QShortcut(self)
        ctrlF10.setKey("Ctrl+0")
        self.connect(ctrlF10, QtCore.SIGNAL("activated()"), self.pulsadoShortcutCtrl0)

        F11 = QtGui.QShortcut(self)
        F11.setKey("F11")
        self.connect(F11, QtCore.SIGNAL("activated()"), self.pulsadoShortcutF11)
        self.activadoF11 = False

        if QtGui.QSystemTrayIcon.isSystemTrayAvailable():
            F12 = QtGui.QShortcut(self)
            F12.setKey("F12")
            self.connect(F12, QtCore.SIGNAL("activated()"), self.pulsadoShortcutF12)

            restoreAction = QtGui.QAction(Iconos.PGN(), _("Show"), self, triggered=self.restauraTrayIcon)
            quitAction = QtGui.QAction(Iconos.Terminar(), _("Quit"), self, triggered=self.quitTrayIcon)
            trayIconMenu = QtGui.QMenu(self)
            trayIconMenu.addAction(restoreAction)
            trayIconMenu.addSeparator()
            trayIconMenu.addAction(quitAction)

            self.trayIcon = QtGui.QSystemTrayIcon(self)
            self.trayIcon.setContextMenu(trayIconMenu)
            self.trayIcon.setIcon(Iconos.Otros())  # Aplicacion())
            self.connect(self.trayIcon, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),
                         self.activateTrayIcon)
        else:
            self.trayIcon = None

        self.resizing = None

        self.cursorPensando = QtGui.QCursor(QtCore.Qt.BusyCursor)  # BusyCursor )#Iconos.pmTime())

    def onTopWindow(self):
        self.onTop = not self.onTop
        self.muestra()

    def activateTrayIcon(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.restauraTrayIcon()

    def restauraTrayIcon(self):
        self.showNormal()
        self.trayIcon.hide()

    def quitTrayIcon(self):
        self.trayIcon.hide()
        self.accept()
        self.gestor.pararMotores()

    def pulsadoShortcutF12(self):
        if self.trayIcon:
            self.trayIcon.show()
            self.hide()

    def pulsadoShortcutF11(self):
        self.activadoF11 = not self.activadoF11
        if self.activadoF11:
            self.showFullScreen()
        else:
            self.showNormal()

    def closeEvent(self, event):  # Cierre con X
        self.guardarVideo()
        if not self.gestor.finalX0():
            event.ignore()

    def ponGestor(self, gestor):
        self.gestor = gestor
        self.base.ponGestor(gestor)

    def muestra(self):
        flags = QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint
        if self.onTop:
            flags |= QtCore.Qt.WindowStaysOnTopHint

        self.setWindowFlags(flags)
        if self.tablero.siMaximizado():
            self.showMaximized()
        else:
            self.recuperarVideo(siTam=False)
            self.ajustaTam()
            self.show()

        self.ponTitulo()

    def changeEvent(self, event):
        QtGui.QWidget.changeEvent(self, event)
        if event.type() != QtCore.QEvent.WindowStateChange:
            return

        nue = EstadoWindow(self.windowState())
        ant = EstadoWindow(event.oldState())

        ct = self.tablero.confTablero

        if getattr(self.gestor, "siPresentacion", False):
            self.gestor.presentacion(False)

        if nue.fullscreen:
            self.base.tb.hide()
            self.tablero.siF11 = True
            self.antiguoAnchoPieza = 1000 if ant.maximizado else ct.anchoPieza()
            self.tablero.maximizaTam(True)
        else:
            if ant.fullscreen:
                self.base.tb.show()
                self.tablero.normalTam(self.antiguoAnchoPieza)
                self.ajustaTam()
                if self.antiguoAnchoPieza == 1000:
                    self.setWindowState(QtCore.Qt.WindowMaximized)
            elif nue.maximizado:
                self.antiguoAnchoPieza = ct.anchoPieza()
                self.tablero.maximizaTam(False)
            elif ant.maximizado:
                if not self.antiguoAnchoPieza or self.antiguoAnchoPieza == 1000:
                    self.antiguoAnchoPieza = self.tablero.calculaAnchoMXpieza()
                self.tablero.normalTam(self.antiguoAnchoPieza)
                self.ajustaTam()
                # ct.anchoPieza(self.antiguoAnchoPieza)
                # ct.guardaEnDisco()
                # self.tablero.ponAncho()
                # self.ajustaTam()

    def muestraVariantes(self, titulo):
        flags = QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint

        self.setWindowFlags(flags)

        self.setWindowTitle(titulo)

        self.exec_()

    def ajustaTam(self):
        if self.isMaximized():
            if not self.tablero.siMaximizado():
                self.tablero.maximizaTam(self.activadoF11)
        else:
            n = 0
            while self.height() > self.tablero.ancho + 80:
                self.adjustSize()
                self.refresh()
                n += 1
                if n > 3:
                    break
        if hasattr(self, "capturas"):
            self.capturas.resetPZ(self.tablero)
        self.refresh()

    def ajustaTamH(self):
        if not self.isMaximized():
            for n in range(3):
                self.adjustSize()
                self.refresh()
        self.refresh()

    def ponTitulo(self):
        titulo = _("Lucas Chess")
        conf = self.gestor.configuracion

        titulo += " - %s" % conf.jugador

        self.setWindowTitle(titulo)

    def ponRotulo1(self, rotulo):
        return self.base.ponRotulo1(rotulo)

    def ponRotulo2(self, rotulo):
        return self.base.ponRotulo2(rotulo)

    def ponRotulo3(self, rotulo):
        return self.base.ponRotulo3(rotulo)

    def alturaRotulo3(self, px):
        return self.base.alturaRotulo3(px)

    def ponRevision(self, siponer):
        return
        if siponer:
            self.base.lbRevision.show()
        else:
            self.base.lbRevision.hide()

    def ponActivarTutor(self, siActivar):
        self.base.ponActivarTutor(siActivar)

    def ponToolBar(self, liAcciones, separator=True):
        self.base.ponToolBar(liAcciones, separator)

    def dameToolBar(self):
        return self.base.dameToolBar()

    def ponAyudas(self, puntos, siAtras=True):
        self.base.ponAyudas(puntos, siAtras)

    def quitaAyudas(self, siTambienTutorAtras, siAtras=True):
        self.base.quitaAyudas(siTambienTutorAtras, siAtras)

    def habilitaToolbar(self, opcion, siHabilitar):
        self.base.habilitaToolbar(opcion, siHabilitar)

    def mostrarOpcionToolbar(self, opcion, siMostrar):
        self.base.mostrarOpcionToolbar(opcion, siMostrar)

    def pgnRefresh(self, siBlancas):
        self.base.pgnRefresh()
        self.base.pgn.gobottom(2 if siBlancas else 1)

    def pgnColocate(self, fil, siBlancas):
        col = 1 if siBlancas else 2
        self.base.pgn.goto(fil, col)

    def pgnPosActual(self):
        return self.base.pgn.posActual()

    def refresh(self):
        self.update()
        QTUtil.xrefreshGUI()

    def activaCapturas(self, siActivar=None):
        if siActivar is None:
            self.siCapturas = not self.siCapturas
        else:
            self.siCapturas = siActivar
        self.capturas.setVisible(self.siCapturas)
        if self.siCapturas:
            self.capturas.ponLayout(self.tablero.siBlancasAbajo)
        else:
            self.splitter.setHandleWidth(1)

        self.ajustaTamH()

    def activaInformacionPGN(self, siActivar=None):
        if siActivar is None:
            self.siInformacionPGN = not self.siInformacionPGN
        else:
            self.siInformacionPGN = siActivar
        self.informacionPGN.setVisible(self.siInformacionPGN)
        self.ajustaTamH()

    def quitaChat(self):
        self.chat.hide()
        self.ajustaTamH()

    def ponCapturas(self, dic, jg, apertura):
        self.capturas.pon(dic, jg, apertura)

    def ponInformacionPGN(self, partida, jg, apertura):
        self.informacionPGN.ponJG(partida, jg, apertura)

    def activaJuego(self, siActivar=True, siReloj=False, siAyudas=None):
        self.base.activaJuego(siActivar, siReloj, siAyudas)
        self.ajustaTamH()

    def ponDatosReloj(self, bl, rb, ng, rn):
        self.base.ponDatosReloj(bl, rb, ng, rn)

    def ponRelojBlancas(self, tm, tm2):
        self.base.ponRelojBlancas(tm, tm2)

    def ponRelojNegras(self, tm, tm2):
        self.base.ponRelojNegras(tm, tm2)

    def cambiaRotulosReloj(self, bl, ng):
        self.base.cambiaRotulosReloj(bl, ng)

    def iniciaReloj(self, enlace, transicion=100):
        if self.timer is not None:
            self.timer.stop()
            del self.timer

        self.timer = QtCore.QTimer(self)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), enlace)
        self.timer.start(transicion)

    def paraReloj(self):
        if self.timer is not None:
            self.timer.stop()
            del self.timer
            self.timer = None

    def columnas60(self, siPoner, cNivel=None):
        if cNivel is None:
            cNivel = _("Level")
        self.base.columnas60(siPoner, cNivel)

    def pulsadoShortcutCtrl1(self):
        if self.gestor and hasattr(self.gestor, "control1"):
            self.gestor.control1()

    def pulsadoShortcutCtrl0(self):
        if self.gestor and hasattr(self.gestor, "control0"):
            self.gestor.control0()

    def soloEdicionPGN(self, fichero):
        if fichero:
            titulo = fichero
        else:
            titulo = "<<< %s >>>" % _("Temporary file")

        self.setWindowTitle(titulo)
        self.setWindowIcon(Iconos.PGN())

    def cursorFueraTablero(self):
        p = self.mapToParent(self.tablero.pos())
        p.setX(p.x() + self.tablero.ancho + 4)

        QtGui.QCursor.setPos(p)

    def pensando(self, siPensando):
        if siPensando:
            QtGui.QApplication.setOverrideCursor(self.cursorPensando)
        else:
            QtGui.QApplication.restoreOverrideCursor()
        self.refresh()

