import sys, math
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QRadialGradient, QLinearGradient, QPolygonF, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class TornoWidget(QWidget):
    def __init__(self, ciclos=30, velocidad_rpm=120, largo=80, ancho=20):
        super().__init__()
        self.setWindowTitle("Torno 2.0 - Animación Realista")
        self.resize(640, 360)

        # Parámetros
        self.ciclos_max = max(1, ciclos)
        self.velocidad_rpm = velocidad_rpm
        self.largo = max(20, min(largo, 150))
        self.ancho = max(5, min(ancho, 60))

        # Estado animación
        self.ciclo = 0
        self.broca_x = 50.0
        self.broca_y = self.height() * 0.5
        # Centro y radio del mandril
        self.radio = 60
        self.cx = int(self.width() * 0.55)
        self.cy = int(self.height() * 0.5)

        # Cálculo de avance
        distancia_total = (self.cx - self.radio) - self.broca_x - self.largo
        self.frames_por_ciclo = 10
        self.total_frames = self.ciclos_max * self.frames_por_ciclo
        self.dx = distancia_total / self.total_frames

        # Timer ~60 FPS
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

        # Ángulo de rotación
        self.angulo = 0.0

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Fondo
        p.fillRect(self.rect(), Qt.white)

        # Actualizar estado
        if self.ciclo < self.ciclos_max:
            # Rotación por frame: 360 * rpm/60 fps * tiempo(frame)
            self.angulo = (self.angulo + (360 * self.velocidad_rpm/60)*0.016) % 360
            self.broca_x += self.dx
            # Contar frames y ciclos
            # Aquí simplemente incrementamos ciclo al avanzar 'frames_por_ciclo' veces
            if int((self.broca_x - 50.0) / self.dx) % self.frames_por_ciclo == 0:
                self.ciclo += 1
        else:
            if self.timer.isActive():
                self.timer.stop()
                QMessageBox.information(self, "¡Broca rota!", f"La broca se rompió tras {self.ciclos_max} ciclos.")

        # Dibuja torno y broca
        self.draw_mandrill(p)
        self.draw_disco(p)
        self.draw_broca(p)

        # Texto ciclo
        p.setPen(Qt.black)
        p.setFont(QFont("Arial", 10))
        p.drawText(10, 20, f"Ciclo {self.ciclo}/{self.ciclos_max}")

    def draw_mandrill(self, p: QPainter):
        # Mandril: tres mordazas giratorias
        p.save()
        p.translate(self.cx, self.cy)
        p.rotate(self.angulo)
        for ang in (0, 120, 240):
            p.save()
            p.rotate(ang)
            rect = QRectF(int(self.radio*0.3), -10, 40, 20)
            p.setBrush(QBrush(QColor(120, 120, 120)))
            p.setPen(Qt.NoPen)
            p.drawRect(rect)
            p.restore()
        p.restore()

    def draw_disco(self, p: QPainter):
        # Disco con gradiente radial
        grad = QRadialGradient(self.cx, self.cy, self.radio)
        grad.setColorAt(0, QColor(220,220,220))
        grad.setColorAt(1, QColor(80,80,80))
        p.setBrush(QBrush(grad))
        p.setPen(QPen(Qt.black, 2))
        p.drawEllipse(self.cx-self.radio, self.cy-self.radio, 2*self.radio, 2*self.radio)

        # Marcas radiales
        p.save()
        p.translate(self.cx, self.cy)
        p.rotate(self.angulo)
        p.setPen(QPen(Qt.black,2))
        for i in range(12):
            p.drawLine(0,0,0,-self.radio)
            p.rotate(30)
        p.restore()

    def draw_broca(self, p: QPainter):
        x = self.broca_x
        y = self.broca_y
        largo_c = self.largo*0.75
        ancho = self.ancho

        # Color según proximidad
        dist = max(0, (self.cx - self.radio) - (x + self.largo))
        frac = 1 - min(1, dist/(self.dx*self.frames_por_ciclo))
        hsv_h = (1 - frac) * 0.33  # 0.33 verde, 0 rojo
        color = QColor.fromHsvF(hsv_h, 1, 1)

        # Cuerpo con gradiente
        grad = QLinearGradient(int(x), int(y-ancho/2), int(x+largo_c), int(y+ancho/2))
        grad.setColorAt(0, color.lighter(150))
        grad.setColorAt(1, color.darker(150))
        p.setBrush(QBrush(grad))
        p.setPen(QPen(Qt.black,1))
        rect = QRectF(x, y-ancho/2, largo_c, ancho)
        p.drawRoundedRect(rect, 5, 5)

        # Líneas helicoidales
        p.setPen(QPen(color.darker(),1))
        sep = 8
        for i in range(int(largo_c/sep)):
            x1 = x + i*sep
            y1 = y-ancho/2
            x2 = x1+sep/2
            y2 = y+ancho/2
            p.drawLine(int(x1), int(y1), int(x2), int(y2))

        # Punta cónica
        grad2 = QLinearGradient(int(x+largo_c), int(y-ancho/2), int(x+self.largo), int(y+ancho/2))
        grad2.setColorAt(0, color)
        grad2.setColorAt(1, color.darker(250))
        p.setBrush(QBrush(grad2))
        p.setPen(QPen(Qt.black,1))
        punta = QPolygonF([
            QPointF(x+largo_c, y-ancho/2),
            QPointF(x+self.largo, y),
            QPointF(x+largo_c, y+ancho/2),
        ])
        p.drawPolygon(punta)


def main():
    app = QApplication(sys.argv)
    w = TornoWidget(ciclos=30, velocidad_rpm=120, largo=100, ancho=30)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
