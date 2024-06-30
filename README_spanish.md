# Cliente OAuth de Gmail para IMAP y SMTP

Este repositorio proporciona una guía completa y herramientas para configurar la autenticación OAuth2 tanto para conexiones IMAP como SMTP con Gmail, utilizando Python. Ya sea que necesites enviar correos electrónicos a través de SMTP o leer correos electrónicos a través de IMAP en tus pruebas o scripts automatizados de extremo a extremo, este proyecto te cubre. Está construido sobre las bibliotecas de autenticación de Google y simplifica aún más el proceso con una capa adicional, facilitando la integración de la autenticación OAuth2 de Gmail en tus proyectos.

## Sobre el Proyecto

El proyecto está dividido en dos partes principales: una para el envío de correos electrónicos SMTP usando OAuth2 de Google Gmail, y otra para configurar la autenticación OAuth2 de Google para conexiones IMAP con Gmail. Es ideal para aquellos que buscan integrar de manera segura las funcionalidades de envío y recepción de correos electrónicos de Gmail en sus aplicaciones Python.

## Primeros Pasos

### Configuración de la API de Google Gmail:

Para usar OAuth2 para SMTP e IMAP de Gmail, sigue estos pasos iniciales:

1. **Cuenta de Google Cloud Platform:** Se requiere una cuenta de Google Cloud Platform.
2. **Habilitar la API de Gmail:** Ve a la página de [APIs y servicios habilitados](https://console.cloud.google.com/apis/dashboard) y habilita la API de Gmail.
3. **Configurar la Pantalla de Consentimiento de OAuth:** (Accede clickando al apartado del panel de la izquierda `Pantalla de consentimiento OAuth`). Agrega el alcance 'https://mail.google.com/' para que coincida con los SCOPES utilizados en el código Python. También agrega tu correo electrónico como usuarios de prueba.
4. **Crear ID de Cliente OAuth 2.0:** Navega a [Credenciales](https://console.cloud.google.com/apis/credentials), haz clic en "+ Crear Credenciales" y selecciona "ID de Cliente OAuth".
5. **Descargar Credenciales:** Descarga el archivo de secreto del cliente y renómbralo a `credentials.json` en el directorio del proyecto.

## Uso

### Envío de Correos Electrónicos SMTP

Consulta la parte de configuración de SMTP para enviar correos electrónicos utilizando Gmail con autenticación OAuth2.

### Lectura de Correos Electrónicos IMAP

Una vez que tengas el archivo de token, puedes autenticar conexiones IMAP para leer correos electrónicos de Gmail usando las funciones proporcionadas por Pyioga.

```python
import pyioga
from imap_tools import MailBox, AND

username = "user@gmail.com"
access_token = pyioga.get_access_token("token.json")
with MailBox('imap.gmail.com').xoauth2(username, access_token) as mailbox:
    for msg in mailbox.fetch():
        print(msg.date, msg.subject, len(msg.text or msg.html))
```

`pyioga.get_access_token` asegura que recibas un token válido, generando una excepción de lo contrario.

## Conclusión

Este repositorio ofrece un enfoque simplificado para integrar la autenticación OAuth2 de Gmail tanto para el envío como para la recepción de correos electrónicos en tus proyectos Python. Siguiendo los pasos descritos, puedes configurar de manera segura las funcionalidades SMTP e IMAP con Gmail.

Recuerda mantener tus credenciales seguras y seguir las mejores prácticas para gestionar tokens OAuth y secretos de aplicaciones.

## Bibliografía
- [IMAP OAuth](https://github.com/mbroton/pyioga/blob/main/README.md)
- [SMTP OAuth](https://github.com/zamyen/smtp_oauth_python_gmail/blob/main/main.py)
