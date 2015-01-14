# -*- coding: latin-1 -*-

from Code.Constantes import *

import Code.VarGen as VarGen

import Code.Jugada as Jugada
import Code.Tutor as Tutor
import Code.XMotorRespuesta as XMotorRespuesta

import Code.Apertura as Apertura

import Code.Gestor as Gestor

import Code.QT.QTUtil2 as QTUtil2

class GestorNueva(Gestor.Gestor):
    def inicio(self, categoria, nivel, siBlancas, puntos, aplazamiento=None):

        self.tipoJuego = kJugNueva

        self.liReiniciar = categoria, nivel, siBlancas

        self.resultado = None
        self.siJuegaHumano = False
        self.estado = kJugando

        self.siJuegaPorMi = True

        self.siJugamosConBlancas = siBlancas
        self.siRivalConBlancas = not siBlancas

        self.rmRival = None

        self.categoria = categoria
        self.nivelJugado = nivel
        self.puntos = puntos

        self.siTutorActivado = (VarGen.dgtDispatch is None) and self.configuracion.tutorActivoPorDefecto
        self.pantalla.ponActivarTutor(self.siTutorActivado)

        self.ayudas = categoria.ayudas
        self.ayudasPGN = self.ayudas  # Se guarda para guardar el PGN

        self.siApertura = True
        self.apertura = Apertura.AperturaPol(nivel)  # lee las aperturas

        self.xrival = self.procesador.creaGestorMotor(self.configuracion.rival, None, nivel)

        # -Aplazamiento 1/2--------------------------------------------------
        if aplazamiento:
            self.partida.recuperaDeTexto(aplazamiento["JUGADAS"])

            self.siApertura = aplazamiento["SIAPERTURA"]
            self.partida.pendienteApertura = aplazamiento["PENDIENTEAPERTURA"]
            self.partida.apertura = None if aplazamiento["APERTURA"] is None else self.listaAperturasStd.dic[
                aplazamiento["APERTURA"]]
            self.apertura.recuperaEstado(aplazamiento["ESTADOAPERTURA"])

            self.siTutorActivado = aplazamiento["SITUTOR"]
            self.pantalla.ponActivarTutor(self.siTutorActivado)
            self.ayudas = aplazamiento["AYUDAS"]

        self.pantalla.ponToolBar(
            ( k_cancelar, k_rendirse, k_atras, k_reiniciar, k_aplazar, k_configurar, k_utilidades  ))
        self.pantalla.activaJuego(True, False)
        self.ponMensajero(self.mueveHumano)
        self.ponPosicion(self.partida.ultPosicion)
        self.ponPiezasAbajo(siBlancas)
        self.ponAyudas(self.ayudas)
        self.mostrarIndicador(True)
        rotulo = "%s: <b>%s</b><br>%s %s %d" % (
            _("Opponent"), self.xrival.nombre, categoria.nombre(), _("Level"), nivel )
        if self.puntos:
            rotulo += " (+%d %s)" % ( self.puntos, _("points") )
        self.ponRotulo1(rotulo)
        self.xrotulo2()

        self.pgnRefresh(True)
        self.ponCapInfoPorDefecto()

        #-Aplazamiento 2/2--------------------------------------------------
        if aplazamiento:
            self.mueveJugada(kMoverFinal)

        self.siAnalizadoTutor = False

        self.ponPosicionDGT()

        self.siguienteJugada()

    def xrotulo2(self):
        self.ponRotulo2("%s: <b>%s</b><br>%s: %d %s" % (
            _("Tutor"), self.xtutor.nombre, _("Total score"), self.configuracion.puntuacion(), _("pts")))

    def procesarAccion(self, clave):

        if clave == k_cancelar:
            self.finalizar()

        elif clave == k_rendirse:
            self.rendirse()

        elif clave == k_atras:
            self.atras()

        elif clave == k_reiniciar:
            self.reiniciar()

        elif clave == k_configurar:
            self.configurar(siSonidos=True, siCambioTutor=True)

        elif clave == k_utilidades:
            self.utilidades(siArbol=False)

        elif clave == k_aplazar:
            self.aplazar()

        else:
            self.rutinaAccionDef(clave)

    def reiniciar(self):
        if self.partida.numJugadas() and QTUtil2.pregunta(self.pantalla, _("Restart the game?")):
            self.partida.reset()
            categoria, nivel, siBlancas = self.liReiniciar
            self.inicio(categoria, nivel, siBlancas, self.puntos)

    def aplazar(self):
        if self.partida.numJugadas() and QTUtil2.pregunta(self.pantalla, _("Do you want to adjourn the game?")):
            aplazamiento = {}
            aplazamiento["TIPOJUEGO"] = self.tipoJuego
            aplazamiento["SIBLANCAS"] = self.siJugamosConBlancas
            aplazamiento["JUGADAS"] = self.partida.guardaEnTexto()
            aplazamiento["SITUTOR"] = self.siTutorActivado
            aplazamiento["AYUDAS"] = self.ayudas

            aplazamiento["SIAPERTURA"] = self.siApertura
            aplazamiento["PENDIENTEAPERTURA"] = self.partida.pendienteApertura
            aplazamiento["APERTURA"] = self.partida.apertura.a1h8 if self.partida.apertura else None
            aplazamiento["ESTADOAPERTURA"] = self.apertura.marcaEstado()

            aplazamiento["CATEGORIA"] = self.categoria.clave
            aplazamiento["NIVEL"] = self.nivelJugado
            aplazamiento["PUNTOS"] = self.puntos

            self.configuracion.graba(aplazamiento)
            self.pantalla.accept()

    def finalX(self):
        return self.finalizar()

    def finalizar(self):
        if self.estado == kFinJuego:
            self.ponFinJuego()
            return True
        siJugadas = self.partida.numJugadas() > 0
        if siJugadas:
            if not QTUtil2.pregunta(self.pantalla, _("End game?")):
                return False  # no termina
            self.resultado = kDesconocido
            self.partida.liJugadas[-1].siDesconocido = True
            self.guardarNoTerminados()
            self.ponFinJuego()
        else:
            self.procesador.inicio()

        return False

    def rendirse(self):
        if self.estado == kFinJuego:
            return True
        siJugadas = self.partida.numJugadas() > 0
        if siJugadas:
            if not QTUtil2.pregunta(self.pantalla, _("Do you want to resign?")):
                return False  # no abandona
            self.resultado = kGanaRival
            self.partida.abandona(self.siJugamosConBlancas)
            self.guardarGanados(False)
            self.ponFinJuego()
        else:
            self.procesador.inicio()

        return False

    def atras(self):
        if self.ayudas and self.partida.numJugadas():
            if QTUtil2.pregunta(self.pantalla, _("Do you want to go back in the last movement?")):
                self.ayudas -= 1
                self.ponAyudas(self.ayudas)
                self.partida.anulaUltimoMovimiento(self.siJugamosConBlancas)
                self.siApertura = False
                self.listaAperturasStd.asignaApertura(self.partida)
                self.ponteAlFinal()
                self.siAnalizadoTutor = False
                self.refresh()
                self.siguienteJugada()

    def siguienteJugada(self):

        if self.estado == kFinJuego:
            return

        self.estado = kJugando

        self.siJuegaHumano = False
        self.ponVista()
        siBlancas = self.partida.ultPosicion.siBlancas

        if self.partida.numJugadas() > 0:
            jgUltima = self.partida.liJugadas[-1]
            if jgUltima:
                if jgUltima.siJaqueMate:
                    self.ponResultado(kGanaRival if self.siJugamosConBlancas == siBlancas else kGanamos)
                    return
                if jgUltima.siAhogado:
                    self.ponResultado(kTablas)
                    return
                if jgUltima.siTablasRepeticion:
                    self.ponResultado(kTablasRepeticion)
                    return
                if jgUltima.siTablas50:
                    self.ponResultado(kTablas50)
                    return
                if jgUltima.siTablasFaltaMaterial:
                    self.ponResultado(kTablasFaltaMaterial)
                    return

        if self.ayudas == 0:
            if self.categoria.sinAyudasFinal:
                self.quitaAyudas()
                self.siTutorActivado = False

        siRival = siBlancas == self.siRivalConBlancas
        self.ponIndicador(siBlancas)

        self.refresh()

        if siRival:
            self.pensando(True)
            self.desactivaTodas()

            siPensar = True

            if self.siApertura:

                siBien, desde, hasta, coronacion = self.apertura.juegaMotor(self.fenUltimo())

                if siBien:
                    self.rmRival = XMotorRespuesta.RespuestaMotor("Apertura", self.siRivalConBlancas)
                    self.rmRival.desde = desde
                    self.rmRival.hasta = hasta
                    self.rmRival.coronacion = coronacion
                    siPensar = False
                else:
                    self.siApertura = False

            if siPensar:
                self.rmRival = self.xrival.juega()

            self.pensando(False)

            if self.mueveRival(self.rmRival):
                self.siguienteJugada()
        else:

            self.siJuegaHumano = True
            self.activaColor(siBlancas)

    def mueveHumano(self, desde, hasta, coronacion=None):

        if self.siJuegaHumano:
            self.paraHumano()
        else:
            self.sigueHumano()
            return False

        movimiento = desde + hasta

        # Pe�n coronando
        if not coronacion and self.partida.ultPosicion.siPeonCoronando(desde, hasta):
            coronacion = self.tablero.peonCoronando(self.partida.ultPosicion.siBlancas)
            if coronacion is None:
                self.sigueHumano()
                return False
        if coronacion:
            movimiento += coronacion

        siBien, mens, jg = Jugada.dameJugada(self.partida.ultPosicion, desde, hasta, coronacion)

        if self.siTeclaPanico:
            self.sigueHumano()
            return False

        if siBien:

            siMirarTutor = self.siTutorActivado

            if self.siApertura:
                if self.apertura.compruebaHumano(self.fenUltimo(), desde, hasta):
                    siMirarTutor = False

            if self.siTeclaPanico:
                self.sigueHumano()
                return False

            if siMirarTutor:
                if not self.siAnalizadoTutor:
                    self.analizaTutor()
                    self.siAnalizadoTutor = True
                if self.mrmTutor is None:
                    self.sigueHumano()
                    return False
                if self.mrmTutor.mejorMovQue(movimiento):
                    self.refresh()
                    if not jg.siJaqueMate:
                        tutor = Tutor.Tutor(self, self, jg, desde, hasta, False)

                        if self.siApertura:
                            liApPosibles = self.listaAperturasStd.listaAperturasPosibles(self.partida)
                        else:
                            liApPosibles = None

                        if tutor.elegir(self.ayudas > 0, liApPosibles=liApPosibles):
                            if self.ayudas > 0:  # doble entrada a tutor.
                                self.reponPieza(desde)
                                self.ayudas -= 1
                                desde = tutor.desde
                                hasta = tutor.hasta
                                coronacion = tutor.coronacion
                                siBien, mens, jgTutor = Jugada.dameJugada(self.partida.ultPosicion, desde, hasta,
                                                                          coronacion)
                                if siBien:
                                    jg = jgTutor
                        elif self.configuracion.guardarVariantesTutor:
                            tutor.ponVariantes(jg, 1 + self.partida.numJugadas() / 2)

                        del tutor

            if self.siTeclaPanico:
                self.sigueHumano()
                return False

            self.movimientosPiezas(jg.liMovs)

            self.partida.ultPosicion = jg.posicion
            self.masJugada(jg, True)
            self.error = ""
            self.siguienteJugada()
            return True
        else:
            self.error = mens
            self.sigueHumano()
            return False

    def masJugada(self, jg, siNuestra):

        # Preguntamos al mono si hay movimiento
        if self.siTerminada():
            jg.siJaqueMate = jg.siJaque
            jg.siAhogado = not jg.siJaque

        self.partida.liJugadas.append(jg)
        if self.partida.pendienteApertura:
            self.listaAperturasStd.asignaApertura(self.partida)

        resp = self.partida.si3repetidas()
        if resp:
            jg.siTablasRepeticion = True
            rotulo = ""
            for j in resp:
                rotulo += "%d," % (j / 2 + 1,)
            rotulo = rotulo.strip(",")
            self.rotuloTablasRepeticion = rotulo

        if self.partida.ultPosicion.movPeonCap >= 100:
            jg.siTablas50 = True

        if self.partida.ultPosicion.siFaltaMaterial():
            jg.siTablasFaltaMaterial = True

        self.ponFlechaSC(jg.desde, jg.hasta)
        self.beepExtendido(siNuestra)

        self.ponAyudas(self.ayudas)

        self.pgnRefresh(self.partida.ultPosicion.siBlancas)
        self.refresh()

        self.ponPosicionDGT()

    def mueveRival(self, respMotor):
        desde = respMotor.desde
        hasta = respMotor.hasta

        coronacion = respMotor.coronacion

        siBien, mens, jg = Jugada.dameJugada(self.partida.ultPosicion, desde, hasta, coronacion)
        if siBien:
            self.partida.ultPosicion = jg.posicion

            if self.siApertura or not self.siTutorActivado:
                self.siAnalizadoTutor = False
            else:
                self.analizaTutor()  # Que analice antes de activar humano, para que no tenga que esperar
                self.siAnalizadoTutor = True
            self.error = ""
            self.masJugada(jg, False)
            self.movimientosPiezas(jg.liMovs, True)

            return True
        else:
            self.error = mens
            return False

    def ponResultado(self, quien):
        self.resultado = quien
        self.desactivaTodas()
        self.siJuegaHumano = False

        self.beepResultado(quien)

        nombreContrario = "%s (%s %d)" % ( self.xrival.nombre, _("Level"), self.nivelJugado )

        mensaje = _("End Game")

        if quien == kGanamos:

            mensaje = _X(_("Congratulations you have won against %1."), nombreContrario)
            hecho = "B" if self.siJugamosConBlancas else "N"
            if self.configuracion.rival.categorias.ponResultado(self.categoria, self.nivelJugado, hecho):
                mensaje += "<br><br>%s: %d (%s)" % (
                    _("Move to the next level"), self.categoria.nivelHecho + 1, self.categoria.nombre() )
            self.configuracion.graba()
            if self.puntos:
                puntuacion = self.configuracion.puntuacion()
                mensaje += "<br><br>%s: %d+%d = %d %s" % (
                    _("Total score"), puntuacion - self.puntos, self.puntos, puntuacion, _("pts"))
                self.xrotulo2()

        elif quien == kGanaRival:
            mensaje = _X(_("Unfortunately you have lost against %1"), nombreContrario)

        elif quien == kTablas:
            mensaje = _X(_("Draw against %1."), nombreContrario)

        elif quien == kTablasRepeticion:
            mensaje = _X(_("Draw due to three times repetition (n. %1) against %2."), self.rotuloTablasRepeticion,
                         nombreContrario)
            self.resultado = kTablas

        elif quien == kTablas50:
            mensaje = _X(_("Draw according to the 50 move rule against %1."), nombreContrario)
            self.resultado = kTablas

        elif quien == kTablasFaltaMaterial:
            mensaje = _X(_("Draw, not enough material to mate %1"), nombreContrario)
            self.resultado = kTablas

        self.guardarGanados(quien == kGanamos)
        QTUtil2.mensaje(self.pantalla, mensaje)
        self.ponFinJuego()

