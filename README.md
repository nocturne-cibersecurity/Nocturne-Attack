# Nocturne-Attack Python

*Simulador de tráfico para pruebas — proyecto para entender cómo funcionan las cargas y mitigación de tráfico.
Estado: Experimental.*

```
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
```
## Descripción

Este repositorio contiene código y ejemplos de simulación de tráfico pensados para fines educativos y de investigación en ciberseguridad defensiva. El objetivo es permitir a estudiantes y profesionales:
Aprender cómo se comportan redes y servidores bajo carga.
Desarrollar y probar estrategias de mitigación en entornos controlados.
Enseñar detección y análisis de tráfico anómalo.

**Advertencia legal y ética**

Este proyecto no debe usarse para atacar, interrumpir o comprometer sistemas de terceros. Utilizar estas herramientas contra servidores sin autorización es ilegal y podría tener consecuencias penales y civiles. El autor no se hace responsable por el mal uso del código.

**Requisitos**

- Python 3.x
- Dependencias: (lista de librerías necesarias si es que el proyecto queda como simulador)

ejemplo: requirements.txt con locust, requests (si corresponde para simulación local), etc.

## Istalación
# Nocturne

**Nocturne** — Herramienta de pruebas de red (modo educativo).  
**IMPORTANTE:** Usar solo en entornos propios o con autorización expresa.

