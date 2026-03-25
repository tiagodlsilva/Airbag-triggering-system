from machine import Pin, I2C
from time import sleep, ticks_ms
import math
import socket
import network

# ──────────  TENTATIVA DE CONEXÃO WI-FI ──────────
wifi_ok = False
try:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('Wifi Tiago', 'Tiago4321')

    timeout = 5  # segundos
    while not wlan.isconnected() and timeout > 0:
        print("Tentando conectar ao Wi-Fi...")
        sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("Wi-Fi conectado")
        print("IP do ESP32:", wlan.ifconfig()[0])
        wifi_ok = True
    else:
        print("Wi-Fi não conectado – executando offline")
except Exception as e:
    print("Erro ao configurar Wi-Fi:", e)

# ──────────  ADXL345 DEFINES  ──────────
ADDR        = 0x53
DATA_FORMAT = 0x31
POWER_CTL   = 0x2D
DATA_X0     = 0x32

# ──────────  I2C / LED  ──────────
i2c = I2C(0, scl=Pin(25), sda=Pin(26))
led_danger = Pin(21, Pin.OUT)
led_danger.value(0)
botão = Pin(23, Pin.IN)

estado_botao = False
start_time = 0

def handler_botao(Pin):
    global estado_botao, start_time
    estado_botao = not estado_botao
    start_time = ticks_ms()
    if estado_botao:
        i2c.writeto_mem(ADDR, POWER_CTL, b'\x08')
        i2c.writeto_mem(ADDR, DATA_FORMAT, b'\x0B')
    else:
        i2c.writeto_mem(ADDR, POWER_CTL, b'\x00')

botão.irq(trigger=Pin.IRQ_FALLING, handler=handler_botao)

# ──────────  COMPLEMENT‑2 16‑bit  ──────────
def twos_comp16(raw):
    return raw - 65536 if raw & 0x8000 else raw

# ──────────  FILTRO E VARIÁVEIS  ──────────
alpha = 0.9
x_filt = y_filt = z_filt = 0
angle_duration = 0
free_fall = 0

# ──────────  SOCKET OPCIONAL ──────────
cli = None
if wifi_ok:
    try:
        PORT = 12345
        srv = socket.socket()
        srv.bind(("0.0.0.0", PORT))
        srv.listen(1)
        print("Aguardando conexão do LabVIEW na porta", PORT)
        srv.settimeout(10)  # evita travar para sempre
        try:
            cli, addr = srv.accept()
            print("Conectado a", addr)
        except:
            print("Sem conexão do LabVIEW – prosseguindo offline")
            cli = None
    except Exception as e:
        print("Erro ao configurar socket:", e)
        cli = None

wait = 0
crash_type = 0
g = 9.81

# ──────────  LOOP PRINCIPAL  ──────────
while True:
    now = ticks_ms() - start_time
    if estado_botao:
        # ─ Leitura dos dados do ADXL345 ─
        d = i2c.readfrom_mem(ADDR, DATA_X0, 6)
        y = + twos_comp16(d[0] | d[1]<<8) * 0.0393
        x = - twos_comp16(d[2] | d[3]<<8) * 0.0393
        z = - twos_comp16(d[4] | d[5]<<8) * 0.0393

        # ─ Filtro IIR ─
        x_filt = alpha*x + (1-alpha)*x_filt
        y_filt = alpha*y + (1-alpha)*y_filt
        z_filt = alpha*z + (1-alpha)*z_filt

        roll  = math.atan2(y_filt, math.sqrt(x_filt**2 + z_filt**2)) * 57.2958
        pitch = math.atan2(-x_filt, math.sqrt(y_filt**2 + z_filt**2)) * 57.2958

        # ─ Envio para LabVIEW, se estiver conectado ─
        if cli:
            try:
                cli.send(f"{x_filt*100:.0f},{y_filt*100:.0f},{z_filt*100:.0f},{pitch:.2f},{roll:.2f},{crash_type},{now:.2f}\n".encode())
            except OSError:
                cli.close()
                cli = None
                print("Conexão com LabVIEW perdida")

        print(f"{x:.2f}, {y:.2f}, {z:.2f}, {pitch:.2f}, {roll:.2f}")

        # ─ DETECÇÃO DE EVENTOS ─
        crash = abs(x) > 5 * g or abs(y) > 5 * g or abs(z) > 5 * g
        tilt = abs(roll) > 50

        if abs(x_filt) < 0.5*g and abs(y_filt) < 0.5*g and abs(z_filt) < 0.5*g or wait == 3:
            free_fall += 1
            if free_fall > 10:
                if wait == 0:
                    last = now
                wait = 3
                led_danger.value(1)
                print("Queda livre!")
                crash_type = 3
                if now - last >= 1000:
                    sleep(4)
                    led_danger.value(0)
                    print('BACK TO START')
                    wait = 0
                    crash_type = 0
                    free_fall = 0

        elif crash or wait == 1:
            if wait == 0:
                last = now
            wait = 1
            led_danger.value(1)
            print("Colisão detectada!")
            crash_type = 1
            if now - last >= 1000:
                sleep(4)
                led_danger.value(0)
                wait = 0
                crash_type = 0

        elif tilt or wait == 2:
            angle_duration += 1
            if angle_duration > 10:
                if wait == 0:
                    last = now
                wait = 2
                led_danger.value(1)
                print('Capotou!')
                crash_type = 2
                if now - last >= 1000:
                    sleep(4)
                    led_danger.value(0)
                    wait = 0
                    crash_type = 0
                    angle_duration = 0
        else:
            angle_duration = 0

        sleep(0.01)  # 100 Hz
