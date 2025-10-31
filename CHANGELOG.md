# Registro de Cambios

Todos los cambios notables en este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2023-10-30

### Agregado
- Sistema completo de internacionalización (i18n) con soporte para inglés y español
- Menú de configuración interactivo
- Soporte para Tor con rotación de identidad
- Documentación completa del proyecto
- Políticas de seguridad

### Cambiado
- Refactorización completa del código para mejor mantenibilidad
- Mejora en el manejo de errores
- Optimización del rendimiento en ataques DDoS

### Corregido
- Problema de cambio de idioma que no persistía
- Errores menores en la interfaz de usuario
- Problemas de estabilidad en conexiones de red

## [0.9.0] - 2023-10-15

### Agregado
- Funcionalidad básica de escaneo de puertos
- Ataque HTTP Flood
- Ataque TCP Flood
- Ataque Slowloris
- Ataque DDoS básico

### Cambiado
- Mejoras en la estructura del proyecto
- Optimización de recursos

### Corregido
- Problemas de concurrencia
- Errores en el manejo de sockets

---

## Notas de Versión

### Convención de Versiones

Dado un número de versión MAYOR.MENOR.PARCHE, se incrementa:

1. **MAYOR**: Cambios incompatibles con versiones anteriores
2. **MENOR**: Nuevas funcionalidades compatibles
3. **PARCHE**: Correcciones de errores compatibles

### Tipos de Cambios

- **Agregado**: Nueva funcionalidad
- **Cambiado**: Cambios en funcionalidad existente
- **Obsoleto**: Próxima eliminación
- **Eliminado**: Funcionalidad eliminada
- **Corregido**: Corrección de errores
- **Seguridad**: Vulnerabilidades corregidas

---

## Historial de Versiones

- **1.0.0** - Versión estable con todas las características
- **0.9.0** - Versión beta inicial

## Próximas Características

- [ ] Soporte para más idiomas
- [ ] Interfaz gráfica de usuario (GUI)
- [ ] Más técnicas de ataque
- [ ] Panel de estadísticas en tiempo real
- [ ] API REST para integración con otras herramientas

---

*Este archivo sigue el estándar [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).*