## Quickstart
Clona el repo:
```bash
git clone https://github.com/tu-usuario/nocturne.git
cd nocturne

## Segunda Forma


*Copy the code and create script or proyect in pycharm or vs code
After it, in a terminal (bash) write: ls for find the proyect
If you stay in linux, write cd for find the proyect and cd for
enter to the directory, when you find the proyect, ejecute the proyect using python 3.*

**Search the script**
```
ls
```
**Find the location of the script**
```
cd Documents
cd Escritorio
```
**Ejecute the script with python3 in dis of linux**
```
IN THE BASH
python3 nocturne.py
```

# NOCTURNE.TXT

This is a script ejecutable directly to the bash
copy to clipboard and with CAT in the linux terminal and give permiss with chmod +x nocturne.py

```
cat nocturne.py
chmod +x nocturne.py
python3 nocturne.py
```

# DOCUMENTACION - HERRAMIENTA DE PRUEBAS DE CARGA NOCTURNE
## DESCRIPCION GENERAL

Nocturne es una herramienta profesional de pruebas de carga y seguridad diseñada para auditorias legitimas y testing de infraestructura. Desarrollada para equipos de seguridad y administradores de sistemas.

### Caracteristicas Principales:

    Interfaz multidioma (Espanol/Ingles)

    Multiples tecnicas de testing

    Interfaz profesional adaptable

    Enfoque en seguridad etica

### INDICE

    Requisitos del Sistema

    Instalacion

    Uso Basico

    Modulos Disponibles

    Ejemplos de Uso

    Parametros de Configuracion

    Consideraciones de Seguridad

    Solucion de Problemas

### REQUISITOS DEL SISTEMA

**Requisitos Minimos:**

    Python 3.8 o superior
    2 GB RAM
    100 MB espacio libre
    Conexion a internet (para dependencias)

Dependencias Python:
pip install requests
INSTALACION

Metodo 1: Ejecucion Directa
python nocturne_tool.py

Metodo 2: Clonacion
git clone https://github.com/nocturne-cibersecurity/DDoS-Nocturne
cd nocturne-tool
python nocturne_tool.py
USO BASICO

Flujo de Ejecucion Tipico:

    Seleccionar idioma (Espanol/Ingles)

    Ingresar objetivo (URL o IP)

    Seleccionar tipo de prueba

    Configurar parametros especificos

    Ejecutar y analizar resultados

Ejemplo Rapido:
Selecciona idioma: 2 (Espanol)
Objetivo: mi-servidor.local
Tipo de prueba: 1 (Escaneo de Puertos)
Puerto inicial: 1
Puerto final: 1000
MODULOS DISPONIBLES

    ESCANEO DE PUERTOS
    Proposito: Identificar servicios activos en el objetivo.

Parametros:

    Host: IP o dominio objetivo

    Puerto inicial: Rango inferior (default: 1)

    Puerto final: Rango superior (default: 1000)

Salida Ejemplo:
[ESCANEO] Escaneando puertos 1-1000 en 192.168.1.1
[OK] Puerto 22 ABIERTO (ssh)
[OK] Puerto 80 ABIERTO (http)
[OK] Puerto 443 ABIERTO (https)
[OBJETIVO] Escaneo completado. Puertos abiertos: 3

    HTTP FLOOD
    Proposito: Pruebas de carga en servicios web.

Parametros:

    URL: Endpoint objetivo

    Numero de requests: Volumen de prueba

    Delay: Intervalo entre requests

Metricas:

    Requests exitosos/fallidos

    Tiempo total de ejecucion

    Requests por segundo

    TCP FLOOD
    Proposito: Pruebas de conectividad y carga TCP.

Parametros:

    IP objetivo: Direccion del servidor

    Puerto: Puerto TCP objetivo

    Conexiones: Numero de conexiones simultaneas

    Mensaje: Datos a enviar (opcional)

    SLOWLORIS ATTACK
    Proposito: Pruebas de resistencia a conexiones lentas.

Caracteristicas:

    Conexiones HTTP parciales

    Mantenimiento de sockets abiertos

    Bajo ancho de banda requerido

    DDOS SIMULADO
    Proposito: Pruebas de resistencia multi-tecnica.

Tecnicas incluidas:

    Multiples workers simultaneos

    Requests HTTP variados

    User-Agents rotativos

PARAMETROS DE CONFIGURACION

Configuracion Global (En codigo):

class Config:
LANGUAGE = "spanish" # "english" or "spanish"
EMOJIS = False # True para interfaz visual
MAX_WORKERS = 200 # Maximo de hilos concurrentes

Limites Recomendados:

    PORT_SCAN_MAX_PORTS: 10000

    HTTP_FLOOD_MAX_REQUESTS: 10000

    TCP_FLOOD_MAX_CONNECTIONS: 500

CONSIDERACIONES DE SEGURIDAD

Uso Etico Requerido:

SOLO usar en sistemas propios o con autorizacion explicita.
No utilizar contra infraestructura ajena sin permiso.

Objetivos Permitidos:

    localhost

    127.0.0.1

    Redes locales (192.168.., 10...*)

    Dominios de propiedad propia

Protecciones Implementadas:

    Timeouts en todas las operaciones

    Limites de recursos configurables

    Validacion de objetivos

    Manejo seguro de excepciones

EJEMPLOS DE USO

Caso 1: Auditoria de Servidor Web

    Escaneo de puertos
    Objetivo: mi-sitio.com
    Modulo: Escaneo de Puertos
    Puertos: 1-1000

    Prueba de carga HTTP
    Modulo: HTTP Flood
    Requests: 1000
    Delay: 0.1

Caso 2: Testing de Firewall

    TCP Flood testing
    Objetivo: firewall.local
    Puerto: 80
    Conexiones: 100

    Slowloris testing
    Objetivo: sitio-web.com
    Sockets: 150

Caso 3: Pruebas de Resiliencia

    DDoS simulado
    Objetivo: api.servicio.com
    Duracion: 120 segundos

SOLUCION DE PROBLEMAS

Error: "Connection refused"

    Verificar que el objetivo este activo

    Confirmar conectividad de red

    Verificar firewall

Error: "Too many open files"

    Reducir MAX_WORKERS

    Limitar numero de conexiones

    Cerrar otras aplicaciones

Rendimiento Lento:

    Aumentar MAX_WORKERS

    Reducir timeouts

    Verificar recursos del sistema

Problemas de DNS:

    Usar IP en lugar de hostname

    Verificar configuracion DNS

    Probar con diferentes resolvers

PREGUNTAS FRECUENTES

P: ¿Es legal usar esta herramienta?
R: Solo es legal en sistemas propios o con autorizacion explicita por escrito.

P: ¿Puedo usar esto para testing de mi sitio web?
R: Si, siempre que sea tu propiedad o tengas permiso del propietario.

P: ¿Que diferencia hay entre los modos de idioma?
R: Solo cambia el idioma de la interfaz, la funcionalidad es identica.

P: ¿Como puedo contribuir al proyecto?
R: Reportando bugs, sugiriendo mejoras o desarrollando nuevos modulos.
LICENCIA Y USO

Esta herramienta se proporciona solo con fines educativos y de testing autorizado.
El usuario es responsable del uso que le de a la herramienta.
Siempre obtener autorizacion explicita antes de realizar cualquier prueba.
CONTACTO Y SOPORTE

Para reportar problemas o sugerir mejoras:

    GitHub: https://github.com/nocturne-cibersecurity

    Email: private

Documentacion version: 1.4
Ultima actualizacion: 2025
Herramienta desarrollada por @Nocturne
