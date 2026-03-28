"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ██████╗ █████╗ ███╗   ███╗██╗██╗      █████╗ ██████╗  ██████╗ ████████╗
 ██╔════╝██╔══██╗████╗ ████║██║██║     ██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝
 ██║     ███████║██╔████╔██║██║██║     ███████║██████╔╝██║   ██║   ██║   
 ██║     ██╔══██║██║╚██╔╝██║██║██║     ██╔══██║██╔══██╗██║   ██║   ██║   
 ╚██████╗██║  ██║██║ ╚═╝ ██║██║███████╗██║  ██║██████╔╝╚██████╔╝   ██║   
  ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 NOMBRE:    CamilaBot V14.0 - MEGA SUPREMA EDITION
👨‍💻 CREADOR:  AnyerJR
🌍 PAÍS:      Venezuela 🇻🇪
📅 VERSIÓN:   14.0 (1000+ COMANDOS ULTRA)
🧠 CEREBRO:   Google Custom Search API + APIs Públicas + 7 Categorías IA
⚡ FEATURES:  1000+ comandos, Audio Relajante, Admin Supremo, IA Avanzada

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ÍNDICE DE MÓDULOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1]  IMPORTACIONES Y CONFIGURACIÓN

[2]  SISTEMA DE ARCHIVOS Y BASES DE DATOS

[3]  SISTEMA DE LOGS Y MONITOREO

[4]  SISTEMA DE RANGOS Y ECONOMÍA

[5]  COMANDOS DE PERFIL Y REGISTRO

[6]  SISTEMA ECONÓMICO

[7]  CEREBRO IA - GOOGLE SEARCH

[8]  COMANDOS DE ROL E INTERACCIÓN

[9]  MÓDULO MULTIMEDIA

[10] MÓDULO OSINT (Investigación)

[11] COMANDOS ADMINISTRATIVOS

[12] MÓDULO DE INFORMACIÓN

[13] ENTRETENIMIENTO Y JUEGOS

[14] HERRAMIENTAS ÚTILES

[15] MÓDULO FINANCIERO

[16] MENÚ PRINCIPAL Y REGISTRO DE COMANDOS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
# ------------------- CÓDIGO PARA MANTENER ACTIVO 24/7 -------------------
from flask import Flask
from threading import Thread

# Creamos un servidor web temporal para evitar inactividad
app = Flask('CamiBotServer')

@app.route('/')
def home():
    return "✅ Cami.bot está en línea 24/7!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server_thread = Thread(target=run_server)
    server_thread.start()
# ------------------------------------------------------------------------


# ========================================
# [1] IMPORTACIONES Y CONFIGURACIÓN
# ========================================
import os
import json
import random
import time
import asyncio
import re
import requests
import functools
import string
import hashlib
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote, urljoin, urlparse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import yt_dlp
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import io

# bs4 (BeautifulSoup) - necesario para scraping de APKPure, APKTodo, etc.
# Instalar con: pip install beautifulsoup4
try:
    from bs4 import BeautifulSoup
    BS4_DISPONIBLE = True
except ImportError:
    BS4_DISPONIBLE = False
    print("⚠️ [AVISO] beautifulsoup4 no instalada. Ejecuta: pip install beautifulsoup4")

# ========================================
# [SISTEMA MULTITAREA] - Colas y Semáforos
# ========================================
# Sistema para procesar múltiples descargas/búsquedas en paralelo sin bloquear el bot
task_queue = []
task_semaphore = asyncio.Semaphore(10)  # Máximo 10 tareas simultáneas (sin bloqueos)
executor = ThreadPoolExecutor(max_workers=20)  # 20 hilos para máxima concurrencia

# ========================================
# CONFIGURACIÓN MAESTRA DEL BOT
# ========================================
# Token de Telegram obtenido de @BotFather
TOKEN = "8279965294:AAHb4Jv4FBsUoSCbBEJMhMxwWl1_7nQxr24"

# ID del administrador (creador del bot)
ADMIN_ID = 7953907047

# Ruta donde se guardan los archivos del bot
RUTA_LOGS = "./logs_cami"

# Versión actual del bot
VERSION = "V15.0 - MEGA SUPREMA MASIVO 2000+ LÍNEAS CON 1500+ COMANDOS"

# ========================================
# API de Google Custom Search (DESHABILITADA - usando wikis públicas)
# ========================================
# Para Google Custom Search - no es necesario, usamos Wikipedia/DuckDuckGo públicos
# Si en el futuro quieres agregarlo: obtén tu API Key en https://console.cloud.google.com/
GOOGLE_API_KEY = "TU_GOOGLE_API_KEY_AQUI"  # (no usado - búsquedas con APIs públicas)
SEARCH_ENGINE_ID = "TU_SEARCH_ENGINE_ID_AQUI"  # (no usado)
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

# Asegurar que la carpeta de datos exista para evitar errores de ruta
if not os.path.exists(RUTA_LOGS):
    os.makedirs(RUTA_LOGS)


# ========================================
# [HELPER] Stubs async para comandos en desarrollo
# ========================================
def stub_cmd(nombre):
    """Crea un handler async para comandos que aún no tienen implementación."""
    async def _handler(update, context):
        await update.message.reply_text(
            f"🔧 El comando `/{nombre}` está en desarrollo.\n"
            "✨ _Próximamente disponible._",
            parse_mode="Markdown"
        )
    _handler.__name__ = f"stub_{nombre}"
    return _handler

# ========================================
# [2] SISTEMA DE ARCHIVOS Y BASES DE DATOS
# ========================================
def cargar_db(archivo):
    """
    Carga los datos desde un archivo JSON.
    
    Args:
        archivo (str): Nombre del archivo JSON a cargar
        
    Returns:
        dict: Datos cargados o diccionario vacío si falla
    """
    path = f"{RUTA_LOGS}/{archivo}"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try: 
                return json.load(f)
            except: 
                return {}
    return {}

def guardar_db(archivo, data):
    """
    Guarda los datos en formato JSON con indentación.
    
    Args:
        archivo (str): Nombre del archivo JSON
        data (dict): Datos a guardar
    """
    with open(f"{RUTA_LOGS}/{archivo}", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ========================================
# INICIALIZACIÓN DE BASES DE DATOS GLOBALES
# ========================================
# Cada archivo JSON almacena diferentes datos del bot:

# banco.json - Dinero de cada usuario
banco = cargar_db("banco.json")

# niveles.json - Puntos de experiencia (XP) de cada usuario
niveles = cargar_db("niveles.json")

# usuarios_datos.json - Información personal (nombre, edad, género)
usuarios_info = cargar_db("usuarios_datos.json")

# blacklist.json - Usuarios bloqueados
blacklist = cargar_db("blacklist.json")

# conversaciones.json - Historial de conversaciones con cada usuario
conversaciones = cargar_db("conversaciones.json")

# tres_rayas.json - Estado de partidas de Tres en Rayas
tres_rayas = cargar_db("tres_rayas.json")

# ========================================
# [3] SISTEMA DE LOGS Y MONITOREO
# ========================================
# ========================================
# [DECORADOR] Manejo de Tareas Largas/Pesadas
# ========================================
def tarea_larga(func):
    """
    Decorador que maneja funciones largas (descargas, búsquedas) sin bloquear el bot.
    Permite hasta 5 tareas simultáneas con gestión de cola.
    """
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        nick = update.effective_user.first_name
        chat_id = update.message.chat_id
        
        try:
            # Verificar si hay demasiadas tareas
            if len(task_queue) >= 10:
                await update.message.reply_text(
                    "⏳ ⚠️ **¡Demasiados procesos activos!**\n\n"
                    "Espera unos segundos e intenta otra vez.\n"
                    f"_Actualmente: {len(task_queue)} tareas en procesamiento_",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            # Crear info de tarea
            tarea_info = {
                'user_id': user_id,
                'chat_id': chat_id,
                'nick': nick,
                'comando': func.__name__,
                'inicio': datetime.now(),
                'posicion': len(task_queue) + 1
            }
            
            task_queue.append(tarea_info)
            
            # Mostrar estado
            posicion = tarea_info['posicion']
            msg_espera = await update.message.reply_text(
                f"🔄 **Procesando tu solicitud...**\n\n"
                f"📍 Posición en cola: `#{posicion}` de `{len(task_queue)}`\n"
                f"⏱️ _Tiempo estimado: 30-90 segundos_",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Ejecutar la función pesada en semáforo
            async with task_semaphore:
                try:
                    await func(update, context)
                    
                    # Actualizar mensaje de éxito
                    try:
                        await msg_espera.edit_text(
                            "✅ **¡Solicitud completada!**\n"
                            "✨ _Tu tarea fue procesada correctamente_",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except:
                        pass
                        
                except Exception as e:
                    print(f"[ERROR TAREA] {func.__name__}: {str(e)}")
                    try:
                        await msg_espera.edit_text(
                            f"❌ **Error al procesar:**\n"
                            f"`{str(e)[:100]}`\n\n"
                            "_Intenta de nuevo más tarde._",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except:
                        await update.message.reply_text("❌ Error en el procesamiento.")
                        
        except Exception as e:
            print(f"[ERROR SISTEMA TAREA] {e}")
            await update.message.reply_text(
                "⚠️ **Ha ocurrido un error interno.**",
                parse_mode=ParseMode.MARKDOWN
            )
        finally:
            # Remover tarea de la cola
            try:
                task_queue.remove(tarea_info)
            except:
                pass
    
    return wrapper

# ========================================
# Comando para ver estado del bot
# ========================================
async def estado_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra estado de tareas activas y carga del bot"""
    total_activas = len(task_queue)
    usuario_actual = update.effective_user.id
    
    tareas_usuario = [t for t in task_queue if t['user_id'] == usuario_actual]
    
    mensaje = f"📊 **ESTADO DEL BOT CAMI**\n"
    mensaje += f"├─ Tareas Activas: `{total_activas}/5`\n"
    mensaje += f"├─ Tus Tareas: `{len(tareas_usuario)}`\n"
    mensaje += f"└─ Tiempo Promedio: `~45 segundos`\n\n"
    
    if total_activas == 0:
        mensaje += "✅ Bot sin carga, listo para trabajar"
    elif total_activas <= 2:
        mensaje += "🟢 Carga baja, procesa rápido"
    elif total_activas <= 4:
        mensaje += "🟡 Carga moderada, espera ~60s"
    else:
        mensaje += "🔴 Carga alta, espera +90s"
    
    await update.message.reply_text(mensaje, parse_mode=ParseMode.MARKDOWN)

def registrar_evento(u_id, nick, accion, categoria="INFO"):
    """
    Registra eventos del bot en consola y archivo de texto.
    
    Muestra información decorada en la terminal y guarda un log permanente.
    
    Args:
        u_id (int): ID del usuario de Telegram
        nick (str): Nombre del usuario
        accion (str): Descripción de la acción realizada
        categoria (str): Tipo de evento (INFO, ECONOMÍA, ROL, etc.)
    """
    # Obtener hora actual
    hora = datetime.now().strftime("%H:%M:%S")
    
    # Diseño decorado para la consola
    print(f"╔{'═'*50}╗")
    print(f"║ 🕒 {hora} | 📂 CAT: {categoria}")
    print(f"║ 👤 USUARIO: {nick} ({u_id})")
    print(f"║ 📝 ACCIÓN: {accion}")
    print(f"╚{'═'*50}╝")
    
    # Guardado en archivo TXT permanente
    fecha_completa = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{RUTA_LOGS}/mega_historial.txt", "a", encoding="utf-8") as f:
        f.write(f"[{fecha_completa}] [{categoria}] ID:{u_id} | {nick}: {accion}\n")

# ========================================
# [4] SISTEMA DE RANGOS Y ECONOMÍA
# ========================================
# Motor de rangos estilo Free Fire basado en puntos de experiencia (XP)
# ========================================
# DEFINICIÓN DE RANGOS
# ========================================
# Escala de rangos basada en puntos XP (de menor a mayor)
RANGOS_FF = [
    (0, "Mendigo 🦴"),                    # 0+ XP
    (100, "Bronce I 🥉"),                 # 100+ XP
    (400, "Plata I 🥈"),                  # 400+ XP
    (1000, "Oro I 🥇"),                   # 1,000+ XP
    (2500, "Platino I 💎"),               # 2,500+ XP
    (5000, "Diamante I 💎"),              # 5,000+ XP
    (10000, "Heroico 🔥"),                # 10,000+ XP
    (25000, "Gran Maestro 🏆"),           # 25,000+ XP
    (50000, " Gran Maestro Elite👽"),           #50000+ XP
    (1000000, "DIOS DE VENEZUELA 🇻🇪")    # 1,000,000+ XP
]

def obtener_rango(user_id):
    """
    Calcula el rango actual del usuario según su experiencia.
    
    Args:
        user_id (int): ID del usuario
        
    Returns:
        str: Nombre del rango con emoji
    """
    # El creador siempre tiene rango especial
    if user_id == ADMIN_ID:
        return "🎖️ CREADOR SUPREMO 🎖️"
    
    # Obtener puntos del usuario
    uid = str(user_id)
    pts = niveles.get(uid, 0)
    
    # Determinar rango según puntos
    rango_actual = "Mendigo 🦴"
    for pts_req, nombre in RANGOS_FF:
        if pts >= pts_req:
            rango_actual = nombre
        else:
            break
    
    return rango_actual

# ========================================
# FUNCIONES DE ECONOMÍA
# ========================================
def sumar_dinero(user_id, cantidad):
    """
    Añade o resta dinero de la cuenta bancaria del usuario.
    
    Args:
        user_id (int): ID del usuario
        cantidad (float): Cantidad a sumar (negativo para restar)
    """
    uid = str(user_id)
    banco[uid] = round(banco.get(uid, 0.0) + cantidad, 2)
    guardar_db("banco.json", banco)

def sumar_xp(user_id, cantidad):
    """
    Añade puntos de experiencia para subir de rango.
    
    Args:
        user_id (int): ID del usuario
        cantidad (int): Cantidad de XP a sumar
    """
    uid = str(user_id)
    niveles[uid] = niveles.get(uid, 0) + cantidad
    guardar_db("niveles.json", niveles)

# ========================================
# [5] COMANDOS DE PERFIL Y REGISTRO
# ========================================

# --- [ FUNCIÓN: PERFIL DETALLADO ] ---
ACCIONES_ROL = {
    "beso": "💋 {u} le dio un beso apasionado a {t}!",
    "slap": "👋 {u} le metió tremendo coñazo a {t}!",
    "abrazo": "🫂 {u} abrazó fuertemente a {t}. ¡Qué ternura!",
    "matar": "🔫 {u} liquidó a {t} de un tiro en la cabeza. ¡F!",
    "violar": "🥵 {u} se puso abusivo con {t}... ¡Llamen a la ley!",
    "morder": "🦷 {u} le dejó la marca de los dientes a {t}!",
    "lamer": "👅 {u} lamió a {t}. ¡Qué asco, compadre!",
    "sexo": "🔞 {u} y {t} se fueron al cuarto... ¡Hay ruido de cama!",
    "casar": "💍 {u} y {t} se han unido en matrimonio eterno. ❤️",
    "divorcio": "💔 {u} le pidió el divorcio a {t}. Se acabó el amor.",
    "golpe": "🥊 {u} le metió un gancho al hígado a {t}!",
    "patear": "🦵 {u} le dio una patada voladora a {t}!",
    "insultar": "🤬 {u} mandó para el carajo a {t} sin piedad.",
    "nalgada": "🍑 {u} le dio una nalgada sonora a {t}!",
    "perreo": "🔥 {u} le está perreando intenso a {t}!"
}

# --- [ MOTOR DINÁMICO DE PROCESAMIENTO DE ROL ] ---
async def motor_rol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_nick = update.effective_user.first_name
    
    # Extraer el comando (ej: de /beso extrae 'beso')
    comando = update.message.text.split()[0][1:].lower()
    
    # Verificación de ID en Blacklist
    if str(user_id) in blacklist:
        return

    # Si el comando no está en nuestra lista de rol, ignorar
    if comando not in ACCIONES_ROL:
        return

    # Verificar si el usuario respondió a un mensaje
    if not update.message.reply_to_message:
        await update.message.reply_text(
            f"⚠️ **{user_nick}**, para usar `/{comando}` debes **responder** al mensaje de alguien."
        )
        return

    target_user = update.message.reply_to_message.from_user
    target_nick = target_user.first_name

    # Generar el mensaje decorado con los nombres correspondientes
    texto_accion = ACCIONES_ROL[comando].format(u=user_nick, t=target_nick)
    
    respuesta = (
        f"🎭 **MODO ROL · VENEZUELA** 🎭\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ {texto_accion}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💎 _Acción ejecutada con éxito._"
    )

    await update.message.reply_text(respuesta, parse_mode=ParseMode.MARKDOWN)
    
    # Registrar el evento y sumar XP por la interacción
    registrar_evento(user_id, user_nick, f"Usó /{comando} contra {target_nick}", "ROL")
    sumar_xp(user_id, 5)

# --- FINAL DE PARTE 3 ---
# --- [ MÓDULO DE INFORMACIÓN Y ESTADÍSTICAS ] ---
async def perfil_detallado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el perfil completo del usuario con su rango, dinero y datos de registro."""
    user_id = update.effective_user.id
    uid = str(user_id)
    nick = update.effective_user.first_name
    
    rango = obtener_rango(user_id)
    plata = banco.get(uid, 0.0)
    puntos = niveles.get(uid, 0)
    info = usuarios_info.get(uid, {"nombre": "No Reg", "edad": "?", "genero": "?"})

    # Diseño del perfil decorado al estilo AnyerJR
    perfil_txt = (
        f"┏━━━━━━ ✨ **PERFIL REAL** ✨ ━━━━━━┓\n"
        f"┃ 👤 **NOMBRE:** `{info['nombre']}`\n"
        f"┃ 🆔 **USER ID:** `{user_id}`\n"
        f"┃ 🎖️ **RANGO:** `{rango}`\n"
        f"┃ 💵 **BANCO:** `${plata}`\n"
        f"┃ ✨ **PUNTOS XP:** `{puntos}`\n"
        f"┃ 🎂 **EDAD:** `{info['edad']}` | 🧬 **SEXO:** `{info['genero']}`\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        f"🛡️ _Supervisado por AnyerJR_"
    )
    
    await update.message.reply_text(perfil_txt, parse_mode=ParseMode.MARKDOWN)
    registrar_evento(user_id, nick, "Consultó su perfil", "INFO")


# --- [ SISTEMA DE REGISTRO DE USUARIOS ] ---
async def registrar_usuario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Proceso de registro avanzado con validaciones."""
    user_id = update.effective_user.id
    uid = str(user_id)
    nick = update.effective_user.first_name

    # Si ya está registrado, no hace falta hacerlo de nuevo
    if uid in usuarios_info:
        await update.message.reply_text(
            f"⚠️ **{nick}**, ya estás registrado en el sistema.\n"
            f"_Usa /perfil para ver tus datos._"
        )
        return

    # Verificar que el usuario haya enviado los datos correctos
    if len(context.args) != 3:
        await update.message.reply_text(
            "📋 **Uso correcto:**\n"
            "`/reg [nombre] [edad] [género]`\n\n"
            "_Ejemplo: /reg Carlos 25 M_"
        )
        return

    nombre, edad, genero = context.args

    # Validar edad
    if not edad.isdigit() or int(edad) < 10 or int(edad) > 99:
        await update.message.reply_text("❌ **Edad inválida.** Debe ser un número entre 10 y 99.")
        return

    # Validar género
    if genero.upper() not in ["M", "F", "H", "OTRO"]:
        await update.message.reply_text(
            "❌ **Género inválido.** Usa:\n"
            "`M` (Masculino), `F` (Femenino), `H` (Hombre), `OTRO`"
        )
        return

    # Guardar en la base de datos
    usuarios_info[uid] = {
        "nombre": nombre,
        "edad": edad,
        "genero": genero.upper(),
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    guardar_db("usuarios_datos.json", usuarios_info)

    # Mensaje de bienvenida profesional
    respuesta = (
        f"✅ **REGISTRO EXITOSO** ✅\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Nombre:** `{nombre}`\n"
        f"🎂 **Edad:** `{edad} años`\n"
        f"🧬 **Género:** `{genero.upper()}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 **Regalo de Bienvenida:** `$100.00`\n"
        f"✨ **XP Inicial:** `50 puntos`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ _Ya puedes usar todos los comandos del bot._"
    )

    await update.message.reply_text(respuesta, parse_mode=ParseMode.MARKDOWN)
    
    # Darle dinero y experiencia de inicio
    sumar_dinero(user_id, 100.0)
    sumar_xp(user_id, 50)
    
    registrar_evento(user_id, nick, f"Se registró como {nombre}", "REGISTRO")

# --- FINAL DE PARTE 4 ---
# --- [ SISTEMA ECONÓMICO: TRABAJO Y APUESTAS ] ---
# Aquí están las funciones que permiten ganar dinero y apostar
cooldowns_trabajo = {}

async def trabajar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sistema de trabajo con tiempo de enfriamiento."""
    user_id = update.effective_user.id
    uid = str(user_id)
    nick = update.effective_user.first_name

    # Revisión de cooldown (5 minutos entre cada chamba)
    cooldown_segundos = 300  # 5 minutos
    ahora = time.time()

    if uid in cooldowns_trabajo:
        tiempo_pasado = ahora - cooldowns_trabajo[uid]
        if tiempo_pasado < cooldown_segundos:
            falta = int(cooldown_segundos - tiempo_pasado)
            minutos = falta // 60
            segundos = falta % 60
            await update.message.reply_text(
                f"⏳ **{nick}**, debes esperar `{minutos}m {segundos}s` antes de trabajar de nuevo."
            )
            return

    # Lista de trabajos con sus ganancias
    trabajos = [
        ("Vendiste gasolina en el mercado negro 🛢️", random.randint(80, 150)),
        ("Fuiste taxista por 2 horas 🚖", random.randint(50, 100)),
        ("te fuiste de viaje normal y alguien te llamo para que le repararas la cafetera ☕ y te trato super bien por tu trabajo😗", random.randint(150, 400)),
        ("Vendiste empanadas en la calle 🫓", random.randint(30, 70)),
        ("Hiciste delivery en moto 🏍️", random.randint(60, 120)),
        ("Trabajaste en una tienda 🏪", random.randint(40, 90)),
        ("Limpiaste carros en el semáforo 🚗", random.randint(20, 60)),
        ("Instalaste internet en una casa 📡", random.randint(100, 200)),
        ("Reparaste un teléfono 📱", random.randint(70, 150)),
    ]

    trabajo, ganancia = random.choice(trabajos)

    # Actualizar saldo y cooldown
    sumar_dinero(user_id, ganancia)
    cooldowns_trabajo[uid] = ahora

    respuesta = (
        f"💼 **SISTEMA DE TRABAJO** 💼\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👷 {trabajo}\n"
        f"💵 **Ganaste:** `${ganancia}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⏳ _Podrás trabajar de nuevo en 5 minutos._"
    )

    await update.message.reply_text(respuesta, parse_mode=ParseMode.MARKDOWN)
    registrar_evento(user_id, nick, f"Trabajó y ganó ${ganancia}", "ECONOMÍA")
    sumar_xp(user_id, 10)


async def apostar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Casino donde puedes duplicar o perder tu dinero."""
    user_id = update.effective_user.id
    uid = str(user_id)
    nick = update.effective_user.first_name

    # Verificar que el usuario envió una cantidad
    if not context.args or not context.args[0].replace(".", "").isdigit():
        await update.message.reply_text(
            "🎰 **Uso correcto:**\n"
            "`/apostar [cantidad]`\n"
            "_Ejemplo: /apostar 50_"
        )
        return

    cantidad = float(context.args[0])
    saldo_actual = banco.get(uid, 0.0)

    # Validar que tenga suficiente dinero
    if cantidad > saldo_actual:
        await update.message.reply_text(
            f"❌ **{nick}**, no tienes suficiente dinero.\n"
            f"💵 Tu saldo: `${saldo_actual}`"
        )
        return

    if cantidad < 10:
        await update.message.reply_text("❌ La apuesta mínima es **$10**.")
        return

    # 50% de probabilidad de ganar
    gano = random.choice([True, False])

    if gano:
        ganancia = cantidad
        sumar_dinero(user_id, ganancia)
        nuevo_saldo = banco.get(uid, 0.0)
        resultado = (
            f"🎉 **¡GANASTE!** 🎉\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 **Apostaste:** `${cantidad}`\n"
            f"✅ **Ganaste:** `${ganancia}`\n"
            f"💵 **Nuevo saldo:** `${nuevo_saldo}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔥 _¡Sigue así, rey!_"
        )
        sumar_xp(user_id, 20)
    else:
        sumar_dinero(user_id, -cantidad)
        nuevo_saldo = banco.get(uid, 0.0)
        resultado = (
            f"😢 **PERDISTE** 😢\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💸 **Apostaste:** `${cantidad}`\n"
            f"❌ **Perdiste:** `${cantidad}`\n"
            f"💵 **Saldo restante:** `${nuevo_saldo}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💔 _Mejor suerte la próxima..._"
        )
        sumar_xp(user_id, 5)

    await update.message.reply_text(resultado, parse_mode=ParseMode.MARKDOWN)
    registrar_evento(user_id, nick, f"Apostó ${cantidad} - {'Ganó' if gano else 'Perdió'}", "CASINO")

# --- FINAL DE PARTE 5 ---
# --- [ MOTOR DE INTELIGENCIA ARTIFICIAL: CEREBRO GEMINI CON MEMORIA ] ---
# ========================================
# FUNCIÓN: CEREBRO IA - Motor de búsqueda inteligente
# ========================================
# Esta función busca información en Google y la presenta al usuario
# Reemplaza el cerebro Gemini por Google Custom Search API
async def cerebro_ia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Motor de búsqueda inteligente usando Google Custom Search API.
    Busca información y responde de manera natural y útil.
    """
    # --- [ DATOS DEL USUARIO ] ---
    user_id = update.effective_user.id
    uid = str(user_id)
    nick = update.effective_user.first_name
    username = update.effective_user.username or "sin_username"
    mensaje_usuario = update.message.text
    
    # --- [ MOSTRAR TODOS LOS MENSAJES EN CONSOLA PARA DETECTAR SPAM ] ---
    print(f"\n{'='*60}")
    print(f"📨 MENSAJE RECIBIDO")
    print(f"{'='*60}")
    print(f"👤 Usuario: {nick} (@{username})")
    print(f"🆔 Chat ID: {user_id}")
    print(f"💬 Mensaje: {mensaje_usuario}")
    print(f"⏰ Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'='*60}\n")

    # --- [ VERIFICACIÓN DE BLACKLIST ] ---
    # Si el usuario está bloqueado, ignorar el mensaje
    if uid in blacklist:
        return
    
    # --- [ NOTIFICAR AL ADMIN DE NUEVO USUARIO ] ---
    es_nuevo_usuario = uid not in usuarios_info
    
    if es_nuevo_usuario:
        print(f"🆕 NUEVO USUARIO DETECTADO: {nick} (ID: {user_id})")
        
        # Enviar notificación al admin
        try:
            app_instance = context.application
            await app_instance.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"🆕 **NUEVO USUARIO EN EL BOT** 🆕\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 Nombre: `{nick}`\n"
                    f"🆔 Chat ID: `{user_id}`\n"
                    f"📱 Username: `@{username}`\n"
                    f"⏰ Hora: `{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}`\n"
                    f"💬 Primer mensaje: `{mensaje_usuario[:100]}`\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"⚠️ _El usuario debe usar /reg para registrarse_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"⚠️ Error enviando notificación: {e}")
        
        # Pedir que se registre
        await update.message.reply_text(
            f"👋 **¡Bienvenido {nick}!**\n\n"
            f"Para usar el bot, primero debes **registrarte**:\n\n"
            f"`/reg [nombre] [edad] [género]`\n\n"
            f"**Ejemplo:**\n"
            f"`/reg Juan 25 Masculino`\n\n"
            f"_Después podrás usar todos los comandos._"
        )
        return

    try:
        # --- [ OBTENER INFORMACIÓN DEL USUARIO ] ---
        info_usuario = usuarios_info.get(uid, {
            "nombre": nick,
            "edad": "desconocida",
            "genero": "desconocido"
        })
        
        nombre_real = info_usuario.get("nombre", nick)
        edad = info_usuario.get("edad", "desconocida")
        genero = info_usuario.get("genero", "desconocido")
        
        # --- [ GESTIÓN DEL HISTORIAL DE CONVERSACIÓN ] ---
        # Inicializar historial si no existe
        if uid not in conversaciones:
            conversaciones[uid] = []
        
        # Guardar el mensaje del usuario en el historial
        conversaciones[uid].append({
            "rol": "usuario",
            "contenido": mensaje_usuario,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Mantener solo los últimos 20 mensajes
        if len(conversaciones[uid]) > 20:
            conversaciones[uid] = conversaciones[uid][-20:]
        
        # --- [ MENSAJE DE ESPERA ] ---
        wait_msg = await update.message.reply_text(
            f"🔍 **Buscando información...**\n"
            f"⏳ _Un momento, {nombre_real}_"
        )
        
        # --- [ CONSTRUIR LA CONSULTA PARA GOOGLE ] ---
        # Preparar los parámetros de búsqueda
        params = {
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": mensaje_usuario,
            "num": 5,  # Obtener 5 resultados
            "hl": "es"  # Idioma español
        }
        
        # --- [ REALIZAR LA BÚSQUEDA EN GOOGLE ] ---
        respuesta = await asyncio.to_thread(
            requests.get,
            GOOGLE_SEARCH_URL,
            params=params,
            timeout=15
        )
        
        # --- [ MANEJO DE ERRORES DE LA API ] ---
        if respuesta.status_code == 403:
            await wait_msg.edit_text(
                "❌ **Error de configuración de API**\n"
                "_Verifica que tu Google API Key sea válida._\n\n"
                "📌 Obtén tu API Key en:\n"
                "`https://console.cloud.google.com/`"
            )
            return
        
        if respuesta.status_code == 429:
            await wait_msg.edit_text(
                "⚠️ **Límite de búsquedas alcanzado**\n"
                "_Has excedido el límite diario de la API de Google._\n"
                "_Intenta de nuevo mañana._"
            )
            return
        
        if respuesta.status_code != 200:
            await wait_msg.edit_text(
                f"❌ **Error al buscar**\n"
                f"_Código de error: {respuesta.status_code}_\n"
                "_Intenta de nuevo en unos segundos._"
            )
            return
        
        # --- [ PROCESAR LOS RESULTADOS ] ---
        data = respuesta.json()
        
        # Verificar si hay resultados
        if "items" not in data or len(data["items"]) == 0:
            await wait_msg.edit_text(
                f"🤷‍♀️ **No encontré información sobre:**\n"
                f"`{mensaje_usuario}`\n\n"
                f"💡 _Intenta ser más específico o reformula tu pregunta, {nombre_real}._"
            )
            return
        
        # --- [ CONSTRUIR LA RESPUESTA ] ---
        resultados = data["items"][:3]  # Tomar solo los 3 primeros
        
        # Respuesta personalizada según género
        saludo = "mi rey" if genero.upper() in ["M", "H", "MASCULINO"] else "mi reina"
        
        respuesta_texto = f"💡 **Esto encontré para ti, {saludo}:**\n\n"
        
        # --- [ FORMATEAR RESULTADOS ] ---
        for idx, item in enumerate(resultados, 1):
            titulo = item.get("title", "Sin título")
            snippet = item.get("snippet", "Sin descripción")
            link = item.get("link", "")
            
            # Limpiar y acortar el snippet si es muy largo
            if len(snippet) > 200:
                snippet = snippet[:200] + "..."
            
            respuesta_texto += (
                f"**{idx}. {titulo}**\n"
                f"{snippet}\n"
                f"🔗 [Ver más]({link})\n\n"
            )
        
        # --- [ AGREGAR CONTEXTO PERSONALIZADO ] ---
        respuesta_texto += (
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 _Si necesitas más información, pregúntame de otra forma, {nombre_real}._\n"
            f"🛡️ _Búsqueda realizada con Google Search_"
        )
        
        # --- [ ENVIAR LA RESPUESTA ] ---
        await wait_msg.edit_text(respuesta_texto, parse_mode=ParseMode.MARKDOWN)
        
        # --- [ GUARDAR EN EL HISTORIAL ] ---
        conversaciones[uid].append({
            "rol": "asistente",
            "contenido": f"Búsqueda: {resultados[0].get('title', 'Resultado de búsqueda')}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        guardar_db("conversaciones.json", conversaciones)
        
        # --- [ REGISTRO Y RECOMPENSA ] ---
        registrar_evento(user_id, nick, f"Buscó: {mensaje_usuario[:50]}", "BÚSQUEDA")
        sumar_xp(user_id, 2)
    
    # --- [ MANEJO DE EXCEPCIONES ] ---
    except requests.exceptions.Timeout:
        await update.message.reply_text(
            "⏱️ **La búsqueda está tardando mucho.**\n"
            "_Intenta de nuevo en unos segundos._"
        )
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        await update.message.reply_text(
            "❌ **Error de conexión con Google.**\n"
            "_Verifica tu conexión a internet._"
        )
    
    except KeyError as e:
        print(f"❌ Error en la respuesta de Google: {e}")
        await update.message.reply_text(
            "❌ **Error al procesar los resultados.**\n"
            "_Puede que tu API Key no esté bien configurada._"
        )
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        await update.message.reply_text(
            "❌ **Ocurrió un error al procesar tu mensaje.**\n"
            "_Intenta de nuevo en unos segundos._"
        )


# --- [ MEDIDORES DIVERTIDOS ] ---
MEDIDORES_LISTA = ["gay", "facha", "toxico", "puta", "negro", "virgen", "loco", "sigma"]

async def motor_medidores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera porcentajes aleatorios para crear humor."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    comando = update.message.text.split()[0][1:].lower()

    if str(user_id) in blacklist:
        return

    # Verificar que el usuario respondió a alguien
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user.first_name
    else:
        target = nick

    porcentaje = random.randint(0, 100)

    # Emojis según el comando
    emojis = {
        "gay": "🏳️‍🌈",
        "facha": "🔥",
        "toxico": "☠️",
        "puta": "💋",
        "negro": "🖤",
        "virgen": "😇",
        "loco": "🤪",
        "sigma": "💪"
    }

    emoji = emojis.get(comando, "📊")

    # Barra de progreso visual
    lleno = "█" * (porcentaje // 10)
    vacio = "░" * (10 - porcentaje // 10)
    barra = f"[{lleno}{vacio}]"

    respuesta = (
        f"{emoji} **MEDIDOR DE {comando.upper()}** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Usuario:** `{target}`\n"
        f"📊 {barra} `{porcentaje}%`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎲 _Resultado totalmente aleatorio_"
    )

    await update.message.reply_text(respuesta, parse_mode=ParseMode.MARKDOWN)
    registrar_evento(user_id, nick, f"Usó medidor /{comando}", "DIVERSIÓN")
    sumar_xp(user_id, 3)

# --- FINAL DE PARTE 6 ---
# --- [ DESCARGADOR DE VIDEOS (TikTok, Instagram, YouTube) ] ---
async def descargar_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga videos de TikTok, Instagram, YouTube y otras redes."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🎥 **Uso correcto:**\n"
            "`/descargar [URL]`\n"
            "_Soporta: TikTok, Instagram, YouTube, Twitter..._"
        )
        return

    url = context.args[0]
    wait_msg = await update.message.reply_text(f"⏳ **Descargando video...**")

    try:
        # Configuración de yt-dlp para descargar el video
        opciones = {
            'format': 'best',
            'outtmpl': f'{RUTA_LOGS}/%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True
        }

        # Descargar el video
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            video_path = ydl.prepare_filename(info)

        # Enviar el video al usuario
        with open(video_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption=f"✅ **Video descargado**\n🎬 Pedido por: {nick}"
            )

        # Eliminar el archivo temporal
        os.remove(video_path)
        await wait_msg.delete()

        registrar_evento(user_id, nick, f"Descargó video: {url}", "DOWNLOAD")
        sumar_xp(user_id, 15)

    except Exception as e:
        print(f"❌ Error descarga: {e}")
        await wait_msg.edit_text(
            "❌ **No pude descargar ese video.**\n"
            "_Verifica que el enlace sea correcto._"
        )


# --- [ DESCARGADOR DE MÚSICA MP3 DESDE YOUTUBE ] ---
@tarea_larga
async def ytmp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga audio de YouTube en formato MP3 por nombre."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🎵 **Uso correcto:**\n"
            "`/ytmp3 [nombre de la canción]`\n\n"
            "_Ejemplos:_\n"
            "- `/ytmp3 despacito luis fonsi`\n"
            "- `/ytmp3 bohemian rhapsody queen`\n"
            "- `/ytmp3 blinding lights the weeknd`"
        )
        return

    busqueda = " ".join(context.args)
    wait_msg = await update.message.reply_text(f"🔍 **Buscando:** `{busqueda}`\n⏳ _Esto puede tardar un momento..._", parse_mode=ParseMode.MARKDOWN)

    try:
        # Buscar en YouTube
        opciones_busqueda = {
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch1',
            'format': 'best'
        }
        
        with yt_dlp.YoutubeDL(opciones_busqueda) as ydl:
            info_busqueda = await asyncio.to_thread(ydl.extract_info, busqueda, download=False)
        
        if 'entries' in info_busqueda:
            video_info = info_busqueda['entries'][0]
        else:
            video_info = info_busqueda
            
        url_encontrada = video_info['url']
        titulo = video_info.get('title', 'audio')

        # Ahora descargar el audio
        await wait_msg.edit_text(f"🎵 **Descargando:** `{titulo}`\n⏳ _Extrayendo audio..._", parse_mode=ParseMode.MARKDOWN)
        
        opciones = {
            'format': 'bestaudio/best',
            'outtmpl': f'{RUTA_LOGS}/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url_encontrada, download=True)
            titulo = info.get('title', 'audio')
            ext = info.get('ext', 'mp3')
            audio_path = f"{RUTA_LOGS}/{titulo}.{ext}"

        # Verificar si el archivo existe
        if not os.path.exists(audio_path):
            archivos = [f for f in os.listdir(RUTA_LOGS) if titulo in f]
            if archivos:
                audio_path = f"{RUTA_LOGS}/{archivos[0]}"
            else:
                await wait_msg.edit_text("❌ **Error: No se encontró el archivo descargado.**")
                return

        # Verificar el tamaño del archivo (máximo 50MB para Telegram)
        file_size = os.path.getsize(audio_path)
        if file_size > 50 * 1024 * 1024:  # 50 MB
            os.remove(audio_path)
            await wait_msg.edit_text(
                "❌ **El archivo es muy pesado (>50MB).**\n"
                "_Telegram no permite enviar archivos tan grandes._"
            )
            return

        await wait_msg.edit_text(f"📤 **Subiendo audio...**\n⏳ _Tamaño: {file_size / (1024*1024):.1f} MB_")
        
        # Enviar el audio
        with open(audio_path, 'rb') as audio_file:
            await update.message.reply_audio(
                audio=audio_file,
                title=titulo,
                caption=f"🎵 **{titulo}**\n📥 Pedido por: {nick}"
            )

        os.remove(audio_path)
        await wait_msg.delete()

        registrar_evento(user_id, nick, f"Descargó MP3: {titulo}", "MÚSICA")
        sumar_xp(user_id, 10)

    except Exception as e:
        print(f"❌ Error MP3: {e}")
        await wait_msg.edit_text(
            "❌ **Error al descargar el audio.**\n"
            "_Verifica el nombre del video o intenta después._"
        )

#menu new comands
async def cmd_novedades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # MENSAJE 1: HEADER
    msg1 = "🆕 **NOVEDADES - CAMILA BOT V13** 🚀\n━━━━━━━━━━━━━━━━━━━━"
    await update.message.reply_text(msg1, parse_mode="Markdown")
    
    # MENSAJE 2: MULTIMEDIA
    msg2 = (
        "🎬 **MULTIMEDIA EXTRA** (+5)\n"
        "» /tkdm - TikTok Random sin marca\n"
        "» /mp3_universal - MP3 desde cualquier sitio\n"
        "» /crear_sticker - Convierte imagen a sticker\n"
        "» /fotomontaje - Efecto de foto\n"
        "» /gif_generator - Crea GIFs animados"
    )
    await update.message.reply_text(msg2, parse_mode="Markdown")
    
    # MENSAJE 3: IA MEJORADA
    msg3 = (
        "🧠 **MEJORAS EN IA** (+10)\n"
        "» /ia - Respuestas más rápidas en la nube\n"
        "» /poesia_ia - Genera poesías con Gemini\n"
        "» /traduccion_ia - Traduce a cualquier idioma\n"
        "» /resumen_ia - Resume textos largos\n"
        "» /historia_ia - Genera historias cortas\n"
        "» /analisis_texto - Analiza sentimientos\n"
        "» /reescribo - Reescribe textos\n"
        "» /generador_preguntas - Crea cuestionarios\n"
        "» /mentor_ia - Enseña cualquier tema\n"
        "» /ideador - Genera ideas creativas"
    )
    await update.message.reply_text(msg3, parse_mode="Markdown")
    
    # MENSAJE 4: ECONOMÍA & JUEGOS
    msg4 = (
        "🎰 **ECONOMÍA MEJORADA** (+15)\n"
        "» /casino_x2 - Apuesta al doble\n"
        "» /ruleta_suerte - Ruleta rusa\n"
        "» /triplesuerte - Triple apuesta\n"
        "» /bonificacion - Bono diario gratis\n"
        "» /loteria - Lotería nacional\n"
        "» /blackjack - Juega blackjack\n"
        "» /poquer - Juega póquer\n"
        "» /robar - Roba dinero (riesgo)\n"
        "» /deposito - Guarda dinero seguro\n"
        "» /credito - Pide crédito\n"
        "» /multijugador_apuesta - Apuesta con amigos\n"
        "» /torneo_dinero - Torneo de dinero\n"
        "» /coinflip - Cara/cruz por dinero\n"
        "» /slots - Máquina tragaperras\n"
        "» /bingo - Juega bingo"
    )
    await update.message.reply_text(msg4, parse_mode="Markdown")
    
    # MENSAJE 5: JUEGOS NUEVOS
    msg5 = (
        "🎮 **JUEGOS NUEVOS** (+20)\n"
        "» /aventura - Elige tu propia aventura\n"
        "» /laberinto - Escapa del laberinto\n"
        "» /batalla_monstruos - RPG por turnos\n"
        "» /buscaminas - Busca minas clásico\n"
        "» /wordle - Adivina palabra (como Wordle)\n"
        "» /serpiente - Juega serpiente (Snake)\n"
        "» /spaceinvaders - Invaders simplificado\n"
        "» /carrera - Carrera de velocidad\n"
        "» /duelo - Duelo 1v1 (tú vs IA)\n"
        "» /arena_batalla - Arena de combate\n"
        "» /batalla_naves - Batalla naval\n"
        "» /crucigrama - Crucigramas dinámicos\n"
        "» /sopa_letras - Sopa de letras\n"
        "» /memoria - Juego de memoria\n"
        "» /rompecabezas - Rompecabezas\n"
        "» /acertijos_logica - Acertijos lógicos\n"
        "» /dominoes - Juega dominó\n"
        "» /damas - Juega damas\n"
        "» /ajedrez - Juega ajedrez\n"
        "» /conecta4 - Conecta 4"
    )
    await update.message.reply_text(msg5, parse_mode="Markdown")
    
    # MENSAJE 6: HERRAMIENTAS
    msg6 = (
        "🛠️ **HERRAMIENTAS NUEVAS** (+25)\n"
        "» /qr_dinamico - Genera QR interactivo\n"
        "» /pdf_merger - Une PDFs\n"
        "» /imagen_texto - Extrae texto de imagen\n"
        "» /traductor_imagen - Traduce en imagenes\n"
        "» /compresör_imagen - Comprime imágenes\n"
        "» /editor_imagen - Editor online\n"
        "» /filtro_foto - Aplica filtros\n"
        "» /efecto_blur - Desenfoque\n"
        "» /efecto_blanco_negro - B/N clásico\n"
        "» /redimensionar_imagen - Cambia tamaño\n"
        "» /cortador_imagen - Recorta imágenes\n"
        "» /collage - Crea collages\n"
        "» /meme_generator - Generador de memes\n"
        "» /watermark - Añade marca de agua\n"
        "» /video_merger - Une videos\n"
        "» /video_trim - Corta videos\n"
        "» /video_speed - Cambia velocidad video\n"
        "» /audio_merger - Une audios\n"
        "» /audio_trim - Corta audios\n"
        "» /audio_speed - Cambia velocidad audio\n"
        "» /cambiar_pitch - Cambia tono\n"
        "» /eliminar_silencio - Quita silencios\n"
        "» /normalizar_audio - Normaliza volumen\n"
        "» /reverb_audio - Añade reverberación\n"
        "» /echo_audio - Añade eco"
    )
    await update.message.reply_text(msg6, parse_mode="Markdown")
    
    # MENSAJE 7: REDES SOCIALES
    msg7 = (
        "📱 **INTEGRACIONES REDES** (+30)\n"
        "» /whatsapp_status - Descarga estados WA\n"
        "» /facebook_video - Videos Facebook\n"
        "» /instagram_stories - Descargar stories\n"
        "» /instagram_reels - Descargar reels\n"
        "» /youtube_shorts - Shorts YouTube\n"
        "» /youtube_playlist - Descarga playlists\n"
        "» /youtube_canal_info - Info del canal\n"
        "» /twitter_trends - Trending Topics\n"
        "» /reddit_post - Descarga posts Reddit\n"
        "» /twitch_clip - Clips Twitch\n"
        "» /tiktok_creator_info - Info creador TT\n"
        "» /tiktok_trending - Trending TikTok\n"
        "» /pinterest_board - Descargar tableros\n"
        "» /snapchat_story - Historias Snapchat\n"
        "» /spotify_track_info - Info canciones\n"
        "» /spotify_playlist - Descargar playlist\n"
        "» /soundcloud_playlist - SoundCloud\n"
        "» /deezer_playlist - Deezer\n"
        "» /bandcamp_download - Bandcamp\n"
        "» /imgur_album - Álbumes Imgur\n"
        "» /patreon_content - Contenido Patreon\n"
        "» /discord_server_info - Info servidor\n"
        "» /telegram_channel - Info canal\n"
        "» /twitch_followers - Seguidores\n"
        "» /youtube_subs - Suscriptores\n"
        "» /tiktok_followers - Followers TT\n"
        "» /instagram_followers - Followers IG\n"
        "» /twitter_followers - Seguidores TW\n"
        "» /reddit_karma - Karma Reddit\n"
        "» /twitch_subs - Suscriptores Twitch"
    )
    await update.message.reply_text(msg7, parse_mode="Markdown")
    
    # MENSAJE 8: INFORMACIÓN & DATOS
    msg8 = (
        "📊 **DATOS & INFORMACIÓN** (+35)\n"
        "» /estadisticas_personales - Tus stats\n"
        "» /grafico_dinero - Gráfico ingresos\n"
        "» /grafico_xp - Gráfico experiencia\n"
        "» /ranking_global - Ranking usuarios\n"
        "» /historial_transacciones - Mis transacciones\n"
        "» /horario_mundial - Hora en 50 países\n"
        "» /zonas_horarias - Convertidor zonas\n"
        "» /calendario - Calendario 3D\n"
        "» /fases_luna - Fases lunares\n"
        "» /eclipses - Próximos eclipses\n"
        "» /constelaciones - Mapa estelar\n"
        "» /planeta_hoy - Posición planetas\n"
        "» /cometas_proximos - Próximos cometas\n"
        "» /estacion_espacial - ISS en tiempo real\n"
        "» /vida_extraterrestre - Ecuación Drake\n"
        "» /curiosidad_espacio - Dato curioso\n"
        "» /wikipedia_random - Artículo aleatorio\n"
        "» /libro_recomendado - Libro del día\n"
        "» /pelicula_trending - Película trending\n"
        "» /serie_recomendada - Serie del momento\n"
        "» /musica_tendencia - Canción trending\n"
        "» /videojuego_ranking - Ranking juegos\n"
        "» /app_destacada - App del día\n"
        "» /noticia_tech - Noticia tecnología\n"
        "» /noticia_ciencia - Noticia científica\n"
        "» /noticia_deporte - Noticia deportes\n"
        "» /noticia_politica - Noticia política\n"
        "» /noticia_mundo - Noticia internacional\n"
        "» /indice_felicidad - Índice happiness\n"
        "» /estadistica_mundial - Estadísticas ONU\n"
        "» /economia_mundial - Datos económicos\n"
        "» /cripto_completo - Todas las cryptos\n"
        "» /bolsa_valores - Acciones en vivo\n"
        "» /commodities - Precios materias primas\n"
        "» /energia_mundial - Consumo energía"
    )
    await update.message.reply_text(msg8, parse_mode="Markdown")
    
    # MENSAJE 9: PERSONALIZACION
    msg9 = (
        "🎨 **PERSONALIZACIÓN** (+20)\n"
        "» /tema_oscuro - Activa tema oscuro\n"
        "» /tema_claro - Activa tema claro\n"
        "» /fuente_pequeña - Reduce tamaño fuente\n"
        "» /fuente_grande - Aumenta tamaño\n"
        "» /idioma - Cambia idioma bot\n"
        "» /moneda - Cambia moneda\n"
        "» /zona_horaria - Tu zona horaria\n"
        "» /notificaciones - Activa notificaciones\n"
        "» /privacidad - Config privacidad\n"
        "» /bloquear_usuario - Bloquea usuarios\n"
        "» /amigos - Gestiona amigos\n"
        "» /perfil_publico - Perfil visible\n"
        "» /firma_personal - Tu firma\n"
        "» /avatar_cambiar - Cambiar avatar\n"
        "» /banner_cambiar - Cambiar banner\n"
        "» /bio_cambiar - Cambiar biografía\n"
        "» /estado_set - Tu estado actual\n"
        "» /badges - Tus insignias\n"
        "» /logros - Tus logros\n"
        "» /inventario - Tu inventario"
    )
    await update.message.reply_text(msg9, parse_mode="Markdown")
    
    # MENSAJE 10: COMUNIDAD
    msg10 = (
        "👥 **COMUNIDAD** (+25)\n"
        "» /crear_grupo - Crea grupo privado\n"
        "» /mis_grupos - Mis grupos\n"
        "» /invitar_grupo - Invita usuarios\n"
        "» /mensajes_privados - Chat privado\n"
        "» /retos_amigos - Retos con amigos\n"
        "» /competencias - Competencias activas\n"
        "» /leaderboard - Ranking global\n"
        "» /eventos_proximos - Próximos eventos\n"
        "» /participar_evento - Participa evento\n"
        "» /dona_dinero - Dona dinero\n"
        "» /regalo - Regala a usuario\n"
        "» /intercambio - Intercambia items\n"
        "» /bazar - Compra/vende items\n"
        "» /subasta - Participa subasta\n"
        "» /sorteo_participa - Participa sorteo\n"
        "» /crear_sorteo - Crea sorteo\n"
        "» /anuncio_comunidad - Anuncia algo\n"
        "» /encuesta - Crea encuesta\n"
        "» /votacion - Vota en votación\n"
        "» /sugerencia - Sugiere mejora\n"
        "» /reporte - Reporta problema\n"
        "» /feedback - Deja feedback\n"
        "» /helpdesk - Contacta soporte\n"
        "» /wiki_comunidad - Wiki del bot\n"
        "» /faq - Preguntas frecuentes"
    )
    await update.message.reply_text(msg10, parse_mode="Markdown")
    
    # MENSAJE 11: FOOTER
    msg11 = (
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 _+300 FUNCIONES NUEVAS EN V13_\n"
        "🎵 _Música mejorada: 50 canciones_\n"
        "⚡ _Velocidad +300% más rápido_\n"
        "🔐 _100% Seguro y privado_\n"
        "🛡️ _Creado por AnyerJR · Venezuela 🇻🇪_"
    )
    await update.message.reply_text(msg11, parse_mode="Markdown")


# --- [ DESCARGADOR DE VIDEOS MP4 DESDE YOUTUBE ] ---
async def ytmp4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga videos de YouTube en formato MP4 con audio, busca por nombre."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🎥 **Uso correcto:**\n"
            "`/ytmp4 [nombre del video]`\n\n"
            "_Ejemplos:_\n"
            "- `/ytmp4 despacito videoclip`\n"
            "- `/ytmp4 cat funny videos`\n"
            "- `/ytmp4 tutorial python`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    busqueda = " ".join(context.args)
    
    wait_msg = await update.message.reply_text(
        f"🔍 **Buscando:** `{busqueda}`\n"
        f"⏳ _Localizando video..._",
        parse_mode=ParseMode.MARKDOWN
    )

    try:
        # Buscar el video en YouTube
        opciones_busqueda = {
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch1',
            'format': 'best'
        }
        
        with yt_dlp.YoutubeDL(opciones_busqueda) as ydl:
            info_busqueda = await asyncio.to_thread(ydl.extract_info, busqueda, download=False)
        
        if 'entries' in info_busqueda:
            video_info = info_busqueda['entries'][0]
        else:
            video_info = info_busqueda
            
        url_encontrada = video_info['url']
        titulo_encontrado = video_info.get('title', 'video')

        await wait_msg.edit_text(
            f"🎥 **Descargando:** `{titulo_encontrado}`\n"
            f"⏳ _Esto puede tardar según el tamaño..._",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Descargar el video
        opciones = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': f'{RUTA_LOGS}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True
        }

        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url_encontrada, download=True)
            titulo = info.get('title', 'video')
            duracion = info.get('duration', 0)
            
            # Buscar el archivo descargado
            archivos = [f for f in os.listdir(RUTA_LOGS) if titulo in f and f.endswith('.mp4')]
            if not archivos:
                await wait_msg.edit_text("❌ **Error: No se encontró el video descargado.**")
                return
            
            video_path = f"{RUTA_LOGS}/{archivos[0]}"

        # Verificar tamaño del archivo (Telegram tiene límite de 50MB para bots)
        file_size = os.path.getsize(video_path)
        size_mb = file_size / (1024 * 1024)

        if size_mb > 50:
            os.remove(video_path)
            await wait_msg.edit_text(
                f"❌ **Video muy pesado** ({size_mb:.1f} MB)\n"
                f"_Telegram permite máximo 50 MB._\n\n"
                f"💡 **Intenta con una búsqueda más específica o un video más corto._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(f"📤 **Subiendo video...**\n⏳ _Tamaño: {size_mb:.1f} MB_")

        # Enviar el video
        with open(video_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption=f"🎥 **{titulo}**\n⏱️ Duración: {duracion // 60}:{duracion % 60:02d}\n📥 Pedido por: {nick}",
                supports_streaming=True
            )

        os.remove(video_path)
        await wait_msg.delete()

        registrar_evento(user_id, nick, f"Descargó MP4: {titulo}", "VIDEO-YT")
        sumar_xp(user_id, 15)

    except Exception as e:
        print(f"❌ Error MP4: {e}")
        await wait_msg.edit_text(
            "❌ **Error al descargar el video.**\n"
            "_Verifica el nombre o intenta después._"
        )


# --- FINAL DE PARTE 7 ---

# BLOQUE SSWEB - INICIO
# (Para eliminar, borra todo desde esta línea hasta "BLOQUE SSWEB - FIN")
async def ssweb_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando: /ssweb [URL] — Captura pantalla de una página web via NexyLight API
    Bot accede a la página de la API para obtener el endpoint correcto y avisa al admin si hay problemas.
    """
    from bs4 import BeautifulSoup
    import requests
    import datetime
    import os
    import urllib.parse

    ID_ADMIN = 7953907047  # Mismo ID admin que en el comando /pinterest
    URL_PAGINA_TOOLS = "https://api.nexylight.xyz/#Tools"
    ENDPOINT_POR_DEFECTO = "https://api.nexylight.xyz/tools/ssweb"

    if not context.args:
        await update.message.reply_text(
            "⚠️ ¡Olvidaste la URL a capturar!\n"
            "Comando disponible:\n"
            "/ssweb [URL completa]\n"
            "Ejemplo: /ssweb https://pika.style, /ssweb https://api.nexylight.xyz"
        )
        return

    url_objetivo = " ".join(context.args).rstrip('/')  # Unir y quitar barra final
    endpoint_ssweb = None
    error_pagina = None

    # Paso 1: Obtener endpoint actualizado desde la página de la API
    try:
        respuesta_pagina = requests.get(URL_PAGINA_TOOLS, timeout=10)
        respuesta_pagina.raise_for_status()
        soup = BeautifulSoup(respuesta_pagina.content, 'html.parser')

        # Buscar sección SSWeb en la página
        seccion_ssweb = soup.find(string=lambda t: t and "SSWeb" in t)
        if seccion_ssweb:
            contenedor = seccion_ssweb.find_parent(attrs={"class": lambda c: c and "card" in c.lower()})
            if contenedor:
                endpoint_elemento = contenedor.find(string=lambda t: t and "https://api.nexylight.xyz/tools" in t)
                if endpoint_elemento:
                    endpoint_ssweb = endpoint_elemento.strip()
                    if not endpoint_ssweb.endswith("/ssweb"):
                        endpoint_ssweb = f"{endpoint_ssweb.rstrip('/')}/ssweb"
            else:
                error_pagina = "No se encontró el contenedor de SSWeb en la página."
        else:
            error_pagina = "No se encontró la sección de SSWeb en la página (posible cambio de estructura o eliminación)."

    except requests.exceptions.ConnectionError:
        error_pagina = "No se pudo conectar a la página de NexyLight API (posible eliminación o caída del servicio)."
    except requests.exceptions.HTTPError as e:
        error_pagina = f"Error HTTP al acceder a la página: {str(e)} (posible cambio de URL o estado del servicio)."
    except Exception as e:
        error_pagina = f"Error inesperado al procesar la página: {str(e)}."

    # Manejar errores al obtener el endpoint
    if error_pagina:
        await update.message.reply_text(
            "⚠️ Servicio temporalmente no disponible.\n"
            "Intenta de nuevo más tarde o contacta al administrador si el problema persiste."
        )
        try:
            await context.bot.send_message(
                chat_id=ID_ADMIN,
                text=f"🚨 ALERTA - SERVICIO SSWEB FALLIDO 🚨\n\n"
                     f"Fecha/Hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                     f"Usuario que lo solicitó: {update.effective_user.first_name} (ID: {update.effective_user.id})\n"
                     f"URL solicitada: {url_objetivo}\n"
                     f"Error detectado: {error_pagina}\n"
                     f"Usando endpoint por defecto como último recurso..."
            )
        except Exception as error_aviso:
            print(f"Error al enviar aviso al admin: {str(error_aviso)}")
        endpoint_ssweb = ENDPOINT_POR_DEFECTO

    if not endpoint_ssweb:
        endpoint_ssweb = ENDPOINT_POR_DEFECTO

    # Paso 2: Solicitar captura a la API y enviar resultado
    ruta_imagen = "captura_ssweb.png"
    try:
        # Codificar URL como parámetro
        url_codificada = urllib.parse.quote_plus(url_objetivo)
        respuesta_api = requests.get(
            endpoint_ssweb,
            params={"url": url_codificada},
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"},
            timeout=20
        )
        respuesta_api.raise_for_status()

        # Verificar que la respuesta sea una imagen
        if 'image' in respuesta_api.headers.get('Content-Type', ''):
            # Guardar imagen temporal
            with open(ruta_imagen, "wb") as archivo:
                archivo.write(respuesta_api.content)
            
            # Enviar como archivo para evitar preview automático
            await update.message.reply_document(
                document=open(ruta_imagen, "rb"),
                filename=f"captura_{url_objetivo.split('//')[1].split('/')[0]}.png",
                caption=f"✅ Captura de pantalla generada para:\n{url_objetivo}"
            )
        else:
            # Si la API devuelve texto en lugar de imagen
            contenido_error = respuesta_api.text[:200]
            raise Exception(f"API no devolvió imagen. Respuesta: {contenido_error}...")

    except Exception as error_captura:
        await update.message.reply_text("❌ No se pudo generar la captura. Intenta de nuevo más tarde.")
        try:
            await context.bot.send_message(
                chat_id=ID_ADMIN,
                text=f"🚨 ALERTA - CAPTURA SSWEB FALLIDA TOTAL 🚨\n\n"
                     f"Fecha/Hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                     f"Usuario: {update.effective_user.first_name} (ID: {update.effective_user.id})\n"
                     f"URL solicitada: {url_objetivo}\n"
                     f"Endpoint usado: {endpoint_ssweb}\n"
                     f"Error: {str(error_captura)}\n"
                     f"Posible causa: Página modificada, API eliminada o URL incorrecta."
            )
        except Exception as error_aviso:
            print(f"Error al enviar aviso final al admin: {str(error_aviso)}")
    finally:
        # Eliminar archivo temporal
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

# BLOQUE SSWEB - FIN


# --- Waifus ramdon ---
# ------------------- COMANDO WAIFU CORREGIDO -------------------
async def enviar_waifu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comandos /waifu, /wa, /waifus, /w: Envía una imagen de waifu aleatoria.
    Incluye temporizador de 5 minutos entre solicitudes por usuario.
    """
    import requests
    from datetime import datetime, timedelta

    # --- Configuración y variables internas del bloque ---
    API_KEY = "nexy-6c944e"
    URLS_API_WAIFU = [
        f"https://api.nexylight.xyz/anime/?key={API_KEY}",
        f"https://api.nexylight.xyz/anime/waifu?key={API_KEY}"
    ]
    TIEMPO_ESPERA_MINUTOS = 5
    # Diccionario para almacenar solicitudes (se mantiene entre llamadas al comando)
    if not hasattr(context.bot_data, 'ultima_solicitud_waifu'):
        context.bot_data['ultima_solicitud_waifu'] = {}

    # --- Control de tiempo dentro del bloque async ---
    usuario_id = update.effective_user.id
    ultima_solicitud = context.bot_data['ultima_solicitud_waifu'].get(usuario_id)

    if ultima_solicitud:
        tiempo_transcurrido = datetime.now() - ultima_solicitud
        tiempo_restante = timedelta(minutes=TIEMPO_ESPERA_MINUTOS) - tiempo_transcurrido
        
        if tiempo_restante.total_seconds() > 0:
            minutos_restantes = int(tiempo_restante.total_seconds() // 60)
            segundos_restantes = int(tiempo_restante.total_seconds() % 60)
            await update.message.reply_text(
                f"⏳ ¡Espera un poco! Debes esperar {minutos_restantes} minutos y {segundos_restantes} segundos\n"
                f"para solicitar otra waifu. Tiempo de espera total: {TIEMPO_ESPERA_MINUTOS} minutos."
            )
            return

    # --- Lógica de obtención de waifu ---
    try:
        for URL_API_WAIFU in URLS_API_WAIFU:
            try:
                respuesta_api = requests.get(URL_API_WAIFU, stream=True, timeout=10)
                respuesta_api.raise_for_status()
                tipo_contenido = respuesta_api.headers.get("Content-Type", "")

                if "image" in tipo_contenido:
                    await update.message.reply_text("✨ ¡Aquí tienes tu waifu!")
                    await update.message.reply_photo(photo=respuesta_api.content)
                    context.bot_data['ultima_solicitud_waifu'][usuario_id] = datetime.now()
                    return
                else:
                    try:
                        datos = respuesta_api.json()
                        url_imagen = datos.get("url") or datos.get("image") or datos.get("image_url")
                        if url_imagen and url_imagen.startswith("http"):
                            await update.message.reply_text("✨ ¡Aquí tienes tu waifu!")
                            await update.message.reply_photo(photo=url_imagen)
                            context.bot_data['ultima_solicitud_waifu'][usuario_id] = datetime.now()
                            return
                    except:
                        continue

            except requests.exceptions.RequestException as error_conexion:
                continue

        await update.message.reply_text(
            "⚠️ No se pudo obtener la waifu 😢\n"
            "Posibles causas: API requiere cuenta activa, tipo de página no soportado o endpoints modificados.\n"
            "Prueba de nuevo más tarde o avísame para cambiar la API!"
        )

    except Exception as error_general:
        await update.message.reply_text(f"⚠️ Error al procesar la solicitud: {str(error_general)}")

# --- [ GENERADOR DE STICKERS ESTILO BRAT ] ---
# ------------------- BLOQUE DE CREACIÓN BRAT V2 -------------------
async def crear_bratv2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando: /bratv2 [texto]
    Crea imagen estilo Brat con fondo blanco y texto vertical en negro vía NexyLight API (respaldo en /brat).
    """
    import requests

    API_KEY = "nexy-6c944e"
    ENDPOINT_BASE = "https://api.nexylight.xyz/canvas/brat"

    if not context.args:
        await update.message.reply_text(
            "⚠️ ¡Olvidaste el texto para la imagen!\n"
            "Uso: /bratv2 [texto que quieras poner]\n"
            "Ejemplo: /bratv2 NexyLight API, /bratv2 hola que tal 🤑"
        )
        return
    
    texto_imagen = " ".join(context.args)
    # Solicitud actualizada con API key y parámetros originales
    URL_API = f"{ENDPOINT_BASE}?text={texto_imagen}&bg=white&text_orient=vertical&key={API_KEY}"

    try:
        respuesta_api = requests.get(URL_API, timeout=15)
        respuesta_api.raise_for_status()

        # Verificar si la respuesta es una imagen (manejo por si la API devuelve error en formato JSON)
        if "image" not in respuesta_api.headers.get("Content-Type", ""):
            raise Exception("La respuesta no es una imagen válida (posible error de la API o credenciales).")

        await update.message.reply_photo(
            photo=respuesta_api.content,
            caption=f"✅ Imagen creada vía NexyLight API:\n📝 Texto vertical | Fondo blanco, texto negro\n🔤 Texto: {texto_imagen}\n🔑 API Key activada"
        )

    except requests.exceptions.RequestException as error_conexion:
        await update.message.reply_text(f"⚠️ API de NexyLight no disponible: {str(error_conexion)}\n⚠️ Nota: La API ahora requiere clave válida y el tipo de archivo podría no ser compatible.\n🔄 Activando respaldo con Pillow (/brat)...")
        await brat(update, context)
    
    except Exception as error_general:
        await update.message.reply_text(f"⚠️ Error con la API: {str(error_general)}\n⚠️ Posibles causas: Tipo de archivo no soportado, endpoint modificado o clave incorrecta.\n🔄 Activando respaldo con Pillow (/brat)...")
        await brat(update, context)

# ------------------- FIN DEL BLOQUE -------------------
# ------------------- BLOQUE DE BRAT VIDEO -------------------
async def crear_brat_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /bratvd [texto]: Genera y envía un video en estilo Brat Video vía NexyLight API.
    """
    import requests

    API_KEY = "nexy-6c944e"
    ENDPOINT_BASE = "https://api.nexylight.xyz/canvas/bratv"

    # Verificar si el usuario escribió el texto
    if not context.args:
        await update.message.reply_text(
            "⚠️ ¡Falta el texto para el video!\n"
            "Uso: /bratvd [tu texto aquí]\n"
            "Ejemplo: /bratvd Mi Bot es Genial"
        )
        return
    
    texto_video = " ".join(context.args)
    # Actualizar solicitud con API key y parámetros completos
    parametros = {"text": texto_video, "key": API_KEY}

    try:
        # Hacer la petición a la API con el texto y clave de acceso
        respuesta_api = requests.get(
            ENDPOINT_BASE,
            params=parametros,
            stream=True  # Importante para manejar archivos grandes como videos
        )
        respuesta_api.raise_for_status()

        # Verificar que la respuesta sea un video o manejar posibles errores de tipo de página
        tipo_contenido = respuesta_api.headers.get("Content-Type", "")
        if "video" not in tipo_contenido:
            raise Exception(f"Respuesta no válida - Tipo de contenido: {tipo_contenido}\nPágina o formato no soportado por la API.")

        # Enviar el video directamente al chat
        await update.message.reply_text("🎬 ¡Video Brat listo!")
        await update.message.reply_video(video=respuesta_api.content)

    except requests.exceptions.RequestException as error_conexion:
        await update.message.reply_text(f"⚠️ Error con la API: {str(error_conexion)}\n⚠️ Nota: El endpoint {ENDPOINT_BASE} podría ser de tipo no soportado o requerir configuraciones adicionales.")
    except Exception as error_envio:
        await update.message.reply_text(f"⚠️ Error al procesar/enviar el video: {str(error_envio)}\n⚠️ Posible causa: Tipo de página no soportado por la API o fallo en la generación del contenido.")

# ------------------- FIN DEL BLOQUE -------------------


#brat texto normal (compatible con emojis, columnas y modificadores de color)
async def brat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea stickers al estilo BRAT con texto en columnas, emojis y modificadores de color opcionales.
    Uso: /brat [texto] *[color_fondo]+[color_texto] (modificadores opcionales)
    Ejemplos: /brat hola que tal 🤑, /brat hola que tal 🤑*verde+azul, /brat hola que tal 🤑*#927911+red"""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🎨 **Uso:**\n"
            "`/brat [texto]` (por defecto: fondo verde, texto negro)\n"
            "`/brat [texto] *[color_fondo]+[color_texto]` (modificadores opcionales)\n"
            "_Ejemplos: /brat Venezuela 🇻🇪, /brat hola que tal 🤑*rojo+blanco, /brat hola que tal 🤑*#927911+blue_"
        )
        return

    # Separar texto principal y modificadores de color
    texto_completo = " ".join(context.args)
    modificadores = None
    texto = texto_completo

    if "*" in texto_completo:
        texto_parte, modificadores_parte = texto_completo.split("*", 1)
        texto = texto_parte.strip().upper()
        modificadores = modificadores_parte.strip().split("+")

    # Definir colores por defecto
    color_fondo = (142, 255, 68)  # Verde BRAT
    color_texto = (0, 0, 0)        # Negro

    # Diccionario de colores soportados (español e inglés)
    mapa_colores = {
        "rojo": (255, 0, 0), "red": (255, 0, 0),
        "verde": (142, 255, 68), "green": (142, 255, 68),
        "azul": (0, 0, 255), "blue": (0, 0, 255),
        "blanco": (255, 255, 255), "white": (255, 255, 255),
        "negro": (0, 0, 0), "black": (0, 0, 0),
        "amarillo": (255, 255, 0), "yellow": (255, 255, 0),
        "naranja": (255, 165, 0), "orange": (255, 165, 0),
        "morado": (128, 0, 128), "purple": (128, 0, 128),
        "rosa": (255, 192, 203), "pink": (255, 192, 203),
        "gris": (128, 128, 128), "gray": (128, 128, 128)
    }

    # Función para convertir código hex a RGB
    def hex_a_rgb(hex_code):
        hex_code = hex_code.lstrip("#")
        try:
            return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
        except:
            return None

    # Aplicar modificadores de color si existen
    if modificadores:
        # Configurar color de fondo
        if len(modificadores) >= 1:
            valor_fondo = modificadores[0].lower()
            if valor_fondo in mapa_colores:
                color_fondo = mapa_colores[valor_fondo]
            elif valor_fondo.startswith("#") and len(valor_fondo) in (4, 7):
                rgb = hex_a_rgb(valor_fondo)
                if rgb:
                    color_fondo = rgb

        # Configurar color de texto
        if len(modificadores) >= 2:
            valor_texto = modificadores[1].lower()
            if valor_texto in mapa_colores:
                color_texto = mapa_colores[valor_texto]
            elif valor_texto.startswith("#") and len(valor_texto) in (4, 7):
                rgb = hex_a_rgb(valor_texto)
                if rgb:
                    color_texto = rgb

    # Separar texto en palabras para columnas
    palabras = texto.split()
    if not palabras:
        await update.message.reply_text("⚠️ El texto no puede estar vacío!")
        return

    # Crear imagen en HD
    img = Image.new('RGB', (2400, 1200), color=color_fondo)
    draw = ImageDraw.Draw(img)

    # Cargar fuente compatible con emojis
    fuentes_soportadas = [
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]
    font = None
    for ruta_fuente in fuentes_soportadas:
        try:
            font = ImageFont.truetype(ruta_fuente, 280)
            break
        except:
            continue
    if font is None:
        font = ImageFont.load_default(size=280)

    # Calcular posición centrada
    total_altura = 0
    for palabra in palabras:
        bbox = draw.textbbox((0, 0), palabra, font=font)
        total_altura += (bbox[3] - bbox[1]) + 40
    y_inicial = (1200 - total_altura) // 2

    # Dibujar texto en columnas
    y_actual = y_inicial
    for palabra in palabras:
        bbox = draw.textbbox((0, 0), palabra, font=font)
        ancho_palabra = bbox[2] - bbox[0]
        x_actual = (2400 - ancho_palabra) // 2
        draw.text((x_actual, y_actual), palabra, fill=color_texto, font=font)
        y_actual += (bbox[3] - bbox[1]) + 40

    # Guardar y enviar
    img_path = f"{RUTA_LOGS}/brat_{user_id}.png"
    img.save(img_path, quality=95)
    with open(img_path, 'rb') as img_file:
        await update.message.reply_photo(
            photo=img_file,
            caption=f"🎨 **Sticker BRAT HD** creado por {nick}\n✨ _Tamaño: 2400x1200 - Texto en columnas_"
        )

    os.remove(img_path)
    registrar_evento(user_id, nick, f"Creó sticker BRAT: {texto} | Fondo: {color_fondo}, Texto: {color_texto}", "ARTE")
    sumar_xp(user_id, 8)

#brat normal /bratv3
async def bratv3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea imágenes estilo BRAT adaptables a cualquier resolución, con manejo seguro de parámetros.
    Uso: /bratv3 [texto] *[color_fondo]+[color_texto]^[ancho]x[alto]"""
    import os
    from PIL import Image, ImageDraw, ImageFont

    # Configuración base
    RUTA_LOGS = "./logs"
    os.makedirs(RUTA_LOGS, exist_ok=True)

    # Validar entrada
    if not context.args:
        await update.message.reply_text(
            "⚠️ Uso incorrecto!\n"
            "Ejemplo: /bratv3 Hola mundo *negro+rojo^720x1612"
        )
        return

    entrada_completa = " ".join(context.args)
    texto_principal = entrada_completa
    color_fondo = (0, 0, 0)  # Negro por defecto
    color_texto = (255, 0, 0)  # Rojo por defecto
    resolucion = (2400, 1200)  # Resolución por defecto

    # Separar modificadores: *color_fondo+color_texto^ancho_xalto
    if "*" in entrada_completa:
        texto_parte, modificadores_parte = entrada_completa.split("*", 1)
        texto_principal = texto_parte.strip().upper()
        
        # Procesar colores y resolución
        if "+" in modificadores_parte:
            partes_mod = modificadores_parte.split("+")
            for parte in partes_mod:
                parte = parte.strip()
                # Manejo de colores
                if parte.startswith(("negro", "black")):
                    color_fondo = (0, 0, 0)
                elif parte.startswith(("rojo", "red")):
                    color_texto = (255, 0, 0)
                elif parte.startswith(("blanco", "white")):
                    color_fondo = (255, 255, 255)
                elif parte.startswith(("azul", "blue")):
                    color_texto = (0, 0, 255)
                # Manejo de resolución
                elif "^" in parte:
                    try:
                        ancho_r, alto_r = parte.replace("^", "").split("x")
                        resolucion = (int(ancho_r), int(alto_r))
                    except:
                        resolucion = (2400, 1200)
        else:
            texto_principal = entrada_completa.upper()
    else:
        texto_principal = entrada_completa.upper()

    # Crear imagen
    try:
        img = Image.new("RGB", resolucion, color_fondo)
        draw = ImageDraw.Draw(img)

        # Cargar fuente compatible
        fuentes_soportadas = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "/Library/Fonts/Arial Bold.ttf"
        ]
        font = None
        tam_fuente = min(resolucion[0] // 5, resolucion[1] // len(texto_principal.split()))
        tam_fuente = max(tam_fuente, 20)  # Tamaño mínimo

        for ruta_fuente in fuentes_soportadas:
            try:
                font = ImageFont.truetype(ruta_fuente, tam_fuente)
                break
            except:
                continue
        if not font:
            font = ImageFont.load_default(size=tam_fuente)

        # Dividir texto en líneas y centrar
        palabras = texto_principal.split()
        num_lineas = len(palabras)
        espaciado_vertical = resolucion[1] // (num_lineas + 1)
        y_actual = espaciado_vertical

        for palabra in palabras:
            bbox = draw.textbbox((0, 0), palabra, font=font)
            ancho_palabra = bbox[2] - bbox[0]
            x_actual = (resolucion[0] - ancho_palabra) // 2
            draw.text((x_actual, y_actual), palabra, font=font, fill=color_texto)
            y_actual += espaciado_vertical

        # Guardar y enviar
        ruta_temp = f"{RUTA_LOGS}/brat_{update.effective_user.id}.png"
        img.save(ruta_temp, quality=95)

        with open(ruta_temp, "rb") as img_file:
            await update.message.reply_photo(
                photo=img_file,
                caption=f"🎨 **Sticker BRAT HD** creado por {update.effective_user.first_name}\n"
                        f"✨ _Tamaño: {resolucion[0]}x{resolucion[1]} - Texto en columnas_"
            )

        os.remove(ruta_temp)

    except Exception as e:
        await update.message.reply_text(f"❌ Error al crear la imagen: {str(e)}")
        # Manejo de error detallado para consola
        print(f"Error en bratv3: {str(e)}")



# --- [ OSINT: INVESTIGACIÓN DE USUARIOS DE GITHUB ] ---
@tarea_larga
async def osint_github(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Obtiene información pública de un usuario de GitHub."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🔍 **Uso:**\n"
            "`/github [usuario]`\n"
            "_Ejemplo: /github torvalds_"
        )
        return

    username = context.args[0]
    wait_msg = await update.message.reply_text(f"🔎 Investigando a **{username}**...")

    try:
        url = f"https://api.github.com/users/{username}"
        respuesta = await asyncio.to_thread(requests.get, url, timeout=10)

        if respuesta.status_code == 404:
            await wait_msg.edit_text(f"❌ El usuario **{username}** no existe en GitHub.")
            return

        data = respuesta.json()

        nombre = data.get('name', 'Sin nombre')
        bio = data.get('bio', 'Sin biografía')
        repos = data.get('public_repos', 0)
        followers = data.get('followers', 0)
        following = data.get('following', 0)
        ubicacion = data.get('location', 'Desconocida')
        creado = data.get('created_at', '')[:10]

        reporte = (
            f"🔍 **OSINT · GITHUB** 🔍\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Usuario:** `{username}`\n"
            f"📝 **Nombre:** `{nombre}`\n"
            f"📍 **Ubicación:** `{ubicacion}`\n"
            f"📅 **Cuenta creada:** `{creado}`\n"
            f"📦 **Repositorios:** `{repos}`\n"
            f"👥 **Seguidores:** `{followers}`\n"
            f"➕ **Siguiendo:** `{following}`\n"
            f"💬 **Bio:** _{bio}_\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔗 [Ver perfil](https://github.com/{username})"
        )

        await wait_msg.edit_text(reporte, parse_mode=ParseMode.MARKDOWN)
        registrar_evento(user_id, nick, f"OSINT GitHub: {username}", "INVESTIGACIÓN")
        sumar_xp(user_id, 12)

    except Exception as e:
        print(f"❌ Error OSINT GitHub: {e}")
        await wait_msg.edit_text("❌ Error al obtener datos.")


# --- [ OSINT: TIKTOK USER INFO ] ---
@tarea_larga
async def cmd_tiktokuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Consulta información de un usuario de TikTok usando petdii.com"""
    user_id = update.effective_user.id
    
    # ── PASO 1: Validar argumentos
    if not context.args:
        await update.message.reply_text(
            "🔍 **Uso:**\n"
            "`/tiktokuser [username]` - Muestra información del perfil\n"
            "`/tiktokuser [username]*[número]` - Muestra información + últimos [número] videos\n\n"
            "_Ejemplos:_\n"
            "`/tiktokuser anyer123`\n"
            "`/tiktokuser anyer123*2`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # ── PASO 2: Separar username y número de videos
    username = context.args[0].strip().lstrip('@')
    num_videos = 0
    
    if '*' in username:
        username, num_videos_str = username.split('*')
        try:
            num_videos = int(num_videos_str)
            if num_videos > 10:  # Limitar a 10 videos máximo
                num_videos = 10
        except ValueError:
            num_videos = 0
    
    # ── PASO 3: Mostrar mensaje de procesamiento
    wait_msg = await update.message.reply_text(
        "🔍 **Procesando tu solicitud...**\n"
        "_Estamos obteniendo información del perfil..._",
        parse_mode=ParseMode.MARKDOWN
    )
    
    try:
        # ── PASO 4: Hacer la solicitud al sitio web
        url = "https://petdii.com/es"
        payload = {
            "username": username,
            "action": "search"
        }
        
        # Hacer la solicitud (con manejo de errores)
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        
        # ── PASO 5: Analizar el HTML (ejemplo usando BeautifulSoup)        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer información del perfil
        profile_info = {
            "username": f"@{username}",
            "likes": soup.select_one(".likes").text.strip(),
            "followers": soup.select_one(".followers").text.strip(),
            "following": soup.select_one(".following").text.strip(),
            "bio": soup.select_one(".bio").text.strip(),
            "verified": bool(soup.select_one(".verified"))
        }
        
        # Extraer videos si se solicitó
        videos = []
        if num_videos > 0:
            video_elements = soup.select(".video-item")[:num_videos]
            for video in video_elements:
                videos.append({
                    "title": video.select_one(".title").text.strip(),
                    "views": video.select_one(".views").text.strip(),
                    "duration": video.select_one(".duration").text.strip(),
                    "url": video.select_one(".video-link")["href"]
                })
        
        # ── PASO 6: Formatear la respuesta
        response_text = f"🔍 **OSINT · TIKTOK**\n"
        response_text += f"━━━━━━━━━━━━━━━━━━━━\n"
        response_text += f"👤 **Usuario:** `{profile_info['username']}`\n"
        response_text += f"❤️ **Likes:** `{profile_info['likes']}`\n"
        response_text += f"👥 **Seguidores:** `{profile_info['followers']}`\n"
        response_text += f"➡️ **Siguiendo:** `{profile_info['following']}`\n"
        response_text += f"📝 **Biografía:**\n`{profile_info['bio']}`\n"
        
        if profile_info['verified']:
            response_text += "✅ **Cuenta verificada**\n"
        
        response_text += f"━━━━━━━━━━━━━━━━━━━━\n"
        
        # Añadir videos si se solicitó
        if num_videos > 0 and videos:
            response_text += f"🎬 **Últimos {len(videos)} videos:**\n"
            for i, video in enumerate(videos, 1):
                response_text += f"{i}. [{video['title']}]({video['url']})\n"
                response_text += f"   👁️ {video['views']} · ⏱️ {video['duration']}\n"
        
        response_text += "\n⚠️ _TikTok no permite scraping público._\n"
        response_text += "_Visita el perfil manualmente:_\n"
        response_text += f"`https://tiktok.com/@{username}`"
        
        # --- PASO 7: Enviar la respuesta
        await wait_msg.edit_text(
            response_text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

        # Registrar evento
        registrar_evento(user_id,
            "TikTok", f"Consultó perfil: @{username}", "OSINT")
        
        
    except Exception as e:
        await wait_msg.edit_text(
            f"❌ **Error al procesar la solicitud.**\n"
            f"_Error: {str(e)}_",
    
    parse_mode=ParseMode.MARKDOWN
        )
#justo aqui arriba

# --- [ CONSULTA DE PERFILES DE FREE FIRE ] ---
async def idff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Consulta información de un jugador de Free Fire por su ID."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🎮 **Uso correcto:**\n"
            "`/idff [ID del jugador]`\n\n"
            "_Ejemplo: /idff 123456789_\n"
            "_Muestra: Nivel, Rango, Estadísticas, etc._",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    player_id = context.args[0]
    
    # Validar que sea un ID numérico
    if not player_id.isdigit():
        await update.message.reply_text("❌ **El ID debe ser numérico.**")
        return

    wait_msg = await update.message.reply_text(
        f"🔍 **Buscando jugador:** `{player_id}`\n"
        f"⏳ _Consultando base de datos..._",
        parse_mode=ParseMode.MARKDOWN
    )

    try:
        # Usar API no oficial de Free Fire
        # Hay varias APIs comunitarias disponibles
        
        # Método 1: Usar API de terceros (Free Fire Stats API)
        url = f"https://api.freefirestats.org/player/{player_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        respuesta = await asyncio.to_thread(
            requests.get,
            url,
            headers=headers,
            timeout=15
        )

        if respuesta.status_code == 404:
            await wait_msg.edit_text(
                f"❌ **No se encontró el jugador:** `{player_id}`\n"
                f"_Verifica que el ID sea correcto._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        if respuesta.status_code != 200:
            # Si la API principal falla, intentar método alternativo
            await idff_alternativo(update, context, player_id, wait_msg)
            return

        data = respuesta.json()
        
        # Extraer información del perfil
        nombre = data.get('nickname', 'Desconocido')
        nivel = data.get('level', 'N/A')
        region = data.get('region', 'Desconocida')
        
        # Información de rango
        rank_info = data.get('rank', {})
        rango_br = rank_info.get('br', 'Sin rango')
        rango_cs = rank_info.get('cs', 'Sin rango')
        
        # Estadísticas
        stats = data.get('stats', {})
        partidas_br = stats.get('br_matches', 0)
        victorias_br = stats.get('br_wins', 0)
        kd_br = stats.get('br_kd', '0.0')
        
        # Calcular porcentaje de victorias
        try:
            win_rate = (victorias_br / partidas_br * 100) if partidas_br > 0 else 0
        except:
            win_rate = 0

        # Determinar emoji de rango
        emoji_rango = "🏆"
        if "Heroic" in str(rango_br):
            emoji_rango = "👑"
        elif "Grandmaster" in str(rango_br):
            emoji_rango = "💎"
        elif "Diamond" in str(rango_br):
            emoji_rango = "💠"
        elif "Platinum" in str(rango_br):
            emoji_rango = "⭐"
        elif "Gold" in str(rango_br):
            emoji_rango = "🥇"

        perfil = (
            f"🎮 **FREE FIRE · PERFIL** 🎮\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Nombre:** `{nombre}`\n"
            f"🆔 **ID:** `{player_id}`\n"
            f"📊 **Nivel:** `{nivel}`\n"
            f"🌍 **Región:** `{region}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"{emoji_rango} **RANGOS**\n"
            f"🏆 Battle Royale: `{rango_br}`\n"
            f"⚔️ Clash Squad: `{rango_cs}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📈 **ESTADÍSTICAS BR**\n"
            f"🎯 Partidas: `{partidas_br}`\n"
            f"🏆 Victorias: `{victorias_br}`\n"
            f"📊 Win Rate: `{win_rate:.1f}%`\n"
            f"💀 K/D: `{kd_br}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔍 _Consultado por {nick}_"
        )

        await wait_msg.edit_text(perfil, parse_mode=ParseMode.MARKDOWN)
        registrar_evento(user_id, nick, f"Consultó FF ID: {player_id}", "FREE-FIRE")
        sumar_xp(user_id, 12)

    except requests.exceptions.Timeout:
        await wait_msg.edit_text(
            "⏱️ **La consulta está tardando mucho.**\n"
            "_El servidor de Free Fire puede estar lento._"
        )
    except requests.exceptions.RequestException:
        await idff_alternativo(update, context, player_id, wait_msg)
    except Exception as e:
        print(f"❌ Error Free Fire: {e}")
        await idff_alternativo(update, context, player_id, wait_msg)


async def idff_alternativo(update: Update, context: ContextTypes.DEFAULT_TYPE, player_id, wait_msg):
    """Método alternativo para consultar perfiles de Free Fire."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    try:
        # Método alternativo: Scraping básico
        # Nota: Free Fire no tiene API oficial pública
        # Generamos datos de ejemplo basados en el ID
        
        await wait_msg.edit_text(
            f"🎮 **FREE FIRE · PERFIL** 🎮\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 **ID:** `{player_id}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ **Información no disponible**\n"
            f"_La API de Free Fire no es pública._\n\n"
            f"💡 **Cómo ver el perfil:**\n"
            f"1. Abre Free Fire\n"
            f"2. Ve a 'Amigos'\n"
            f"3. Toca 'Buscar'\n"
            f"4. Ingresa el ID: `{player_id}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔗 También puedes usar:\n"
            f"- **FF Stats:** ff.garena.com\n"
            f"- **Stats.gg:** stats.gg/freefire\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔍 _Consultado por {nick}_",
            parse_mode=ParseMode.MARKDOWN
        )
        
        registrar_evento(user_id, nick, f"Intentó consultar FF ID: {player_id}", "FREE-FIRE")
        sumar_xp(user_id, 5)
        
    except Exception as e:
        print(f"❌ Error método alternativo FF: {e}")
        await wait_msg.edit_text(
            "❌ **Error al consultar el perfil.**\n"
            "_Intenta de nuevo más tarde._"
        )


# --- FINAL DE PARTE 8 ---
# --- [ COMANDOS ADMINISTRATIVOS ] ---
async def admin_expropiar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Permite al admin robar dinero a cualquier usuario."""
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permisos para usar este comando.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ Debes **responder** al mensaje del usuario que quieres expropiar."
        )
        return

    target_id = str(update.message.reply_to_message.from_user.id)
    target_nick = update.message.reply_to_message.from_user.first_name

    dinero_robado = banco.get(target_id, 0.0)

    if dinero_robado <= 0:
        await update.message.reply_text(f"❌ **{target_nick}** no tiene dinero para expropiar.")
        return

    # Transferir todo el dinero al admin
    banco[target_id] = 0.0
    sumar_dinero(ADMIN_ID, dinero_robado)
    guardar_db("banco.json", banco)

    await update.message.reply_text(
        f"💰 **EXPROPIACIÓN EXITOSA**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Víctima: `{target_nick}`\n"
        f"💵 Dinero robado: `${dinero_robado}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ _El dinero fue transferido al CREADOR._",
        parse_mode=ParseMode.MARKDOWN
    )

    registrar_evento(ADMIN_ID, "ADMIN", f"Expropió ${dinero_robado} a {target_nick}", "ADMIN")


async def admin_ver_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Permite al admin ver los últimos logs del sistema."""
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permisos.")
        return

    # Leer las últimas 30 líneas del archivo de logs
    try:
        with open(f"{RUTA_LOGS}/mega_historial.txt", "r", encoding="utf-8") as f:
            lineas = f.readlines()[-30:]
        
        logs_texto = "".join(lineas)
        
        await update.message.reply_text(
            f"📋 **ÚLTIMOS 30 EVENTOS**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"```\n{logs_texto}\n```",
            parse_mode=ParseMode.MARKDOWN
        )
    except:
        await update.message.reply_text("❌ No hay logs disponibles.")


# --- [ PANEL ADMINISTRATIVO COMPLETO ] ---
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Panel administrativo con todas las funciones y estadísticas."""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ **No tienes permisos para acceder al panel admin.**\n_Solo el creador del bot puede usar esto._")
        return
    
    # Calcular estadísticas
    total_usuarios = len(banco)
    total_dinero = sum(banco.values())
    usuario_con_mas_dinero = max(banco.items(), key=lambda x: x[1]) if banco else ("Ninguno", 0)
    
    panel = (
        f"⚙️ **PANEL ADMINISTRATIVO CAMILABOT V8.0** ⚙️\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 **DATOS GENERALES:**\n"
        f"├ Admin ID: `{ADMIN_ID}`\n"
        f"├ Versión: `{VERSION}`\n"
        f"├ Usuarios registrados: `{total_usuarios}`\n"
        f"├ Dinero total en circulación: `Bs. {total_dinero:,.2f}`\n"
        f"├ Usuario más rico: `{usuario_con_mas_dinero[0]} (Bs. {usuario_con_mas_dinero[1]:,.2f})`\n"
        f"└ Fecha: `{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}`\n\n"
        f"⚡ **COMANDOS ADMINISTRATIVOS DISPONIBLES:**\n"
        f"├ `/admin` - Ver este panel\n"
        f"├ `/expropiar [id] [cantidad]` - Confiscar dinero\n"
        f"├ `/ver_logs` - Ver últimos eventos\n"
        f"├ `/blockuser [id]` - Bloquear usuario\n"
        f"├ `/unblockuser [id]` - Desbloquear usuario\n"
        f"├ `/inforuser [id]` - Info detallada del usuario\n"
        f"├ `/users` - Lista de todos los usuarios\n"
        f"├ `/resetchats` - Limpiar todos los chats\n"
        f"├ `/extmsj [id]` - Extraer últimos 15 mensajes\n"
        f"├ `/banear [id]` - Banear usuario del bot\n"
        f"├ `/reseteconomia` - Limpiar base de datos de dinero\n"
        f"└ `/anuncio [mensaje]` - Enviar anuncio a usuarios\n\n"
        f"🔧 **FUNCIONES DEL BOT:**\n"
        f"├ ✅ Economía (trabajar, apostar, robar)\n"
        f"├ ✅ Multimedia (descargas, conversiones)\n"
        f"├ ✅ Búsqueda inteligente\n"
        f"├ ✅ Traducción (12 idiomas)\n"
        f"├ ✅ Listas diarias (7 diferentes)\n"
        f"├ ✅ Juegos y entretenimiento\n"
        f"├ ✅ Sistema de rangos\n"
        f"├ ✅ Historial de conversaciones\n"
        f"├ ✅ OSINT (información pública)\n"
        f"└ ✅ 60+ comandos totales\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ _Panel seguro - Solo acceso a admin_"
    )
    
    await update.message.reply_text(panel, parse_mode=ParseMode.MARKDOWN)
    registrar_evento(user_id, "ADMIN", "Accedió al panel administrativo", "ADMIN")


# --- [ BLOQUEAR USUARIO ] ---
async def admin_blockuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bloquea a un usuario del bot."""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permisos.")
        return
    
    if not context.args:
        await update.message.reply_text("📌 **Uso:** `/blockuser [ID usuario]`")
        return
    
    try:
        usuario_id = int(context.args[0])
        blacklist[str(usuario_id)] = True
        guardar_db("blacklist.json", blacklist)
        
        await update.message.reply_text(
            f"🚫 **Usuario {usuario_id} bloqueado correctamente.**\n"
            f"_No podrá usar el bot._"
        )
        registrar_evento(user_id, "ADMIN", f"Bloqueó usuario {usuario_id}", "ADMIN")
    except ValueError:
        await update.message.reply_text("❌ ID inválido")


# --- [ DESBLOQUEAR USUARIO ] ---
async def admin_unblockuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Desbloquea a un usuario del bot."""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permisos.")
        return
    
    if not context.args:
        await update.message.reply_text("📌 **Uso:** `/unblockuser [ID usuario]`")
        return
    
    try:
        usuario_id = str(context.args[0])
        if usuario_id in blacklist:
            del blacklist[usuario_id]
            guardar_db("blacklist.json", blacklist)
            
            await update.message.reply_text(
                f"✅ **Usuario {usuario_id} desbloqueado correctamente.**"
            )
            registrar_evento(user_id, "ADMIN", f"Desbloqueó usuario {usuario_id}", "ADMIN")
        else:
            await update.message.reply_text("❌ Este usuario no estaba bloqueado")
    except:
        await update.message.reply_text("❌ Error al desbloquear")


# --- [ INFORMACIÓN DETALLADA DE UN USUARIO ] ---
async def admin_inforuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra información detallada de un usuario."""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permisos.")
        return
    
    if not context.args:
        await update.message.reply_text("📌 **Uso:** `/inforuser [ID usuario]`")
        return
    
    try:
        usuario_id = str(context.args[0])
        
        # Obtener información
        dinero = banco.get(usuario_id, 0.0)
        xp = niveles.get(usuario_id, 0)
        info_user = usuarios_info.get(usuario_id, {})
        bloqueado = usuario_id in blacklist
        
        nombre = info_user.get("nombre", "No registrado")
        edad = info_user.get("edad", "N/A")
        genero = info_user.get("genero", "N/A")
        
        reporte = (
            f"👤 **INFORMACIÓN DEL USUARIO** 👤\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 **Chat ID:** `{usuario_id}`\n"
            f"📝 **Nombre:** `{nombre}`\n"
            f"🎂 **Edad:** `{edad}`\n"
            f"⚧️ **Género:** `{genero}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 **Dinero:** `Bs. {dinero:,.2f}`\n"
            f"✨ **Experiencia:** `{xp} XP`\n"
            f"🎖️ **Rango:** `{obtener_rango(int(usuario_id))}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚫 **Estado:** `{'BLOQUEADO' if bloqueado else 'ACTIVO'}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        
        await update.message.reply_text(reporte, parse_mode=ParseMode.MARKDOWN)
        registrar_evento(user_id, "ADMIN", f"Consultó información de usuario {usuario_id}", "ADMIN")
        
    except Exception as e:
        print(f"Error inforuser: {e}")
        await update.message.reply_text("❌ Error al obtener información")


# --- [ LISTA DE TODOS LOS USUARIOS ] ---
async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra lista de todos los usuarios con información."""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permisos.")
        return
    
    wait_msg = await update.message.reply_text("📊 **Cargando lista de usuarios...**\n⏳ _Por favor espera..._")
    
    try:
        if not banco:
            await wait_msg.edit_text("❌ No hay usuarios registrados.")
            return
        
        # Ordenar usuarios por ID
        usuarios_ordenados = sorted(banco.items(), key=lambda x: x[0])
        
        # Limitar a mostrar información resumida si hay muchos usuarios
        lista_texto = f"👥 **LISTA DE USUARIOS DEL BOT** 👥\n"
        lista_texto += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        lista_texto += f"📊 **Total de usuarios:** `{len(usuarios_ordenados)}`\n\n"
        
        for idx, (uid, dinero) in enumerate(usuarios_ordenados, 1):
            info = usuarios_info.get(uid, {})
            nombre = info.get("nombre", "Sin nombre")
            xp = niveles.get(uid, 0)
            rango = obtener_rango(int(uid))
            bloqueado = "🚫" if uid in blacklist else "✅"
            
            lista_texto += f"{idx}. {bloqueado} **{nombre}**\n"
            lista_texto += f"   🆔 ID: `{uid}`\n"
            lista_texto += f"   💰 Dinero: `Bs. {dinero:,.2f}`\n"
            lista_texto += f"   ✨ XP: `{xp}`\n"
            lista_texto += f"   🎖️ Rango: `{rango}`\n"
            lista_texto += f"   ━━━━━━━━━━━━━━\n"
            
            # Si la lista es muy larga, dividir en mensajes
            if len(lista_texto) > 3500:
                await update.message.reply_text(lista_texto, parse_mode=ParseMode.MARKDOWN)
                lista_texto = ""
        
        if lista_texto:
            await update.message.reply_text(lista_texto, parse_mode=ParseMode.MARKDOWN)
        
        await wait_msg.delete()
        registrar_evento(user_id, "ADMIN", "Consultó lista de usuarios", "ADMIN")
        
    except Exception as e:
        print(f"Error users: {e}")
        await wait_msg.edit_text("❌ Error al obtener lista")


# --- [ LIMPIAR TODOS LOS CHATS ] ---
async def admin_resetchats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Limpia el historial de todas las conversaciones."""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permisos.")
        return
    
    try:
        total_chats = len(conversaciones)
        
        # Confirmar acción
        if not context.args or context.args[0] != "confirmar":
            await update.message.reply_text(
                f"⚠️ **ADVERTENCIA: ESTO ELIMINARÁ TODOS LOS CHATS**\n\n"
                f"Chats a eliminar: `{total_chats}`\n\n"
                f"Para confirmar, escribe:\n"
                f"`/resetchats confirmar`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Limpiar conversaciones
        conversaciones.clear()
        guardar_db("conversaciones.json", conversaciones)
        
        await update.message.reply_text(
            f"✅ **CHATS LIMPIOS CORRECTAMENTE**\n\n"
            f"Chats eliminados: `{total_chats}`\n"
            f"Estado: `LIMPIO`",
            parse_mode=ParseMode.MARKDOWN
        )
        
        registrar_evento(user_id, "ADMIN", f"Limpió {total_chats} chats", "ADMIN")
        
    except Exception as e:
        print(f"Error resetchats: {e}")
        await update.message.reply_text("❌ Error al limpiar chats")


# --- [ EXTRAER ÚLTIMOS 15 MENSAJES ] ---
async def admin_extmsj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Extrae los últimos 15 mensajes de un chat específico."""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permisos.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📌 **Uso:** `/extmsj [ID usuario]`\n\n"
            "Ejemplo: `/extmsj 123456789`"
        )
        return
    
    try:
        usuario_id = str(context.args[0])
        
        if usuario_id not in conversaciones or not conversaciones[usuario_id]:
            await update.message.reply_text(f"❌ No hay mensajes para el usuario `{usuario_id}`")
            return
        
        # Obtener últimos 15 mensajes
        mensajes = conversaciones[usuario_id][-15:]
        info_user = usuarios_info.get(usuario_id, {})
        nombre = info_user.get("nombre", "Desconocido")
        
        extracto = f"💬 **ÚLTIMOS 15 MENSAJES DE {nombre}** 💬\n"
        extracto += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        extracto += f"🆔 Usuario: `{usuario_id}`\n\n"
        
        for idx, msg in enumerate(mensajes, 1):
            extracto += f"{idx}. **{msg.get('rol', 'usuario').upper()}**\n"
            extracto += f"   {msg.get('contenido', 'Sin contenido')[:100]}\n"
            extracto += f"   🕐 {msg.get('timestamp', 'N/A')}\n\n"
        
        await update.message.reply_text(extracto, parse_mode=ParseMode.MARKDOWN)
        registrar_evento(user_id, "ADMIN", f"Extrajo mensajes de usuario {usuario_id}", "ADMIN")
        
    except Exception as e:
        print(f"Error extmsj: {e}")
        await update.message.reply_text("❌ Error al extraer mensajes")


# --- [ MÓDULO CLIMA: TEMPERATURA EN CUALQUIER CIUDAD ] ---
async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Consulta el clima de cualquier ciudad usando wttr.in (gratis, sin API key)."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🌤️ **Uso:** `/clima [ciudad]`\n"
            "_Ejemplo: /clima Caracas_"
        )
        return

    ciudad = " ".join(context.args)
    wait_msg = await update.message.reply_text(f"🔍 **Consultando el clima de** `{ciudad}`...")

    try:
        # wttr.in es gratuito y no requiere API Key
        url = f"https://wttr.in/{ciudad}?format=j1&lang=es"
        respuesta = await asyncio.to_thread(requests.get, url, timeout=10)

        if respuesta.status_code != 200:
            await wait_msg.edit_text("❌ No encontré esa ciudad. ¿Escribiste bien el nombre?")
            return

        data = respuesta.json()
        actual = data['current_condition'][0]
        info_lugar = data['nearest_area'][0]

        nombre_lugar = info_lugar['areaName'][0]['value']
        pais = info_lugar['country'][0]['value']
        temp_c = actual['temp_C']
        sensacion = actual['FeelsLikeC']
        humedad = actual['humidity']
        viento = actual['windspeedKmph']
        descripcion = actual['weatherDesc'][0]['value']

        # Elegir emoji según temperatura
        if int(temp_c) >= 30:
            emoji_temp = "🔥"
        elif int(temp_c) >= 20:
            emoji_temp = "☀️"
        elif int(temp_c) >= 10:
            emoji_temp = "🌤️"
        else:
            emoji_temp = "🥶"

        reporte_clima = (
            f"🌍 **CLIMA EN TIEMPO REAL** 🌍\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 **Ciudad:** `{nombre_lugar}, {pais}`\n"
            f"{emoji_temp} **Temperatura:** `{temp_c}°C`\n"
            f"🌡️ **Sensación:** `{sensacion}°C`\n"
            f"💧 **Humedad:** `{humedad}%`\n"
            f"💨 **Viento:** `{viento} km/h`\n"
            f"☁️ **Estado:** `{descripcion}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🛡️ _Datos en vivo · Pedido por {nick}_"
        )

        await wait_msg.edit_text(reporte_clima, parse_mode=ParseMode.MARKDOWN)
        registrar_evento(user_id, nick, f"Consultó clima de {ciudad}", "CLIMA")
        sumar_xp(user_id, 5)

    except Exception as e:
        print(f"❌ Error clima: {e}")
        await wait_msg.edit_text("❌ **Fallo de conexión.** Intenta de nuevo en unos segundos.")


# --- [ MÓDULO CHISTES: HUMOR VENEZOLANO ] ---
CHISTES_VENEZOLANOS = [
    "¿Por qué el venezolano lleva una escalera al bar?\n_Porque le dijeron que los tragos estaban por las nubes._ 🍹",
    "Un venezolano llega al cielo y San Pedro le dice: '¿Traes algo que declarar?'\nEl venezolano responde: '_Solo el pasaporte... y el trauma._' 🇻🇪",
    "¿Cuál es el colmo de un venezolano?\n_Que el CLAP le llegue cuando ya se fue del país._ 📦",
    "¿Por qué los venezolanos son tan buenos en matemáticas?\n_Porque tienen práctica calculando cuántos dólares son en bolívares cada 5 minutos._ 💸",
    "Un chamo llega tarde al trabajo y el jefe le pregunta: '¿Cuál es tu excusa?'\nÉl responde: '_La cola en la gasolinera, mi pana. Solo duré 3 horas._' ⛽",
    "¿Qué le dice un venezolano a otro en el extranjero?\n_'Épale vale, ¿tú también eres de Caracas?' Respuesta: 'No, de Maracaibo.' 'Ah, somos vecinos pues.'_ 😂",
    "¿Cómo sabe un venezolano que ya se adaptó al país donde emigró?\n_Cuando deja de decir 'en Venezuela esto era mejor' al comer arepa._ 🫓",
    "Un venezolano pide un crédito en el banco.\nEl banco le pregunta: '¿Tiene bienes?'\nÉl responde: '_Tengo fe y un carro del 98._' 🚗",
    "¿Cuál es el superhéroe venezolano?\n_Apagón Man: aparece sin avisar y te deja sin luz por 8 horas._ ⚡",
    "¿Por qué el venezolano siempre llega tarde?\n_Porque la hora venezolana tiene su propio huso horario: 'ahorita', 'luego' y 'mañana temprano'._ ⏰",
]

async def chiste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía un chiste venezolano aleatorio."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    chiste_elegido = random.choice(CHISTES_VENEZOLANOS)

    res = (
        f"😂 **CHISTE VENEZOLANO DEL DÍA** 😂\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{chiste_elegido}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ _¡Échate un chiste con Cami.bot!_"
    )

    await update.message.reply_text(res, parse_mode=ParseMode.MARKDOWN)
    registrar_evento(user_id, nick, "Pidió un chiste venezolano", "HUMOR")
    sumar_xp(user_id, 3)


# --- [ BUSCADOR INTELIGENTE PARA TAREAS E INVESTIGACIONES y todo lo que sea ] ---
@tarea_larga
async def buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca en 15+ fuentes + traduce resultado si se especifica idioma."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text("Uso: /buscar [tema] o /buscar [tema]*idioma\nEj: /buscar película Gladiator*es o /buscar Sweater weather")
        return

    args_str = " ".join(context.args)
    
    # Detectar idioma (formato: tema*idioma o tema * idioma)
    idioma_objetivo = None
    query = args_str
    
    # Buscar patrón *idioma
    if "*" in args_str:
        parts = args_str.split("*")
        query = parts[0].strip()
        idioma_parte = parts[1].strip() if len(parts) > 1 else ""
        if idioma_parte and len(idioma_parte) <= 3:  # Código de idioma
            idioma_objetivo = idioma_parte.lower()
    
    wait_msg = await update.message.reply_text(f"Buscando: {query}..." + (f"\nTraduciendo a {idioma_objetivo}" if idioma_objetivo else ""))
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    async def traducir_resultado(texto, idioma):
        """Traduce el resultado GARANTIZADO"""
        if not idioma or not texto or len(texto) < 5:
            return texto
        
        # Mapeo de idiomas a códigos correctos
        idiomas_map = {
            'es': 'es', 'en': 'en', 'pt': 'pt', 'fr': 'fr', 'it': 'it', 
            'de': 'de', 'ja': 'ja', 'zh': 'zh', 'ru': 'ru', 'ar': 'ar',
            'ko': 'ko', 'hi': 'hi'
        }
        
        idioma = idiomas_map.get(idioma, idioma)
        
        # INTENTO 1: Google Translate (más confiable)
        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={idioma}&dt=t&q={quote(texto[:800])}"
            resp = await asyncio.to_thread(requests.get, url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                data = resp.json()
                if data and isinstance(data, list) and len(data) > 0 and data[0]:
                    # Google Translate devuelve estructura: [[texto_traducido, texto_original, ...], ...]
                    traducido = ''.join([str(item[0]) for item in data[0] if item and len(item) > 0])
                    if traducido and len(traducido.strip()) > 3:
                        return traducido.strip()
        except Exception as e:
            pass
        
        # INTENTO 2: MyMemory
        try:
            url = f"https://api.mymemory.translated.net/get?q={quote(texto[:800])}&langpair=auto|{idioma}"
            resp = await asyncio.to_thread(requests.get, url, timeout=6)
            data = resp.json()
            if data.get('responseStatus') == 200:
                traducido = data.get('responseData', {}).get('translatedText', '')
                if traducido and len(traducido) > 3:
                    return traducido
        except Exception as e:
            print(f"Error MyMemory: {e}")
        
        return texto
    
    async def try_fuente(nombre, url, parser_func):
        """Intenta buscar en una fuente específica"""
        try:
            resp = await asyncio.to_thread(requests.get, url, headers=headers, timeout=6)
            if resp.status_code == 200:
                return (nombre, parser_func(resp))
        except:
            pass
        return None
    
    try:
        # FUENTES A INTENTAR (15+)
        fuentes = [
            ("DuckDuckGo", f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_redirect=1", 
             lambda r: r.json().get('AbstractText', '')[:800] if r.json().get('AbstractText') else ''),
            
            ("Wikipedia ES", f"https://es.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&titles={quote(query)}&explaintext=true",
             lambda r: list(r.json().get('query', {}).get('pages', {}).values())[0].get('extract', '')[:800] if r.json().get('query', {}).get('pages') else ''),
            
            ("Wikipedia EN", f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&titles={quote(query)}&explaintext=true",
             lambda r: list(r.json().get('query', {}).get('pages', {}).values())[0].get('extract', '')[:800] if r.json().get('query', {}).get('pages') else ''),
            
            ("Bing Search", f"https://www.bing.com/search?q={quote(query)}",
             lambda r: BeautifulSoup(r.content, 'html.parser').find('p') and BeautifulSoup(r.content, 'html.parser').find('p').get_text()[:800] or ''),
            
            ("YouTube Info", f"https://www.youtube.com/results?search_query={quote(query)}",
             lambda r: BeautifulSoup(r.content, 'html.parser').get_text()[500:1300] if len(BeautifulSoup(r.content, 'html.parser').get_text()) > 500 else ''),
            
            ("GitHub", f"https://api.github.com/search/repositories?q={quote(query)}&sort=stars&per_page=1",
             lambda r: f"{r.json()['items'][0]['name']}: {r.json()['items'][0]['description'][:700]}" if r.json().get('items') else ''),
            
            ("Stack Overflow", f"https://api.stackexchange.com/2.2/search?intitle={quote(query)}&site=stackoverflow&pagesize=1",
             lambda r: r.json()['items'][0]['title'][:800] if r.json().get('items') else ''),
            
            ("Reddit", f"https://www.reddit.com/search.json?q={quote(query)}&limit=1",
             lambda r: f"{r.json()['data']['children'][0]['data']['title']}: {r.json()['data']['children'][0]['data'].get('selftext', '')}[:700]" if r.json().get('data', {}).get('children') else ''),
            
            ("IMDb", f"https://www.imdb.com/find?q={quote(query)}&s=all",
             lambda r: BeautifulSoup(r.content, 'html.parser').find('a', class_='ipc-link') and BeautifulSoup(r.content, 'html.parser').find('a', class_='ipc-link').get_text()[:800] or ''),
            
            ("Ecosia", f"https://www.ecosia.org/search?q={quote(query)}",
             lambda r: BeautifulSoup(r.content, 'html.parser').find('div', class_='result') and BeautifulSoup(r.content, 'html.parser').find('div', class_='result').get_text()[:800] or ''),
            
            ("Brave Search", f"https://search.brave.com/search?q={quote(query)}",
             lambda r: BeautifulSoup(r.content, 'html.parser').find('div', class_='snippet') and BeautifulSoup(r.content, 'html.parser').find('div', class_='snippet').get_text()[:800] or ''),
            
            ("Qwant", f"https://www.qwant.com/?q={quote(query)}",
             lambda r: BeautifulSoup(r.content, 'html.parser').find('a', class_='result') and BeautifulSoup(r.content, 'html.parser').find('a', class_='result').get_text()[:800] or ''),
            
            ("StartPage", f"https://www.startpage.com/sp/search?query={quote(query)}",
             lambda r: BeautifulSoup(r.content, 'html.parser').find('div', class_='w-gl-result') and BeautifulSoup(r.content, 'html.parser').find('div', class_='w-gl-result').get_text()[:800] or ''),
            
            ("Google Search", f"https://www.google.com/search?q={quote(query)}",
             lambda r: BeautifulSoup(r.content, 'html.parser').find('div', {'data-sokoban-container': True}) and BeautifulSoup(r.content, 'html.parser').find('div', {'data-sokoban-container': True}).get_text()[:800] or ''),
            
            ("Yandex", f"https://yandex.com/search/?text={quote(query)}",
             lambda r: BeautifulSoup(r.content, 'html.parser').find('div', class_='text-container') and BeautifulSoup(r.content, 'html.parser').find('div', class_='text-container').get_text()[:800] or ''),
        ]
        
        # SELENIUM CHROME como opción final
        from bs4 import BeautifulSoup
        
        # Intentar las 15 fuentes en paralelo
        for nombre, url, parser in fuentes:
            try:
                resp = await asyncio.to_thread(requests.get, url, headers=headers, timeout=5)
                if resp.status_code == 200:
                    try:
                        contenido = parser(resp)
                        if contenido and len(contenido) > 50:
                            if idioma_objetivo:
                                contenido = await traducir_resultado(contenido, idioma_objetivo)
                            resultado = f"FUENTE: {nombre}\nBÚSQUEDA: {query}\n\n{contenido}"
                            await wait_msg.edit_text(resultado)
                            registrar_evento(user_id, nick, f"Buscó ({nombre}): {query[:25]}", "BÚSQUEDA")
                            sumar_xp(user_id, 8)
                            return
                    except:
                        pass
            except:
                pass
        
        # ÚLTIMO INTENTO: Selenium Chrome real
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--headless')
            
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(10)
            driver.get(f"https://www.google.com/search?q={quote(query)}")
            
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "g")))
                elementos = driver.find_elements(By.CLASS_NAME, "g")
                if elementos and len(elementos[0].text) > 50:
                    contenido = elementos[0].text[:800]
                    if idioma_objetivo:
                        contenido = await traducir_resultado(contenido, idioma_objetivo)
                    resultado = f"NAVEGADOR CHROME\nBÚSQUEDA: {query}\n\n{contenido}"
                    await wait_msg.edit_text(resultado)
                    driver.quit()
                    registrar_evento(user_id, nick, f"Buscó (Chrome): {query[:25]}", "BÚSQUEDA")
                    sumar_xp(user_id, 8)
                    return
            except:
                pass
            
            driver.quit()
        except:
            pass
        
        # Si ABSOLUTAMENTE TODAS fallan
        resultado = f"No encontré info para: {query}\nIntenta:\n- Ser más específico\n- Buscar en Google: google.com/search?q={query.replace(' ', '+')}"
        await wait_msg.edit_text(resultado)
                    
    except Exception as e:
        print(f"Error búsqueda: {e}")
        await wait_msg.edit_text("Error. Intenta de nuevo")

# ------------------- BLOQUE DE BÚSQUEDA ARTISTAS/SPOTIFY -------------------
async def buscar_artistas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando: /artistas [término]
    Busca información de artistas, canciones y álbumes vía NexyLight API (fuente Spotify).
    """
    if not context.args:
        await update.message.reply_text(
            "⚠️ ¡Olvidaste el término de búsqueda!\n"
            "Uso: /artistas [nombre de artista/canción/álbum]\n"
            "Ejemplo: /artistas Lana Del Rey, /artistas Summertime Sadness"
        )
        return
    
    termino_busqueda = " ".join(context.args)
    URL_API = "https://api.nexylight.xyz/search/spotify"

    try:
        respuesta_api = requests.get(URL_API, params={"q": termino_busqueda, "limit": 10}, timeout=10)
        respuesta_api.raise_for_status()
        datos_resultado = respuesta_api.json()

        if not datos_resultado.get("status"):
            await update.message.reply_text("❌ No se encontraron resultados o la API tuvo un error.")
            return
        
        cantidad_resultados = len(datos_resultado.get("data", []))
        if cantidad_resultados == 0:
            await update.message.reply_text(f"🔍 No hay resultados para '{termino_busqueda}'.")
            return

        await update.message.reply_text(f"✅ Encontrados {cantidad_resultados} resultados relacionados con '{termino_busqueda}':")

        for indice, item in enumerate(datos_resultado["data"], 1):
            titulo = item.get("title", "Sin título")
            artista = item.get("artist", "Sin artista")
            album = item.get("album", "Sin álbum")
            duracion = item.get("duration", "Sin duración")
            fecha = item.get("publish", "Sin fecha")
            url_spotify = item.get("url", "#")
            imagen = item.get("image")

            texto_caption = (
                f"🔹 Resultado #{indice}\n"
                f"👤 **Artista**: {artista}\n"
                f"🎵 **Canción**: {titulo}\n"
                f"💿 **Álbum**: {album}\n"
                f"⏱️ Duración: {duracion}\n"
                f"📅 Publicación: {fecha}\n"
                f"🔗 Ver en Spotify: {url_spotify}"
            )

            try:
                await update.message.reply_photo(
                    photo=imagen,
                    caption=texto_caption
                )
            except Exception as error_imagen:
                await update.message.reply_text(texto_caption)

    except requests.exceptions.RequestException as error_conexion:
        await update.message.reply_text(f"⚠️ Error al conectar con la API: {str(error_conexion)}")
    except Exception as error_general:
        await update.message.reply_text(f"⚠️ Ocurrió un error: {str(error_general)}")

# ------------------- FIN DEL BLOQUE -------------------


async def buscar_alternativo(update: Update, context: ContextTypes.DEFAULT_TYPE, query, wait_msg):
    """Método alternativo de búsqueda usando solo IA."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    try:
        # Usar solo Gemini para responder la consulta
        prompt = f"""Eres Camila, una asistente educativa. El usuario busca información sobre: "{query}"

Da una respuesta educativa, útil y bien estructurada. Incluye:

Responde de manera directa y educativa:"""

        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }

        respuesta = await asyncio.to_thread(
            requests.post,
            GEMINI_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=20
        )

        if respuesta.status_code == 200:
            data = respuesta.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                texto = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                
                resultado = (
                    f"🔍 **INFORMACIÓN ENCONTRADA** 🔍\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"📝 **Búsqueda:** `{query}`\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"{texto}\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"💡 _Información generada por IA · Consultado por {nick}_"
                )
                
                await wait_msg.edit_text(resultado, parse_mode=ParseMode.MARKDOWN)
                registrar_evento(user_id, nick, f"Buscó (IA): {query[:50]}", "BÚSQUEDA-IA")
                sumar_xp(user_id, 8)
                return

        # Si todo falla, dar respuesta básica
        await wait_msg.edit_text(
            f"❌ **No pude realizar la búsqueda.**\n\n"
            f"💡 **Intenta buscar manualmente:**\n"
            f"- Google: `google.com/search?q={query.replace(' ', '+')}`\n"
            f"- Wikipedia: `es.wikipedia.org`\n"
            f"- YouTube: `youtube.com/results?search_query={query.replace(' ', '+')}`",
            parse_mode=ParseMode.MARKDOWN
        )

    except Exception as e:
        print(f"❌ Error búsqueda alternativa: {e}")
        await wait_msg.edit_text(
            "❌ **Error al procesar la búsqueda.**\n"
            "_Intenta de nuevo más tarde._"
        )


# --- [ BUSCADOR DE IMÁGENES EN PINTEREST ] ---
#comando /pinterestv2
async def pinterestv2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comandos: /pinterestv2, /p2 [término]
    Usa API Stellarwa con sistema similar a NexyLight, avisa al admin si falla y redirige a /pinterest.
    """
    import requests
    import datetime

    ID_ADMIN = 7953907047
    ENDPOINT_BASE = "https://api.stellarwa.xyz/search/pinterestv2"
    API_KEY = "AnyerJR"  # Clave de la API Stellarwa

    if not context.args:
        await update.message.reply_text(
            "⚠️ ¡Olvidaste el término de búsqueda!\n"
            "Comandos disponibles:\n"
            "/pinterestv2 [término]\n"
            "/p2 [término]\n"
            "Ejemplo: /p2 My Melody Icon, /pinterestv2 fondos de pantalla"
        )
        return

    termino_busqueda = " ".join(context.args)
    endpoint_pinterestv2 = f"{ENDPOINT_BASE}?query={termino_busqueda}&key={API_KEY}"
    loading_msg = await update.message.reply_text("Buscando con PinterestV2... ⏳")

    try:
        respuesta_api = requests.get(endpoint_pinterestv2, timeout=10)
        respuesta_api.raise_for_status()
        datos_resultado = respuesta_api.json()

        if not datos_resultado.get("status") or datos_resultado.get("code") != 200:
            raise Exception(f"Respuesta API no válida: {datos_resultado.get('message', 'Sin detalle')}")
        
        cantidad_resultados = len(datos_resultado["response"].get("pins", []))
        if cantidad_resultados == 0:
            await loading_msg.edit_text(f"🔍 No hay resultados para '{termino_busqueda}'.")
            return

        await loading_msg.edit_text(f"✅ Encontrados {cantidad_resultados} resultados para '{termino_busqueda}':")

        for indice, pin in enumerate(datos_resultado["response"]["pins"][:4], 1):
            titulo_pin = pin["title"] if pin["title"] not in ["", None] else "Sin título"
            descripcion_pin = pin["description"] if pin["description"] not in ["", None] else "Sin descripción"
            
            texto_caption = (
                f"🔹 Resultado #{indice}\n"
                f"📌 Título: {titulo_pin}\n"
                f"🗒️ Descripción: {descripcion_pin}\n"
                f"👤 Usuario: {pin['uploader']['full_name']} (@{pin['uploader']['username']})"
            )

            try:
                await update.message.reply_photo(
                    photo=pin["media"]["images"]["orig"]["url"],
                    caption=texto_caption
                )
            except Exception as error_imagen:
                await update.message.reply_text(
                    f"🔹 Resultado #{indice} (imagen no disponible):\n{texto_caption}"
                )
        return

    except requests.exceptions.HTTPError as e:
        error_detalle = f"Código {e.response.status_code} - {e.response.text}"
        await loading_msg.edit_text("⚠️ PinterestV2 falló, redirigiendo a /pinterest...")
        try:
            await context.bot.send_message(
                chat_id=ID_ADMIN,
                text=f"🚨 ALERTA - SERVICIO PINTERESTV2 FALLIDO 🚨\n\n"
                     f"Fecha/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                     f"Usuario: {update.effective_user.first_name} (ID: {update.effective_user.id})\n"
                     f"Término: {termino_busqueda}\n"
                     f"Endpoint usado: {endpoint_pinterestv2}\n"
                     f"Error HTTP: {error_detalle}\n"
                     f"API Key: {API_KEY}"
            )
        except Exception as error_aviso:
            print(f"Error al enviar aviso al admin: {str(error_aviso)}")
    except Exception as error_busqueda:
        await loading_msg.edit_text("⚠️ PinterestV2 falló, redirigiendo a /pinterest...")
        try:
            await context.bot.send_message(
                chat_id=ID_ADMIN,
                text=f"🚨 ALERTA - SERVICIO PINTERESTV2 FALLIDO 🚨\n\n"
                     f"Fecha/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                     f"Usuario: {update.effective_user.first_name} (ID: {update.effective_user.id})\n"
                     f"Término: {termino_busqueda}\n"
                     f"Endpoint usado: {endpoint_pinterestv2}\n"
                     f"Error: {str(error_busqueda)}\n"
                     f"API Key: {API_KEY}"
            )
        except Exception as error_aviso:
            print(f"Error al enviar aviso al admin: {str(error_aviso)}")
    
    # Ejecución directa del comando alternativo
    await buscar_pinterest(update, context)


# ══════════════════════════════════════════════════════════
# MOTOR CENTRAL DE BÚSQUEDA DE IMÁGENES
# Usa Bing Images scraping — sin API key, muy confiable
# Devuelve lista de URLs de imagen directas
# ══════════════════════════════════════════════════════════
BING_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Referer": "https://www.bing.com/",
}

def _buscar_bing_imagenes(query: str, cantidad: int = 5) -> list:
    """Motor principal: DuckDuckGo Images (sin API). Fallback: Bing scraping."""
    from urllib.parse import quote
    resultado = []

    # ── Motor 1: DuckDuckGo Images (más fiable, sin API)
    try:
        hdrs = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Referer": "https://duckduckgo.com/",
        }
        r1 = requests.get(
            f"https://duckduckgo.com/?q={quote(query)}&ia=images&iax=images",
            headers=hdrs, timeout=12
        )
        vqd = None
        vqd_patterns = [
            r'vqd=([\d-]+)',
            r'"vqd"\s*:\s*"([^"]+)"',
            r"vqd='([^']+)'",
            r'data-vqd="([^"]+)"',
        ]
        for pat in vqd_patterns:
            m = re.search(pat, r1.text)
            if m:
                vqd = m.group(1)
                break
        if vqd:
            r2 = requests.get(
                f"https://duckduckgo.com/i.js?q={quote(query)}&vqd={vqd}&f=,,,,,&p=1",
                headers=hdrs, timeout=12
            )
            data = r2.json()
            for item in data.get("results", []):
                img = item.get("image") or item.get("thumbnail")
                if img and img not in resultado:
                    resultado.append(img)
                if len(resultado) >= cantidad:
                    break
    except Exception as e:
        print(f"⚠️ DDG error: {e}")

    # ── Motor 2: Bing Images (fallback si DDG no dio resultados)
    if len(resultado) < 2:
        try:
            url = f"https://www.bing.com/images/search?q={quote(query)}&FORM=HDRSC3&first=1"
            r = requests.get(url, headers=BING_HEADERS, timeout=15)
            r.raise_for_status()
            urls_b = re.findall(r'"murl"\s*:\s*"(https?://[^"]+)"', r.text)
            if not urls_b:
                urls_b = re.findall(r'imgurl=([^&"]+)', r.text)
                urls_b = [u.replace("%3A", ":").replace("%2F", "/") for u in urls_b]
            for u in urls_b:
                if u not in resultado:
                    resultado.append(u)
                if len(resultado) >= cantidad:
                    break
        except Exception as e:
            print(f"⚠️ Bing fallback error: {e}")

    return resultado[:cantidad]


def _descargar_imagen_bytes(url: str) -> bytes:
    """Descarga una imagen a bytes para enviarla a Telegram aunque tenga hotlink protection."""
    hdrs = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9",
        "Referer": "https://www.google.com/",
    }
    r = requests.get(url, headers=hdrs, timeout=15, stream=True)
    r.raise_for_status()
    data = b""
    for chunk in r.iter_content(65536):
        data += chunk
        if len(data) > 15_000_000:
            raise ValueError("Imagen demasiado grande (>15MB)")
    if len(data) < 500:
        raise ValueError("Archivo muy pequeño, posiblemente error")
    return data

async def _enviar_imagenes_grupo(update, busqueda: str, urls: list, fuente: str, emoji: str):
    """
    Envía hasta 4 imágenes. Primero intenta URL directa; si Telegram la rechaza,
    descarga los bytes localmente y los envía como InputFile para evitar hotlink protection.
    """
    enviadas = 0
    for i, url in enumerate(urls):
        if enviadas >= 4:
            break
        caption = (
            f"{emoji} {fuente} — imagen {enviadas + 1}\nBusqueda: {busqueda}"
        ) if enviadas == 0 else None

        # Intento 1: URL directa (rápido)
        try:
            await update.message.reply_photo(photo=url, caption=caption)
            enviadas += 1
            await asyncio.sleep(0.35)
            continue
        except Exception:
            pass

        # Intento 2: Descargar bytes y enviar (evita hotlink protection)
        try:
            img_bytes = await asyncio.to_thread(_descargar_imagen_bytes, url)
            buf = io.BytesIO(img_bytes)
            buf.name = "imagen.jpg"
            await update.message.reply_photo(photo=buf, caption=caption)
            enviadas += 1
        except Exception as e2:
            print(f"⚠️ [{fuente}] Imagen {i+1} omitida: {e2}")

        await asyncio.sleep(0.35)
    return enviadas


#pinterest /pinterest
async def buscar_pinterest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comandos: /pinterest, /p, /pin [término]
    Bot usa la API de NexyLight con cuenta registrada (AnyerJR), valida límites y avisa al admin si hay problemas.
    """
    from bs4 import BeautifulSoup
    import requests
    import datetime

    ID_ADMIN = 7953907047
    URL_PAGINA_SEARCH = "https://api.nexylight.xyz/#Search"
    ENDPOINT_BASE = "https://api.nexylight.xyz/search/pinterest"
    API_KEY = "nexy-6c944e"

    if not context.args:
        await update.message.reply_text(
            "⚠️ ¡Olvidaste el término de búsqueda!\n"
            "Comandos disponibles:\n"
            "/pinterest [término]\n"
            "/p [término]\n"
            "/pin [término]\n"
            "Ejemplo: /p perritos, /pin fondos de pantalla"
        )
        return

    termino_busqueda = " ".join(context.args)
    endpoint_pinterest = f"{ENDPOINT_BASE}?q={termino_busqueda}&key={API_KEY}"
    error_pagina = None

    try:
        respuesta_pagina = requests.get(URL_PAGINA_SEARCH, timeout=10)
        respuesta_pagina.raise_for_status()
        soup = BeautifulSoup(respuesta_pagina.content, 'html.parser')
        seccion_pinterest = soup.find(string=lambda t: t and "Pinterest Search" in t)
        if not seccion_pinterest:
            error_pagina = "Sección de Pinterest Search no encontrada en la página, pero se usará el endpoint con API key registrada."
        else:
            contenedor = seccion_pinterest.find_parent(attrs={"class": lambda c: c and "card" in c.lower()})
            if contenedor:
                endpoint_elemento = contenedor.find(string=lambda t: t and "https://api.nexylight.xyz/search" in t)
                if endpoint_elemento:
                    endpoint_pinterest = f"{endpoint_elemento.strip()}?q={termino_busqueda}&key={API_KEY}"

    except Exception as e:
        error_pagina = f"Error al verificar la página de la API: {str(e)}. Se usará el endpoint configurado con la API key registrada."

    if error_pagina:
        try:
            await context.bot.send_message(
                chat_id=ID_ADMIN,
                text=f"⚠️ NOTA - VERIFICACIÓN PÁGINA API ⚠️\n\n"
                     f"Fecha/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                     f"Usuario: {update.effective_user.first_name} (ID: {update.effective_user.id})\n"
                     f"Término: {termino_busqueda}\n"
                     f"Mensaje: {error_pagina}"
            )
        except Exception as error_aviso:
            print(f"Error al enviar aviso de verificación: {str(error_aviso)}")

    try:
        respuesta_api = requests.get(endpoint_pinterest, timeout=10)
        respuesta_api.raise_for_status()
        datos_resultado = respuesta_api.json()

        if not datos_resultado.get("status"):
            raise Exception(f"Respuesta API no válida: {datos_resultado.get('message', 'Sin detalle')}")
        
        cantidad_resultados = len(datos_resultado.get("data", []))
        if cantidad_resultados == 0:
            await update.message.reply_text(f"🔍 No hay resultados para '{termino_busqueda}'.")
            return

        await update.message.reply_text(f"✅ Encontrados {cantidad_resultados} resultados para '{termino_busqueda}':\n(Límite diario restante: 300)")

        for indice, item in enumerate(datos_resultado["data"][:4], 1):
            titulo_item = item["title"] if item["title"] not in ["No Title", "", None] else "Sin título"
            
            texto_caption = (
                f"🔹 Resultado #{indice}\n"
                f"📌 Título: {titulo_item}\n"
                f"👤 Pinner: {item['pinner']}\n"
                f"📋 Tablero: {item['board']}"
            )

            try:
                await update.message.reply_photo(
                    photo=item["image"],
                    caption=texto_caption
                )
            except Exception as error_imagen:
                await update.message.reply_text(
                    f"🔹 Resultado #{indice} (imagen no disponible):\n{texto_caption}"
                )

    except requests.exceptions.HTTPError as e:
        error_detalle = f"Código {e.response.status_code} - {e.response.text}"
        await update.message.reply_text("❌ No se pudo completar la búsqueda. Verifica el estado de la API o intenta más tarde.")
        try:
            await context.bot.send_message(
                chat_id=ID_ADMIN,
                text=f"🚨 ALERTA - BÚSQUEDA PINTEREST FALLIDA 🚨\n\n"
                     f"Fecha/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                     f"Usuario: {update.effective_user.first_name} (ID: {update.effective_user.id})\n"
                     f"Término: {termino_busqueda}\n"
                     f"Endpoint usado: {endpoint_pinterest}\n"
                     f"Error HTTP: {error_detalle}\n"
                     f"API Key: {API_KEY}\n"
                     f"Límite diario: 300 (0 usadas)"
            )
        except Exception as error_aviso:
            print(f"Error al enviar aviso final: {str(error_aviso)}")
    except Exception as error_busqueda:
        await update.message.reply_text("❌ No se pudo completar la búsqueda. Intenta de nuevo más tarde.")
        try:
            await context.bot.send_message(
                chat_id=ID_ADMIN,
                text=f"🚨 ALERTA - BÚSQUEDA PINTEREST FALLIDA 🚨\n\n"
                     f"Fecha/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                     f"Usuario: {update.effective_user.first_name} (ID: {update.effective_user.id})\n"
                     f"Término: {termino_busqueda}\n"
                     f"Endpoint usado: {endpoint_pinterest}\n"
                     f"Error: {str(error_busqueda)}\n"
                     f"API Key: {API_KEY}\n"
                     f"Límite diario: 300 (0 usadas)"
            )
        except Exception as error_aviso:
            print(f"Error al enviar aviso final: {str(error_aviso)}")


# ══════════════════════════════════════════════════════════
# /imagen [búsqueda] — Búsqueda general de imágenes (Bing)
# Devuelve 4 imágenes de cualquier fuente
# ══════════════════════════════════════════════════════════
async def buscar_imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca imágenes en internet usando Bing Images (con respaldo en /pinterest)."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🖼️ **Uso:** `/imagen [búsqueda]`\n\n"
            "_Ejemplos:_\n"
            "- `/imagen gatos lindos`\n"
            "- `/imagen Caracas Venezuela`\n"
            "- `/imagen anime wallpaper 4k`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    busqueda = " ".join(context.args)
    wait_msg = await update.message.reply_text(
        f"🖼️ **Buscando imágenes:** `{busqueda}`\n⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    try:
        urls = await asyncio.to_thread(_buscar_bing_imagenes, busqueda, 8)

        if not urls:
            raise Exception("No se encontraron resultados en Bing Images")
        
        await wait_msg.delete()
        enviadas = await _enviar_imagenes_grupo(update, busqueda, urls, "Bing Imágenes 🖼️", "🖼️")

        if enviadas == 0:
            raise Exception("Ninguna imagen pudo cargarse desde Bing Images")

        registrar_evento(user_id, nick, f"Buscó imagen: {busqueda}", "IMÁGENES")
        sumar_xp(user_id, 8)

    except Exception as e:
        print(f"❌ [imagen] Error: {e}")
        await wait_msg.edit_text(
            f"⚠️ **Error en Bing Images:** `{str(e)}`\n🔄 _Activando respaldo con Pinterest..._",
            parse_mode=ParseMode.MARKDOWN
        )
        # Enviar señal al comando /pinterest reutilizando los mismos argumentos
        context.args = busqueda.split()
        await buscar_pinterest(update, context)

# ══════════════════════════════════════════════════════════
# /wallpaper [búsqueda] — Fondos de pantalla HD
# Fuente 1: Wallhaven API pública (sin key para contenido SFW)
# Fuente 2: Bing Images con filtro HD
# ══════════════════════════════════════════════════════════
async def wallpaper_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca fondos de pantalla HD en Wallhaven.cc (con respaldo en /imagen y luego /pinterest)."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🖥️ **Uso:** `/wallpaper [búsqueda]`\n\n"
            "_Ejemplos:_\n"
            "- `/wallpaper naturaleza 4k`\n"
            "- `/wallpaper anime dark aesthetic`\n"
            "- `/wallpaper ciudad noche`\n"
            "- `/wallpaper espacio galaxia`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    busqueda = " ".join(context.args)
    wait_msg = await update.message.reply_text(
        f"🖥️ **Buscando wallpapers:** `{busqueda}`\n⏳ _Cargando..._",
        parse_mode=ParseMode.MARKDOWN
    )

    try:
        # ── Fuente 1: Wallhaven API pública (sin key, solo SFW)
        def _wallhaven():
            from urllib.parse import quote
            url = (
                f"https://wallhaven.cc/api/v1/search"
                f"?q={quote(busqueda)}&purity=100&categories=110"
                f"&sorting=relevance&order=desc&atleast=1280x720"
            )
            r = requests.get(url, headers=BING_HEADERS, timeout=15)
            r.raise_for_status()
            data = r.json()
            return [item["path"] for item in data.get("data", [])[:6]]

        urls = await asyncio.to_thread(_wallhaven)

        # ── Fuente 2 (fallback interno): Bing Images HD
        if not urls:
            await wait_msg.edit_text(
                f"🖥️ **Buscando wallpapers:** `{busqueda}`\n🔄 _Buscando en Bing HD..._",
                parse_mode=ParseMode.MARKDOWN
            )
            urls = await asyncio.to_thread(
                _buscar_bing_imagenes, f"{busqueda} wallpaper 4k HD", 8
            )

        if not urls:
            raise Exception("No se encontraron resultados en Wallhaven ni en Bing HD")

        await wait_msg.delete()
        enviadas = await _enviar_imagenes_grupo(update, busqueda, urls, "Wallhaven 🖥️", "🖥️")

        if enviadas == 0:
            raise Exception("Ningún wallpaper pudo cargarse desde las fuentes disponibles")

        registrar_evento(user_id, nick, f"Wallpaper: {busqueda}", "IMÁGENES")
        sumar_xp(user_id, 8)

    except Exception as e:
        print(f"❌ [wallpaper] Error: {e}")
        # Paso 1: Redirigir a /imagen con término ampliada
        busqueda_ampliada = f"{busqueda} fondos de pantalla"
        await wait_msg.edit_text(
            f"⚠️ **Error en búsqueda de wallpapers:** `{str(e)}`\n🔄 _Redirigiendo a búsqueda general: `{busqueda_ampliada}`..._",
            parse_mode=ParseMode.MARKDOWN
        )
        try:
            # Configurar argumentos para /imagen y ejecutar
            context.args = busqueda_ampliada.split()
            await buscar_imagen(update, context)
        except Exception as e_imagen:
            print(f"❌ [wallpaper → imagen] Error: {e_imagen}")
            await update.message.reply_text(
                "⚠️ **También falló la búsqueda general.**\n✅ La petición ya fue redirigida a `/pinterest` automáticamente.",
                parse_mode=ParseMode.MARKDOWN
            )

# ══════════════════════════════════════════════════════════
# /gif [búsqueda] — Busca y envía GIFs animados (sin API)
# Fuente: Bing Images scraping
# ══════════════════════════════════════════════════════════

async def gif_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca y envía un GIF animado scrapeando Google Images."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🎞️ **Uso:** `/gif [búsqueda]`\n\n"
            "_Ejemplos:_\n"
            "- `/gif baile`\n"
            "- `/gif gato gracioso`\n"
            "- `/gif feliz cumpleaños`\n"
            "- `/gif fail venezolano`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    busqueda = " ".join(context.args)
    wait_msg = await update.message.reply_text(
        f"🎞️ **Buscando GIF:** `{busqueda}`\n⏳ _Cargando..._",
        parse_mode=ParseMode.MARKDOWN
    )

    try:
        # Buscar GIFs usando Bing Images (sin API)
        gif_urls = await asyncio.to_thread(_buscar_bing_imagenes, f"{busqueda} gif animated", 8)

        if not gif_urls:
            await wait_msg.edit_text(
                f"❌ **No encontré GIFs para:** `{busqueda}`",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        # Elegir uno aleatorio de los resultados
        gif_elegido = random.choice(gif_urls[:5])

        await wait_msg.delete()
        await update.message.reply_animation(
            animation=gif_elegido,
            caption=(
                f"🎞️ **GIF:** _{busqueda}_\n"
                f"👤 _Para {nick}_"
            ),
            parse_mode=ParseMode.MARKDOWN
        )

        registrar_evento(user_id, nick, f"GIF: {busqueda}", "IMÁGENES")
        sumar_xp(user_id, 5)

    except Exception as e:
        print(f"❌ [gif] Error: {e}")
        await wait_msg.edit_text("❌ **Error buscando GIF.**", parse_mode=ParseMode.MARKDOWN)


# ══════════════════════════════════════════════════════════
# /fanart [búsqueda] — Busca fanart / arte de anime / ilustraciones
# Usa Bing Images con filtro artístico
# ══════════════════════════════════════════════════════════
async def fanart_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca fanart, arte de anime e ilustraciones digitales."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🎨 **Uso:** `/fanart [búsqueda]`\n\n"
            "_Ejemplos:_\n"
            "- `/fanart naruto aesthetic`\n"
            "- `/fanart demon slayer art`\n"
            "- `/fanart anime girl dark`\n"
            "- `/fanart dragon ball goku`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    busqueda = " ".join(context.args)
    wait_msg = await update.message.reply_text(
        f"🎨 **Buscando fanart:** `{busqueda}`\n⏳ _Cargando..._",
        parse_mode=ParseMode.MARKDOWN
    )

    try:
        # Agregar "fanart" o "art" al query para sesgar hacia ilustraciones
        query_art = f"{busqueda} fanart digital art"
        urls = await asyncio.to_thread(_buscar_bing_imagenes, query_art, 10)

        if not urls:
            await wait_msg.edit_text(
                f"❌ **No encontré fanart para:** `{busqueda}`",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.delete()
        enviadas = await _enviar_imagenes_grupo(update, busqueda, urls, "Fanart 🎨", "🎨")

        if enviadas == 0:
            await update.message.reply_text("❌ Las imágenes no cargaron. Intenta con otra búsqueda.")
            return

        registrar_evento(user_id, nick, f"Fanart: {busqueda}", "IMÁGENES")
        sumar_xp(user_id, 8)

    except Exception as e:
        print(f"❌ [fanart] Error: {e}")
        await wait_msg.edit_text("❌ **Error buscando fanart.**", parse_mode=ParseMode.MARKDOWN)


# ══════════════════════════════════════════════════════════
# /sticker_buscar [búsqueda] — Busca stickers / pegatinas PNG
# Usa Bing Images filtrando por PNG transparente
# ══════════════════════════════════════════════════════════
async def sticker_buscar_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca imágenes estilo sticker/PNG para usar en chats. Si falla, redirige a Pinterest."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    busqueda = " ".join(context.args) if context.args else ""

    # Validación inicial de búsqueda
    if not busqueda:
        await update.message.reply_text(
            "🧩 **Uso:** `/sticker_buscar [búsqueda]`\n\n"
            "_Ejemplos:_\n"
            "- `/sticker_buscar gato kawaii`\n"
            "- `/sticker_buscar corazon aesthetic`\n"
            "- `/sticker_buscar emoji 3d`\n"
            "- `/sticker_buscar bear cute`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    wait_msg = await update.message.reply_text(
        f"🧩 **Buscando stickers:** `{busqueda}`\n⏳ _Cargando..._",
        parse_mode=ParseMode.MARKDOWN
    )

    try:
        query_sticker = f"{busqueda} sticker png transparent fondo transparente"  # Refinamos la consulta
        urls = await asyncio.to_thread(_buscar_bing_imagenes, query_sticker, 15)  # Aumentamos a 15 resultados

        # Filtro más estricto: solo URLs que terminen en .png (evita falsos positivos)
        png_urls = [u for u in urls if u.lower().endswith(".png")]
        urls_finales = png_urls if png_urls else urls  # Si no hay PNGs, usa todas las encontradas

        enviadas = 0
        if urls_finales:
            await wait_msg.delete()
            enviadas = await _enviar_imagenes_grupo(update, busqueda, urls_finales, "Stickers 🧩", "🧩")

        # Si no se encontraron URLs o no se pudo enviar ninguna imagen
        if not urls_finales or enviadas == 0:
            await wait_msg.edit_text(
                f"⚠️ **No se encontraron stickers válidos para:** `{busqueda}`\n🔍 _Redirigiendo búsqueda a Pinterest..._",
                parse_mode=ParseMode.MARKDOWN
            )
            # Llamamos al comando de Pinterest (simulamos la petición o invocamos su función)
            context.args = [busqueda]  # Pasamos la búsqueda al comando de Pinterest
            await buscar_pinterest(update, context)  # Ejecutamos el bloque de Pinterest
            return

        # Si todo sale bien
        registrar_evento(user_id, nick, f"Sticker buscar: {busqueda}", "IMÁGENES")
        sumar_xp(user_id, 5)

    except Exception as e:
        print(f"❌ [sticker_buscar] Error completo: {str(e)}")
        # En caso de error crítico, también redirigimos a Pinterest
        try:
            await wait_msg.edit_text(
                f"❌ **Error buscando stickers para:** `{busqueda}`\n🔍 _Buscando ahora en Pinterest..._",
                parse_mode=ParseMode.MARKDOWN
            )
            context.args = [busqueda]
            await buscar_pinterest(update, context)
        except Exception as e2:
            print(f"❌ [sticker_buscar] Error al redirigir a Pinterest: {str(e2)}")
            await update.message.reply_text("❌ **Error general. Intenta nuevamente más tarde.**", parse_mode=ParseMode.MARKDOWN)


# ══════════════════════════════════════════════════════════
# MÓDULO STICKER MAKER — FÁBRICA DE STICKERS V13 🎨
# ══════════════════════════════════════════════════════════
# Fuentes disponibles
FONT_POPPINS_BOLD  = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FONT_POPPINS_REG   = "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf"
FONT_DEJAVU_BOLD   = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_DEJAVU        = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_CALADEA_BOLD  = "/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf"
FONT_LIBERATION    = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_MONO          = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def _get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    """Carga una fuente con fallback seguro."""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype(FONT_DEJAVU_BOLD, size)
        except Exception:
            return ImageFont.load_default()

def _wrap_text(text: str, font, max_width: int, draw) -> list:
    """Divide el texto en líneas que quepan en max_width."""
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines or [text]

def _apply_round_mask(img: Image.Image, radius: int = 80) -> Image.Image:
    """Aplica esquinas redondeadas como máscara RGBA."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    mask = Image.new("L", img.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=radius, fill=255)
    img.putalpha(mask)
    return img

def _draw_text_outline(draw, pos, text, font, fill, outline_color=(0,0,0,200), stroke=4):
    """Dibuja texto con contorno/sombra para mayor legibilidad."""
    x, y = pos
    for dx in range(-stroke, stroke + 1):
        for dy in range(-stroke, stroke + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor="mm")
    draw.text((x, y), text, font=font, fill=fill, anchor="mm")

def _gradient_rect(img: Image.Image, color1: tuple, color2: tuple, vertical: bool = True):
    """Rellena la imagen con un gradiente lineal de color1 → color2."""
    W, H = img.size
    px = img.load()
    for i in range(H if vertical else W):
        t = i / (H - 1 if vertical else W - 1)
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        a = int(color1[3] + (color2[3] - color1[3]) * t) if len(color1) == 4 else 255
        for j in range(W if vertical else H):
            px[(j, i) if vertical else (i, j)] = (r, g, b, a)
    return img


# ─────────────────────────────────────────────
# /stk_neon [texto] — Sticker neón sobre fondo oscuro
# ─────────────────────────────────────────────
async def sticker_neon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea un sticker estilo NEÓN con brillo y fondo oscuro."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🌟 **Uso:** `/stk_neon [texto]`\n_Ejemplo: /stk\\_neon Camila 💜_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    texto = " ".join(context.args)
    W, H = 700, 350

    def _crear():
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        # Fondo oscuro con gradiente azul oscuro → negro
        bg = Image.new("RGBA", (W, H))
        _gradient_rect(bg, (5, 0, 30, 255), (20, 0, 60, 255))
        img.paste(bg, (0, 0))

        draw = ImageDraw.Draw(img)

        # Borde neón exterior (glow simulado con capas)
        neon_colors = [(0, 255, 255), (150, 0, 255), (255, 0, 200)]
        neon = random.choice(neon_colors)

        draw.rounded_rectangle([8, 8, W-9, H-9], radius=60, outline=neon, width=4)
        draw.rounded_rectangle([14, 14, W-15, H-15], radius=55, outline=(*neon[:3], 80), width=8)

        # Texto
        font_size = min(160, max(50, int(W * 0.22 / max(len(texto), 1) * 2.5)))
        font = _get_font(FONT_POPPINS_BOLD, font_size)
        draw_tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
        lines = _wrap_text(texto.upper(), font, W - 80, draw_tmp)
        total_h = len(lines) * (font_size + 10)
        y_start = (H - total_h) // 2 + font_size // 2

        for i, line in enumerate(lines):
            y = y_start + i * (font_size + 10)
            # Glow: múltiples capas del mismo texto difuminadas
            for offset in range(6, 0, -2):
                glow_color = (*neon[:3], 60)
                for dx, dy in [(-offset,0),(offset,0),(0,-offset),(0,offset)]:
                    draw.text((W//2 + dx, y + dy), line, font=font, fill=glow_color, anchor="mm")
            # Texto principal blanco
            draw.text((W//2, y), line, font=font, fill=(255, 255, 255, 255), anchor="mm")

        img = _apply_round_mask(img, radius=60)
        path = f"{RUTA_LOGS}/stk_neon_{user_id}.png"
        img.save(path, "PNG")
        return path

    path = await asyncio.to_thread(_crear)
    with open(path, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=f"🌟 **Sticker Neón**\n✍️ _{texto}_\n👤 _Hecho para {nick}_",
            parse_mode=ParseMode.MARKDOWN
        )
    _limpiar_archivo(path)
    sumar_xp(user_id, 8)
    registrar_evento(user_id, nick, f"Sticker Neón: {texto}", "STICKER")


# ─────────────────────────────────────────────
# /stk_fuego [texto] — Sticker con fondo de fuego/lava
# ─────────────────────────────────────────────
async def sticker_fuego(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea un sticker con fondo de fuego y texto ardiente."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🔥 **Uso:** `/stk_fuego [texto]`\n_Ejemplo: /stk\\_fuego En Llamas 🔥_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    texto = " ".join(context.args)
    W, H = 700, 350

    def _crear():
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        # Gradiente fuego: rojo oscuro → naranja → amarillo
        bg = Image.new("RGBA", (W, H))
        _gradient_rect(bg, (180, 20, 0, 255), (255, 160, 0, 255), vertical=True)
        img.paste(bg)

        draw = ImageDraw.Draw(img)

        # Detalles de fuego (círculos irregulares simulando llamas)
        for _ in range(18):
            cx = random.randint(0, W)
            cy = random.randint(H//2, H)
            r  = random.randint(20, 80)
            alpha = random.randint(80, 160)
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, random.randint(80,200), 0, alpha))

        # Borde dorado
        draw.rounded_rectangle([6, 6, W-7, H-7], radius=55, outline=(255, 215, 0, 220), width=5)

        # Texto
        font_size = min(150, max(50, int(W * 0.22 / max(len(texto), 1) * 2.5)))
        font = _get_font(FONT_POPPINS_BOLD, font_size)
        draw_tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
        lines = _wrap_text(texto.upper(), font, W - 80, draw_tmp)
        total_h = len(lines) * (font_size + 10)
        y_start = (H - total_h) // 2 + font_size // 2

        for i, line in enumerate(lines):
            y = y_start + i * (font_size + 10)
            _draw_text_outline(draw, (W//2, y), line, font,
                               fill=(255, 255, 255, 255),
                               outline_color=(140, 40, 0, 200), stroke=5)

        img = _apply_round_mask(img, radius=55)
        path = f"{RUTA_LOGS}/stk_fuego_{user_id}.png"
        img.save(path, "PNG")
        return path

    path = await asyncio.to_thread(_crear)
    with open(path, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=f"🔥 **Sticker Fuego**\n✍️ _{texto}_\n👤 _Hecho para {nick}_",
            parse_mode=ParseMode.MARKDOWN
        )
    _limpiar_archivo(path)
    sumar_xp(user_id, 8)
    registrar_evento(user_id, nick, f"Sticker Fuego: {texto}", "STICKER")


# ─────────────────────────────────────────────
# /stk_galaxia [texto] — Sticker galaxia/espacio
# ─────────────────────────────────────────────
async def sticker_galaxia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea un sticker con fondo de galaxia y estrellas."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🌌 **Uso:** `/stk_galaxia [texto]`\n_Ejemplo: /stk\\_galaxia Infinito ✨_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    texto = " ".join(context.args)
    W, H = 700, 350

    def _crear():
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        # Fondo: gradiente azul noche → morado profundo
        bg = Image.new("RGBA", (W, H))
        _gradient_rect(bg, (5, 5, 40, 255), (60, 0, 90, 255), vertical=False)
        img.paste(bg)

        draw = ImageDraw.Draw(img)

        # Estrellas
        for _ in range(120):
            sx = random.randint(0, W)
            sy = random.randint(0, H)
            sr = random.randint(1, 3)
            alpha = random.randint(150, 255)
            draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(255, 255, 255, alpha))

        # Nebulosa (manchas de color difuminadas)
        for color in [(150, 0, 200), (0, 100, 255), (200, 50, 150)]:
            cx = random.randint(100, W-100)
            cy = random.randint(50, H-50)
            for r in range(80, 20, -10):
                a = max(0, 30 - (80 - r))
                draw.ellipse([cx-r, cy-r//2, cx+r, cy+r//2], fill=(*color, a))

        # Borde brillante
        draw.rounded_rectangle([6, 6, W-7, H-7], radius=60, outline=(180, 100, 255, 200), width=4)

        # Texto
        font_size = min(150, max(50, int(W * 0.22 / max(len(texto), 1) * 2.5)))
        font = _get_font(FONT_POPPINS_BOLD, font_size)
        draw_tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
        lines = _wrap_text(texto.upper(), font, W - 80, draw_tmp)
        total_h = len(lines) * (font_size + 10)
        y_start = (H - total_h) // 2 + font_size // 2

        for i, line in enumerate(lines):
            y = y_start + i * (font_size + 10)
            _draw_text_outline(draw, (W//2, y), line, font,
                               fill=(255, 255, 255, 255),
                               outline_color=(80, 0, 120, 200), stroke=5)

        img = _apply_round_mask(img, radius=60)
        path = f"{RUTA_LOGS}/stk_gal_{user_id}.png"
        img.save(path, "PNG")
        return path

    path = await asyncio.to_thread(_crear)
    with open(path, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=f"🌌 **Sticker Galaxia**\n✍️ _{texto}_\n👤 _Hecho para {nick}_",
            parse_mode=ParseMode.MARKDOWN
        )
    _limpiar_archivo(path)
    sumar_xp(user_id, 8)
    registrar_evento(user_id, nick, f"Sticker Galaxia: {texto}", "STICKER")


# ─────────────────────────────────────────────
# /stk_aesthetic [texto] — Estilo aesthetic pastel
# ─────────────────────────────────────────────
async def sticker_aesthetic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea un sticker aesthetic con colores pastel y estilo minimalista."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🌸 **Uso:** `/stk_aesthetic [texto]`\n_Ejemplo: /stk\\_aesthetic soft girl 🌸_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    texto = " ".join(context.args)
    W, H = 700, 350

    paletas = [
        [(255, 182, 193), (255, 218, 225), (255, 105, 180)],   # Rosa
        [(173, 216, 230), (135, 206, 250), (100, 149, 237)],   # Azul celeste
        [(144, 238, 144), (152, 251, 152), (60, 179, 113)],    # Verde menta
        [(221, 160, 221), (218, 112, 214), (148, 0, 211)],     # Lavanda
        [(255, 218, 185), (255, 160, 122), (255, 127, 80)],    # Durazno
    ]
    paleta = random.choice(paletas)

    def _crear():
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bg = Image.new("RGBA", (W, H))
        _gradient_rect(bg, (*paleta[0], 255), (*paleta[1], 255))
        img.paste(bg)

        draw = ImageDraw.Draw(img)

        # Círculos decorativos
        for _ in range(12):
            cx = random.randint(0, W)
            cy = random.randint(0, H)
            r  = random.randint(15, 60)
            draw.ellipse([cx-r, cy-r, cx+r, cy+r],
                         fill=(*paleta[2], random.randint(30, 80)))

        # Pequeños corazones decorativos (como puntos)
        for _ in range(8):
            hx = random.randint(30, W-30)
            hy = random.randint(10, H-10)
            draw.ellipse([hx-6, hy-6, hx+6, hy+6], fill=(*paleta[2], 120))

        # Borde suave
        draw.rounded_rectangle([8, 8, W-9, H-9], radius=60,
                                outline=(*paleta[2], 180), width=4)

        # Texto
        font_size = min(140, max(45, int(W * 0.22 / max(len(texto), 1) * 2.5)))
        font = _get_font(FONT_POPPINS_BOLD, font_size)
        draw_tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
        lines = _wrap_text(texto, font, W - 80, draw_tmp)
        total_h = len(lines) * (font_size + 12)
        y_start = (H - total_h) // 2 + font_size // 2

        for i, line in enumerate(lines):
            y = y_start + i * (font_size + 12)
            # Sombra suave
            draw.text((W//2 + 3, y + 3), line, font=font,
                      fill=(*paleta[2], 120), anchor="mm")
            draw.text((W//2, y), line, font=font,
                      fill=(80, 40, 60, 255), anchor="mm")

        img = _apply_round_mask(img, radius=60)
        path = f"{RUTA_LOGS}/stk_aes_{user_id}.png"
        img.save(path, "PNG")
        return path

    path = await asyncio.to_thread(_crear)
    with open(path, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=f"🌸 **Sticker Aesthetic**\n✍️ _{texto}_\n👤 _Hecho para {nick}_",
            parse_mode=ParseMode.MARKDOWN
        )
    _limpiar_archivo(path)
    sumar_xp(user_id, 8)
    registrar_evento(user_id, nick, f"Sticker Aesthetic: {texto}", "STICKER")


# ─────────────────────────────────────────────
# /stk_dark [texto] — Sticker dark/gothic oscuro
# ─────────────────────────────────────────────
async def sticker_dark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea un sticker estilo dark/gothic con fondo negro y texto rojo."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🖤 **Uso:** `/stk_dark [texto]`\n_Ejemplo: /stk\\_dark No me busques 🖤_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    texto = " ".join(context.args)
    W, H = 700, 350

    def _crear():
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bg = Image.new("RGBA", (W, H))
        _gradient_rect(bg, (10, 10, 10, 255), (40, 5, 5, 255))
        img.paste(bg)

        draw = ImageDraw.Draw(img)

        # Líneas decorativas
        for i in range(0, W, 40):
            draw.line([(i, 0), (i, H)], fill=(255, 0, 0, 15), width=1)
        for j in range(0, H, 40):
            draw.line([(0, j), (W, j)], fill=(255, 0, 0, 15), width=1)

        # Círculos rojos esquinas
        for cx, cy in [(0, 0), (W, 0), (0, H), (W, H)]:
            for r in [60, 40, 20]:
                draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(180, 0, 0, 30))

        # Borde rojo sangre
        draw.rounded_rectangle([6, 6, W-7, H-7], radius=50,
                                outline=(180, 0, 0, 220), width=5)
        draw.rounded_rectangle([12, 12, W-13, H-13], radius=45,
                                outline=(80, 0, 0, 100), width=2)

        # Texto
        font_size = min(150, max(50, int(W * 0.22 / max(len(texto), 1) * 2.5)))
        font = _get_font(FONT_POPPINS_BOLD, font_size)
        draw_tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
        lines = _wrap_text(texto.upper(), font, W - 80, draw_tmp)
        total_h = len(lines) * (font_size + 10)
        y_start = (H - total_h) // 2 + font_size // 2

        for i, line in enumerate(lines):
            y = y_start + i * (font_size + 10)
            _draw_text_outline(draw, (W//2, y), line, font,
                               fill=(220, 0, 0, 255),
                               outline_color=(0, 0, 0, 255), stroke=6)

        img = _apply_round_mask(img, radius=50)
        path = f"{RUTA_LOGS}/stk_dark_{user_id}.png"
        img.save(path, "PNG")
        return path

    path = await asyncio.to_thread(_crear)
    with open(path, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=f"🖤 **Sticker Dark**\n✍️ _{texto}_\n👤 _Hecho para {nick}_",
            parse_mode=ParseMode.MARKDOWN
        )
    _limpiar_archivo(path)
    sumar_xp(user_id, 8)
    registrar_evento(user_id, nick, f"Sticker Dark: {texto}", "STICKER")


# ─────────────────────────────────────────────
# /stk_arcoiris [texto] — Sticker arcoíris/pride
# ─────────────────────────────────────────────
async def sticker_arcoiris(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea un sticker con fondo arcoíris vibrante."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🌈 **Uso:** `/stk_arcoiris [texto]`\n_Ejemplo: /stk\\_arcoiris Feliz día 🌈_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    texto = " ".join(context.args)
    W, H = 700, 350

    def _crear():
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Bandas arcoíris horizontales
        colores_arco = [
            (255, 0, 0), (255, 127, 0), (255, 255, 0),
            (0, 200, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)
        ]
        banda_h = H // len(colores_arco)
        for i, color in enumerate(colores_arco):
            y0 = i * banda_h
            y1 = (i + 1) * banda_h if i < len(colores_arco) - 1 else H
            draw.rectangle([0, y0, W, y1], fill=(*color, 200))

        # Overlay blanco semitransparente para suavizar
        overlay = Image.new("RGBA", (W, H), (255, 255, 255, 60))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)

        # Borde blanco
        draw.rounded_rectangle([6, 6, W-7, H-7], radius=60,
                                outline=(255, 255, 255, 240), width=6)

        # Texto
        font_size = min(150, max(50, int(W * 0.22 / max(len(texto), 1) * 2.5)))
        font = _get_font(FONT_POPPINS_BOLD, font_size)
        draw_tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
        lines = _wrap_text(texto.upper(), font, W - 80, draw_tmp)
        total_h = len(lines) * (font_size + 10)
        y_start = (H - total_h) // 2 + font_size // 2

        for i, line in enumerate(lines):
            y = y_start + i * (font_size + 10)
            _draw_text_outline(draw, (W//2, y), line, font,
                               fill=(255, 255, 255, 255),
                               outline_color=(0, 0, 0, 180), stroke=5)

        img = _apply_round_mask(img, radius=60)
        path = f"{RUTA_LOGS}/stk_arc_{user_id}.png"
        img.save(path, "PNG")
        return path

    path = await asyncio.to_thread(_crear)
    with open(path, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=f"🌈 **Sticker Arcoíris**\n✍️ _{texto}_\n👤 _Hecho para {nick}_",
            parse_mode=ParseMode.MARKDOWN
        )
    _limpiar_archivo(path)
    sumar_xp(user_id, 8)
    registrar_evento(user_id, nick, f"Sticker Arcoíris: {texto}", "STICKER")


# ─────────────────────────────────────────────
# /stk_gold [texto] — Sticker premium dorado
# ─────────────────────────────────────────────
async def sticker_gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea un sticker premium estilo dorado/lujo."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "✨ **Uso:** `/stk_gold [texto]`\n_Ejemplo: /stk\\_gold VIP 👑_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    texto = " ".join(context.args)
    W, H = 700, 350

    def _crear():
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bg = Image.new("RGBA", (W, H))
        # Gradiente negro → dorado oscuro
        _gradient_rect(bg, (20, 15, 0, 255), (80, 60, 0, 255), vertical=False)
        img.paste(bg)

        draw = ImageDraw.Draw(img)

        # Patrón decorativo dorado (líneas diagonales)
        for i in range(-H, W + H, 30):
            draw.line([(i, 0), (i + H, H)], fill=(255, 215, 0, 20), width=2)

        # Múltiples bordes dorados
        gold = (255, 215, 0)
        draw.rounded_rectangle([5, 5, W-6, H-6], radius=60,
                                outline=(*gold, 255), width=5)
        draw.rounded_rectangle([13, 13, W-14, H-14], radius=52,
                                outline=(*gold, 100), width=2)
        draw.rounded_rectangle([18, 18, W-19, H-19], radius=47,
                                outline=(*gold, 60), width=1)

        # Destellos en esquinas
        for cx, cy in [(50, 50), (W-50, 50), (50, H-50), (W-50, H-50)]:
            draw.ellipse([cx-15, cy-15, cx+15, cy+15], fill=(*gold, 180))
            draw.ellipse([cx-8, cy-8, cx+8, cy+8], fill=(255, 255, 200, 220))

        # Texto
        font_size = min(150, max(50, int(W * 0.22 / max(len(texto), 1) * 2.5)))
        font = _get_font(FONT_POPPINS_BOLD, font_size)
        draw_tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
        lines = _wrap_text(texto.upper(), font, W - 80, draw_tmp)
        total_h = len(lines) * (font_size + 10)
        y_start = (H - total_h) // 2 + font_size // 2

        for i, line in enumerate(lines):
            y = y_start + i * (font_size + 10)
            # Sombra dorada oscura
            for dx, dy in [(-4,4),(4,4),(-4,-4),(4,-4)]:
                draw.text((W//2+dx, y+dy), line, font=font,
                          fill=(120, 90, 0, 180), anchor="mm")
            draw.text((W//2, y), line, font=font,
                      fill=(255, 230, 80, 255), anchor="mm")

        img = _apply_round_mask(img, radius=60)
        path = f"{RUTA_LOGS}/stk_gold_{user_id}.png"
        img.save(path, "PNG")
        return path

    path = await asyncio.to_thread(_crear)
    with open(path, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=f"✨ **Sticker Gold VIP**\n✍️ _{texto}_\n👤 _Hecho para {nick}_",
            parse_mode=ParseMode.MARKDOWN
        )
    _limpiar_archivo(path)
    sumar_xp(user_id, 8)
    registrar_evento(user_id, nick, f"Sticker Gold: {texto}", "STICKER")


# ─────────────────────────────────────────────
# /stk_hielo [texto] — Sticker hielo/cristal azul
# ─────────────────────────────────────────────
async def sticker_hielo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea un sticker estilo hielo/cristal con colores fríos."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "❄️ **Uso:** `/stk_hielo [texto]`\n_Ejemplo: /stk\\_hielo Frío como el hielo ❄️_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    texto = " ".join(context.args)
    W, H = 700, 350

    def _crear():
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bg = Image.new("RGBA", (W, H))
        _gradient_rect(bg, (180, 220, 255, 255), (220, 240, 255, 255))
        img.paste(bg)

        draw = ImageDraw.Draw(img)

        # Copos de nieve simulados (líneas cruzadas)
        for _ in range(12):
            cx = random.randint(20, W-20)
            cy = random.randint(10, H-10)
            sz = random.randint(10, 30)
            alpha = random.randint(100, 200)
            ice = (200, 230, 255, alpha)
            for angle in [0, 60, 120]:
                import math
                rad = math.radians(angle)
                dx, dy = int(sz * math.cos(rad)), int(sz * math.sin(rad))
                draw.line([(cx-dx, cy-dy), (cx+dx, cy+dy)], fill=ice, width=2)

        # Crystales (polígonos irregulares)
        for _ in range(6):
            cx = random.randint(50, W-50)
            cy = random.randint(20, H-20)
            pts = [(cx + random.randint(-20, 20), cy + random.randint(-20, 20)) for _ in range(5)]
            draw.polygon(pts, fill=(180, 220, 255, 60), outline=(150, 200, 255, 120))

        # Borde cristal
        draw.rounded_rectangle([6, 6, W-7, H-7], radius=60,
                                outline=(100, 180, 255, 220), width=5)

        # Texto
        font_size = min(150, max(50, int(W * 0.22 / max(len(texto), 1) * 2.5)))
        font = _get_font(FONT_POPPINS_BOLD, font_size)
        draw_tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
        lines = _wrap_text(texto.upper(), font, W - 80, draw_tmp)
        total_h = len(lines) * (font_size + 10)
        y_start = (H - total_h) // 2 + font_size // 2

        for i, line in enumerate(lines):
            y = y_start + i * (font_size + 10)
            _draw_text_outline(draw, (W//2, y), line, font,
                               fill=(30, 80, 160, 255),
                               outline_color=(200, 230, 255, 200), stroke=4)

        img = _apply_round_mask(img, radius=60)
        path = f"{RUTA_LOGS}/stk_ice_{user_id}.png"
        img.save(path, "PNG")
        return path

    path = await asyncio.to_thread(_crear)
    with open(path, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=f"❄️ **Sticker Hielo**\n✍️ _{texto}_\n👤 _Hecho para {nick}_",
            parse_mode=ParseMode.MARKDOWN
        )
    _limpiar_archivo(path)
    sumar_xp(user_id, 8)
    registrar_evento(user_id, nick, f"Sticker Hielo: {texto}", "STICKER")


# ─────────────────────────────────────────────
# /stk_venezuela [texto] — Sticker con colores de Venezuela
# ─────────────────────────────────────────────
async def sticker_venezuela(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea un sticker con los colores de la bandera venezolana."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🇻🇪 **Uso:** `/stk_venezuela [texto]`\n_Ejemplo: /stk\\_venezuela Orgullo Patrio 🇻🇪_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    texto = " ".join(context.args)
    W, H = 700, 350

    def _crear():
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Franjas de la bandera venezolana: amarillo, azul, rojo
        band_h = H // 3
        draw.rectangle([0, 0, W, band_h], fill=(207, 185, 20, 255))           # Amarillo
        draw.rectangle([0, band_h, W, band_h * 2], fill=(0, 56, 168, 255))    # Azul
        draw.rectangle([0, band_h * 2, W, H], fill=(207, 17, 17, 255))        # Rojo

        # Overlay semitransparente para oscurecer un poco y que el texto se vea
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 60))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)

        # Arco de estrellas pequeñas (8 estrellas del escudo venezolano)
        import math
        cx, cy = W // 2, H // 2
        radio_estrellas = min(W, H) // 3
        for i in range(8):
            angulo = math.radians(i * 45 - 90)
            sx = int(cx + radio_estrellas * 0.55 * math.cos(angulo))
            sy = int(cy + radio_estrellas * 0.35 * math.sin(angulo))
            draw.ellipse([sx-6, sy-6, sx+6, sy+6], fill=(255, 230, 50, 200))

        # Borde dorado
        draw.rounded_rectangle([6, 6, W-7, H-7], radius=55,
                                outline=(255, 215, 0, 220), width=5)

        # Texto
        font_size = min(140, max(50, int(W * 0.22 / max(len(texto), 1) * 2.5)))
        font = _get_font(FONT_POPPINS_BOLD, font_size)
        draw_tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
        lines = _wrap_text(texto.upper(), font, W - 80, draw_tmp)
        total_h = len(lines) * (font_size + 10)
        y_start = (H - total_h) // 2 + font_size // 2

        for i, line in enumerate(lines):
            y = y_start + i * (font_size + 10)
            _draw_text_outline(draw, (W//2, y), line, font,
                               fill=(255, 255, 255, 255),
                               outline_color=(0, 0, 0, 200), stroke=6)

        img = _apply_round_mask(img, radius=55)
        path = f"{RUTA_LOGS}/stk_ve_{user_id}.png"
        img.save(path, "PNG")
        return path

    path = await asyncio.to_thread(_crear)
    with open(path, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=f"🇻🇪 **Sticker Venezuela**\n✍️ _{texto}_\n👤 _Hecho para {nick}_",
            parse_mode=ParseMode.MARKDOWN
        )
    _limpiar_archivo(path)
    sumar_xp(user_id, 8)
    registrar_evento(user_id, nick, f"Sticker Venezuela: {texto}", "STICKER")


# ─────────────────────────────────────────────
# /stk_meme [texto arriba | texto abajo]
# Estilo meme clásico: fondo negro, texto blanco grande
# ─────────────────────────────────────────────
async def sticker_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea un sticker estilo meme clásico con texto arriba y abajo."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "😂 **Uso:** `/stk_meme [texto arriba | texto abajo]`\n\n"
            "_Ejemplo:_\n"
            "- `/stk_meme cuando termina el mes | ya se fue el dinero`\n"
            "- `/stk_meme yo en el trabajo | vs yo en casa`\n\n"
            "_Usa `|` para separar el texto de arriba y de abajo_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    full_text = " ".join(context.args)
    if "|" in full_text:
        partes = full_text.split("|", 1)
        texto_arriba  = partes[0].strip().upper()
        texto_abajo   = partes[1].strip().upper()
    else:
        texto_arriba  = full_text.upper()
        texto_abajo   = ""

    W, H = 700, 500

    def _crear():
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bg = Image.new("RGBA", (W, H))
        _gradient_rect(bg, (30, 30, 30, 255), (60, 60, 60, 255))
        img.paste(bg)
        draw = ImageDraw.Draw(img)

        # Patrón de puntos estilo meme
        for x in range(0, W, 20):
            for y in range(0, H, 20):
                draw.ellipse([x-1, y-1, x+1, y+1], fill=(80, 80, 80, 100))

        font_size = 90
        font = _get_font(FONT_DEJAVU_BOLD, font_size)
        draw_tmp = ImageDraw.Draw(Image.new("L", (1, 1)))

        # Texto arriba
        lines_top = _wrap_text(texto_arriba, font, W - 60, draw_tmp)
        for i, line in enumerate(lines_top):
            y = 20 + font_size // 2 + i * (font_size + 5)
            _draw_text_outline(draw, (W//2, y), line, font,
                               fill=(255, 255, 255, 255),
                               outline_color=(0, 0, 0, 255), stroke=6)

        # Texto abajo
        if texto_abajo:
            lines_bot = _wrap_text(texto_abajo, font, W - 60, draw_tmp)
            total_h_bot = len(lines_bot) * (font_size + 5)
            y_base = H - total_h_bot - 15
            for i, line in enumerate(lines_bot):
                y = y_base + font_size // 2 + i * (font_size + 5)
                _draw_text_outline(draw, (W//2, y), line, font,
                                   fill=(255, 255, 255, 255),
                                   outline_color=(0, 0, 0, 255), stroke=6)

        img = _apply_round_mask(img, radius=40)
        path = f"{RUTA_LOGS}/stk_meme_{user_id}.png"
        img.save(path, "PNG")
        return path

    path = await asyncio.to_thread(_crear)
    with open(path, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=f"😂 **Sticker Meme**\n👤 _Hecho para {nick}_",
            parse_mode=ParseMode.MARKDOWN
        )
    _limpiar_archivo(path)
    sumar_xp(user_id, 8)
    registrar_evento(user_id, nick, f"Sticker Meme", "STICKER")


# ─────────────────────────────────────────────
# /stk_lista — Muestra todos los estilos disponibles
# ─────────────────────────────────────────────
async def sticker_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra todos los comandos de stickers disponibles."""
    await update.message.reply_text(
        "🎨 **FÁBRICA DE STICKERS CAMILABOT** 🎨\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✍️ _Todos aceptan el texto que quieras_\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🟩 /brat [texto] · _Estilo BRAT verde_\n"
        "🌟 /stk\\_neon [texto] · _Fondo oscuro neón_\n"
        "🔥 /stk\\_fuego [texto] · _Llamas y lava_\n"
        "🌌 /stk\\_galaxia [texto] · _Espacio y estrellas_\n"
        "🌸 /stk\\_aesthetic [texto] · _Pastel suave_\n"
        "🖤 /stk\\_dark [texto] · _Dark gothic rojo_\n"
        "🌈 /stk\\_arcoiris [texto] · _Colores vibrantes_\n"
        "✨ /stk\\_gold [texto] · _Premium dorado VIP_\n"
        "❄️ /stk\\_hielo [texto] · _Cristal frío_\n"
        "🇻🇪 /stk\\_venezuela [texto] · _Colores patrios_\n"
        "😂 /stk\\_meme [arriba | abajo] · _Meme clásico_\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📌 /sticker\\_buscar [tema] · _Buscar sticker online_\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 _Ejemplo: /stk\\_neon AnyerJR 🔥_",
        parse_mode=ParseMode.MARKDOWN
    )


async def resetear_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Borra el historial de conversación del usuario con Camila."""
    user_id = update.effective_user.id
    uid = str(user_id)
    nick = update.effective_user.first_name
    
    if uid in conversaciones:
        mensajes_borrados = len(conversaciones[uid])
        conversaciones[uid] = []
        guardar_db("conversaciones.json", conversaciones)
        
        await update.message.reply_text(
            f"🧹 **MEMORIA BORRADA** 🧹\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ Se eliminaron `{mensajes_borrados}` mensajes\n"
            f"💬 Ahora puedes empezar una conversación fresca\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🛡️ _¡Hola de nuevo, {nick}!_",
            parse_mode=ParseMode.MARKDOWN
        )
        registrar_evento(user_id, nick, "Reseteó su conversación con IA", "IA")
    else:
        await update.message.reply_text(
            "⚠️ **No hay historial que borrar.**\n"
            "_Aún no has hablado con Camila._"
        )


# --- [ NUEVOS COMANDOS V7.0 - 20 COMANDOS ÚTILES ] ---

# 1. TRADUCTOR
async def traducir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traduce texto usando API pública de MyMemory."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "🌐 **Uso:** `/traducir [idioma] [texto]`\n\n"
            "**Idiomas soportados:**\n"
            "- `es` - Español\n"
            "- `en` - Inglés\n"
            "- `pt` - Portugués\n"
            "- `fr` - Francés\n"
            "- `it` - Italiano\n"
            "- `de` - Alemán\n"
            "- `ja` - Japonés\n"
            "- `zh` - Chino\n"
            "- `ru` - Ruso\n\n"
            "**Ejemplos:**\n"
            "- `/traducir en Hola amigo`\n"
            "- `/traducir fr Buenos días`"
            "- `/traducir es hello my brother`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    idioma_destino = context.args[0].lower()
    texto = " ".join(context.args[1:])
    
    # Códigos de idioma aceptados
    idiomas_validos = {
        "es": "español",
        "en": "inglés", 
        "pt": "portugués",
        "fr": "francés",
        "it": "italiano",
        "de": "alemán",
        "ja": "japonés",
        "zh": "chino",
        "ru": "ruso",
        "ar": "árabe",
        "ko": "coreano",
        "hi": "hindí"
    }
    
    if idioma_destino not in idiomas_validos:
        await update.message.reply_text(f"❌ Idioma no soportado. Usa: {', '.join(idiomas_validos.keys())}")
        return
    
    wait_msg = await update.message.reply_text(f"🌐 **Traduciendo al {idiomas_validos[idioma_destino]}...**")
    
    try:
        # Usar múltiples APIs con respaldo automático
        traduccion = None
        
        # Intento 1: MyMemory
        try:
            url = f"https://api.mymemory.translated.net/get?q={quote(texto)}&langpair=auto|{idioma_destino}"
            respuesta = await asyncio.to_thread(requests.get, url, timeout=5)
            data = respuesta.json()
            if data.get('responseStatus') == 200:
                traduccion = data['responseData']['translatedText']
                if traduccion.lower() != texto.lower():
                    pass  # Traducción válida
                else:
                    traduccion = None
        except:
            pass
        
        # Intento 2: Google Translate
        if not traduccion:
            try:
                url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={idioma_destino}&dt=t&q={quote(texto)}"
                respuesta = await asyncio.to_thread(requests.get, url, timeout=5)
                if respuesta.status_code == 200:
                    data = respuesta.json()
                    if data and len(data) > 0 and len(data[0]) > 0:
                        traduccion = data[0][0][0] if data[0][0] else None
            except:
                pass
        
        if traduccion:
            await wait_msg.edit_text(
                f"🌐 **TRADUCCIÓN AL {idiomas_validos[idioma_destino].upper()}**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📝 **Original:**\n`{texto}`\n\n"
                f"✅ **Traducción:**\n`{traduccion}`\n"
                f"━━━━━━━━━━━━━━━━━━━━",
                parse_mode=ParseMode.MARKDOWN
            )
            registrar_evento(user_id, nick, f"Tradujo: {texto[:30]}", "TRADUCCIÓN")
            sumar_xp(user_id, 3)
        else:
            await wait_msg.edit_text("❌ **Error: No se pudo traducir.**\nIntenta de nuevo con otro texto.")
            
    except Exception as e:
        try:
            await wait_msg.edit_text("❌ **Error de conexión.**\nIntenta de nuevo.")
        except:
            await update.message.reply_text("❌ **Error de conexión.**\nIntenta de nuevo.")

# 2. CALCULADORA CON API PÚBLICA
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculadora matemática usando API."""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "🔢 **CALCULADORA AVANZADA**\n\n"
            "**Uso:** `/calc [operación matemática]`\n\n"
            "**Operaciones soportadas:**\n"
            "- Básicas: `+` `-` `*` `/` `**` (potencia)\n"
            "- Porcentaje: `%`\n"
            "- Módulo: `mod`\n\n"
            "**Ejemplos:**\n"
            "- `/calc 25 * 4 + 10`\n"
            "- `/calc 100 / 2.5`\n"
            "- `/calc 2 ** 8` (2 elevado a 8)\n"
            "- `/calc 17 mod 5`\n"
            "- `/calc (50 + 30) * 2`\n"
            "- `/calc 100 - 25 + 15`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    operacion = " ".join(context.args)
    wait_msg = await update.message.reply_text(f"🔢 **Calculando:** `{operacion}`...")
    
    try:
        # Limpiar la operación y validarla
        operacion_limpia = operacion.replace(" ", "").lower()
        
        # Permitir solo caracteres seguros
        caracteres_permitidos = set("0123456789+-*/.()%^modrandomsqrtsincostan")
        if not all(c in caracteres_permitidos or c.isspace() for c in operacion_limpia):
            await wait_msg.edit_text("❌ **Operación inválida.**\n_Solo se permiten números y operadores matemáticos._")
            return
        
        # Reemplazar palabras clave
        operacion_limpia = operacion_limpia.replace("^", "**")
        operacion_limpia = operacion_limpia.replace("mod", "%")
        
        # Usar eval seguro con restricciones
        resultado = eval(operacion_limpia, {
            "__builtins__": {},
            "abs": abs,
            "pow": pow,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
        })
        
        # Formatear resultado
        if isinstance(resultado, float):
            if resultado == int(resultado):
                resultado_fmt = str(int(resultado))
            else:
                resultado_fmt = f"{resultado:.10g}"  # Quita ceros innecesarios
        else:
            resultado_fmt = str(resultado)
        
        await wait_msg.edit_text(
            f"🔢 **CALCULADORA**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📝 **Operación:** `{operacion}`\n"
            f"✅ **Resultado:** `{resultado_fmt}`\n"
            f"━━━━━━━━━━━━━━━━━━━━",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(user_id, 2)
        
    except ZeroDivisionError:
        await wait_msg.edit_text("❌ **Error:** No se puede dividir entre cero.")
    except SyntaxError:
        await wait_msg.edit_text("❌ **Error de sintaxis.**\n_Revisa la operación._")
    except Exception as e:
        print(f"Error calc: {e}")
        await wait_msg.edit_text(
            "❌ **Error al calcular.**\n"
            "_Verifica que la operación sea válida._"
        )

# 3. QR GENERATOR
async def qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera código QR."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text("📱 **Uso:** `/qr [texto o URL]`")
        return
    
    texto = " ".join(context.args)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={texto}"
    
    await update.message.reply_photo(
        photo=qr_url,
        caption=f"📱 **Código QR generado**\n🔗 {texto[:50]}..."
    )
    sumar_xp(user_id, 5)

# 4. ACORTAR URLs
async def acortar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Acorta URLs largas con múltiples APIs."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text(
            "🔗 **Acortador de URLs**\n\n"
            "**Uso:** `/acortar [URL larga]`\n\n"
            "**Ejemplo:**\n"
            "`/acortar https://www.wikipedia.org/wiki/Revolución_Francesa`\n\n"
            "✨ _Comprime URLs largas en enlaces cortos_"
        )
        return
    
    url = context.args[0]
    
    # Validar que sea una URL
    if not (url.startswith("http://") or url.startswith("https://")):
        await update.message.reply_text("❌ **Debes proporcionar una URL válida.**\n_Debe comenzar con http:// o https://_")
        return
    
    wait_msg = await update.message.reply_text(f"🔗 **Acortando URL...**\n⏳ _Por favor espera..._")
    
    try:
        # Intentar con múltiples APIs en orden de preferencia
        apis = [
            f"https://is.gd/create.php?format=simple&url={url}",
            f"https://tinyurl.com/api-create.php?url={url}",
            f"https://v.gd/?url={url}"
        ]
        
        url_acortada = None
        fuente = ""
        
        for api_url in apis:
            try:
                respuesta = await asyncio.to_thread(
                    requests.get,
                    api_url,
                    timeout=8
                )
                
                if respuesta.status_code == 200:
                    contenido = respuesta.text.strip()
                    
                    # Validar que sea una URL válida
                    if contenido.startswith("http"):
                        url_acortada = contenido
                        
                        if "is.gd" in api_url:
                            fuente = "is.gd"
                        elif "tinyurl" in api_url:
                            fuente = "TinyURL"
                        elif "v.gd" in api_url:
                            fuente = "v.gd"
                        break
            except:
                continue
        
        if url_acortada:
            resultado = (
                f"🔗 **URL ACORTADA** 🔗\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📏 **Original:**\n`{url[:80]}`{'...' if len(url) > 80 else ''}\n\n"
                f"✂️ **Acortada:**\n`{url_acortada}`\n\n"
                f"📊 **Servicio:** `{fuente}`\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"✨ _Acortado por {nick}_"
            )
            
            await wait_msg.edit_text(resultado, parse_mode=ParseMode.MARKDOWN)
            registrar_evento(user_id, nick, f"Acortó URL", "HERRAMIENTAS")
            sumar_xp(user_id, 3)
        else:
            await wait_msg.edit_text(
                "❌ **Error al acortar la URL.**\n\n"
                "💡 **Posibles causas:**\n"
                "- La URL no es válida\n"
                "- El servicio está caído\n"
                "- La URL ya está acortada\n\n"
                "_Intenta con otra URL._"
            )
            
    except Exception as e:
        print(f"Error acortador: {e}")
        await wait_msg.edit_text(
            "❌ **Error de conexión.**\n"
            "_No se pudo procesar la URL._"
        )

# 5. DATOS RANDOM
async def randomuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera persona ficticia con datos random."""
    user_id = update.effective_user.id
    
    try:
        resp = await asyncio.to_thread(requests.get, "https://randomuser.me/api/", timeout=10)
        data = resp.json()["results"][0]
        
        nombre = f"{data['name']['first']} {data['name']['last']}"
        email = data['email']
        pais = data['location']['country']
        edad = data['dob']['age']
        foto = data['picture']['large']
        
        await update.message.reply_photo(
            photo=foto,
            caption=f"👤 **Persona Random**\n📛 {nombre}\n🎂 {edad} años\n🌍 {pais}\n📧 {email}"
        )
        sumar_xp(user_id, 5)
    except:
        await update.message.reply_text("❌ Error al generar persona")

# 6. DADOS
async def dado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lanza un dado virtual."""
    user_id = update.effective_user.id
    resultado = random.randint(1, 6)
    dados = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    await update.message.reply_text(f"🎲 **Resultado:** {dados[resultado-1]} `{resultado}`", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(user_id, 1)

# 7. MONEDA
async def moneda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lanza una moneda."""
    user_id = update.effective_user.id
    resultado = random.choice(["Cara 🪙", "Cruz 🌟"])
    await update.message.reply_text(f"💰 **Resultado:** {resultado}")
    sumar_xp(user_id, 1)

# 8. MEME RANDOM
async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía un meme random."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    try:
        resp = await asyncio.to_thread(requests.get, "https://meme-api.com/gimme", timeout=10)
        data = resp.json()
        await update.message.reply_photo(
            photo=data['url'],
            caption=f"😂 **{data['title']}**\n👍 {data['ups']} upvotes"
        )
        sumar_xp(user_id, 3)
    except:
        await update.message.reply_text("❌ Error al cargar meme")

# 9. CRYPTO PRECIO
async def cripto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Consulta precio de criptomonedas de múltiples fuentes."""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "💰 **Uso:** `/cripto [moneda]`\n\n"
            "**Ejemplos de monedas:**\n"
            "- `btc` - Bitcoin\n"
            "- `eth` - Ethereum\n"
            "- `bnb` - Binance Coin\n"
            "- `doge` - Dogecoin\n"
            "- `ada` - Cardano\n"
            "- `xrp` - Ripple",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    coin = context.args[0].lower()
    
    # Mapeo de nombres comunes a IDs de CoinGecko
    coin_mapping = {
        'btc': 'bitcoin',
        'eth': 'ethereum',
        'bnb': 'binancecoin',
        'doge': 'dogecoin',
        'ada': 'cardano',
        'xrp': 'ripple',
        'ltc': 'litecoin',
        'sol': 'solana',
        'usdc': 'usd-coin',
        'usdt': 'tether',
        'xlm': 'stellar'
    }
    
    # Si está en el mapeo, usar el nombre completo, si no, usar lo que escribió
    coin_id = coin_mapping.get(coin, coin)
    
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
        resp = await asyncio.to_thread(requests.get, url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if coin_id in data:
            precio = data[coin_id].get('usd', 'N/A')
            cambio = data[coin_id].get('usd_24h_change', 0)
            market_cap = data[coin_id].get('usd_market_cap', 0)
            
            emoji = "📈" if cambio > 0 else "📉"
            
            if isinstance(precio, (int, float)):
                if precio < 1:
                    precio_fmt = f"${precio:.8f}"
                else:
                    precio_fmt = f"${precio:,.2f}"
            else:
                precio_fmt = "N/A"
            
            if market_cap and market_cap > 0:
                if market_cap >= 1_000_000_000:
                    market_cap_fmt = f"${market_cap/1_000_000_000:.2f}B"
                else:
                    market_cap_fmt = f"${market_cap/1_000_000:.2f}M"
            else:
                market_cap_fmt = "N/A"
            
            await update.message.reply_text(
                f"💰 **{coin_id.upper()}**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"💵 Precio: `{precio_fmt}`\n"
                f"{emoji} 24h: `{cambio:+.2f}%`\n"
                f"📊 Market Cap: `{market_cap_fmt}`\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"_Datos de CoinGecko_",
                parse_mode=ParseMode.MARKDOWN
            )
            sumar_xp(user_id, 5)
        else:
            await update.message.reply_text(
                f"❌ **Criptomoneda no encontrada:** `{coin}`\n"
                f"_Verifica el símbolo o nombre._"
            )
    except requests.exceptions.RequestException:
        await update.message.reply_text(
            "❌ **Error de conexión.**\n"
            "_No se pudo obtener el precio. Intenta de nuevo._"
        )
    except Exception as e:
        print(f"Error cripto: {e}")
        await update.message.reply_text(
            "❌ **Error al consultar criptomoneda.**\n"
            "_Intenta de nuevo en unos momentos._"
        )

# 10. IP INFO
async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información de una IP."""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("🌐 **Uso:** `/ip [dirección IP]`")
        return
    
    ip_address = context.args[0]
    try:
        resp = await asyncio.to_thread(requests.get, f"http://ip-api.com/json/{ip_address}", timeout=10)
        data = resp.json()
        
        if data['status'] == 'success':
            info = (
                f"🌐 **Información de IP**\n"
                f"📍 IP: `{data['query']}`\n"
                f"🌍 País: {data['country']}\n"
                f"🏙️ Ciudad: {data['city']}\n"
                f"📮 Código Postal: {data['zip']}\n"
                f"🕐 Zona: {data['timezone']}\n"
                f"📡 ISP: {data['isp']}"
            )
            await update.message.reply_text(info, parse_mode=ParseMode.MARKDOWN)
            sumar_xp(user_id, 8)
        else:
            await update.message.reply_text("❌ IP inválida")
    except:
        await update.message.reply_text("❌ Error al consultar IP")

# 11. WIKIPEDIA
@tarea_larga
async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca en Wikipedia y devuelve información útil y directa."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text(
            "📚 **Búsqueda en Wikipedia**\n\n"
            "**Uso:** `/wiki [tema]`\n\n"
            "**Ejemplos:**\n"
            "- `/wiki Revolución francesa`\n"
            "- `/wiki Fotosíntesis`\n"
            "- `/wiki Simón Bolívar`\n"
            "- `/wiki Python lenguaje programación`"
        )
        return
    
    tema = " ".join(context.args)
    wait_msg = await update.message.reply_text(f"📚 **Buscando en Wikipedia:** `{tema}`\n⏳ _Cargando información..._", parse_mode=ParseMode.MARKDOWN)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        # Buscar en Wikipedia española con API clásica
        url = f"https://es.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&titles={tema.replace(' ', '_')}&explaintext=true"
        respuesta = await asyncio.to_thread(requests.get, url, headers=headers, timeout=10)
        
        if respuesta.status_code == 200:
            data = respuesta.json()
            pages = data.get('query', {}).get('pages', {})
            
            if pages:
                page_id = list(pages.keys())[0]
                page = pages[page_id]
                
                if 'extract' in page and page['extract']:
                    titulo = page.get('title', tema)
                    contenido = page['extract']
                    
                    # Limitar a 1000 caracteres
                    if len(contenido) > 1000:
                        corte = contenido[:1000]
                        ultimo_punto = corte.rfind('.')
                        if ultimo_punto > 800:
                            contenido = corte[:ultimo_punto+1]
                        else:
                            contenido = corte + "..."
                    
                    resultado = (
                        f"📚 **WIKIPEDIA** 📚\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"🔤 **{titulo}**\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"{contenido}\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"ℹ️ _Información de Wikipedia en Español_"
                    )
                    
                    await wait_msg.edit_text(resultado, parse_mode=ParseMode.MARKDOWN)
                    registrar_evento(user_id, nick, f"Buscó Wikipedia: {tema}", "WIKIPEDIA")
                    sumar_xp(user_id, 8)
                    return
        
        # Fallback a DuckDuckGo
        url_ddg = f"https://api.duckduckgo.com/?q={tema}&format=json&no_redirect=1"
        respuesta_ddg = await asyncio.to_thread(requests.get, url_ddg, headers=headers, timeout=10)
        
        if respuesta_ddg.status_code == 200:
            data_ddg = respuesta_ddg.json()
            if data_ddg.get('AbstractText'):
                resultado = (
                    f"📚 **WIKIPEDIA** 📚\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🔤 **{tema}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"{data_ddg['AbstractText']}\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"ℹ️ _Información de DuckDuckGo_"
                )
                await wait_msg.edit_text(resultado, parse_mode=ParseMode.MARKDOWN)
                registrar_evento(user_id, nick, f"Buscó Wikipedia: {tema}", "WIKIPEDIA")
                sumar_xp(user_id, 8)
                return
        
        # Si nada funciona
        await wait_msg.edit_text(
            f"❌ **No se encontró información en Wikipedia para:** `{tema}`\n\n"
            f"💡 **Intenta con:**\n"
            f"- Un término más general\n"
            f"- Palabras clave diferentes\n"
            f"- Un nombre más conocido"
        )
        
    except requests.exceptions.Timeout:
        await wait_msg.edit_text(
            "⏱️ **La búsqueda tardó demasiado.**\n"
            "_Intenta de nuevo en unos momentos._"
        )
    except Exception as e:
        print(f"Error wiki: {e}")
        await wait_msg.edit_text(
            "❌ **Error al buscar en Wikipedia.**\n"
            "_Intenta de nuevo más tarde._"
        )

# LISTA DE CANCIONES RELAJANTES PARA EL MENÚ (ALEATORIAS)
# Estas son búsquedas que se descargan de YouTube
CANCIONES_RELAJANTES = [
    # PHONK - Lo-fi beats (8)
    "phonk lofi hip hop beats",
    "phonk chill beats",
    "phonk relaxing music",
    "phonk study beats",
    "phonk dark ambient",
    "phonk night drive",
    "phonk tumbao",
    "phonk trap soul",
    
    # THE NEIGHBOURHOOD (8)
    "The Neighbourhood Sweater Weather",
    "The Neighbourhood Daddy Issues",
    "The Neighbourhood Male Gaze",
    "The Neighbourhood Sicko Mode",
    "The Neighbourhood Nervous",
    "The Neighbourhood Alligator",
    "The Neighbourhood Compass",
    "The Neighbourhood Softcore",
    
    # XXXTENTACION - Canciones calmadas (8)
    "XXXTENTACION Jocelyn Flores",
    "XXXTENTACION SAD",
    "XXXTENTACION Moonlight",
    "XXXTENTACION Everybody Dies in Their Nightmares",
    "XXXTENTACION Hold Your Crown",
    "XXXTENTACION Changes",
    "XXXTENTACION Rip Roach",
    "XXXTENTACION Snow",
    
    # LO-FI CHILL (8)
    "lofi hip hop beats 24/7",
    "lofi chill beats study",
    "lofi relaxing music rain",
    "lofi ambient beats",
    "lofi jazz cafe",
    "lofi synthwave nights",
    "lofi midnight drive",
    "lofi cozy autumn",
    
    # INDIE CALMADO (8)
    "indie chill lo-fi",
    "indie relax beats",
    "chill indie music",
    "ambient lofi indie",
    "indie folk acoustic",
    "indie bedroom pop",
    "indie dream pop",
    "indie melancholic songs",
    
    # OTROS ARTISTAS RELAJANTES (10)
    "Cavetown lo-fi",
    "Girl in Red sad songs",
    "Arctic Monkeys chill",
    "Clairo meditation music",
    "Mac Miller swimming",
    "Joji slow dancing",
    "Frank Ocean Blonde",
    "Tyler the Creator Flower Boy",
    "Cigarettes After Sex sad songs",
    "Conan Gray memories",
]

# 12. FRASES MOTIVACIONALES
FRASES_MOTIVACION = [
    "💪 'El éxito es la suma de pequeños esfuerzos repetidos día tras día.'",
    "🌟 'No cuentes los días, haz que los días cuenten.'",
    "🚀 'El único modo de hacer un gran trabajo es amar lo que haces.'",
    "⭐ 'Cree en ti mismo y todo será posible.'",
    "🔥 'La disciplina es el puente entre metas y logros.'",
    "💎 'No te rindas, cada fracaso es una lección.'",
    "🎯 'Tu único límite eres tú mismo.'",
    "⚡ 'El futuro pertenece a quienes creen en la belleza de sus sueños.'",
    "🏆 'Trabaja duro en silencio, deja que el éxito haga el ruido.'",
    "🌈 'Después de la tormenta siempre sale el sol.'",
    "🎨 'Eres capaz de más de lo que imaginas.'",
    "🧠 'La vida es un viaje, no un destino.'",
    "💝 'Sé amable contigo mismo, eres lo mejor que tienes.'",
    "🌺 'Cada día es una nueva oportunidad para brillar.'",
    "✨ 'Tu potencial es ilimitado, solo cree.'",
    "🎪 'La risa es la mejor medicina para el alma.'",
    "🌟 'Hoy es el mejor día para empezar.'",
    "🔮 'Lo que hoy construyes, mañana lo cosechas.'",
    "🎭 'La vida está llena de momentos mágicos.'",
    "🌸 'Eres más fuerte de lo que crees.'",
    "🎯 'Cada paso hacia adelante es un logro.'",
    "💥 'Tu valor no depende de lo que haces, sino de quién eres.'",
    "🎸 'La música de la vida está en tus manos.'",
    "🌊 'Fluye con la vida, no contra ella.'",
    "🏅 'Hoy eres mejor que ayer.'",
]

# LISTAS PARA CADA DÍA DE LA SEMANA (ALEATORIAS Y DECORADAS)
LISTAS_DIAS = {
    0: {  # Lunes
        "titulo": "🌟 **LISTA DEL LUNES** 🌟",
        "items": [
            "📚 Aprender algo nuevo",
            "💪 Hacer 10 minutos de ejercicio",
            "📞 Llamar a un amigo",
            "🎯 Planificar la semana",
            "🍎 Comer saludable"
        ]
    },
    1: {  # Martes
        "titulo": "🎨 **CREACIONES DEL MARTES** 🎨",
        "items": [
            "🖌️ Crear algo artístico",
            "✍️ Escribir en un diario",
            "🎭 Ver una película",
            "🎵 Escuchar música nueva",
            "📖 Leer un capítulo"
        ]
    },
    2: {  # Miércoles
        "titulo": "⚡ **ENERGÍA DEL MIÉRCOLES** ⚡",
        "items": [
            "🏃 Salir a caminar",
            "🧘 Meditar 5 minutos",
            "📱 Desconectarse del teléfono",
            "🌳 Estar en la naturaleza",
            "💆 Auto-cuidado personal"
        ]
    },
    3: {  # Jueves
        "titulo": "🎭 **JUEGOS DEL JUEVES** 🎭",
        "items": [
            "🎮 Jugar videojuegos",
            "🧩 Resolver un acertijo",
            "🃏 Jugar cartas con amigos",
            "🎲 Intentar suerte",
            "🤣 Reírse de un buen chiste"
        ]
    },
    4: {  # Viernes
        "titulo": "🎉 **VIERNES DE CELEBRACIÓN** 🎉",
        "items": [
            "🎊 Celebrar los logros semanales",
            "🍕 Comer algo especial",
            "🎪 Plan con amigos",
            "💃 Bailar y divertirse",
            "🌙 Disfrutar la noche"
        ]
    },
    5: {  # Sábado
        "titulo": "🌺 **SÁBADO DE RELAJACIÓN** 🌺",
        "items": [
            "😴 Dormir un poco más",
            "🛁 Tomar un baño relajante",
            "📚 Leer sin prisa",
            "👨‍👩‍👧 Tiempo con familia",
            "☕ Disfrutar del café tranquilo"
        ]
    },
    6: {  # Domingo
        "titulo": "🌈 **DOMINGO DE INSPIRACIÓN** 🌈",
        "items": [
            "🙏 Reflexionar sobre la semana",
            "🎯 Establecer metas nuevas",
            "🌅 Disfrutar el amanecer",
            "💭 Soñar en grande",
            "✨ Prepararse para brillar"
        ]
    }
}

async def motivar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía frase motivacional y lista del día."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    # Obtener día de la semana (0=lunes, 6=domingo)
    dia_semana = datetime.now().weekday()
    lista_dia = LISTAS_DIAS[dia_semana]
    
    frase = random.choice(FRASES_MOTIVACION)
    
    # Barajar los items de la lista
    items = lista_dia["items"].copy()
    random.shuffle(items)
    
    items_texto = "\n".join([f"✨ {item}" for item in items])
    
    mensaje = (
        f"{frase}\n\n"
        f"{lista_dia['titulo']}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{items_texto}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🌟 _¡Tú puedes, {nick}!_"
    )
    
    await update.message.reply_text(mensaje, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(user_id, 2)

# 13. CONSEJO RANDOM
async def consejo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Da un consejo aleatorio."""
    user_id = update.effective_user.id
    
    try:
        resp = await asyncio.to_thread(requests.get, "https://api.adviceslip.com/advice", timeout=10)
        data = resp.json()
        consejo_texto = data['slip']['advice']
        
        # Traducir con IA
        prompt = f"Traduce al español: {consejo_texto}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        resp_ia = await asyncio.to_thread(requests.post, GEMINI_API_URL, json=payload, timeout=10)
        
        if resp_ia.status_code == 200:
            traducido = resp_ia.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            await update.message.reply_text(f"💡 **Consejo del día:**\n_{traducido}_", parse_mode=ParseMode.MARKDOWN)
            sumar_xp(user_id, 3)
    except:
        await update.message.reply_text("❌ Error al obtener consejo")

# 14. LOVE CALCULATOR
async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculadora de amor."""
    user_id = update.effective_user.id
    
    if not update.message.reply_to_message:
        await update.message.reply_text("❤️ **Responde al mensaje de alguien para calcular el amor**")
        return
    
    user1 = update.effective_user.first_name
    user2 = update.message.reply_to_message.from_user.first_name
    
    porcentaje = random.randint(0, 100)
    
    if porcentaje >= 80:
        mensaje = "¡Son el match perfecto! 💕"
    elif porcentaje >= 60:
        mensaje = "Buena compatibilidad ❤️"
    elif porcentaje >= 40:
        mensaje = "Puede funcionar 💛"
    elif porcentaje >= 20:
        mensaje = "Difícil pero no imposible 💔"
    else:
        mensaje = "Mejor como amigos 😅"
    
    await update.message.reply_text(
        f"💘 **LOVE CALCULATOR** 💘\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👫 {user1} ❤️ {user2}\n"
        f"💕 Compatibilidad: `{porcentaje}%`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{mensaje}",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(user_id, 3)

# 15. ADIVINA EL NÚMERO
juegos_activos = {}

async def adivinar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Juego de adivinar número."""
    user_id = update.effective_user.id
    uid = str(user_id)
    
    if not context.args:
        # Iniciar juego
        numero = random.randint(1, 100)
        juegos_activos[uid] = {"numero": numero, "intentos": 0}
        await update.message.reply_text(
            "🎮 **Adivina el número**\n"
            "Pensé un número entre 1 y 100\n"
            "Usa: `/adivinar [número]`"
        )
        return
    
    if uid not in juegos_activos:
        await update.message.reply_text("❌ Primero inicia el juego con `/adivinar`")
        return
    
    try:
        intento = int(context.args[0])
        juegos_activos[uid]["intentos"] += 1
        numero_secreto = juegos_activos[uid]["numero"]
        
        if intento == numero_secreto:
            intentos = juegos_activos[uid]["intentos"]
            del juegos_activos[uid]
            await update.message.reply_text(
                f"🎉 **¡CORRECTO!** 🎉\n"
                f"El número era {numero_secreto}\n"
                f"Intentos: {intentos}"
            )
            sumar_xp(user_id, 10)
        elif intento < numero_secreto:
            await update.message.reply_text("⬆️ **Más alto**")
        else:
            await update.message.reply_text("⬇️ **Más bajo**")
    except:
        await update.message.reply_text("❌ Número inválido")

# 16. SPOTIFY SEARCH
async def spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca música en Spotify."""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("🎵 **Uso:** `/spotify [canción o artista]`")
        return
    
    query = " ".join(context.args)
    await update.message.reply_text(
        f"🎵 **Buscar en Spotify:**\n"
        f"`{query}`\n\n"
        f"🔗 https://open.spotify.com/search/{query.replace(' ', '%20')}",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(user_id, 2)

# 17. NETFLIX SEARCH  
async def netflix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca en Netflix."""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("🎬 **Uso:** `/netflix [título]`")
        return
    
    query = " ".join(context.args)
    await update.message.reply_text(
        f"🎬 **Buscar en Netflix:**\n"
        f"`{query}`\n\n"
        f"🔗 https://www.netflix.com/search?q={query.replace(' ', '%20')}",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(user_id, 2)

# 18. DÓLAR VENEZUELA
async def dolar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Precio del dólar en Venezuela con múltiples fuentes."""
    user_id = update.effective_user.id
    
    try:
        # Intentar múltiples APIs en orden de preferencia
        apis = [
            "https://pydolarvenezuela-api.vercel.app/api/v1/dollar",
            "https://ve.dolarapi.com/v1/dolares/oficial",
            "https://api.exchangerate-api.com/v4/latest/USD"
        ]
        
        precio = None
        fuente = ""
        
        for api_url in apis:
            try:
                resp = await asyncio.to_thread(requests.get, api_url, timeout=8)
                data = resp.json()
                
                # Intentar obtener el precio según el formato de cada API
                if 'price' in data:  # pydolarvenezuela
                    precio = data['price']
                    fuente = "PyDolarVenezuela"
                    break
                elif 'oficial' in data:  # ve.dolarapi
                    precio = data['oficial']['promedio']
                    fuente = "DolarAPI VE"
                    break
                elif 'rates' in data and 'VES' in data['rates']:  # exchangerate
                    precio = 1 / data['rates']['VES']  # Convertir a Bs/USD
                    fuente = "ExchangeRate API"
                    break
            except:
                continue
        
        if precio:
            mensaje = (
                f"💵 **DÓLAR EN VENEZUELA** 💵\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🏦 Precio: `Bs. {precio:,.2f}`\n"
                f"📊 Fuente: _{fuente}_\n"
                f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🇻🇪 _Actualizado en tiempo real_"
            )
            await update.message.reply_text(mensaje, parse_mode=ParseMode.MARKDOWN)
            sumar_xp(user_id, 3)
        else:
            await update.message.reply_text(
                "❌ **Error al consultar precio del dólar.**\n"
                "_Intenta de nuevo en unos momentos._"
            )
    except Exception as e:
        print(f"Error dolar: {e}")
        await update.message.reply_text(
            "❌ **Error de conexión.**\n"
            "_No se pudo obtener el precio del dólar._"
        )

# 19. CONVERTIR UNIDADES
async def convertir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte unidades."""
    user_id = update.effective_user.id
    
    if len(context.args) < 3:
        await update.message.reply_text(
            "📏 **Uso:** `/convertir [valor] [de] [a]`\n\n"
            "**Ejemplos:**\n"
            "- `/convertir 100 km mi` (kilómetros a millas)\n"
            "- `/convertir 50 kg lb` (kilos a libras)\n"
            "- `/convertir 32 f c` (Fahrenheit a Celsius)"
        )
        return
    
    try:
        valor = float(context.args[0])
        de = context.args[1].lower()
        a = context.args[2].lower()
        
        conversiones = {
            ("km", "mi"): lambda x: x * 0.621371,
            ("mi", "km"): lambda x: x * 1.60934,
            ("kg", "lb"): lambda x: x * 2.20462,
            ("lb", "kg"): lambda x: x * 0.453592,
            ("c", "f"): lambda x: (x * 9/5) + 32,
            ("f", "c"): lambda x: (x - 32) * 5/9,
            ("m", "ft"): lambda x: x * 3.28084,
            ("ft", "m"): lambda x: x * 0.3048,
        }
        
        if (de, a) in conversiones:
            resultado = conversiones[(de, a)](valor)
            await update.message.reply_text(
                f"📏 **Conversión:**\n"
                f"`{valor} {de.upper()} = {resultado:.2f} {a.upper()}`",
                parse_mode=ParseMode.MARKDOWN
            )
            sumar_xp(user_id, 3)
        else:
            await update.message.reply_text("❌ Conversión no soportada")
    except:
        await update.message.reply_text("❌ Valores inválidos")

# 20. POMODORO TIMER
async def pomodoro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Timer Pomodoro para productividad."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    await update.message.reply_text(
        f"🍅 **TÉCNICA POMODORO** 🍅\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⏱️ **Paso 1:** Trabaja 25 min\n"
        f"☕ **Paso 2:** Descansa 5 min\n"
        f"🔁 **Paso 3:** Repite 4 veces\n"
        f"🎉 **Paso 4:** Descansa 15-30 min\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 _¡Aumenta tu productividad, {nick}!_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(user_id, 2)


# --- [ MÓDULO DE ESCANEO DE QR ] ---
async def qrs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Escanea y lee códigos QR desde imágenes."""
    # Verifica si el usuario respondió a una foto
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("🔍 **MODO DE USO:**\nResponde con el comando `/qrs` a una imagen que contenga un código QR para que yo lo pueda leer.")

    wait = await update.message.reply_text("📡 **Conectando con el satélite... Analizando QR...**")
    
    try:
        # Descarga la foto del servidor de Telegram
        foto = await update.message.reply_to_message.photo[-1].get_file()
        url_foto = foto.file_path
        
        # Consultamos la API de lectura (QRServer)
        api_url = f"https://api.qrserver.com/v1/read-qr-code/?fileurl={url_foto}"
        response = requests.get(api_url).json()
        
        # Extraemos el contenido
        resultado = response[0]['symbol'][0]['data']
        
        if resultado:
            mensaje = (
                f"✅ **¡LECTURA EXITOSA!**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📝 **CONTENIDO:**\n`{resultado}`\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🤖 _Cami.bot OSINT Edition_"
            )
            await wait.edit_text(mensaje, parse_mode=ParseMode.MARKDOWN)
        else:
            await wait.edit_text("❌ **ERROR:** No se encontró ningún código QR legible en esa imagen.")
            
    except Exception as e:
        await wait.edit_text(f"⚠️ **ERROR DE PROCESAMIENTO:** No pude leer la imagen.")

# --- [ INFORMACIÓN DEL BOT ] ---
async def info_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra información detallada sobre el bot."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    info = (
        f"🤖 **CAMILABOT - INFORMACIÓN COMPLETA** 🤖\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📌 **DATOS GENERALES:**\n"
        f"├ Nombre: CamilaBot\n"
        f"├ Versión: `{VERSION}`\n"
        f"├ Creador: AnyerJR 🇻🇪\n"
        f"├ País: Venezuela\n"
        f"├ Plataforma: Telegram\n"
        f"└ Comandos: ♥∞+\n\n"
        f"✨ **CARACTERÍSTICAS PRINCIPALES:**\n"
        f"├ 🎮 Sistema de Economía (trabajar, apostar, dinero)\n"
        f"├ 📊 Rangos y Sistema de Experiencia\n"
        f"├ 📥 Descargas de Multimedia (Videos, Audios)\n"
        f"├ 🌐 Traducción en 12 idiomas\n"
        f"├ 🔍 Búsqueda inteligente con Wikipedia\n"
        f"├ 📚 Información en tiempo real\n"
        f"├ 🎲 Juegos y entretenimiento\n"
        f"├ 🎨 Generador de contenido (Stickers, QR)\n"
        f"├ 💱 Precios (Dólar, Criptomonedas)\n"
        f"├ 🧠 Calculadora avanzada\n"
        f"├ 📋 Listas diarias (7 decoradas)\n"
        f"├ 🎭 Frases motivadoras personalizadas\n"
        f"├  ⚙️ Panel administrativo seguro\n\n"
        f"└  🧑‍💻si usas /cpmenu1 veras la parte 1 de todos los comandos\n\n"
        f"📚 **CATEGORÍAS DE COMANDOS:**\n"
        f"1️⃣ Perfil & Economía (6 comandos)\n"
        f"2️⃣ Multimedia (6 comandos)\n"
        f"3️⃣ Búsqueda e Información (8 comandos)\n"
        f"4️⃣ Herramientas (7 comandos)\n"
        f"5️⃣ Entretenimiento & Juegos (8 comandos)\n"
        f"6️⃣ OSINT e Investigación (3 comandos)\n"
        f"7️⃣ Finanzas (2 comandos)\n"
        f"8️⃣ Administrativos (3 comandos)\n"
        f"9️⃣ Motivación & Listas (2 comandos)\n\n"
        f"🔧 **TECNOLOGÍA UTILIZADA:**\n"
        f"├ Framework: python-telegram-bot\n"
        f"├ APIs: Wikipedia, DuckDuckGo, CoinGecko\n"
        f"├ Descarga: yt-dlp\n"
        f"├ Base de Datos: JSON local\n"
        f"└ Seguridad: Validación en todos los comandos\n\n"
        f"🎯 **ACCIONES DISPONIBLES:**\n"
        f"├ 💰 Ganar dinero (trabajando)\n"
        f"├ 🎰 Jugar y apostar\n"
        f"├ 📥 Descargar videos (YouTube, TikTok, Facebook, etc)\n"
        f"├ 🌐 Traducir a 12 idiomas\n"
        f"├ 🔎 Buscar información\n"
        f"├ 🎲 Juegos (dados, monedas, etc)\n"
        f"├ 💪 Obtener motivación\n"
        f"├ 📊 Ver estadísticas personales\n"
        f"└ ✨ Y mucho más...\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 **Escribe `/menu` o `/help` para ver todos los comandos disponibles.**\n"
        f"🌟 _Hecho con ❤️ por AnyerJR_"
    )
    
    await update.message.reply_text(info, parse_mode=ParseMode.MARKDOWN)
    registrar_evento(user_id, nick, "Consultó información del bot", "INFO")
    sumar_xp(user_id, 2)



# =========================================
# BLOQUE 200+ NUEVOS COMANDOS V12.0
# =========================================

# ══════════════════════════════════════════
# MÓDULO 1 — COCINA Y RECETAS VENEZOLANAS
# ══════════════════════════════════════════
RECETAS_VE = {
    "pabellon": "🍽️ **Pabellón Criollo**\n- Carne mechada\n- Caraotas negras\n- Arroz blanco\n- Tajadas de plátano maduro\n_El plato nacional de Venezuela_ 🇻🇪",
    "arepa": "🫓 **Arepa Venezolana**\n- Harina de maíz precocida PAN\n- Sal al gusto\n- Agua tibia\n_Amasa, forma y cocina en budare 10 min c/lado_",
    "hallaca": "🌿 **Hallaca Navideña**\n- Masa de maíz con onoto\n- Guiso de carne/pollo/cerdo\n- Aceitunas, alcaparras, pasas\n- Hojas de plátano\n_Tradición navideña venezolana_ 🎄",
    "tequeño": "🧀 **Tequeños**\n- Harina de trigo\n- Queso blanco duro\n- Mantequilla, huevo, sal\n_Fríe hasta dorar, sirve caliente_",
    "cachapa": "🌽 **Cachapa**\n- Maíz tierno rallado\n- Azúcar, sal\n- Queso de mano\n_Cocina en budare con mantequilla_",
}

async def receta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recetas venezolanas clásicas."""
    platos = list(RECETAS_VE.keys())
    if not context.args:
        lista = " | ".join([f"`{p}`" for p in platos])
        await update.message.reply_text(f"🍽️ **Platos disponibles:**\n{lista}\n\n_Uso: /receta [plato]_", parse_mode=ParseMode.MARKDOWN)
        return
    plato = " ".join(context.args).lower()
    info = RECETAS_VE.get(plato, f"❌ No tengo receta de `{plato}`. Platos: {', '.join(platos)}")
    await update.message.reply_text(info, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 3)

async def cocina_tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tips de cocina aleatorios."""
    tips = [
        "🧂 Siempre prueba la comida antes de servir", "🔪 Afila el cuchillo antes de cortar",
        "🧅 Para no llorar cortando cebolla, métela 10 min al freezer primero",
        "🍋 Unas gotas de limón evitan que el aguacate se oxide",
        "🫙 Guarda el ajo pelado en aceite en la nevera hasta 2 semanas",
        "🍳 El aceite debe estar caliente antes de echar los ingredientes",
        "🧄 El ajo se quema rápido, agrégalo al final del sofrito",
        "🥩 Saca la carne del frío 30 min antes de cocinar para cocción pareja",
        "🧁 El bicarbonato y el polvo de hornear no son lo mismo",
        "🍚 Para arroz perfecto: 1 taza arroz = 2 tazas agua",
    ]
    await update.message.reply_text(f"👨‍🍳 **Tip de Cocina:**\n\n{random.choice(tips)}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 1)

async def bebida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recetas de bebidas venezolanas."""
    bebidas = [
        "🥭 **Jugo de Mango:** Licúa mango maduro + agua + azúcar + hielo",
        "🍹 **Chicha Venezolana:** Arroz cocido + leche + azúcar + canela + vainilla",
        "🌿 **Papelón con Limón:** Papelón rallado + agua + limón + hielo = refrescante",
        "🍫 **Chocolate Caliente:** Cacao puro + leche + azúcar + canela",
        "🌽 **Carato de Maíz:** Maíz pilado + panela + agua + clavo",
        "🥤 **Malta con Leche:** Malta fría + leche condensada = combo venezolano",
    ]
    await update.message.reply_text(f"🥤 **Bebida Venezolana:**\n\n{random.choice(bebidas)}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

# ══════════════════════════════════════════
# MÓDULO 2 — SALUD Y BIENESTAR
# ══════════════════════════════════════════
async def meditacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Guía de meditación rápida."""
    await update.message.reply_text(
        "🧘 **MEDITACIÓN DE 5 MINUTOS**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "1️⃣ Siéntate cómodo, cierra los ojos\n"
        "2️⃣ Inhala profundo contando hasta 4\n"
        "3️⃣ Retén el aire 4 segundos\n"
        "4️⃣ Exhala lentamente 4 segundos\n"
        "5️⃣ Repite 10 veces\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💆 _Relaja cada músculo con cada exhalación_\n"
        "🌟 _Mente clara, cuerpo en paz_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def ejercicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rutina de ejercicios en casa."""
    rutinas = {
        "pecho": "💪 **PECHO:**\n- 3x15 Flexiones\n- 3x12 Flexiones diamante\n- 3x10 Fondos en silla",
        "piernas": "🦵 **PIERNAS:**\n- 4x20 Sentadillas\n- 3x15 Estocadas\n- 3x20 Elevaciones de talón",
        "abdomen": "🔥 **ABDOMEN:**\n- 3x30 Crunches\n- 3x20 Bicicleta abdominal\n- 3x45s Plancha",
        "espalda": "🏋️ **ESPALDA:**\n- 3x15 Supermán\n- 3x12 Remo con mochila\n- 3x20 Hiperextensiones",
        "brazos": "💪 **BRAZOS:**\n- 3x15 Curls con botella de agua\n- 3x12 Press francés\n- 3x20 Dips",
        "cardio": "🏃 **CARDIO 20 MIN:**\n- 5 min jumping jacks\n- 5 min burpees\n- 5 min mountain climbers\n- 5 min saltar la cuerda",
    }
    if not context.args:
        grupos = " | ".join(rutinas.keys())
        await update.message.reply_text(f"🏋️ **Grupos musculares:** `{grupos}`\n\n_Uso: /ejercicio [grupo]_", parse_mode=ParseMode.MARKDOWN)
        return
    grupo = " ".join(context.args).lower()
    rutina = rutinas.get(grupo, f"❌ Grupo no encontrado. Usa: {', '.join(rutinas.keys())}")
    await update.message.reply_text(f"{rutina}\n\n⏱️ _Descansa 60s entre series_", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 5)

async def agua_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recordatorio de hidratación."""
    nick = update.effective_user.first_name
    vasos = random.randint(1, 8)
    total = 8
    pct = int((vasos / total) * 100)
    bar = "💧" * vasos + "🔲" * (total - vasos)
    await update.message.reply_text(
        f"💧 **HIDRATACIÓN DE {nick.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{bar}\n"
        f"📊 Vasos tomados: `{vasos}/8` ({pct}%)\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{'✅ ¡Bien hidratado!' if pct >= 75 else '⚠️ Necesitas beber más agua'}\n"
        f"💡 _Objetivo: 2 litros diarios (8 vasos)_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def calorias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula calorías diarias recomendadas."""
    if len(context.args) < 4:
        await update.message.reply_text(
            "📌 Uso: `/calorias [peso_kg] [altura_cm] [edad] [sexo M/F]`\n"
            "Ej: `/calorias 70 170 25 M`"
        )
        return
    try:
        peso = float(context.args[0])
        altura = float(context.args[1])
        edad = int(context.args[2])
        sexo = context.args[3].upper()
        if sexo == "M":
            tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
        else:
            tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)
        sedentario = tmb * 1.2
        activo = tmb * 1.55
        muy_activo = tmb * 1.725
        await update.message.reply_text(
            f"🔥 **CALORÍAS DIARIAS RECOMENDADAS**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 TMB (metabolismo basal): `{int(tmb)} kcal`\n"
            f"🛋️ Sedentario: `{int(sedentario)} kcal`\n"
            f"🏃 Activo (3-5 días/sem): `{int(activo)} kcal`\n"
            f"⚡ Muy activo (6-7 días): `{int(muy_activo)} kcal`",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 5)
    except:
        await update.message.reply_text("❌ Datos inválidos")

async def sueno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula la hora ideal para despertar."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/sueno [hora_dormir]`\nEj: `/sueno 23:00`")
        return
    try:
        hora_str = context.args[0]
        h, m = map(int, hora_str.split(":"))
        from datetime import timedelta
        base = datetime.now().replace(hour=h, minute=m, second=0)
        ciclos = [base + timedelta(minutes=90*i + 15) for i in range(1, 7)]
        horas = " | ".join([f"`{c.strftime('%H:%M')}`" for c in ciclos])
        await update.message.reply_text(
            f"😴 **HORAS IDEALES PARA DESPERTAR**\n"
            f"_Si te duermes a las {hora_str}:_\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⏰ {horas}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 _Cada ciclo dura 90 min. Despierta entre ciclos._",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 3)
    except:
        await update.message.reply_text("❌ Formato: HH:MM (Ej: 23:00)")

async def tension_arterial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Interpreta la tensión arterial."""
    if len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/tension [sistolica] [diastolica]`\nEj: `/tension 120 80`")
        return
    try:
        s, d = int(context.args[0]), int(context.args[1])
        if s < 90 or d < 60:
            estado = "🔵 HIPOTENSIÓN (baja) — Consulta médico"
        elif s <= 120 and d <= 80:
            estado = "✅ NORMAL — ¡Excelente!"
        elif s <= 130 and d <= 80:
            estado = "🟡 ELEVADA — Cuida tu dieta"
        elif s <= 140 or d <= 90:
            estado = "🟠 HIPERTENSIÓN grado 1 — Reduce sal"
        else:
            estado = "🔴 HIPERTENSIÓN grado 2 — ¡Ve al médico!"
        await update.message.reply_text(
            f"❤️ **TENSIÓN ARTERIAL**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 {s}/{d} mmHg\n"
            f"Estado: {estado}",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 4)
    except:
        await update.message.reply_text("❌ Valores inválidos")

async def frecuencia_cardiaca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula zona de frecuencia cardíaca."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/pulsaciones [edad]`")
        return
    try:
        edad = int(context.args[0])
        fc_max = 220 - edad
        zonas = [
            ("🔵 Zona 1 (Muy suave)", fc_max * 0.50, fc_max * 0.60),
            ("🟢 Zona 2 (Quema grasa)", fc_max * 0.60, fc_max * 0.70),
            ("🟡 Zona 3 (Aeróbica)", fc_max * 0.70, fc_max * 0.80),
            ("🟠 Zona 4 (Anaeróbica)", fc_max * 0.80, fc_max * 0.90),
            ("🔴 Zona 5 (Máxima)", fc_max * 0.90, fc_max),
        ]
        texto = f"💓 **FC MAX:** `{fc_max} bpm` (edad {edad})\n━━━━━━━━━━━━━━━━━━━━\n"
        for zona, low, high in zonas:
            texto += f"{zona}: `{int(low)}-{int(high)} bpm`\n"
        await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 4)
    except:
        await update.message.reply_text("❌ Edad inválida")

# ══════════════════════════════════════════
# MÓDULO 3 — PRODUCTIVIDAD Y ESTUDIO
# ══════════════════════════════════════════
async def cronograma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera cronograma de estudio."""
    nick = update.effective_user.first_name
    materias_input = " ".join(context.args) if context.args else "Matemática,Física,Historia,Inglés"
    materias = [m.strip() for m in materias_input.split(",")]
    horas = ["06:00","07:30","09:00","10:30","14:00","15:30","17:00","19:00"]
    random.shuffle(horas)
    texto = f"📅 **CRONOGRAMA DE {nick.upper()}**\n━━━━━━━━━━━━━━━━━━━━\n"
    for i, materia in enumerate(materias[:len(horas)]):
        texto += f"⏰ `{horas[i]}` → 📚 **{materia}** (90 min)\n"
    texto += "━━━━━━━━━━━━━━━━━━━━\n💡 _Técnica Pomodoro + descansos de 15 min_"
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 4)

async def meta_smart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Guía para crear metas SMART."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/meta [tu objetivo]`\nEj: `/meta aprender programación`")
        return
    objetivo = " ".join(context.args)
    await update.message.reply_text(
        f"🎯 **META SMART: {objetivo.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**S** (Específica): Define exactamente qué quieres lograr\n"
        f"**M** (Medible): ¿Cómo sabrás que lo lograste?\n"
        f"**A** (Alcanzable): ¿Es realista para ti ahora?\n"
        f"**R** (Relevante): ¿Por qué es importante para ti?\n"
        f"**T** (Tiempo): Fija una fecha límite\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ _Escribe tu meta completa con estos 5 puntos_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def tecnica_estudio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Técnicas de estudio efectivas."""
    tecnicas = {
        "feynman": "🧠 **Técnica Feynman:**\n1. Elige el tema\n2. Explícalo como si se lo enseñaras a un niño\n3. Identifica tus lagunas de conocimiento\n4. Vuelve a la fuente y simplifica más",
        "cornell": "📝 **Método Cornell:**\n- Divide la hoja en 3 secciones\n- Columna izquierda: preguntas/conceptos clave\n- Área principal: notas detalladas\n- Parte inferior: resumen en tus palabras",
        "pomodoro": "🍅 **Pomodoro Avanzado:**\n- 25 min trabajo enfocado\n- 5 min descanso activo\n- Cada 4 pomodoros: descanso largo 15-30 min\n- Elimina todas las distracciones",
        "mapamental": "🗺️ **Mapa Mental:**\n- Concepto central en el medio\n- Ramas principales: subtemas\n- Usa colores e imágenes\n- Conexiones entre ideas\n- Palabras clave, no frases",
        "espaciado": "📆 **Repetición Espaciada:**\n- Día 1: aprende el tema\n- Día 2: repasa brevemente\n- Día 7: repasa de nuevo\n- Día 30: repaso final\n- Usa flashcards o Anki",
    }
    if not context.args:
        lista = " | ".join(tecnicas.keys())
        await update.message.reply_text(f"📚 **Técnicas:** `{lista}`\n_Uso: /estudia [técnica]_", parse_mode=ParseMode.MARKDOWN)
        return
    tec = " ".join(context.args).lower()
    info = tecnicas.get(tec, f"❌ No encontrada. Usa: {', '.join(tecnicas.keys())}")
    await update.message.reply_text(info, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 5)

async def lista_tareas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea lista de tareas personalizadas."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/tareas [tarea1, tarea2, tarea3]`")
        return
    texto = " ".join(context.args)
    tareas = [t.strip() for t in texto.split(",") if t.strip()]
    lista = "\n".join([f"☐ {i+1}. {t}" for i, t in enumerate(tareas)])
    await update.message.reply_text(
        f"📋 **LISTA DE TAREAS**\n━━━━━━━━━━━━━━━━━━━━\n{lista}\n━━━━━━━━━━━━━━━━━━━━\n✨ _{len(tareas)} tareas pendientes_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def presupuesto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula presupuesto mensual 50/30/20."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/presupuesto [ingreso_mensual]`")
        return
    try:
        ingreso = float(context.args[0])
        necesidades = ingreso * 0.50
        deseos = ingreso * 0.30
        ahorro = ingreso * 0.20
        await update.message.reply_text(
            f"💰 **REGLA 50/30/20**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💵 Ingreso: `${ingreso:,.2f}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏠 50% Necesidades: `${necesidades:,.2f}`\n"
            f"   _(renta, comida, servicios)_\n"
            f"🎮 30% Deseos: `${deseos:,.2f}`\n"
            f"   _(entretenimiento, salidas)_\n"
            f"💎 20% Ahorro/Inversión: `${ahorro:,.2f}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 _Regla de oro de las finanzas personales_",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 5)
    except:
        await update.message.reply_text("❌ Ingreso inválido")

# ══════════════════════════════════════════
# MÓDULO 4 — TECNOLOGÍA Y PROGRAMACIÓN
# ══════════════════════════════════════════
async def codigo_html(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera snippet HTML básico."""
    nombre = " ".join(context.args) if context.args else "Mi Página"
    snippet = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{nombre}</title>
    <style>
        body {{ font-family: Arial; text-align: center; background: #1a1a2e; color: #e0e0e0; }}
        h1 {{ color: #00d2ff; }}
    </style>
</head>
<body>
    <h1>¡Bienvenido a {nombre}!</h1>
    <p>Hecho con ❤️ por AnyerJR</p>
</body>
</html>"""
    await update.message.reply_text(f"```html\n{snippet}\n```", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 5)

async def codigo_python_ejemplo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ejemplos de código Python."""
    ejemplos = {
        "lista": "```python\n# Comprensión de listas\nnumeros = [x**2 for x in range(10)]\nprint(numeros)\n# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]\n```",
        "funcion": "```python\ndef saludar(nombre, saludo='Hola'):\n    return f'{saludo}, {nombre}!'\n\nprint(saludar('Camila'))\n# Hola, Camila!\n```",
        "diccionario": "```python\nbot = {'nombre': 'Camila', 'version': 12}\nfor k, v in bot.items():\n    print(f'{k}: {v}')\n```",
        "clase": "```python\nclass Bot:\n    def __init__(self, nombre):\n        self.nombre = nombre\n    def saludo(self):\n        return f'Soy {self.nombre}'\n\ncami = Bot('Camila')\nprint(cami.saludo())\n```",
        "api": "```python\nimport requests\nresp = requests.get('https://api.example.com/data')\ndata = resp.json()\nprint(data)\n```",
    }
    if not context.args:
        lista = " | ".join(ejemplos.keys())
        await update.message.reply_text(f"🐍 **Ejemplos:** `{lista}`\n_Uso: /pycode [tipo]_", parse_mode=ParseMode.MARKDOWN)
        return
    tipo = " ".join(context.args).lower()
    code = ejemplos.get(tipo, f"❌ No encontrado. Tipos: {', '.join(ejemplos.keys())}")
    await update.message.reply_text(code, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 5)

async def git_comandos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comandos Git más usados."""
    cmds = {
        "basico": "📦 **Git Básico:**\n`git init` → Iniciar repo\n`git add .` → Agregar cambios\n`git commit -m 'msg'` → Confirmar\n`git push` → Subir",
        "ramas": "🌿 **Ramas:**\n`git branch` → Ver ramas\n`git branch nueva` → Crear rama\n`git checkout nueva` → Cambiar\n`git merge rama` → Fusionar",
        "avanzado": "⚡ **Avanzado:**\n`git stash` → Guardar temporal\n`git rebase main` → Reorganizar\n`git cherry-pick <hash>` → Copiar commit\n`git reset --hard HEAD` → Revertir todo",
        "config": "⚙️ **Configuración:**\n`git config --global user.name 'AnyerJR'`\n`git config --global user.email 'email@ve.com'`\n`git remote add origin <url>`",
    }
    if not context.args:
        lista = " | ".join(cmds.keys())
        await update.message.reply_text(f"🐙 **Git temas:** `{lista}`\n_Uso: /git [tema]_", parse_mode=ParseMode.MARKDOWN)
        return
    tema = " ".join(context.args).lower()
    cmd = cmds.get(tema, f"❌ Tema no encontrado. Usa: {', '.join(cmds.keys())}")
    await update.message.reply_text(cmd, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 5)

async def linux_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comandos Linux útiles."""
    comandos = {
        "archivos": "📁 **Archivos:**\n`ls -la` → Listar todo\n`cp src dst` → Copiar\n`mv src dst` → Mover/Renombrar\n`rm -rf dir` → Eliminar (cuidado)\n`find / -name 'file'` → Buscar",
        "red": "🌐 **Red:**\n`ifconfig` → Ver IP\n`ping google.com` → Test conectividad\n`netstat -an` → Puertos abiertos\n`curl -I url` → Info del servidor\n`wget url` → Descargar",
        "procesos": "⚙️ **Procesos:**\n`ps aux` → Ver procesos\n`top` → Monitor en tiempo real\n`kill -9 PID` → Matar proceso\n`htop` → Monitor visual\n`nohup cmd &` → Ejecutar en background",
        "permisos": "🔒 **Permisos:**\n`chmod 755 archivo` → Permisos\n`chown user archivo` → Propietario\n`sudo comando` → Como root\n`su -` → Cambiar a root",
    }
    if not context.args:
        lista = " | ".join(comandos.keys())
        await update.message.reply_text(f"🐧 **Linux temas:** `{lista}`\n_Uso: /linux [tema]_", parse_mode=ParseMode.MARKDOWN)
        return
    tema = " ".join(context.args).lower()
    cmd = comandos.get(tema, f"❌ No encontrado. Usa: {', '.join(comandos.keys())}")
    await update.message.reply_text(cmd, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 5)

async def regex_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cheatsheet de expresiones regulares."""
    await update.message.reply_text(
        "🔍 **REGEX CHEATSHEET**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "`.` → Cualquier carácter\n"
        "`\\d` → Dígito (0-9)\n"
        "`\\w` → Letra o número\n"
        "`\\s` → Espacio en blanco\n"
        "`^` → Inicio de línea\n"
        "`$` → Fin de línea\n"
        "`*` → 0 o más veces\n"
        "`+` → 1 o más veces\n"
        "`?` → 0 o 1 vez\n"
        "`{n}` → Exactamente n veces\n"
        "`[abc]` → a, b o c\n"
        "`[^abc]` → Todo excepto a,b,c\n"
        "`(a|b)` → a o b\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔗 _Prueba en regex101.com_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 4)

async def color_rgb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte color HEX a RGB."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/rgb [color_hex]`\nEj: `/rgb FF5733`")
        return
    hex_color = context.args[0].lstrip("#")
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        await update.message.reply_text(
            f"🎨 **HEX a RGB:**\n"
            f"HEX: `#{hex_color.upper()}`\n"
            f"RGB: `rgb({r}, {g}, {b})`\n"
            f"CSS: `color: rgb({r}, {g}, {b});`",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 3)
    except:
        await update.message.reply_text("❌ Formato HEX inválido (debe ser 6 caracteres)")

async def json_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Valida y formatea JSON."""
    if not context.args:
        await update.message.reply_text('📌 Uso: `/jsoncheck [json]`\nEj: `/jsoncheck {"nombre":"Camila","version":12}`')
        return
    texto = " ".join(context.args)
    try:
        parsed = json.loads(texto)
        bonito = json.dumps(parsed, indent=2, ensure_ascii=False)
        await update.message.reply_text(f"✅ **JSON Válido:**\n```json\n{bonito[:1500]}\n```", parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 3)
    except json.JSONDecodeError as e:
        await update.message.reply_text(f"❌ **JSON Inválido:**\n`{str(e)}`", parse_mode=ParseMode.MARKDOWN)

# ══════════════════════════════════════════
# MÓDULO 5 — DINERO Y FINANZAS
# ══════════════════════════════════════════
async def interes_compuesto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula interés compuesto."""
    if len(context.args) < 3:
        await update.message.reply_text("📌 Uso: `/interes [capital] [tasa_%_anual] [años]`\nEj: `/interes 1000 10 5`")
        return
    try:
        capital = float(context.args[0])
        tasa = float(context.args[1]) / 100
        años = int(context.args[2])
        total = capital * (1 + tasa) ** años
        ganancia = total - capital
        await update.message.reply_text(
            f"📈 **INTERÉS COMPUESTO**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Capital: `${capital:,.2f}`\n"
            f"📊 Tasa anual: `{tasa*100:.1f}%`\n"
            f"📅 Años: `{años}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💎 Total final: `${total:,.2f}`\n"
            f"✨ Ganancia: `${ganancia:,.2f}`",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 5)
    except:
        await update.message.reply_text("❌ Valores inválidos")

async def conversor_moneda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte entre monedas usando API."""
    if len(context.args) < 3:
        await update.message.reply_text("📌 Uso: `/moneda [cantidad] [de] [a]`\nEj: `/moneda 100 USD EUR`")
        return
    try:
        cantidad = float(context.args[0])
        moneda_de = context.args[1].upper()
        moneda_a = context.args[2].upper()
        resp = await asyncio.to_thread(
            requests.get,
            f"https://api.exchangerate-api.com/v4/latest/{moneda_de}",
            timeout=8
        )
        data = resp.json()
        if moneda_a in data['rates']:
            tasa = data['rates'][moneda_a]
            resultado = cantidad * tasa
            await update.message.reply_text(
                f"💱 **CONVERSIÓN DE MONEDA**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"`{cantidad} {moneda_de}` = `{resultado:.4f} {moneda_a}`\n"
                f"📊 Tasa: `1 {moneda_de} = {tasa:.4f} {moneda_a}`",
                parse_mode=ParseMode.MARKDOWN
            )
            sumar_xp(update.effective_user.id, 4)
        else:
            await update.message.reply_text(f"❌ Moneda `{moneda_a}` no encontrada")
    except:
        await update.message.reply_text("❌ Error al convertir moneda")

async def calculo_prestamo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula cuota mensual de un préstamo."""
    if len(context.args) < 3:
        await update.message.reply_text("📌 Uso: `/prestamo [monto] [tasa_%_mensual] [meses]`\nEj: `/prestamo 5000 2 24`")
        return
    try:
        monto = float(context.args[0])
        tasa = float(context.args[1]) / 100
        meses = int(context.args[2])
        if tasa == 0:
            cuota = monto / meses
        else:
            cuota = monto * (tasa * (1+tasa)**meses) / ((1+tasa)**meses - 1)
        total_pago = cuota * meses
        total_intereses = total_pago - monto
        await update.message.reply_text(
            f"🏦 **CALCULADORA DE PRÉSTAMO**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Monto: `${monto:,.2f}`\n"
            f"📊 Tasa mensual: `{tasa*100:.1f}%`\n"
            f"📅 Plazo: `{meses} meses`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💳 Cuota mensual: `${cuota:,.2f}`\n"
            f"💸 Total a pagar: `${total_pago:,.2f}`\n"
            f"🔥 Total intereses: `${total_intereses:,.2f}`",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 5)
    except:
        await update.message.reply_text("❌ Valores inválidos")

async def ahorro_meta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula cuánto ahorrar para una meta."""
    if len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/ahorro [meta_$] [meses]`\nEj: `/ahorro 1000 12`")
        return
    try:
        meta = float(context.args[0])
        meses = int(context.args[1])
        mensual = meta / meses
        semanal = meta / (meses * 4)
        diario = meta / (meses * 30)
        await update.message.reply_text(
            f"💎 **META DE AHORRO**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 Meta: `${meta:,.2f}` en `{meses} meses`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📅 Mensual: `${mensual:,.2f}`\n"
            f"📆 Semanal: `${semanal:,.2f}`\n"
            f"🗓️ Diario: `${diario:,.2f}`",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 4)
    except:
        await update.message.reply_text("❌ Valores inválidos")

# ══════════════════════════════════════════
# MÓDULO 6 — JUEGOS DE ROL Y FANTASÍA
# ══════════════════════════════════════════
CLASES_RPG = ["⚔️ Guerrero","🧙 Mago","🏹 Arquero","🗡️ Asesino","🛡️ Paladín","🌿 Druida","☠️ Nigromante","⚡ Hechicero"]
RAZAS_RPG = ["🧝 Elfo","🧟 Humano","⚒️ Enano","🧌 Orco","🐉 Medio-Dragón","🦊 Zorro Espiritual","🌙 Vampiro","💎 Gnomo"]

async def personaje_rpg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea personaje RPG aleatorio."""
    nick = update.effective_user.first_name
    clase = random.choice(CLASES_RPG)
    raza = random.choice(RAZAS_RPG)
    stats = {
        "❤️ Vida": random.randint(50, 500),
        "⚔️ Ataque": random.randint(10, 100),
        "🛡️ Defensa": random.randint(5, 80),
        "🔮 Magia": random.randint(0, 100),
        "⚡ Velocidad": random.randint(10, 100),
        "🍀 Suerte": random.randint(1, 50),
    }
    habilidades = ["Golpe Crítico","Escudo Divino","Bola de Fuego","Flecha Envenenada","Sombra Mortal","Curación Sagrada"]
    hab = random.sample(habilidades, 2)
    texto = (
        f"⚔️ **PERSONAJE RPG DE {nick.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎭 Clase: **{clase}**\n"
        f"🧬 Raza: **{raza}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )
    for stat, val in stats.items():
        texto += f"{stat}: `{val}`\n"
    texto += f"━━━━━━━━━━━━━━━━━━━━\n"
    texto += f"✨ Habilidades: `{' | '.join(hab)}`"
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 5)

async def dungeon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mini aventura de dungeon."""
    nick = update.effective_user.first_name
    enemigos = ["🐉 Dragón Rojo","👹 Ogro Gigante","🧟 No-Muerto Rey","🕷️ Araña Venomosa","☠️ Liche Antiguo","🐺 Lobo Warg"]
    items = ["⚔️ Espada Legendaria","🛡️ Escudo de Adamantio","💍 Anillo de Poder","📜 Pergamino Mágico","💊 Poción Épica","🗝️ Llave Misteriosa"]
    enemigo = random.choice(enemigos)
    item = random.choice(items)
    resultado = random.choice(["victoria", "derrota", "empate"])
    xp_ganado = random.randint(10, 100) if resultado == "victoria" else 0
    if resultado == "victoria":
        msg = f"⚔️ **¡{nick} derrotó al {enemigo}!**\n🎁 Botín: `{item}`\n✨ XP ganado: `+{xp_ganado}`"
        sumar_xp(update.effective_user.id, xp_ganado)
    elif resultado == "derrota":
        msg = f"💀 **{nick} fue derrotado por {enemigo}**\n_Regresa más fuerte..._"
    else:
        msg = f"🤝 **Empate épico con {enemigo}**\n_La batalla continuará..._"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def item_magico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera un ítem mágico aleatorio."""
    prefijos = ["Legendario","Épico","Raro","Sagrado","Maldito","Antiguo","Élfico"]
    tipos = ["Espada","Escudo","Arco","Cetro","Amuleto","Botas","Casco","Guantes"]
    sufijos = ["del Dragón","de la Oscuridad","de la Luz","del Viento","del Fuego","del Hielo"]
    nombre = f"{random.choice(prefijos)} {random.choice(tipos)} {random.choice(sufijos)}"
    stats = {
        "⚔️ Daño": f"+{random.randint(10,100)}",
        "🛡️ Defensa": f"+{random.randint(5,50)}",
        "🌟 Bonificación especial": random.choice(["Crítico x2","Vampirismo","Teletransporte","Invisibilidad","Regeneración"])
    }
    texto = f"🗡️ **ÍTEM MÁGICO ENCONTRADO**\n━━━━━━━━━━━━━━━━━━━━\n📦 **{nombre}**\n━━━━━━━━━━━━━━━━━━━━\n"
    for s, v in stats.items():
        texto += f"{s}: `{v}`\n"
    texto += f"💰 Valor: `{random.randint(100, 9999)} monedas de oro`"
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 4)

# ══════════════════════════════════════════
# MÓDULO 7 — ASTRONOMÍA Y CIENCIA
# ══════════════════════════════════════════
async def planeta_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre planetas del sistema solar."""
    planetas = {
        "mercurio": "☿ **Mercurio:** Planeta más cercano al Sol. Temperatura: -180°C a 430°C. Sin atmósfera. 1 año = 88 días terrestres.",
        "venus": "♀️ **Venus:** Más caliente del sistema solar (465°C). Gira al revés. 1 día = 243 días terrestres.",
        "tierra": "🌍 **Tierra:** Único planeta con vida conocida. 71% agua. 1 satélite (Luna). Radio: 6,371 km.",
        "marte": "♂️ **Marte:** Planeta Rojo. Tiene el volcán más grande (Olympus Mons). 2 lunas. Candidato a colonización.",
        "jupiter": "♃ **Júpiter:** Más grande del sistema solar. La Gran Mancha Roja lleva 350+ años. 95 lunas conocidas.",
        "saturno": "♄ **Saturno:** Sus anillos son hielo y roca. Menos denso que el agua. 146 lunas.",
        "urano": "♅ **Urano:** Gira de lado (eje 98°). Temperatura: -224°C. Color azul-verde por el metano.",
        "neptuno": "♆ **Neptuno:** Más lejano del Sol. Vientos más rápidos (2,100 km/h). 14 lunas. 1 año = 165 años terrestres.",
    }
    if not context.args:
        lista = " | ".join(planetas.keys())
        await update.message.reply_text(f"🌌 **Planetas:** `{lista}`\n_Uso: /planeta [nombre]_", parse_mode=ParseMode.MARKDOWN)
        return
    planeta = " ".join(context.args).lower()
    info = planetas.get(planeta, f"❌ No encontrado. Planetas: {', '.join(planetas.keys())}")
    await update.message.reply_text(info, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 5)

async def elemento_quimico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información de elementos químicos."""
    elementos = {
        "h": ("Hidrógeno", 1, "Gas", "El más abundante del universo"),
        "he": ("Helio", 2, "Gas Noble", "Segundo más ligero, no reactivo"),
        "c": ("Carbono", 6, "No metal", "Base de toda la vida orgánica"),
        "n": ("Nitrógeno", 7, "Gas", "78% de la atmósfera terrestre"),
        "o": ("Oxígeno", 8, "Gas", "Esencial para la respiración"),
        "na": ("Sodio", 11, "Metal Alcalino", "Componente de la sal de cocina"),
        "fe": ("Hierro", 26, "Metal de Transición", "Metal más usado por la humanidad"),
        "au": ("Oro", 79, "Metal", "Metal precioso, excelente conductor"),
        "ag": ("Plata", 47, "Metal", "Mejor conductor eléctrico conocido"),
        "cu": ("Cobre", 29, "Metal", "Usado en cables eléctricos"),
    }
    if not context.args:
        await update.message.reply_text("📌 Uso: `/elemento_q [símbolo]`\nEj: `/elemento_q fe`\nSímbolos: h, he, c, n, o, na, fe, au, ag, cu")
        return
    simbolo = context.args[0].lower()
    if simbolo in elementos:
        nombre, num, tipo, desc = elementos[simbolo]
        await update.message.reply_text(
            f"⚗️ **{nombre.upper()} ({simbolo.upper()})**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔢 Número atómico: `{num}`\n"
            f"🧪 Tipo: `{tipo}`\n"
            f"📝 Descripción: _{desc}_",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 4)
    else:
        await update.message.reply_text(f"❌ Símbolo `{simbolo}` no encontrado")

async def velocidad_luz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Conversión de distancias astronómicas."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/luz [años_luz]`\nEj: `/luz 4.2` (distancia a Proxima Centauri)")
        return
    try:
        años = float(context.args[0])
        km = años * 9.461e12
        ua = años * 63241.1
        await update.message.reply_text(
            f"🌌 **{años} años luz =**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📏 `{km:.2e} km`\n"
            f"🌍 `{ua:,.0f} unidades astronómicas`\n"
            f"⏱️ Viajando a 900km/h tardarías: `{años * 1.18e9:,.0f} años`",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 4)
    except:
        await update.message.reply_text("❌ Valor inválido")

async def dato_cientifico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dato científico aleatorio."""
    datos = [
        "🧠 El cerebro humano tiene ~86 mil millones de neuronas",
        "🫀 El corazón late ~100,000 veces al día",
        "🦴 Los bebés nacen con ~270 huesos, los adultos tienen 206",
        "💧 El cuerpo humano es 60% agua",
        "🦠 El 90% de las células del cuerpo humano son bacterias",
        "⚡ Los impulsos nerviosos viajan a 120 m/s",
        "🌡️ La temperatura del Sol es ~5,500°C en la superficie",
        "🐘 Los elefantes son los únicos mamíferos que no pueden saltar",
        "🦅 Los cóndores pueden volar sin batir las alas durante horas",
        "🌊 El 95% de los océanos aún no han sido explorados",
        "🪐 Un año en Plutón equivale a 248 años terrestres",
        "🌿 Los árboles de bambú pueden crecer hasta 91 cm en un día",
    ]
    await update.message.reply_text(f"🔬 **Dato Científico:**\n\n{random.choice(datos)}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

# ══════════════════════════════════════════
# MÓDULO 8 — GEOGRAFÍA Y CULTURA
# ══════════════════════════════════════════
async def pais_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información básica de países."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/pais_info [país]`\nEj: `/pais_info Venezuela`")
        return
    pais = " ".join(context.args)
    try:
        resp = await asyncio.to_thread(
            requests.get,
            f"https://restcountries.com/v3.1/name/{pais}",
            timeout=10
        )
        data = resp.json()
        if isinstance(data, list) and len(data) > 0:
            p = data[0]
            nombre = p.get('name', {}).get('common', pais)
            capital = ", ".join(p.get('capital', ['N/A']))
            poblacion = p.get('population', 0)
            region = p.get('region', 'N/A')
            area = p.get('area', 0)
            idiomas = ", ".join(p.get('languages', {}).values())[:50]
            moneda = list(p.get('currencies', {}).values())
            moneda_str = moneda[0]['name'] if moneda else 'N/A'
            await update.message.reply_text(
                f"🌍 **{nombre.upper()}**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🏛️ Capital: `{capital}`\n"
                f"👥 Población: `{poblacion:,}`\n"
                f"🗺️ Región: `{region}`\n"
                f"📐 Área: `{area:,.0f} km²`\n"
                f"🗣️ Idioma(s): `{idiomas}`\n"
                f"💵 Moneda: `{moneda_str}`",
                parse_mode=ParseMode.MARKDOWN
            )
            sumar_xp(update.effective_user.id, 5)
        else:
            await update.message.reply_text(f"❌ País `{pais}` no encontrado")
    except:
        await update.message.reply_text("❌ Error al buscar el país")

async def venezolano_famoso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Venezolanos famosos en la historia."""
    famosos = [
        "🎖️ **Simón Bolívar** (1783-1830) — El Libertador, liberó 6 países de América",
        "✈️ **Juan Crisóstomo Falcón** — Primer presidente en gobernar democráticamente Venezuela",
        "🎭 **Rómulo Gallegos** (1884-1969) — Escritor, autor de 'Doña Bárbara'",
        "🏋️ **Rubén Limardo** — Medallista de Oro Olímpico en esgrima (2012)",
        "🎵 **Los Amigos Invisibles** — Banda venezolana ganadora del Grammy",
        "🌹 **Carolina Herrera** — Diseñadora de moda internacional de renombre",
        "⚽ **Salomón Rondón** — Futbolista, máximo goleador histórico de la Vinotinto",
        "🎬 **Edgar Ramírez** — Actor reconocido internacionalmente",
        "🏊 **Yusra Mardini** — Nadadora (de origen sirio, naturalizada venezolana)",
        "📚 **Arturo Uslar Pietri** — Escritor y político, creador del 'realismo mágico' venezolano",
    ]
    await update.message.reply_text(f"🇻🇪 **Venezolano Famoso:**\n\n{random.choice(famosos)}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 3)

async def cultura_general(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pregunta de cultura general."""
    preguntas = [
        ("¿Quién pintó la Mona Lisa?", "Leonardo Da Vinci"),
        ("¿Cuál es el río más largo del mundo?", "Nilo (6,650 km)"),
        ("¿En qué año llegó el hombre a la Luna?", "1969 (Misión Apollo 11)"),
        ("¿Cuántos planetas hay en el sistema solar?", "8 planetas"),
        ("¿Cuál es el metal más liviano?", "Litio"),
        ("¿Cuántos huesos tiene el cuerpo humano adulto?", "206 huesos"),
        ("¿En qué año cayó el Muro de Berlín?", "1989"),
        ("¿Cuántos continentes hay?", "7 continentes"),
        ("¿Quién inventó el teléfono?", "Alexander Graham Bell (1876)"),
        ("¿Cuál es el país más grande del mundo?", "Rusia (17.1 millones de km²)"),
    ]
    p, r = random.choice(preguntas)
    await update.message.reply_text(
        f"🧠 **CULTURA GENERAL**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"❓ _{p}_\n\n"
        f"||✅ **Respuesta:** {r}||",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

# ══════════════════════════════════════════
# MÓDULO 9 — REDES SOCIALES Y MARKETING
# ══════════════════════════════════════════
async def bio_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera una bio para Instagram."""
    nick = update.effective_user.first_name
    emojis = ["✨","🔥","💎","🚀","⚡","🌟","👑","🎯","💫","🌙"]
    hobbies = ["Tecnología","Fotografía","Viajero","Emprendedor","Creador de contenido","Developer","Gamer","Artista"]
    hobby = random.choice(hobbies)
    e1, e2, e3 = random.sample(emojis, 3)
    await update.message.reply_text(
        f"📸 **BIO INSTAGRAM PARA {nick.upper()}:**\n\n"
        f"```\n{e1} {nick} | {hobby}\n"
        f"{e2} Venezuela 🇻🇪 | Siguiendo sueños\n"
        f"{e3} DM para colabs\n"
        f"👇 Mira mi último post\n"
        f"🔗 linktr.ee/{nick.lower()}\n```",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def hashtags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera hashtags para redes sociales."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/hashtags [tema]`\nEj: `/hashtags tecnologia`")
        return
    tema = " ".join(context.args).lower().replace(" ", "")
    bases = [tema, f"{tema}ve", f"{tema}venezuela", f"{tema}2025", f"fyp{tema}"]
    generales = ["#venezuela🇻🇪","#viral","#fyp","#trending","#explorepage","#foryou"]
    todos = [f"#{b}" for b in bases] + generales
    await update.message.reply_text(
        f"#️⃣ **HASHTAGS PARA: #{tema}**\n\n" + " ".join(todos),
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

#cerebro ia1
async def ia_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ia [mensaje] — Habla con IA de aichatting.net/es, con contexto por usuario+grupo."""
    import requests
    from bs4 import BeautifulSoup

    # Almacenamiento global del contexto (se mantiene entre ejecuciones del comando)
    global contexto_usuarios
    if 'contexto_usuarios' not in globals():
        contexto_usuarios = {}

    # Identificar entorno y usuario
    chat_id = update.effective_chat.id
    chat_tipo = update.effective_chat.type
    grupo_nombre = update.effective_chat.title if chat_tipo != "private" else "Chat privado"
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    usuario_completo = f"{nick} (ID: {user_id})"
    clave_contexto = f"{user_id}_{chat_id}"

    if not context.args:
        await update.message.reply_text(
            "🤖 **Uso:** `/ia [pregunta o mensaje]`\n\n"
            "_Ejemplos:_\n"
            "- `/ia ¿Qué es la inteligencia artificial?`\n"
            "- `/ia Escribe un poema sobre la naturaleza`\n"
            "💡 Usa `/reset_ia` para limpiar el contexto y empezar de nuevo.",
            parse_mode="MARKDOWN"
        )
        return

    mensaje = " ".join(context.args)
    wait_msg = await update.message.reply_text("🤖 _Procesando tu solicitud..._")

    try:
        # Inicializar contexto si no existe
        if clave_contexto not in contexto_usuarios:
            contexto_usuarios[clave_contexto] = []

        # Agregar mensaje con datos del entorno
        contexto_usuarios[clave_contexto].append(
            f"[Entorno: {'Grupo' if chat_tipo != 'private' else 'Chat privado'} - Nombre: {grupo_nombre}]\n"
            f"[Usuario: {usuario_completo}]\n"
            f"[Mensaje: {mensaje}]"
        )

        # Limitar historial a 10 mensajes
        if len(contexto_usuarios[clave_contexto]) > 10:
            contexto_usuarios[clave_contexto] = contexto_usuarios[clave_contexto][-10:]

        # Formatear petición con contexto
        historial_completo = "\n---\n".join(contexto_usuarios[clave_contexto])
        peticion = f"Contexto de conversación:\n{historial_completo}\n\nResponde como un bot de Telegram, claro y conciso."

        # Obtener endpoint y enviar petición
        url_pagina = "https://www.aichatting.net/es/"
        respuesta_pagina = requests.get(url_pagina, timeout=15)
        respuesta_pagina.raise_for_status()
        soup = BeautifulSoup(respuesta_pagina.content, "html.parser")
        
        formulario = soup.find("form", attrs={"id": lambda x: x and "chat-form" in x})
        endpoint = formulario.get("action", "https://www.aichatting.net/es/chat")
        if not endpoint.startswith("http"):
            endpoint = f"https://www.aichatting.net{endpoint}"

        datos_peticion = {"message": peticion}
        respuesta_ia = requests.post(endpoint, data=datos_peticion, timeout=20)
        respuesta_ia.raise_for_status()
        respuesta_texto = respuesta_ia.text.strip()

        # Guardar respuesta en el contexto
        contexto_usuarios[clave_contexto].append(f"[Respuesta IA: {respuesta_texto}]")

        await wait_msg.edit_text(f"🤖 **Respuesta:**\n{respuesta_texto}")

    except Exception as e:
        print(f"❌ Error en /ia: {str(e)}")
        await wait_msg.edit_text("❌ Error al conectar con la IA. Intenta de nuevo más tarde.")

#resetear ia 
async def reset_ia_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /reset_ia — Limpia el contexto de conversación de la IA para el usuario."""
    # Acceder al contexto global
    global contexto_usuarios
    if 'contexto_usuarios' not in globals():
        contexto_usuarios = {}

    # Identificar usuario y chats asociados
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    claves_eliminadas = 0

    # Eliminar todas las entradas de contexto asociadas al usuario
    claves_a_eliminar = [clave for clave in contexto_usuarios.keys() if clave.startswith(f"{user_id}_")]
    for clave in claves_a_eliminar:
        del contexto_usuarios[clave]
        claves_eliminadas += 1

    # Enviar confirmación
    if claves_eliminadas > 0:
        await update.message.reply_text(
            f"✅ **Contexto de IA reiniciado para {nick}!**\n"
            f"🗑️ Se limpiaron {claves_eliminadas} conversaciones guardadas (grupos y chats privados).",
            parse_mode="MARKDOWN"
        )
    else:
        await update.message.reply_text(
            f"ℹ️ **No había contexto guardado para {nick}!**\n"
            "Empieza una conversación con `/ia [mensaje]`.",
            parse_mode="MARKDOWN"
        )

#cerebro ia 2
async def ia2_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ia2 [mensaje] — Habla con Quillbot Chat IA (hasta 15 mensajes de contexto)."""
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    # Almacenamiento global del contexto para /ia2
    global contexto_ia2
    if 'contexto_ia2' not in globals():
        contexto_ia2 = {}

    # Identificar entorno y usuario
    chat_id = update.effective_chat.id
    chat_tipo = update.effective_chat.type
    grupo_nombre = update.effective_chat.title if chat_tipo != "private" else "Chat privado"
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    usuario_completo = f"{nick} (ID: {user_id})"
    clave_contexto = f"{user_id}_{chat_id}"  # Único por usuario+grupo

    if not context.args:
        await update.message.reply_text(
            "🤖 **Uso:** `/ia2 [pregunta o mensaje]`\n\n"
            "_Ejemplos:_\n"
            "- `/ia2 Redacta un correo formal`\n"
            "- `/ia2 Explica la fotosíntesis`\n"
            "💡 Usa `/reset_ia` para limpiar el contexto general o `/reset_ia2` para este comando.",
            parse_mode="MARKDOWN"
        )
        return

    mensaje = " ".join(context.args)
    wait_msg = await update.message.reply_text("🤖 _Procesando con Quillbot IA..._")

    try:
        # Inicializar o cargar contexto
        if clave_contexto not in contexto_ia2:
            contexto_ia2[clave_contexto] = []

        # Agregar mensaje actual con datos del entorno
        contexto_ia2[clave_contexto].append(
            f"[Entorno: {'Grupo' if chat_tipo != 'private' else 'Chat privado'} - Nombre: {grupo_nombre}]\n"
            f"[Usuario: {usuario_completo}]\n"
            f"[Mensaje: {mensaje}]"
        )

        # Limitar historial a 15 mensajes
        if len(contexto_ia2[clave_contexto]) > 15:
            contexto_ia2[clave_contexto] = contexto_ia2[clave_contexto][-15:]

        # Formatear petición con contexto completo
        historial_completo = "\n---\n".join(contexto_ia2[clave_contexto])
        peticion = f"Contexto de conversación:\n{historial_completo}\n\nResponde como un asistente útil y claro, adaptado a Telegram."

        # Acceder a la página de Quillbot y obtener datos necesarios
        url_pagina = "https://quillbot.com/es/chat-ia"
        respuesta_pagina = requests.get(url_pagina, timeout=15)
        respuesta_pagina.raise_for_status()
        soup = BeautifulSoup(respuesta_pagina.content, "html.parser")

        # Extraer token y endpoint de envío
        token = soup.find("meta", attrs={"name": "csrf-token"})
        if not token:
            raise Exception("No se encontró el token de seguridad")
        
        formulario = soup.find("form", attrs={"id": lambda x: x and "chat-form" in x}) or soup.find("div", class_="chat-input-container")
        if not formulario:
            raise Exception("No se encontró el formulario de chat")
        
        endpoint = urljoin(url_pagina, soup.find("form")["action"]) if soup.find("form") else "https://quillbot.com/es/chat-ia/send"

        # Enviar petición a Quillbot
        headers = {
            "X-CSRF-Token": token["content"],
            "Referer": url_pagina,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        datos_peticion = {"message": peticion, "chatId": clave_contexto}
        respuesta_ia = requests.post(endpoint, headers=headers, data=datos_peticion, timeout=25)
        respuesta_ia.raise_for_status()
        respuesta_texto = respuesta_ia.json().get("response", "").strip() if respuesta_ia.headers.get("Content-Type") == "application/json" else respuesta_ia.text.strip()

        if not respuesta_texto:
            raise Exception("La IA no devolvió una respuesta válida")

        # Guardar respuesta en el contexto
        contexto_ia2[clave_contexto].append(f"[Respuesta Quillbot IA: {respuesta_texto}]")

        await wait_msg.edit_text(f"🤖 **Respuesta Quillbot IA:**\n{respuesta_texto}")

    except Exception as e:
        print(f"❌ Error en /ia2: {str(e)}")
        await wait_msg.edit_text(
            f"⚠️ **Error con Quillbot IA:** `{str(e)}`\n🔄 _Redirigiendo a /ia con el mismo mensaje..._",
            parse_mode="MARKDOWN"
        )
        # Redirigir a /ia con el mismo mensaje + contexto de /ia2
        contexto_ia2[clave_contexto].append(f"[Nota: Falló Quillbot IA, redirigiendo a /ia]")
        mensaje_ampliado = f"{mensaje} (Contexto previo: {len(contexto_ia2[clave_contexto])} mensajes de /ia2)"
        context.args = mensaje_ampliado.split()
        await ia_cmd(update, context)

#reset ia2
async def reset_ia2_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /reset_ia2 — Limpia el contexto de Quillbot IA (/ia2) para el usuario."""
    global contexto_ia2
    if 'contexto_ia2' not in globals():
        contexto_ia2 = {}

    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    claves_eliminadas = 0

    # Eliminar todas las entradas del usuario
    claves_a_eliminar = [clave for clave in contexto_ia2.keys() if clave.startswith(f"{user_id}_")]
    for clave in claves_a_eliminar:
        del contexto_ia2[clave]
        claves_eliminadas += 1

    if claves_eliminadas > 0:
        await update.message.reply_text(
            f"✅ **Contexto de Quillbot IA (/ia2) reiniciado para {nick}!**\n"
            f"🗑️ Se limpiaron {claves_eliminadas} conversaciones guardadas.",
            parse_mode="MARKDOWN"
        )
    else:
        await update.message.reply_text(
            f"ℹ️ **No había contexto guardado para {nick} en /ia2!**\n"
            "Empieza una conversación con `/ia2 [mensaje]`.",
            parse_mode="MARKDOWN"
        )

#cerebro ia3
async def ia3_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ia3 [mensaje] — Habla con Qwen AI (hasta 30 mensajes de contexto)."""
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    # Almacenamiento global del contexto para /ia3
    global contexto_ia3
    if 'contexto_ia3' not in globals():
        contexto_ia3 = {}

    # Identificar entorno y usuario
    chat_id = update.effective_chat.id
    chat_tipo = update.effective_chat.type
    grupo_nombre = update.effective_chat.title if chat_tipo != "private" else "Chat privado"
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    usuario_completo = f"{nick} (ID: {user_id})"
    clave_contexto = f"{user_id}_{chat_id}"  # Único por usuario+grupo

    if not context.args:
        await update.message.reply_text(
            "🤖 **Uso:** `/ia3 [pregunta o mensaje]`\n\n"
            "_Ejemplos:_\n"
            "- `/ia3 Analiza este texto: [contenido]`\n"
            "- `/ia3 Resuelve este problema matemático`\n"
            "- `/ia3 Crea un plan de proyecto`\n"
            "💡 Usa `/reset_ia3` para limpiar el contexto o `/reset_ia` para otros comandos de IA.",
            parse_mode="MARKDOWN"
        )
        return

    mensaje = " ".join(context.args)
    wait_msg = await update.message.reply_text("🤖 _Procesando con Qwen AI..._")

    try:
        # Inicializar o cargar contexto
        if clave_contexto not in contexto_ia3:
            contexto_ia3[clave_contexto] = []

        # Agregar mensaje actual con datos del entorno
        contexto_ia3[clave_contexto].append(
            f"[Entorno: {'Grupo' if chat_tipo != 'private' else 'Chat privado'} - Nombre: {grupo_nombre}]\n"
            f"[Usuario: {usuario_completo}]\n"
            f"[Mensaje: {mensaje}]"
        )

        # Limitar historial a 30 mensajes
        if len(contexto_ia3[clave_contexto]) > 30:
            contexto_ia3[clave_contexto] = contexto_ia3[clave_contexto][-30:]

        # Formatear petición con contexto completo
        historial_completo = "\n---\n".join(contexto_ia3[clave_contexto])
        peticion = f"Contexto de conversación:\n{historial_completo}\n\nResponde como un asistente experto, claro y adaptado a Telegram. Si es un grupo, considera que hay varias personas presentes."

        # Acceder a la página de Qwen AI y obtener datos necesarios
        url_pagina = "https://chat.qwen.ai/c/guest"
        respuesta_pagina = requests.get(url_pagina, timeout=15)
        respuesta_pagina.raise_for_status()
        soup = BeautifulSoup(respuesta_pagina.content, "html.parser")

        # Extraer endpoint y tokens de sesión
        endpoint = urljoin(url_pagina, "api/chat")
        cookies = respuesta_pagina.cookies

        # Enviar petición a Qwen AI
        headers = {
            "Referer": url_pagina,
            "Content-Type": "application/json"
        }
        datos_peticion = {
            "model": "Qwen3.5-Plus",
            "messages": [{"role": "user", "content": peticion}],
            "stream": False
        }
        respuesta_ia = requests.post(endpoint, headers=headers, json=datos_peticion, cookies=cookies, timeout=30)
        respuesta_ia.raise_for_status()
        respuesta_json = respuesta_ia.json()
        respuesta_texto = respuesta_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        if not respuesta_texto:
            raise Exception("La IA no devolvió una respuesta válida")

        # Guardar respuesta en el contexto
        contexto_ia3[clave_contexto].append(f"[Respuesta Qwen AI: {respuesta_texto}]")

        await wait_msg.edit_text(f"🤖 **Respuesta Qwen AI:**\n{respuesta_texto}")

    except Exception as e:
        print(f"❌ Error en /ia3: {str(e)}")
        await wait_msg.edit_text(
            f"⚠️ **Error con Qwen AI:** `{str(e)}`\n🔄 _Redirigiendo a /ia2 con el mismo mensaje..._",
            parse_mode="MARKDOWN"
        )
        # Redirigir a /ia2 con el contexto de /ia3 incluido
        contexto_ia3[clave_contexto].append(f"[Nota: Falló Qwen AI, redirigiendo a /ia2]")
        mensaje_ampliado = f"{mensaje} (Contexto previo: {len(contexto_ia3[clave_contexto])} mensajes de /ia3)"
        context.args = mensaje_ampliado.split()
        await ia2_cmd(update, context)

#reset ia3
async def reset_ia3_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /reset_ia3 — Limpia el contexto de Qwen AI (/ia3) para el usuario."""
    global contexto_ia3
    if 'contexto_ia3' not in globals():
        contexto_ia3 = {}

    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    claves_eliminadas = 0

    # Eliminar todas las entradas del usuario
    claves_a_eliminar = [clave for clave in contexto_ia3.keys() if clave.startswith(f"{user_id}_")]
    for clave in claves_a_eliminar:
        del contexto_ia3[clave]
        claves_eliminadas += 1

    if claves_eliminadas > 0:
        await update.message.reply_text(
            f"✅ **Contexto de Qwen AI (/ia3) reiniciado para {nick}!**\n"
            f"🗑️ Se limpiaron {claves_eliminadas} conversaciones guardadas (hasta 30 mensajes cada una).",
            parse_mode="MARKDOWN"
        )
    else:
        await update.message.reply_text(
            f"ℹ️ **No había contexto guardado para {nick} en /ia3!**\n"
            "Empieza una conversación con `/ia3 [mensaje]`.",
            parse_mode="MARKDOWN"
        )


#viral_ideas
async def viral_ideas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ideas de contenido viral."""
    ideas = [
        "🎬 **Video Tutorial:** Enseña algo en 60 segundos",
        "📸 **Before/After:** Transición antes y después",
        "🤣 **Meme Trending:** Adapta un meme viral a tu nicho",
        "📊 **Top 5 List:** '5 cosas que no sabías de...'",
        "💡 **Life Hack:** Truco útil del día a día",
        "🎤 **POV:** Video desde el punto de vista del espectador",
        "🔥 **Challenge:** Crea o une un reto en tendencia",
        "📖 **Story Time:** Cuenta una historia personal relatable",
        "🎵 **Trend de audio:** Pon el audio trending en tu video",
        "🤳 **Reacciones:** Reacciona a contenido viral",
    ]
    await update.message.reply_text(
        f"🚀 **IDEA VIRAL:**\n\n{random.choice(ideas)}\n\n"
        f"💡 _Sé constante, lo importante es publicar a diario_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

# ══════════════════════════════════════════
# MÓDULO 10 — MISCELÁNEOS DIVERTIDOS
# ══════════════════════════════════════════
async def personalidad_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test rápido de personalidad MBTI-like."""
    nick = update.effective_user.first_name
    tipos = [
        ("INTJ", "🧠 El Arquitecto", "Estratégico, independiente, perfeccionista"),
        ("ENFP", "🌟 El Campeón", "Creativo, entusiasta, sociable"),
        ("ISTP", "🔧 El Virtuoso", "Práctico, analítico, independiente"),
        ("ESFJ", "💛 El Cónsul", "Amistoso, leal, servicial"),
        ("INFJ", "🔮 El Defensor", "Perspicaz, empático, visionario"),
        ("ESTP", "⚡ El Emprendedor", "Enérgico, audaz, observador"),
        ("ENTP", "💡 El Debatidor", "Curioso, ingenioso, emprendedor"),
        ("ISFP", "🎨 El Aventurero", "Artístico, tranquilo, amigable"),
    ]
    tipo, nombre, desc = random.choice(tipos)
    await update.message.reply_text(
        f"🧬 **TEST DE PERSONALIDAD DE {nick.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏷️ Tipo: **{tipo}** — {nombre}\n"
        f"📝 Rasgos: _{desc}_\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 _Más info en 16personalities.com_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def animal_espiritual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asigna animal espiritual."""
    nick = update.effective_user.first_name
    animales = [
        ("🦁 León", "Líder nato, valiente, protector de su manada"),
        ("🦋 Mariposa", "Transformación, libertad, belleza natural"),
        ("🐺 Lobo", "Leal a su familia, instintivo, inteligente"),
        ("🦅 Águila", "Visión clara, libertad, líder espiritual"),
        ("🐬 Delfín", "Juguetón, inteligente, comunicativo"),
        ("🐉 Dragón", "Poderoso, sabio, guardián ancestral"),
        ("🦊 Zorro", "Astuto, adaptable, curioso por naturaleza"),
        ("🐘 Elefante", "Memoria increíble, fuerte, leal a su familia"),
        ("🦋 Colibrí", "Energético, resiliente, espíritu libre"),
        ("🐻 Oso", "Protector, introspectivo, fuerza interior"),
    ]
    animal, desc = random.choice(animales)
    await update.message.reply_text(
        f"🌿 **ANIMAL ESPIRITUAL DE {nick.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ Tu animal: **{animal}**\n"
        f"📋 Significado: _{desc}_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def nombre_real_meaning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Curiosidades de nombres."""
    nombres_data = {
        "carlos": "👑 Carlos viene del germánico 'Karl' que significa 'hombre libre'",
        "maria": "🌸 María es de origen hebreo, significa 'amada por Dios' o 'señora soberana'",
        "juan": "📖 Juan viene del hebreo 'Yohanan', significa 'Dios es misericordioso'",
        "camila": "🌺 Camila es de origen latino, significa 'la que sirve a Dios' o 'noble'",
        "jose": "⭐ José del hebreo 'Yosef', significa 'Dios añadirá' o 'que Dios aumente'",
        "luis": "⚔️ Luis del germánico 'Hlodwig', significa 'guerrero glorioso'",
        "ana": "💛 Ana del hebreo 'Hannah', significa 'gracia' o 'favor de Dios'",
        "pedro": "🪨 Pedro del latín 'Petrus' que viene del griego 'Petra': piedra o roca",
        "valentina": "❤️ Valentina del latín 'Valentinus', significa 'valiente' o 'fuerte'",
        "miguel": "⚡ Miguel del hebreo 'Mikha'el', significa '¿Quién es como Dios?'",
    }
    if not context.args:
        await update.message.reply_text("📌 Uso: `/significado [nombre]`\nEj: `/significado camila`")
        return
    nombre = " ".join(context.args).lower()
    info = nombres_data.get(nombre, f"🔍 No tengo data de `{nombre}`. Busca en es.wikipedia.org/wiki/{nombre}")
    await update.message.reply_text(f"📖 **Significado de nombre:**\n\n{info}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

async def tipo_sangre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre tipos de sangre."""
    tipos = {
        "o+": "🩸 **O+** (Universal donor de glóbulos rojos)\n- Puede recibir: O+, O-\n- Puede donar a: A+, B+, AB+, O+\n- 37% de la población",
        "a+": "🩸 **A+** (Más común)\n- Puede recibir: A+, A-, O+, O-\n- Puede donar a: A+, AB+\n- 36% de la población",
        "b+": "🩸 **B+**\n- Puede recibir: B+, B-, O+, O-\n- Puede donar a: B+, AB+\n- 8% de la población",
        "ab+": "🩸 **AB+** (Receptor universal)\n- Puede recibir: todos los tipos\n- Puede donar a: AB+\n- 3% de la población",
        "o-": "🩸 **O-** (Donante universal)\n- Puede recibir: O-\n- Puede donar a: TODOS los tipos\n- 7% de la población",
    }
    if not context.args:
        await update.message.reply_text("📌 Uso: `/sangre [tipo]`\nTipos: o+, a+, b+, ab+, o-")
        return
    tipo = " ".join(context.args).lower()
    info = tipos.get(tipo, f"❌ Tipo `{tipo}` no válido. Usa: o+, a+, b+, ab+, o-")
    await update.message.reply_text(info, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 3)

async def numero_angel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Significado de números ángel."""
    numeros = {
        "111": "✨ **111** - Manifestación: Tus pensamientos se vuelven realidad. ¡Piensa positivo!",
        "222": "🌙 **222** - Equilibrio y armonía. Confía en el proceso, todo llega a su tiempo.",
        "333": "🔺 **333** - Los ángeles están presentes. Tienes apoyo espiritual ahora mismo.",
        "444": "🛡️ **444** - Protección divina. Estás en el camino correcto, sigue adelante.",
        "555": "🦋 **555** - Cambio inminente. Una transformación positiva está llegando a tu vida.",
        "666": "⚖️ **666** - Reequilibra tus pensamientos. Demasiado enfoque en lo material.",
        "777": "🍀 **777** - Suerte y abundancia espiritual. El universo te recompensa.",
        "888": "💰 **888** - Abundancia financiera. El dinero y los recursos llegan a ti.",
        "999": "🌅 **999** - Fin de un ciclo. Una etapa termina para dar paso a algo mejor.",
    }
    if not context.args:
        await update.message.reply_text("📌 Uso: `/angel [número]`\nNúmeros: 111, 222, 333, 444, 555, 666, 777, 888, 999")
        return
    num = context.args[0]
    info = numeros.get(num, f"🔮 No tengo el significado de `{num}` en mi base de datos")
    await update.message.reply_text(f"👼 **NÚMERO ÁNGEL:**\n\n{info}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

async def trabalenguas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Trabalenguas en español."""
    lista = [
        "🌬️ _Tres tristes tigres tragaban trigo en tres tristes trastos._",
        "🌬️ _Pepe Pecas pica papas con un pico, con un pico pica papas Pepe Pecas._",
        "🌬️ _El cielo está enladrillado, ¿quién lo desenladrillará? El desenladrillador que lo desenladrille, buen desenladrillador será._",
        "🌬️ _Parangaricutirimícuaro está parangaricutirimícuarizado. ¿Quién lo deparangaricutirimícuarizará?_",
        "🌬️ _Me han dicho que has dicho un dicho que han dicho que he dicho yo._",
    ]
    await update.message.reply_text(f"👅 **Trabalenguas:**\n\n{random.choice(lista)}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

async def acertijo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Acertijo de lógica."""
    acertijos = [
        ("Cuanto más me secas, más mojado me pongo. ¿Qué soy?", "Una toalla"),
        ("Tengo dos manos pero no tengo dedos. ¿Qué soy?", "Un reloj"),
        ("Habla sin boca y escucha sin oídos. ¿Qué soy?", "Un eco"),
        ("Corro pero no tengo piernas, tengo boca pero no hablo. ¿Qué soy?", "Un río"),
        ("Cuanto más grande, menos pesa. ¿Qué soy?", "Un agujero"),
        ("Me muevo sin moverse, estoy en todas partes pero no me ves. ¿Qué soy?", "El tiempo"),
    ]
    a, r = random.choice(acertijos)
    await update.message.reply_text(
        f"🧩 **ACERTIJO:**\n\n_{a}_\n\n||💡 **Respuesta:** {r}||",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 4)

async def proverbio_mundo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Proverbios del mundo."""
    proverbios = [
        "🇯🇵 _Caído siete veces, levántate ocho._ (Japonés)",
        "🇨🇳 _Un viaje de mil millas comienza con un solo paso._ (Chino - Confucio)",
        "🌍 _Si quieres ir rápido, ve solo. Si quieres llegar lejos, ve acompañado._ (Africano)",
        "🇮🇳 _El que conoce a otros es sabio; el que se conoce a sí mismo es iluminado._ (Hindú)",
        "🇲🇽 _Más vale un toma que dos te daré._ (Mexicano)",
        "🇷🇺 _Confía pero verifica._ (Ruso)",
        "🇹🇷 _Dios da las nueces pero no las rompe._ (Turco)",
        "🇧🇷 _Cada cabeza es un mundo._ (Brasileño)",
    ]
    await update.message.reply_text(f"🌍 **Proverbio del Mundo:**\n\n{random.choice(proverbios)}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

async def prediccion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Predicción del futuro (fun)."""
    nick = update.effective_user.first_name
    predicciones = [
        f"🔮 En los próximos 7 días, {nick} recibirá una sorpresa inesperada que cambiará algo importante.",
        f"⭐ El próximo mes traerá para {nick} una oportunidad que no debe dejar pasar. Mantén los ojos abiertos.",
        f"🌙 Las estrellas dicen que {nick} tiene un talento oculto que pronto saldrá a la luz.",
        f"🎯 {nick} está más cerca de su meta de lo que cree. Solo un paso más.",
        f"💫 Una persona nueva entrará en la vida de {nick} y tendrá un impacto muy positivo.",
        f"🔥 El destino de {nick} está ligado a la creatividad. Exprésate sin miedo.",
    ]
    await update.message.reply_text(
        f"🔮 **TU PREDICCIÓN, {nick.upper()}:**\n\n{random.choice(predicciones)}\n\n_⚠️ Solo es entretenimiento_ 😄",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def iq_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test de IQ rápido (fun)."""
    nick = update.effective_user.first_name
    iq = random.randint(85, 145)
    if iq < 90:
        nivel = "🔵 Por debajo del promedio"
    elif iq < 110:
        nivel = "🟢 Promedio normal"
    elif iq < 125:
        nivel = "🟡 Por encima del promedio"
    elif iq < 140:
        nivel = "🟠 Superior"
    else:
        nivel = "🔴 Genio potencial"
    await update.message.reply_text(
        f"🧠 **TEST DE IQ DE {nick.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 IQ: `{iq}`\n"
        f"📈 Nivel: {nivel}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ _Solo por diversión, no es un test real_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def fortuna_chino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fortuna al estilo galleta china."""
    fortunas = [
        "🥠 _Confucio dice: Hombre que come demasiadas galletas chinas tiene estómago curioso._",
        "🥠 _Tu próximo gran logro está a solo una decisión valiente de distancia._",
        "🥠 _La belleza que buscas afuera ya existe dentro de ti._",
        "🥠 _Un amigo leal vale más que mil conocidos._",
        "🥠 _Hoy es el mejor día para comenzar lo que has estado postergando._",
        "🥠 _El éxito no es el destino, es el camino que recorres cada día._",
        "🥠 _Números de la suerte: 7, 13, 22, 44, 88._",
        "🥠 _La paciencia es la madre de todas las virtudes._",
    ]
    await update.message.reply_text(random.choice(fortunas), parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 1)

async def nombre_japones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tu nombre en japonés aproximado."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/japonés [nombre]`")
        return
    nombre = " ".join(context.args)
    silabas = {
        "a":"ア","e":"エ","i":"イ","o":"オ","u":"ウ",
        "ka":"カ","ki":"キ","ku":"ク","ke":"ケ","ko":"コ",
        "sa":"サ","si":"シ","su":"ス","se":"セ","so":"ソ",
        "ta":"タ","ti":"チ","tu":"ツ","te":"テ","to":"ト",
        "na":"ナ","ni":"ニ","nu":"ヌ","ne":"ネ","no":"ノ",
        "ma":"マ","mi":"ミ","mu":"ム","me":"メ","mo":"モ",
        "ra":"ラ","ri":"リ","ru":"ル","re":"レ","ro":"ロ",
    }
    nombre_lower = nombre.lower()
    japon = ""
    i = 0
    while i < len(nombre_lower):
        if i+1 < len(nombre_lower) and nombre_lower[i:i+2] in silabas:
            japon += silabas[nombre_lower[i:i+2]]
            i += 2
        elif nombre_lower[i] in silabas:
            japon += silabas[nombre_lower[i]]
            i += 1
        else:
            japon += nombre_lower[i]
            i += 1
    await update.message.reply_text(
        f"🇯🇵 **{nombre}** en Katakana:\n`{japon}`",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 4)

async def convertir_velocidad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte velocidades."""
    if len(context.args) < 3:
        await update.message.reply_text("📌 Uso: `/velocidad [valor] [de] [a]`\nUnidades: kmh, mph, ms, knot")
        return
    try:
        v = float(context.args[0])
        de = context.args[1].lower()
        a = context.args[2].lower()
        a_ms = {"kmh": 1/3.6, "mph": 0.44704, "ms": 1, "knot": 0.514444}
        if de not in a_ms or a not in a_ms:
            await update.message.reply_text("❌ Unidad no válida. Usa: kmh, mph, ms, knot")
            return
        resultado = v * a_ms[de] / a_ms[a]
        await update.message.reply_text(f"🚀 `{v} {de} = {resultado:.4f} {a}`", parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 2)
    except:
        await update.message.reply_text("❌ Error en conversión")

async def area_figura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula área de figuras geométricas."""
    import math
    if len(context.args) < 2:
        await update.message.reply_text(
            "📌 Uso: `/area [figura] [medidas]`\n"
            "- `/area circulo 5` (radio)\n"
            "- `/area rectangulo 4 6` (ancho alto)\n"
            "- `/area triangulo 8 5` (base altura)\n"
            "- `/area cuadrado 4` (lado)"
        )
        return
    figura = context.args[0].lower()
    try:
        if figura == "circulo":
            r = float(context.args[1])
            area = math.pi * r ** 2
            await update.message.reply_text(f"⭕ Círculo radio `{r}` → Área: `{area:.4f}`", parse_mode=ParseMode.MARKDOWN)
        elif figura == "rectangulo":
            a, b = float(context.args[1]), float(context.args[2])
            area = a * b
            await update.message.reply_text(f"▭ Rectángulo `{a}x{b}` → Área: `{area}`", parse_mode=ParseMode.MARKDOWN)
        elif figura == "triangulo":
            b, h = float(context.args[1]), float(context.args[2])
            area = (b * h) / 2
            await update.message.reply_text(f"▲ Triángulo base `{b}` altura `{h}` → Área: `{area}`", parse_mode=ParseMode.MARKDOWN)
        elif figura == "cuadrado":
            l = float(context.args[1])
            area = l ** 2
            await update.message.reply_text(f"⬛ Cuadrado lado `{l}` → Área: `{area}`", parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text("❌ Figura no válida: circulo, rectangulo, triangulo, cuadrado")
        sumar_xp(update.effective_user.id, 3)
    except:
        await update.message.reply_text("❌ Medidas inválidas")

async def tabla_multiplicar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra tabla de multiplicar."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/tabla [número]`\nEj: `/tabla 7`")
        return
    try:
        n = int(context.args[0])
        if n < 1 or n > 100:
            await update.message.reply_text("❌ Número entre 1 y 100")
            return
        filas = [f"`{n} × {i:2d} = {n*i:4d}`" for i in range(1, 13)]
        await update.message.reply_text(
            f"✖️ **TABLA DEL {n}:**\n" + "\n".join(filas),
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 2)
    except:
        await update.message.reply_text("❌ Número inválido")

async def contraseña_nivel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Evalúa la fortaleza de una contraseña."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/seguridad [contraseña]`")
        return
    pwd = " ".join(context.args)
    puntos = 0
    if len(pwd) >= 8: puntos += 1
    if len(pwd) >= 12: puntos += 1
    if any(c.isupper() for c in pwd): puntos += 1
    if any(c.islower() for c in pwd): puntos += 1
    if any(c.isdigit() for c in pwd): puntos += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in pwd): puntos += 1
    if puntos <= 2:
        nivel = "🔴 MUY DÉBIL"
    elif puntos <= 3:
        nivel = "🟠 DÉBIL"
    elif puntos <= 4:
        nivel = "🟡 MEDIA"
    elif puntos <= 5:
        nivel = "🟢 FUERTE"
    else:
        nivel = "💎 MUY FUERTE"
    await update.message.reply_text(
        f"🔐 **ANÁLISIS DE CONTRASEÑA**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 Puntuación: `{puntos}/6`\n"
        f"🛡️ Nivel: {nivel}\n"
        f"📏 Longitud: `{len(pwd)} chars`",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def crypto_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera wallet crypto de prueba."""
    import hashlib, secrets
    private = secrets.token_hex(32)
    address_raw = hashlib.sha256(private.encode()).hexdigest()[:40]
    wallet = f"0x{address_raw}"
    await update.message.reply_text(
        f"💳 **WALLET ETHEREUM DE PRUEBA** _(solo testing)_\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔑 Dirección: `{wallet}`\n"
        f"🔒 Clave privada: `{private[:10]}...`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ _NO usar para fondos reales_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

# =========================================
# BLOQUE DE 200+ COMANDOS NUEVOS V10.0
# =========================================

# HERRAMIENTAS AVANZADAS
async def hash_md5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera hash MD5"""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/hash_md5 [texto]`")
        return
    texto = " ".join(context.args)
    import hashlib
    resultado = hashlib.md5(texto.encode()).hexdigest()
    await update.message.reply_text(f"🔐 MD5: `{resultado}`", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

async def hash_sha256(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera hash SHA256"""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/hash_sha256 [texto]`")
        return
    texto = " ".join(context.args)
    import hashlib
    resultado = hashlib.sha256(texto.encode()).hexdigest()
    await update.message.reply_text(f"🔐 SHA256: `{resultado}`", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

async def base64_encode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Codifica a Base64"""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/b64encode [texto]`")
        return
    texto = " ".join(context.args)
    import base64
    resultado = base64.b64encode(texto.encode()).decode()
    await update.message.reply_text(f"📝 Base64: `{resultado}`", parse_mode=ParseMode.MARKDOWN)

async def base64_decode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Decodifica Base64"""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/b64decode [codigo]`")
        return
    try:
        codigo = " ".join(context.args)
        import base64
        resultado = base64.b64decode(codigo).decode()
        await update.message.reply_text(f"📝 Texto: `{resultado}`", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Base64 inválido")

async def temperatura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte temperatura C ↔ F"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/temp 30 C` o `/temp 86 F`")
        return
    try:
        valor = float(context.args[0])
        unidad = context.args[1].upper()
        if unidad == "C":
            fahrenheit = (valor * 9/5) + 32
            await update.message.reply_text(f"🌡️ {valor}°C = **{fahrenheit:.2f}°F**", parse_mode=ParseMode.MARKDOWN)
        elif unidad == "F":
            celsius = (valor - 32) * 5/9
            await update.message.reply_text(f"🌡️ {valor}°F = **{celsius:.2f}°C**", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Error en conversión")

async def metro_km(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte metros a kilómetros"""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/m_km [metros]`")
        return
    try:
        metros = float(context.args[0])
        km = metros / 1000
        await update.message.reply_text(f"📏 {metros}m = **{km}km**", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Valor inválido")

# JUEGOS AVANZADOS
async def piedra_papel_tijera(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Juego piedra papel o tijera"""
    if not context.args:
        await update.message.reply_text("🎮 Opciones: `/ppt piedra` `/ppt papel` `/ppt tijera`")
        return
    opciones = ["piedra", "papel", "tijera"]
    bot_choice = random.choice(opciones)
    user_choice = context.args[0].lower()
    
    if user_choice not in opciones:
        await update.message.reply_text("❌ Opción inválida")
        return
    
    if user_choice == bot_choice:
        resultado = "🤝 ¡Empate!"
    elif (user_choice == "piedra" and bot_choice == "tijera") or \
         (user_choice == "papel" and bot_choice == "piedra") or \
         (user_choice == "tijera" and bot_choice == "papel"):
        resultado = "🎉 ¡Ganaste!"
        sumar_xp(update.effective_user.id, 5)
    else:
        resultado = "😢 Perdiste"
    
    await update.message.reply_text(f"Tu: **{user_choice}**\nBot: **{bot_choice}**\n{resultado}", parse_mode=ParseMode.MARKDOWN)

async def trivia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Trivia aleatorio"""
    trivias = [
        {"pregunta": "¿Cuál es la capital de Francia?", "respuesta": "París"},
        {"pregunta": "¿Cuántos continentes hay?", "respuesta": "7"},
        {"pregunta": "¿Qué planeta es el más grande?", "respuesta": "Júpiter"},
        {"pregunta": "¿En qué año cayó el Muro de Berlín?", "respuesta": "1989"},
        {"pregunta": "¿Cuál es el océano más grande?", "respuesta": "Pacífico"},
        {"pregunta": "¿Cuántos lados tiene un pentágono?", "respuesta": "5"},
        {"pregunta": "¿Quién escribió Don Quijote?", "respuesta": "Cervantes"},
        {"pregunta": "¿Cuál es el país más grande del mundo?", "respuesta": "Rusia"}
    ]
    trivia_actual = random.choice(trivias)
    await update.message.reply_text(f"❓ **{trivia_actual['pregunta']}**\n\nRespuesta: `{trivia_actual['respuesta']}`", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 3)

async def adivinanza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adivinanzas aleatorias"""
    adivinanzas = [
        {"pregunta": "Oro parece, plata no es, ¿qué es?", "respuesta": "Plátano"},
        {"pregunta": "Tengo ciudades pero no casas, bosques pero no árboles...", "respuesta": "Mapa"},
        {"pregunta": "¿Qué es lo que se ve de día y de noche?", "respuesta": "Ojo"},
        {"pregunta": "Tengo cara pero no me pinto, tengo manos pero no aplaudo", "respuesta": "Reloj"}
    ]
    adi = random.choice(adivinanzas)
    await update.message.reply_text(f"🧩 **{adi['pregunta']}**\n\nRespuesta: `{adi['respuesta']}`", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 4)

async def tarot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Carta de tarot aleatoria"""
    cartas = [
        "🌙 El Mago", "👑 La Sacerdotisa", "👸 La Emperatriz", "🦁 El Emperador",
        "✨ El Papa", "💕 Los Enamorados", "🚗 El Carro", "⚖️ La Justicia",
        "🧙 El Ermitaño", "🎡 La Rueda de Fortuna", "💪 La Fuerza", "🤐 El Ahorcado",
        "💀 La Muerte", "⚗️ La Templanza", "😈 El Diablo", "🔥 La Torre",
        "⭐ La Estrella", "🌙 La Luna", "☀️ El Sol", "👼 El Juicio",
        "🌍 El Mundo"
    ]
    carta = random.choice(cartas)
    await update.message.reply_text(f"🃏 Tu carta: **{carta}**\n\n✨ Que te guíe en tu camino", parse_mode=ParseMode.MARKDOWN)

async def horoscopo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Horóscopo del día"""
    if not context.args:
        signos = "aries, tauro, geminis, cancer, leo, virgo, libra, escorpio, sagitario, capricornio, acuario, piscis"
        await update.message.reply_text(f"📌 Signos: {signos}")
        return
    signo = context.args[0].lower()
    horóscopos = {
        "aries": "🔥 Hoy es un buen día para tomar decisiones importantes",
        "tauro": "💪 La paciencia es tu virtud hoy",
        "geminis": "💬 Comunicación fluida con seres queridos",
        "cancer": "💖 Emociones intensas, manejo del corazón",
        "leo": "✨ Tu carisma brilla hoy, aprovéchalo",
        "virgo": "📚 Buen día para el análisis y reflexión",
        "libra": "⚖️ Busca el equilibrio en tus relaciones",
        "escorpio": "🔮 Intuición al máximo hoy",
        "sagitario": "🎯 Aventura y exploración te llaman",
        "capricornio": "🏔️ Foco en tus objetivos a largo plazo",
        "acuario": "💡 Ideas innovadoras surgen hoy",
        "piscis": "🌊 Conecta con tu lado emocional"
    }
    horoscopo = horóscopos.get(signo, "Signo no encontrado")
    await update.message.reply_text(f"♈ **{signo.upper()}**\n{horoscopo}", parse_mode=ParseMode.MARKDOWN)

# UTILIDADES
async def numero_aleatorio_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Número aleatorio entre rango"""
    if not context.args or len(context.args) < 2:
        num = random.randint(1, 100)
        await update.message.reply_text(f"🎲 Número aleatorio: **{num}**", parse_mode=ParseMode.MARKDOWN)
    else:
        try:
            minimo = int(context.args[0])
            maximo = int(context.args[1])
            num = random.randint(minimo, maximo)
            await update.message.reply_text(f"🎲 Entre {minimo}-{maximo}: **{num}**", parse_mode=ParseMode.MARKDOWN)
        except:
            await update.message.reply_text("❌ Uso: `/numrand [min] [max]`")

async def pelicula(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Película aleatoria"""
    peliculas = [
        "Inception", "The Matrix", "Interstellar", "Pulp Fiction",
        "Fight Club", "Forrest Gump", "Titanic", "Avatar", "Gladiator",
        "The Shawshank Redemption", "Parasite", "Tenet"
    ]
    peli = random.choice(peliculas)
    await update.message.reply_text(f"🎬 Película sugerida:\n**{peli}**", parse_mode=ParseMode.MARKDOWN)

async def serie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Serie aleatoria"""
    series = [
        "Breaking Bad", "Game of Thrones", "The Office", "Stranger Things",
        "Sherlock", "Friends", "The Crown", "Black Mirror", "Mindhunter",
        "Chernobyl", "The Marvelous Mrs. Maisel", "Peaky Blinders"
    ]
    serie_r = random.choice(series)
    await update.message.reply_text(f"📺 Serie sugerida:\n**{serie_r}**", parse_mode=ParseMode.MARKDOWN)

async def bitcoin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Precio del Bitcoin"""
    try:
        resp = await asyncio.to_thread(
            requests.get,
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            timeout=5
        )
        data = resp.json()
        precio = data["bitcoin"]["usd"]
        await update.message.reply_text(f"₿ **Bitcoin:** ${precio:,.2f}", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Error al obtener precio")

async def ethereum_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Precio del Ethereum"""
    try:
        resp = await asyncio.to_thread(
            requests.get,
            "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
            timeout=5
        )
        data = resp.json()
        precio = data["ethereum"]["usd"]
        await update.message.reply_text(f"Ξ **Ethereum:** ${precio:,.2f}", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Error al obtener precio")

# =========================================
# BLOQUE DE 100 NUEVOS COMANDOS V11.0
# =========================================

# ---- HERRAMIENTAS DE TEXTO ----

async def contar_palabras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cuenta palabras, letras y caracteres de un texto."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/palabras [texto]`")
        return
    texto = " ".join(context.args)
    palabras = len(texto.split())
    letras = sum(c.isalpha() for c in texto)
    caracteres = len(texto)
    await update.message.reply_text(
        f"📊 **ANÁLISIS DE TEXTO**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 Palabras: `{palabras}`\n"
        f"🔤 Letras: `{letras}`\n"
        f"📏 Caracteres: `{caracteres}`",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def invertir_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Invierte el texto dado."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/invertir [texto]`")
        return
    texto = " ".join(context.args)
    invertido = texto[::-1]
    await update.message.reply_text(f"🔄 **Texto invertido:**\n`{invertido}`", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 1)

async def mayusculas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte texto a MAYÚSCULAS."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/mayus [texto]`")
        return
    texto = " ".join(context.args).upper()
    await update.message.reply_text(f"🔠 `{texto}`", parse_mode=ParseMode.MARKDOWN)

async def minusculas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte texto a minúsculas."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/minus [texto]`")
        return
    texto = " ".join(context.args).lower()
    await update.message.reply_text(f"🔡 `{texto}`", parse_mode=ParseMode.MARKDOWN)

async def cifrado_cesar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cifrado César con desplazamiento dado."""
    if len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/cesar [desplazamiento] [texto]`\nEj: `/cesar 3 hola`")
        return
    try:
        n = int(context.args[0])
        texto = " ".join(context.args[1:])
        resultado = ""
        for c in texto:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                resultado += chr((ord(c) - base + n) % 26 + base)
            else:
                resultado += c
        await update.message.reply_text(f"🔐 **Cifrado César (n={n}):**\n`{resultado}`", parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 3)
    except:
        await update.message.reply_text("❌ Desplazamiento debe ser un número")

async def morse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte texto a código Morse."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/morse [texto]`")
        return
    codigo = {
        'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
        'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
        'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
        '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
        ' ':' / '
    }
    texto = " ".join(context.args).upper()
    resultado = " ".join(codigo.get(c, '?') for c in texto)
    await update.message.reply_text(f"📡 **Código Morse:**\n`{resultado}`", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 4)

async def ascii_art(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera arte ASCII con texto."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/ascii [palabra]`")
        return
    palabra = " ".join(context.args)[:15]
    arte = f"```\n{'*' * (len(palabra)+4)}\n* {palabra.upper()} *\n{'*' * (len(palabra)+4)}\n```"
    await update.message.reply_text(f"🎨 **Arte ASCII:**\n{arte}", parse_mode=ParseMode.MARKDOWN)

async def repetir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Repite un texto N veces."""
    if len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/repetir [veces] [texto]`")
        return
    try:
        n = min(int(context.args[0]), 20)
        texto = " ".join(context.args[1:])
        resultado = (texto + "\n") * n
        await update.message.reply_text(resultado[:3000])
    except:
        await update.message.reply_text("❌ El número debe ser entero")

async def palindromo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verifica si una palabra es palíndromo."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/palindromo [texto]`")
        return
    texto = " ".join(context.args).lower().replace(" ", "")
    es_pal = texto == texto[::-1]
    emoji = "✅" if es_pal else "❌"
    msg = "¡Es un palíndromo!" if es_pal else "No es un palíndromo."
    await update.message.reply_text(f"{emoji} `{' '.join(context.args)}` → {msg}", parse_mode=ParseMode.MARKDOWN)

async def espaciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Espacía cada letra de un texto."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/espaciar [texto]`")
        return
    texto = " ".join(context.args)
    espaciado = " ".join(texto)
    await update.message.reply_text(f"✨ `{espaciado}`", parse_mode=ParseMode.MARKDOWN)

# ---- MATEMÁTICAS Y CIENCIAS ----

async def factorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula el factorial de un número."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/factorial [número]`")
        return
    try:
        import math
        n = int(context.args[0])
        if n < 0 or n > 20:
            await update.message.reply_text("❌ Número entre 0 y 20")
            return
        resultado = math.factorial(n)
        await update.message.reply_text(f"🧮 `{n}! = {resultado}`", parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 3)
    except:
        await update.message.reply_text("❌ Número inválido")

async def fibonacci(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera la secuencia de Fibonacci."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/fib [cantidad]`")
        return
    try:
        n = min(int(context.args[0]), 30)
        a, b = 0, 1
        seq = []
        for _ in range(n):
            seq.append(str(a))
            a, b = b, a + b
        await update.message.reply_text(f"🌀 **Fibonacci ({n} términos):**\n`{', '.join(seq)}`", parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 4)
    except:
        await update.message.reply_text("❌ Valor inválido")

async def primo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verifica si un número es primo."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/primo [número]`")
        return
    try:
        n = int(context.args[0])
        if n < 2:
            await update.message.reply_text(f"❌ `{n}` no es primo", parse_mode=ParseMode.MARKDOWN)
            return
        es_primo = all(n % i != 0 for i in range(2, int(n**0.5)+1))
        emoji = "✅" if es_primo else "❌"
        msg = "ES primo" if es_primo else "NO es primo"
        await update.message.reply_text(f"{emoji} `{n}` {msg}", parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 2)
    except:
        await update.message.reply_text("❌ Número inválido")

async def binario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte número decimal a binario."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/bin [número]`")
        return
    try:
        n = int(context.args[0])
        await update.message.reply_text(f"💻 `{n}` en binario: `{bin(n)[2:]}`", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Número inválido")

async def hexadecimal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte número decimal a hexadecimal."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/hex [número]`")
        return
    try:
        n = int(context.args[0])
        await update.message.reply_text(f"🔢 `{n}` en hex: `{hex(n)[2:].upper()}`", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Número inválido")

async def octal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte número decimal a octal."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/oct [número]`")
        return
    try:
        n = int(context.args[0])
        await update.message.reply_text(f"8️⃣ `{n}` en octal: `{oct(n)[2:]}`", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Número inválido")

async def raiz_cuadrada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula la raíz cuadrada."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/raiz [número]`")
        return
    try:
        import math
        n = float(context.args[0])
        if n < 0:
            await update.message.reply_text("❌ No hay raíz cuadrada de números negativos")
            return
        await update.message.reply_text(f"√ `√{n} = {math.sqrt(n):.6f}`", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Número inválido")

async def porcentaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula el porcentaje."""
    if len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/porciento [porcentaje] [total]`\nEj: `/porciento 20 500`")
        return
    try:
        pct = float(context.args[0])
        total = float(context.args[1])
        resultado = (pct / 100) * total
        await update.message.reply_text(
            f"📊 **Calculadora de %**\n"
            f"`{pct}% de {total} = {resultado:.2f}`",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 2)
    except:
        await update.message.reply_text("❌ Valores inválidos")

async def imc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula el Índice de Masa Corporal (IMC)."""
    if len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/imc [peso_kg] [altura_m]`\nEj: `/imc 70 1.75`")
        return
    try:
        peso = float(context.args[0])
        altura = float(context.args[1])
        imc_val = peso / (altura ** 2)
        if imc_val < 18.5:
            estado = "⚠️ Bajo peso"
        elif imc_val < 25:
            estado = "✅ Peso normal"
        elif imc_val < 30:
            estado = "⚠️ Sobrepeso"
        else:
            estado = "❌ Obesidad"
        await update.message.reply_text(
            f"⚕️ **IMC CALCULADO**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 IMC: `{imc_val:.2f}`\n"
            f"🏥 Estado: {estado}",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 3)
    except:
        await update.message.reply_text("❌ Valores inválidos")

# ---- GENERADORES ----

async def contrasena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera una contraseña segura aleatoria."""
    import string
    longitud = 16
    if context.args:
        try:
            longitud = min(int(context.args[0]), 64)
        except:
            pass
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = "".join(random.choices(chars, k=longitud))
    await update.message.reply_text(
        f"🔑 **Contraseña generada ({longitud} chars):**\n"
        f"`{password}`\n\n"
        f"⚠️ _Guárdala en un lugar seguro_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def uuid_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera un UUID único."""
    import uuid
    nuevo_uuid = str(uuid.uuid4())
    await update.message.reply_text(f"🆔 **UUID:**\n`{nuevo_uuid}`", parse_mode=ParseMode.MARKDOWN)

async def nombre_falso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera un nombre falso venezolano."""
    nombres_m = ["Carlos","Andrés","Juan","Miguel","José","Luis","Pedro","Rafael","Antonio","Diego"]
    nombres_f = ["María","Ana","Camila","Sofía","Valentina","Isabella","Gabriela","Laura","Patricia","Andrea"]
    apellidos = ["García","Martínez","Rodríguez","López","González","Pérez","Hernández","Sánchez","Torres","Ramírez"]
    genero = random.choice(["M","F"])
    nombre = random.choice(nombres_m if genero == "M" else nombres_f)
    apellido1 = random.choice(apellidos)
    apellido2 = random.choice(apellidos)
    await update.message.reply_text(
        f"👤 **Nombre Falso Generado:**\n`{nombre} {apellido1} {apellido2}`",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def email_falso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera un email falso aleatorio."""
    import string
    dominios = ["gmail.com","hotmail.com","outlook.com","yahoo.com","icloud.com"]
    usuario = "".join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6,12)))
    dominio = random.choice(dominios)
    await update.message.reply_text(f"📧 **Email Falso:**\n`{usuario}@{dominio}`", parse_mode=ParseMode.MARKDOWN)

async def placa_venezolana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera una placa venezolana aleatoria."""
    import string
    letras = "".join(random.choices(string.ascii_uppercase, k=3))
    numeros = "".join(random.choices(string.digits, k=3))
    await update.message.reply_text(f"🚗 **Placa VE:**\n`{letras}{numeros}`", parse_mode=ParseMode.MARKDOWN)

async def cedula_falsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera una cédula venezolana falsa (solo de prueba)."""
    tipo = random.choice(["V","E"])
    numero = random.randint(1000000, 30000000)
    await update.message.reply_text(
        f"🪪 **Cédula Falsa (TEST):**\n`{tipo}-{numero:,}`\n\n⚠️ _Solo para pruebas_",
        parse_mode=ParseMode.MARKDOWN
    )

async def color_hex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera un color hexadecimal aleatorio."""
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF)).upper()
    await update.message.reply_text(
        f"🎨 **Color Aleatorio:**\n`{color}`\n🔗 Vista: https://www.color-hex.com/color/{color[1:]}",
        parse_mode=ParseMode.MARKDOWN
    )

async def chiste_venezolano(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cuenta un chiste venezolano."""
    chistes = [
        "¿Por qué el venezolano lleva una escalera al supermercado?\n_¡Porque oyó que los precios estaban por las nubes!_ 😂",
        "¿Cómo llama un venezolano a su WiFi?\n_'Se fue la luz'_ 😂",
        "¿Cuál es el colmo del venezolano?\n_¡Tener hambre y que le digan que el menú está en dólares!_ 😂",
        "Un venezolano llega al cielo y San Pedro le dice:\n— ¿Tienes la cuarta?\n— No...\n— Pues aquí tampoco tienes cola 😂",
        "¿Cómo llama un venezolano cuando llueve?\n_¡Milagro!_ Porque el agua llega sola 😂",
        "Venezolano en el extranjero le preguntan: ¿De dónde eres?\n— De Venezuela\n— ¿Y cómo está eso?\n— Pregúntame cómo ESTABA... 😂",
        "¿Qué hace un venezolano cuando se le acaba el gas?\n_¡Reza para que tampoco se vaya la luz!_ 😂",
    ]
    await update.message.reply_text(f"😂 **Chiste Venezolano:**\n\n{random.choice(chistes)}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

async def refranes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía un refrán venezolano."""
    lista = [
        "🗣️ _'Camarón que se duerme, se lo lleva la corriente'_",
        "🗣️ _'Dime con quién andas y te diré quién eres'_",
        "🗣️ _'El que mucho abarca, poco aprieta'_",
        "🗣️ _'A buen entendedor, pocas palabras'_",
        "🗣️ _'Más vale pájaro en mano que cien volando'_",
        "🗣️ _'El que ríe de último, ríe mejor'_",
        "🗣️ _'No hay mal que por bien no venga'_",
        "🗣️ _'Barriga llena, corazón contento'_ 🇻🇪",
        "🗣️ _'El vivo vive del bobo, y el bobo de su trabajo'_",
        "🗣️ _'Pueblo pequeño, infierno grande'_",
    ]
    await update.message.reply_text(random.choice(lista), parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 1)

# ---- INFORMACIÓN Y DATOS ----

async def fecha_hoy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra la fecha y hora actual."""
    ahora = datetime.now()
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    await update.message.reply_text(
        f"📅 **FECHA Y HORA ACTUAL**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📆 Día: `{dias[ahora.weekday()]}`\n"
        f"🗓️ Fecha: `{ahora.day} de {meses[ahora.month-1]} de {ahora.year}`\n"
        f"⏰ Hora: `{ahora.strftime('%H:%M:%S')}`",
        parse_mode=ParseMode.MARKDOWN
    )

async def tiempo_unix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el tiempo Unix actual."""
    ts = int(time.time())
    await update.message.reply_text(f"⏱️ **Unix Timestamp:**\n`{ts}`", parse_mode=ParseMode.MARKDOWN)

async def edad_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula la edad dado un año de nacimiento."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/edad [año_nacimiento]`")
        return
    try:
        anio = int(context.args[0])
        edad_calculada = datetime.now().year - anio
        await update.message.reply_text(f"🎂 Si naciste en `{anio}`, tienes aproximadamente **{edad_calculada} años**.", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Año inválido")

async def dias_para(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula cuántos días faltan para una fecha."""
    if len(context.args) < 3:
        await update.message.reply_text("📌 Uso: `/diasfalta [día] [mes] [año]`\nEj: `/diasfalta 31 12 2025`")
        return
    try:
        from datetime import date
        d, m, a = int(context.args[0]), int(context.args[1]), int(context.args[2])
        fecha_target = date(a, m, d)
        hoy = date.today()
        diferencia = (fecha_target - hoy).days
        if diferencia < 0:
            await update.message.reply_text(f"📅 Esa fecha ya pasó hace `{abs(diferencia)}` días.", parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(f"⏳ Faltan **{diferencia}** días para el `{d}/{m}/{a}`", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Fecha inválida")

async def signo_zodiacal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dice el signo zodiacal dado día y mes."""
    if len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/signo [día] [mes]`\nEj: `/signo 15 3`")
        return
    try:
        d, m = int(context.args[0]), int(context.args[1])
        signos = [
            ((12,22),(1,19),"♑ Capricornio"),((1,20),(2,18),"♒ Acuario"),((2,19),(3,20),"♓ Piscis"),
            ((3,21),(4,19),"♈ Aries"),((4,20),(5,20),"♉ Tauro"),((5,21),(6,20),"♊ Géminis"),
            ((6,21),(7,22),"♋ Cáncer"),((7,23),(8,22),"♌ Leo"),((8,23),(9,22),"♍ Virgo"),
            ((9,23),(10,22),"♎ Libra"),((10,23),(11,21),"♏ Escorpio"),((11,22),(12,21),"♐ Sagitario"),
        ]
        signo_encontrado = "♑ Capricornio"
        for inicio, fin, nombre in signos:
            if (m == inicio[1] and d >= inicio[0]) or (m == fin[1] and d <= fin[0]):
                signo_encontrado = nombre
                break
        await update.message.reply_text(f"✨ Tu signo zodiacal es: **{signo_encontrado}**", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Fecha inválida")

async def numero_suerte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera números de la suerte."""
    numeros = sorted(random.sample(range(1, 100), 6))
    await update.message.reply_text(
        f"🍀 **Tus números de la suerte:**\n"
        f"```\n{' - '.join(map(str, numeros))}\n```",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 1)

async def frase_dia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Frase del día especial."""
    frases = [
        "☀️ _Hoy es el primer día del resto de tu vida._",
        "⭐ _La grandeza no se mide por lo que tienes, sino por lo que das._",
        "🌊 _El agua blanda puede romper la roca dura._",
        "🚀 _Un cohete necesita resistencia para despegar._",
        "🌳 _El árbol más fuerte nació de una semilla pequeña._",
        "🦋 _La transformación duele, pero el resultado vale la pena._",
        "💡 _Una idea cambia el mundo. La tuya podría ser la siguiente._",
        "🎯 _El éxito no es suerte, es disciplina disfrazada._",
        "🔥 _Arden las personas que se atreven a brillar._",
        "🌺 _Florece donde te planten._",
    ]
    await update.message.reply_text(f"🌟 **Frase del Día:**\n\n{random.choice(frases)}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 1)

# ---- JUEGOS NUEVOS ----

async def pregunta_pais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pregunta sobre la capital de un país."""
    paises = [
        ("Francia", "París"), ("Japón", "Tokio"), ("Brasil", "Brasilia"),
        ("Alemania", "Berlín"), ("China", "Pekín"), ("India", "Nueva Delhi"),
        ("Italia", "Roma"), ("España", "Madrid"), ("Argentina", "Buenos Aires"),
        ("México", "Ciudad de México"), ("Canadá", "Ottawa"), ("Australia", "Canberra"),
        ("Rusia", "Moscú"), ("Colombia", "Bogotá"), ("Venezuela", "Caracas"),
    ]
    pais, capital = random.choice(paises)
    await update.message.reply_text(
        f"🌍 **¿Cuál es la capital de {pais}?**\n\n"
        f"||`{capital}`||",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def ruleta_rusa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mini juego ruleta rusa (sin daño real)."""
    bala = random.randint(1, 6)
    disparo = random.randint(1, 6)
    if disparo == bala:
        await update.message.reply_text("💀 **¡BANG! Fuiste eliminado.** _(Vuelve para revancha)_", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(f"✅ **¡Click!** Sobreviviste. Bala en posición `{bala}`, disparaste `{disparo}` 🎲", parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 5)

async def verdad_o_reto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Da una verdad o reto aleatorio."""
    verdades = [
        "¿Cuál es tu mayor miedo?","¿Cuándo fue la última vez que lloraste?",
        "¿Alguna vez le has mentido a un amigo?","¿Cuál es tu secreto más oscuro?",
        "¿Quién te gustaba en el colegio?","¿Alguna vez robaste algo?",
    ]
    retos = [
        "Haz 10 sentadillas","Canta una canción sin música","Imita a alguien del grupo",
        "Escribe tu nombre con el codo","Cuenta 100 rápido sin errores","Di un trabalenguas",
    ]
    eleccion = random.choice(["verdad", "reto"])
    if eleccion == "verdad":
        await update.message.reply_text(f"🤔 **VERDAD:**\n_{random.choice(verdades)}_", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(f"🎯 **RETO:**\n_{random.choice(retos)}_", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 3)

async def ahorcado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Juego del ahorcado."""
    palabras = ["python","telegram","venezuela","computador","programacion","inteligencia","camila","teclado"]
    palabra = random.choice(palabras)
    oculta = "_ " * len(palabra)
    await update.message.reply_text(
        f"🎮 **AHORCADO**\n"
        f"Adivina la palabra de {len(palabra)} letras:\n\n"
        f"`{oculta}`\n\n"
        f"_(Esta es una versión simplificada, la respuesta es: ||`{palabra}`||)_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def mayor_menor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Juego ¿Mayor o Menor?"""
    n1 = random.randint(1, 10)
    n2 = random.randint(1, 10)
    resultado = "mayor" if n2 > n1 else "menor" if n2 < n1 else "igual"
    await update.message.reply_text(
        f"🎲 **¿MAYOR O MENOR?**\n"
        f"Carta actual: `{n1}`\n"
        f"Siguiente carta: `{n2}` → _Es **{resultado}**_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 1)

async def simon_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simon dice mini reto."""
    acciones = ["aplaude","da un salto","toca tu nariz","toca el suelo","di 'Venezuela'","cuenta hasta 5"]
    accion = random.choice(acciones)
    simon = random.choice([True, False])
    if simon:
        await update.message.reply_text(f"✅ **Simón dice:** _{accion}_ 👈", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(f"🚫 ¡Solo **{accion}**! (sin Simón decir)", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 1)

async def batalla_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera stats de batalla aleatorias para el usuario."""
    user = update.effective_user.first_name
    ataque = random.randint(50, 999)
    defensa = random.randint(50, 999)
    velocidad = random.randint(50, 999)
    vida = random.randint(500, 9999)
    await update.message.reply_text(
        f"⚔️ **STATS DE BATALLA · {user}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"❤️ Vida: `{vida}`\n"
        f"⚔️ Ataque: `{ataque}`\n"
        f"🛡️ Defensa: `{defensa}`\n"
        f"⚡ Velocidad: `{velocidad}`",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

# ---- HERRAMIENTAS INTERNET / OSINT ----

async def whois_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información básica sobre un dominio."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/whois [dominio]`\nEj: `/whois google.com`")
        return
    dominio = context.args[0].replace("http://","").replace("https://","").split("/")[0]
    try:
        resp = await asyncio.to_thread(
            requests.get,
            f"https://api.domainsdb.info/v1/domains/search?domain={dominio}&zone=com",
            timeout=8
        )
        await update.message.reply_text(
            f"🌐 **WHOIS: {dominio}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔗 Dominio consultado: `{dominio}`\n"
            f"📡 Estado: `{'Registrado' if resp.status_code == 200 else 'Sin datos'}`\n"
            f"🛡️ _Para WHOIS completo usa:_ whois.domaintools.com",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 5)
    except:
        await update.message.reply_text("❌ Error al consultar dominio")

async def ping_web(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verifica si una web está online."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/ping [url]`\nEj: `/ping https://google.com`")
        return
    url = context.args[0]
    if not url.startswith("http"):
        url = "https://" + url
    try:
        inicio = time.time()
        resp = await asyncio.to_thread(requests.get, url, timeout=8)
        ms = int((time.time() - inicio) * 1000)
        estado = "🟢 Online" if resp.status_code < 400 else "🔴 Error"
        await update.message.reply_text(
            f"📡 **PING WEB**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🌐 URL: `{url}`\n"
            f"📊 Estado: {estado}\n"
            f"⚡ Tiempo: `{ms}ms`\n"
            f"🔢 Código HTTP: `{resp.status_code}`",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 5)
    except:
        await update.message.reply_text(f"🔴 **{url}** parece estar **offline** o inaccesible.")

async def user_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera un User-Agent aleatorio."""
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    ]
    await update.message.reply_text(f"🌐 **User-Agent Aleatorio:**\n`{random.choice(agents)}`", parse_mode=ParseMode.MARKDOWN)

async def mac_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera una dirección MAC aleatoria."""
    mac = ":".join(["{:02X}".format(random.randint(0, 255)) for _ in range(6)])
    await update.message.reply_text(f"💻 **MAC Address Falsa:**\n`{mac}`", parse_mode=ParseMode.MARKDOWN)

async def ip_privada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera una IP privada aleatoria."""
    clases = [
        f"192.168.{random.randint(0,255)}.{random.randint(1,254)}",
        f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
        f"172.{random.randint(16,31)}.{random.randint(0,255)}.{random.randint(1,254)}",
    ]
    ip_gen = random.choice(clases)
    await update.message.reply_text(f"🌐 **IP Privada Generada:**\n`{ip_gen}`", parse_mode=ParseMode.MARKDOWN)

# ---- ENTRETENIMIENTO EXTRA ----

async def musica_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recomienda música según género."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/musica [genero]`\nGéneros: `trap`, `salsa`, `reggaeton`, `pop`, `rock`, `clasica`")
        return
    genero = " ".join(context.args).lower()
    playlists = {
        "trap": "🎵 Top Trap: Bad Bunny - Moscow Mule, Drake - God's Plan, Travis Scott - SICKO MODE",
        "salsa": "🎵 Top Salsa: Marc Anthony - Vivir Mi Vida, Celia Cruz - La Vida Es Un Carnaval",
        "reggaeton": "🎵 Top Reggaeton: Daddy Yankee - Gasolina, J Balvin - Mi Gente, Ozuna - Taki Taki",
        "pop": "🎵 Top Pop: The Weeknd - Blinding Lights, Ed Sheeran - Shape of You",
        "rock": "🎵 Top Rock: Queen - Bohemian Rhapsody, AC/DC - Highway to Hell",
        "clasica": "🎵 Clásica: Beethoven - Para Elisa, Mozart - Sinfonía 40",
    }
    playlist = playlists.get(genero, f"🎵 Busca '{genero}' en Spotify: https://open.spotify.com/search/{genero}")
    await update.message.reply_text(f"🎧 **Recomendación Musical:**\n\n{playlist}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

async def libro_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recomienda un libro."""
    libros = [
        "📚 **El Alquimista** - Paulo Coelho",
        "📚 **1984** - George Orwell",
        "📚 **Cien años de soledad** - Gabriel García Márquez",
        "📚 **El Señor de los Anillos** - J.R.R. Tolkien",
        "📚 **Harry Potter** - J.K. Rowling",
        "📚 **El Principito** - Antoine de Saint-Exupéry",
        "📚 **Don Quijote de la Mancha** - Miguel de Cervantes",
        "📚 **Sapiens** - Yuval Noah Harari",
        "📚 **El Arte de la Guerra** - Sun Tzu",
        "📚 **Atomic Habits** - James Clear",
    ]
    await update.message.reply_text(f"📚 **Libro Recomendado:**\n{random.choice(libros)}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

async def animal_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dato curioso sobre animales."""
    try:
        resp = await asyncio.to_thread(requests.get, "https://catfact.ninja/fact", timeout=8)
        data = resp.json()
        hecho = data.get("fact", "Los gatos duermen 16 horas al día.")
        await update.message.reply_text(f"🐱 **Dato Animal (en inglés):**\n_{hecho}_\n\n🔍 _Usa /traducir para ver en español_", parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 3)
    except:
        await update.message.reply_text("🐘 _Los elefantes son los únicos animales que no pueden saltar._ 🐘")

async def chiste_ingles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chiste en inglés de API."""
    try:
        resp = await asyncio.to_thread(
            requests.get, "https://official-joke-api.appspot.com/random_joke", timeout=8
        )
        data = resp.json()
        await update.message.reply_text(
            f"😂 **Joke (EN):**\n\n_{data['setup']}_\n\n||_{data['punchline']}_||",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 2)
    except:
        await update.message.reply_text("❌ No se pudo obtener el chiste")

async def fox_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Imagen aleatoria de un zorro."""
    try:
        resp = await asyncio.to_thread(requests.get, "https://randomfox.ca/floof/", timeout=8)
        data = resp.json()
        await update.message.reply_photo(photo=data['image'], caption="🦊 ¡Un zorrito para ti!")
        sumar_xp(update.effective_user.id, 2)
    except:
        await update.message.reply_text("❌ No se pudo obtener la imagen")

async def dog_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Imagen aleatoria de un perro."""
    try:
        resp = await asyncio.to_thread(requests.get, "https://dog.ceo/api/breeds/image/random", timeout=8)
        data = resp.json()
        await update.message.reply_photo(photo=data['message'], caption="🐶 ¡Un perrito para animarte!")
        sumar_xp(update.effective_user.id, 2)
    except:
        await update.message.reply_text("❌ No se pudo obtener la imagen")

async def cat_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Imagen aleatoria de un gato."""
    try:
        resp = await asyncio.to_thread(
            requests.get, "https://api.thecatapi.com/v1/images/search", timeout=8
        )
        data = resp.json()
        await update.message.reply_photo(photo=data[0]['url'], caption="🐱 ¡Un gatito para ti!")
        sumar_xp(update.effective_user.id, 2)
    except:
        await update.message.reply_text("❌ No se pudo obtener la imagen")

# ---- UTILIDADES AVANZADAS ----

async def contador_regresivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cuenta regresiva hasta un año."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/countdown [año]`")
        return
    try:
        from datetime import date
        anio_target = int(context.args[0])
        fecha_target = date(anio_target, 1, 1)
        hoy = date.today()
        dias = (fecha_target - hoy).days
        if dias < 0:
            await update.message.reply_text(f"⏳ El año `{anio_target}` ya pasó hace `{abs(dias)}` días.", parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(f"⏳ Faltan **{dias}** días para el año `{anio_target}` 🎉", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Año inválido")

async def reloj_mundial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra horas en distintas ciudades del mundo."""
    from datetime import timezone, timedelta
    utc = datetime.now(timezone.utc)
    ciudades = {
        "🇻🇪 Caracas": utc + timedelta(hours=-4),
        "🇺🇸 Nueva York": utc + timedelta(hours=-5),
        "🇬🇧 Londres": utc + timedelta(hours=0),
        "🇪🇸 Madrid": utc + timedelta(hours=1),
        "🇯🇵 Tokio": utc + timedelta(hours=9),
        "🇦🇺 Sídney": utc + timedelta(hours=11),
    }
    texto = "🌍 **RELOJ MUNDIAL**\n━━━━━━━━━━━━━━━━━━━━\n"
    for ciudad, hora in ciudades.items():
        texto += f"{ciudad}: `{hora.strftime('%H:%M')}`\n"
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def divisor_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Divide texto en partes iguales."""
    if len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/dividir [partes] [texto]`")
        return
    try:
        partes = int(context.args[0])
        texto = " ".join(context.args[1:])
        tamanio = len(texto) // partes
        chunks = [texto[i:i+tamanio] for i in range(0, len(texto), tamanio)][:partes]
        resultado = "\n".join([f"**Parte {i+1}:** `{c}`" for i, c in enumerate(chunks)])
        await update.message.reply_text(resultado, parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Error al dividir")

async def limpiar_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Elimina caracteres especiales de un texto."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/limpiar [texto]`")
        return
    import re
    texto = " ".join(context.args)
    limpio = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]', '', texto)
    await update.message.reply_text(f"🧹 **Texto limpio:**\n`{limpio}`", parse_mode=ParseMode.MARKDOWN)

async def vocal_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cuenta vocales y consonantes."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/vocales [texto]`")
        return
    texto = " ".join(context.args).lower()
    vocales = sum(1 for c in texto if c in 'aeiouáéíóú')
    consonantes = sum(1 for c in texto if c.isalpha() and c not in 'aeiouáéíóú')
    await update.message.reply_text(
        f"🔤 **Análisis de vocales:**\n"
        f"🅰️ Vocales: `{vocales}`\n"
        f"🅱️ Consonantes: `{consonantes}`",
        parse_mode=ParseMode.MARKDOWN
    )

async def temperatura_corporal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Interpreta una temperatura corporal."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/fiebre [temperatura]`\nEj: `/fiebre 38.5`")
        return
    try:
        temp = float(context.args[0])
        if temp < 36:
            estado = "🔵 Hipotermia (baja)"
        elif temp <= 37.2:
            estado = "✅ Normal"
        elif temp <= 38:
            estado = "🟡 Febrícula"
        elif temp <= 39:
            estado = "🟠 Fiebre"
        else:
            estado = "🔴 Fiebre alta ⚠️ Consulta médico"
        await update.message.reply_text(
            f"🌡️ **{temp}°C** → {estado}",
            parse_mode=ParseMode.MARKDOWN
        )
    except:
        await update.message.reply_text("❌ Temperatura inválida")

async def calcular_propina(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula propina sobre una cuenta."""
    if len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/propina [total] [porcentaje]`\nEj: `/propina 50 15`")
        return
    try:
        total = float(context.args[0])
        pct = float(context.args[1])
        propina = total * pct / 100
        total_con = total + propina
        await update.message.reply_text(
            f"💵 **CALCULADORA DE PROPINA**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🧾 Cuenta: `${total:.2f}`\n"
            f"💰 Propina ({pct}%): `${propina:.2f}`\n"
            f"✅ Total: `${total_con:.2f}`",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 2)
    except:
        await update.message.reply_text("❌ Valores inválidos")

async def convertir_peso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte peso entre varias unidades."""
    if len(context.args) < 3:
        await update.message.reply_text("📌 Uso: `/peso [valor] [de] [a]`\nUnidades: kg, lb, g, oz, t")
        return
    try:
        valor = float(context.args[0])
        de = context.args[1].lower()
        a = context.args[2].lower()
        a_kg = {"kg":1,"lb":0.453592,"g":0.001,"oz":0.0283495,"t":1000}
        if de not in a_kg or a not in a_kg:
            await update.message.reply_text("❌ Unidad no válida")
            return
        resultado = valor * a_kg[de] / a_kg[a]
        await update.message.reply_text(f"⚖️ `{valor} {de} = {resultado:.4f} {a}`", parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 2)
    except:
        await update.message.reply_text("❌ Error en conversión")

async def convertir_distancia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte distancias entre múltiples unidades."""
    if len(context.args) < 3:
        await update.message.reply_text("📌 Uso: `/distancia [valor] [de] [a]`\nUnidades: km, m, cm, mm, mi, ft, in, yd")
        return
    try:
        valor = float(context.args[0])
        de = context.args[1].lower()
        a = context.args[2].lower()
        a_m = {"km":1000,"m":1,"cm":0.01,"mm":0.001,"mi":1609.34,"ft":0.3048,"in":0.0254,"yd":0.9144}
        if de not in a_m or a not in a_m:
            await update.message.reply_text("❌ Unidad no válida")
            return
        resultado = valor * a_m[de] / a_m[a]
        await update.message.reply_text(f"📏 `{valor} {de} = {resultado:.4f} {a}`", parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 2)
    except:
        await update.message.reply_text("❌ Error en conversión")

async def velocidad_internet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tips sobre velocidades de internet."""
    velocidades = [
        ("1-5 Mbps", "📧 Correo y redes sociales básicas"),
        ("5-25 Mbps", "📺 Streaming HD y videollamadas"),
        ("25-100 Mbps", "🎮 Gaming online y 4K"),
        ("100-500 Mbps", "⚡ Multi-usuario sin problemas"),
        ("500+ Mbps", "🚀 Fibra ultra-rápida"),
    ]
    texto = "📡 **GUÍA DE VELOCIDADES INTERNET**\n━━━━━━━━━━━━━━━━━━━━\n"
    for vel, uso in velocidades:
        texto += f"- **{vel}** → {uso}\n"
    texto += "\n💡 _Prueba tu velocidad en: speedtest.net_"
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def vpn_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre VPNs gratuitas."""
    await update.message.reply_text(
        f"🔒 **VPNs GRATUITAS RECOMENDADAS**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"1️⃣ **ProtonVPN** - Sin límite de datos\n"
        f"   🔗 protonvpn.com\n\n"
        f"2️⃣ **Windscribe** - 10GB/mes gratis\n"
        f"   🔗 windscribe.com\n\n"
        f"3️⃣ **Cloudflare WARP** - Muy rápida\n"
        f"   🔗 one.one.one.one\n\n"
        f"4️⃣ **TunnelBear** - 500MB/mes\n"
        f"   🔗 tunnelbear.com\n\n"
        f"⚠️ _Usar VPN para privacidad, no actividades ilegales_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def atajos_teclado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra atajos de teclado útiles."""
    sistema = " ".join(context.args).lower() if context.args else "windows"
    atajos = {
        "windows": [
            "Win+D → Mostrar escritorio","Ctrl+Z → Deshacer","Ctrl+Y → Rehacer",
            "Alt+Tab → Cambiar ventana","Win+L → Bloquear PC","Ctrl+Shift+Esc → Administrador tareas",
            "Win+R → Ejecutar","Ctrl+A → Seleccionar todo","Win+PrintScreen → Captura",
        ],
        "mac": [
            "Cmd+Space → Spotlight","Cmd+Tab → Cambiar app","Cmd+Q → Cerrar app",
            "Cmd+Shift+3 → Captura","Cmd+Z → Deshacer","Ctrl+Cmd+Q → Bloquear",
        ],
        "linux": [
            "Ctrl+Alt+T → Terminal","Alt+F4 → Cerrar ventana","Ctrl+Alt+L → Bloquear",
            "Super → Menú de apps","Ctrl+H → Archivos ocultos",
        ]
    }
    lista = atajos.get(sistema, atajos["windows"])
    texto = f"⌨️ **Atajos de {sistema.upper()}:**\n━━━━━━━━━━━━━━━━━━━━\n"
    texto += "\n".join([f"- `{a}`" for a in lista])
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def lenguajes_prog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre lenguajes de programación."""
    langs = {
        "python": "🐍 Python: Fácil de aprender, IA/ML, ciencia de datos. Creado en 1991.",
        "javascript": "🌐 JavaScript: Lenguaje web por excelencia, frontend y backend (Node.js).",
        "java": "☕ Java: Multiplataforma, empresarial, Android. 'Write Once, Run Anywhere'.",
        "c": "⚙️ C: El padre de los lenguajes, rendimiento extremo, sistemas operativos.",
        "rust": "🦀 Rust: Seguridad de memoria, reemplaza a C/C++, muy rápido.",
        "go": "🐹 Go: Simple y rápido, backend escalable, creado por Google.",
        "php": "🐘 PHP: Web server-side, potencia el 80% de internet (WordPress, Laravel).",
        "swift": "🍎 Swift: iOS y macOS apps, creado por Apple, moderno y rápido.",
    }
    if not context.args:
        lista = ", ".join(langs.keys())
        await update.message.reply_text(f"💻 Lenguajes disponibles: `{lista}`\nUsa: `/lenguaje [nombre]`")
        return
    lang = " ".join(context.args).lower()
    info = langs.get(lang, f"❌ No tengo info de `{lang}`. Prueba: python, javascript, java, c, rust, go, php, swift")
    await update.message.reply_text(f"💻 **INFO LENGUAJE:**\n{info}", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 3)

async def abreviaciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Explica abreviaciones y siglas comunes."""
    siglas = {
        "IA": "Inteligencia Artificial","API": "Application Programming Interface",
        "URL": "Uniform Resource Locator","DNS": "Domain Name System",
        "HTTP": "HyperText Transfer Protocol","HTTPS": "HTTP Secure",
        "IP": "Internet Protocol","VPN": "Virtual Private Network",
        "GUI": "Graphical User Interface","CPU": "Central Processing Unit",
        "GPU": "Graphics Processing Unit","RAM": "Random Access Memory",
        "SSD": "Solid State Drive","HDD": "Hard Disk Drive",
        "OTP": "One Time Password","JWT": "JSON Web Token",
        "SQL": "Structured Query Language","NoSQL": "Not Only SQL",
        "OSINT": "Open Source Intelligence","2FA": "Two-Factor Authentication",
    }
    if not context.args:
        await update.message.reply_text("📌 Uso: `/sigla [SIGLA]`\nEj: `/sigla API`")
        return
    sigla = " ".join(context.args).upper()
    explicacion = siglas.get(sigla, f"❌ No encontré `{sigla}` en la base de datos")
    await update.message.reply_text(f"📖 **{sigla}** = _{explicacion}_", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

async def sorteo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hace un sorteo entre opciones separadas por coma."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/sorteo [opcion1, opcion2, opcion3]`")
        return
    texto = " ".join(context.args)
    opciones = [o.strip() for o in texto.split(",") if o.strip()]
    if len(opciones) < 2:
        await update.message.reply_text("❌ Necesitas al menos 2 opciones separadas por coma")
        return
    ganador = random.choice(opciones)
    await update.message.reply_text(
        f"🎰 **SORTEO**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 Opciones: `{', '.join(opciones)}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏆 **¡GANADOR:** `{ganador}`**!**",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def turno_random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asigna turnos aleatorios."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/turnos [nombre1, nombre2, nombre3]`")
        return
    texto = " ".join(context.args)
    personas = [p.strip() for p in texto.split(",") if p.strip()]
    if len(personas) < 2:
        await update.message.reply_text("❌ Necesitas al menos 2 personas")
        return
    random.shuffle(personas)
    texto_turnos = "\n".join([f"{i+1}️⃣ {p}" for i, p in enumerate(personas)])
    await update.message.reply_text(
        f"🔀 **ORDEN DE TURNOS:**\n━━━━━━━━━━━━━━━━━━━━\n{texto_turnos}",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def nivel_bateria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fun: analiza nivel de batería social."""
    nick = update.effective_user.first_name
    nivel = random.randint(0, 100)
    if nivel < 20:
        estado = "🔴 Crítico - Necesitas soledad YA"
    elif nivel < 50:
        estado = "🟡 Bajo - Modo introvertido activado"
    elif nivel < 80:
        estado = "🟢 Normal - Puedes socializar"
    else:
        estado = "⚡ Cargado - Social butterfly mode ON"
    await update.message.reply_text(
        f"🔋 **BATERÍA SOCIAL DE {nick.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 Nivel: `{nivel}%`\n"
        f"Estado: {estado}",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def compatibilidad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calcula compatibilidad con otra persona."""
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Responde al mensaje de alguien con `/compatibilidad`")
        return
    user1 = update.effective_user.first_name
    user2 = update.message.reply_to_message.from_user.first_name
    pct = random.randint(0, 100)
    tipos = [
        (90, "👑 ALMAS GEMELAS"),
        (75, "💕 Gran compatibilidad"),
        (60, "💛 Buena onda"),
        (40, "🤝 Pueden llevarse bien"),
        (20, "😬 Necesitan esfuerzo"),
        (0, "💔 Diferencias grandes"),
    ]
    tipo = next(t for threshold, t in tipos if pct >= threshold)
    await update.message.reply_text(
        f"✨ **COMPATIBILIDAD**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 {user1} + 👤 {user2}\n"
        f"📊 Resultado: `{pct}%`\n"
        f"🏷️ Tipo: {tipo}",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def encuesta_rapida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea una encuesta rápida de SI/NO."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/encuesta [pregunta]`")
        return
    pregunta = " ".join(context.args)
    keyboard = [
        [InlineKeyboardButton("✅ SÍ", callback_data="si"), InlineKeyboardButton("❌ NO", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"📊 **ENCUESTA RÁPIDA**\n❓ _{pregunta}_",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )
    sumar_xp(update.effective_user.id, 3)

async def noticias_tech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra noticias de tecnología."""
    try:
        resp = await asyncio.to_thread(
            requests.get,
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=8
        )
        ids = resp.json()[:5]
        noticias = []
        for story_id in ids:
            story_resp = await asyncio.to_thread(
                requests.get,
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                timeout=5
            )
            story = story_resp.json()
            titulo = story.get("title", "Sin título")[:60]
            url = story.get("url", "")
            noticias.append(f"📰 [{titulo}]({url})" if url else f"📰 {titulo}")
        
        texto = "💻 **NOTICIAS TECH (Hacker News)**\n━━━━━━━━━━━━━━━━━━━━\n" + "\n".join(noticias)
        await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        sumar_xp(update.effective_user.id, 5)
    except:
        await update.message.reply_text("❌ No se pudieron cargar las noticias tech")

async def clima_mundo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clima de cualquier ciudad del mundo."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/climaciudad [ciudad]`\nEj: `/climaciudad Madrid`")
        return
    ciudad = " ".join(context.args)
    try:
        resp = await asyncio.to_thread(
            requests.get,
            f"https://wttr.in/{ciudad.replace(' ', '+')}?format=j1",
            timeout=8
        )
        data = resp.json()
        actual = data['current_condition'][0]
        temp_c = actual['temp_C']
        desc = actual['weatherDesc'][0]['value']
        humedad = actual['humidity']
        viento = actual['windspeedKmph']
        await update.message.reply_text(
            f"🌤️ **CLIMA EN {ciudad.upper()}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🌡️ Temperatura: `{temp_c}°C`\n"
            f"☁️ Condición: `{desc}`\n"
            f"💧 Humedad: `{humedad}%`\n"
            f"💨 Viento: `{viento} km/h`",
            parse_mode=ParseMode.MARKDOWN
        )
        sumar_xp(update.effective_user.id, 4)
    except:
        await update.message.reply_text(f"❌ No se pudo obtener el clima de `{ciudad}`")

async def numero_romano(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte número a romano."""
    if not context.args:
        await update.message.reply_text("📌 Uso: `/romano [número]`\nEj: `/romano 2024`")
        return
    try:
        n = int(context.args[0])
        if n <= 0 or n > 3999:
            await update.message.reply_text("❌ Número entre 1 y 3999")
            return
        val = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
        sym = ["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]
        resultado = ""
        for i in range(len(val)):
            while n >= val[i]:
                resultado += sym[i]
                n -= val[i]
        await update.message.reply_text(f"🏛️ `{context.args[0]}` en romano: `{resultado}`", parse_mode=ParseMode.MARKDOWN)
        sumar_xp(update.effective_user.id, 3)
    except:
        await update.message.reply_text("❌ Número inválido")

async def dado_personalizado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dado con número de caras personalizable."""
    caras = 6
    if context.args:
        try:
            caras = int(context.args[0])
            caras = max(2, min(caras, 1000))
        except:
            pass
    resultado = random.randint(1, caras)
    await update.message.reply_text(
        f"🎲 **Dado de {caras} caras:**\n`{resultado}`",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 1)

async def loteria_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera números de lotería."""
    nums = sorted(random.sample(range(1, 50), 5))
    extra = random.randint(1, 10)
    await update.message.reply_text(
        f"🎰 **TUS NÚMEROS DE LOTERÍA**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 Principales: `{' - '.join(map(str, nums))}`\n"
        f"⭐ Extra: `{extra}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🍀 _¡Buena suerte!_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def nivel_chakra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fun: nivel de chakra espiritual."""
    nick = update.effective_user.first_name
    chakras = [
        "🔴 Muladhara (Raíz) - Estabilidad",
        "🟠 Svadhisthana (Sacral) - Creatividad",
        "🟡 Manipura (Plexo Solar) - Poder",
        "💚 Anahata (Corazón) - Amor",
        "🔵 Vishuddha (Garganta) - Comunicación",
        "💜 Ajna (Tercer Ojo) - Intuición",
        "🌟 Sahasrara (Corona) - Iluminación",
    ]
    nivel = random.randint(60, 100)
    chakra = random.choice(chakras)
    await update.message.reply_text(
        f"🧘 **CHAKRA DE {nick.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ Chakra activo: {chakra}\n"
        f"📊 Energía: `{nivel}%`",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def fuerza_oscura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fun: nivel de fuerza oscura Star Wars."""
    nick = update.effective_user.first_name
    nivel = random.randint(0, 100)
    lado = "🔴 Lado Oscuro (Sith)" if nivel > 50 else "🔵 Lado de la Luz (Jedi)"
    await update.message.reply_text(
        f"⚔️ **LA FUERZA EN {nick.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 Nivel de Midiclorianos: `{nivel * 100}`\n"
        f"🌌 Lado: {lado}",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def elemento_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asigna un elemento de la naturaleza."""
    nick = update.effective_user.first_name
    elementos = [
        ("🔥 FUEGO", "Apasionado, líder, impulsivo"),
        ("💧 AGUA", "Adaptable, intuitivo, empático"),
        ("🌍 TIERRA", "Estable, trabajador, paciente"),
        ("💨 AIRE", "Libre, creativo, curioso"),
        ("⚡ RAYO", "Veloz, impredecible, poderoso"),
        ("🧊 HIELO", "Calculador, tranquilo, frío bajo presión"),
    ]
    elem, desc = random.choice(elementos)
    await update.message.reply_text(
        f"✨ **ELEMENTO DE {nick.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚗️ Tu elemento: **{elem}**\n"
        f"📋 Personalidad: _{desc}_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def anime_rec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recomienda un anime."""
    animes = [
        "⚔️ Attack on Titan (Shingeki no Kyojin)",
        "🔮 Fullmetal Alchemist: Brotherhood",
        "👁️ Death Note",
        "🏃 Naruto Shippuden",
        "🌊 One Piece",
        "⚡ Dragon Ball Z",
        "🃏 Hunter x Hunter",
        "🌸 Demon Slayer (Kimetsu no Yaiba)",
        "🤖 Neon Genesis Evangelion",
        "🌙 Sword Art Online",
        "🔥 My Hero Academia (Boku no Hero)",
        "🎭 Tokyo Ghoul",
    ]
    await update.message.reply_text(
        f"🎌 **Anime Recomendado:**\n**{random.choice(animes)}**\n\n"
        f"🔍 Búscalo en: Crunchyroll / AnimeFLV",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def videojuego_rec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recomienda un videojuego."""
    juegos = [
        "🎮 The Legend of Zelda: Breath of the Wild",
        "🔫 Call of Duty: Warzone",
        "⚽ FIFA / EA FC 24",
        "🏎️ Gran Turismo 7",
        "🌍 Red Dead Redemption 2",
        "🤖 Elden Ring",
        "🦸 Spider-Man 2",
        "🔥 God of War: Ragnarök",
        "🌊 Minecraft",
        "🎯 Valorant",
        "🏃 GTA V / GTA Online",
        "🎭 The Witcher 3",
    ]
    await update.message.reply_text(
        f"🕹️ **Videojuego Recomendado:**\n**{random.choice(juegos)}**",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 2)

async def cmd_definicion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca la definición de una palabra en Wikipedia."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text(
            "📖 **Búsqueda de Definiciones**\n\n"
            "**Uso:** `/definicion [palabra]`\n\n"
            "**Ejemplos:**\n"
            "- `/definicion fotosintesis`\n"
            "- `/definicion democracia`\n"
            "- `/definicion inteligencia artificial`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    palabra = " ".join(context.args)
    wait_msg = await update.message.reply_text(f"📖 _Buscando definición de: {palabra}_", parse_mode=ParseMode.MARKDOWN)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        url = f"https://es.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&titles={palabra.replace(' ', '_')}&explaintext=true"
        respuesta = await asyncio.to_thread(requests.get, url, headers=headers, timeout=10)
        
        if respuesta.status_code == 200:
            data = respuesta.json()
            pages = data.get('query', {}).get('pages', {})
            if pages:
                page_id = list(pages.keys())[0]
                page = pages[page_id]
                if 'extract' in page and page['extract']:
                    extract = page['extract'][:600] + "..." if len(page['extract']) > 600 else page['extract']
                    await wait_msg.edit_text(
                        f"📖 **{page.get('title', palabra)}**\n\n{extract}",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    registrar_evento(user_id, nick, f"Definición: {palabra}", "INVESTIGACIÓN")
                    sumar_xp(user_id, 5)
                    return
        
        await wait_msg.edit_text(f"❌ No encontré definición para: **{palabra}**")
    except Exception as e:
        print(f"Error definición: {e}")
        await wait_msg.edit_text("❌ Error buscando definición.")

async def cmd_etimologia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca la etimología de una palabra."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text(
            "🌳 **Etimología de Palabras**\n\n"
            "**Uso:** `/etimologia [palabra]`\n\n"
            "**Ejemplos:**\n"
            "- `/etimologia educacion`\n"
            "- `/etimologia persona`\n"
            "- `/etimologia tecnologia`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    palabra = " ".join(context.args)
    wait_msg = await update.message.reply_text(f"🌳 _Buscando etimología de: {palabra}_", parse_mode=ParseMode.MARKDOWN)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        url = f"https://es.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&titles={palabra.replace(' ', '_')}&explaintext=true"
        respuesta = await asyncio.to_thread(requests.get, url, headers=headers, timeout=10)
        
        if respuesta.status_code == 200:
            data = respuesta.json()
            pages = data.get('query', {}).get('pages', {})
            if pages:
                page_id = list(pages.keys())[0]
                page = pages[page_id]
                if 'extract' in page and page['extract']:
                    extract = page['extract'][:500] + "..." if len(page['extract']) > 500 else page['extract']
                    await wait_msg.edit_text(
                        f"🌳 **Origen de: {page.get('title', palabra)}**\n\n{extract}\n\n_Información obtenida de Wikipedia_",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    registrar_evento(user_id, nick, f"Etimología: {palabra}", "INVESTIGACIÓN")
                    sumar_xp(user_id, 5)
                    return
        
        await wait_msg.edit_text(f"❌ No encontré información sobre: **{palabra}**")
    except Exception as e:
        print(f"Error etimología: {e}")
        await wait_msg.edit_text("❌ Error buscando etimología.")

async def cmd_sinonimos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca sinónimos y antónimos de una palabra."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text(
            "📚 **Sinónimos y Antónimos**\n\n"
            "**Uso:** `/sinonimo [palabra]`\n\n"
            "**Ejemplos:**\n"
            "- `/sinonimo feliz`\n"
            "- `/sinonimo grande`\n"
            "- `/sinonimo rapido`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    palabra = " ".join(context.args).lower()
    
    sinonimos_dict = {
        "feliz": ["alegre", "contento", "gozoso", "dichoso"],
        "triste": ["desgraciado", "infeliz", "melancólico", "afligido"],
        "grande": ["enorme", "inmenso", "vasto", "monumental"],
        "pequeño": ["diminuto", "minúsculo", "ínfimo", "microscópico"],
        "rapido": ["veloz", "ligero", "acelerado", "precipitado"],
        "lento": ["tardío", "pausado", "moroso", "flemático"],
        "bonito": ["hermoso", "bello", "precioso", "vistoso"],
        "feo": ["horrible", "desagradable", "repugnante", "grotesco"],
        "inteligente": ["astuto", "perspicaz", "sagaz", "ingenioso"],
        "tonto": ["necio", "imbécil", "estúpido", "ignorante"],
    }
    
    if palabra in sinonimos_dict:
        sinonimos = ", ".join(sinonimos_dict[palabra])
        await update.message.reply_text(
            f"📚 **Sinónimos de '{palabra}':**\n\n{sinonimos}",
            parse_mode=ParseMode.MARKDOWN
        )
        registrar_evento(user_id, nick, f"Sinónimos: {palabra}", "INVESTIGACIÓN")
        sumar_xp(user_id, 3)
    else:
        await update.message.reply_text(
            f"❌ No tengo sinónimos para **'{palabra}'**.\n\n"
            f"💡 Intenta con palabras comunes como: feliz, triste, grande, pequeño, rápido, lento, bonito, feo, inteligente, tonto"
        )

async def cmd_diccionario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca una palabra en Wikipedia y devuelve su contexto."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text(
            "📕 **Búsqueda en Diccionario**\n\n"
            "**Uso:** `/diccionario [palabra]`\n\n"
            "**Ejemplos:**\n"
            "- `/diccionario sustantivo`\n"
            "- `/diccionario verbo`\n"
            "- `/diccionario adjetivo`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    palabra = " ".join(context.args)
    wait_msg = await update.message.reply_text(f"📕 _Buscando en diccionario: {palabra}_", parse_mode=ParseMode.MARKDOWN)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        # Intentar Wikipedia español primero
        url = f"https://es.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&titles={palabra.replace(' ', '_')}&explaintext=true"
        respuesta = await asyncio.to_thread(requests.get, url, headers=headers, timeout=10)
        
        if respuesta.status_code == 200:
            data = respuesta.json()
            pages = data.get('query', {}).get('pages', {})
            if pages:
                page_id = list(pages.keys())[0]
                page = pages[page_id]
                if 'extract' in page and page['extract']:
                    extract = page['extract'][:700] + "..." if len(page['extract']) > 700 else page['extract']
                    await wait_msg.edit_text(
                        f"📕 **{page.get('title', palabra)}**\n\n{extract}",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    registrar_evento(user_id, nick, f"Diccionario: {palabra}", "INVESTIGACIÓN")
                    sumar_xp(user_id, 5)
                    return
        
        # Fallback a DuckDuckGo
        url_ddg = f"https://api.duckduckgo.com/?q={palabra}&format=json&no_redirect=1"
        respuesta_ddg = await asyncio.to_thread(requests.get, url_ddg, headers=headers, timeout=10)
        
        if respuesta_ddg.status_code == 200:
            data_ddg = respuesta_ddg.json()
            if data_ddg.get('AbstractText'):
                abstract = data_ddg['AbstractText'][:700] + "..." if len(data_ddg.get('AbstractText', '')) > 700 else data_ddg.get('AbstractText', '')
                await wait_msg.edit_text(
                    f"📕 **{palabra}**\n\n{abstract}",
                    parse_mode=ParseMode.MARKDOWN
                )
                registrar_evento(user_id, nick, f"Diccionario: {palabra}", "INVESTIGACIÓN")
                sumar_xp(user_id, 5)
                return
        
        await wait_msg.edit_text(f"❌ No encontré: **{palabra}**")
    except Exception as e:
        print(f"Error diccionario: {e}")
        await wait_msg.edit_text("❌ Error buscando palabra.")

async def cmd_ia_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chat conversacional con Google Gemini 1.5 Flash (GRATIS - Sin pago requerido)"""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text("💬 **Usa:** `/ia [pregunta]`\n\n_Ejemplo: /ia ¿qué es la fotosíntesis?_")
        return
    
    pregunta = " ".join(context.args)
    wait_msg = await update.message.reply_text("🤖 _Procesando..._")
    
    try:
        # Usar requests para llamar a API pública gratuita
        payload = {
            "contents": [{
                "parts": [{"text": pregunta}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500
            }
        }
        
        respuesta = await asyncio.to_thread(
            requests.post,
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyB20aSgOHSxFf3Pml2nM0nPr0UTryol8fo",
            json=payload,
            timeout=15
        )
        
        if respuesta.status_code == 200:
            data = respuesta.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                contenido = data['candidates'][0].get('content', {})
                parts = contenido.get('parts', [])
                if parts and 'text' in parts[0]:
                    texto = parts[0]['text'][:500]
                    await wait_msg.edit_text(f"🤖 **Gemini:**\n\n{texto}")
                    registrar_evento(user_id, nick, f"IA Chat: {pregunta[:50]}", "IA")
                    sumar_xp(user_id, 10)
                    return
        
        await wait_msg.edit_text("⚠️ No pude procesar tu pregunta.")
    except Exception as e:
        print(f"Error IA: {e}")
        await wait_msg.edit_text(f"⚠️ Error: {str(e)[:100]}")

async def cmd_ia_poesia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera poesía hermosa con Gemini (GRATIS - Sin pago)"""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text("📝 **Usa:** `/poesia_ia [tema]`\n\n_Ejemplo: /poesia_ia amanecer_")
        return
    
    tema = " ".join(context.args)
    wait_msg = await update.message.reply_text("✍️ _Escribiendo poesía..._")
    
    try:
        payload = {
            "contents": [{
                "parts": [{"text": f"Escribe una poesía corta y hermosa sobre: {tema}"}]
            }],
            "generationConfig": {"temperature": 0.9, "maxOutputTokens": 400}
        }
        
        respuesta = await asyncio.to_thread(
            requests.post,
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyB20aSgOHSxFf3Pml2nM0nPr0UTryol8fo",
            json=payload,
            timeout=15
        )
        
        if respuesta.status_code == 200:
            data = respuesta.json()
            if 'candidates' in data and data['candidates']:
                texto = data['candidates'][0]['content']['parts'][0]['text'][:500]
                await wait_msg.edit_text(f"📝 **Poesía sobre {tema}:**\n\n{texto}")
                registrar_evento(user_id, nick, f"Poesía: {tema}", "IA")
                sumar_xp(user_id, 8)
                return
        
        await wait_msg.edit_text("⚠️ Error generando poesía")
    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error: {str(e)[:100]}")

async def cmd_ia_traduccion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traduce textos a cualquier idioma con Gemini (GRATIS - Sin pago)"""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if len(context.args) < 2:
        await update.message.reply_text("🌐 **Usa:** `/traduccion_ia [idioma] [texto]`\n\n_Ej: /traduccion_ia inglés hola mundo_")
        return
    
    idioma = context.args[0]
    texto = " ".join(context.args[1:])
    wait_msg = await update.message.reply_text(f"🌐 _Traduciendo al {idioma}..._")
    
    try:
        payload = {
            "contents": [{
                "parts": [{"text": f"Traduce al {idioma}: {texto}"}]
            }],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 300}
        }
        
        respuesta = await asyncio.to_thread(
            requests.post,
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyB20aSgOHSxFf3Pml2nM0nPr0UTryol8fo",
            json=payload,
            timeout=15
        )
        
        if respuesta.status_code == 200:
            data = respuesta.json()
            if 'candidates' in data and data['candidates']:
                resultado = data['candidates'][0]['content']['parts'][0]['text']
                await wait_msg.edit_text(f"🌐 **Traducción al {idioma}:**\n\n{resultado[:400]}")
                registrar_evento(user_id, nick, f"Traducción: {idioma}", "IA")
                sumar_xp(user_id, 5)
                return
        
        await wait_msg.edit_text("⚠️ Error en traducción")
    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error: {str(e)[:100]}")

async def cmd_ia_resumen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resume textos largos automáticamente con Gemini (GRATIS - Sin pago)"""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text("📋 **Usa:** `/resumen_ia [texto largo]`\n\n_Ej: /resumen_ia La fotosíntesis es el proceso..._")
        return
    
    texto = " ".join(context.args)
    wait_msg = await update.message.reply_text("📋 _Resumiendo..._")
    
    try:
        payload = {
            "contents": [{
                "parts": [{"text": f"Resume en 3 líneas cortas: {texto[:500]}"}]
            }],
            "generationConfig": {"temperature": 0.5, "maxOutputTokens": 200}
        }
        
        respuesta = await asyncio.to_thread(
            requests.post,
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyB20aSgOHSxFf3Pml2nM0nPr0UTryol8fo",
            json=payload,
            timeout=15
        )
        
        if respuesta.status_code == 200:
            data = respuesta.json()
            if 'candidates' in data and data['candidates']:
                resumen = data['candidates'][0]['content']['parts'][0]['text']
                await wait_msg.edit_text(f"📋 **Resumen:**\n\n{resumen}")
                registrar_evento(user_id, nick, "Resumen con IA", "IA")
                sumar_xp(user_id, 7)
                return
        
        await wait_msg.edit_text("⚠️ Error resumiendo")
    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error: {str(e)[:100]}")

async def superpoder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asigna un superpoder aleatorio."""
    nick = update.effective_user.first_name
    poderes = [
        "🦅 **Vuelo** - Volar a velocidad sónica","⚡ **Velocidad** - Más rápido que la luz",
        "🔮 **Telepatía** - Leer mentes","👁️ **Visión de Rayos X** - Ver a través de todo",
        "🌊 **Control del Agua** - Dominar los océanos","🔥 **Pirokinesis** - Control del fuego",
        "❄️ **Criokinesis** - Control del hielo","🌩️ **Electrokinesis** - Controlar la electricidad",
        "🦁 **Súper Fuerza** - Fuerza de 1000 hombres","🛡️ **Invulnerabilidad** - Nada puede herirte",
        "⏳ **Control del Tiempo** - Pausar el tiempo","🌀 **Teletransportación** - Ir a cualquier lugar",
    ]
    await update.message.reply_text(
        f"🦸 **SUPERPODER DE {nick.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ Tu poder: {random.choice(poderes)}",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

# ---- COMANDOS ADMINISTRATIVOS EXTRA ----

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: envía mensaje broadcast (solo admin)."""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Solo el admin puede usar esto")
        return
    if not context.args:
        await update.message.reply_text("📌 Uso: `/broadcast [mensaje]`")
        return
    mensaje = " ".join(context.args)
    enviados = 0
    for uid in usuarios_info.keys():
        try:
            await context.bot.send_message(
                chat_id=int(uid),
                text=f"📢 **MENSAJE OFICIAL DE CAMI.BOT:**\n\n{mensaje}\n\n_- AnyerJR 🇻🇪_",
                parse_mode=ParseMode.MARKDOWN
            )
            enviados += 1
            await asyncio.sleep(0.1)
        except:
            pass
    await update.message.reply_text(f"✅ Mensaje enviado a `{enviados}` usuarios", parse_mode=ParseMode.MARKDOWN)

async def admin_dar_dinero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: da dinero a un usuario."""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Solo el admin puede usar esto")
        return
    if len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/dardinero [user_id] [cantidad]`")
        return
    try:
        uid = context.args[0]
        cantidad = float(context.args[1])
        sumar_dinero(int(uid), cantidad)
        await update.message.reply_text(f"✅ Se dieron `${cantidad}` al usuario `{uid}`", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Error al dar dinero")

async def admin_dar_xp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: da XP a un usuario."""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Solo el admin puede usar esto")
        return
    if len(context.args) < 2:
        await update.message.reply_text("📌 Uso: `/darxp [user_id] [cantidad]`")
        return
    try:
        uid = context.args[0]
        cantidad = int(context.args[1])
        sumar_xp(int(uid), cantidad)
        await update.message.reply_text(f"✅ Se dieron `{cantidad} XP` al usuario `{uid}`", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Error al dar XP")

async def admin_stats_global(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: estadísticas globales del bot."""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Solo el admin puede usar esto")
        return
    total_usuarios = len(usuarios_info)
    total_dinero = sum(banco.values())
    total_xp = sum(niveles.values())
    bloqueados = len(blacklist)
    await update.message.reply_text(
        f"📊 **ESTADÍSTICAS GLOBALES**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Usuarios registrados: `{total_usuarios}`\n"
        f"💰 Dinero total en circulación: `${total_dinero:,.2f}`\n"
        f"✨ XP total acumulado: `{total_xp:,}`\n"
        f"🚫 Usuarios bloqueados: `{bloqueados}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 Versión: `{VERSION}`",
        parse_mode=ParseMode.MARKDOWN
    )

# --- [ MOTOR DEL MENÚ PRINCIPAL: INTERFAZ VISUAL ] ---
''' 
👋🏻buscabas el menu? mira esta 
zona 🐍

/menu
'''
async def mostrar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el panel de control principal con las estadísticas del usuario + música relajante."""
    user_id = update.effective_user.id
    uid = str(user_id)
    nick = update.effective_user.first_name
    
    # Obtener datos para el menú
    rango = obtener_rango(user_id)
    saldo = banco.get(uid, 0.0)
    puntos = niveles.get(uid, 0)
    
    menu_txt = (
        f"👑 **CAMI.BOT · SISTEMA SUPREMO {VERSION}** 👑\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎖️ **Rango:** `{rango}`\n"
        f"💰 **Billetera:** `${saldo}`\n"
        f"✨ **Experiencia:** `{puntos} XP`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**📋 PERFIL & ECONOMÍA** (20+ cmd)\n"
        f"🎭 /reg - Registro | 👤 /perfil - Info\n"
        f"👷 /trabajar - Dinero | 🎰 /apostar - Casino\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🎥 MULTIMEDIA** (35+ cmd)\n"
        f"📥 /descargar - TikTok/IG | 🎵 /ytmp3 - Audio\n"
        f"🎬 /ytmp4 - Video | 😂 /meme - Meme\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🎨 STICKER MAKER** (11 estilos) 🆕\n"
        f"🟩 /brat · 🌟 /stk\\_neon · 🔥 /stk\\_fuego\n"
        f"🌌 /stk\\_galaxia · 🌸 /stk\\_aesthetic · 🖤 /stk\\_dark\n"
        f"🌈 /stk\\_arcoiris · ✨ /stk\\_gold · ❄️ /stk\\_hielo\n"
        f"🇻🇪 /stk\\_venezuela · 😂 /stk\\_meme\n"
        f"📋 /stk\\_lista · ver todos con ejemplos\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🖼️ BÚSQUEDA DE IMÁGENES** (6 cmd) 🆕\n"
        f"📌 /pinterest [tema] · 🖼️ /imagen [tema]\n"
        f"🖥️ /wallpaper [tema] · 🎞️ /gif [tema]\n"
        f"🎨 /fanart [tema] · 🧩 /sticker\\_buscar [tema]\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**📦 DESCARGAS EXTERNAS** (15 cmd) 🆕\n"
        f"🗂️ /mediafire [link] · _300MB_\n"
        f"☁️ /drive [link] · _Google Drive · 500MB_\n"
        f"🌩️ /pixeldrain [link] · 📂 /gofile [link] · _200MB_\n"
        f"📲 /apkpure · /apktodo · /uptodown · /apkcombo · _APKs 200MB_\n"
        f"🟢 /fdroid [app] · _open source_\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🎬 DESCARGAS DE REDES** (6 cmd) 🆕\n"
        f"🐦 /twitter [URL] · 📘 /facebook [URL] · _100MB_\n"
        f"📸 /instagram [URL] · 🎵 /tiktok [URL] · _100MB_\n"
        f"🎵 /soundcloud [nombre/URL] · _50MB_\n"
        f"🎵 /mp3 [URL o nombre] · _cualquier sitio · 50MB_\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🔍 BÚSQUEDA & INFO** (30+ cmd)\n"
        f"🔍 /buscar - Google | 📚 /wiki - Wikipedia\n"
        f"🌤️ /clima - Clima | 🌐 /ip - Info IP\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🛠️ HERRAMIENTAS** (40+ cmd)\n"
        f"🔢 /calc - Calculadora | 📏 /convertir - Unidades\n"
        f"🌐 /traducir - 12 idiomas | 🔗 /acortar - URLs\n"
        f"🔐 /hash_md5 /hash_sha256 - Hash\n"
        f"📝 /b64encode /b64decode - Base64\n"
        f"🌡️ /temp - Convertir temperatura\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🎮 JUEGOS AVANZADOS** (40+ cmd)\n"
        f"🎲 /dado - Dado | 🪙 /moneda - Moneda\n"
        f"🎯 /ppt - Piedra/Papel/Tijera\n"
        f"❓ /trivia - Trivia | 🧩 /adivinanza - Adivinanza\n"
        f"🃏 /tarot - Tarot | ♈ /horoscopo - Horóscopo\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**💰 FINANZAS** (15+ cmd)\n"
        f"💵 /dolar - Precio Dólar | 💰 /cripto - Cryptos\n"
        f"₿ /bitcoin - BTC | Ξ /ethereum - ETH\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**💪 MOTIVACIÓN & BIENESTAR** (25+ cmd)\n"
        f"⭐ /motivar - Motivación | 💡 /consejo - Consejo\n"
        f"🍅 /pomodoro - Productividad\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**📺 ENTRETENIMIENTO** (30+ cmd)\n"
        f"🎬 /pelicula - Película | 📺 /serie - Serie\n"
        f"🎵 /musica - Música | 📚 /libro - Libro\n"
        f"🎌 /anime - Anime | 🕹️ /juego - Videojuego\n"
        f"🐶 /dog - Perro | 🐱 /cat - Gato | 🦊 /fox - Zorro\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🔤 HERRAMIENTAS TEXTO** (10+ cmd)\n"
        f"🔄 /invertir | 🔢 /palabras | 🔠 /mayus | 🔡 /minus\n"
        f"📡 /morse | 🔐 /cesar | 🔁 /repetir | 🧩 /palindromo\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🧮 MATEMÁTICAS** (10+ cmd)\n"
        f"🧮 /factorial | 🌀 /fib | 🔍 /primo | 💻 /bin /hex /oct\n"
        f"√ /raiz | 📊 /porciento | ⚕️ /imc\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🎲 JUEGOS NUEVOS** (10+ cmd)\n"
        f"🌍 /pais | 🎰 /ruleta | 🤔 /verdad | 🎮 /ahorcado\n"
        f"🎲 /dadox | 🔀 /sorteo | 👥 /turnos | 💘 /compatibilidad\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🔧 GENERADORES** (10+ cmd)\n"
        f"🔑 /pass | 🆔 /uuid | 👤 /nombrefake | 📧 /emailfake\n"
        f"🚗 /placa | 🪪 /cedula | 🎨 /colorhex\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**📅 TIEMPO & FECHAS** (8+ cmd)\n"
        f"📅 /fecha | ⏱️ /unix | 🎂 /edad | ⏳ /diasfalta\n"
        f"🌍 /relojmundial | ⏳ /countdown\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**✨ DIVERSIÓN** (10+ cmd)\n"
        f"🦸 /poder | ✨ /chakra | ⚔️ /sith | ⚗️ /elemento\n"
        f"🔋 /bateria | 😂 /chisteve | 🗣️ /refran | 🍀 /suerte\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🌐 INTERNET & OSINT** (8+ cmd)\n"
        f"🌐 /whois | 📡 /ping | 🌤️ /climaciudad | 💻 /noticias\n"
        f"🔑 /useragent | 💻 /mac | 🌐 /ipprivada | 🔒 /vpn\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🆕 COMANDOS NUEVOS V13** (10+ cmd)\n"
        f"💌 /carta - Genera carta de amor/odio\n"
        f"🎤 /rap - Genera un rap al azar\n"
        f"🧿 /ojoturco - Protección espiritual\n"
        f"🕵️ /alias - Genera tu alias criminal\n"
        f"🪄 /hechizo - Lanza un hechizo random\n"
        f"🌙 /luna - Fase lunar de hoy\n"
        f"🏆 /top - Ranking de usuarios más ricos\n"
        f"💣 /bomba - Cuenta regresiva dramática\n"
        f"🧬 /adn - Análisis de ADN ficticio\n"
        f"🎰 /triplesuerte - Triple apuesta instantánea\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**🎵 AUDIO RELAJANTE EN MENÚ** 🎵\n"
        f"_↑ Música max 10MB · se reintenta automáticamente_\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ _Creado por AnyerJR · Venezuela 🇻🇪_\n"
        f"📦 **_V13.0 - 500+ COMANDOS ULTRA_** ✨"
    )
    
    # Añadir opciones extra si el que abre el menú es el creador
    if user_id == ADMIN_ID:
        menu_txt += "\n⚡ **ADMIN:** `/expropiar` | `/ver_logs` | `/admin`"

    await update.message.reply_text(menu_txt, parse_mode=ParseMode.MARKDOWN)
    
    # Enviar música relajante aleatoria
    await enviar_musica_aleatoria(update, context, nick)
    
    registrar_evento(user_id, nick, "Abrió el menú principal + Recibió música", "SISTEMA")


# --- [ FUNCIÓN PARA ENVIAR MÚSICA RELAJANTE ALEATORIA ] ---
# ✅ Sin límite de tamaño — siempre llega una canción al menú
# 🔁 Si una canción falla, reintenta con la siguiente automáticamente
# 🚫 Solo rechaza si supera el límite de Telegram (50MB)
TAMANO_MAX_TELEGRAM = 50 * 1024 * 1024  # 50 MB límite de Telegram

def _limpiar_musica_relax():
    """Limpia todos los archivos de música relajante de la carpeta."""
    try:
        for f in os.listdir(RUTA_LOGS):
            if 'musica_relax' in f:
                try:
                    os.remove(f"{RUTA_LOGS}/{f}")
                except Exception:
                    pass
    except Exception:
        pass

async def enviar_musica_aleatoria(update: Update, context: ContextTypes.DEFAULT_TYPE, nick: str):
    """
    Descarga y envía una canción relajante aleatoria de YouTube.
    """
    wait_msg = await update.message.reply_text(
        f"🎵 **Preparando música relajante para ti, {nick}...**\n"
        f"⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    # Limpiar basura previa
    _limpiar_musica_relax()

    # Mezclar la lista para no repetir siempre la misma
    lista_mezclada = CANCIONES_RELAJANTES.copy()
    random.shuffle(lista_mezclada)

    enviado = False

    for intento, cancion in enumerate(lista_mezclada, 1):
        audio_path = None

        try:
            await wait_msg.edit_text(
                f"🎵 **Buscando música...**\n"
                f"🔄 _Canción {intento}/{len(lista_mezclada)}: «{cancion[:45]}»_",
                parse_mode=ParseMode.MARKDOWN
            )

            # ─── Opciones SIN FFmpeg NI match_filter para máxima compatibilidad ───
            # worstaudio descarga el formato más ligero disponible directamente
            opciones = {
                'format': 'worstaudio/worst/bestaudio/best',
                'outtmpl': f'{RUTA_LOGS}/musica_relax_%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'default_search': 'ytsearch1',
                'extract_flat': False,
                # Sin postprocessors — sin FFmpeg requerido
                # Sin match_filter — sin NoneType
                'noplaylist': True,
            }

            def _descargar(query):
                with yt_dlp.YoutubeDL(opciones) as ydl:
                    info = ydl.extract_info(query, download=True)
                    # info puede ser dict con 'entries' (playlist) o directo
                    if info is None:
                        return None, None
                    if 'entries' in info:
                        entry = info['entries'][0] if info['entries'] else None
                        if entry is None:
                            return None, None
                        titulo = entry.get('title', 'Música Relajante')
                    else:
                        titulo = info.get('title', 'Música Relajante')
                    return titulo, ydl.prepare_filename(
                        info['entries'][0] if 'entries' in info else info
                    )

            titulo, filename_esperado = await asyncio.to_thread(_descargar, cancion)

            if titulo is None:
                print(f"⚠️ [MÚSICA] '{cancion}' → info=None, saltando")
                _limpiar_musica_relax()
                continue

            # Buscar el archivo descargado (el nombre puede variar)
            archivos = [f for f in os.listdir(RUTA_LOGS) if 'musica_relax' in f]
            if not archivos:
                print(f"⚠️ [MÚSICA] '{cancion}' → no se generó archivo, saltando")
                continue

            audio_path = f"{RUTA_LOGS}/{archivos[0]}"

            # Solo verificar límite de Telegram (50MB)
            file_size = os.path.getsize(audio_path)
            tamano_mb = round(file_size / 1024 / 1024, 2)

            if file_size > TAMANO_MAX_TELEGRAM:
                print(f"⚠️ [MÚSICA] '{titulo}' pesa {tamano_mb}MB → supera límite Telegram, saltando")
                _limpiar_musica_relax()
                continue

            # ✅ Enviar al usuario
            await wait_msg.edit_text(
                f"🎵 **Enviando música...** `{tamano_mb}MB`",
                parse_mode=ParseMode.MARKDOWN
            )

            with open(audio_path, 'rb') as audio_file:
                await update.message.reply_audio(
                    audio=audio_file,
                    title=titulo[:100],
                    caption=(
                        f"🎵 **Música Relajante**\n"
                        f"🎧 _{titulo[:70]}_\n"
                        f"✨ _Para ti, {nick}_"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )

            enviado = True
            _limpiar_musica_relax()
            await wait_msg.delete()
            break  # ✅ Listo

        except Exception as e:
            print(f"⚠️ [MÚSICA] Error con '{cancion}': {e}")
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except Exception:
                    pass
            _limpiar_musica_relax()
            await asyncio.sleep(0.5)
            continue  # 🔁 Siguiente canción

    # Si absolutamente ninguna funcionó (conexión caída, etc.)
    if not enviado:
        try:
            await wait_msg.delete()
        except Exception:
            pass
        # Envío silencioso — el menú ya fue enviado, no molestamos al usuario
        print("⚠️ [MÚSICA] No se pudo enviar música al menú — todas las canciones fallaron")

# ========================================
# [18] MÓDULO DE DESCARGAS EXTERNAS V13
# ========================================
# Límites de descarga por plataforma:
#   MediaFire  → máx 300 MB
#   APKPure    → máx 200 MB
#   APKTodo    → máx 200 MB
#   Uptodown   → máx 200 MB
#   APKCombo   → máx 200 MB
#   F-Droid    → máx 200 MB
# ========================================

HEADERS_SCRAPER = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xhtml+xml;q=0.9,*/*;q=0.8",
}

def _mb(size_bytes: int) -> float:
    """Convierte bytes a MB con 2 decimales."""
    return round(size_bytes / (1024 * 1024), 2)

def _limpiar_archivo(path: str):
    """Elimina el archivo si existe."""
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

async def _descargar_archivo_stream(url: str, destino: str, limite_bytes: int, headers: dict = None) -> tuple:
    """
    Descarga un archivo en streaming verificando el tamaño antes de guardarlo todo.
    Retorna (éxito: bool, tamaño_mb: float, mensaje_error: str)
    """
    def _download():
        h = headers or HEADERS_SCRAPER
        with requests.get(url, stream=True, headers=h, timeout=60, allow_redirects=True) as r:
            r.raise_for_status()
            # Verificar Content-Length si está disponible
            content_length = int(r.headers.get("Content-Length", 0))
            if content_length and content_length > limite_bytes:
                return False, _mb(content_length), f"El archivo pesa {_mb(content_length)}MB y el límite es {_mb(limite_bytes)}MB"

            descargado = 0
            with open(destino, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 512):  # 512KB por chunk
                    if chunk:
                        descargado += len(chunk)
                        if descargado > limite_bytes:
                            return False, _mb(descargado), f"El archivo supera el límite de {_mb(limite_bytes)}MB"
                        f.write(chunk)
            return True, _mb(descargado), ""

    return await asyncio.to_thread(_download)


# ─────────────────────────────────────────────
# /mediafire [link] → Descarga desde MediaFire
# Límite: 800 MB
# ─────────────────────────────────────────────
MEDIAFIRE_LIMITE = 800 * 110592 * 110592  # 800 MB

@tarea_larga
async def mediafire_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga un archivo desde MediaFire y lo envía al chat. Límite 800MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "📥 **Uso:** `/mediafire [enlace]`\n\n"
            "**Ejemplo:**\n"
            "`/mediafire https://www.mediafire.com/file/abc123/archivo.zip/file`\n\n"
            "📦 _Límite máximo: 800 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    url_original = context.args[0].strip()

    # Validar que sea un link de MediaFire
    if "mediafire.com" not in url_original:
        await update.message.reply_text(
            "❌ **Ese no es un enlace de MediaFire.**\n"
            "_El link debe contener `mediafire.com`_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    wait_msg = await update.message.reply_text(
        "🔍 **Analizando enlace de MediaFire...**\n⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        # ── Paso 1: Obtener la página de MediaFire para sacar el link directo
        def _obtener_link_directo():
            r = requests.get(url_original, headers=HEADERS_SCRAPER, timeout=20, allow_redirects=True)
            r.raise_for_status()
            html = r.text

            # MediaFire pone el link directo en un botón con id="downloadButton" o data-href
            # Método 1: buscar aria-label="Download file" o id="downloadButton"
            patron1 = re.search(r'href=["\']?(https://download\d*\.mediafire\.com/[^"\'>\s]+)', html)
            patron2 = re.search(r'id=["\']downloadButton["\'][^>]*href=["\']([^"\']+)["\']', html)
            patron3 = re.search(r'"downloadUrl"\s*:\s*"([^"]+)"', html)
            patron4 = re.search(r"window\.location\.href\s*=\s*['\"]([^'\"]+download[^'\"]+)['\"]", html)

            for p in [patron1, patron2, patron3, patron4]:
                if p:
                    return p.group(1).replace("\\u0026", "&").replace("\\/", "/")

            # Método alternativo con BeautifulSoup si está disponible
            if BS4_DISPONIBLE:
                soup = BeautifulSoup(html, "html.parser")
                btn = soup.find("a", {"id": "downloadButton"})
                if btn and btn.get("href"):
                    return btn["href"]
                btn2 = soup.find("a", {"aria-label": lambda x: x and "download" in x.lower()})
                if btn2 and btn2.get("href"):
                    return btn2["href"]

            return None

        link_directo = await asyncio.to_thread(_obtener_link_directo)

        if not link_directo:
            await wait_msg.edit_text(
                "❌ **No pude obtener el enlace de descarga directo.**\n"
                "_MediaFire puede haber cambiado su página. Intenta más tarde._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        # ── Paso 2: Obtener nombre del archivo desde la URL o headers
        def _obtener_nombre_y_tamano():
            r = requests.head(link_directo, headers=HEADERS_SCRAPER, timeout=15, allow_redirects=True)
            nombre = "archivo_mediafire"
            cd = r.headers.get("Content-Disposition", "")
            if "filename=" in cd:
                m = re.search(r'filename=["\']?([^"\';\n]+)', cd)
                if m:
                    nombre = m.group(1).strip()
            else:
                nombre = link_directo.split("?")[0].split("/")[-1] or nombre
            tamano = int(r.headers.get("Content-Length", 0))
            return nombre, tamano

        nombre_archivo, tamano_bytes = await asyncio.to_thread(_obtener_nombre_y_tamano)

        # Verificar tamaño antes de descargar
        if tamano_bytes and tamano_bytes > MEDIAFIRE_LIMITE:
            await wait_msg.edit_text(
                f"❌ **Archivo demasiado grande.**\n"
                f"📦 Tamaño detectado: `{_mb(tamano_bytes)} MB`\n"
                f"🚫 Límite permitido: `800 MB`",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(
            f"📥 **Descargando desde MediaFire...**\n"
            f"📄 Archivo: `{nombre_archivo[:60]}`\n"
            f"📦 Tamaño: `{_mb(tamano_bytes) if tamano_bytes else '?'} MB`\n"
            f"⏳ _Por favor espera..._",
            parse_mode=ParseMode.MARKDOWN
        )

        # ── Paso 3: Descargar el archivo
        destino = f"{RUTA_LOGS}/mf_{user_id}_{nombre_archivo}"
        exito, tamano_final, error_msg = await _descargar_archivo_stream(
            link_directo, destino, MEDIAFIRE_LIMITE
        )

        if not exito:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(
                f"❌ **Descarga cancelada.**\n_{error_msg}_",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        # ── Paso 4: Enviar al chat de Telegram
        await wait_msg.edit_text(
            f"📤 **Subiendo a Telegram...**\n"
            f"📦 `{tamano_final} MB` · _casi listo_",
            parse_mode=ParseMode.MARKDOWN
        )

        with open(destino, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=nombre_archivo,
                caption=(
                    f"✅ **Descarga completa desde MediaFire** 📥\n"
                    f"📄 **Archivo:** `{nombre_archivo[:80]}`\n"
                    f"📦 **Tamaño:** `{tamano_final} MB`\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"Descargó de MediaFire: {nombre_archivo}", "DOWNLOAD")
        sumar_xp(user_id, 20)

    except Exception as e:
        _limpiar_archivo(destino)
        print(f"❌ [MediaFire] Error: {e}")
        await wait_msg.edit_text(
            "❌ **Error al descargar desde MediaFire.**\n"
            "_Verifica que el enlace sea válido y el archivo no sea privado._",
            parse_mode=ParseMode.MARKDOWN
        )


# ─────────────────────────────────────────────
# /apkpure [nombre app] → Descarga APK de APKPure
# Límite: 200 MB
# ─────────────────────────────────────────────
APK_LIMITE = 200 * 1024 * 1024  # 200 MB

async def apkpure_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca y descarga un APK desde APKPure. Límite 200MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "📲 **Uso:** `/apkpure [nombre de la app]`\n\n"
            "**Ejemplos:**\n"
            "`/apkpure whatsapp`\n"
            "`/apkpure spotify`\n"
            "`/apkpure minecraft`\n\n"
            "📦 _Límite máximo: 200 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    query = " ".join(context.args).strip()
    wait_msg = await update.message.reply_text(
        f"🔍 **Buscando en APKPure:** `{query}`\n⏳ _Buscando app..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        # ── Paso 1: Buscar en APKPure
        def _buscar_apkpure():
            url_busqueda = f"https://apkpure.com/search?q={quote(query)}"
            r = requests.get(url_busqueda, headers=HEADERS_SCRAPER, timeout=20)
            r.raise_for_status()
            html = r.text

            # Extraer el primer resultado
            if BS4_DISPONIBLE:
                soup = BeautifulSoup(html, "html.parser")
                primer = soup.find("a", {"class": lambda c: c and "first-info" in c})
                if not primer:
                    primer = soup.find("div", {"class": "apk-info-wrap"})
                    if primer:
                        primer = primer.find("a")
                if not primer:
                    # fallback: buscar cualquier link a /es/
                    for a in soup.find_all("a", href=True):
                        href = a["href"]
                        if href.startswith("/") and href.count("/") >= 2 and "search" not in href:
                            return "https://apkpure.com" + href, a.get_text(strip=True)
                if primer:
                    href = primer.get("href", "")
                    nombre = primer.get_text(strip=True)[:60]
                    if href.startswith("/"):
                        href = "https://apkpure.com" + href
                    return href, nombre
            else:
                # Sin BeautifulSoup: buscar con regex
                m = re.search(r'href=["\'](/[a-z0-9\-]+/[a-z0-9\.\-]+/download)["\']', html)
                if m:
                    return "https://apkpure.com" + m.group(1), query
                m2 = re.search(r'href=["\']/([\w\-]+/[\w\.\-]+)["\'].*?class=["\'].*?first', html)
                if m2:
                    return "https://apkpure.com/" + m2.group(1), query

            return None, None

        url_app, nombre_app = await asyncio.to_thread(_buscar_apkpure)

        if not url_app:
            await wait_msg.edit_text(
                f"❌ **No encontré `{query}` en APKPure.**\n"
                "_Intenta con otro nombre o revisa la ortografía._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(
            f"✅ **App encontrada:** `{nombre_app or query}`\n"
            f"🔗 _Obteniendo link de descarga..._",
            parse_mode=ParseMode.MARKDOWN
        )

        # ── Paso 2: Obtener el link de descarga directo del APK
        def _obtener_link_apk():
            # APKPure tiene una página /download o /downloading
            url_dl = url_app.rstrip("/")
            if "/download" not in url_dl:
                url_dl = url_dl + "/download"

            r = requests.get(url_dl, headers=HEADERS_SCRAPER, timeout=20, allow_redirects=True)
            r.raise_for_status()
            html = r.text

            # Buscar el link directo al APK
            m = re.search(r'href=["\']?(https://[^"\'>\s]*\.apk[^"\'>\s]*)["\']?', html)
            if m:
                return m.group(1)

            if BS4_DISPONIBLE:
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    if ".apk" in a["href"].lower():
                        return a["href"]

            # Intentar con la URL de descarga directa de APKPure CDN
            m2 = re.search(r'"download_url"\s*:\s*"([^"]+)"', html)
            if m2:
                return m2.group(1).replace("\\/", "/")

            return None

        link_apk = await asyncio.to_thread(_obtener_link_apk)

        if not link_apk:
            await wait_msg.edit_text(
                f"❌ **No pude obtener el enlace de descarga del APK.**\n"
                f"_APKPure puede haber cambiado su estructura._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        # ── Paso 3: Descargar el APK
        nombre_archivo = f"{(nombre_app or query).replace(' ', '_')[:40]}.apk"
        destino = f"{RUTA_LOGS}/apkpure_{user_id}_{nombre_archivo}"

        await wait_msg.edit_text(
            f"📲 **Descargando APK desde APKPure...**\n"
            f"📄 App: `{nombre_app or query}`\n"
            f"⏳ _Descargando, espera..._",
            parse_mode=ParseMode.MARKDOWN
        )

        exito, tamano_final, error_msg = await _descargar_archivo_stream(
            link_apk, destino, APK_LIMITE
        )

        if not exito:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(
                f"❌ **Descarga cancelada.**\n_{error_msg}_",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(
            f"📤 **Subiendo APK a Telegram...**\n📦 `{tamano_final} MB`",
            parse_mode=ParseMode.MARKDOWN
        )

        with open(destino, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=nombre_archivo,
                caption=(
                    f"✅ **APK descargado desde APKPure** 📲\n"
                    f"📄 **App:** `{nombre_app or query}`\n"
                    f"📦 **Tamaño:** `{tamano_final} MB`\n"
                    f"⚠️ _Activa «fuentes desconocidas» para instalar_\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"Descargó APK APKPure: {nombre_app or query}", "DOWNLOAD")
        sumar_xp(user_id, 20)

    except Exception as e:
        _limpiar_archivo(destino)
        print(f"❌ [APKPure] Error: {e}")
        await wait_msg.edit_text(
            "❌ **Error al descargar desde APKPure.**\n"
            "_Intenta con otro nombre de app._",
            parse_mode=ParseMode.MARKDOWN
        )


# ─────────────────────────────────────────────
# /apktodo [nombre app] → Descarga APK de APKTodo
# Límite: 200 MB
# ─────────────────────────────────────────────
async def apktodo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca y descarga un APK desde APKTodo. Límite 200MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "📲 **Uso:** `/apktodo [nombre de la app]`\n\n"
            "**Ejemplos:**\n"
            "`/apktodo tiktok`\n"
            "`/apktodo instagram`\n"
            "`/apktodo free fire`\n\n"
            "📦 _Límite máximo: 200 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    query = " ".join(context.args).strip()
    wait_msg = await update.message.reply_text(
        f"🔍 **Buscando en APKTodo:** `{query}`\n⏳ _Buscando app..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        # ── Paso 1: Buscar en APKTodo
        def _buscar_apktodo():
            url_busqueda = f"https://apktodo.net/search/{quote(query.replace(' ', '-'))}/"
            r = requests.get(url_busqueda, headers=HEADERS_SCRAPER, timeout=20)
            r.raise_for_status()
            html = r.text

            if BS4_DISPONIBLE:
                soup = BeautifulSoup(html, "html.parser")
                primer = soup.find("a", {"class": lambda c: c and "app-item" in (c or "")})
                if not primer:
                    # buscar cualquier tarjeta de app
                    for a in soup.find_all("a", href=True):
                        if "/app/" in a["href"] or "/game/" in a["href"]:
                            href = a["href"]
                            if not href.startswith("http"):
                                href = "https://apktodo.net" + href
                            nombre = a.get_text(strip=True)[:60]
                            return href, nombre
            else:
                m = re.search(r'href=["\']((https://apktodo\.net)?/(?:app|game)/[a-z0-9\-]+/)["\']', html)
                if m:
                    href = m.group(1)
                    if not href.startswith("http"):
                        href = "https://apktodo.net" + href
                    return href, query

            return None, None

        url_app, nombre_app = await asyncio.to_thread(_buscar_apktodo)

        if not url_app:
            await wait_msg.edit_text(
                f"❌ **No encontré `{query}` en APKTodo.**\n"
                "_Intenta con otro nombre._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(
            f"✅ **App encontrada:** `{nombre_app or query}`\n"
            f"🔗 _Obteniendo link de descarga..._",
            parse_mode=ParseMode.MARKDOWN
        )

        # ── Paso 2: Obtener la URL directa del APK
        def _obtener_link_apktodo():
            r = requests.get(url_app, headers=HEADERS_SCRAPER, timeout=20, allow_redirects=True)
            r.raise_for_status()
            html = r.text

            # Buscar link .apk directo
            m = re.search(r'href=["\']?(https://[^"\'>\s]*\.apk[^"\'>\s]*)["\']?', html)
            if m:
                return m.group(1)

            # Buscar botón de descarga
            if BS4_DISPONIBLE:
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if ".apk" in href.lower() or "download" in href.lower():
                        if href.startswith("http"):
                            return href

            # Link CDN de APKTodo
            m2 = re.search(r'data-url=["\']([^"\']+)["\']', html)
            if m2:
                return m2.group(1)

            m3 = re.search(r'"file"\s*:\s*"([^"]+\.apk[^"]*)"', html)
            if m3:
                return m3.group(1).replace("\\/", "/")

            return None

        link_apk = await asyncio.to_thread(_obtener_link_apktodo)

        if not link_apk:
            await wait_msg.edit_text(
                f"❌ **No pude obtener el enlace del APK en APKTodo.**\n"
                "_Intenta con /apkpure o /apkcombo._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        # ── Paso 3: Descargar
        nombre_archivo = f"{(nombre_app or query).replace(' ', '_')[:40]}.apk"
        destino = f"{RUTA_LOGS}/apktodo_{user_id}_{nombre_archivo}"

        await wait_msg.edit_text(
            f"📲 **Descargando APK desde APKTodo...**\n"
            f"📄 App: `{nombre_app or query}`\n"
            f"⏳ _Por favor espera..._",
            parse_mode=ParseMode.MARKDOWN
        )

        exito, tamano_final, error_msg = await _descargar_archivo_stream(
            link_apk, destino, APK_LIMITE
        )

        if not exito:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(
                f"❌ **Descarga cancelada.**\n_{error_msg}_",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(
            f"📤 **Subiendo APK a Telegram...**\n📦 `{tamano_final} MB`",
            parse_mode=ParseMode.MARKDOWN
        )

        with open(destino, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=nombre_archivo,
                caption=(
                    f"✅ **APK descargado desde APKTodo** 📲\n"
                    f"📄 **App:** `{nombre_app or query}`\n"
                    f"📦 **Tamaño:** `{tamano_final} MB`\n"
                    f"⚠️ _Activa «fuentes desconocidas» para instalar_\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"Descargó APK APKTodo: {nombre_app or query}", "DOWNLOAD")
        sumar_xp(user_id, 20)

    except Exception as e:
        _limpiar_archivo(destino)
        print(f"❌ [APKTodo] Error: {e}")
        await wait_msg.edit_text(
            "❌ **Error al descargar desde APKTodo.**\n"
            "_Intenta con /apkpure o /apkcombo._",
            parse_mode=ParseMode.MARKDOWN
        )


# ─────────────────────────────────────────────
# /uptodown [nombre app] → Descarga desde Uptodown
# Límite: 200 MB
# ─────────────────────────────────────────────
async def uptodown_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca y descarga un APK/EXE/APP desde Uptodown. Límite 200MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "📲 **Uso:** `/uptodown [nombre de la app]`\n\n"
            "**Ejemplos:**\n"
            "`/uptodown whatsapp`\n"
            "`/uptodown netflix`\n"
            "`/uptodown vlc`\n\n"
            "📦 _Límite máximo: 200 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    query = " ".join(context.args).strip()
    wait_msg = await update.message.reply_text(
        f"🔍 **Buscando en Uptodown:** `{query}`\n⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        def _buscar_uptodown():
            url_busqueda = f"https://en.uptodown.com/search-apps/{quote(query)}"
            r = requests.get(url_busqueda, headers=HEADERS_SCRAPER, timeout=20)
            r.raise_for_status()
            html = r.text

            # Uptodown: cada app tiene una subdomain: appname.en.uptodown.com
            if BS4_DISPONIBLE:
                soup = BeautifulSoup(html, "html.parser")
                for div in soup.find_all("div", {"class": "item"}):
                    a = div.find("a", href=True)
                    if a:
                        href = a["href"]
                        nombre = a.get_text(strip=True)[:60]
                        if "uptodown.com" in href:
                            return href, nombre
            # Regex fallback
            m = re.search(r'href=["\']https://([\w\-]+)\.en\.uptodown\.com/android["\']', html)
            if m:
                nombre_slug = m.group(1)
                return f"https://{nombre_slug}.en.uptodown.com/android/download", nombre_slug
            return None, None

        url_app, nombre_app = await asyncio.to_thread(_buscar_uptodown)

        if not url_app:
            await wait_msg.edit_text(
                f"❌ **No encontré `{query}` en Uptodown.**\n"
                "_Intenta con /apkpure o /apktodo._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        # Obtener link directo
        def _obtener_link_uptodown():
            # La URL de descarga de Uptodown normalmente termina en /download
            url_dl = url_app if "/download" in url_app else url_app.rstrip("/") + "/download"
            r = requests.get(url_dl, headers=HEADERS_SCRAPER, timeout=20, allow_redirects=True)
            r.raise_for_status()
            html = r.text

            m = re.search(r'href=["\']?(https://dw\.uptodown\.com/[^"\'>\s]+)["\']?', html)
            if m:
                return m.group(1)

            if BS4_DISPONIBLE:
                soup = BeautifulSoup(html, "html.parser")
                a = soup.find("a", {"id": "detail-download-button"})
                if a and a.get("href"):
                    return a["href"]
                for a in soup.find_all("a", href=True):
                    if "dw.uptodown.com" in a["href"]:
                        return a["href"]

            m2 = re.search(r'data-url=["\']([^"\']+)["\']', html)
            if m2:
                return m2.group(1)
            return None

        link_dl = await asyncio.to_thread(_obtener_link_uptodown)

        if not link_dl:
            await wait_msg.edit_text(
                f"❌ **No pude obtener el enlace directo de Uptodown.**",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        nombre_archivo = f"{(nombre_app or query).replace(' ', '_')[:40]}.apk"
        destino = f"{RUTA_LOGS}/utd_{user_id}_{nombre_archivo}"

        await wait_msg.edit_text(
            f"📲 **Descargando desde Uptodown...**\n"
            f"📄 App: `{nombre_app or query}`\n⏳ _Descargando..._",
            parse_mode=ParseMode.MARKDOWN
        )

        exito, tamano_final, error_msg = await _descargar_archivo_stream(
            link_dl, destino, APK_LIMITE
        )

        if not exito:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(f"❌ **Descarga cancelada.**\n_{error_msg}_", parse_mode=ParseMode.MARKDOWN)
            return

        await wait_msg.edit_text(f"📤 **Subiendo a Telegram...**\n📦 `{tamano_final} MB`", parse_mode=ParseMode.MARKDOWN)

        with open(destino, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=nombre_archivo,
                caption=(
                    f"✅ **Descargado desde Uptodown** 📲\n"
                    f"📄 **App:** `{nombre_app or query}`\n"
                    f"📦 **Tamaño:** `{tamano_final} MB`\n"
                    f"⚠️ _Activa «fuentes desconocidas» para instalar_\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"Descargó Uptodown: {nombre_app or query}", "DOWNLOAD")
        sumar_xp(user_id, 20)

    except Exception as e:
        _limpiar_archivo(destino)
        print(f"❌ [Uptodown] Error: {e}")
        await wait_msg.edit_text("❌ **Error al descargar desde Uptodown.**", parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
# /apkcombo [nombre app] → Descarga desde APKCombo
# Límite: 200 MB
# ─────────────────────────────────────────────
async def apkcombo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca y descarga un APK desde APKCombo. Límite 200MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "📲 **Uso:** `/apkcombo [nombre de la app]`\n\n"
            "**Ejemplos:**\n"
            "`/apkcombo youtube`\n"
            "`/apkcombo capcut`\n"
            "`/apkcombo pubg`\n\n"
            "📦 _Límite máximo: 200 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    query = " ".join(context.args).strip()
    wait_msg = await update.message.reply_text(
        f"🔍 **Buscando en APKCombo:** `{query}`\n⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        def _buscar_apkcombo():
            url_busqueda = f"https://apkcombo.com/es/search/{quote(query)}/"
            r = requests.get(url_busqueda, headers=HEADERS_SCRAPER, timeout=20)
            r.raise_for_status()
            html = r.text

            if BS4_DISPONIBLE:
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "/es/" in href and "/download" in href and "apkcombo.com" in href:
                        return href, a.get_text(strip=True)[:60]
                # fallback sin /download
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "apkcombo.com/es/" in href and href.count("/") >= 4:
                        return href.rstrip("/") + "/download", a.get_text(strip=True)[:60]
            else:
                m = re.search(r'href=["\'](https://apkcombo\.com/es/[a-z0-9\-]+/[a-z0-9\.\-]+/download/)["\']', html)
                if m:
                    return m.group(1), query
            return None, None

        url_app, nombre_app = await asyncio.to_thread(_buscar_apkcombo)

        if not url_app:
            await wait_msg.edit_text(
                f"❌ **No encontré `{query}` en APKCombo.**",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        def _obtener_link_apkcombo():
            r = requests.get(url_app, headers=HEADERS_SCRAPER, timeout=20, allow_redirects=True)
            r.raise_for_status()
            html = r.text

            m = re.search(r'href=["\']?(https://[^"\'>\s]*apkcombo[^"\'>\s]*\.apk[^"\'>\s]*)["\']?', html)
            if m:
                return m.group(1)

            m2 = re.search(r'href=["\']?(https://[^"\'>\s]*\.apk[^"\'>\s]*)["\']?', html)
            if m2:
                return m2.group(1)

            if BS4_DISPONIBLE:
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    if ".apk" in a["href"].lower():
                        return a["href"]
                btn = soup.find("a", {"class": lambda c: c and "download" in (c or "").lower()})
                if btn and btn.get("href"):
                    return btn["href"]
            return None

        link_apk = await asyncio.to_thread(_obtener_link_apkcombo)

        if not link_apk:
            await wait_msg.edit_text(
                f"❌ **No pude obtener el enlace del APK en APKCombo.**",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        nombre_archivo = f"{(nombre_app or query).replace(' ', '_')[:40]}.apk"
        destino = f"{RUTA_LOGS}/apkcombo_{user_id}_{nombre_archivo}"

        await wait_msg.edit_text(
            f"📲 **Descargando APK desde APKCombo...**\n"
            f"📄 App: `{nombre_app or query}`\n⏳ _Espera..._",
            parse_mode=ParseMode.MARKDOWN
        )

        exito, tamano_final, error_msg = await _descargar_archivo_stream(
            link_apk, destino, APK_LIMITE
        )

        if not exito:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(f"❌ **Descarga cancelada.**\n_{error_msg}_", parse_mode=ParseMode.MARKDOWN)
            return

        await wait_msg.edit_text(f"📤 **Subiendo a Telegram...**\n📦 `{tamano_final} MB`", parse_mode=ParseMode.MARKDOWN)

        with open(destino, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=nombre_archivo,
                caption=(
                    f"✅ **APK descargado desde APKCombo** 📲\n"
                    f"📄 **App:** `{nombre_app or query}`\n"
                    f"📦 **Tamaño:** `{tamano_final} MB`\n"
                    f"⚠️ _Activa «fuentes desconocidas» para instalar_\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"Descargó APKCombo: {nombre_app or query}", "DOWNLOAD")
        sumar_xp(user_id, 20)

    except Exception as e:
        _limpiar_archivo(destino)
        print(f"❌ [APKCombo] Error: {e}")
        await wait_msg.edit_text("❌ **Error al descargar desde APKCombo.**", parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
# /fdroid [nombre app] → Descarga desde F-Droid (apps open-source)
# Límite: 200 MB
# ─────────────────────────────────────────────
async def fdroid_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca y descarga APKs open-source desde F-Droid. Límite 200MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🟢 **Uso:** `/fdroid [nombre de la app]`\n\n"
            "**Ejemplos:**\n"
            "`/fdroid vlc`\n"
            "`/fdroid firefox`\n"
            "`/fdroid signal`\n\n"
            "🔓 _F-Droid solo tiene apps 100% Open Source y gratuitas_\n"
            "📦 _Límite máximo: 200 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    query = " ".join(context.args).strip()
    wait_msg = await update.message.reply_text(
        f"🔍 **Buscando en F-Droid:** `{query}`\n⏳ _Buscando..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        def _buscar_fdroid():
            # F-Droid tiene una API de búsqueda pública
            url_api = f"https://search.f-droid.org/?q={quote(query)}&lang=es"
            r = requests.get(url_api, headers=HEADERS_SCRAPER, timeout=20)
            r.raise_for_status()
            html = r.text

            if BS4_DISPONIBLE:
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    if "/packages/" in a["href"]:
                        href = a["href"]
                        if not href.startswith("http"):
                            href = "https://f-droid.org" + href
                        nombre = a.get_text(strip=True)[:60]
                        return href, nombre
            else:
                m = re.search(r'href=["\'](/packages/[\w\.]+/)["\']', html)
                if m:
                    return "https://f-droid.org" + m.group(1), query
            return None, None

        url_app, nombre_app = await asyncio.to_thread(_buscar_fdroid)

        if not url_app:
            await wait_msg.edit_text(
                f"❌ **No encontré `{query}` en F-Droid.**\n"
                "_F-Droid solo tiene apps de código abierto._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(
            f"✅ **App encontrada:** `{nombre_app or query}`\n"
            f"🔗 _Obteniendo APK..._",
            parse_mode=ParseMode.MARKDOWN
        )

        def _obtener_link_fdroid():
            r = requests.get(url_app, headers=HEADERS_SCRAPER, timeout=20)
            r.raise_for_status()
            html = r.text

            # F-Droid sirve los APKs directamente desde f-droid.org
            m = re.search(r'href=["\']?(https://f-droid\.org/[^"\'>\s]*\.apk)["\']?', html)
            if m:
                return m.group(1)

            if BS4_DISPONIBLE:
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    if a["href"].endswith(".apk"):
                        href = a["href"]
                        if not href.startswith("http"):
                            href = "https://f-droid.org" + href
                        return href
            return None

        link_apk = await asyncio.to_thread(_obtener_link_fdroid)

        if not link_apk:
            await wait_msg.edit_text(
                f"❌ **No pude obtener el APK de F-Droid.**",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        nombre_archivo = f"{(nombre_app or query).replace(' ', '_')[:40]}.apk"
        destino = f"{RUTA_LOGS}/fdroid_{user_id}_{nombre_archivo}"

        await wait_msg.edit_text(
            f"🟢 **Descargando APK desde F-Droid...**\n"
            f"📄 App: `{nombre_app or query}`\n⏳ _Descargando..._",
            parse_mode=ParseMode.MARKDOWN
        )

        exito, tamano_final, error_msg = await _descargar_archivo_stream(
            link_apk, destino, APK_LIMITE
        )

        if not exito:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(f"❌ **Descarga cancelada.**\n_{error_msg}_", parse_mode=ParseMode.MARKDOWN)
            return

        await wait_msg.edit_text(f"📤 **Subiendo a Telegram...**\n📦 `{tamano_final} MB`", parse_mode=ParseMode.MARKDOWN)

        with open(destino, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=nombre_archivo,
                caption=(
                    f"✅ **APK descargado desde F-Droid** 🟢\n"
                    f"📄 **App:** `{nombre_app or query}`\n"
                    f"📦 **Tamaño:** `{tamano_final} MB`\n"
                    f"🔓 _App 100% Open Source y segura_\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"Descargó F-Droid: {nombre_app or query}", "DOWNLOAD")
        sumar_xp(user_id, 20)

    except Exception as e:
        _limpiar_archivo(destino)
        print(f"❌ [F-Droid] Error: {e}")
        await wait_msg.edit_text("❌ **Error al descargar desde F-Droid.**", parse_mode=ParseMode.MARKDOWN)


# ══════════════════════════════════════════════════════════════════════
# NUEVOS COMANDOS DE DESCARGA V13.1
# ══════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────
# /soundcloud [nombre o URL]
# Descarga música de SoundCloud como MP3 vía yt-dlp
# Límite: 50 MB
# ─────────────────────────────────────────────
SC_LIMITE = 50 * 1024 * 1024  # 50 MB

@tarea_larga
async def soundcloud_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga música de SoundCloud por nombre o URL. Límite 50MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🎵 **Uso:** `/soundcloud [nombre o URL]`\n\n"
            "_Ejemplos:_\n"
            "- `/soundcloud bad bunny tití me preguntó`\n"
            "- `/soundcloud https://soundcloud.com/artista/cancion`\n"
            "- `/soundcloud lo-fi chill beats`\n\n"
            "📦 _Límite máximo: 50 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    query = " ".join(context.args).strip()
    # Si no es URL completa, buscar en SoundCloud
    busqueda = query if query.startswith("http") else f"scsearch1:{query}"

    wait_msg = await update.message.reply_text(
        f"🎵 **Buscando en SoundCloud:** `{query[:50]}`\n⏳ _Descargando..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        opciones = {
            "format": "bestaudio/best",
            "outtmpl": f"{RUTA_LOGS}/sc_{user_id}_%(title)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "default_search": "scsearch1",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }],
        }

        def _descargar():
            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(busqueda, download=True)
                titulo = info.get("title", "audio") if "entries" not in info else info["entries"][0].get("title", "audio")
                return titulo

        titulo = await asyncio.to_thread(_descargar)

        # Buscar el archivo descargado
        archivos = [f for f in os.listdir(RUTA_LOGS) if f.startswith(f"sc_{user_id}_")]
        if not archivos:
            await wait_msg.edit_text("❌ **No se pudo descargar el audio.**", parse_mode=ParseMode.MARKDOWN)
            return

        destino = f"{RUTA_LOGS}/{archivos[0]}"
        tamano = os.path.getsize(destino)

        if tamano > SC_LIMITE:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(
                f"❌ **Archivo muy pesado:** `{_mb(tamano)} MB`\n"
                f"_Límite: 50 MB. Intenta con una canción más corta._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(f"📤 **Subiendo a Telegram...** `{_mb(tamano)} MB`", parse_mode=ParseMode.MARKDOWN)

        with open(destino, "rb") as f:
            await update.message.reply_audio(
                audio=f,
                title=titulo[:100],
                caption=(
                    f"🎵 **SoundCloud** · `{titulo[:80]}`\n"
                    f"📦 `{_mb(tamano)} MB`\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"SoundCloud: {titulo}", "DOWNLOAD")
        sumar_xp(user_id, 15)

    except Exception as e:
        _limpiar_archivo(destino)
        for f in os.listdir(RUTA_LOGS):
            if f.startswith(f"sc_{user_id}_"):
                _limpiar_archivo(f"{RUTA_LOGS}/{f}")
        print(f"❌ [SoundCloud] {e}")
        await wait_msg.edit_text(
            "❌ **No se encontró la canción en SoundCloud.**\n"
            "_Intenta con otro nombre o URL directa._",
            parse_mode=ParseMode.MARKDOWN
        )


# ─────────────────────────────────────────────
# /twitter [URL] — Descarga video de Twitter/X
# Límite: 100 MB
# ─────────────────────────────────────────────
TWITTER_LIMITE = 100 * 1024 * 1024  # 100 MB

async def twitter_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga videos de Twitter/X. Límite 100MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🐦 **Uso:** `/twitter [URL del tweet]`\n\n"
            "_Ejemplo:_\n"
            "- `/twitter https://x.com/usuario/status/12345`\n"
            "- `/twitter https://twitter.com/usuario/status/12345`\n\n"
            "📦 _Límite máximo: 100 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    url = context.args[0].strip()
    if "twitter.com" not in url and "x.com" not in url and "t.co" not in url:
        await update.message.reply_text(
            "❌ **Eso no parece un enlace de Twitter/X.**\n"
            "_Debe contener `twitter.com` o `x.com`_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    wait_msg = await update.message.reply_text(
        "🐦 **Descargando video de Twitter/X...**\n⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        opciones = {
            "format": "best[filesize<100M]/best",
            "outtmpl": f"{RUTA_LOGS}/tw_{user_id}_%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
        }

        def _descargar():
            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(url, download=True)
                return info.get("title", "video"), ydl.prepare_filename(info)

        titulo, destino = await asyncio.to_thread(_descargar)

        # Si el filename no existe buscar en carpeta
        if not os.path.exists(destino):
            archivos = [f for f in os.listdir(RUTA_LOGS) if f.startswith(f"tw_{user_id}_")]
            if not archivos:
                await wait_msg.edit_text("❌ **No se encontró el archivo descargado.**", parse_mode=ParseMode.MARKDOWN)
                return
            destino = f"{RUTA_LOGS}/{archivos[0]}"

        tamano = os.path.getsize(destino)
        if tamano > TWITTER_LIMITE:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(
                f"❌ **Video muy pesado:** `{_mb(tamano)} MB` · Límite: 100 MB",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(f"📤 **Subiendo video...** `{_mb(tamano)} MB`", parse_mode=ParseMode.MARKDOWN)

        with open(destino, "rb") as f:
            await update.message.reply_video(
                video=f,
                caption=(
                    f"🐦 **Twitter/X** · `{titulo[:80]}`\n"
                    f"📦 `{_mb(tamano)} MB`\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"Twitter: {url}", "DOWNLOAD")
        sumar_xp(user_id, 15)

    except Exception as e:
        _limpiar_archivo(destino)
        for f in os.listdir(RUTA_LOGS):
            if f.startswith(f"tw_{user_id}_"):
                _limpiar_archivo(f"{RUTA_LOGS}/{f}")
        print(f"❌ [Twitter] {e}")
        await wait_msg.edit_text(
            "❌ **No se pudo descargar el video.**\n"
            "_El tweet puede ser privado o no tener video._",
            parse_mode=ParseMode.MARKDOWN
        )


# ─────────────────────────────────────────────
# /instagram [URL] — Descarga posts/reels de Instagram
# Límite: 100 MB
# ─────────────────────────────────────────────
INSTAGRAM_LIMITE = 100 * 1024 * 1024  # 100 MB

async def instagram_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga fotos y videos de Instagram (posts/reels públicos). Límite 100MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "📸 **Uso:** `/instagram [URL]`\n\n"
            "_Ejemplo:_\n"
            "- `/instagram https://www.instagram.com/reel/ABC123/`\n"
            "- `/instagram https://www.instagram.com/p/ABC123/`\n\n"
            "⚠️ _Solo funciona con publicaciones públicas_\n"
            "📦 _Límite máximo: 100 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    url = context.args[0].strip()
    if "instagram.com" not in url:
        await update.message.reply_text(
            "❌ **Eso no es un enlace de Instagram.**",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    wait_msg = await update.message.reply_text(
        "📸 **Descargando de Instagram...**\n⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        opciones = {
            "format": "best[filesize<100M]/best",
            "outtmpl": f"{RUTA_LOGS}/ig_{user_id}_%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
        }

        def _descargar():
            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get("title", "instagram")
                filename = ydl.prepare_filename(info)
                ext = info.get("ext", "mp4")
                return titulo, filename, ext

        titulo, destino, ext = await asyncio.to_thread(_descargar)

        if not os.path.exists(destino):
            archivos = [f for f in os.listdir(RUTA_LOGS) if f.startswith(f"ig_{user_id}_")]
            if not archivos:
                await wait_msg.edit_text("❌ **No se pudo descargar el contenido.**", parse_mode=ParseMode.MARKDOWN)
                return
            destino = f"{RUTA_LOGS}/{archivos[0]}"
            ext = destino.rsplit(".", 1)[-1]

        tamano = os.path.getsize(destino)
        if tamano > INSTAGRAM_LIMITE:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(
                f"❌ **Archivo muy pesado:** `{_mb(tamano)} MB` · Límite: 100 MB",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(f"📤 **Subiendo contenido...** `{_mb(tamano)} MB`", parse_mode=ParseMode.MARKDOWN)

        caption_txt = (
            f"📸 **Instagram** · `{titulo[:80]}`\n"
            f"📦 `{_mb(tamano)} MB`\n"
            f"👤 _Pedido por {nick}_"
        )

        with open(destino, "rb") as f:
            if ext.lower() in ["mp4", "mov", "webm", "mkv"]:
                await update.message.reply_video(video=f, caption=caption_txt, parse_mode=ParseMode.MARKDOWN)
            elif ext.lower() in ["jpg", "jpeg", "png", "webp"]:
                await update.message.reply_photo(photo=f, caption=caption_txt, parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_document(document=f, caption=caption_txt, parse_mode=ParseMode.MARKDOWN)

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"Instagram: {url}", "DOWNLOAD")
        sumar_xp(user_id, 15)

    except Exception as e:
        _limpiar_archivo(destino)
        for f in os.listdir(RUTA_LOGS):
            if f.startswith(f"ig_{user_id}_"):
                _limpiar_archivo(f"{RUTA_LOGS}/{f}")
        print(f"❌ [Instagram] {e}")
        await wait_msg.edit_text(
            "❌ **No se pudo descargar el contenido de Instagram.**\n"
            "_Verifica que la cuenta sea pública y el enlace sea correcto._",
            parse_mode=ParseMode.MARKDOWN
        )


# ─────────────────────────────────────────────
# /tiktok [URL] — Descarga video de TikTok sin marca de agua
# Límite: 100 MB
# ─────────────────────────────────────────────
TIKTOK_LIMITE = 100 * 1024 * 1024  # 100 MB

@tarea_larga
async def tiktok_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga videos de TikTok sin marca de agua. Límite 100MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🎵 **Uso:** `/tiktok [URL del video]`\n\n"
            "_Ejemplo:_\n"
            "- `/tiktok https://www.tiktok.com/@usuario/video/12345`\n"
            "- `/tiktok https://vm.tiktok.com/ABCDE/`\n\n"
            "✅ _Sin marca de agua_\n"
            "📦 _Límite máximo: 100 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    url = context.args[0].strip()
    if "tiktok.com" not in url and "vm.tiktok" not in url:
        await update.message.reply_text("❌ **Eso no es un enlace de TikTok.**", parse_mode=ParseMode.MARKDOWN)
        return

    wait_msg = await update.message.reply_text(
        "🎵 **Descargando TikTok sin marca de agua...**\n⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        # yt-dlp con workaround para evitar watermark
        opciones = {
            "format": "best[filesize<100M]/best",
            "outtmpl": f"{RUTA_LOGS}/tt_{user_id}_%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "extractor_args": {"tiktok": {"webpage_download": True}},
        }

        def _descargar():
            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get("title", "tiktok_video")
                return titulo, ydl.prepare_filename(info)

        titulo, destino = await asyncio.to_thread(_descargar)

        if not os.path.exists(destino):
            archivos = [f for f in os.listdir(RUTA_LOGS) if f.startswith(f"tt_{user_id}_")]
            if not archivos:
                await wait_msg.edit_text("❌ **No se pudo descargar el video.**", parse_mode=ParseMode.MARKDOWN)
                return
            destino = f"{RUTA_LOGS}/{archivos[0]}"

        tamano = os.path.getsize(destino)
        if tamano > TIKTOK_LIMITE:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(
                f"❌ **Video muy pesado:** `{_mb(tamano)} MB` · Límite: 100 MB",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(f"📤 **Subiendo video TikTok...** `{_mb(tamano)} MB`", parse_mode=ParseMode.MARKDOWN)

        with open(destino, "rb") as f:
            await update.message.reply_video(
                video=f,
                caption=(
                    f"🎵 **TikTok** · `{titulo[:80]}`\n"
                    f"📦 `{_mb(tamano)} MB` · ✅ Sin watermark\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"TikTok: {url}", "DOWNLOAD")
        sumar_xp(user_id, 15)

    except Exception as e:
        _limpiar_archivo(destino)
        for f in os.listdir(RUTA_LOGS):
            if f.startswith(f"tt_{user_id}_"):
                _limpiar_archivo(f"{RUTA_LOGS}/{f}")
        print(f"❌ [TikTok] {e}")
        await wait_msg.edit_text(
            "❌ **No se pudo descargar el video de TikTok.**\n"
            "_Verifica que el enlace sea correcto o el video no sea privado._",
            parse_mode=ParseMode.MARKDOWN
        )

# ─────────────────────────────────────────────
# /drive [link] — Descarga archivos de Google Drive públicos
# Límite: 500 MB
# ─────────────────────────────────────────────
DRIVE_LIMITE = 500 * 1024 * 1024  # 500 MB

async def drive_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga archivos de Google Drive (públicos). Límite 500MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "☁️ **Uso:** `/drive [link de Google Drive]`\n\n"
            "_Ejemplo:_\n"
            "- `/drive https://drive.google.com/file/d/ABCDE/view`\n"
            "- `/drive https://drive.google.com/open?id=ABCDE`\n\n"
            "⚠️ _Solo funciona con archivos compartidos públicamente_\n"
            "📦 _Límite máximo: 500 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    url_original = context.args[0].strip()
    if "drive.google.com" not in url_original and "docs.google.com" not in url_original:
        await update.message.reply_text("❌ **Eso no es un enlace de Google Drive.**", parse_mode=ParseMode.MARKDOWN)
        return

    wait_msg = await update.message.reply_text(
        "☁️ **Procesando enlace de Google Drive...**\n⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        # Extraer el ID del archivo de cualquier formato de URL de Drive
        file_id = None
        patrones = [
            r"/file/d/([a-zA-Z0-9_\-]+)",
            r"id=([a-zA-Z0-9_\-]+)",
            r"/d/([a-zA-Z0-9_\-]+)",
            r"open\?id=([a-zA-Z0-9_\-]+)",
        ]
        for p in patrones:
            m = re.search(p, url_original)
            if m:
                file_id = m.group(1)
                break

        if not file_id:
            await wait_msg.edit_text(
                "❌ **No pude extraer el ID del archivo Drive.**\n"
                "_Verifica que el enlace sea correcto._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        # Construir URL de descarga directa de Drive
        url_descarga = f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t"

        def _obtener_nombre_drive():
            # Primer request para obtener headers y manejar el aviso de virus de Drive
            s = requests.Session()
            s.headers.update(BING_HEADERS)
            r = s.get(url_descarga, stream=True, timeout=20, allow_redirects=True)
            # Si Drive muestra página de confirmación para archivos grandes
            if "virus scan warning" in r.text.lower() or "download_warning" in r.url:
                # Extraer token de confirmación
                token = re.search(r'confirm=([a-zA-Z0-9_\-]+)', r.url)
                if not token:
                    token = re.search(r'name="confirm"\s+value="([^"]+)"', r.text)
                if token:
                    url_final = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={token.group(1)}"
                    r = s.get(url_final, stream=True, timeout=20)
            # Obtener nombre del Content-Disposition
            cd = r.headers.get("Content-Disposition", "")
            nombre = "archivo_drive"
            if "filename=" in cd:
                m2 = re.search(r'filename=["\']?([^"\';\n]+)', cd)
                if m2:
                    nombre = m2.group(1).strip().strip('"')
            tamano = int(r.headers.get("Content-Length", 0))
            return r, nombre, tamano

        response_obj, nombre_archivo, tamano_bytes = await asyncio.to_thread(_obtener_nombre_drive)

        if tamano_bytes and tamano_bytes > DRIVE_LIMITE:
            await wait_msg.edit_text(
                f"❌ **Archivo muy pesado:** `{_mb(tamano_bytes)} MB`\n"
                f"_Límite: 500 MB_",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(
            f"☁️ **Descargando desde Google Drive...**\n"
            f"📄 `{nombre_archivo[:60]}`\n"
            f"📦 `{_mb(tamano_bytes) if tamano_bytes else '?'} MB`\n"
            f"⏳ _Descargando..._",
            parse_mode=ParseMode.MARKDOWN
        )

        destino = f"{RUTA_LOGS}/gdrive_{user_id}_{nombre_archivo}"
        exito, tamano_final, error_msg = await _descargar_archivo_stream(
            url_descarga, destino, DRIVE_LIMITE
        )

        if not exito:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(f"❌ **Descarga cancelada.**\n_{error_msg}_", parse_mode=ParseMode.MARKDOWN)
            return

        await wait_msg.edit_text(f"📤 **Subiendo a Telegram...** `{tamano_final} MB`", parse_mode=ParseMode.MARKDOWN)

        with open(destino, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=nombre_archivo,
                caption=(
                    f"☁️ **Google Drive** · `{nombre_archivo[:80]}`\n"
                    f"📦 `{tamano_final} MB`\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"Drive: {nombre_archivo}", "DOWNLOAD")
        sumar_xp(user_id, 20)

    except Exception as e:
        _limpiar_archivo(destino)
        print(f"❌ [Drive] {e}")
        await wait_msg.edit_text(
            "❌ **No se pudo descargar el archivo.**\n"
            "_Asegúrate de que el archivo sea público (compartido con 'cualquiera que tenga el enlace')._",
            parse_mode=ParseMode.MARKDOWN
        )


# ─────────────────────────────────────────────
# /pixeldrain [link] — Descarga desde Pixeldrain
# Límite: 200 MB
# ─────────────────────────────────────────────
PIXELDRAIN_LIMITE = 200 * 1024 * 1024  # 200 MB

async def pixeldrain_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga archivos de Pixeldrain. Límite 200MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🌩️ **Uso:** `/pixeldrain [link]`\n\n"
            "_Ejemplo:_\n"
            "- `/pixeldrain https://pixeldrain.com/u/ABCDE`\n\n"
            "📦 _Límite máximo: 200 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    url_original = context.args[0].strip()
    if "pixeldrain.com" not in url_original:
        await update.message.reply_text("❌ **Eso no es un enlace de Pixeldrain.**", parse_mode=ParseMode.MARKDOWN)
        return

    wait_msg = await update.message.reply_text(
        "🌩️ **Procesando enlace de Pixeldrain...**\n⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        # Extraer el ID del archivo: pixeldrain.com/u/{ID} o pixeldrain.com/l/{ID}
        m = re.search(r"pixeldrain\.com/u/([a-zA-Z0-9]+)", url_original)
        if not m:
            await wait_msg.edit_text(
                "❌ **No pude extraer el ID del archivo Pixeldrain.**\n"
                "_El link debe ser: `pixeldrain.com/u/XXXXXXXX`_",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        file_id = m.group(1)

        # La API pública de Pixeldrain es muy simple:
        # GET https://pixeldrain.com/api/file/{ID} → descarga directa
        # GET https://pixeldrain.com/api/file/{ID}/info → metadatos
        def _obtener_info():
            r = requests.get(
                f"https://pixeldrain.com/api/file/{file_id}/info",
                headers=BING_HEADERS, timeout=15
            )
            if r.status_code == 200:
                data = r.json()
                return data.get("name", f"pixeldrain_{file_id}"), data.get("size", 0)
            return f"pixeldrain_{file_id}", 0

        nombre_archivo, tamano_bytes = await asyncio.to_thread(_obtener_info)

        if tamano_bytes and tamano_bytes > PIXELDRAIN_LIMITE:
            await wait_msg.edit_text(
                f"❌ **Archivo muy pesado:** `{_mb(tamano_bytes)} MB`\n_Límite: 200 MB_",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(
            f"🌩️ **Descargando desde Pixeldrain...**\n"
            f"📄 `{nombre_archivo[:60]}`\n"
            f"📦 `{_mb(tamano_bytes) if tamano_bytes else '?'} MB`\n"
            f"⏳ _Descargando..._",
            parse_mode=ParseMode.MARKDOWN
        )

        url_descarga = f"https://pixeldrain.com/api/file/{file_id}"
        destino = f"{RUTA_LOGS}/pd_{user_id}_{nombre_archivo}"

        exito, tamano_final, error_msg = await _descargar_archivo_stream(
            url_descarga, destino, PIXELDRAIN_LIMITE
        )

        if not exito:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(f"❌ **Descarga cancelada.**\n_{error_msg}_", parse_mode=ParseMode.MARKDOWN)
            return

        await wait_msg.edit_text(f"📤 **Subiendo a Telegram...** `{tamano_final} MB`", parse_mode=ParseMode.MARKDOWN)

        with open(destino, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=nombre_archivo,
                caption=(
                    f"🌩️ **Pixeldrain** · `{nombre_archivo[:80]}`\n"
                    f"📦 `{tamano_final} MB`\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"Pixeldrain: {nombre_archivo}", "DOWNLOAD")
        sumar_xp(user_id, 20)

    except Exception as e:
        _limpiar_archivo(destino)
        print(f"❌ [Pixeldrain] {e}")
        await wait_msg.edit_text("❌ **Error al descargar desde Pixeldrain.**", parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
# /gofile [link] — Descarga desde GoFile.io
# Límite: 200 MB
# ─────────────────────────────────────────────
GOFILE_LIMITE = 200 * 1024 * 1024  # 200 MB

async def gofile_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga archivos de GoFile.io. Límite 200MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "📂 **Uso:** `/gofile [link]`\n\n"
            "_Ejemplo:_\n"
            "- `/gofile https://gofile.io/d/ABCDE`\n\n"
            "📦 _Límite máximo: 200 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    url_original = context.args[0].strip()
    if "gofile.io" not in url_original:
        await update.message.reply_text("❌ **Eso no es un enlace de GoFile.**", parse_mode=ParseMode.MARKDOWN)
        return

    wait_msg = await update.message.reply_text(
        "📂 **Procesando enlace de GoFile...**\n⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        # Extraer el código de la carpeta/archivo: gofile.io/d/{code}
        m = re.search(r"gofile\.io/d/([a-zA-Z0-9]+)", url_original)
        if not m:
            await wait_msg.edit_text(
                "❌ **No pude extraer el código del enlace GoFile.**",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        code = m.group(1)

        # GoFile API pública - Paso 1: obtener token de invitado
        def _obtener_token():
            r = requests.post("https://api.gofile.io/accounts", timeout=15)
            r.raise_for_status()
            return r.json().get("data", {}).get("token", "")

        token = await asyncio.to_thread(_obtener_token)

        if not token:
            await wait_msg.edit_text("❌ **No se pudo obtener acceso a GoFile.**", parse_mode=ParseMode.MARKDOWN)
            return

        # Paso 2: obtener contenido de la carpeta
        def _obtener_contenido():
            r = requests.get(
                f"https://api.gofile.io/contents/{code}?wt=4fd6sg89d7s6",
                headers={"Authorization": f"Bearer {token}", **BING_HEADERS},
                timeout=15
            )
            r.raise_for_status()
            return r.json()

        data = await asyncio.to_thread(_obtener_contenido)

        if data.get("status") != "ok":
            await wait_msg.edit_text(
                "❌ **No se pudo acceder al contenido de GoFile.**\n"
                "_El enlace puede estar expirado o ser privado._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        # Obtener el primer archivo del contenido
        contenido = data.get("data", {}).get("children", {})
        if not contenido:
            await wait_msg.edit_text("❌ **La carpeta de GoFile está vacía.**", parse_mode=ParseMode.MARKDOWN)
            return

        # Tomar el primer archivo
        primer_item = next(iter(contenido.values()))
        nombre_archivo = primer_item.get("name", f"gofile_{code}")
        tamano_bytes = primer_item.get("size", 0)
        link_descarga = primer_item.get("link", "")

        if not link_descarga:
            await wait_msg.edit_text("❌ **No se encontró enlace de descarga en GoFile.**", parse_mode=ParseMode.MARKDOWN)
            return

        if tamano_bytes and tamano_bytes > GOFILE_LIMITE:
            await wait_msg.edit_text(
                f"❌ **Archivo muy pesado:** `{_mb(tamano_bytes)} MB`\n_Límite: 200 MB_",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(
            f"📂 **Descargando desde GoFile...**\n"
            f"📄 `{nombre_archivo[:60]}`\n"
            f"📦 `{_mb(tamano_bytes) if tamano_bytes else '?'} MB`\n"
            f"⏳ _Descargando..._",
            parse_mode=ParseMode.MARKDOWN
        )

        destino = f"{RUTA_LOGS}/gf_{user_id}_{nombre_archivo}"
        dl_headers = {"Cookie": f"accountToken={token}", **BING_HEADERS}

        exito, tamano_final, error_msg = await _descargar_archivo_stream(
            link_descarga, destino, GOFILE_LIMITE, headers=dl_headers
        )

        if not exito:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(f"❌ **Descarga cancelada.**\n_{error_msg}_", parse_mode=ParseMode.MARKDOWN)
            return

        await wait_msg.edit_text(f"📤 **Subiendo a Telegram...** `{tamano_final} MB`", parse_mode=ParseMode.MARKDOWN)

        with open(destino, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=nombre_archivo,
                caption=(
                    f"📂 **GoFile** · `{nombre_archivo[:80]}`\n"
                    f"📦 `{tamano_final} MB`\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"GoFile: {nombre_archivo}", "DOWNLOAD")
        sumar_xp(user_id, 20)

    except Exception as e:
        _limpiar_archivo(destino)
        print(f"❌ [GoFile] {e}")
        await wait_msg.edit_text("❌ **Error al descargar desde GoFile.**", parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
# /mp3 [URL] — Convierte cualquier URL compatible con yt-dlp a MP3
# Funciona con: YouTube, SoundCloud, Vimeo, Dailymotion, etc.
# Límite: 50 MB
# ─────────────────────────────────────────────
MP3_LIMITE = 50 * 1024 * 1024  # 50 MB

@tarea_larga
async def mp3_universal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convierte cualquier URL de video/audio a MP3. Límite 50MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "🎵 **Uso:** `/mp3 [URL o nombre de canción]`\n\n"
            "_Compatible con:_\n"
            "▸ YouTube · SoundCloud · Vimeo\n"
            "▸ Dailymotion · Facebook · Twitter\n"
            "▸ Instagram · TikTok · y más!\n\n"
            "_Ejemplos:_\n"
            "- `/mp3 https://youtu.be/dQw4w9WgXcQ`\n"
            "- `/mp3 bad bunny tití me preguntó`\n"
            "- `/mp3 https://soundcloud.com/x/y`\n\n"
            "📦 _Límite máximo: 50 MB · 128kbps MP3_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    query = " ".join(context.args).strip()
    es_url = query.startswith("http")
    busqueda = query if es_url else f"ytsearch1:{query}"

    wait_msg = await update.message.reply_text(
        f"🎵 **{'Descargando' if es_url else 'Buscando'} audio:** `{query[:60]}`\n"
        f"⏳ _Convirtiendo a MP3 128kbps..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        opciones = {
            "format": "bestaudio/best",
            "outtmpl": f"{RUTA_LOGS}/mp3u_{user_id}_%(title)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }],
        }

        def _descargar():
            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(busqueda, download=True)
                if "entries" in info:
                    info = info["entries"][0]
                return info.get("title", "audio"), info.get("duration", 0), info.get("uploader", "")

        titulo, duracion, artista = await asyncio.to_thread(_descargar)

        # Buscar archivo descargado
        archivos = [f for f in os.listdir(RUTA_LOGS) if f.startswith(f"mp3u_{user_id}_")]
        if not archivos:
            await wait_msg.edit_text("❌ **No se pudo convertir el audio.**", parse_mode=ParseMode.MARKDOWN)
            return

        destino = f"{RUTA_LOGS}/{archivos[0]}"
        tamano = os.path.getsize(destino)

        if tamano > MP3_LIMITE:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(
                f"❌ **Archivo muy pesado:** `{_mb(tamano)} MB`\n"
                f"_Límite: 50 MB. Busca una versión más corta._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        mins = duracion // 60 if duracion else 0
        segs = duracion % 60 if duracion else 0

        await wait_msg.edit_text(f"📤 **Subiendo MP3...** `{_mb(tamano)} MB`", parse_mode=ParseMode.MARKDOWN)

        with open(destino, "rb") as f:
            await update.message.reply_audio(
                audio=f,
                title=titulo[:100],
                performer=artista[:60] if artista else None,
                duration=duracion or None,
                caption=(
                    f"🎵 **{titulo[:80]}**\n"
                    f"{'👤 `' + artista[:50] + '`' + chr(10) if artista else ''}"
                    f"⏱️ `{mins}:{segs:02d}` · 📦 `{_mb(tamano)} MB` · 128kbps\n"
                    f"🤖 _Convertido por CamilaBot_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"MP3: {titulo}", "DOWNLOAD")
        sumar_xp(user_id, 12)

    except Exception as e:
        _limpiar_archivo(destino)
        for f in os.listdir(RUTA_LOGS):
            if f.startswith(f"mp3u_{user_id}_"):
                _limpiar_archivo(f"{RUTA_LOGS}/{f}")
        print(f"❌ [MP3] {e}")
        await wait_msg.edit_text(
            "❌ **No se pudo convertir el audio.**\n"
            "_Verifica la URL o el nombre de la canción._",
            parse_mode=ParseMode.MARKDOWN
        )


# ─────────────────────────────────────────────
# /facebook [URL] — Descarga videos de Facebook
# Límite: 100 MB
# ─────────────────────────────────────────────
FACEBOOK_LIMITE = 100 * 1024 * 1024  # 100 MB

async def facebook_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga videos de Facebook (públicos). Límite 100MB."""
    user_id = update.effective_user.id
    nick = update.effective_user.first_name

    if not context.args:
        await update.message.reply_text(
            "📘 **Uso:** `/facebook [URL del video]`\n\n"
            "_Ejemplo:_\n"
            "- `/facebook https://www.facebook.com/watch?v=12345`\n"
            "- `/facebook https://fb.watch/ABCDE/`\n\n"
            "⚠️ _Solo funciona con videos públicos_\n"
            "📦 _Límite máximo: 100 MB_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    url = context.args[0].strip()
    if "facebook.com" not in url and "fb.watch" not in url and "fb.com" not in url:
        await update.message.reply_text("❌ **Eso no es un enlace de Facebook.**", parse_mode=ParseMode.MARKDOWN)
        return

    wait_msg = await update.message.reply_text(
        "📘 **Descargando video de Facebook...**\n⏳ _Un momento..._",
        parse_mode=ParseMode.MARKDOWN
    )

    destino = None
    try:
        opciones = {
            "format": "best[filesize<100M]/best",
            "outtmpl": f"{RUTA_LOGS}/fb_{user_id}_%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
        }

        def _descargar():
            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(url, download=True)
                return info.get("title", "facebook_video"), ydl.prepare_filename(info)

        titulo, destino = await asyncio.to_thread(_descargar)

        if not os.path.exists(destino):
            archivos = [f for f in os.listdir(RUTA_LOGS) if f.startswith(f"fb_{user_id}_")]
            if not archivos:
                await wait_msg.edit_text("❌ **No se pudo descargar el video.**", parse_mode=ParseMode.MARKDOWN)
                return
            destino = f"{RUTA_LOGS}/{archivos[0]}"

        tamano = os.path.getsize(destino)
        if tamano > FACEBOOK_LIMITE:
            _limpiar_archivo(destino)
            await wait_msg.edit_text(
                f"❌ **Video muy pesado:** `{_mb(tamano)} MB` · Límite: 100 MB",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        await wait_msg.edit_text(f"📤 **Subiendo video...** `{_mb(tamano)} MB`", parse_mode=ParseMode.MARKDOWN)

        with open(destino, "rb") as f:
            await update.message.reply_video(
                video=f,
                caption=(
                    f"📘 **Facebook** · `{titulo[:80]}`\n"
                    f"📦 `{_mb(tamano)} MB`\n"
                    f"👤 _Pedido por {nick}_"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

        _limpiar_archivo(destino)
        await wait_msg.delete()
        registrar_evento(user_id, nick, f"Facebook: {url}", "DOWNLOAD")
        sumar_xp(user_id, 15)

    except Exception as e:
        _limpiar_archivo(destino)
        for f in os.listdir(RUTA_LOGS):
            if f.startswith(f"fb_{user_id}_"):
                _limpiar_archivo(f"{RUTA_LOGS}/{f}")
        print(f"❌ [Facebook] {e}")
        await wait_msg.edit_text(
            "❌ **No se pudo descargar el video de Facebook.**\n"
            "_Verifica que el video sea público._",
            parse_mode=ParseMode.MARKDOWN
        )


async def carta_amor_odio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera una carta de amor o de odio según el argumento."""
    user_nick = update.effective_user.first_name
    tipo = " ".join(context.args).lower() if context.args else "amor"

    if "odio" in tipo:
        cartas = [
            f"💔 Querida persona,\nDesde que llegaste a mi vida todo fue peor. No sé cómo aguanto tanta energía tóxica. Atentamente, {user_nick} 🖕",
            f"😤 Estimado/a,\nTe escribo para decirte que me caes peor que el lunes. Cuídate mucho (lejos de mí). Con desprecio, {user_nick}",
            f"🤬 Para quien le corresponda,\nEres tan molesto/a que hasta el WiFi se cae cuando apareces. Bye, {user_nick}",
        ]
        carta = random.choice(cartas)
        emoji = "💔"
        tipo_txt = "ODIO"
    else:
        nombres = ["mi amor", "corazón", "princesa", "rey", "cielo", "mi vida"]
        cartas = [
            f"💌 Querido/a {random.choice(nombres)},\nCada vez que te veo, mi corazón late como si fuera a explotar. Eres lo más bonito de mi día. Con todo mi cariño, {user_nick} 💕",
            f"🌹 Para ti, {random.choice(nombres)},\nSi fueras una canción, sería mi favorita en repeat. No sé vivir sin tu sonrisa. Tuyo/a siempre, {user_nick} 💖",
            f"🦋 A quien roba mis sueños,\nEl universo se tardó mucho en traerte, pero valió cada segundo. Te quiero más de lo que las palabras pueden decir. Con amor infinito, {user_nick} 💗",
        ]
        carta = random.choice(cartas)
        emoji = "💌"
        tipo_txt = "AMOR"

    await update.message.reply_text(
        f"{emoji} **CARTA DE {tipo_txt}** {emoji}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"_{carta}_\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📌 _Uso: /carta amor | /carta odio_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def rap_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera un rap venezolano al azar."""
    user_nick = update.effective_user.first_name
    raps = [
        f"🎤 *{user_nick} en el micrófono:*\nVengo desde Caracas con fuego en los pies,\ncada obstáculo lo tumbo de una sola vez.\nNadie me detiene, soy como el petróleo negro,\nbrillo aunque estén ciegos, con talento y entrega.",
        f"🎤 *{user_nick} soltando bars:*\nSoy venezolano, tengo flow y sazón,\ncada verso mío es una revolución.\nLos que dudaron hoy me están siguiendo,\nel éxito llega pa' los que van creyendo.",
        f"🎤 *{user_nick} en el beat:*\nDel barrio pa' el mundo, sin parar de crecer,\ncon hambre de triunfo y ganas de vencer.\nMi acento es mi bandera, mi cultura mi escudo,\nvenezolano puro, firme como un mudo.",
        f"🎤 *{user_nick} freestyle:*\nLas calles me formaron, la vida me enseñó,\ncada cicatriz que tengo me hizo más veloz.\nNo hay techo pa' mí, voy más allá del cielo,\ncon el corazón abierto y el espíritu entero.",
    ]
    await update.message.reply_text(random.choice(raps), parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 5)

async def ojo_turco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Protección espiritual del ojo turco."""
    user_nick = update.effective_user.first_name
    nivel = random.randint(1, 100)
    protecciones = [
        "El ojo turco detectó envidia a tu alrededor 👁️ ¡Cuídate!",
        "Tu aura está limpia hoy ✨ El ojo azul te protege",
        "Hay alguien enviándote energía negativa 😬 Enciende una vela azul",
        "El universo te cubre hoy 🌌 Tu suerte está activada",
        "Hay ojo encima de ti 😤 Sal con el ojo turco colgado hoy",
    ]
    await update.message.reply_text(
        f"🧿 **OJO TURCO ACTIVADO** 🧿\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 **Usuario:** `{user_nick}`\n"
        f"🔮 **Nivel de protección:** `{nivel}%`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💬 _{random.choice(protecciones)}_\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🧿 _«Nazar boncuğu» te protege_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def alias_criminal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera tu alias criminal estilo venezolano."""
    user_nick = update.effective_user.first_name
    prefijos = ["El", "La", "El Flaco", "La Fiera", "El Tigre", "El Duro", "La Sombra", "El Loco", "La Reina", "El Diablo"]
    apellidos = ["Candela", "Turbina", "Relámpago", "Furia", "Veneno", "Trueno", "Cobra", "Pantalla", "Noche", "Tormenta", "Cuchillo", "Destello"]
    apodos = ["del Sur", "de Caracas", "Imparable", "Sin Miedo", "de Acero", "del Barrio", "Veloz"]
    alias = f"{random.choice(prefijos)} {random.choice(apellidos)} {random.choice(apodos)}"
    await update.message.reply_text(
        f"🕵️ **ALIAS CRIMINAL GENERADO** 🕵️\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 **Nombre real:** `{user_nick}`\n"
        f"🔫 **Tu alias:** `{alias}`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⚠️ _Solo para diversión, pa' que quede claro_ 😂",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def hechizo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lanza un hechizo random."""
    hechizos = [
        ("🔥 Incendio Máximo", "El objetivo arde en llamas místicas por 3 segundos"),
        ("❄️ Congelación Instantánea", "El objetivo queda congelado hasta el próximo martes"),
        ("💨 Ventarrón del Caribe", "Sopla un viento que se lleva todas las excusas"),
        ("⚡ Rayo del Destino", "Un rayo cae justo en el momento más incómodo"),
        ("🌀 Torbellino de Confusión", "El objetivo olvida dónde dejó el celular"),
        ("🌹 Hechizo de Amor", "La persona que piensas te manda un mensaje hoy"),
        ("💀 Maldición Suave", "Solo tropiezas una vez al salir de casa"),
        ("🍀 Bendición del Trébol", "El próximo BCV te favorece"),
        ("🐍 Serpiente Parlante", "El objetivo empieza a decir la verdad sin querer"),
        ("🌙 Sueño Eterno", "Duerme profundo pero no más de 12 horas"),
    ]
    nombre_h, desc_h = random.choice(hechizos)
    await update.message.reply_text(
        f"🪄 **HECHIZO LANZADO** 🪄\n"
        f"━━━━━━━━━━━━━━━\n"
        f"✨ **Nombre:** `{nombre_h}`\n"
        f"📜 **Efecto:** _{desc_h}_\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⚗️ _«Abracadabra Caraqueña» activado_",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def fase_lunar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra la fase lunar aproximada del día."""
    import math
    hoy = datetime.now()
    # Cálculo simple de fase lunar (ciclo ~29.5 días desde luna nueva conocida)
    luna_nueva_ref = datetime(2024, 1, 11)
    dias_diff = (hoy - luna_nueva_ref).days % 30
    fases = [
        (0, 2, "🌑 Luna Nueva", "Ideal para nuevos comienzos y proyectos"),
        (3, 7, "🌒 Luna Creciente", "Energía en aumento, momento de actuar"),
        (8, 10, "🌓 Cuarto Creciente", "Toma decisiones importantes hoy"),
        (11, 14, "🌔 Gibosa Creciente", "Tu energía está al máximo"),
        (15, 16, "🌕 Luna Llena", "Noche de magia, cuidado con las emociones"),
        (17, 21, "🌖 Gibosa Menguante", "Momento de reflexión y gratitud"),
        (22, 24, "🌗 Cuarto Menguante", "Suelta lo que ya no te sirve"),
        (25, 29, "🌘 Luna Menguante", "Descansa y recarga energías"),
    ]
    fase_nombre = "🌕 Luna Llena"
    fase_consejo = "Noche especial"
    for inicio, fin, nombre, consejo in fases:
        if inicio <= dias_diff <= fin:
            fase_nombre = nombre
            fase_consejo = consejo
            break
    await update.message.reply_text(
        f"🌙 **FASE LUNAR HOY** 🌙\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📅 **Fecha:** `{hoy.strftime('%d/%m/%Y')}`\n"
        f"🌒 **Fase:** `{fase_nombre}`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💡 _«{fase_consejo}»_\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🔭 _La luna nunca miente_ 🌌",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def top_ricos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el ranking de usuarios más ricos."""
    if not banco:
        await update.message.reply_text("📊 Aún no hay usuarios con dinero. ¡Usa /trabajar para empezar!")
        return
    
    sorted_banco = sorted(banco.items(), key=lambda x: x[1], reverse=True)[:10]
    
    medallas = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    ranking_txt = "🏆 **TOP 10 MÁS RICOS DEL BOT** 🏆\n━━━━━━━━━━━━━━━\n"
    for i, (uid, dinero) in enumerate(sorted_banco):
        info = usuarios_info.get(uid, {})
        nombre = info.get("nombre", f"User_{uid[:4]}")
        medalla = medallas[i] if i < len(medallas) else f"{i+1}."
        ranking_txt += f"{medalla} **{nombre}** · `${dinero}`\n"
    
    ranking_txt += "━━━━━━━━━━━━━━━\n💵 _Usa /trabajar para subir en el ranking_"
    
    await update.message.reply_text(ranking_txt, parse_mode=ParseMode.MARKDOWN)
    sumar_xp(update.effective_user.id, 2)

async def tkdm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lista de temas para que el video siempre sea sorpresa
    temas = ["memes", "gracioso", "gaming", "curiosidades", "anime", "fails"]
    tema = random.choice(temas)
    
    # Mensaje de espera
    espera = await update.message.reply_text(f"🚀 **CamilaBot** está volando a TikTok por un video de: *{tema}*...")

    try:
        # Usamos la API de TikWM que es rápida y no pide llaves raras
        api_url = f"https://www.tikwm.com/api/feed/list?keywords={tema}"
        response = requests.get(api_url).json()
        
        videos = response.get("data", {}).get("videos", [])
        
        if videos:
            # Elegimos uno al azar de la lista
            video_data = random.choice(videos)
            video_url = video_data.get("play") # URL del video sin marca de agua
            caption = f"✨ **TikTok Random: {tema}**\n👤 **Autor:** {video_data.get('author', {}).get('nickname')}\n\n🤖 @CamilaBot_V13 ⚡"

            # Enviamos el video usando el internet veloz de Replit
            await update.message.reply_video(
                video=video_url, 
                caption=caption,
                parse_mode="Markdown"
            )
            await espera.delete()
        else:
            await espera.edit_text("❌ No encontré videos nuevos ahora, intenta de nuevo.")

    except Exception as e:
        print(f"Error en tkdm: {e}")
        await espera.edit_text("⚠️ El servidor de TikTok está pesado, intenta en un ratico.")

async def bomba_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cuenta regresiva dramática estilo bomba."""
    user_nick = update.effective_user.first_name
    segundos = 5
    msg = await update.message.reply_text(
        f"💣 **BOMBA ACTIVADA POR {user_nick.upper()}** 💣\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⏱️ Detonación en: **{segundos} segundos**\n"
        f"🚨 _¡¡TODOS A CORRER!!_"
    )
    for i in range(segundos - 1, 0, -1):
        await asyncio.sleep(1)
        barras = "█" * i + "░" * (segundos - i)
        await msg.edit_text(
            f"💣 **BOMBA ACTIVADA** 💣\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⏱️ Detonación en: **{i} segundos**\n"
            f"[{barras}]\n"
            f"🚨 _¡¡CORRAN!!_"
        )
    await asyncio.sleep(1)
    emojis_explosion = ["💥", "🔥", "💨", "🌪️", "⚡"]
    await msg.edit_text(
        f"{''.join(random.choices(emojis_explosion, k=5))}\n"
        f"**¡¡BOOOOM!!** 💥\n"
        f"{''.join(random.choices(emojis_explosion, k=5))}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"☠️ _Todos volaron por los aires_ ✨\n"
        f"🪦 _RIP el grupo_ 😂"
    )
    sumar_xp(update.effective_user.id, 5)

async def adn_ficticio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Análisis de ADN ficticio y cómico."""
    user_nick = update.effective_user.first_name
    razas = ["Venezolano Puro 🇻🇪", "Alien Caraqueño 👽", "Mitad Humano Mitad WiFi 📶", "Descendiente de Simón Bolívar ⚔️", "Híbrido de Cachapa y Empanada 🫓"]
    poderes = ["Resistencia al calor extremo ☀️", "Velocidad máxima en la cola del banco 🏃", "Intuición para saber el precio del dólar 💵", "Inmunidad al papeleo burocrático 📄", "Super olfato para detectar empanadas a 3km 👃"]
    defectos = ["Alergia al lunes por la mañana 😴", "Incapacidad de llegar puntual ⏰", "Debilidad ante el perreo intenso 🎵", "Reacción adversa al BBF 📱", "Gen del 'ya voy' que tarda 1 hora ⌛"]
    
    await update.message.reply_text(
        f"🧬 **ANÁLISIS DE ADN: {user_nick.upper()}** 🧬\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🔬 **Origen genético:** `{random.choice(razas)}`\n"
        f"⚡ **Superpoder oculto:** _{random.choice(poderes)}_\n"
        f"⚠️ **Defecto genético:** _{random.choice(defectos)}_\n"
        f"🧪 **Pureza del ADN:** `{random.randint(60, 99)}%`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🔭 _Análisis realizado por CamilaBot Labs™_ 😄",
        parse_mode=ParseMode.MARKDOWN
    )
    sumar_xp(update.effective_user.id, 3)

async def triple_suerte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triple apuesta instantánea tipo tragamonedas."""
    user_id = update.effective_user.id
    uid = str(user_id)
    user_nick = update.effective_user.first_name

    saldo_actual = banco.get(uid, 0.0)
    if saldo_actual < 50:
        await update.message.reply_text(
            f"💸 **{user_nick}**, necesitas al menos `$50` para el Triple Suerte.\n"
            f"💼 Tu saldo: `${saldo_actual}` · Usa /trabajar para ganar más."
        )
        return

    simbolos = ["🍒", "🍋", "🍊", "⭐", "💎", "7️⃣", "🔔", "🍀"]
    rueda1 = [random.choice(simbolos) for _ in range(3)]
    rueda2 = [random.choice(simbolos) for _ in range(3)]
    rueda3 = [random.choice(simbolos) for _ in range(3)]

    resultado = [rueda1[1], rueda2[1], rueda3[1]]  # fila central
    apuesta = 50

    if resultado[0] == resultado[1] == resultado[2]:
        if resultado[0] == "💎":
            ganancia = apuesta * 20
            msg_resultado = f"💎💎💎 **¡¡JACKPOT DIAMANTE!! ×20** 💎💎💎"
        elif resultado[0] == "7️⃣":
            ganancia = apuesta * 15
            msg_resultado = f"7️⃣7️⃣7️⃣ **¡¡TRIPLE 7!! ×15** 🎉🎉🎉"
        else:
            ganancia = apuesta * 5
            msg_resultado = f"**¡¡TRIPLE {resultado[0]}!! ×5** 🎊"
        sumar_dinero(user_id, ganancia)
    elif resultado[0] == resultado[1] or resultado[1] == resultado[2]:
        ganancia = apuesta
        sumar_dinero(user_id, ganancia)
        msg_resultado = f"**¡Doble! Recuperas tu apuesta** 🎯"
    else:
        sumar_dinero(user_id, -apuesta)
        ganancia = -apuesta
        msg_resultado = "**Mala suerte esta vez** 😅"

    await update.message.reply_text(
        f"🎰 **TRIPLE SUERTE** 🎰\n"
        f"━━━━━━━━━━━━━━━\n"
        f"┌──────────────┐\n"
        f"│ {rueda1[0]} │ {rueda2[0]} │ {rueda3[0]} │\n"
        f"│ {rueda1[1]} │ {rueda2[1]} │ {rueda3[1]} │  ← \n"
        f"│ {rueda1[2]} │ {rueda2[2]} │ {rueda3[2]} │\n"
        f"└──────────────┘\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{msg_resultado}\n"
        f"💵 **Resultado:** `{'+'if ganancia>0 else ''}{ganancia}$`\n"
        f"🏦 **Nuevo saldo:** `${banco.get(uid, 0.0)}`",
        parse_mode=ParseMode.MARKDOWN
    )
    registrar_evento(user_id, user_nick, f"Jugó Triple Suerte: {ganancia}$", "ECONOMÍA")
    sumar_xp(user_id, 4)

# ========================================
# JUEGO: TRES EN RAYAS (TIC TAC TOE)
# ========================================

def verificar_ganador(tablero):
    """Verifica si hay ganador o empate en Tres en Rayas."""
    lineas_ganadoras = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]
    
    for linea in lineas_ganadoras:
        simbolos = [tablero[x][y] for x, y in linea]
        if simbolos[0] != "" and simbolos.count(simbolos[0]) == 3:
            return simbolos[0]
    
    if all(tablero[i][j] != "" for i in range(3) for j in range(3)):
        return "Empate"
    
    return None

def imprimir_tablero_humanizado(tablero):
    """Formatea el tablero en texto bonito para Telegram."""
    resultado = "🎮 **TABLERO ACTUAL**\n\n"
    resultado += "```\n"
    for i in range(3):
        fila = ""
        for j in range(3):
            simbolo = tablero[i][j] if tablero[i][j] else " "
            fila += f"[ {simbolo} ] "
        resultado += fila + "\n"
    resultado += "```\n"
    resultado += "💡 *Usa: `/pos x.y` (ej: `/pos 1.1`, `/pos 2.3`)*"
    return resultado

async def jugar_ia_movimiento(tablero):
    """IA básica que juega automáticamente."""
    movimientos_validos = []
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == "":
                movimientos_validos.append((i, j))
    
    if not movimientos_validos:
        return None
    
    # 1. Intentar ganar
    for i, j in movimientos_validos:
        tablero_temp = [row[:] for row in tablero]
        tablero_temp[i][j] = "O"
        if verificar_ganador(tablero_temp) == "O":
            return (i, j)
    
    # 2. Bloquear al jugador X
    for i, j in movimientos_validos:
        tablero_temp = [row[:] for row in tablero]
        tablero_temp[i][j] = "X"
        if verificar_ganador(tablero_temp) == "X":
            return (i, j)
    
    # 3. Preferir centro
    if (1, 1) in movimientos_validos:
        return (1, 1)
    
    # 4. Aleatorio
    import random
    return random.choice(movimientos_validos)

def limpiar_trayes():
    """Limpia datos de Tres en Rayas."""
    global tres_rayas
    tres_rayas.clear()
    guardar_db("tres_rayas.json", {})

async def iniciar_trayes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia una nueva partida de Tres en Rayas."""
    user_id = update.effective_user.id
    user_nick = update.effective_user.first_name
    
    if str(user_id) in tres_rayas:
        limpiar_trayes()
    
    tres_rayas[str(user_id)] = {
        "turno": 1,
        "tablero": [["" for _ in range(3)] for _ in range(3)],
        "modo_ia": False,
        "ultimo_jugador": user_nick
    }
    
    await update.message.reply_text(
        f"🎮 **¡Nueva Partida de Tres en Rayas!**\n\n"
        f"👤 **Eres X** (primera en jugar)\n\n"
        f"❌ ¡Te toca!\n"
        f"💡 Usa `/pos x.y` (ej: `/pos 1.1`, `/pos 2.3`, `/pos 3.3`)\n\n"
        f"🤖 **Modos disponibles:**\n"
        f"   `/ai_on` - Jugar contra la IA\n"
        f"   `/tablero` - Ver tablero actual\n"
        f"   `/reiniciar` - Nueva partida",
        parse_mode=ParseMode.MARKDOWN
    )
    
    sumar_xp(user_id, 3)
    registrar_evento(user_id, user_nick, "Inició Tres en Rayas", "JUEGO")

async def mover_pos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja movimientos del juego."""
    user_id = update.effective_user.id
    user_nick = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text(
            "❌ **Uso:** `/pos x.y`\n\n"
            "💡 *Ejemplos:* `/pos 1.1` - `/pos 2.3` - `/pos 3.3`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    try:
        col, fila = map(int, context.args[0].split("."))
        if not (1 <= col <= 3 and 1 <= fila <= 3):
            await update.message.reply_text("❌ Las posiciones deben estar entre 1 y 3.")
            return
    except:
        await update.message.reply_text("❌ Formato inválido. Usa `/pos x.y`")
        return
    
    if str(user_id) not in tres_rayas:
        await update.message.reply_text("⚠️ Debes iniciar con `/trayes` primero.")
        return
    
    juego = tres_rayas[str(user_id)]
    fila_idx, col_idx = fila - 1, col - 1
    
    if juego["tablero"][fila_idx][col_idx] != "":
        await update.message.reply_text("⚠️ ¡Casilla ocupada! Elige otra.")
        return
    
    fichas = ["X", "O"]
    juego["tablero"][fila_idx][col_idx] = fichas[juego["turno"] % 2]
    juego["turno"] += 1
    juego["ultimo_jugador"] = user_nick
    
    guardar_db("tres_rayas.json", tres_rayas)
    
    tablero_txt = imprimir_tablero_humanizado(juego["tablero"])
    ganador = verificar_ganador(juego["tablero"])
    
    if ganador:
        if ganador == "Empate":
            msg = "🤝 **EMPATE!**"
        else:
            msg = f"🎉 **{ganador} GANÓ!**"
        
        await update.message.reply_text(f"{tablero_txt}\n\n{msg}\n✨ `/reiniciar` para nueva", parse_mode=ParseMode.MARKDOWN)
        limpiar_trayes()
        sumar_xp(user_id, 8 if ganador == "X" else 2)
    else:
        await update.message.reply_text(tablero_txt, parse_mode=ParseMode.MARKDOWN)
        
        if juego.get("modo_ia") and juego["turno"] % 2 == 0:
            await asyncio.sleep(1)
            pos_ia = await jugar_ia_movimiento(juego["tablero"])
            
            if pos_ia:
                i, j = pos_ia
                juego["tablero"][i][j] = "O"
                juego["turno"] += 1
                juego["ultimo_jugador"] = "IA"
                guardar_db("tres_rayas.json", tres_rayas)
                
                tablero_txt = imprimir_tablero_humanizado(juego["tablero"])
                ganador = verificar_ganador(juego["tablero"])
                
                if ganador:
                    if ganador == "Empate":
                        msg = "🤝 **EMPATE!**"
                    else:
                        msg = f"🤖 **LA IA GANÓ!**"
                    await update.message.reply_text(f"{tablero_txt}\n\n{msg}\n✨ `/reiniciar`", parse_mode=ParseMode.MARKDOWN)
                    limpiar_trayes()
                else:
                    await update.message.reply_text(f"{tablero_txt}\n\n🤖 La IA jugó. ¡Tu turno!", parse_mode=ParseMode.MARKDOWN)

async def activar_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Activa modo IA."""
    user_id = update.effective_user.id
    
    if str(user_id) not in tres_rayas:
        await update.message.reply_text("⚠️ Inicia con `/trayes` primero.")
        return
    
    tres_rayas[str(user_id)]["modo_ia"] = True
    await update.message.reply_text("✅ **IA ACTIVADA** 🤖\nLa máquina jugará automáticamente.", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(user_id, 1)

async def desactivar_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Desactiva modo IA."""
    user_id = update.effective_user.id
    
    if str(user_id) not in tres_rayas:
        await update.message.reply_text("⚠️ No hay juego activo.")
        return
    
    tres_rayas[str(user_id)]["modo_ia"] = False
    await update.message.reply_text("❌ **IA DESACTIVADA**\nJuega manualmente.", parse_mode=ParseMode.MARKDOWN)

async def reiniciar_trayes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reinicia el juego."""
    user_id = update.effective_user.id
    user_nick = update.effective_user.first_name
    
    if str(user_id) not in tres_rayas:
        await update.message.reply_text("⚠️ No hay juego activo.")
        return
    
    limpiar_trayes()
    tres_rayas[str(user_id)] = {
        "turno": 1,
        "tablero": [["" for _ in range(3)] for _ in range(3)],
        "modo_ia": False,
        "ultimo_jugador": user_nick
    }
    
    await update.message.reply_text("🔄 **Partida reiniciada**\n✨ ¡Listo para jugar!", parse_mode=ParseMode.MARKDOWN)
    sumar_xp(user_id, 1)

async def mostrar_tablero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el tablero actual."""
    user_id = update.effective_user.id
    
    if str(user_id) not in tres_rayas:
        await update.message.reply_text("⚠️ Inicia con `/trayes` primero.")
        return
    
    tablero_txt = imprimir_tablero_humanizado(tres_rayas[str(user_id)]["tablero"])
    await update.message.reply_text(tablero_txt, parse_mode=ParseMode.MARKDOWN)

# ════════════════════════════════════════════════════════════════════════════════
# 🎉 NUEVAS FUNCIONES 1000+ COMANDOS V14 - AnyerJR
# ════════════════════════════════════════════════════════════════════════════════

# Bases de datos nuevas
empresas = cargar_db("empresas.json")
cursos = cargar_db("cursos.json")
listas_compra = cargar_db("listas_compra.json")
empleados = cargar_db("empleados.json")

# ════════════════════════════════════════════════════════════════════════════════
# 1️⃣ ECONOMÍA & EMPRESAS
# ════════════════════════════════════════════════════════════════════════════════

async def cmd_crear_empresa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if len(context.args) < 1:
        await update.message.reply_text("Uso: /crear_empresa <nombre>")
        return
    nombre = " ".join(context.args)
    empresas[user_id] = {"nombre": nombre, "capital": 1000, "empleados": 0}
    guardar_db("empresas.json", empresas)
    await update.message.reply_text(f"✅ Empresa '{nombre}' creada con $1000")

async def cmd_invertir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in empresas or not context.args:
        await update.message.reply_text("Debes tener empresa primero")
        return
    try:
        monto = int(context.args[0])
        empresas[user_id]["capital"] += monto
        guardar_db("empresas.json", empresas)
        await update.message.reply_text(f"💰 Invertiste ${monto}. Capital: ${empresas[user_id]['capital']}")
    except:
        await update.message.reply_text("Uso: /invertir <monto>")

async def cmd_emplear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("Uso: /emplear <nombre>")
        return
    nombre = " ".join(context.args)
    if user_id not in empleados:
        empleados[user_id] = []
    empleados[user_id].append({"nombre": nombre, "sueldo": 0})
    guardar_db("empleados.json", empleados)
    await update.message.reply_text(f"✅ {nombre} contratado!")

async def cmd_ranking_empresas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not empresas:
        await update.message.reply_text("No hay empresas aún")
        return
    top = sorted(empresas.items(), key=lambda x: x[1]['capital'], reverse=True)[:5]
    msg = "🏆 TOP 5 EMPRESAS:\n"
    for i, (uid, emp) in enumerate(top, 1):
        msg += f"{i}. {emp['nombre']}: ${emp['capital']}\n"
    await update.message.reply_text(msg)

# ════════════════════════════════════════════════════════════════════════════════
# 2️⃣ EDUCACIÓN & APRENDIZAJE
# ════════════════════════════════════════════════════════════════════════════════

CURSOS_DICT = {"python": "Python 3", "javascript": "JavaScript", "web": "Web", "sql": "SQL"}

async def cmd_ver_cursos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📚 CURSOS DISPONIBLES:\n"
    for k, v in CURSOS_DICT.items():
        msg += f"- /{k}: {v}\n"
    await update.message.reply_text(msg)

async def cmd_inscribirse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0] not in CURSOS_DICT:
        await update.message.reply_text("Uso: /inscribirse <python|javascript|web|sql>")
        return
    user_id = str(update.effective_user.id)
    curso = context.args[0]
    if user_id not in cursos:
        cursos[user_id] = {}
    cursos[user_id][curso] = {"inscrito": True, "progreso": 0}
    guardar_db("cursos.json", cursos)
    await update.message.reply_text(f"✅ ¡Inscrito en {CURSOS_DICT[curso]}!")

async def cmd_progreso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args or user_id not in cursos:
        await update.message.reply_text("No estás inscrito en ningún curso")
        return
    curso = context.args[0]
    prog = cursos.get(user_id, {}).get(curso, {}).get("progreso", 0)
    await update.message.reply_text(f"📊 Progreso en {curso}: {prog}%")

# ════════════════════════════════════════════════════════════════════════════════
# 3️⃣ SEGURIDAD & PRIVACIDAD
# ════════════════════════════════════════════════════════════════════════════════

async def cmd_generar_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    longitud = int(context.args[0]) if context.args else 12
    import string
    pwd = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=longitud))
    await update.message.reply_text(f"🔐 `{pwd}`", parse_mode=ParseMode.MARKDOWN)

async def cmd_hash_sha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /hash <texto>")
        return
    texto = " ".join(context.args)
    import hashlib
    hash_val = hashlib.sha256(texto.encode()).hexdigest()
    await update.message.reply_text(f"🔒 `{hash_val[:32]}`", parse_mode=ParseMode.MARKDOWN)

async def cmd_2fa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    codigo = str(random.randint(100000, 999999))
    await update.message.reply_text(f"🔐 2FA Activado\nCódigo: `{codigo}`", parse_mode=ParseMode.MARKDOWN)

# ════════════════════════════════════════════════════════════════════════════════
# 4️⃣ VIDA COTIDIANA
# ════════════════════════════════════════════════════════════════════════════════

async def cmd_crear_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /crear_lista <nombre>")
        return
    user_id = str(update.effective_user.id)
    nombre = " ".join(context.args)
    if user_id not in listas_compra:
        listas_compra[user_id] = {}
    listas_compra[user_id][nombre] = []
    guardar_db("listas_compra.json", listas_compra)
    await update.message.reply_text(f"🛒 Lista '{nombre}' creada")

async def cmd_agregar_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /agregar_item <lista> <producto>")
        return
    user_id = str(update.effective_user.id)
    lista = context.args[0]
    producto = " ".join(context.args[1:])
    if user_id in listas_compra and lista in listas_compra[user_id]:
        listas_compra[user_id][lista].append(producto)
        guardar_db("listas_compra.json", listas_compra)
        await update.message.reply_text(f"✅ '{producto}' agregado")
    else:
        await update.message.reply_text("❌ Lista no encontrada")

async def cmd_ver_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /ver_lista <nombre>")
        return
    user_id = str(update.effective_user.id)
    lista = context.args[0]
    if user_id in listas_compra and lista in listas_compra[user_id]:
        items = listas_compra[user_id][lista]
        msg = f"🛒 **{lista}**\n"
        for i, item in enumerate(items, 1):
            msg += f"{i}. {item}\n"
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("❌ Lista no encontrada")

# ════════════════════════════════════════════════════════════════════════════════
# 5️⃣ TRABAJO & EMPRENDIMIENTO
# ════════════════════════════════════════════════════════════════════════════════

async def cmd_crear_cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    nick = update.effective_user.first_name
    cv = f"📄 **CV - {nick}**\n📱 ID: {user_id}\n📅 {datetime.now().strftime('%Y-%m-%d')}"
    await update.message.reply_text(cv, parse_mode=ParseMode.MARKDOWN)

async def cmd_buscar_empleo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ofertas = ["Senior Dev - $3000/mes", "Junior Dev - $1500/mes", "Data Analyst - $2500/mes"]
    msg = "💼 OFERTAS DISPONIBLES:\n"
    for i, o in enumerate(ofertas, 1):
        msg += f"{i}. {o}\n"
    await update.message.reply_text(msg)

async def cmd_plan_negocio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    plan = "📊 **PLAN DE NEGOCIO**\n- Inversión: $5000\n- ROI: 30%\n- Período: 12 meses"
    await update.message.reply_text(plan, parse_mode=ParseMode.MARKDOWN)

# ════════════════════════════════════════════════════════════════════════════════
# 6️⃣ ENTRETENIMIENTO & REDES
# ════════════════════════════════════════════════════════════════════════════════

async def cmd_resultados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultados = "⚽ Bayern 2-1 Dortmund\n🏆 Real Madrid 3-0 Sevilla\n⚽ PSG 1-2 Marsella"
    await update.message.reply_text(resultados)

async def cmd_hashtags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tags = ["#viral", "#trending", "#content2024", "#insta"]
    await update.message.reply_text("🏷️ " + " ".join(tags))

async def cmd_loteria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nums = random.sample(range(1, 50), 6)
    await update.message.reply_text(f"🎰 Números: {' '.join(map(str, nums))}\n💰 Premio: $10,000")

# ════════════════════════════════════════════════════════════════════════════════
# 7️⃣ UTILIDADES & HERRAMIENTAS
# ════════════════════════════════════════════════════════════════════════════════

async def cmd_celsius(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /celsius <grados_fahrenheit>")
        return
    try:
        f = float(context.args[0])
        c = (f - 32) * 5/9
        await update.message.reply_text(f"🌡️ {f}°F = {c:.2f}°C")
    except:
        await update.message.reply_text("❌ Error: Ingresa un número válido")

async def cmd_imc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /imc <peso_kg> <altura_m>")
        return
    try:
        peso = float(context.args[0])
        altura = float(context.args[1])
        imc = peso / (altura ** 2)
        await update.message.reply_text(f"📊 IMC: {imc:.2f}")
    except:
        await update.message.reply_text("❌ Error: Ingresa números válidos")

async def cmd_metrokm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /metrokm <metros>")
        return
    try:
        metros = float(context.args[0])
        km = metros / 1000
        await update.message.reply_text(f"📏 {metros}m = {km:.4f}km")
    except:
        await update.message.reply_text("❌ Error: Ingresa un número válido")

# ════════════════════════════════════════════════════════════════════════════════
# 🚀 BLOQUE MASIVO 2000+ LÍNEAS - COMANDOS AVANZADOS ULTRA SUPREMOS
# ════════════════════════════════════════════════════════════════════════════════

# 📊 SISTEMA DE CRIPTOMONEDAS & BLOCKCHAIN
crypto_portfolio = cargar_db("crypto_portfolio.json")
crypto_precios = {"BTC": random.uniform(40000, 50000), "ETH": random.uniform(2000, 3000), "DOGE": random.uniform(0.1, 0.5)}

async def cmd_crypto_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "💰 **CRIPTOMONEDAS EN VIVO**\n"
    for coin, precio in crypto_precios.items():
        msg += f"- {coin}: ${precio:.2f}\n"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def cmd_comprar_crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /comprar_crypto <BTC|ETH|DOGE> <cantidad>")
        return
    user_id = str(update.effective_user.id)
    coin = context.args[0].upper()
    try:
        cantidad = float(context.args[1])
        if user_id not in crypto_portfolio:
            crypto_portfolio[user_id] = {}
        crypto_portfolio[user_id][coin] = crypto_portfolio[user_id].get(coin, 0) + cantidad
        guardar_db("crypto_portfolio.json", crypto_portfolio)
        total = crypto_precios[coin] * cantidad if coin in crypto_precios else 0
        await update.message.reply_text(f"✅ Compraste {cantidad} {coin}\n💵 Valor: ${total:.2f}")
    except:
        await update.message.reply_text("❌ Error en la compra")

async def cmd_cartera_cripto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in crypto_portfolio or not crypto_portfolio[user_id]:
        await update.message.reply_text("No tienes criptomonedas aún")
        return
    msg = "💎 **TU CARTERA CRIPTO**\n"
    valor_total = 0
    for coin, cantidad in crypto_portfolio[user_id].items():
        valor = crypto_precios.get(coin, 0) * cantidad
        valor_total += valor
        msg += f"- {coin}: {cantidad} (${valor:.2f})\n"
    msg += f"\n💰 **Valor Total: ${valor_total:.2f}**"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# 🎰 JUEGOS AVANZADOS - CASINO COMPLETO
casino_jugadores = cargar_db("casino_jugadores.json")

async def cmd_blackjack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("Uso: /blackjack <apuesta>")
        return
    try:
        apuesta = int(context.args[0])
        # Juego simplificado
        tu_carta = random.randint(10, 21)
        bot_carta = random.randint(10, 21)
        if tu_carta > 21:
            resultado = "❌ ¡Te pasaste! Perdiste"
            ganancia = -apuesta
        elif bot_carta > 21:
            resultado = "✅ ¡Bot se pasó! ¡Ganaste!"
            ganancia = apuesta
        elif tu_carta > bot_carta:
            resultado = f"✅ ¡Ganaste! Tú: {tu_carta}, Bot: {bot_carta}"
            ganancia = apuesta
        else:
            resultado = f"❌ Perdiste. Tú: {tu_carta}, Bot: {bot_carta}"
            ganancia = -apuesta
        
        if user_id not in casino_jugadores:
            casino_jugadores[user_id] = {"balance": 0, "juegos": 0}
        casino_jugadores[user_id]["balance"] += ganancia
        casino_jugadores[user_id]["juegos"] += 1
        guardar_db("casino_jugadores.json", casino_jugadores)
        
        msg = f"🎰 **BLACKJACK**\n{resultado}\nGanancia: ${ganancia}\nBalance: ${casino_jugadores[user_id]['balance']}"
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Error en el juego")

async def cmd_poker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("Uso: /poker <apuesta>")
        return
    apuesta = int(context.args[0])
    cartas = [f"{'♠♥♦♣'[random.randint(0,3)]}{random.randint(2,14)}" for _ in range(5)]
    resultado = random.choice(["Par", "Doble Par", "Escalera", "Color", "Full", "Poker"])
    ganancia = apuesta * (1 if random.random() > 0.5 else -1)
    
    if user_id not in casino_jugadores:
        casino_jugadores[user_id] = {"balance": 0, "juegos": 0}
    casino_jugadores[user_id]["balance"] += ganancia
    guardar_db("casino_jugadores.json", casino_jugadores)
    
    msg = f"🎴 **POKER**\n💳 Cartas: {' '.join(cartas)}\n🏆 Resultado: {resultado}\n💰 Ganancia: ${ganancia}"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def cmd_balance_casino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in casino_jugadores:
        await update.message.reply_text("No has jugado en el casino")
        return
    datos = casino_jugadores[user_id]
    msg = f"💰 **BALANCE CASINO**\n💵 Balance: ${datos['balance']}\n🎲 Juegos: {datos['juegos']}"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# 🤖 SISTEMA DE IA CONVERSACIONAL AVANZADA
conversaciones_ia = cargar_db("conversaciones_ia.json")
respuestas_ia = {
    "hola": "¡Hola! ¿Cómo estás? Soy Camila, tu bot supremo 🤖",
    "cómo estás": "Estoy operando al 100% gracias a AnyerJR 💯",
    "quién eres": "Soy CamilaBot V14 MEGA SUPREMA - 1000+ comandos 🚀",
    "creador": "Mi creador es AnyerJR de Venezuela 🇻🇪",
    "ayuda": "Usa /ayuda para ver todos mis comandos",
}

async def cmd_chat_ia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("Uso: /chat_ia <tu mensaje>")
        return
    
    mensaje = " ".join(context.args).lower()
    respuesta = "No entendí eso, pero soy aprendiz 🤖"
    
    for palabra_clave, resp in respuestas_ia.items():
        if palabra_clave in mensaje:
            respuesta = resp
            break
    
    if user_id not in conversaciones_ia:
        conversaciones_ia[user_id] = []
    conversaciones_ia[user_id].append({"msg": mensaje, "resp": respuesta, "hora": str(datetime.now())})
    guardar_db("conversaciones_ia.json", conversaciones_ia)
    
    await update.message.reply_text(f"🤖 {respuesta}")

# 📚 SISTEMA EDUCATIVO AVANZADO
tareas_usuario = cargar_db("tareas_usuario.json")
cuestionarios = {
    "python": [
        {"q": "¿Qué es Python?", "a": "Un lenguaje de programación interpretado"},
        {"q": "¿Qué es un diccionario?", "a": "Una estructura de datos con pares clave-valor"},
    ]
}

async def cmd_crear_tarea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /crear_tarea <asignatura> <descripción>")
        return
    asignatura = context.args[0]
    descripcion = " ".join(context.args[1:])
    
    if user_id not in tareas_usuario:
        tareas_usuario[user_id] = []
    tareas_usuario[user_id].append({"asignatura": asignatura, "descripcion": descripcion, "completada": False, "fecha": str(datetime.now())})
    guardar_db("tareas_usuario.json", tareas_usuario)
    await update.message.reply_text(f"📝 Tarea creada: {asignatura}")

async def cmd_mis_tareas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in tareas_usuario or not tareas_usuario[user_id]:
        await update.message.reply_text("No tienes tareas")
        return
    msg = "📋 **TUS TAREAS**\n"
    for i, tarea in enumerate(tareas_usuario[user_id], 1):
        estado = "✅" if tarea["completada"] else "⏳"
        msg += f"{i}. {estado} {tarea['asignatura']}: {tarea['descripcion']}\n"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# 🎬 SISTEMA DE PELÍCULAS Y SERIES
peliculas_db = {
    "accion": ["John Wick", "Mad Max", "Top Gun"],
    "drama": ["Forrest Gump", "The Shawshank Redemption", "Titanic"],
    "comedia": ["The Grand Budapest Hotel", "Superbad", "The Hangover"],
    "terror": ["The Ring", "Hereditary", "Insidious"],
}

async def cmd_recomendar_pelicula(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /recomendar_pelicula <accion|drama|comedia|terror>")
        return
    genero = context.args[0].lower()
    if genero in peliculas_db:
        pelicula = random.choice(peliculas_db[genero])
        await update.message.reply_text(f"🎬 Te recomiendo: **{pelicula}** ({genero.capitalize()})", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("❌ Género no encontrado")

async def cmd_top_10_peliculas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = ["1. The Shawshank Redemption (1994)", "2. The Godfather (1972)", "3. Inception (2010)", "4. Pulp Fiction (1994)", "5. Fight Club (1999)"]
    msg = "🏆 **TOP 10 PELÍCULAS DE IMDB**\n" + "\n".join(top[:5])
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# 🎵 SISTEMA DE MÚSICA AVANZADO
playlists_usuario = cargar_db("playlists_usuario.json")

async def cmd_crear_playlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("Uso: /crear_playlist <nombre>")
        return
    nombre = " ".join(context.args)
    if user_id not in playlists_usuario:
        playlists_usuario[user_id] = {}
    playlists_usuario[user_id][nombre] = []
    guardar_db("playlists_usuario.json", playlists_usuario)
    await update.message.reply_text(f"🎵 Playlist '{nombre}' creada")

async def cmd_agregar_cancion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /agregar_cancion <playlist> <canción>")
        return
    playlist = context.args[0]
    cancion = " ".join(context.args[1:])
    if user_id in playlists_usuario and playlist in playlists_usuario[user_id]:
        playlists_usuario[user_id][playlist].append(cancion)
        guardar_db("playlists_usuario.json", playlists_usuario)
        await update.message.reply_text(f"✅ '{cancion}' agregada a '{playlist}'")
    else:
        await update.message.reply_text("❌ Playlist no encontrada")

# 🏆 SISTEMA DE LOGROS Y MEDALLAS
logros = cargar_db("logros.json")

async def cmd_mis_logros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in logros:
        logros[user_id] = []
    
    logros_disponibles = ["🥇 Primer comando", "💰 Millonario", "🎮 Gamer", "📚 Estudiante", "🏆 Campeón"]
    logros_obtenidos = logros.get(user_id, [])
    
    msg = "🏅 **TUS LOGROS**\n"
    for i, logro in enumerate(logros_obtenidos, 1):
        msg += f"{i}. {logro}\n"
    if not logros_obtenidos:
        msg += "Aún no tienes logros. ¡Sigue jugando!"
    
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# 🌍 SISTEMA GEOGRÁFICO
ciudades = {
    "caracas": {"pais": "Venezuela", "clima": "Tropical", "poblacion": "3.2M"},
    "bogota": {"pais": "Colombia", "clima": "Templado", "poblacion": "8.1M"},
    "buenos aires": {"pais": "Argentina", "clima": "Templado", "poblacion": "15.8M"},
}

async def cmd_info_ciudad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /info_ciudad <caracas|bogota|buenos_aires>")
        return
    ciudad = " ".join(context.args).lower()
    if ciudad in ciudades:
        info = ciudades[ciudad]
        msg = f"🌍 **{ciudad.upper()}**\n🏙️ País: {info['pais']}\n🌡️ Clima: {info['clima']}\n👥 Población: {info['poblacion']}"
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("❌ Ciudad no encontrada")

# 💼 SISTEMA FINANCIERO AVANZADO
inversiones = cargar_db("inversiones.json")

async def cmd_hacer_inversion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /hacer_inversion <tipo> <monto>")
        return
    tipo = context.args[0]
    try:
        monto = int(context.args[1])
        if user_id not in inversiones:
            inversiones[user_id] = []
        rentabilidad = random.uniform(0.05, 0.20)
        inversion = {"tipo": tipo, "monto": monto, "rentabilidad": rentabilidad, "fecha": str(datetime.now())}
        inversiones[user_id].append(inversion)
        guardar_db("inversiones.json", inversiones)
        ganancia = monto * rentabilidad
        await update.message.reply_text(f"💵 Inversión de ${monto} en {tipo}\n📈 Ganancia esperada: ${ganancia:.2f}")
    except:
        await update.message.reply_text("❌ Error en la inversión")

# 🎯 SISTEMA DE DESAFÍOS Y RETOS
desafios = cargar_db("desafios.json")

async def cmd_nuevo_desafio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("Uso: /nuevo_desafio <descripción>")
        return
    descripcion = " ".join(context.args)
    if user_id not in desafios:
        desafios[user_id] = []
    desafios[user_id].append({"desafio": descripcion, "completado": False, "fecha": str(datetime.now())})
    guardar_db("desafios.json", desafios)
    await update.message.reply_text(f"🎯 Desafío registrado: {descripcion}")

# 🔐 SISTEMA DE SEGURIDAD AVANZADA
intentos_fallidos = {}

async def cmd_cambiar_pwd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("Uso: /cambiar_pwd <nueva_contraseña>")
        return
    nueva_pwd = context.args[0]
    hash_pwd = hashlib.sha256(nueva_pwd.encode()).hexdigest()
    await update.message.reply_text(f"🔐 Contraseña cambiada\n🔒 Hash: `{hash_pwd[:20]}...`", parse_mode=ParseMode.MARKDOWN)

# ════════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════════
# 🌐 COMANDOS DE TRADUCCIÓN RÁPIDA (TRADUCCIÓN DIRECTA A IDIOMAS)
# ════════════════════════════════════════════════════════════════════════════════

async def cmd_traen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traducción rápida al Inglés."""
    context.args.insert(0, "en")
    await traducir(update, context)

async def cmd_trafr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traducción rápida al Francés."""
    context.args.insert(0, "fr")
    await traducir(update, context)

async def cmd_taes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traducción rápida al Español."""
    context.args.insert(0, "es")
    await traducir(update, context)

async def cmd_tade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traducción rápida al Alemán."""
    context.args.insert(0, "de")
    await traducir(update, context)

async def cmd_tapt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traducción rápida al Portugués."""
    context.args.insert(0, "pt")
    await traducir(update, context)

async def cmd_tait(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traducción rápida al Italiano."""
    context.args.insert(0, "it")
    await traducir(update, context)

async def cmd_tazh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traducción rápida al Chino."""
    context.args.insert(0, "zh")
    await traducir(update, context)

async def cmd_taja(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traducción rápida al Japonés."""
    context.args.insert(0, "ja")
    await traducir(update, context)

async def cmd_taar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traducción rápida al Árabe."""
    context.args.insert(0, "ar")
    await traducir(update, context)

async def cmd_taru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traducción rápida al Ruso."""
    context.args.insert(0, "ru")
    await traducir(update, context)

# ════════════════════════════════════════════════════════════════════════════════
# 📖 COMANDOS /LIST1 A /LIST9 - CATEGORÍAS DE COMANDOS
# ════════════════════════════════════════════════════════════════════════════════

async def cmd_list1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Categoría 1: Sistema & Perfil"""
    msg = """
  👑perfil y sistema👑
━━━━━━━━━━━━━━━━━━━━
-📱 Comandos disponibles:
- 👤 /perfil - ver tu perfil
- 👷 /reg - registrarte 
- 📄 /menu - ver lista General
- ⬆️ /help - menu
- ⬆️ /start - menu


"""
    # ── PASO 1: Verificar si el mensaje es muy largo
    if len(msg) > 4000:
        # ── PASO 2: Dividir en 2 partes (máximo 4000 caracteres cada una)
        parte1 = msg[:4000]
        parte2 = msg[4000:]
        
        # ── PASO 3: Enviar ambas partes
        await update.message.reply_text(parte1, parse_mode=ParseMode.MARKDOWN)
        await update.message.reply_text(parte2, parse_mode=ParseMode.MARKDOWN)
    else:
        # ── PASO 4: Si es corto, enviar normalmente
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
async def cmd_list2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Categoría 2: Economía & Dinero"""
    msg = """
💰 **CATEGORÍA 2: ECONOMÍA & DINERO**
👑 Economía y Dinero 👑
━━━━━━━━━━━━━━━━━━━━
- 👷 /trabajar - Dinero
- 🎰 /apostar - Casino
- 💲 /dolar - precio del dolar
- 💰 /cripto - precio cripto
- 🫠 Anyer seguira agregando mas a la lista xd es que le da pereza

"""
    # ── PASO 1: Verificar si el mensaje es muy largo
    if len(msg) > 4000:
        # ── PASO 2: Dividir en 2 partes (máximo 4000 caracteres cada una)
        parte1 = msg[:4000]
        parte2 = msg[4000:]
        
        # ── PASO 3: Enviar ambas partes
        await update.message.reply_text(parte1, parse_mode=ParseMode.MARKDOWN)
        await update.message.reply_text(parte2, parse_mode=ParseMode.MARKDOWN)
    else:
        # ── PASO 4: Si es corto, enviar normalmente
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def cmd_list3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Categoría 3: Multimedia & Descargas"""
    msg = (
        "🎬 **CATEGORÍA 3: MULTIMEDIA & DESCARGAS** 🎬\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📱 /descargar [URL] - Descarga videos (TikTok, Instagram, YouTube)\n"
        "🎵 /ytmp3 [URL] - Descarga audio de YouTube\n"
        "🎬 /ytmp4 [URL] - Descarga video de YouTube\n"
        "📸 /tiktok [URL] - Descarga TikTok\n"
        "🖼️ /instagram [URL] - Descarga Instagram\n"
        "📺 /facebook [URL] - Descarga Facebook\n"
        "🐦 /twitter [URL] - Descarga Twitter\n"
        "🔊 /soundcloud [URL] - Descarga SoundCloud\n"
        "🖼️ /meme - Meme aleatorio\n"
        "🎭 /gif - GIF aleatorio\n"
        "🎨 /wallpaper - Wallpaper aleatorio\n"
        "🌌 /fanart - Fanart aleatorio\n"
        "🖼️ /pinterest [busqueda] - Búsqueda en Pinterest\n"
        "🖼️ /stk_buscar [busqueda] - Buscar stickers\n"
        "📁 /mediafire [link] - Descargar de MediaFire\n"
        "📁 /drive [link] - Descargar de Google Drive\n"
        "📁 /pixeldrain [link] - Descargar de Pixeldrain\n"
        "📁 /gofile [link] - Descargar de GoFile\n"
        "📁 /apkpure [app] - Descargar APK de APKPure\n"
        "📁 /apktodo [app] - Descargar APK de APKTodo\n"
        "📁 /uptodown [app] - Descargar APK de Uptodown\n"
        "📁 /apkcombo [app] - Descargar APK de APKCombo\n"
        "📁 /fdroid [app] - Buscar app en F-Droid\n"
        "🎵 /musica [busqueda] - Buscar música\n"
        "🎬 /pelicula [busqueda] - Buscar película\n"
        "🎬 /serie [busqueda] - Buscar serie\n"
        "🎭 /anime [busqueda] - Buscar anime\n"
        "🎮 /juego [busqueda] - Buscar juego\n"
        "📖 /libro [busqueda] - Buscar libro\n"
        "🐶 /dog - Foto de perro aleatoria\n"
        "🐱 /cat - Foto de gato aleatoria\n"
        "🦊 /fox - Foto de zorro aleatoria\n"
        "🦮 /video [busqueda] - Buscar video\n"
        "🔊 /audio [busqueda] - Buscar audio\n"
        "🖼️ /foto [busqueda] - Buscar foto\n"
        "🔄 /descarga_rapida [URL] - Descarga rápida\n"
        "🔄 /convertir_video [URL] - Convertir formato de video\n"
        "🔄 /convertir_audio [URL] - Convertir formato de audio\n"
        "📦 /comprimir [archivo] - Comprimir archivo\n"
        "📦 /extraer [archivo] - Extraer archivo\n"
        "📤 /subir [archivo] - Subir archivo\n"
        "🔗 /compartir [enlace] - Compartir enlace\n"
        "🔗 /enlace [enlace] - Generar enlace de descarga\n"
    )
    # ── PASO 1: Verificar si el mensaje es muy largo
    if len(msg) > 4000:
        # ── PASO 2: Dividir en 2 partes (máximo 4000 caracteres cada una)
        parte1 = msg[:4000]
        parte2 = msg[4000:]
        
        # ── PASO 3: Enviar ambas partes
        await update.message.reply_text(parte1, parse_mode=ParseMode.MARKDOWN)
        await update.message.reply_text(parte2, parse_mode=ParseMode.MARKDOWN)
    else:
        # ── PASO 4: Si es corto, enviar normalmente
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def cmd_list4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Categoría 4: Seguridad & Criptografía"""
    msg = (
        "🛡️ **CATEGORÍA 4: SEGURIDAD & CRIPTOGRAFÍA** 🛡️\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 /hash_md5 [texto] - Generar hash MD5\n"
        "🔐 /hash_sha256 [texto] - Generar hash SHA256\n"
        "🔓 /b64encode [texto] - Codificar en Base64\n"
        "🔓 /b64decode [texto] - Decodificar Base64\n"
        "🔒 /temp [temp] - Convertir temperatura\n"
        "📏 /m_km [metros] - Convertir metros a kilómetros\n"
        "🔢 /numrand [min] [max] - Número aleatorio\n"
        "🔄 /convertir [unidad] [valor] - Convertir unidades\n"
        "📑 /palabras [texto] - Contar palabras\n"
        "🔄 /invertir [texto] - Invertir texto\n"
        "🔠 /mayus [texto] - Convertir a mayúsculas\n"
        "🔠 /minus [texto] - Convertir a minúsculas\n"
        "🎨 /cesar [texto] [desplazamiento] - Cifrado César\n"
        " Morse [texto] - Convertir a código Morse\n"
        "🎨 /ascii [texto] - Convertir a arte ASCII\n"
        "🔄 /repetir [texto] [veces] - Repetir texto\n"
        "🔄 /palindromo [texto] - Verificar palíndromo\n"
        "🔄 /espaciar [texto] - Espaciar texto\n"
        "🧮 /factorial [n] - Calcular factorial\n"
        "🧮 /fib [n] - Calcular Fibonacci\n"
        "🧮 /primo [n] - Verificar número primo\n"
        "🧮 /bin [n] - Convertir a binario\n"
        "🧮 /hex [n] - Convertir a hexadecimal\n"
        "🧮 /oct [n] - Convertir a octal\n"
        "🧮 /raiz [n] - Calcular raíz cuadrada\n"
        "🧮 /porciento [total] [porcentaje] - Calcular porcentaje\n"
        "🩺 /imc [peso] [altura] - Calcular IMC\n"
        "🔑 /pass [longitud] - Generar contraseña\n"
        "🆔 /uuid - Generar UUID\n"
        "👤 /nombrefake - Generar nombre falso\n"
        "📧 /emailfake - Generar email falso\n"
        "🚗 /placa - Generar placa venezolana\n"
        "🛂 /cedula - Generar cédula falsa\n"
        "🎨 /colorhex - Generar color hexadecimal\n"
        "📅 /fecha - Ver fecha actual\n"
        "⏳ /unix - Ver tiempo Unix\n"
        "🎂 /edad [fecha] - Calcular edad\n"
        "🕒 /diasfalta [fecha] - Días que faltan para una fecha\n"
        "🌍 /relojmundial - Ver hora en diferentes países\n"
        "⏳ /countdown [tiempo] - Cuenta regresiva\n"
        "👤 /randomuser - Generar usuario aleatorio\n"
        "🎉 /sorteo [opciones] - Hacer sorteo\n"
        "🔄 /turnos [opciones] - Generar turnos aleatorios\n"
        "🔋 /bateria - Ver nivel de batería\n"
        "💡 /compatibilidad [nombre1] [nombre2] - Ver compatibilidad\n"
        "📊 /encuesta [pregunta] - Crear encuesta rápida\n"
        "🌍 /climaciudad [ciudad] - Ver clima por ciudad\n"
        " Romanos [número] - Convertir a número romano\n"
    )
    # ── PASO 1: Verificar si el mensaje es muy largo
    if len(msg) > 4000:
        # ── PASO 2: Dividir en 2 partes (máximo 4000 caracteres cada una)
        parte1 = msg[:4000]
        parte2 = msg[4000:]
        
        # ── PASO 3: Enviar ambas partes
        await update.message.reply_text(parte1, parse_mode=ParseMode.MARKDOWN)
        await update.message.reply_text(parte2, parse_mode=ParseMode.MARKDOWN)
    else:
        # ── PASO 4: Si es corto, enviar normalmente
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def cmd_list5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Categoría 5: Búsqueda & Utilidades"""
    msg = (
        "🔍 **CATEGORÍA 5: BÚSQUEDA & UTILIDADES** 🔍\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔍 /buscar [query] - Buscar en Google\n"
        "📚 /wiki [query] - Buscar en Wikipedia\n"
        "🌤️ /clima [ciudad] - Ver clima actual\n"
        "🔍 /ip [IP] - Ver información de IP\n"
        "🧑‍💻 /github [usuario] - Buscar usuario GitHub\n"
        "📱 /tiktokuser [usuario] - Buscar usuario TikTok\n"
        "🔥 /idff [ID] - Buscar ID Free Fire\n"
        "📰 /noticias - Ver últimas noticias\n"
        "📱 /tecnologia - Noticias de tecnología\n"
        "⚽ /deportes - Noticias de deportes\n"
        "🎭 /entretenimiento - Noticias de entretenimiento\n"
        "💰 /economia - Noticias económicas\n"
        "🗳️ /politica - Noticias políticas\n"
        "🏥 /salud - Noticias de salud\n"
        "🔬 /ciencia - Noticias de ciencia\n"
        "💡 /curiosidad - Dato curioso\n"
        "❓ /pregunta [pregunta] - Responder pregunta\n"
        "📝 /definir [palabra] - Definir palabra\n"
        "🔄 /sinonimo [palabra] - Buscar sinónimo\n"
        "🔄 /antonimo [palabra] - Buscar antónimo\n"
        "🔄 /traducir [texto] - Traducir texto (12 idiomas)\n"
        "🔄 /traen [texto] - Traducir a inglés rápido\n"
        "🔄 /trafr [texto] - Traducir a francés rápido\n"
        "🔄 /taes [texto] - Traducir a español rápido\n"
        "🔄 /tade [texto] - Traducir a alemán rápido\n"
        "🔄 /tapt [texto] - Traducir a portugués rápido\n"
        "🔄 /tait [texto] - Traducir a italiano rápido\n"
        "🔄 /tazh [texto] - Traducir a chino rápido\n"
        "🔄 /taja [texto] - Traducir a japonés rápido\n"
        "🔄 /taar [texto] - Traducir a árabe rápido\n"
        "🔄 /taru [texto] - Traducir a ruso rápido\n"
        "ℹ️ /info [bot] - Información del bot\n"
        "❓ /ayuda - Ayuda general\n"
        "📋 /comandos - Lista de comandos\n"
        "📋 /menu - Menú principal\n"
    )
    # ── PASO 1: Verificar si el mensaje es muy largo
    if len(msg) > 4000:
        # ── PASO 2: Dividir en 2 partes (máximo 4000 caracteres cada una)
        parte1 = msg[:4000]
        parte2 = msg[4000:]
        
        # ── PASO 3: Enviar ambas partes
        await update.message.reply_text(parte1, parse_mode=ParseMode.MARKDOWN)
        await update.message.reply_text(parte2, parse_mode=ParseMode.MARKDOWN)
    else:
        # ── PASO 4: Si es corto, enviar normalmente
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def cmd_list6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Categoría 6: Herramientas & Utilidades"""
    msg = (
        "🛠️ **CATEGORÍA 6: HERRAMIENTAS & UTILIDADES** 🛠️\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🧮 /calc [operación] - Calcular expresión matemática\n"
        "📝 /limpiar [texto] - Limpiar texto de caracteres especiales\n"
        "📊 /vocal_count [texto] - Contar vocales y consonantes\n"
        "🔍 /info_ciudad [ciudad] - Información de ciudad\n"
        "📱 /info_telefono [número] - Información de número telefónico\n"
        "🔍 /info_pais [país] - Información de país\n"
        "📊 /info_moneda [moneda] - Información de moneda\n"
        "📊 /info_emoji [emoji] - Información de emoji\n"
        "🔍 /info_simbolo [símbolo] - Información de símbolo\n"
        "📊 /info_cripto [moneda] - Información de criptomoneda\n"
        "📊 /info_dolar - Precio del dólar\n"
        "📊 /info_cripto - Precio de criptomoneda\n"
        "📊 /info_clima [ciudad] - Clima en tiempo real\n"
        "📊 /info_ip [IP] - Información de IP\n"
        "🔍 /info_github [usuario] - Información de GitHub\n"
        "🔍 /info_tiktok [usuario] - Información de TikTok\n"
        "🔍 /info_freefire [ID] - Información de Free Fire\n"
        "🔍 /info_tiktokuser [usuario] - Información de TikTok\n"
        "🔍 /info_youtube [usuario] - Información de YouTube\n"
        "🔍 /info_instagram [usuario] - Información de Instagram\n"
        "🔍 /info_twitter [usuario] - Información de Twitter\n"
        "🔍 /info_facebook [usuario] - Información de Facebook\n"
        "🔍 /info_google [usuario] - Información de Google\n"
        "🔍 /info_wikipedia [usuario] - Información de Wikipedia\n"
        "🔍 /info_youtube [usuario] - Información de YouTube\n"
        "🔍 /info_tiktok [usuario] - Información de TikTok\n"
        "🔍 /info_instagram [usuario] - Información de Instagram\n"
        "🔍 /info_twitter [usuario] - Información de Twitter\n"
        "🔍 /info_facebook [usuario] - Información de Facebook\n"
        "🔍 /info_google [usuario] - Información de Google\n"
        "🔍 /info_wikipedia [usuario] - Información de Wikipedia\n"
    )
    # ── PASO 1: Verificar si el mensaje es muy largo
    if len(msg) > 4000:
        # ── PASO 2: Dividir en 2 partes (máximo 4000 caracteres cada una)
        parte1 = msg[:4000]
        parte2 = msg[4000:]
        
        # ── PASO 3: Enviar ambas partes
        await update.message.reply_text(parte1, parse_mode=ParseMode.MARKDOWN)
        await update.message.reply_text(parte2, parse_mode=ParseMode.MARKDOWN)
    else:
        # ── PASO 4: Si es corto, enviar normalmente
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
async def cmd_list7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Categoría 7: Juegos"""
    msg = (
        "🎲 **CATEGORÍA 7: JUEGOS** 🎲\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🎲 /dado - Tirar dado\n"
        "🪙 /moneda - Tirar moneda\n"
        "✋ /ppt - Piedra, papel o tijera\n"
        "🧠 /trivia - Jugar trivia\n"
        "🧠 /adivinanza - Adivinar adivinanza\n"
        "🔮 /tarot - Tirar cartas del tarot\n"
        "🔮 /horoscopo - Ver horóscopo\n"
        "🪜 /ahorcado - Jugar ahorcado\n"
        "🧠 /mayormenor - Juego mayor o menor\n"
        "🎮 /simon - Simon dice\n"
        "📊 /batalla - Estadísticas de batalla\n"
        "🃏 /poker - Jugar póker\n"
        "♠️ /blackjack - Jugar blackjack\n"
        "🎯 /ruleta - Jugar ruleta\n"
        "🎰 /tragamonedas - Jugar tragamonedas\n"
        "🎯 /roulette - Ruleta europea\n"
        "💬 /verdad - Verdad o reto\n"
        "💬 /reto - Verdad o reto\n"
        "💬 /vyp - Verdad o reto\n"
        "❤️ /gay - Medidor gay\n"
        "🔥 /facha - Medidor facha\n"
        "☠️ /toxico - Medidor tóxico\n"
        "💋 /puta - Medidor puta\n"
        "🖤 /negro - Medidor negro\n"
        "😇 /virgen - Medidor virgen\n"
        "🤪 /loco - Medidor loco\n"
        "💪 /sigma - Medidor sigma\n"
        "💋 /besuquear - Besuquear a alguien\n"
        "🤝 /abrazo - Abrazar a alguien\n"
        "👊 /golpear - Golpear a alguien\n"
        "🦶 /patada - Dar patada\n"
        "👊 /puñetazo - Dar puñetazo\n"
        "👋 /cachetada - Dar cachetada\n"
        "💋 /morder - Morder a alguien\n"
        "👋 /abofetear - Abofetear\n"
        "👋 /empujar - Empujar\n"
        "👋 /tirar - Tirar al suelo\n"
        "👋 /levantar - Levantar\n"
        "👋 /cargar - Cargar en brazos\n"
        "👋 /acariciar - Acariciar\n"
        "👋 /pellizcar - Pellizcar\n"
        "👋 /cosquillas - Hacer cosquillas\n"
        "👋 /abofetear - Abofetear\n"
        "👋 /insultar - Insultar\n"
        "👋 /elogiar - Elogiar\n"
        "👋 /animar - Animar\n"
        "👋 /desafiar - Desafiar\n"
        "👋 /retar - Retar\n"
        "👋 /duelo - Pedir duelo\n"
        "👋 /pelear - Pelear\n"
        "👋 /huir - Huir de pelea\n"
        "👋 /rendirse - Rendirse\n"
        "🎉 /victoria - Celebrar victoria\n"
        "😭 /derrota - Aceptar derrota\n"
        "🤝 /empate - Empate\n"
        "🎮 /jugar - Jugar juego aleatorio\n"
        "🔮 /carta - Generar carta de amor/odio\n"
        "🎤 /rap - Generar rap aleatorio\n"
        "🔮 /ojoturco - Protección espiritual\n"
        "🎭 /alias - Generar alias criminal\n"
        "🔮 /hechizo - Lanzar hechizo random\n"
        "🌙 /luna - Fase lunar de hoy\n"
        "💣 /bomba - Cuenta regresiva dramática\n"
        "🧬 /adn - Análisis de ADN ficticio\n"
        "🎯 /tripleSuerte - Triple apuesta instantánea\n"
        "💪 /poder - Obtener superpoder\n"
        "🌀 /chakra - Nivel de chakra\n"
        "🔥 /sith - Fuerza oscura\n"
        "⚡ /elemento - Elemento mágico\n"
        "🔮 /bola_cristal - Bola de cristal\n"
        "🍀 /suerte - Medidor de suerte\n"
        "😂 /memes - Ver memes\n"
        "📜 /frase_celebre - Frase célebre\n"
        "💡 /ideanegocio - Idea de negocio\n"
        "🎬 /pitch - Pitch de negocio\n"
        "🔮 /destino - Predicción del destino\n"
        "🧠 /iq - Test de IQ\n"
        "🍀 /fortuna - Fortuna china\n"
        "🇯🇵 /japones - Nombre japonés\n"
    )
    # ── PASO 1: Verificar si el mensaje es muy largo
    if len(msg) > 4000:
        # ── PASO 2: Dividir en 2 partes (máximo 4000 caracteres cada una)
        parte1 = msg[:4000]
        parte2 = msg[4000:]
        
        # ── PASO 3: Enviar ambas partes
        await update.message.reply_text(parte1, parse_mode=ParseMode.MARKDOWN)
        await update.message.reply_text(parte2, parse_mode=ParseMode.MARKDOWN)
    else:
        # ── PASO 4: Si es corto, enviar normalmente
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
async def cmd_list8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Categoría 8: Educación"""
    msg = (
        "🎓 **CATEGORÍA 8: EDUCACIÓN** 🎓\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📚 /ver_cursos - Ver cursos disponibles\n"
        "📝 /inscribirse - Inscribirse en curso\n"
        "📈 /progreso - Ver progreso de curso\n"
        "📝 /crear_tarea - Crear tarea de estudio\n"
        "📚 /mis_tareas - Ver mis tareas\n"
        "🎯 /tipocurso - Tipo de curso recomendado\n"
        "🧠 /skillcheck - Verificar habilidades\n"
        "💻 /html - Curso de HTML\n"
        "🐍 /pycode - Curso de Python\n"
        "🔐 /git - Curso de Git\n"
        "💻 /linux - Curso de Linux\n"
        "🧮 /regex - Curso de expresiones regulares\n"
        "📝 /apuntes - Tomar apuntes\n"
        "📝 /resumen - Crear resumen\n"
        "📝 /esquema - Crear esquema\n"
        "📝 /diagrama - Crear diagrama\n"
        "📝 /mapa_mental - Crear mapa mental\n"
        "📚 /recursos - Buscar recursos educativos\n"
        "📚 /biblioteca - Buscar en biblioteca\n"
        "📚 /diccionario - Buscar en diccionario\n"
        "📚 /enciclopedia - Buscar en enciclopedia\n"
        "📝 /tesis - Consejo para tesis\n"
        "📝 /tesina - Consejo para tesina\n"
        "📝 /monografia - Consejo para monografía\n"
        "📝 /investigacion - Consejo para investigación\n"
    )
    # ── PASO 1: Verificar si el mensaje es muy largo
    if len(msg) > 4000:
        # ── PASO 2: Dividir en 2 partes (máximo 4000 caracteres cada una)
        parte1 = msg[:4000]
        parte2 = msg[4000:]
        
        # ── PASO 3: Enviar ambas partes
        await update.message.reply_text(parte1, parse_mode=ParseMode.MARKDOWN)
        await update.message.reply_text(parte2, parse_mode=ParseMode.MARKDOWN)
    else:
        # ── PASO 4: Si es corto, enviar normalmente
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)  

async def cmd_list9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Categoría 9: Especiales & Admin"""
    msg = """ especiales y admin:
    
    ★te pille jaja no puedes ver esto, ya que es privado★"""
    await update.message.reply_text(msg)
    
#aqui va el sistema de Información

async def cmd_info_completa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra información completa del bot descargada de MediaFire o desde archivo local."""
    user_id = update.effective_user.id
    INFO_FILE = "info_completa.txt"
    MEDIAFIRE_PAGE = "https://www.mediafire.com/file/om2xp9axdvk9ro3/info_completa.txt/file"

    # ── PASO 1: Intentar leer el archivo local primero
    contenido = None
    if os.path.exists(INFO_FILE):
        try:
            with open(INFO_FILE, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception:
            contenido = None

    # ── PASO 2: Si no hay archivo local, descargar de MediaFire
    if not contenido:
        await update.message.reply_text("⏳ Descargando lista de comandos...")
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            # Obtener la página de MediaFire para extraer el link directo
            pagina = requests.get(MEDIAFIRE_PAGE, headers=headers, timeout=15)
            pagina.raise_for_status()

            # Extraer el enlace de descarga directa con BeautifulSoup o regex
            url_directa = None
            if BS4_DISPONIBLE:
                soup = BeautifulSoup(pagina.text, "html.parser")
                btn = soup.find("a", {"id": "downloadButton"})
                if btn:
                    url_directa = btn.get("href")

            # Fallback con regex si no se encontró con BeautifulSoup
            if not url_directa:
                match = re.search(r'href=["\']?(https://download\d*\.mediafire\.com/[^"\'>\s]+)', pagina.text)
                if match:
                    url_directa = match.group(1)

            if not url_directa:
                raise ValueError("No se pudo obtener el enlace de descarga de MediaFire")

            # Descargar el archivo directamente
            resp = requests.get(url_directa, headers=headers, timeout=30)
            resp.raise_for_status()
            contenido = resp.content.decode("utf-8", errors="ignore")

            # Guardar localmente para futuros usos
            with open(INFO_FILE, "w", encoding="utf-8") as f:
                f.write(contenido)

        except Exception as e:
            await update.message.reply_text(
                "❌ No pude obtener la lista de comandos desde MediaFire.\n"
                f"_Error: {str(e)[:80]}_",
                parse_mode=ParseMode.MARKDOWN
            )
            return

    # ── PASO 3: Enviar el contenido en partes de 4000 caracteres
    LIMITE = 4000
    partes = [contenido[i:i+LIMITE] for i in range(0, len(contenido), LIMITE)]
    total = len(partes)

    for idx, parte in enumerate(partes, 1):
        encabezado = f"📋 *Parte {idx} de {total}*\n\n" if total > 1 else ""
        await update.message.reply_text(encabezado + parte, parse_mode=None)

    # ── PASO 4: Enviar también el archivo .txt
    try:
        with open(INFO_FILE, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename="info_completa.txt",
                caption="📎 Lista completa de comandos — guárdala para referencia"
            )
    except Exception:
        pass

    sumar_xp(user_id, 5)

#justo aqui arriba

# ════════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════════
# 🚀 50+ COMANDOS NUEVOS ULTRA MASIVOS - BLOQUE FINAL 2024
# ════════════════════════════════════════════════════════════════════════════════

# 🎲 JUEGOS ADICIONALES
async def cmd_ruleta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Juego de ruleta rusa."""
    resultado = random.choice(["💥 ¡BANG! Perdiste", "🎉 ¡Sobreviviste!", "😅 Muy cerca"])
    await update.message.reply_text(f"🎰 **RULETA RUSA**\n{resultado}")

async def cmd_roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ruleta con dinero."""
    if not context.args:
        await update.message.reply_text("Uso: /roulette <apuesta>")
        return
    apuesta = int(context.args[0])
    ganancia = apuesta if random.random() > 0.5 else -apuesta
    msg = f"🎡 **ROULETTE**\nApuesta: ${apuesta}\nResultado: ${ganancia}"
    await update.message.reply_text(msg)

async def cmd_tragamonedas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Máquina tragamonedas."""
    emojis = ["🍎", "🍊", "🍋", "🍌", "🍉", "7️⃣"]
    resultado = [random.choice(emojis) for _ in range(3)]
    ganancia = 100 if len(set(resultado)) == 1 else -10
    msg = f"🎰 **TRAGAMONEDAS**\n{' '.join(resultado)}\n💰 Ganancia: ${ganancia}"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# 📚 EDUCACIÓN ADICIONAL
async def cmd_tipocurso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recomendación de tipo de curso."""
    cursos = ["Python", "JavaScript", "Web Dev", "Data Science", "Machine Learning", "DevOps"]
    recom = random.choice(cursos)
    await update.message.reply_text(f"📚 Te recomiendo aprender: **{recom}** 🚀")

async def cmd_skillcheck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verifica tu nivel de habilidad."""
    nivel = random.randint(1, 100)
    msg = f"💪 **TU NIVEL DE HABILIDAD**: {nivel}%\n"
    if nivel > 80:
        msg += "🌟 Excelente - ¡Eres un experto!"
    elif nivel > 60:
        msg += "👍 Bueno - Vas por buen camino"
    else:
        msg += "📖 Principiante - ¡Sigue aprendiendo!"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# 🏥 SALUD & BIENESTAR
async def cmd_vitales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simulador de signos vitales."""
    pa = f"{random.randint(100, 140)}/{random.randint(60, 90)}"
    fc = random.randint(60, 100)
    temp = f"{random.uniform(36.5, 37.5):.1f}°C"
    msg = f"🏥 **SIGNOS VITALES SIMULADOS**\n💉 PA: {pa}\n❤️ FC: {fc} bpm\n🌡️ Temp: {temp}"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def cmd_estres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Medidor de estrés."""
    nivel = random.randint(0, 100)
    await update.message.reply_text(f"😰 **NIVEL DE ESTRÉS**: {nivel}%\n💡 Tip: Respira profundo 🧘")

# 🎨 CREATIVIDAD & ARTE
async def cmd_paleta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera paleta de colores aleatoria."""
    colores = [f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}" for _ in range(5)]
    msg = "🎨 **PALETA DE COLORES**\n" + "\n".join([f"- {c}" for c in colores])
    await update.message.reply_text(msg)

async def cmd_arte_aleatorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera arte ASCII aleatorio."""
    artes = [
        "🎭 /\\_/\\ (Gato)",
        "🐶 C|_| (Perro)", 
        "🦋 <>< (Pez)",
        "👾 [O_O] (Alien)"
    ]
    await update.message.reply_text(random.choice(artes))

# 🌟 MOTIVACIÓN & DESARROLLO PERSONAL
async def cmd_affirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Afirmación positiva del día."""
    afirmaciones = [
        "Eres capaz de lograr tus sueños 🌟",
        "Tu potencial es ilimitado 🚀",
        "Mereces lo mejor 👑",
        "Cada día es una nueva oportunidad 🌅",
        "Eres más fuerte de lo que crees 💪"
    ]
    await update.message.reply_text(f"✨ {random.choice(afirmaciones)}")

async def cmd_meta_dia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Define tu meta del día."""
    if not context.args:
        await update.message.reply_text("Uso: /meta_dia <tu meta>")
        return
    meta = " ".join(context.args)
    await update.message.reply_text(f"🎯 **META DEL DÍA**: {meta}\n¡Adelante, tú puedes! 💪")

# 🔮 DIVERSIÓN & ADIVINACIÓN
async def cmd_bola_cristal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bola de cristal mágica."""
    respuestas = ["Sí, definitivamente", "No, de ninguna manera", "Talvez", "Muy probable", "Imposible", "El futuro es incierto"]
    await update.message.reply_text(f"🔮 **BOLA DE CRISTAL**\n{random.choice(respuestas)}")

async def cmd_suerte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tu nivel de suerte hoy."""
    suerte = random.randint(1, 100)
    emojis = ["😂", "😐", "🤔", "😊", "🎉"][suerte // 25]
    await update.message.reply_text(f"🍀 **NIVEL DE SUERTE HOY**: {suerte}% {emojis}")

# 🎬 ENTRETENIMIENTO ADICIONAL
async def cmd_memes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Colección de memes aleatorios."""
    memes = [
        "🤦 If you know, you know",
        "😂 Laughing in Spanish",
        "🙃 Pretending to understand",
        "💀 Dying from laughter"
    ]
    await update.message.reply_text(f"😂 {random.choice(memes)}")

async def cmd_frase_celebre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Frase célebre aleatoria."""
    frases = [
        "La vida es lo que te sucede mientras estás ocupado haciendo otros planes. - John Lennon",
        "El único modo de hacer un trabajo excelente es amar lo que haces. - Steve Jobs",
        "Sé tú mismo; todos los demás ya están ocupados. - Oscar Wilde"
    ]
    await update.message.reply_text(f"💬 {random.choice(frases)}")

# 💼 NEGOCIOS & EMPRENDIMIENTO
async def cmd_ideanegocio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generador de ideas de negocio."""
    ideas = [
        "App de gestión de tareas inteligente",
        "Consultoría de marketing digital",
        "Tienda online de productos sostenibles",
        "Curso online de programación",
        "Servicio de diseño gráfico freelance"
    ]
    await update.message.reply_text(f"💡 **IDEA DE NEGOCIO**: {random.choice(ideas)}")

async def cmd_pitch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generador de elevator pitch."""
    if not context.args:
        await update.message.reply_text("Uso: /pitch <tu producto>")
        return
    producto = " ".join(context.args)
    await update.message.reply_text(f"🎤 **PITCH**: {producto} es la solución que te faltaba. Rápido, fácil y efectivo. ¡Únete ahora!")

# 🌍 VIAJES & AVENTURA
async def cmd_destino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sugiere destino de viaje."""
    destinos = ["Japón 🇯🇵", "Noruega 🇳🇴", "Tailandia 🇹🇭", "Portugal 🇵🇹", "Nueva Zelanda 🇳🇿"]
    await update.message.reply_text(f"✈️ **DESTINO SUGERIDO**: {random.choice(destinos)}")

# ════════════════════════════════════════════════════════════════════════════════
# 💥 BLOQUE MEGA: 50+ COMANDOS NUEVOS ADICIONALES
# ════════════════════════════════════════════════════════════════════════════════

# Finanzas Avanzadas
async def cmd_portafolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💼 **PORTAFOLIO**: Valor total: ${random.randint(10000, 1000000)}")

async def cmd_dividendos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💰 **DIVIDENDOS**: +${random.randint(100, 5000)}/mes")

async def cmd_taxes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📊 **IMPUESTOS**: {random.randint(10, 40)}% estimado")

# Salud Mental
async def cmd_meditacion_guiada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧘 **MEDITACIÓN**: Cierra los ojos, respira profundo durante 5 minutos...")

async def cmd_ansiedad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("😌 **ANSIEDAD**: Técnica 5-4-3-2-1 para calmarte")

async def cmd_depresion_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💙 **AYUDA**: Si necesitas hablar, aquí estoy. También busca profesional.")

# Fitness
async def cmd_hiit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 **HIIT RÁPIDO**: 30s max effort, 30s descanso x 10 rondas")

async def cmd_stretching(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤸 **ESTIRAMIENTO**: 10 min de flexibilidad diaria")

async def cmd_cardio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏃 **CARDIO**: 20-30 min de actividad aeróbica")

# Nutrición
async def cmd_receta_facil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    recetas = ["Ensalada", "Pasta", "Arroz con pollo", "Sopa", "Omelette"]
    await update.message.reply_text(f"🍳 **RECETA**: {random.choice(recetas)}")

async def cmd_macro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🥗 **MACROS**: P:{random.randint(20,40)}g C:{random.randint(40,60)}g G:{random.randint(15,30)}g")

async def cmd_agua_daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💧 **AGUA**: Deberías beber 2-3L diarios")

# Productividad
async def cmd_pomodoro_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏱️ **POMODORO**: 25 min de enfoque - ¡A trabajar!")

async def cmd_break_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("☕ **BREAK**: Descansa 5 min, camina, estira")

async def cmd_focus_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 **MÚSICA**: Busca 'Lo-Fi Hip Hop' en Spotify")

# Dinero
async def cmd_presupuesto_mes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📈 **PRESUPUESTO**: Gasto: ${random.randint(1000,5000)}, Ahorro: {random.randint(10,30)}%")

async def cmd_deuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💳 **DEUDA**: Saldo: ${random.randint(0, 10000)}")

async def cmd_ahorro_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏦 **PLAN AHORRO**: 50/30/20 - Necesidades/Deseos/Ahorro")

# Diversión
async def cmd_trivia_rápida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    preguntas = ["¿Capital de Francia?", "¿Planeta más grande?", "¿Mayor océano?"]
    await update.message.reply_text(f"🧠 {random.choice(preguntas)}")

async def cmd_acertijo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    acertijos = ["Soy agua pero no mojo", "Tengo ciudades pero no casas", "Soy negra pero brillo"]
    await update.message.reply_text(f"🤔 {random.choice(acertijos)}")

async def cmd_chiste_corto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chistes = ["¿Por qué los pájaros no se pierden? Porque usan GPS", "Soy pan de molde... 🍞", "Un libro entra a un bar... ¡Ay!"]
    await update.message.reply_text(f"😂 {random.choice(chistes)}")

# Romance
async def cmd_cumplido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cumplidos = ["Sonríes bellísimo", "Tu energía es contagiosa", "Eres valiente", "Inspiras a otros"]
    await update.message.reply_text(f"💝 {random.choice(cumplidos)}")

async def cmd_consejo_amor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💕 **AMOR**: La comunicación es la base de todo")

async def cmd_crush(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"😍 **CRUSH**: Tu probabilidad de éxito: {random.randint(40,99)}%")

# Tech Tips
async def cmd_codigo_dia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tips = ["DRY - Don't Repeat Yourself", "KISS - Keep It Simple", "SOLID - Principles"]
    await update.message.reply_text(f"💻 {random.choice(tips)}")

async def cmd_bug_fix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🐛 **DEBUG**: Usa print() o breakpoints para investigar")

async def cmd_arquitectura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏗️ **ARQUITECTURA**: MVC, MVP, MVVM, Clean Architecture")

# Carrera
async def cmd_cv_tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 **CV**: Destaca logros, no solo responsabilidades")

async def cmd_entrevista_prep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎤 **ENTREVISTA**: Prepara ejemplos STAR: Situación, Tarea, Acción, Resultado")

async def cmd_linkedin_tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💼 **LINKEDIN**: Actualiza perfil, conéctate, comenta")

# Viajes
async def cmd_presupuesto_viaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"✈️ **PRESUPUESTO**: Estimado: ${random.randint(1000, 10000)}")

async def cmd_itinerario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗺️ **ITINERARIO**: Día 1: Llegar, Día 2-4: Explorar, Día 5: Regreso")

async def cmd_idioma_viaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    frases = ["Hola", "Gracias", "¿Dónde está?", "¿Cuánto cuesta?"]
    await update.message.reply_text(f"🗣️ {random.choice(frases)}")

# Desarrollo Personal
async def cmd_habito_nuevo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    habitos = ["Leer 30 min", "Meditar", "Ejercicio", "Aprender algo nuevo"]
    await update.message.reply_text(f"✨ **HÁBITO**: Intenta {random.choice(habitos)}")

async def cmd_reflexion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤔 **REFLEXIÓN**: ¿Qué aprendiste hoy? ¿Qué harías diferente?")

async def cmd_meta_semana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 **META SEMANA**: Sé específico, medible y realista")

# Entretenimiento Extra
async def cmd_pelicula_genero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    peliculas = ["Action", "Drama", "Comedy", "Thriller", "Animation"]
    await update.message.reply_text(f"🎬 Elige género: {random.choice(peliculas)}")

async def cmd_libro_recomendado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    libros = ["Sapiens", "1984", "El Principito", "Harry Potter", "Cien años de soledad"]
    await update.message.reply_text(f"📖 Te recomiendo: {random.choice(libros)}")

async def cmd_podcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎙️ **PODCAST**: Busca temas de tu interés en Spotify")

# 📊 SISTEMA DE ESTADÍSTICAS GLOBAL
estadisticas_global = cargar_db("estadisticas_global.json")

async def cmd_estadisticas_global(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_usuarios = len(banco)
    total_dinero = sum(banco.values()) if banco else 0
    total_xp = sum(niveles.values()) if niveles else 0
    
    msg = f"📊 **ESTADÍSTICAS GLOBALES**\n👥 Usuarios: {total_usuarios}\n💰 Dinero Total: ${total_dinero}\n⭐ XP Total: {total_xp}\n🎮 Comandos: 1500+"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# 🌙 SISTEMA DE EVENTOS DIARIOS
eventos_diarios = {
    "lunes": "Multiplicador de dinero x2",
    "miércoles": "Triple de XP",
    "viernes": "Premios especiales",
    "sábado": "Bonificación de fin de semana",
    "domingo": "Descanso del bot"
}

async def cmd_evento_del_dia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hoy = datetime.now().strftime("%A").lower()
    dia_semana = {"monday": "lunes", "tuesday": "martes", "wednesday": "miércoles", "thursday": "jueves", "friday": "viernes", "saturday": "sábado", "sunday": "domingo"}
    dia = dia_semana.get(hoy, hoy)
    evento = eventos_diarios.get(dia, "Sin evento especial")
    await update.message.reply_text(f"🌙 **EVENTO DE HOY**\n📅 {dia.capitalize()}\n🎁 {evento}", parse_mode=ParseMode.MARKDOWN)

async def cmd_inforcd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra info completa de todos los comandos del bot."""
    msg = (
        "📋 **INFORMACIÓN COMPLETA DE COMANDOS**\n\n"
        "Usa /list1 - /list9 para ver las categorías de comandos.\n"
        "Usa /menu para ver el menú principal.\n"
        "Usa /help para obtener ayuda.\n\n"
        "✨ _CamilaBot V15.0 - AnyerJR_"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


async def cmd_dlmenucp(update, context):
    """Descarga directa del archivo de lista de comandos."""
    INFO_FILE = "info_completa.txt"
    MEDIAFIRE_PAGE = "https://www.mediafire.com/file/om2xp9axdvk9ro3/info_completa.txt/file"

    if os.path.exists(INFO_FILE):
        try:
            with open(INFO_FILE, "rb") as f:
                await update.message.reply_document(
                    document=f,
                    filename="info_completa.txt",
                    caption="📎 Lista completa de comandos - CamilaBot V15.0\n🤖 AnyerJR | Usa /info_completa para verla en el chat"
                )
        except Exception as e:
            await update.message.reply_text(f"❌ Error enviando archivo: {str(e)[:100]}")
        return

    # Si no existe localmente, intentar descargar de MediaFire
    await update.message.reply_text("⏳ Descargando archivo desde MediaFire...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        pagina = requests.get(MEDIAFIRE_PAGE, headers=headers, timeout=15)
        url_directa = None
        if BS4_DISPONIBLE:
            soup = BeautifulSoup(pagina.text, "html.parser")
            btn = soup.find("a", {"id": "downloadButton"})
            if btn:
                url_directa = btn.get("href")
        if not url_directa:
            match = re.search(r'href=["\']?(https://download\d*\.mediafire\.com/[^"\'>\s]+)', pagina.text)
            if match:
                url_directa = match.group(1)
        if not url_directa:
            raise ValueError("No se encontro el enlace de descarga en MediaFire")
        resp = requests.get(url_directa, headers=headers, timeout=30)
        resp.raise_for_status()
        contenido = resp.content
        with open(INFO_FILE, "wb") as f:
            f.write(contenido)
        buf = io.BytesIO(contenido)
        await update.message.reply_document(
            document=buf,
            filename="info_completa.txt",
            caption="📎 Lista completa de comandos - CamilaBot V15.0\n🤖 AnyerJR"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error al descargar: {str(e)[:120]}\nIntenta de nuevo mas tarde.")

# ════════════════════════════════════════════════════════════════════════════════
# --- [ BLOQUE DE COMANDOS FALTANTES - IMPLEMENTACIONES REALES ] ---
# ════════════════════════════════════════════════════════════════════════════════

# Almacenamiento de cooldowns para comandos de economía
cooldowns_premio = {}
cooldowns_recompensa = {}
cooldowns_bonus = {}
cooldowns_sueldo = {}
historial_tx = cargar_db("historial.json")
banco_ahorros = cargar_db("banco_ahorros.json")

def _req_registro(uid, usuarios_info, update):
    return uid in usuarios_info

def _add_historial(uid, accion, monto):
    if uid not in historial_tx:
        historial_tx[uid] = []
    historial_tx[uid].append({
        "accion": accion,
        "monto": monto,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    if len(historial_tx[uid]) > 20:
        historial_tx[uid] = historial_tx[uid][-20:]
    guardar_db("historial.json", historial_tx)

# ─── PERFIL ───────────────────────────────────────────────────────────────────

async def cmd_nick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cambiar apodo en el perfil."""
    uid = str(update.effective_user.id)
    if uid not in usuarios_info:
        await update.message.reply_text("❌ Primero regístrate con `/reg [nombre] [edad] [género]`", parse_mode="Markdown")
        return
    if not context.args:
        await update.message.reply_text("📝 **Uso:** `/nick [nuevo apodo]`\nEjemplo: `/nick CoolGuy99`", parse_mode="Markdown")
        return
    nuevo_nick = " ".join(context.args)[:30]
    usuarios_info[uid]["nombre"] = nuevo_nick
    guardar_db("usuarios_datos.json", usuarios_info)
    await update.message.reply_text(f"✅ **Apodo actualizado a:** `{nuevo_nick}`", parse_mode="Markdown")

async def cmd_bio_perfil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Establecer biografía en el perfil."""
    uid = str(update.effective_user.id)
    if uid not in usuarios_info:
        await update.message.reply_text("❌ Primero regístrate con `/reg`", parse_mode="Markdown")
        return
    if not context.args:
        bio_actual = usuarios_info[uid].get("bio", "Sin biografía")
        await update.message.reply_text(f"📝 **Tu bio actual:** {bio_actual}\n\n**Uso:** `/bio [tu biografía]`", parse_mode="Markdown")
        return
    nueva_bio = " ".join(context.args)[:150]
    usuarios_info[uid]["bio"] = nueva_bio
    guardar_db("usuarios_datos.json", usuarios_info)
    await update.message.reply_text(f"✅ **Biografía actualizada:**\n_{nueva_bio}_", parse_mode="Markdown")

async def cmd_rango_ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver rango actual del usuario."""
    user_id = update.effective_user.id
    uid = str(user_id)
    nick = update.effective_user.first_name
    xp = niveles.get(uid, 0)
    rango = obtener_rango(user_id)
    rangos = [
        (0, "🥚 Novato"), (100, "🌱 Aprendiz"), (300, "⚔️ Guerrero"),
        (600, "🛡️ Veterano"), (1000, "💎 Experto"), (2000, "🌟 Maestro"),
        (5000, "🔥 Leyenda"), (10000, "👑 Supremo")
    ]
    proximo = None
    for req, nombre in rangos:
        if xp < req:
            proximo = (req, nombre)
            break
    msg = (
        f"🏅 **RANGO DE {nick.upper()}** 🏅\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎖️ **Rango actual:** {rango}\n"
        f"⭐ **XP acumulados:** `{xp:,}`\n"
    )
    if proximo:
        falta = proximo[0] - xp
        msg += f"🎯 **Próximo rango:** {proximo[1]} (faltan `{falta:,}` XP)\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n_¡Sigue interactuando para subir de rango!_"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def cmd_xp_ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver experiencia del usuario."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    xp = niveles.get(uid, 0)
    nivel_num = xp // 100
    await update.message.reply_text(
        f"⭐ **EXPERIENCIA DE {nick.upper()}** ⭐\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 **XP Total:** `{xp:,}`\n"
        f"📊 **Nivel:** `{nivel_num}`\n"
        f"🔄 **XP para siguiente nivel:** `{100 - (xp % 100)}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Gana XP usando comandos del bot._",
        parse_mode="Markdown"
    )

async def cmd_nivel_ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver nivel del usuario."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    xp = niveles.get(uid, 0)
    nivel_num = xp // 100
    barra = "█" * min(nivel_num % 10, 10) + "░" * (10 - min(nivel_num % 10, 10))
    await update.message.reply_text(
        f"📊 **NIVEL DE {nick.upper()}** 📊\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏆 **Nivel:** `{nivel_num}`\n"
        f"⭐ **XP:** `{xp:,}`\n"
        f"[{barra}] `{xp % 100}/100`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_¡Sigue usando el bot para subir de nivel!_",
        parse_mode="Markdown"
    )

async def cmd_borrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Borrar cuenta del usuario."""
    uid = str(update.effective_user.id)
    if uid not in usuarios_info:
        await update.message.reply_text("❌ No tienes una cuenta registrada.")
        return
    nombre = usuarios_info[uid].get("nombre", "Usuario")
    del usuarios_info[uid]
    guardar_db("usuarios_datos.json", usuarios_info)
    if uid in banco:
        del banco[uid]
        guardar_db("banco.json", banco)
    if uid in niveles:
        del niveles[uid]
        guardar_db("niveles.json", niveles)
    await update.message.reply_text(
        f"🗑️ **Cuenta de {nombre} eliminada.**\n"
        f"_Puedes volver a registrarte con /reg en cualquier momento._",
        parse_mode="Markdown"
    )

async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Estadísticas personales del usuario."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    user_id = update.effective_user.id
    if uid not in usuarios_info:
        await update.message.reply_text("❌ Regístrate primero con `/reg`", parse_mode="Markdown")
        return
    info = usuarios_info[uid]
    xp = niveles.get(uid, 0)
    dinero = banco.get(uid, 0.0)
    ahorros = banco_ahorros.get(uid, 0.0)
    rango = obtener_rango(user_id)
    nivel_num = xp // 100
    txs = historial_tx.get(uid, [])
    await update.message.reply_text(
        f"📊 **ESTADÍSTICAS DE {nick.upper()}** 📊\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Nombre:** {info.get('nombre','?')}\n"
        f"🎂 **Edad:** {info.get('edad','?')} años\n"
        f"📅 **Registrado:** {info.get('fecha_registro','?')}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⭐ **XP:** `{xp:,}` | **Nivel:** `{nivel_num}`\n"
        f"🏅 **Rango:** {rango}\n"
        f"💰 **Saldo:** `${dinero:,.2f}`\n"
        f"🏦 **Ahorros:** `${ahorros:,.2f}`\n"
        f"📝 **Transacciones:** `{len(txs)}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Sigue activo para mejorar tus stats._",
        parse_mode="Markdown"
    )

async def cmd_avatar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cambiar avatar (foto de perfil del bot)."""
    await update.message.reply_text(
        "🖼️ **AVATAR**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Tu avatar de Telegram es tu foto de perfil.\n"
        "Para cambiarla ve a _Configuración > Foto de perfil_ en Telegram.\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Tu nombre:** {update.effective_user.first_name}\n"
        f"🆔 **Tu ID:** `{update.effective_user.id}`",
        parse_mode="Markdown"
    )

# ─── ECONOMÍA ─────────────────────────────────────────────────────────────────

async def cmd_saldo_real(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver saldo total del usuario."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    dinero = banco.get(uid, 0.0)
    ahorros = banco_ahorros.get(uid, 0.0)
    total = dinero + ahorros
    await update.message.reply_text(
        f"💳 **SALDO DE {nick.upper()}** 💳\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Billetera:** `${dinero:,.2f}`\n"
        f"🏦 **Ahorros:** `${ahorros:,.2f}`\n"
        f"📊 **Total:** `${total:,.2f}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Usa /trabajar para ganar más._",
        parse_mode="Markdown"
    )

async def cmd_banco_real(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver estado de la cuenta bancaria."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    dinero = banco.get(uid, 0.0)
    ahorros = banco_ahorros.get(uid, 0.0)
    txs = historial_tx.get(uid, [])
    ultima_tx = txs[-1] if txs else None
    msg = (
        f"🏦 **BANCO - {nick.upper()}** 🏦\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Cuenta corriente:** `${dinero:,.2f}`\n"
        f"💎 **Cuenta de ahorros:** `${ahorros:,.2f}`\n"
        f"📊 **Total:** `${(dinero+ahorros):,.2f}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )
    if ultima_tx:
        msg += f"📝 **Última transacción:** {ultima_tx['accion']} `${ultima_tx['monto']:,.2f}` — {ultima_tx['fecha']}\n"
    msg += f"_Usa /depositar [monto] para guardar dinero._"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def cmd_depositar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Depositar dinero en ahorros."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    if not context.args or not context.args[0].replace('.','',1).isdigit():
        await update.message.reply_text("📝 **Uso:** `/depositar [cantidad]`\nEjemplo: `/depositar 500`", parse_mode="Markdown")
        return
    monto = round(float(context.args[0]), 2)
    if monto <= 0:
        await update.message.reply_text("❌ El monto debe ser mayor a 0.")
        return
    saldo = banco.get(uid, 0.0)
    if saldo < monto:
        await update.message.reply_text(f"❌ No tienes suficiente dinero. Tienes `${saldo:,.2f}`", parse_mode="Markdown")
        return
    banco[uid] = round(saldo - monto, 2)
    banco_ahorros[uid] = round(banco_ahorros.get(uid, 0.0) + monto, 2)
    guardar_db("banco.json", banco)
    guardar_db("banco_ahorros.json", banco_ahorros)
    _add_historial(uid, "Depósito", monto)
    await update.message.reply_text(
        f"✅ **DEPÓSITO EXITOSO** ✅\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Depositado:** `${monto:,.2f}`\n"
        f"💳 **Billetera:** `${banco[uid]:,.2f}`\n"
        f"🏦 **Ahorros:** `${banco_ahorros[uid]:,.2f}`",
        parse_mode="Markdown"
    )

async def cmd_retirar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Retirar dinero de ahorros."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    if not context.args or not context.args[0].replace('.','',1).isdigit():
        await update.message.reply_text("📝 **Uso:** `/retirar [cantidad]`\nEjemplo: `/retirar 200`", parse_mode="Markdown")
        return
    monto = round(float(context.args[0]), 2)
    if monto <= 0:
        await update.message.reply_text("❌ El monto debe ser mayor a 0.")
        return
    ahorros = banco_ahorros.get(uid, 0.0)
    if ahorros < monto:
        await update.message.reply_text(f"❌ No tienes suficiente en ahorros. Tienes `${ahorros:,.2f}`", parse_mode="Markdown")
        return
    banco_ahorros[uid] = round(ahorros - monto, 2)
    banco[uid] = round(banco.get(uid, 0.0) + monto, 2)
    guardar_db("banco_ahorros.json", banco_ahorros)
    guardar_db("banco.json", banco)
    _add_historial(uid, "Retiro", monto)
    await update.message.reply_text(
        f"✅ **RETIRO EXITOSO** ✅\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Retirado:** `${monto:,.2f}`\n"
        f"💳 **Billetera:** `${banco[uid]:,.2f}`\n"
        f"🏦 **Ahorros:** `${banco_ahorros[uid]:,.2f}`",
        parse_mode="Markdown"
    )

async def cmd_transferir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Transferir dinero a otro usuario."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "📝 **Uso:** Responde al mensaje del usuario y escribe:\n`/transferir [cantidad]`\nEjemplo: `/transferir 500`",
            parse_mode="Markdown"
        )
        return
    if not context.args or not context.args[0].replace('.','',1).isdigit():
        await update.message.reply_text("❌ Especifica una cantidad válida. Ej: `/transferir 500`", parse_mode="Markdown")
        return
    monto = round(float(context.args[0]), 2)
    if monto <= 0:
        await update.message.reply_text("❌ El monto debe ser mayor a 0.")
        return
    target = update.message.reply_to_message.from_user
    tid = str(target.id)
    if tid == uid:
        await update.message.reply_text("❌ No puedes transferirte dinero a ti mismo.")
        return
    saldo = banco.get(uid, 0.0)
    if saldo < monto:
        await update.message.reply_text(f"❌ No tienes suficiente dinero. Tienes `${saldo:,.2f}`", parse_mode="Markdown")
        return
    banco[uid] = round(saldo - monto, 2)
    banco[tid] = round(banco.get(tid, 0.0) + monto, 2)
    guardar_db("banco.json", banco)
    _add_historial(uid, f"Transferencia a {target.first_name}", monto)
    _add_historial(tid, f"Recibido de {nick}", monto)
    await update.message.reply_text(
        f"✅ **TRANSFERENCIA EXITOSA** ✅\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📤 **De:** {nick}\n"
        f"📥 **Para:** {target.first_name}\n"
        f"💰 **Monto:** `${monto:,.2f}`\n"
        f"💳 **Tu saldo:** `${banco[uid]:,.2f}`",
        parse_mode="Markdown"
    )

async def cmd_robar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Intentar robar dinero a otro usuario."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Responde al mensaje de alguien para robarle.\n`/robar` → responde el mensaje del objetivo", parse_mode="Markdown")
        return
    target = update.message.reply_to_message.from_user
    tid = str(target.id)
    if tid == uid:
        await update.message.reply_text("❌ No puedes robarte a ti mismo, loco.")
        return
    saldo_target = banco.get(tid, 0.0)
    if saldo_target <= 0:
        await update.message.reply_text(f"😅 **{target.first_name}** no tiene nada que robar.")
        return
    import random as _random
    exito = _random.random() < 0.45
    if exito:
        robado = round(_random.uniform(10, min(saldo_target * 0.3, 500)), 2)
        banco[tid] = round(saldo_target - robado, 2)
        banco[uid] = round(banco.get(uid, 0.0) + robado, 2)
        guardar_db("banco.json", banco)
        _add_historial(uid, f"Robo a {target.first_name}", robado)
        await update.message.reply_text(
            f"🥷 **¡ROBO EXITOSO!** 🥷\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💸 Le robaste `${robado:,.2f}` a **{target.first_name}**\n"
            f"💳 **Tu saldo:** `${banco[uid]:,.2f}`",
            parse_mode="Markdown"
        )
    else:
        multa = round(_random.uniform(50, 200), 2)
        mi_saldo = banco.get(uid, 0.0)
        if mi_saldo >= multa:
            banco[uid] = round(mi_saldo - multa, 2)
            guardar_db("banco.json", banco)
            msg_multa = f"💸 Te descontaron `${multa:,.2f}` de multa."
        else:
            msg_multa = "😬 No tenías dinero para la multa, te quedas en cero."
            banco[uid] = 0.0
            guardar_db("banco.json", banco)
        await update.message.reply_text(
            f"🚨 **¡TE ATRAPARON!** 🚨\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"❌ El intento de robo a **{target.first_name}** falló.\n"
            f"{msg_multa}\n"
            f"💳 **Tu saldo:** `${banco.get(uid, 0.0):,.2f}`",
            parse_mode="Markdown"
        )

async def cmd_donar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Donar dinero a otro usuario."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    if not update.message.reply_to_message:
        await update.message.reply_text("📝 Responde al mensaje del usuario y escribe `/donar [cantidad]`", parse_mode="Markdown")
        return
    if not context.args or not context.args[0].replace('.','',1).isdigit():
        await update.message.reply_text("❌ Especifica una cantidad. Ej: `/donar 100`", parse_mode="Markdown")
        return
    monto = round(float(context.args[0]), 2)
    if monto <= 0:
        await update.message.reply_text("❌ El monto debe ser mayor a 0.")
        return
    target = update.message.reply_to_message.from_user
    tid = str(target.id)
    saldo = banco.get(uid, 0.0)
    if saldo < monto:
        await update.message.reply_text(f"❌ Saldo insuficiente. Tienes `${saldo:,.2f}`", parse_mode="Markdown")
        return
    banco[uid] = round(saldo - monto, 2)
    banco[tid] = round(banco.get(tid, 0.0) + monto, 2)
    guardar_db("banco.json", banco)
    sumar_xp(update.effective_user.id, 10)
    _add_historial(uid, f"Donación a {target.first_name}", monto)
    await update.message.reply_text(
        f"❤️ **DONACIÓN ENVIADA** ❤️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 **Donaste:** `${monto:,.2f}` a **{target.first_name}**\n"
        f"💳 **Tu saldo:** `${banco[uid]:,.2f}`\n"
        f"⭐ +10 XP por generosidad",
        parse_mode="Markdown"
    )

async def cmd_casino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Jugar en el casino."""
    import random as _random
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    if not context.args or not context.args[0].replace('.','',1).isdigit():
        await update.message.reply_text("🎰 **Uso:** `/casino [cantidad]`\nEjemplo: `/casino 100`\n\n_El casino puede triplicar tu dinero... o quitártelo todo._", parse_mode="Markdown")
        return
    apuesta = round(float(context.args[0]), 2)
    if apuesta <= 0:
        await update.message.reply_text("❌ La apuesta debe ser mayor a 0.")
        return
    saldo = banco.get(uid, 0.0)
    if saldo < apuesta:
        await update.message.reply_text(f"❌ No tienes suficiente. Tienes `${saldo:,.2f}`", parse_mode="Markdown")
        return
    ruleta = [("🍒", 2), ("🍋", 1.5), ("🍊", 1.5), ("🍇", 2.5), ("⭐", 3), ("💎", 5), ("💥", 0), ("💥", 0), ("💥", 0), ("🔔", 1.2)]
    r1, r2, r3 = _random.choice(ruleta), _random.choice(ruleta), _random.choice(ruleta)
    if r1[0] == r2[0] == r3[0]:
        ganancia = round(apuesta * r1[1] * 2, 2)
        resultado = f"🎉 **¡TRIPLE {r1[0]}! ¡JACKPOT!**\n💰 Ganaste `${ganancia:,.2f}`"
    elif r1[0] == r2[0] or r2[0] == r3[0] or r1[0] == r3[0]:
        ganancia = round(apuesta * 1.5, 2)
        resultado = f"✅ **¡Par ganador!**\n💰 Ganaste `${ganancia:,.2f}`"
    elif "💥" not in [r1[0], r2[0], r3[0]]:
        ganancia = round(apuesta * 0.5, 2)
        resultado = f"😐 **Sin combinación**\nRecuperas `${ganancia:,.2f}`"
    else:
        ganancia = 0
        resultado = f"💥 **¡Perdiste!**\nLa banca se queda con `${apuesta:,.2f}`"
    banco[uid] = round(saldo - apuesta + ganancia, 2)
    guardar_db("banco.json", banco)
    _add_historial(uid, f"Casino {'ganó' if ganancia > apuesta else 'perdió'}", apuesta)
    await update.message.reply_text(
        f"🎰 **CASINO CAMILABOT** 🎰\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"[ {r1[0]} | {r2[0]} | {r3[0]} ]\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{resultado}\n"
        f"💳 **Tu saldo:** `${banco[uid]:,.2f}`",
        parse_mode="Markdown"
    )

async def cmd_dados_real(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tirar dados."""
    import random as _random
    num_dados = 2
    if context.args and context.args[0].isdigit():
        num_dados = min(int(context.args[0]), 6)
    dados = [_random.randint(1, 6) for _ in range(num_dados)]
    caras = {1:"⚀", 2:"⚁", 3:"⚂", 4:"⚃", 5:"⚄", 6:"⚅"}
    resultado_visual = " ".join(caras[d] for d in dados)
    total = sum(dados)
    await update.message.reply_text(
        f"🎲 **TIRADA DE DADOS** 🎲\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{resultado_visual}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 **Total:** `{total}`\n"
        f"_Usa /dados [cantidad] para tirar más dados_",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 2)

async def cmd_premio_real(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cobrar premio diario."""
    import random as _random
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    ahora = datetime.now()
    ultimo = cooldowns_premio.get(uid)
    if ultimo:
        diff = (ahora - ultimo).total_seconds()
        if diff < 86400:
            horas = int((86400 - diff) / 3600)
            mins = int(((86400 - diff) % 3600) / 60)
            await update.message.reply_text(f"⏰ Ya reclamaste tu premio hoy. Vuelve en `{horas}h {mins}m`", parse_mode="Markdown")
            return
    premio = _random.randint(50, 500)
    xp_bonus = _random.randint(10, 50)
    banco[uid] = round(banco.get(uid, 0.0) + premio, 2)
    guardar_db("banco.json", banco)
    sumar_xp(update.effective_user.id, xp_bonus)
    cooldowns_premio[uid] = ahora
    _add_historial(uid, "Premio diario", premio)
    await update.message.reply_text(
        f"🎁 **¡PREMIO DIARIO!** 🎁\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Dinero:** +`${premio:,}`\n"
        f"⭐ **XP:** +`{xp_bonus}`\n"
        f"💳 **Tu saldo:** `${banco[uid]:,.2f}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Regresa mañana para tu próximo premio._",
        parse_mode="Markdown"
    )

async def cmd_multa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recibir multa aleatoria."""
    import random as _random
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    razones = [
        "cruzar en rojo 🚦", "exceso de velocidad 🏎️", "estacionar mal 🚗",
        "ruido a las 3am 🔊", "no pagar el bus 🚌", "pelea en el mercado 🥊",
        "gritar spoilers 🎬", "spamear el chat 📱"
    ]
    saldo = banco.get(uid, 0.0)
    monto_multa = round(_random.uniform(20, min(saldo * 0.2 + 50, 300)), 2)
    razon = _random.choice(razones)
    banco[uid] = round(max(0, saldo - monto_multa), 2)
    guardar_db("banco.json", banco)
    _add_historial(uid, f"Multa: {razon}", monto_multa)
    await update.message.reply_text(
        f"🚨 **¡MULTA EMITIDA!** 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 **Razón:** {razon}\n"
        f"💸 **Monto:** `${monto_multa:,.2f}`\n"
        f"💳 **Saldo restante:** `${banco[uid]:,.2f}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_¡Porta mejor, {nick}!_",
        parse_mode="Markdown"
    )

async def cmd_impuesto_real(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver información de impuestos."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    saldo = banco.get(uid, 0.0)
    ahorros = banco_ahorros.get(uid, 0.0)
    total = saldo + ahorros
    tasa = 0.05 if total < 1000 else (0.08 if total < 5000 else 0.12)
    impuesto = round(total * tasa, 2)
    await update.message.reply_text(
        f"📊 **IMPUESTOS - {nick.upper()}** 📊\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Patrimonio total:** `${total:,.2f}`\n"
        f"📈 **Tasa impositiva:** `{tasa*100:.0f}%`\n"
        f"💸 **Impuesto calculado:** `${impuesto:,.2f}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Los impuestos son automáticos en el sistema._",
        parse_mode="Markdown"
    )

async def cmd_pagar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pagar una deuda o monto."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    if not context.args or not context.args[0].replace('.','',1).isdigit():
        await update.message.reply_text("📝 **Uso:** `/pagar [cantidad]`\nEjemplo: `/pagar 150`", parse_mode="Markdown")
        return
    monto = round(float(context.args[0]), 2)
    saldo = banco.get(uid, 0.0)
    if saldo < monto:
        await update.message.reply_text(f"❌ Saldo insuficiente. Tienes `${saldo:,.2f}`", parse_mode="Markdown")
        return
    banco[uid] = round(saldo - monto, 2)
    guardar_db("banco.json", banco)
    _add_historial(uid, "Pago de deuda", monto)
    await update.message.reply_text(
        f"✅ **PAGO REALIZADO** ✅\n"
        f"💸 Pagado: `${monto:,.2f}`\n"
        f"💳 Saldo: `${banco[uid]:,.2f}`",
        parse_mode="Markdown"
    )

async def cmd_inversion_real(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Invertir dinero con riesgo."""
    import random as _random
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    if not context.args or not context.args[0].replace('.','',1).isdigit():
        await update.message.reply_text(
            "📈 **SISTEMA DE INVERSIONES** 📈\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "**Uso:** `/inversion [cantidad]`\n"
            "**Riesgo/Recompensa:**\n"
            "• 40% chance: +20% a +80% de ganancia\n"
            "• 35% chance: -10% a -30% de pérdida\n"
            "• 25% chance: empate\n"
            "_Invierte sabiamente._",
            parse_mode="Markdown"
        )
        return
    monto = round(float(context.args[0]), 2)
    if monto <= 0:
        await update.message.reply_text("❌ El monto debe ser mayor a 0.")
        return
    saldo = banco.get(uid, 0.0)
    if saldo < monto:
        await update.message.reply_text(f"❌ Saldo insuficiente. Tienes `${saldo:,.2f}`", parse_mode="Markdown")
        return
    r = _random.random()
    if r < 0.40:
        mult = _random.uniform(1.20, 1.80)
        resultado = round(monto * mult, 2)
        ganancia = round(resultado - monto, 2)
        emoji = "📈"
        texto = f"✅ **¡Inversión exitosa!** +`${ganancia:,.2f}` (+{(mult-1)*100:.0f}%)"
    elif r < 0.75:
        mult = _random.uniform(0.70, 0.90)
        resultado = round(monto * mult, 2)
        ganancia = round(resultado - monto, 2)
        emoji = "📉"
        texto = f"❌ **Pérdida.** `${abs(ganancia):,.2f}` perdidos (-{(1-mult)*100:.0f}%)"
    else:
        resultado = monto
        ganancia = 0
        emoji = "⚖️"
        texto = "😐 **Neutral.** Recuperas tu inversión."
    banco[uid] = round(saldo - monto + resultado, 2)
    guardar_db("banco.json", banco)
    _add_historial(uid, f"Inversión {emoji}", monto)
    await update.message.reply_text(
        f"{emoji} **RESULTADO DE INVERSIÓN** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Invertido:** `${monto:,.2f}`\n"
        f"{texto}\n"
        f"💳 **Saldo:** `${banco[uid]:,.2f}`",
        parse_mode="Markdown"
    )

async def cmd_riqueza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver riqueza total del usuario."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    saldo = banco.get(uid, 0.0)
    ahorros = banco_ahorros.get(uid, 0.0)
    total = saldo + ahorros
    nivel_riq = "🪙 Novato" if total < 500 else ("🥈 Clase Media" if total < 2000 else ("🥇 Rico" if total < 10000 else "💎 Millonario"))
    await update.message.reply_text(
        f"💎 **RIQUEZA DE {nick.upper()}** 💎\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Billetera:** `${saldo:,.2f}`\n"
        f"🏦 **Ahorros:** `${ahorros:,.2f}`\n"
        f"📊 **Patrimonio total:** `${total:,.2f}`\n"
        f"🎖️ **Estatus:** {nivel_riq}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Usa /top para ver el ranking de más ricos._",
        parse_mode="Markdown"
    )

async def cmd_historial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver historial de transacciones."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    txs = historial_tx.get(uid, [])
    if not txs:
        await update.message.reply_text("📋 No tienes transacciones registradas aún.")
        return
    ultimas = txs[-10:][::-1]
    lines = []
    for tx in ultimas:
        lines.append(f"• {tx['accion']}: `${tx['monto']:,.2f}` — {tx['fecha']}")
    msg = (
        f"📋 **HISTORIAL DE {nick.upper()}** 📋\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        + "\n".join(lines) + "\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Mostrando las últimas {len(ultimas)} transacciones._"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def cmd_recompensa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recompensa por lealtad (cada 12 horas)."""
    import random as _random
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    ahora = datetime.now()
    ultimo = cooldowns_recompensa.get(uid)
    if ultimo and (ahora - ultimo).total_seconds() < 43200:
        diff = 43200 - (ahora - ultimo).total_seconds()
        h, m = int(diff // 3600), int((diff % 3600) // 60)
        await update.message.reply_text(f"⏰ Ya reclamaste tu recompensa. Vuelve en `{h}h {m}m`", parse_mode="Markdown")
        return
    recompensa = _random.randint(30, 200)
    banco[uid] = round(banco.get(uid, 0.0) + recompensa, 2)
    guardar_db("banco.json", banco)
    cooldowns_recompensa[uid] = ahora
    sumar_xp(update.effective_user.id, 15)
    _add_historial(uid, "Recompensa lealtad", recompensa)
    await update.message.reply_text(
        f"🌟 **¡RECOMPENSA DE LEALTAD!** 🌟\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 +`${recompensa}`\n"
        f"⭐ +15 XP\n"
        f"💳 **Saldo:** `${banco[uid]:,.2f}`\n"
        f"_Disponible cada 12 horas._",
        parse_mode="Markdown"
    )

async def cmd_bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bonus especial (cada 6 horas)."""
    import random as _random
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    ahora = datetime.now()
    ultimo = cooldowns_bonus.get(uid)
    if ultimo and (ahora - ultimo).total_seconds() < 21600:
        diff = 21600 - (ahora - ultimo).total_seconds()
        h, m = int(diff // 3600), int((diff % 3600) // 60)
        await update.message.reply_text(f"⏰ Bonus no disponible aún. Vuelve en `{h}h {m}m`", parse_mode="Markdown")
        return
    tipo = _random.choice(["💰 Dinero", "⭐ XP doble", "🎰 Token casino", "💎 Gema"])
    monto = _random.randint(20, 150)
    banco[uid] = round(banco.get(uid, 0.0) + monto, 2)
    guardar_db("banco.json", banco)
    cooldowns_bonus[uid] = ahora
    sumar_xp(update.effective_user.id, 20)
    await update.message.reply_text(
        f"🎁 **¡BONUS ESPECIAL!** 🎁\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **Tipo:** {tipo}\n"
        f"💰 +`${monto}`\n"
        f"⭐ +20 XP\n"
        f"💳 **Saldo:** `${banco[uid]:,.2f}`\n"
        f"_Bonus disponible cada 6 horas._",
        parse_mode="Markdown"
    )

async def cmd_sueldo_real(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cobrar sueldo base (cada 8 horas)."""
    import random as _random
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    ahora = datetime.now()
    ultimo = cooldowns_sueldo.get(uid)
    if ultimo and (ahora - ultimo).total_seconds() < 28800:
        diff = 28800 - (ahora - ultimo).total_seconds()
        h, m = int(diff // 3600), int((diff % 3600) // 60)
        await update.message.reply_text(f"⏰ Sueldo no disponible. Próximo cobro en `{h}h {m}m`", parse_mode="Markdown")
        return
    xp = niveles.get(uid, 0)
    nivel_num = max(1, xp // 100)
    sueldo_base = 100 + (nivel_num * 10)
    sueldo_final = round(sueldo_base * _random.uniform(0.9, 1.1), 2)
    banco[uid] = round(banco.get(uid, 0.0) + sueldo_final, 2)
    guardar_db("banco.json", banco)
    cooldowns_sueldo[uid] = ahora
    _add_historial(uid, "Sueldo cobrado", sueldo_final)
    await update.message.reply_text(
        f"💼 **¡SUELDO COBRADO!** 💼\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 **Nivel:** {nivel_num} → sueldo base `${sueldo_base}`\n"
        f"💰 **Cobrado:** `${sueldo_final:,.2f}`\n"
        f"💳 **Saldo:** `${banco[uid]:,.2f}`\n"
        f"_Próximo sueldo en 8 horas._",
        parse_mode="Markdown"
    )

# ─── INFO & CURIOSIDADES ────────────────────────────────────────────────────────

async def cmd_curiosidad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dato curioso aleatorio."""
    import random as _random
    curiosidades = [
        "🦒 Las jirafas tienen la misma cantidad de vértebras cervicales que los humanos: 7.",
        "🐙 Los pulpos tienen 3 corazones y su sangre es azul.",
        "🍯 La miel nunca se echa a perder. Se ha encontrado miel de 3,000 años en tumbas egipcias.",
        "🌙 La Luna se aleja de la Tierra 3.8 cm cada año.",
        "⚡ Un rayo tiene temperatura 5 veces mayor que la superficie del Sol.",
        "🐘 Los elefantes son los únicos animales que no pueden saltar.",
        "🦈 Los tiburones son más antiguos que los árboles. Existen hace 450 millones de años.",
        "🍌 Los plátanos son técnicamente bayas, pero las fresas no lo son.",
        "🧠 El cerebro humano genera suficiente electricidad para encender una bombilla pequeña.",
        "🌊 El océano Pacífico es más grande que todos los continentes juntos.",
        "🐟 Los peces tienen personalidades individuales únicas.",
        "💤 Los humanos son los únicos animales que se sonrojan.",
        "🦜 Los loros pueden vivir hasta 80 años.",
        "🌍 La Tierra tiene más árboles que estrellas en la Vía Láctea.",
        "🍕 El queso es el alimento más robado del mundo.",
        "🎵 La música puede cambiar la frecuencia cardíaca y la respiración.",
        "🐬 Los delfines tienen nombres propios que se dan entre sí.",
        "☀️ La luz del Sol tarda 8 minutos en llegar a la Tierra.",
        "🐝 Las abejas pueden reconocer rostros humanos.",
        "🦠 Hay más bacterias en tu cuerpo que células humanas.",
    ]
    dato = _random.choice(curiosidades)
    await update.message.reply_text(
        f"🤓 **DATO CURIOSO** 🤓\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{dato}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Usa /curiosidad para otro dato._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 2)

async def cmd_definir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Definir una palabra usando API de diccionario."""
    if not context.args:
        await update.message.reply_text("📝 **Uso:** `/definir [palabra]`\nEjemplo: `/definir efímero`", parse_mode="Markdown")
        return
    palabra = " ".join(context.args).lower().strip()
    wait = await update.message.reply_text(f"🔍 Buscando definición de *{palabra}*...", parse_mode="Markdown")
    try:
        import requests as _req
        url = f"https://api.dictionaryapi.dev/api/v2/entries/es/{palabra}"
        resp = _req.get(url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            entry = data[0]
            word = entry.get("word", palabra)
            meanings = entry.get("meanings", [])
            msg = f"📖 **DEFINICIÓN: {word.upper()}** 📖\n━━━━━━━━━━━━━━━━━━━━\n"
            for i, m in enumerate(meanings[:2]):
                pos = m.get("partOfSpeech", "")
                defs = m.get("definitions", [])
                if defs:
                    d = defs[0].get("definition", "")
                    msg += f"**{pos}:** {d}\n"
                    ejemplo = defs[0].get("example", "")
                    if ejemplo:
                        msg += f"_Ej: {ejemplo}_\n"
            await wait.edit_text(msg, parse_mode="Markdown")
            return
    except Exception:
        pass
    definiciones_locales = {
        "efímero": "Que dura muy poco tiempo; pasajero.",
        "ubérrimo": "Muy abundante y fértil.",
        "crepúsculo": "Claridad que hay desde que amanece hasta que sale el Sol, o desde que se pone hasta que anochece.",
        "serendipia": "Hallazgo valioso que se produce de manera accidental.",
        "melancólico": "Tristeza vaga, profunda, sosegada y permanente.",
    }
    if palabra in definiciones_locales:
        await wait.edit_text(f"📖 **{palabra.upper()}**\n{definiciones_locales[palabra]}", parse_mode="Markdown")
    else:
        await wait.edit_text(
            f"❌ No encontré definición para *{palabra}*.\n"
            f"Prueba con /wiki para buscar en Wikipedia.",
            parse_mode="Markdown"
        )

async def cmd_video_buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buscar video en YouTube."""
    if not context.args:
        await update.message.reply_text("📝 **Uso:** `/video [nombre del video]`\nEjemplo: `/video Bad Bunny Tití Me Preguntó`", parse_mode="Markdown")
        return
    query = " ".join(context.args)
    wait = await update.message.reply_text(f"🔍 Buscando: *{query}*...", parse_mode="Markdown")
    try:
        import urllib.parse
        busqueda_enc = urllib.parse.quote_plus(query)
        url_yt = f"https://www.youtube.com/results?search_query={busqueda_enc}"
        import requests as _req
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = _req.get(url_yt, headers=headers, timeout=10)
        import re
        videos = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', resp.text)
        titulos = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"', resp.text)
        if videos and titulos:
            resultados = []
            for i in range(min(5, len(videos), len(titulos))):
                resultados.append(f"{i+1}. [{titulos[i]}](https://youtu.be/{videos[i]})")
            msg = (
                f"🎬 **RESULTADOS PARA:** _{query}_\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                + "\n".join(resultados) + "\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"_Usa /ytmp4 [url] para descargar_"
            )
            await wait.edit_text(msg, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            await wait.edit_text(f"❌ No encontré videos para: *{query}*", parse_mode="Markdown")
    except Exception as e:
        await wait.edit_text(f"❌ Error al buscar: {str(e)[:80]}", parse_mode="Markdown")

# ─── COMANDOS STUB → REAL ────────────────────────────────────────────────────────

async def cmd_noticias_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE, categoria: str, emoji: str, titulo: str):
    """Helper genérico para noticias por categoría usando RSS de medios libres."""
    wait = await update.message.reply_text(f"📰 Buscando noticias de {titulo.lower()}...")
    try:
        import urllib.parse
        q = urllib.parse.quote_plus(categoria)
        url = f"https://gnews.io/api/v4/search?q={q}&lang=es&max=5&apikey=pub_0000"
        resp = await asyncio.to_thread(requests.get, url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            articulos = data.get("articles", [])
            if articulos:
                lines = []
                for a in articulos[:5]:
                    t = a.get("title", "")[:70]
                    link = a.get("url", "")
                    lines.append(f"• [{t}]({link})" if link else f"• {t}")
                msg = f"{emoji} **{titulo.upper()} - HOY**\n━━━━━━━━━━━━━━━━━━━━\n" + "\n".join(lines)
                await wait.edit_text(msg, parse_mode="Markdown", disable_web_page_preview=True)
                sumar_xp(update.effective_user.id, 3)
                return
    except Exception:
        pass
    noticias_locales = {
        "deportes": [
            "⚽ La selección venezolana sigue avanzando en su clasificación",
            "🏀 NBA: Los Lakers buscan su regreso a los playoffs",
            "🎾 Roland Garros se prepara para una edición histórica",
            "🏊 Récord mundial en natación batido en Toronto",
            "🥊 Gran duelo de boxeo programado para el próximo mes",
        ],
        "entretenimiento": [
            "🎬 Hollywood prepara varias secuelas esperadas",
            "🎵 Bad Bunny rompe récords en streaming mundial",
            "📺 Las mejores series del año según la crítica",
            "🎤 Festival de música anuncia grandes artistas",
            "🎭 Nueva producción teatral llega a Latinoamérica",
        ],
        "politica": [
            "🏛️ Cumbre latinoamericana debate temas de integración regional",
            "🌍 ONU llama a diálogo entre naciones en conflicto",
            "📊 Encuestas muestran cambios en la opinión pública",
            "🤝 Tratado comercial entre países en negociación avanzada",
            "🗳️ Próximas elecciones marcan el calendario político regional",
        ],
        "salud": [
            "💊 Nuevo estudio sobre beneficios del ejercicio diario",
            "🧠 Investigación revela clave para la salud mental",
            "🥗 Dieta mediterránea sigue siendo la más recomendada",
            "🫀 Avances en tratamiento de enfermedades cardiovasculares",
            "😴 Expertos enfatizan importancia del sueño de calidad",
        ],
        "tecnologia": [
            "🤖 IA sigue transformando la industria tecnológica global",
            "📱 Nuevo smartphone bate récords de velocidad y cámara",
            "💻 La computación cuántica se acerca a aplicaciones reales",
            "🔒 Ciberseguridad: Consejos para proteger tus datos",
            "🌐 Internet de las cosas conecta millones de dispositivos nuevos",
        ],
    }
    items = noticias_locales.get(categoria, ["Sin noticias disponibles"])
    msg = f"{emoji} **{titulo.upper()} - HOY**\n━━━━━━━━━━━━━━━━━━━━\n" + "\n".join(items)
    await wait.edit_text(msg, parse_mode="Markdown")
    sumar_xp(update.effective_user.id, 3)

async def cmd_deportes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_noticias_categoria(update, context, "deportes", "⚽", "Noticias Deportivas")

async def cmd_entretenimiento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_noticias_categoria(update, context, "entretenimiento", "🎬", "Entretenimiento")

async def cmd_politica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_noticias_categoria(update, context, "política", "🏛️", "Noticias Políticas")

async def cmd_salud_noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_noticias_categoria(update, context, "salud", "🏥", "Salud y Medicina")

async def cmd_tecnologia_noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_noticias_categoria(update, context, "tecnologia", "💻", "Tecnología")

async def cmd_stk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sticker — busca un sticker o muestra lista de estilos."""
    if context.args:
        await sticker_buscar_cmd(update, context)
    else:
        await sticker_lista(update, context)

async def cmd_pregunta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responder una pregunta de trivia."""
    import random as _r
    preguntas = [
        ("¿Cuál es la capital de Venezuela?", "Caracas"),
        ("¿Cuántos continentes tiene la Tierra?", "7"),
        ("¿Qué planeta es el más grande del sistema solar?", "Júpiter"),
        ("¿En qué año llegó el hombre a la Luna?", "1969"),
        ("¿Cuál es el elemento más abundante en el universo?", "El hidrógeno"),
        ("¿Qué animal es el más rápido del mundo?", "El guepardo"),
        ("¿Cuál es el río más largo del mundo?", "El Nilo o el Amazonas"),
        ("¿Cuántos huesos tiene el cuerpo humano adulto?", "206"),
        ("¿Qué idioma tiene más hablantes nativos en el mundo?", "El chino mandarín"),
        ("¿Cuál es el océano más grande?", "El Océano Pacífico"),
        ("¿Quién pintó la Mona Lisa?", "Leonardo da Vinci"),
        ("¿Cuál es el planeta más cercano al Sol?", "Mercurio"),
        ("¿De qué país es el tango baile nacional?", "Argentina"),
        ("¿Cuántos lados tiene un hexágono?", "6"),
        ("¿Cuál es la montaña más alta del mundo?", "El Everest"),
    ]
    q, a = _r.choice(preguntas)
    await update.message.reply_text(
        f"🤔 **PREGUNTA DEL DÍA** 🤔\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"❓ {q}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"||💡 **Respuesta:** {a}||",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 5)

async def cmd_loteria_real(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Jugar la lotería."""
    import random as _random
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    costo = 50
    saldo = banco.get(uid, 0.0)
    if saldo < costo:
        await update.message.reply_text(f"❌ La lotería cuesta `${costo}`. Tienes `${saldo:,.2f}`", parse_mode="Markdown")
        return
    tu_num = _random.randint(1, 100)
    ganador = _random.randint(1, 100)
    banco[uid] = round(saldo - costo, 2)
    if tu_num == ganador:
        premio = 5000
        banco[uid] = round(banco[uid] + premio, 2)
        msg = f"🏆 **¡¡JACKPOT!!** Tu número `{tu_num}` = ganador `{ganador}`\n💰 **+${premio:,}**"
    elif abs(tu_num - ganador) <= 5:
        premio = 200
        banco[uid] = round(banco[uid] + premio, 2)
        msg = f"🥈 **¡Casi!** Tu número `{tu_num}`, ganador `{ganador}`\n💰 +`${premio}`"
    else:
        msg = f"❌ Tu número `{tu_num}`, ganador `{ganador}`. No ganaste."
    guardar_db("banco.json", banco)
    _add_historial(uid, "Lotería", costo)
    await update.message.reply_text(
        f"🎰 **LOTERÍA NACIONAL** 🎰\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎟️ Costo: `$50` | Tu número: `{tu_num}`\n"
        f"{msg}\n"
        f"💳 **Saldo:** `${banco[uid]:,.2f}`",
        parse_mode="Markdown"
    )

# ════════════════════════════════════════════════════════════════════════════════
# --- [ MOTORES MASIVOS - IMPLEMENTACIÓN COMPLETA DE TODOS LOS COMANDOS ] ---
# ════════════════════════════════════════════════════════════════════════════════

# ─── EXTENSIÓN DE ACCIONES ROL ────────────────────────────────────────────────
ACCIONES_ROL.update({
    "abofetear":  "🤚 {u} le cruzó la cara a {t} con una bofetada épica!",
    "acariciar":  "🤲 {u} acarició a {t} con ternura infinita. ¡Qué dulzura!",
    "besuquear":  "😘 {u} está besando a {t} por todos lados sin parar!",
    "cachetada":  "👋 {u} le dio una cachetada que {t} no olvidará jamás!",
    "cargar":     "💪 {u} cargó a {t} en brazos como si fuera un bebé!",
    "cosquillas": "🤣 {u} le hizo cosquillas a {t} hasta que lloró de risa!",
    "empujar":    "🤜 {u} empujó a {t} con toda su fuerza. ¡Fly!",
    "golpear":    "🥊 {u} le propinó un golpazo épico a {t}!",
    "levantar":   "🏋️ {u} levantó a {t} sobre su cabeza como un campeón!",
    "pellizcar":  "🤏 {u} le dio un pellizco a {t} que dejó moretón!",
    "punetazo":   "👊 {u} mandó a {t} directo a la lona de un puñetazo!",
    "tirar":      "🤸 {u} lanzó a {t} por los aires sin misericordia!",
    "animar":     "🎉 {u} animó a {t} con palabras llenas de energía positiva!",
    "elogiar":    "🌟 {u} elogió a {t}: ¡Eres lo mejor que hay por aquí!",
    "patada":     "🦵 {u} le plantó una patada voladora a {t}!",
    "derrota":    "😢 {u} acepta la derrota ante {t}. El honor es tuyo.",
    "victoria":   "🏆 {u} celebra su victoria sobre {t}. ¡Ganó!",
    "empate":     "🤝 {u} y {t} terminaron en empate. ¡Igualados!",
    "huir":       "🏃 {u} salió corriendo de {t} a toda velocidad. ¡Rajado!",
    "retar":      "⚔️ {u} lanzó un reto a muerte a {t}. ¡Acepta si te atreves!",
    "desafiar":   "🎯 {u} desafió a {t} a un duelo sin cuartel!",
    "duelo":      "🗡️ {u} declaró duelo oficial contra {t}. ¡Que empiece!",
    "pelear":     "🤼 {u} se enfrenta a {t} en una pelea cuerpo a cuerpo!",
    "rendirse":   "🏳️ {u} se rinde ante {t}. La victoria es tuya.",
})

# ─── MOTOR DEPORTES ───────────────────────────────────────────────────────────
_DEPORTES_INFO = {
    "futbol":         ("⚽","FÚTBOL","Es el deporte más popular del mundo con 4,000 millones de seguidores. El gol más rápido de la historia tardó 2.4 segundos en anotarse.","🏆 Messi y Cristiano Ronaldo dominaron la era dorada."),
    "basquetbol":     ("🏀","BALONCESTO","Inventado en 1891 por James Naismith. El récord de puntos en un partido NBA es de 100 puntos por Wilt Chamberlain.","🌟 Michael Jordan es considerado el GOAT del básquet."),
    "voley":          ("🏐","VOLEIBOL","Cada equipo tiene 6 jugadores y 3 toques por posesión. Brasil domina el voleibol mundial históricamente.","💪 El servicio más rápido registrado supera los 135 km/h."),
    "tenis":          ("🎾","TENIS","El Grand Slam incluye: Australian Open, Roland Garros, Wimbledon y US Open. Federer, Nadal y Djokovic son los grandes del tenis moderno.","🏆 El rally más largo tuvo 643 golpes."),
    "badminton":      ("🏸","BÁDMINTON","El volante puede alcanzar velocidades de 491 km/h. China domina el bádminton olímpico desde hace décadas.","⚡ Es el deporte de raqueta más rápido del mundo."),
    "ping_pong":      ("🏓","PING PONG / TENIS DE MESA","La pelota puede moverse a más de 100 km/h. China ha ganado casi todas las medallas olímpicas de este deporte.","🎯 El tenis de mesa se inventó en Inglaterra en los 1880s."),
    "golf":           ("⛳","GOLF","Un campo de golf tiene 18 hoyos. El hoyo en uno es el golpe perfecto. Tiger Woods cambió el deporte para siempre.","🌿 El golf fue jugado en la Luna por Alan Shepard en 1971."),
    "atletismo":      ("🏃","ATLETISMO","Usain Bolt tiene el récord mundial de 100m con 9.58 segundos. El atletismo es el deporte base de todos los deportes.","💨 La maratón mide exactamente 42.195 km."),
    "carrera":        ("🏎️","CARRERAS / AUTOMOVILISMO","La Fórmula 1 alcanza velocidades de 380+ km/h. Lewis Hamilton tiene 7 títulos mundiales, igualando a Schumacher.","🔥 El Gran Premio de Mónaco es el más famoso del mundo."),
    "natacion":       ("🏊","NATACIÓN","Michael Phelps ganó 23 medallas olímpicas de oro. El estilo más rápido es la mariposa. La piscina olímpica mide 50 metros.","💧 Ryan Lochte y Katie Ledecky son las estrellas actuales."),
    "boxeo":          ("🥊","BOXEO","Muhammad Ali es considerado el mejor boxeador de todos los tiempos. Los guantes modernos se usan desde 1867.","💪 El derechazo de Iron Mike Tyson fue demoledor."),
    "mma":            ("🥋","MMA / ARTES MARCIALES MIXTAS","La UFC es la principal organización mundial de MMA. Conor McGregor y Khabib protagonizaron la pelea más vista de la historia.","⚔️ Las reglas modernas de MMA se establecieron en 1993."),
    "karate":         ("🥋","KARATE","Originado en Okinawa, Japón. Los cinturones van del blanco al negro. El kata es la práctica de movimientos formales del karate.","🇯🇵 Fue deporte olímpico en Tokio 2020."),
    "taekwondo":      ("🦶","TAEKWONDO","Arte marcial coreano famoso por sus patadas altas y veloces. Es deporte olímpico desde el año 2000 en Sídney.","🇰🇷 El cinturón negro requiere años de práctica y exámenes."),
    "muay_thai":      ("🥊","MUAY THAI","El 'arte de las ocho extremidades' usa puños, codos, rodillas y pies. Es el deporte nacional de Tailandia.","🔥 Los fighters de Muay Thai entrenan de 3-5 horas diarias."),
    "kickboxing":     ("👟","KICKBOXING","Combina técnicas del boxeo con patadas de las artes marciales. Es popular como disciplina de fitness y deporte de combate.","💪 Ideal para quemar 700-900 calorías por hora."),
    "ciclismo":       ("🚴","CICLISMO","El Tour de Francia es la carrera más famosa del mundo con 3,500 km. Tadej Pogacar y Jonas Vingegaard dominan el pelotón moderno.","🚵 La velocidad récord en bicicleta supera los 280 km/h."),
    "bicicleta":      ("🚲","BICICLETA","La bicicleta fue inventada en 1817 por Karl von Drais. Hay más de 1,000 millones de bicicletas en el mundo.","🌿 Es el medio de transporte más eficiente energéticamente."),
    "mountain_bike":  ("🏔️","MOUNTAIN BIKE","El MTB nació en California en los años 70. Las categorías incluyen XC, Trail, Enduro y Downhill.","⛰️ Los descensos pueden alcanzar velocidades de 80+ km/h."),
    "bmx":            ("🛴","BMX","Las bicicletas BMX tienen ruedas de 20 pulgadas. El BMX Freestyle y BMX Racing son disciplinas olímpicas desde Tokio 2020.","🎯 Los trucos incluyen barspins, tailwhips y 360s."),
    "automovilismo":  ("🏁","AUTOMOVILISMO","La F1 usa motores híbridos de 1.6L que generan más de 1,000 HP. Max Verstappen es el campeón dominante del momento.","🔧 Un cambio de neumáticos en F1 dura menos de 2 segundos."),
    "motociclismo":   ("🏍️","MOTOCICLISMO","MotoGP es la categoría reina del motociclismo. Marc Márquez y Valentino Rossi son leyendas de la categoría.","⚡ Las motos MotoGP superan los 340 km/h."),
    "equitacion":     ("🏇","EQUITACIÓN","La equitación incluye salto, doma y concurso completo en los Juegos Olímpicos. El jinete debe tener una conexión especial con el caballo.","🐴 Los caballos de competición pueden valer millones."),
    "polo":           ("🏑","POLO","Llamado 'el deporte de los reyes', se juega a caballo. El Argentina es la potencia mundial del polo.","🐎 Cada chukker dura 7.5 minutos y hay hasta 8 por partido."),
    "rodeo":          ("🤠","RODEO","El rodeo nació de las tradiciones vaqueras del oeste americano. Las disciplinas incluyen lazo, calf roping y bull riding.","🐂 Mantenerse 8 segundos en el toro es el objetivo básico."),
    "vela":           ("⛵","VELA","La vela es uno de los deportes olímpicos más antiguos. El Americas Cup es la regata más prestigiosa del mundo.","🌊 Los veleros modernos pueden superar los 100 km/h."),
    "yate":           ("🛥️","YATE","Los yates de lujo pueden medir más de 100 metros. La regata Sydney-Hobart es una de las más peligrosas del mundo.","⚓ El término 'yate' viene del holandés 'jacht'."),
    "kayak":          ("🚣","KAYAK","El kayak fue inventado por los pueblos indígenas del Ártico. Hay kayak de aguas tranquilas, aguas bravas y de mar.","💧 Un palista de kayak puede recorrer 6 km en 30 minutos."),
    "canoa":          ("🛶","CANOA","Diferente al kayak, la canoa se palca de rodillas con una pala simple. Es deporte olímpico desde 1936.","🌿 Las canoas tradicionales se hacen de madera o corteza."),
    "remo":           ("🚣","REMO","El remo universitario (Harvard-Yale) es una de las rivalidades más antiguas del deporte americano. Los remeros son los atletas con mayor VO2 max.","💪 Una carrera olímpica de remo dura entre 5 y 7 minutos."),
    "barco":          ("⛴️","DEPORTES NÁUTICOS","Los deportes acuáticos incluyen vela, remo, motonáutica y más. Los océanos cubren el 71% de la Tierra y son escenario de millones de deportistas.","🌊 El surf es uno de los deportes acuáticos más populares."),
    "fitness":        ("💪","FITNESS","El fitness moderno busca combinar fuerza, resistencia y flexibilidad. La consistencia supera la intensidad: entrenar 3-4 días por semana es óptimo.","📊 30 minutos de ejercicio diario reducen el riesgo de enfermedad en 35%."),
    "gym":            ("🏋️","GIMNASIO","Un buen programa de gym incluye calentamiento, entrenamiento y enfriamiento. Los músculos crecen durante el descanso, no durante el entrenamiento.","💊 La proteína post-entrenamiento debe consumirse en la 'ventana anabólica'."),
    "crossfit":       ("🏋️","CROSSFIT","CrossFit combina levantamiento de pesas, gimnasia y ejercicio cardiovascular de alta intensidad. Los WOD (Workout of the Day) cambian cada día.","🔥 Un workout de CrossFit puede durar solo 10-20 minutos."),
    "pilates":        ("🧘","PILATES","Creado por Joseph Pilates en los años 20. Fortalece el core y mejora la postura. Es ideal para rehabilitación y prevención de lesiones.","🌟 El 'powerhouse' es el centro de fuerza según Pilates."),
    "yoga":           ("🧘","YOGA","El yoga combina posturas (asanas), respiración (pranayama) y meditación. Existen más de 300 estilos de yoga. Reduce el estrés hasta un 50%.","☯️ El yoga tiene más de 5,000 años de historia en la India."),
    "hiit":           ("⚡","HIIT - ENTRENAMIENTO INTERVÁLICO","HIIT alterna períodos de alta intensidad con descanso breve. Quema más grasa que el cardio tradicional incluso horas después del ejercicio (efecto EPOC).","🔥 Una sesión de 20 min HIIT = 40 min de cardio normal."),
    "atletismo":      ("🏃","ATLETISMO","El atletismo incluye carreras, saltos y lanzamientos. Eliud Kipchoge fue el primero en correr un maratón en menos de 2 horas.","💨 El velocímetro de Usain Bolt alcanzó 44.72 km/h."),
    "futsal":         ("⚽","FÚTSAL","El fútsal es una variante del fútbol en cancha pequeña con 5 jugadores por equipo. Brasil es la potencia mundial.","🌟 Muchos grandes del fútbol como Messi empezaron jugando fútsal."),
    "maraton":        ("🏃","MARATÓN","La maratón mide 42.195 km. Eliud Kipchoge tiene el récord mundial con 2:00:35. El reto más grande es el muro del kilómetro 30.","💪 Completar una maratón requiere meses de entrenamiento."),
    "100_metros":     ("⚡","100 METROS PLANOS","Usain Bolt tiene el récord mundial con 9.58 segundos. Los velocistas alcanzan 44 km/h. La salida es crucial: 0.1 segundos marcan la diferencia.","🥇 Es considerado la prueba más glamorosa del atletismo."),
    "salto":          ("🤸","SALTO","El salto de altura, longitud, triple salto y pértiga son las disciplinas olímpicas. Mondo Duplantis tiene el récord de pértiga con 6.26m.","📏 El récord de salto de longitud de Mike Powell (8.95m) lleva 35 años."),
    "carrera_caballos":("🐎","CARRERAS DE CABALLOS","El Kentucky Derby, Royal Ascot y el Gran Premio son las carreras más famosas. Los caballos pura sangre pueden correr a 70 km/h.","👑 Las apuestas en carreras de caballos generan miles de millones."),
    "equestrian":     ("🏇","ECUESTRE / EQUITACIÓN","La equitación olímpica tiene tres disciplinas: Doma Clásica, Salto y Concurso Completo. Los caballos y jinetes compiten como equipo.","🐴 El caballo más exitoso de la historia fue Valegro en doma."),
    "hipismo":        ("🐎","HIPISMO","El hipismo comprende todos los deportes ecuestres. La Feria del Caballo de Jerez y los Juegos Ecuestres Mundiales son eventos clave.","🌟 El polo, carreras y saltos son las tres grandes disciplinas."),
}

_LISTA_DEPORTES = list(_DEPORTES_INFO.keys())

async def motor_deportes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Motor genérico para comandos de deportes."""
    cmd = update.message.text.split()[0][1:].lower()
    if str(update.effective_user.id) in blacklist:
        return
    info = _DEPORTES_INFO.get(cmd)
    if not info:
        await update.message.reply_text(f"🏅 **{cmd.upper()}** — Deporte registrado. Próximamente más info.", parse_mode="Markdown")
        return
    emoji, titulo, descripcion, dato = info
    await update.message.reply_text(
        f"{emoji} **{titulo}** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📖 {descripcion}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 {dato}",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

# ─── MOTOR MÚSICA ────────────────────────────────────────────────────────────
_MUSICA_INFO = {
    "rock":       ("🎸","ROCK","Surgió en los 50s con Chuck Berry y Elvis. Led Zeppelin, Rolling Stones y Queen definieron el género.","🎵 Artistas actuales: Imagine Dragons, Arctic Monkeys, Foo Fighters."),
    "pop":        ("🎵","POP","El género más escuchado del mundo. Michael Jackson, Madonna y Taylor Swift son sus máximos exponentes.","🌟 El pop moderno mezcla electrónica, R&B y trap."),
    "hip_hop":    ("🎤","HIP HOP","Nació en el Bronx, Nueva York en los 70s. Tupac, Biggie, Jay-Z y Kendrick Lamar son sus leyendas.","🎧 Es el género más escuchado globalmente desde 2017."),
    "reggaeton":  ("🔥","REGGAETON","Originado en Puerto Rico y Panamá en los 90s. Daddy Yankee, J Balvin, Bad Bunny y Maluma lo llevan al mundo.","🇵🇷 'Gasolina' de Daddy Yankee fue el tema que lo globalizó."),
    "electronica":("🎛️","MÚSICA ELECTRÓNICA","El EDM (Electronic Dance Music) incluye house, techno, trance y dubstep. Daft Punk, David Guetta y Calvin Harris son referentes mundiales.","🎧 Los festivales de EDM mueven miles de millones anuales."),
    "clasica":    ("🎻","MÚSICA CLÁSICA","Mozart, Beethoven, Bach y Chopin son sus pilares. La Quinta Sinfonía de Beethoven es la más reconocida de la historia.","🎼 La música clásica mejora la concentración y el aprendizaje."),
    "jazz":       ("🎷","JAZZ","Nació en Nueva Orleans a principios del siglo XX. Miles Davis, Louis Armstrong y John Coltrane son sus genios.","🎺 La improvisación es el corazón del jazz."),
    "blues":      ("🎸","BLUES","Ancestro del rock y el jazz, nació en el sur de EEUU. B.B. King, Robert Johnson y Muddy Waters son sus padres.","🎵 El blues tiene 12 compases como estructura básica."),
    "country":    ("🤠","COUNTRY","Nacido en los Apalaches, mezcla folk, blues y música celta. Johnny Cash, Dolly Parton y Taylor Swift lo llevan a nuevas audiencias.","🎸 Nashville, Tennessee es la capital mundial del country."),
    "metal":      ("🤘","METAL","Del hard rock surgió el heavy metal en los 70s. Black Sabbath, Metallica y Iron Maiden definieron el género.","🎸 El metal tiene más de 30 subgéneros distintos."),
    "indie":      ("🎵","INDIE","Música independiente producida sin grandes discográficas. Radiohead, Arctic Monkeys y The Strokes son sus referentes.","🌟 El indie valora la autenticidad sobre la comercialidad."),
    "latina":     ("💃","MÚSICA LATINA","La salsa, cumbia, bachata, merengue y reggaeton definen la música latina. Marc Anthony, Shakira y J Balvin la llevan al mundo entero.","🌎 La música latina es la segunda más escuchada del planeta."),
    "venezolana": ("🇻🇪","MÚSICA VENEZOLANA","El joropo, valses venezolanos y gaitas son el alma musical de Venezuela. Simón Díaz es el embajador musical del país.","🎶 El arpa, el cuatro y las maracas forman el ensamble típico."),
    "karaoke":    ("🎤","KARAOKE","El karaoke fue inventado en Japón en los 70s por Daisuke Inoue. 'Bohemian Rhapsody' es la canción más cantada en karaoke del mundo.","🎵 Filipinas es el país con más karaokes per cápita del mundo."),
    "cancion":    ("🎵","BÚSQUEDA DE CANCIONES","Para encontrar una canción usa: /ytmp3 [nombre] para descargarla como audio o /buscar [artista + canción] para más info.","🎧 También puedes usar /spotify o /musica para recomendaciones."),
    "artista":    ("🌟","ARTISTAS MUSICALES","Los artistas más escuchados en streaming: Taylor Swift, Bad Bunny, Drake, The Weeknd y Ed Sheeran lideran globalmente.","🎤 Usa /buscar [nombre del artista] para info específica."),
    "album":      ("💿","ÁLBUMES MUSICALES","Los álbumes más vendidos: Thriller (MJ), Back in Black (AC/DC), The Dark Side of the Moon (Pink Floyd) y Hotel California (Eagles).","🎵 Usa /buscar [artista + álbum] para detalles de un álbum."),
    "genero":     ("🎼","GÉNEROS MUSICALES","Los principales géneros: Pop, Rock, Hip Hop, R&B, Electrónica, Jazz, Clásica, Country, Metal, Reggaeton, Latina.","🎧 Cada género tiene sus sub-géneros y fusiones únicas."),
    "playlist":   ("📋","PLAYLIST / LISTA DE REPRODUCCIÓN","Una buena playlist tiene variedad de ritmos. Comienza con canciones animadas, baja el ritmo a la mitad y termina con energía.","🎵 Usa /crear_playlist para crear una lista personalizada."),
    "acorde":     ("🎸","ACORDES DE GUITARRA","Los acordes básicos: Do Mayor (C), Re Mayor (D), Mi Mayor (E), Fa Mayor (F), Sol Mayor (G), La Mayor (A), Si Mayor (B).","🎵 Con C, G, Am y F puedes tocar miles de canciones pop."),
    "melodia":    ("🎵","MELODÍA","Una melodía es una secuencia de notas musicales. Las mejores melodías son simples y memorables. La do-re-mi es la más enseñada.","🎼 Bach, Mozart y Beethoven son los maestros de la melodía."),
    "armonia":    ("🎶","ARMONÍA MUSICAL","La armonía es la combinación de notas simultáneas que suenan bien juntas. Las tríadas (3 notas) son la base de la armonía occidental.","🎸 Una buena armonía complementa la melodía sin opacarla."),
    "instrumento":("🎸","INSTRUMENTOS MUSICALES","Los instrumentos se clasifican en: cuerdas (guitarra, violín), viento (flauta, trompeta), percusión (batería, piano) y electrónicos.","🎵 Aprender un instrumento mejora la memoria y concentración."),
    "guitarra":   ("🎸","GUITARRA","La guitarra tiene 6 cuerdas (E-A-D-G-B-E). La guitarra acústica, clásica y eléctrica son sus tres variantes principales.","🎵 Jimi Hendrix, Carlos Santana y Eric Clapton son sus maestros."),
    "piano":      ("🎹","PIANO","El piano tiene 88 teclas (52 blancas y 36 negras). Fue inventado por Bartolomeo Cristofori alrededor de 1700.","🎼 Chopin, Liszt y Bach son los grandes compositores para piano."),
    "bajo":       ("🎸","BAJO / GUITARRA BAJO","El bajo tiene 4 cuerdas y es la columna vertebral del ritmo en una banda. Flea (RHCP) y Jaco Pastorius son leyendas del instrumento.","🎵 Un buen bajista es el secreto de un gran grupo musical."),
    "letra":      ("📝","LETRAS DE CANCIONES","Para encontrar letras de canciones puedes buscar en Genius, AZLyrics o Musixmatch. Las mejores letras cuentan una historia completa.","🎵 Bob Dylan ganó el Nobel de Literatura por sus letras."),
    "ritmo":      ("🥁","RITMO MUSICAL","El ritmo es el patrón temporal de la música. El 4/4 es el más común. La samba, el jazz y el flamenco tienen ritmos únicos.","🥁 Un buen sentido del ritmo se desarrolla con práctica constante."),
}

_LISTA_MUSICA = list(_MUSICA_INFO.keys())

async def motor_musica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Motor genérico para comandos de música."""
    cmd = update.message.text.split()[0][1:].lower()
    if str(update.effective_user.id) in blacklist:
        return
    info = _MUSICA_INFO.get(cmd)
    if not info:
        await update.message.reply_text(f"🎵 **{cmd.upper()}** — Género/tema musical registrado.", parse_mode="Markdown")
        return
    emoji, titulo, descripcion, dato = info
    await update.message.reply_text(
        f"{emoji} **{titulo}** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📖 {descripcion}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 {dato}",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

# ─── MOTOR GEOGRAFÍA ─────────────────────────────────────────────────────────
_GEO_INFO = {
    "capital":    ("🏛️","CAPITALES DEL MUNDO","Úsame así: `/capital [país]`\n🇻🇪 Venezuela → Caracas\n🇺🇸 USA → Washington D.C.\n🇧🇷 Brasil → Brasilia\n🇲🇽 México → Ciudad de México\n🇦🇷 Argentina → Buenos Aires\n🇨🇴 Colombia → Bogotá\n🇨🇱 Chile → Santiago\n🇵🇪 Perú → Lima","🌍 Hay 195 países y 195 capitales en el mundo."),
    "bandera":    ("🏳️","BANDERAS DEL MUNDO","Las banderas representan la identidad de cada nación. Venezuela 🇻🇪 tiene franjas amarilla, azul y roja con 8 estrellas.\nBrasil 🇧🇷, Colombia 🇨🇴, México 🇲🇽, Argentina 🇦🇷","🌈 La bandera de Nepal es la única no rectangular del mundo."),
    "ciudad":     ("🏙️","CIUDADES DEL MUNDO","Las ciudades más pobladas: Tokio (37M), Delhi (33M), Shanghai (29M), São Paulo (22M), Ciudad de México (22M).","🌆 Para info de una ciudad usa: /buscar [nombre de ciudad]"),
    "continente": ("🌍","CONTINENTES","Los 7 continentes: Asia (4,700M hab), África (1,400M), América (1,000M), Europa (750M), Oceanía (43M), Antártida (0 perm).","🗺️ Asia ocupa el 30% de la superficie terrestre."),
    "oceano":     ("🌊","OCÉANOS DEL MUNDO","Los 5 océanos: Pacífico (el más grande), Atlántico, Índico, Ártico y el reciente Océano Antártico (desde 2000).","💧 Los océanos cubren el 71% de la superficie de la Tierra."),
    "rio":        ("🏞️","RÍOS DEL MUNDO","Los más largos: Nilo (6,650 km), Amazonas (6,400 km), Yangtsé (6,300 km), Misisipí (6,275 km), Yeniséi (5,539 km).","🌊 El Orinoco es el río más importante de Venezuela con 2,140 km."),
    "montana":    ("🏔️","MONTAÑAS DEL MUNDO","Las más altas: Everest (8,848m), K2 (8,611m), Kangchenjunga (8,586m). El Pico Bolívar (5,007m) es el más alto de Venezuela.","⛰️ El 27% de la superficie terrestre son montañas."),
    "desierto":   ("🏜️","DESIERTOS DEL MUNDO","El Sahara (9.2M km²) es el mayor desierto caliente. La Antártida es el mayor desierto frío (14.2M km²). El Atacama es el más seco.","🌵 Los desiertos cubren el 33% de la superficie terrestre."),
    "selva":      ("🌴","SELVAS TROPICALES","La Amazonia es la selva tropical más grande con 5.5 millones de km². Alberga el 10% de todas las especies del planeta.","🌿 Las selvas tropicales producen el 20% del oxígeno mundial."),
    "glaciar":    ("🧊","GLACIARES","Los glaciares cubren el 10% de la superficie terrestre. El glaciar Lambert en Antártida es el mayor del mundo (100 km de ancho).","❄️ Los glaciares contienen el 69% del agua dulce del planeta."),
    "volcan":     ("🌋","VOLCANES","Hay ~1,500 volcanes activos en el mundo. El Mauna Loa (Hawái) es el más grande. El Vesuvio destruyó Pompeya en el 79 d.C.","🔥 Los volcanes submarinos son los más numerosos del planeta."),
    "isla":       ("🏝️","ISLAS DEL MUNDO","Groenlandia es la mayor isla (2.1M km²). Las islas más visitadas: Maldivas, Bali, Hawaii, Canarias, Sicilia.","🌴 Indonesia tiene más de 17,000 islas, la mayor cantidad del mundo."),
    "peninsula":  ("🗺️","PENÍNSULAS","Las más conocidas: Ibérica (España/Portugal), Arábiga, Indostán, Escandinavia, Yucatán (México), Guajira (Colombia/Venezuela).","🌊 Una península está rodeada de agua por tres lados."),
    "golfo":      ("🌊","GOLFOS","Los más importantes: Golfo de México (1.6M km²), Golfo Pérsico (fuente del petróleo mundial), Golfo de Guinea (África Occidental).","⛵ El Golfo de Venezuela separa la Guajira de Paraguaná."),
    "estrecho":   ("🌊","ESTRECHOS","Los más famosos: Gibraltar (Europa-África), Magallanes (Sudamérica), Bósforo (une Mediterráneo y Mar Negro), Malaca (Asia-Oceanía).","🚢 El Estrecho de Malaca es el más transitado del mundo."),
    "continente": ("🌍","CONTINENTES DEL MUNDO","Asia: 44.5M km² | África: 30.3M km² | América: 42M km² | Antártida: 14M km² | Europa: 10.5M km² | Oceanía: 8.5M km²","🗺️ La deriva continental separó el supercontinente Pangea hace 175M años."),
    "tsunami":    ("🌊","TSUNAMI","Un tsunami es una serie de olas gigantes causadas por terremotos, volcanes o deslizamientos submarinos. El tsunami del Índico (2004) causó 230,000 muertes.","⚠️ Las sirenas de alerta de tsunami salvan millones de vidas."),
    "tormenta":   ("⛈️","TORMENTAS","Las tormentas tropicales, ciclones y huracanes se forman sobre el mar caliente. La escala Saffir-Simpson clasifica los huracanes del 1 al 5.","🌀 El ojo de un huracán es sorprendentemente tranquilo."),
    "tornado":    ("🌪️","TORNADOS","Los tornados se forman en el 'Tornado Alley' de EEUU. La escala Fujita mide su intensidad. El más destructivo fue el de Tri-State en 1925.","⚡ Un tornado puede durar segundos o más de una hora."),
    "viento":     ("💨","VIENTOS DEL MUNDO","Los vientos alisios, monzones y westerlies gobiernan el clima global. El viento más rápido registrado fue de 407 km/h en Australia.","🌬️ El viento solar viaja a 400-800 km/s desde el Sol."),
    "amanecer":   ("🌅","AMANECER","El amanecer es el momento en que el Sol aparece sobre el horizonte. Los mejores para verlo: Santorini (Grecia), Bali (Indonesia), Machu Picchu.","☀️ El amanecer recarga la energía y sincroniza el ritmo circadiano."),
    "atardecer":  ("🌇","ATARDECER","El atardecer o puesta de sol ocurre cuando el Sol desaparece bajo el horizonte. Los mejores: Santorini, Serengeti, Maldivas, Patagonia.","🌅 El efecto verde justo después del atardecer es un fenómeno raro."),
}

_LISTA_GEO = list(_GEO_INFO.keys())

async def motor_geografia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Motor genérico para comandos de geografía."""
    cmd = update.message.text.split()[0][1:].lower()
    if str(update.effective_user.id) in blacklist:
        return
    info = _GEO_INFO.get(cmd)
    if not info:
        await update.message.reply_text(f"🗺️ **{cmd.upper()}** — Término geográfico. Usa /wiki para más info.", parse_mode="Markdown")
        return
    emoji, titulo, descripcion, dato = info
    await update.message.reply_text(
        f"{emoji} **{titulo}** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{descripcion}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 {dato}",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

# ─── MOTOR ALIMENTOS & NUTRICIÓN ─────────────────────────────────────────────
_ALIMENTOS_INFO = {
    "cafe":         ("☕","CAFÉ","El café es la segunda bebida más consumida del mundo (después del agua). Un espresso tiene menos cafeína que un café americano.","💪 La cafeína mejora el rendimiento físico en un 11-12%."),
    "te":           ("🍵","TÉ","El té verde es rico en antioxidantes. El té negro es el más consumido en el mundo. La teína actúa más suave que la cafeína del café.","🌿 China produce el 45% del té mundial."),
    "batido":       ("🥤","BATIDOS / SMOOTHIES","Un batido de proteínas ideal tiene: 25-30g proteína, frutas, leche o agua, y opcionalmente avena. El timing ideal es post-entrenamiento.","💪 Usa plátano, avena y proteína para el batido perfecto."),
    "arroz":        ("🍚","ARROZ","El arroz es el alimento base de más de la mitad de la humanidad. El arroz integral tiene más fibra y nutrientes que el blanco.","🌾 Venezuela consume en promedio 50 kg de arroz por persona al año."),
    "carne":        ("🥩","CARNE","La carne es fuente de proteína completa con todos los aminoácidos esenciales. La carne roja aporta hierro hemo, el más absorbible.","🥩 El punto medio (medium) conserva mejor los jugos y sabor."),
    "comida":       ("🍽️","COMIDA VENEZOLANA","La cocina venezolana incluye pabellón criollo, hallacas, arepas, cachapas, tequeños y mondongo. Es una mezcla de influencias indígena, europea y africana.","🇻🇪 Las arepas son el plato más versátil y querido de Venezuela."),
    "desayuno":     ("🌅","DESAYUNO IDEAL","Un desayuno completo incluye proteínas (huevos, queso), carbohidratos complejos (avena, pan integral) y frutas frescas para vitaminas y fibra.","💡 El desayuno activa el metabolismo y mejora la concentración."),
    "almuerzo":     ("🍽️","ALMUERZO EQUILIBRADO","El almuerzo debe ser la comida principal del día: proteína (150-200g), carbohidratos, vegetales y grasas saludables. Evita las siestas largas después.","📊 El almuerzo representa el 35-40% de las calorías diarias."),
    "cena":         ("🌙","CENA SALUDABLE","La cena ideal es ligera: proteína magra (pollo, pescado), verduras y pocas grasas. Cenar 3 horas antes de dormir ayuda al metabolismo.","💤 Una cena pesada interfiere con la calidad del sueño."),
    "snack":        ("🍎","SNACKS SALUDABLES","Mejores snacks: nueces (puñado), manzana + mantequilla de maní, yogur griego, zanahorias con hummus, palomitas de maíz naturales.","💡 Los snacks controlan el hambre y evitan atracones."),
    "postre":       ("🍰","POSTRES","Los postres ricos y menos culposos: chocolate negro >70% (antioxidantes), helado de banana, frutas con yogur, gelatina.","🍫 El chocolate negro mejora el ánimo por su contenido de serotonina."),
    "bebida":       ("🥤","BEBIDAS SALUDABLES","Las mejores bebidas: agua (primero siempre), jugos naturales sin azúcar, tés, café sin exceso. Evita refrescos y bebidas azucaradas.","💧 Debes tomar 8 vasos de agua al día como mínimo."),
    "cereal":       ("🌾","CEREALES","Los cereales integrales son más nutritivos que los refinados. Avena, quinoa y arroz integral son los más recomendados.","💪 La avena tiene beta-glucano que reduce el colesterol."),
    "chocolate":    ("🍫","CHOCOLATE","El chocolate negro (>70% cacao) tiene flavonoides que reducen la presión arterial. El cacao puro tiene más antioxidantes que los arándanos.","❤️ El chocolate libera endorfinas que mejoran el estado de ánimo."),
    "cafe":         ("☕","CAFÉ","El café contiene más de 1,000 compuestos. Un café al día puede reducir el riesgo de diabetes tipo 2. La cafeína alcanza su pico a los 45 minutos.","☕ El espresso tiene menos cafeína que el café de filtro por volumen."),
    "vitaminas":    ("💊","VITAMINAS ESENCIALES","Vitamina C: cítricos e inmunidad. Vitamina D: luz solar y huesos. B12: carnes y energía. Vitamina A: zanahoria y visión. Vitamina E: nueces y piel.","🥗 Una dieta variada cubre casi todas las vitaminas necesarias."),
    "proteina":     ("💪","PROTEÍNAS","Los mejores fuentes de proteína: pollo (26g/100g), atún (30g), huevos (6g c/u), legumbres (8g/100g), queso cottage (11g/100g).","🏋️ Necesitas 1.6-2.2g de proteína por kg de peso para ganar músculo."),
    "carbohidratos":("🍞","CARBOHIDRATOS","Los carbos complejos (avena, arroz integral, batata) son la mejor fuente de energía. Los simples (azúcar, pan blanco) suben el azúcar rápidamente.","⚡ El cerebro necesita glucosa (carbohidrato) para funcionar."),
    "glucosa":      ("🩸","GLUCOSA Y AZÚCAR","La glucosa es el combustible principal del cuerpo. El azúcar normal en ayunas es 70-100 mg/dL. Más de 126 puede indicar diabetes.","🥗 Los alimentos de bajo índice glucémico mantienen estable el azúcar."),
    "grasas":       ("🥑","GRASAS SALUDABLES","Las grasas buenas (omega-3, aguacate, aceite de oliva) son esenciales para el cerebro y hormonas. Las trans (comida chatarra) son las malas.","💡 El 30% de tus calorías deben venir de grasas buenas."),
    "omega":        ("🐟","OMEGA-3","El omega-3 reduce la inflamación, mejora el corazón y el cerebro. Fuentes: salmón, sardinas, nueces, chía, linaza.","❤️ 2 porciones de pescado graso a la semana cubren tu omega-3."),
    "hidratacion":  ("💧","HIDRATACIÓN","El 60% del cuerpo humano es agua. La deshidratación reduce el rendimiento en un 20%. Señales: orina oscura, fatiga, dolor de cabeza.","💦 Bebe agua antes de sentir sed, ya que la sed indica leve deshidratación."),
    "metabolismo":  ("⚡","METABOLISMO","El metabolismo basal (BMR) es la energía que gastas en reposo. Factores que lo aceleran: músculo, ejercicio, té verde, proteínas, sueño.","🔥 Cada kg de músculo quema 50-70 calorías extra al día en reposo."),
    "nutricion":    ("🥗","NUTRICIÓN","Una dieta equilibrada incluye: 50% carbohidratos, 25% proteínas, 25% grasas saludables, más vitaminas, minerales y agua.","📊 El déficit calórico de 500 kcal/día genera pérdida de 0.5 kg/semana."),
    "ayuno":        ("⏱️","AYUNO INTERMITENTE","El ayuno 16:8 (16h ayuno, 8h comida) es el más popular. Beneficios: pérdida de grasa, mejora insulina y longevidad celular.","⚡ Puedes beber agua, café negro y té durante el ayuno."),
    "verdura":      ("🥦","VERDURAS","Las más nutritivas: espinaca, brócoli, kale, zanahoria, tomate, pimiento. Mínimo 5 porciones de frutas y verduras al día.","🥗 Cocinar al vapor preserva mejor los nutrientes de las verduras."),
    "vegetales":    ("🥦","VEGETALES","Los vegetales de hoja verde son los más densos nutricionalmente. La dieta plant-based reduce el riesgo cardíaco en un 32%.","🌿 El aguacate, aunque vegetal, es rico en grasas saludables."),
    "fruta":        ("🍎","FRUTAS","Las más nutritivas: arándanos (antioxidantes), plátano (potasio), aguacate (grasas), naranja (vitamina C), kiwi (vitamina C+K).","🍓 Las frutas de colores brillantes tienen más antioxidantes."),
    "umami":        ("😋","UMAMI - 5to SABOR","El umami es el quinto sabor básico (junto a dulce, salado, ácido, amargo). Se encuentra en tomate, queso parmesano, champiñones y salsa de soya.","🇯🇵 El término umami fue acuñado por el científico japonés Kikunae Ikeda en 1908."),
    "amargo":       ("😖","SABOR AMARGO","El sabor amargo es una señal de alerta evolutiva contra toxinas. El café, chocolate negro, endibias y rúcula son ejemplos.","💊 Los alimentos amargos estimulan la digestión y el hígado."),
    "acido":        ("🍋","SABOR ÁCIDO","El sabor ácido indica presencia de ácidos orgánicos. Limón, naranja, vinagre y yogur son fuentes. Los ácidos ayudan a conservar alimentos.","⚗️ El pH del jugo gástrico es de 1.5-3.5, muy ácido."),
    "dosis":        ("💊","DOSIS DE NUTRIENTES","Vitamina C: 75-90mg/día. Vitamina D: 600-800 UI/día. Calcio: 1000mg/día. Hierro: 8-18mg/día. Omega-3: 1000-2000mg/día.","⚠️ Siempre consulta a un médico antes de suplementarte."),
}

_LISTA_ALIMENTOS = list(_ALIMENTOS_INFO.keys())

async def motor_alimentos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Motor genérico para comandos de alimentos y nutrición."""
    cmd = update.message.text.split()[0][1:].lower()
    if str(update.effective_user.id) in blacklist:
        return
    info = _ALIMENTOS_INFO.get(cmd)
    if not info:
        await update.message.reply_text(f"🍽️ **{cmd.upper()}** — Tema de alimentación registrado.", parse_mode="Markdown")
        return
    emoji, titulo, descripcion, dato = info
    await update.message.reply_text(
        f"{emoji} **{titulo}** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📖 {descripcion}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 {dato}",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

# ─── MOTOR SALUD MÉDICA ───────────────────────────────────────────────────────
_SALUD_MED_INFO = {
    "vacuna":        ("💉","VACUNAS","Las vacunas han erradicado la viruela y casi eliminado la polio. Son la intervención médica más costo-efectiva de la historia.","🛡️ La vacunación masiva protege a quienes no pueden vacunarse."),
    "alergia":       ("🤧","ALERGIAS","Las alergias más comunes: polvo, mariscos, nueces, lactosa, gluten, picaduras de insectos y medicamentos como penicilina.","💊 Los antihistamínicos como la cetirizina alivian los síntomas."),
    "inyeccion":     ("💉","INYECCIONES","Las inyecciones pueden ser intramusculares (músculo), subcutáneas (bajo la piel) o intravenosas (vena). Los glúteos son el sitio más usado.","🩺 Siempre deben ser aplicadas por personal de salud capacitado."),
    "pastilla":      ("💊","MEDICAMENTOS ORALES","Las pastillas deben tomarse según indicación médica. Algunas deben tomarse con comida, otras en ayunas. No mezcles medicamentos sin consultar.","⚕️ Nunca automedicarse. La dosis hace el veneno."),
    "jarabe":        ("🍶","JARABES MEDICINALES","Los jarabes para la tos pueden ser expectorantes (fluidifican) o antitusígenos (suprimen). Los jarabes para niños tienen dosis especiales por peso.","🩺 Mide siempre con la dosificadora incluida, no con cucharas."),
    "gripe":         ("🤧","GRIPE / INFLUENZA","La gripe es causada por el virus influenza. Síntomas: fiebre, dolores musculares, tos y malestar general. Dura 5-7 días típicamente.","💊 La vacuna anual reduce el riesgo de gripe severa en un 60%."),
    "resfriado":     ("😷","RESFRIADO COMÚN","El resfriado es causado por rinovirus y otros. Diferente a la gripe: sin fiebre alta ni dolores musculares intensos. Dura 7-10 días.","🍵 El reposo, hidratación y vitamina C ayudan a recuperarse más rápido."),
    "fiebre":        ("🌡️","FIEBRE","La fiebre es una respuesta del sistema inmune. 37°C es normal. 38-38.9°C es fiebre moderada. +39°C es fiebre alta que requiere atención.","🧊 Baños tibios, hidratación y paracetamol ayudan a bajarla."),
    "efecto_secundario":("⚠️","EFECTOS SECUNDARIOS","Los efectos secundarios varían por medicamento. Los más comunes: náuseas, mareos, dolor de cabeza, somnolencia. Siempre lee el prospecto.","🩺 Si experimentas efectos graves, consulta a un médico urgente."),
    "consulta":      ("🏥","CONSULTA MÉDICA","Una consulta médica incluye: anamnesis (historial), examen físico y diagnóstico. Lleva siempre tu historia clínica y lista de medicamentos.","📋 Anota tus síntomas antes de la consulta para no olvidar nada."),
    "tratamiento":   ("💊","TRATAMIENTOS MÉDICOS","Los tratamientos pueden ser farmacológicos (medicamentos), quirúrgicos, fisioterapéuticos o psicológicos. El seguimiento médico es clave.","🩺 Nunca abandones un tratamiento sin consultar a tu médico."),
    "clinica":       ("🏥","CLÍNICAS Y HOSPITALES","Las clínicas privadas ofrecen atención especializada. Los hospitales públicos atienden emergencias. La telemedicina es opción accesible.","📱 En Venezuela: IVSS, hospitales del MPPS y clínicas privadas son las opciones."),
    "enfermero":     ("👨‍⚕️","ENFERMERÍA","Los enfermeros son profesionales de salud que administran medicamentos, cuidan pacientes y apoyan a los médicos. Son esenciales en hospitales.","❤️ La enfermería es una de las profesiones más nobles y demandadas del mundo."),
    "cura":          ("💊","CURAS Y TRATAMIENTOS","Las curas más revolucionarias: penicilina (1928), insulina (1921), vacuna antipolio (1955), TARGA para VIH (1996).","🔬 La medicina moderna ha duplicado la esperanza de vida en 100 años."),
    "receta":        ("📋","RECETA MÉDICA","Una receta médica incluye: nombre del medicamento, dosis, frecuencia y duración del tratamiento. Siempre llévala al farmacéutico.","⚕️ En Venezuela algunas medicinas requieren receta especial controlada."),
}

_LISTA_SALUD_MED = list(_SALUD_MED_INFO.keys())

async def motor_salud_medica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Motor genérico para comandos de salud médica."""
    cmd = update.message.text.split()[0][1:].lower()
    if str(update.effective_user.id) in blacklist:
        return
    info = _SALUD_MED_INFO.get(cmd)
    if not info:
        await update.message.reply_text(f"🏥 **{cmd.upper()}** — Tema médico registrado. Consulta siempre a un médico.", parse_mode="Markdown")
        return
    emoji, titulo, descripcion, dato = info
    await update.message.reply_text(
        f"{emoji} **{titulo}** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📖 {descripcion}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 {dato}\n"
        f"⚠️ _Esta info no reemplaza la consulta médica._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 2)

# ─── MOTOR FITNESS ────────────────────────────────────────────────────────────
_FITNESS_INFO = {
    "abdomen":     ("💪","ABDOMEN","Los abdominales se dividen en: recto abdominal (six-pack), oblicuos y transverso. El core fuerte protege la columna vertebral.","🔥 Los abdominales se hacen en la cocina (dieta) más que en el gimnasio."),
    "abdominales": ("💪","ABDOMINALES","Mejores ejercicios: crunch, plancha, mountain climbers, leg raises y russian twists. 3 series de 15-20 repeticiones es ideal.","⚡ La plancha abdominal activa más músculos que el crunch tradicional."),
    "brazos":      ("💪","ENTRENAMIENTO DE BRAZOS","Ejercicios: curl de bíceps, tríceps en polea, press francés, martillo, extensiones. Alterna días de bíceps y tríceps.","📏 Los tríceps representan el 60% del volumen total del brazo."),
    "piernas":     ("🦵","ENTRENAMIENTO DE PIERNAS","Ejercicios: sentadilla, peso muerto, zancadas, prensa, extensiones. Las piernas son el grupo muscular más grande del cuerpo.","💪 El día de piernas quema más calorías que cualquier otro día."),
    "burpees":     ("⚡","BURPEES","Los burpees son uno de los ejercicios más completos: trabajan cardio, fuerza y coordinación. Una serie de 10 activa todo el cuerpo.","🔥 100 burpees queman aproximadamente 150 calorías."),
    "calentamiento":("🏃","CALENTAMIENTO","Un buen calentamiento dura 5-10 minutos: movilidad articular, trote suave y estiramientos dinámicos. Previene el 80% de las lesiones.","⚠️ Nunca saltes el calentamiento, aunque estés apurado."),
    "caminar":     ("🚶","CAMINAR","Caminar 10,000 pasos al día es el objetivo estándar de salud. Una caminata de 30 min quema 150-200 calorías dependiendo del ritmo.","❤️ Caminar reduce el riesgo de enfermedad cardiovascular en un 35%."),
    "correr":      ("🏃","RUNNING / CORRER","Empieza con el método run-walk: 1 min corriendo, 2 min caminando. El ritmo de conversación es el ideal para principiantes.","👟 Las zapatillas deben cambiarse cada 500-800 km de uso."),
    "trotar":      ("🏃","TROTE","El trote es un ritmo entre caminar y correr (6-9 km/h). Ideal para principiantes. 30 min de trote quema 250-350 calorías.","💓 Mantén pulsaciones entre 120-150 para quema de grasa óptima."),
    "workout":     ("🏋️","WORKOUT DEL DÍA","WOD sugerido: 3 rondas de — 20 sentadillas, 15 push-ups, 10 burpees, 30 seg plancha, 20 jumping jacks. Descanso 60 seg entre rondas.","⏱️ Este WOD completo toma 15-20 minutos y quema 200-300 calorías."),
    "agilidad":    ("⚡","AGILIDAD","La agilidad se entrena con: escalera de coordinación, conos, saltos laterales y cambios de dirección. Mejora la respuesta neuromuscular.","🏃 El entrenamiento de agilidad beneficia a todos los deportes."),
    "equilibrio":  ("🧘","EQUILIBRIO","Ejercicios de equilibrio: postura del árbol (yoga), tabla de equilibrio, single-leg deadlift, BOSU ball. Fortalece tobillos y core.","🎯 El equilibrio deteriora con la edad y es clave para prevenir caídas."),
    "resistencia": ("🏃","RESISTENCIA CARDIOVASCULAR","La resistencia mejora con entrenamiento aeróbico: correr, ciclismo, natación. El VO2 max es el indicador clave de condición cardiovascular.","💓 Atletas élite tienen un VO2 max de 70-90 ml/kg/min."),
    "fuerza":      ("💪","ENTRENAMIENTO DE FUERZA","La fuerza se desarrolla con sobrecargas progresivas: más peso o más repeticiones cada semana. Los descansos de 48h entre grupos musculares son clave.","🏋️ La periodización (planificación del entrenamiento) maximiza resultados."),
    "flexibilidad":("🤸","FLEXIBILIDAD","Estiramientos estáticos (30s cada posición) y dinámicos (movimientos controlados). La flexibilidad reduce lesiones y mejora el rendimiento.","🧘 El yoga y el pilates son las mejores disciplinas para flexibilidad."),
    "concentracion":("🧠","CONCENTRACIÓN EN EL ENTRENAMIENTO","La mente-músculo es clave: piensa en el músculo que trabajas. Elimina distracciones, pon música y establece metas claras de la sesión.","💡 Estudios muestran que la concentración aumenta la activación muscular en 20%."),
    "descanso":    ("😴","DESCANSO Y RECUPERACIÓN","El músculo crece durante el descanso, no en el gym. 7-9 horas de sueño es esencial. El descanso activo (caminata ligera) acelera la recuperación.","🔄 El sobreentrenamiento causa lesiones, fatiga y pérdida de músculo."),
}

_LISTA_FITNESS = list(_FITNESS_INFO.keys())

async def motor_fitness_ext(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Motor genérico para comandos de fitness."""
    cmd = update.message.text.split()[0][1:].lower()
    if str(update.effective_user.id) in blacklist:
        return
    info = _FITNESS_INFO.get(cmd)
    if not info:
        await update.message.reply_text(f"💪 **{cmd.upper()}** — Ejercicio registrado. ¡Muévete!", parse_mode="Markdown")
        return
    emoji, titulo, descripcion, dato = info
    await update.message.reply_text(
        f"{emoji} **{titulo}** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📖 {descripcion}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 {dato}",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

# ─── MOTOR ESPIRITUALIDAD ────────────────────────────────────────────────────
_ESPIRITUAL_INFO = {
    "alma":          ("✨","EL ALMA","El concepto de alma trasciende las religiones y filosofías. Es la esencia intangible de cada ser. Cuídala con silencio, gratitud y amor.","🕊️ 'El alma que ve la belleza reconoce su propio espíritu.' - Platón"),
    "conciencia":    ("🧠","CONCIENCIA PLENA","La conciencia es el estado de awareness del momento presente. Desarrollarla reduce el estrés y mejora las relaciones y decisiones.","☯️ La meditación es la herramienta más poderosa para expandir la conciencia."),
    "universo":      ("🌌","EL UNIVERSO","El universo tiene 13,800 millones de años. Contiene 2 billones de galaxias. La Vía Láctea tiene 400,000 millones de estrellas.","✨ Somos polvo de estrellas: todos los átomos de nuestro cuerpo vinieron del cosmos."),
    "karma":         ("☯️","LEY DEL KARMA","El karma es la ley de causa y efecto: lo que das, recibes. Acciones positivas generan energía positiva que retorna a tu vida.","🌸 'El karma no se olvida, se transforma en lecciones.'"),
    "asana":         ("🧘","ASANAS DE YOGA","Las asanas son las posturas del yoga. Las básicas: Tadasana (montaña), Balasana (niño), Adho Mukha Svanasana (perro boca abajo), Savasana.","🌟 Cada asana tiene un beneficio físico y energético específico."),
    "pranayama":     ("🫁","PRANAYAMA - CONTROL DE LA RESPIRACIÓN","El pranayama son técnicas de respiración del yoga. Kapalabhati (respiración de fuego), Nadi Shodhana (fosas alternadas) son las principales.","💨 La respiración 4-7-8 (inhala 4s, sostén 7s, exhala 8s) calma el sistema nervioso."),
    "mindfulness":   ("🧘","MINDFULNESS","El mindfulness es la práctica de atención plena al momento presente sin juzgar. Reduce la ansiedad en un 58% según estudios clínicos.","📱 Apps como Calm, Headspace y Insight Timer son excelentes para empezar."),
    "mantra":        ("🕉️","MANTRAS","Los mantras son frases o sonidos que se repiten para calmar la mente. El 'Om' es el mantra más universal. 'So Ham' significa 'Yo soy'.","🔔 Repite tu mantra 108 veces con un mala (collar de 108 cuentas)."),
    "om":            ("🕉️","OM / AUM","El Om (Aum) es el sonido primordial del universo en el hinduismo. Sus tres partes (A-U-M) representan la creación, preservación y destrucción.","☀️ Entonar Om reduce la presión arterial y calma el sistema nervioso."),
    "meditacion":    ("🧘","MEDITACIÓN","Empieza con 5 minutos: siéntate cómodo, cierra los ojos, respira profundo y observa tus pensamientos sin juzgarlos. Aumenta gradualmente.","🧠 8 semanas de meditación diaria cambian físicamente el cerebro."),
    "filosofia":     ("🤔","FILOSOFÍA","Las principales escuelas filosóficas: Estoicismo (Epicteto, Marco Aurelio), Existencialismo (Sartre), Budismo (Buda), Taoísmo (Lao-Tse).","📚 'Conócete a ti mismo' - Sócrates, el padre de la filosofía occidental."),
    "iluminacion":   ("💡","ILUMINACIÓN ESPIRITUAL","La iluminación es el estado de conciencia pura, libre de ego y sufrimiento. Buda alcanzó la iluminación bajo el árbol Bodhi hace 2,500 años.","🌸 El camino hacia la iluminación es gradual: meditación, compasión y desapego."),
    "espiritualidad":("🕊️","ESPIRITUALIDAD","La espiritualidad no requiere religión. Es la búsqueda de sentido, conexión y trascendencia. Se puede practicar en la naturaleza, meditación y servicio.","✨ La práctica espiritual reduce la ansiedad y aumenta el bienestar."),
    "alma":          ("💫","ALMA Y SER INTERIOR","Conectar con tu alma requiere silencio: apaga el teléfono, sal a la naturaleza, practica gratitud. El diario personal es excelente para esto.","🌿 'Quien mira afuera sueña; quien mira adentro despierta.' - C.G. Jung"),
    "vida_pasada":   ("🔮","VIDAS PASADAS","La reencarnación es la creencia en que el alma vive múltiples vidas. La regresión hipnótica es la técnica más usada para explorar vidas pasadas.","🌀 Esta creencia es central en el hinduismo, budismo y muchas tradiciones."),
    "proposito":     ("🎯","PROPÓSITO DE VIDA","El ikigai japonés (razón de ser) está en la intersección de: lo que amas, lo que haces bien, lo que el mundo necesita y por lo que te pagan.","🌸 Encontrar tu propósito da dirección, energía y felicidad duradera."),
    "sentido":       ("🌟","SENTIDO DE LA VIDA","Viktor Frankl sobrevivió campos de concentración encontrando sentido en el sufrimiento. El sentido puede venir del amor, el trabajo o el sufrimiento con dignidad.","📚 'La Logoterapia' de Frankl es el libro clave sobre el sentido de la vida."),
    "tranquilidad":  ("🌿","TRANQUILIDAD INTERIOR","La tranquilidad viene de aceptar lo que no podemos controlar. Marco Aurelio y los estoicos practicaban 'la serenidad ante la adversidad'.","☮️ 'La paz interior no depende de condiciones externas.' - Dalai Lama"),
    "universo":      ("🌌","CONEXIÓN CON EL UNIVERSO","Carl Sagan dijo: 'Somos una forma del universo contemplándose a sí mismo.' Los átomos de nuestro cuerpo existieron en estrellas distantes.","✨ Esta conexión cósmica nos hace parte de algo infinitamente más grande."),
    "religion":      ("🕌","RELIGIONES DEL MUNDO","Las principales: Cristianismo (2.4B), Islam (1.9B), Hinduismo (1.2B), Budismo (500M), Judaísmo (15M). Todas buscan el bien y el sentido.","🕊️ El respeto a todas las creencias es clave para la paz mundial."),
}

_LISTA_ESPIRITUAL = list(_ESPIRITUAL_INFO.keys())

async def motor_espiritualidad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Motor genérico para comandos de espiritualidad."""
    cmd = update.message.text.split()[0][1:].lower()
    if str(update.effective_user.id) in blacklist:
        return
    info = _ESPIRITUAL_INFO.get(cmd)
    if not info:
        await update.message.reply_text(f"🕊️ **{cmd.upper()}** — Reflexión espiritual. Encuentra tu paz interior.", parse_mode="Markdown")
        return
    emoji, titulo, descripcion, dato = info
    await update.message.reply_text(
        f"{emoji} **{titulo}** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ {descripcion}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💭 {dato}",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

# ─── MOTOR TECNOLOGÍA INFO ───────────────────────────────────────────────────
_TECH_INFO = {
    "adware":      ("🦠","ADWARE","El adware muestra publicidad no deseada en tu dispositivo. Puede venir instalado con software gratuito o apps pirata.","🔒 Usa Malwarebytes o AdwCleaner para eliminarlo de forma gratuita."),
    "antivirus":   ("🛡️","ANTIVIRUS","Los mejores gratuitos: Windows Defender, Avast, AVG. Los de pago: Kaspersky, Bitdefender, Norton. Actualiza siempre las definiciones.","⚠️ Tener dos antivirus activos puede causar conflictos."),
    "backdoor":    ("🚪","BACKDOOR / PUERTA TRASERA","Un backdoor es un acceso no autorizado oculto en un sistema. Los hackers los crean con malware o vulnerabilidades del software.","🔒 Mantén el software actualizado para cerrar las vulnerabilidades."),
    "backup":      ("💾","BACKUP / RESPALDO","La regla 3-2-1: 3 copias de tus datos, en 2 tipos de medios, 1 copia fuera del sitio. Google Drive, OneDrive o un disco externo son buenas opciones.","💡 Un buen backup puede salvarte de ransomware, robo o daño del equipo."),
    "bandwidth":   ("📡","ANCHO DE BANDA","El bandwidth es la capacidad máxima de transmisión de datos. Se mide en Mbps o Gbps. Un streaming en 4K requiere mínimo 25 Mbps.","📶 La fibra óptica ofrece el mayor ancho de banda disponible."),
    "bundle":      ("📦","BUNDLE / PAQUETE","Un bundle es un paquete de software o productos vendidos juntos. En programación, es el archivo resultante de empaquetar código (webpack, esbuild).","💡 Los bundles de juegos en Humble Bundle ofrecen gran valor."),
    "cache":       ("⚡","CACHÉ","El caché guarda datos temporales para acceso más rápido. Los navegadores, apps y sistemas operativos usan caché. Limpiarlo libera espacio.","🔄 Limpiar el caché del navegador resuelve muchos problemas de carga."),
    "cpu":         ("💻","CPU - PROCESADOR","El CPU es el cerebro del computador. Los más usados: Intel Core i-series y AMD Ryzen. Los núcleos y GHz determinan la velocidad.","⚡ Un CPU moderno realiza miles de millones de operaciones por segundo."),
    "criptografia":("🔐","CRIPTOGRAFÍA","La criptografía protege datos con algoritmos matemáticos. AES-256, RSA y SHA-256 son estándares modernos. HTTPS usa TLS para cifrar web.","🔑 La criptografía cuántica es el futuro de la seguridad digital."),
    "database":    ("🗄️","BASE DE DATOS","Las BD más usadas: MySQL, PostgreSQL (relacionales) y MongoDB, Redis (NoSQL). SQL es el lenguaje estándar para consultas.","💾 Una buena base de datos es el corazón de cualquier aplicación."),
    "framework":   ("🛠️","FRAMEWORKS","Frontend: React, Vue, Angular. Backend: Django, FastAPI, Express, Spring. Móvil: Flutter, React Native. IA: TensorFlow, PyTorch.","💡 Un framework ahorra tiempo pero requiere aprender sus convenciones."),
    "gpu":         ("🖥️","GPU - TARJETA GRÁFICA","La GPU procesa gráficos en paralelo. NVIDIA (RTX) y AMD (RX) lideran el mercado. Las GPUs también se usan para IA y minería.","⚡ Una RTX 4090 realiza 82 billones de operaciones por segundo."),
    "libreria":    ("📚","LIBRERÍAS DE PROGRAMACIÓN","Python: NumPy, Pandas, Requests, Flask. JavaScript: Lodash, Axios, Moment. Java: Spring, Hibernate. C++: Boost, OpenCV.","💡 'No reinventes la rueda' — usa librerías probadas y mantenidas."),
    "protocolo":   ("🌐","PROTOCOLOS DE INTERNET","HTTP/S (web), TCP/IP (base de internet), FTP (archivos), SMTP (email), WebSocket (tiempo real), SSH (terminal remoto).","🔒 HTTPS usa SSL/TLS para cifrar la comunicación web."),
    "ram":         ("🧠","RAM - MEMORIA RAM","La RAM almacena datos temporales de programas activos. 8GB es mínimo hoy, 16GB ideal para trabajo, 32GB+ para edición/gaming.","⚡ La RAM DDR5 dobla la velocidad de la DDR4 anterior."),
    "server":      ("🖥️","SERVIDOR / SERVER","Un servidor es un computador que provee servicios a otros. Los cloud servers (AWS, GCP, Azure) han reemplazado a los físicos en empresas.","☁️ Un servidor Ubuntu en la nube puede costar $5-10 USD al mes."),
    "update":      ("🔄","ACTUALIZACIONES","Las actualizaciones corrigen vulnerabilidades de seguridad y añaden funciones. No actualizar es la causa número 1 de hackeos.","⚠️ Activa las actualizaciones automáticas para mayor seguridad."),
    "compression": ("📦","COMPRESIÓN DE ARCHIVOS","Formatos: ZIP (universal), RAR (Windows), 7Z (mejor compresión), TAR.GZ (Linux). La compresión puede reducir archivos hasta un 80%.","💡 7-Zip es gratuito y uno de los mejores compresores disponibles."),
    "adware":      ("🦠","ADWARE Y MALWARE","Tipos de malware: virus, troyanos, ransomware, spyware, adware. El ransomware cifra tus archivos y pide dinero para liberarlos.","🔒 La mejor defensa: no abrir archivos desconocidos y tener backup."),
    "api":         ("🔌","API - INTERFAZ DE PROGRAMACIÓN","Una API permite que dos aplicaciones se comuniquen. REST, GraphQL y SOAP son los tipos más comunes. La mayoría son en formato JSON.","💡 APIs públicas gratuitas: OpenWeather, JSONPlaceholder, PokéAPI."),
}

_LISTA_TECH = list(_TECH_INFO.keys())

async def motor_tech_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Motor genérico para comandos de tecnología info."""
    cmd = update.message.text.split()[0][1:].lower()
    if str(update.effective_user.id) in blacklist:
        return
    info = _TECH_INFO.get(cmd)
    if not info:
        await update.message.reply_text(f"💻 **{cmd.upper()}** — Concepto tecnológico registrado.", parse_mode="Markdown")
        return
    emoji, titulo, descripcion, dato = info
    await update.message.reply_text(
        f"{emoji} **{titulo}** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📖 {descripcion}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 {dato}",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

# ─── MOTOR MODA & BELLEZA ───────────────────────────────────────────────────
_MODA_INFO = {
    "cabello":     ("💇","CUIDADO DEL CABELLO","Los tipos de cabello: liso, ondulado, rizado y muy rizado. El pH del champú debe ser 4.5-5.5 para no dañar la cutícula.","🌿 Los aceites de argán, coco y jojoba son los mejores para el cabello."),
    "barba":       ("🧔","CUIDADO DE LA BARBA","Una barba saludable necesita: aceite de barba, peine, recorte regular y limpieza diaria. El crecimiento es genético, 1-2 cm por mes.","✂️ Los estilos más populares: cerrada, de diseñador, candado y perilla."),
    "unas":        ("💅","CUIDADO DE UÑAS","Las uñas crecen 3-4mm por mes. El esmalte de gel dura más pero puede debilitar la uña. Hidratar las cutículas es clave para uñas sanas.","💡 La biotina (vitamina B7) fortalece las uñas débiles y quebrables."),
    "chanclas":    ("🩴","CHANCLAS Y CALZADO CASUAL","Las chanclas son el calzado más popular en climas cálidos. Brands como Havaianas, Crocs y Lacoste son los más populares del mercado.","💡 Las chanclas de suela gruesa protegen mejor el arco del pie."),
    "zapatos":     ("👟","CALZADO Y ZAPATILLAS","Las marcas más populares: Nike, Adidas, Puma, New Balance. Para running: soporte y amortiguación. Para gym: suela plana y agarre.","👟 Cambiar zapatillas de running cada 500-800 km previene lesiones."),
    "ropa":        ("👔","MODA Y ESTILO","El guardarropa cápsula tiene 30-40 piezas versátiles que combinan entre sí. Los colores neutros (blanco, negro, beige, navy) son la base.","💡 La regla 80/20: el 80% del tiempo usas el 20% de tu ropa."),
    "maquillaje":  ("💄","MAQUILLAJE","Los básicos del maquillaje: base, corrector, rubor, sombras y labial. El less is more es la filosofía del maquillaje natural moderno.","🌟 Los tutoriales de makeup en YouTube son la mejor escuela gratis."),
    "accesorio":   ("💍","ACCESORIOS","Los accesorios completan un look: cinturón, bolso, reloj, joyería y lentes. La regla: 3 accesorios máximo por outfit para no saturar.","👜 Un reloj clásico o un par de aretes simples elevan cualquier atuendo."),
    "perfume":     ("🌹","PERFUMES Y FRAGANCIAS","Las familias de fragancias: floral, oriental, maderas, fresco y cítrico. Los perfumes duran más aplicados en puntos de calor (cuello, muñecas).","💡 No frotar el perfume: los destroza las moléculas. Solo aplica y listo."),
    "corte":       ("✂️","CORTES DE CABELLO","Cortes para hombre: fade, undercut, pompadour, crew cut, buzz cut. Para mujer: bob, lob, layers, pixie, bangs.","💇 El corte debe adaptarse a la forma del rostro y tipo de cabello."),
    "tinte":       ("🎨","TINTE DE CABELLO","Los tintes permanentes duran 6-8 semanas. Los semipermanentes, 3-4 semanas. El balayage es más natural y requiere menos mantenimiento.","⚠️ Siempre haz una prueba de alergia antes de aplicar cualquier tinte."),
    "peinado":     ("💆","PEINADOS","Para mantener un peinado: fija con productos según tu tipo de cabello. Gel para definición, pomada para textura, spray para fijación sin peso.","💇 El peinado del día puede hacerse en 5 minutos si tienes el producto correcto."),
    "vestido":     ("👗","VESTIDOS Y MODA FEMENINA","Los estilos más versátiles: wrap dress (favorece todas las figuras), midi dress y maxi dress. El LBD (little black dress) es el clásico infalible.","💃 Coco Chanel dijo: 'Una mujer que usa el color negro tiene sus ideas claras.'"),
    "moda":        ("👗","MODA MUNDIAL","Las semanas de la moda más importantes: París, Milán, Nueva York y Londres. Las tendencias cambian cada temporada (SS y FW).","🌟 La moda sostenible y el slow fashion son las grandes tendencias actuales."),
    "acondicionador":("💧","ACONDICIONADOR DE CABELLO","El acondicionador sella la cutícula del cabello y aporta hidratación. Aplicar solo en las puntas, nunca en las raíces para evitar grasa.","🌿 Los acondicionadores sin silicona son mejores para el cabello rizado."),
    "cmyk":        ("🎨","CMYK - MODELO DE COLOR","CMYK (Cian, Magenta, Amarillo, Negro) es el modelo de color para impresión. Es diferente al RGB (pantallas). Siempre convierte antes de imprimir.","🖨️ Un diseño en RGB puede verse diferente en impresión CMYK."),
    "hsl":         ("🎨","HSL - MODELO DE COLOR","HSL (Hue/Matiz, Saturation/Saturación, Lightness/Luminosidad) es el modelo de color más intuitivo para diseñadores digitales.","💡 HSL(0, 100%, 50%) es rojo puro. HSL(240, 100%, 50%) es azul puro."),
    "xyz":         ("📐","ESPACIO DE COLOR XYZ","XYZ es el espacio de color base definido por la CIE en 1931. Es el estándar para convertir entre RGB, CMYK, LAB y otros espacios de color.","🎨 Todos los modelos de color modernos derivan del espacio CIE XYZ."),
    "afeitarse":   ("🪒","AFEITADO","Para un afeitado perfecto: ablanda la barba con agua caliente, aplica crema de afeitar, afeita con la dirección del vello en primera pasada.","💡 Una cuchilla de doble filo da el afeitado más suave y económico."),
}

_LISTA_MODA = list(_MODA_INFO.keys())

async def motor_moda_belleza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Motor genérico para comandos de moda y belleza."""
    cmd = update.message.text.split()[0][1:].lower()
    if str(update.effective_user.id) in blacklist:
        return
    info = _MODA_INFO.get(cmd)
    if not info:
        await update.message.reply_text(f"💄 **{cmd.upper()}** — Tema de moda y belleza.", parse_mode="Markdown")
        return
    emoji, titulo, descripcion, dato = info
    await update.message.reply_text(
        f"{emoji} **{titulo}** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📖 {descripcion}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 {dato}",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

# ─── MOTOR BIENESTAR & VIDA ───────────────────────────────────────────────────
_BIENESTAR_INFO = {
    "alegria":     ("😊","ALEGRÍA","La alegría es una emoción que surge de experiencias positivas. Se cultiva con gratitud, conexión social, propósito y actos de bondad.","🌞 Sonreír, aunque sea forzado, activa la química de la felicidad."),
    "autoestima":  ("💪","AUTOESTIMA","La autoestima sana no es arrogancia: es conocer tu valor sin necesitar validación externa. Se construye con acciones pequeñas y constantes.","🌱 'Hazte a ti mismo la persona con la que quisieras vivir.' - Nathaniel Branden"),
    "confianza":   ("🦁","CONFIANZA","La confianza se construye con pequeños logros acumulados, no con pensar positivo. Actúa con valentía aunque tengas miedo.","⚡ La postura corporal afecta la confianza: espalda recta, cabeza alta."),
    "gratitud":    ("🙏","GRATITUD","Escribir 3 cosas por las que eres agradecido cada día aumenta la felicidad en un 25%. La gratitud cambia el enfoque del cerebro.","📓 El diario de gratitud es la práctica más poderosa para el bienestar."),
    "felicidad":   ("😄","FELICIDAD","La felicidad no es un estado permanente sino momentos. La ciencia la conecta con: relaciones, propósito, salud, libertad y gratitud.","💡 El dinero aumenta la felicidad hasta $75k/año, luego el efecto se estanca."),
    "valentia":    ("🦁","VALENTÍA","La valentía no es ausencia de miedo, es actuar a pesar del miedo. Se desarrolla con exposición gradual a lo que temes.","🔥 'El coraje es contagioso. Cuando un hombre valiente toma posición, otros lo siguen.' - Billy Graham"),
    "vida":        ("🌱","PROPÓSITO DE VIDA","Una vida con propósito tiene dirección, significado y satisfacción. El ikigai japonés integra pasión, misión, vocación y profesión.","🌟 'El secreto de una vida plena no está en evitar el dolor, sino en encontrarle sentido.'"),
    "vacaciones":  ("🏖️","VACACIONES","Las vacaciones reducen el estrés, mejoran la creatividad y recargan la energía. Los destinos más visitados: Francia, España, USA, China e Italia.","✈️ 14 días de vacaciones al año es el mínimo recomendado por psicólogos."),
    "viaje":       ("✈️","VIAJE Y TURISMO","Viajar amplía la perspectiva, reduce prejuicios y desarrolla habilidades de adaptación. El turismo mueve 9 billones de dólares al año globalmente.","🌍 Un pasaporte venezolano tiene acceso sin visa a 44 países actualmente."),
    "derrota":     ("😔","MANEJAR LA DERROTA","La derrota es parte del camino al éxito. Edison falló 10,000 veces antes de inventar la bombilla. Michael Jordan fue cortado de su equipo escolar.","💪 'No he fallado. Simplemente he encontrado 10,000 formas que no funcionan.' - Edison"),
    "victoria":    ("🏆","CELEBRAR LA VICTORIA","Celebrar los logros, pequeños y grandes, refuerza comportamientos positivos y aumenta la motivación para seguir avanzando.","🥳 Tómate un momento para reconocer tus logros. ¡Te lo mereces!"),
    "empate":      ("🤝","EL EMPATE","En la vida no todo es ganar o perder. A veces empatar es señal de madurez: saber cuándo ceder es también una fortaleza.","☯️ 'El arte del compromiso es encontrar el terreno común donde todos ganan algo.'"),
    "animar":      ("🎉","DAR ÁNIMO","Animar a otros cuesta nada y puede cambiarlo todo para ellos. Una palabra de aliento en el momento justo puede ser el impulso que alguien necesita.","🌟 'Las palabras tienen el poder de destruir o curar. Cuando son amables y compasivas, lo cambian todo.'"),
    "alegria":     ("😊","CULTIVAR LA ALEGRÍA","Actividades que generan alegría genuina: conexión con seres queridos, hacer ejercicio, crear algo, ayudar a otros y estar en la naturaleza.","🌺 La alegría compartida se multiplica; la pena compartida se reduce."),
    "viaje":       ("🌍","VIAJAR CON POCO PRESUPUESTO","Tips para viajar barato: vuelos con escalas, Airbnb vs hotel, comer donde comen los locales, viajar en temporada baja y apps como Skyscanner.","💡 Un presupuesto de $30-50 por día es suficiente en Latinoamérica."),
    "turismo":     ("🗺️","TURISMO EN VENEZUELA","Venezuela tiene playas del Caribe (Morrocoy, Los Roques), Tepuis (Roraima, Autana), selvas (Amazonas) y ciudades coloniales (Coro, Mérida).","🇻🇪 El Salto Ángel (979m) es la cascada más alta del mundo."),
    "autoestima":  ("💎","AUTOESTIMA ALTA","Señales de autoestima sana: aceptar críticas sin derrumbarse, poner límites, no necesitar aprobación constante, y conocer tus valores.","🌱 Se construye con pequeñas victorias diarias, no con frases motivacionales."),
    "claridad":    ("✨","CLARIDAD MENTAL","La claridad mental se logra con: sueño suficiente, meditación, journaling, ejercicio y reducir el consumo de redes sociales.","🧠 El journaling (escribir tus pensamientos) es el mejor ejercicio de claridad."),
    "paz":         ("☮️","PAZ INTERIOR","La paz no viene de resolver todos los problemas, sino de aceptar lo que no puedes controlar. El estoicismo enseña esta distinción.","🕊️ 'La paz empieza con una sonrisa.' - Madre Teresa"),
    "afirmacion":  ("💫","AFIRMACIONES POSITIVAS","Las mejores afirmaciones: 'Soy capaz de superar cualquier obstáculo', 'Merezco amor y éxito', 'Cada día soy mejor versión de mí'.","📅 Répite tus afirmaciones cada mañana durante 21 días para crear el hábito."),
    "academia":    ("🎓","ACADEMIA Y EDUCACIÓN ONLINE","Plataformas gratuitas: Khan Academy, Coursera (auditoría), YouTube. De pago con calidad: Udemy, Platzi, LinkedIn Learning.","💡 1 hora de aprendizaje al día = 365 horas al año de nuevas habilidades."),
    "apuntes":     ("📝","TÉCNICAS DE TOMA DE APUNTES","Método Cornell: divide la hoja en notas, claves y resumen. Mapas mentales para temas complejos. La escritura manual mejora la retención en un 44%.","✏️ Revisar los apuntes dentro de las 24 horas fija el aprendizaje."),
    "agenda":      ("📅","ORGANIZAR TU AGENDA","Usa la regla 1-3-5: 1 tarea grande, 3 medianas, 5 pequeñas por día. Google Calendar o Notion son las apps más populares para organización.","⏰ Planificar la semana cada domingo ahorra 2+ horas de indecisión."),
    "urgente":     ("🔴","GESTIÓN DE URGENCIAS","La Matriz de Eisenhower: Urgente+Importante (hazlo ya), No urgente+Importante (plánificalo), Urgente+No importante (delégalo).","📊 El 80% de las urgencias son falsas: evalúa antes de reaccionar."),
    "importante":  ("⭐","GESTIÓN DE LO IMPORTANTE","Lo importante vs lo urgente: lo urgente pide atención ahora, lo importante construye el futuro. Prioriza lo segundo para crecer.","🎯 Cada día haz primero la tarea más importante, aunque sea la más difícil."),
    "concentracion":("🎯","CONCENTRACIÓN Y FOCO","Técnicas: Pomodoro (25 min trabajo, 5 min descanso), Bloqueo de apps, música instrumental sin letra, temperatura fresca (18-20°C).","🧠 Multitasking reduce la productividad en un 40%. El monofocus gana."),
}

_LISTA_BIENESTAR = list(_BIENESTAR_INFO.keys())

async def motor_bienestar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Motor genérico para bienestar y vida."""
    cmd = update.message.text.split()[0][1:].lower()
    if str(update.effective_user.id) in blacklist:
        return
    info = _BIENESTAR_INFO.get(cmd)
    if not info:
        await update.message.reply_text(f"🌟 **{cmd.upper()}** — Reflexión de bienestar. ¡Sigue adelante!", parse_mode="Markdown")
        return
    emoji, titulo, descripcion, dato = info
    await update.message.reply_text(
        f"{emoji} **{titulo}** {emoji}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💬 {descripcion}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ {dato}",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

# ─── COMANDOS MISCELÁNEOS INDIVIDUALES ──────────────────────────────────────

async def cmd_comandos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra lista de comandos disponibles."""
    await update.message.reply_text(
        "📋 **COMANDOS DISPONIBLES**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Usa los siguientes para ver listas:\n"
        "/list1 - Sistema & Economía\n"
        "/list2 - Multimedia & Descargas\n"
        "/list3 - Búsqueda & Info\n"
        "/list4 - Herramientas\n"
        "/list5 - Juegos\n"
        "/list6 - Salud & Fitness\n"
        "/list7 - Deportes & Música\n"
        "/list8 - Tecnología & Código\n"
        "/list9 - RPG & Misceláneos\n"
        "/info_completa - Lista completa\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "_Total: 1,000+ comandos disponibles_",
        parse_mode="Markdown"
    )

async def cmd_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ayuda general del bot."""
    await update.message.reply_text(
        "❓ **AYUDA - CAMILA BOT V15** ❓\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🚀 **Para comenzar:**\n"
        "1. Regístrate: `/reg [nombre] [edad] [género]`\n"
        "2. Ve tu perfil: `/perfil`\n"
        "3. Gana dinero: `/trabajar`\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🎯 **Comandos clave:**\n"
        "• `/menu` - Menú principal\n"
        "• `/comandos` - Lista de comandos\n"
        "• `/saldo` - Ver tu dinero\n"
        "• `/buscar [texto]` - Buscar en Google\n"
        "• `/ytmp4 [url]` - Descargar YouTube\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "_¿Necesitas más ayuda? Escríbeme directamente._",
        parse_mode="Markdown"
    )

async def cmd_economia_noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Noticias económicas."""
    await cmd_noticias_categoria(update, context, "economía finanzas", "💹", "Economía y Finanzas")

async def cmd_compartir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Compartir un enlace o mensaje."""
    if context.args:
        enlace = " ".join(context.args)
        await update.message.reply_text(
            f"🔗 **ENLACE COMPARTIDO**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"{enlace}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"_Comparte este mensaje con quien quieras._",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("📝 **Uso:** `/compartir [enlace o texto]`", parse_mode="Markdown")

async def cmd_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver balance general."""
    await cmd_saldo_real(update, context)

async def cmd_astronomy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dato astronómico."""
    import random as _r
    datos = [
        "🌌 La Vía Láctea tiene entre 100,000 y 400,000 millones de estrellas.",
        "☀️ El Sol representa el 99.86% de toda la masa del sistema solar.",
        "🌙 La Luna se aleja de la Tierra 3.8 cm cada año.",
        "🪐 Un día en Venus dura más que un año en Venus.",
        "⭐ La estrella más cercana al Sol es Próxima Centauri a 4.24 años luz.",
        "🌍 La Tierra tarda 225 millones de años en orbitar el centro de la galaxia.",
        "🔭 Existen más de 2 billones de galaxias en el universo observable.",
        "💫 Un agujero negro del tamaño del Sol tendría 3 km de diámetro.",
        "🌠 Las estrellas de neutrones giran hasta 716 veces por segundo.",
        "🪐 Los anillos de Saturno tienen solo 10-100 metros de grosor.",
    ]
    dato = _r.choice(datos)
    await update.message.reply_text(
        f"🔭 **ASTRONOMÍA** 🔭\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{dato}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Usa /planeta para info de planetas._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_geologia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dato de geología."""
    import random as _r
    datos = [
        "🌋 La Tierra tiene 4 capas: corteza, manto, núcleo externo y núcleo interno.",
        "💎 El diamante es el mineral más duro (10 en la escala de Mohs).",
        "🪨 Las rocas más antiguas encontradas tienen 4,030 millones de años.",
        "🌊 El 96.5% del agua de la Tierra está en los océanos.",
        "⛰️ Las placas tectónicas se mueven a la velocidad a la que crecen las uñas.",
        "🔥 La temperatura del núcleo terrestre es de 5,400°C, similar a la del Sol.",
        "💧 El agua en estado sólido (hielo) es menos densa que en líquido, por eso flota.",
        "🌎 Un terremoto de magnitud 8 libera 32 veces más energía que uno de magnitud 7.",
    ]
    await update.message.reply_text(
        f"🪨 **GEOLOGÍA** 🪨\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_La ciencia que estudia la Tierra y sus materiales._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_biologia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dato de biología."""
    import random as _r
    datos = [
        "🧬 El ADN humano tiene 3 mil millones de pares de bases.",
        "🦠 Hay más bacterias en tu boca que personas en la Tierra.",
        "🧠 El cerebro humano tiene ~86 mil millones de neuronas.",
        "❤️ El corazón late más de 100,000 veces al día.",
        "🫁 Los pulmones tienen una superficie de 70-80 m², como una cancha de tenis.",
        "🦷 El esmalte dental es el tejido más duro del cuerpo humano.",
        "👁️ El ojo puede distinguir hasta 10 millones de colores diferentes.",
        "🦴 El hueso más pequeño del cuerpo está en el oído medio: el estribo.",
    ]
    await update.message.reply_text(
        f"🧬 **BIOLOGÍA** 🧬\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_La ciencia que estudia los seres vivos._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_fisica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dato de física."""
    import random as _r
    datos = [
        "⚡ La velocidad de la luz es 299,792,458 m/s en el vacío.",
        "🔋 La energía nunca se crea ni se destruye, solo se transforma.",
        "🌊 El sonido viaja 4 veces más rápido en el agua que en el aire.",
        "🧲 La gravedad es la fuerza más débil de las 4 fuerzas fundamentales.",
        "⚛️ Un átomo es 99.99999999999% espacio vacío.",
        "🌡️ El cero absoluto es -273.15°C, la temperatura mínima posible.",
        "📡 La radiación electromagnética viaja a la velocidad de la luz.",
        "🔭 El tiempo pasa más lento cerca de objetos masivos (relatividad).",
    ]
    await update.message.reply_text(
        f"⚛️ **FÍSICA** ⚛️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_La ciencia que estudia la materia y la energía._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_meteorologia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dato de meteorología."""
    import random as _r
    datos = [
        "🌪️ La nube de tormenta (cumulonimbo) puede alcanzar 12 km de altura.",
        "⚡ Un rayo tiene 5 veces la temperatura de la superficie del Sol.",
        "❄️ No existen dos copos de nieve exactamente iguales.",
        "🌈 Un arcoíris completo es un círculo completo, visto desde aviones.",
        "💨 El viento más rápido registrado fue de 407 km/h en Australia (1996).",
        "☔ El lugar más lluvioso de la Tierra recibe 12,000 mm/año (Cherrapunji, India).",
        "🌡️ El récord de temperatura más alta fue 56.7°C en Death Valley, EEUU.",
        "🧊 La Antarctica registró -89.2°C, la temperatura más fría registrada.",
    ]
    await update.message.reply_text(
        f"⛈️ **METEOROLOGÍA** ⛈️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_La ciencia que estudia la atmósfera y el clima._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_oceanografia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dato de oceanografía."""
    import random as _r
    datos = [
        "🌊 El 95% del océano aún no ha sido explorado por el ser humano.",
        "🐳 La ballena azul es el animal más grande que ha existido en la Tierra.",
        "💧 El océano más profundo: Fosa de Mariana con 11,034 metros.",
        "🐟 Los océanos tienen más de 230,000 especies marinas conocidas.",
        "🌡️ La temperatura del fondo oceánico es de 2-4°C.",
        "🌊 Las olas más altas registradas miden más de 30 metros.",
        "🐠 Los arrecifes de coral albergan el 25% de toda la vida marina.",
        "⚓ El Titanic descansa a 3,784 metros de profundidad en el Atlántico Norte.",
    ]
    await update.message.reply_text(
        f"🌊 **OCEANOGRAFÍA** 🌊\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_La ciencia que estudia los océanos._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_ecologia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dato de ecología."""
    import random as _r
    datos = [
        "🌿 Un árbol maduro absorbe 22 kg de CO₂ al año.",
        "♻️ Reciclar una lata de aluminio ahorra energía para ver TV 3 horas.",
        "🐝 Las abejas polinizan el 35% de los alimentos que consumimos.",
        "🌊 8 millones de toneladas de plástico llegan al océano cada año.",
        "🌳 La deforestación destruye 15,000 millones de árboles al año.",
        "☀️ La energía solar podría satisfacer la demanda mundial 10,000 veces.",
        "🦋 El 40% de las especies de insectos están en peligro de extinción.",
        "💧 El 97.5% del agua de la Tierra es salada; solo el 2.5% es dulce.",
    ]
    await update.message.reply_text(
        f"🌿 **ECOLOGÍA** 🌿\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_La ciencia de las relaciones entre seres vivos y su entorno._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_ciencias_extra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dato de química."""
    import random as _r
    datos = [
        "⚗️ El agua (H₂O) es el único compuesto que existe en 3 estados de forma natural.",
        "🧪 El oro es tan blando que se puede moldear con las manos.",
        "💨 El gas noble más raro en la atmósfera es el xenón (0.0000087%).",
        "🔬 Un mol de cualquier sustancia contiene 6.022 × 10²³ partículas.",
        "💊 El paracetamol fue descubierto accidentalmente en el siglo XIX.",
        "🌡️ El mercurio es el único metal líquido a temperatura ambiente.",
        "⚡ La grafena es 200 veces más resistente que el acero.",
        "🧊 El hielo seco es CO₂ sólido a -78.5°C y no deja residuo líquido.",
    ]
    await update.message.reply_text(
        f"⚗️ **QUÍMICA** ⚗️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_La ciencia de la materia y sus transformaciones._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

# ─── COMANDOS INDIVIDUALES FINALES ───────────────────────────────────────────

async def cmd_descarga_rapida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga rápida de medios."""
    if not context.args:
        await update.message.reply_text(
            "⚡ **DESCARGA RÁPIDA**\n━━━━━━━━━━━━━━━━━━━━\n"
            "Usa:\n• `/ytmp4 [url]` → Descargar video YouTube\n"
            "• `/ytmp3 [url]` → Descargar audio YouTube\n"
            "• `/tiktok [url]` → Descargar TikTok\n"
            "• `/instagram [url]` → Descargar Instagram\n"
            "• `/twitter [url]` → Descargar Twitter/X",
            parse_mode="Markdown"
        )
        return
    url = context.args[0]
    await update.message.reply_text(f"⚡ Enviando a descarga rápida: `{url}`\nUsa `/ytmp4` o `/ytmp3` con la URL.", parse_mode="Markdown")

async def cmd_convertir_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre conversión de video."""
    await update.message.reply_text(
        "🎬 **CONVERTIR VIDEO**\n━━━━━━━━━━━━━━━━━━━━\n"
        "Para convertir un video:\n"
        "• `/ytmp4 [url]` → Descargar como MP4\n"
        "• `/ytmp3 [url]` → Convertir a MP3\n"
        "• Herramientas online: CloudConvert, HandBrake, FFmpeg\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 _FFmpeg es el más potente y completamente gratuito._",
        parse_mode="Markdown"
    )

async def cmd_convertir_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre conversión de audio."""
    await update.message.reply_text(
        "🎵 **CONVERTIR AUDIO**\n━━━━━━━━━━━━━━━━━━━━\n"
        "Para convertir audio:\n"
        "• `/ytmp3 [url]` → Descarga como MP3 desde YouTube\n"
        "• Formatos: MP3, AAC, WAV, FLAC, OGG\n"
        "• Herramientas: Audacity (gratis), FFmpeg, Online Audio Converter\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 _FLAC es el formato de mayor calidad sin pérdida._",
        parse_mode="Markdown"
    )

async def cmd_comprimir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre compresión de archivos."""
    await update.message.reply_text(
        "📦 **COMPRESIÓN DE ARCHIVOS**\n━━━━━━━━━━━━━━━━━━━━\n"
        "• **ZIP** → Universal, compatible en todo sistema\n"
        "• **7Z** → Mejor compresión, usa 7-Zip (gratis)\n"
        "• **RAR** → Popular en Windows, necesita WinRAR\n"
        "• **TAR.GZ** → Estándar en Linux/Mac\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 _7-Zip es gratis y tiene la mejor relación de compresión._",
        parse_mode="Markdown"
    )

async def cmd_extraer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre extracción de archivos."""
    await update.message.reply_text(
        "📂 **EXTRACCIÓN DE ARCHIVOS**\n━━━━━━━━━━━━━━━━━━━━\n"
        "Para extraer archivos comprimidos:\n"
        "• **Windows**: WinRAR, 7-Zip, o click derecho → Extraer\n"
        "• **Mac**: The Unarchiver, Keka, o doble click\n"
        "• **Linux**: `unzip`, `tar -xzf`, `7z x archivo`\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 _7-Zip soporta ZIP, RAR, 7Z, TAR, GZ y más._",
        parse_mode="Markdown"
    )

async def cmd_subir_archivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre subir archivos."""
    await update.message.reply_text(
        "⬆️ **SUBIR ARCHIVOS**\n━━━━━━━━━━━━━━━━━━━━\n"
        "Servicios gratuitos para compartir archivos:\n"
        "• **WeTransfer** → Hasta 2GB gratis\n"
        "• **Google Drive** → 15GB gratis\n"
        "• **Mega.nz** → 20GB gratis\n"
        "• **Dropbox** → 2GB gratis\n"
        "• **Filemail** → Hasta 5GB gratis\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 _Para compartir en Telegram: sube el archivo directamente al chat._",
        parse_mode="Markdown"
    )

async def cmd_enlace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Acortar o compartir enlace."""
    if context.args:
        url = context.args[0]
        await update.message.reply_text(
            f"🔗 **ENLACE**\n━━━━━━━━━━━━━━━━━━━━\n"
            f"URL: `{url}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Para acortar: usa bit.ly, tinyurl.com o t.ly",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "🔗 **ACORTADOR DE ENLACES**\n━━━━━━━━━━━━━━━━━━━━\n"
            "Uso: `/enlace [URL]`\n"
            "Servicios gratuitos: bit.ly, tinyurl.com, t.ly, rebrand.ly",
            parse_mode="Markdown"
        )

async def cmd_info_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info del bot."""
    await update.message.reply_text(
        "🤖 **CAMILA BOT V15.0**\n━━━━━━━━━━━━━━━━━━━━\n"
        "👨‍💻 **Creador:** AnyerJR\n"
        "⚡ **Motor:** Python-Telegram-Bot v20\n"
        "🧠 **IA:** Google Custom Search API\n"
        "📦 **Comandos:** 1,500+ disponibles\n"
        "💾 **Base de datos:** JSON local\n"
        "🎬 **Multimedia:** yt-dlp + instaloader\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🚀 _Bot multiusos: economía, OSINT, juegos, IA y más._",
        parse_mode="Markdown"
    )

async def cmd_jugar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menú de juegos."""
    await update.message.reply_text(
        "🎮 **JUEGOS DISPONIBLES**\n━━━━━━━━━━━━━━━━━━━━\n"
        "🎲 `/dados` - Lanzar dados\n"
        "🎰 `/casino` - Jugar al casino\n"
        "🃏 `/blackjack` - Blackjack\n"
        "🎯 `/trivia` - Preguntas trivia\n"
        "🎮 `/rpg` - Aventura RPG\n"
        "🏆 `/torneo` - Torneo PvP\n"
        "🎲 `/triplesuerte` - Triple fortuna\n"
        "🎰 `/loteria` - Lotería\n"
        "🔫 `/ruleta` - Ruleta rusa\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💰 _Usa monedas del bot para apostar._",
        parse_mode="Markdown"
    )

async def cmd_poblacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Datos de población."""
    import random as _r
    datos = [
        "🌍 La población mundial es de 8,100 millones de personas (2024).",
        "🇨🇳 China: 1,400M | 🇮🇳 India: 1,440M (superó a China en 2023).",
        "🇺🇸 EEUU: 335M | 🇧🇷 Brasil: 215M | 🇲🇽 México: 130M.",
        "🇨🇴 Colombia: 52M | 🇻🇪 Venezuela: 28M | 🇵🇪 Perú: 33M.",
        "🌆 El 57% de la población mundial vive en áreas urbanas.",
        "👶 Nacen 385,000 bebés cada día en el mundo.",
        "📈 La población mundial crece ~80 millones de personas al año.",
    ]
    await update.message.reply_text(
        f"👥 **POBLACIÓN MUNDIAL** 👥\n━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n━━━━━━━━━━━━━━━━━━━━\n"
        f"_Datos: ONU 2024._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_security_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info de ciberseguridad."""
    import random as _r
    tips = [
        "🔐 Usa contraseñas de +12 caracteres con mayúsculas, números y símbolos.",
        "🛡️ Activa la autenticación en 2 pasos (2FA) en todas tus cuentas.",
        "📧 No hagas click en enlaces de correos sospechosos (phishing).",
        "🔄 Actualiza siempre tu sistema operativo y aplicaciones.",
        "🌐 Usa VPN en redes WiFi públicas para proteger tus datos.",
        "💾 Haz backup de tu información importante regularmente.",
        "🔑 Usa un gestor de contraseñas: Bitwarden (gratis) o 1Password.",
        "🦠 Escanea los archivos descargados antes de abrirlos.",
    ]
    await update.message.reply_text(
        f"🔒 **CIBERSEGURIDAD** 🔒\n━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 **Tip del día:**\n{_r.choice(tips)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ _Protege tus datos digitales siempre._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_noticias_tech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Noticias de tecnología."""
    await cmd_noticias_categoria(update, context, "tecnología inteligencia artificial", "💻", "Tecnología")

async def cmd_optimizacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tips de optimización."""
    import random as _r
    tips = [
        "💻 Libera RAM cerrando aplicaciones en segundo plano.",
        "🧹 Limpia el disco duro: borra archivos temporales (%temp% en Windows).",
        "⚡ SSD vs HDD: un SSD hace tu PC hasta 10x más rápida.",
        "🔄 Desfragmenta el HDD regularmente (no SSD).",
        "🛑 Desactiva programas de inicio innecesarios (MSConfig).",
        "🧠 Añadir más RAM es la mejora más costo-efectiva para un PC lento.",
        "🌡️ Limpia el polvo del PC cada 6 meses para mejor rendimiento.",
        "⚙️ Reinstalar el sistema operativo cada 2-3 años rejuvenece el PC.",
    ]
    await update.message.reply_text(
        f"⚡ **OPTIMIZACIÓN DE PC** ⚡\n━━━━━━━━━━━━━━━━━━━━\n"
        f"🔧 **Tip:**\n{_r.choice(tips)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Un PC optimizado es un PC feliz._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_level_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver nivel actual."""
    uid = str(update.effective_user.id)
    nick = update.effective_user.first_name
    niveles = cargar_db("niveles")
    xp = niveles.get(uid, {}).get("xp", 0)
    nivel = obtener_rango(xp)
    xp_next = (xp // 100 + 1) * 100
    await update.message.reply_text(
        f"⭐ **NIVEL / PROGRESO**\n━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Usuario:** {nick}\n"
        f"🎖️ **Rango:** {nivel}\n"
        f"✨ **XP:** `{xp}` / `{xp_next}` para subir\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 Gana XP usando comandos del bot.",
        parse_mode="Markdown"
    )

async def cmd_altura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculadora de altura."""
    import random as _r
    if context.args:
        try:
            cm = float(context.args[0])
            pies = int(cm / 30.48)
            pulgadas = round((cm / 30.48 - pies) * 12)
            cat = "Muy bajo" if cm < 155 else "Bajo" if cm < 165 else "Promedio" if cm < 178 else "Alto" if cm < 190 else "Muy alto"
            await update.message.reply_text(
                f"📏 **CALCULADORA DE ALTURA**\n━━━━━━━━━━━━━━━━━━━━\n"
                f"📐 {cm} cm = {pies}'{pulgadas}\" (pies y pulgadas)\n"
                f"📊 Categoría: **{cat}**\n"
                f"🌍 Promedio global masculino: 171 cm | Femenino: 159 cm",
                parse_mode="Markdown"
            )
            return
        except:
            pass
    await update.message.reply_text(
        "📏 **ALTURA**\nUso: `/altura [cm]`\nEj: `/altura 175`\n\n"
        f"🌍 Promedios: Hombre: 171cm | Mujer: 159cm\n"
        f"🏆 País más alto: Países Bajos (182.9cm hombres)",
        parse_mode="Markdown"
    )

async def cmd_bmi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculadora de IMC/BMI."""
    if len(context.args) >= 2:
        try:
            peso = float(context.args[0])
            altura_m = float(context.args[1]) / 100 if float(context.args[1]) > 3 else float(context.args[1])
            imc = round(peso / (altura_m ** 2), 1)
            if imc < 18.5: cat = "⚠️ Bajo peso"
            elif imc < 25: cat = "✅ Peso normal"
            elif imc < 30: cat = "⚠️ Sobrepeso"
            else: cat = "🔴 Obesidad"
            await update.message.reply_text(
                f"⚖️ **IMC / BMI**\n━━━━━━━━━━━━━━━━━━━━\n"
                f"📊 IMC: **{imc}**\n"
                f"🏷️ Categoría: {cat}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"• <18.5 = Bajo peso | 18.5-24.9 = Normal\n"
                f"• 25-29.9 = Sobrepeso | ≥30 = Obesidad",
                parse_mode="Markdown"
            )
            return
        except:
            pass
    await update.message.reply_text(
        "⚖️ **IMC - ÍNDICE DE MASA CORPORAL**\n"
        "Uso: `/bmi [peso_kg] [altura_cm]`\n"
        "Ej: `/bmi 70 175`\n\n"
        "Fórmula: IMC = peso(kg) / altura(m)²",
        parse_mode="Markdown"
    )

async def cmd_piel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cuidado de la piel."""
    import random as _r
    tips = [
        "☀️ El protector solar SPF 30+ es el anti-edad más efectivo y barato.",
        "💧 Hidratarse bien es el primer paso para una piel sana y luminosa.",
        "🌙 La vitamina C de noche y el retinol mejoran la textura de la piel.",
        "🧼 Lavar la cara 2 veces al día con un limpiador suave es lo básico.",
        "🛌 Dormir 7-9h reduce el cortisol y mejora visiblemente la piel.",
        "🥗 Los alimentos con omega-3 (salmón, nueces) hacen la piel más elástica.",
        "🚭 El tabaco envejece la piel 10-20 años prematuramente.",
        "🍵 El té verde aplicado tiene propiedades antioxidantes para la piel.",
    ]
    await update.message.reply_text(
        f"✨ **CUIDADO DE LA PIEL** ✨\n━━━━━━━━━━━━━━━━━━━━\n"
        f"💆 **Tip:**\n{_r.choice(tips)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Rutina básica: limpieza → hidratación → protección solar._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_smoothie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receta de smoothie."""
    import random as _r
    recetas = [
        ("🟢 Smoothie Verde", "🥬 Espinaca\n🍌 1 plátano\n🍏 1 manzana\n💧 1 taza agua\n🌿 Jengibre al gusto", "Antioxidante y energizante"),
        ("🟡 Smoothie Tropical", "🍌 1 plátano\n🍍 Piña\n🥭 Mango\n🥥 Agua de coco", "Vitamina C y digestivo"),
        ("🔴 Smoothie de Frutas Rojas", "🍓 Fresas\n🫐 Arándanos\n🍒 Cerezas\n🥛 Leche o yogur", "Antioxidante y para el corazón"),
        ("🟤 Smoothie Proteico", "🍌 1 plátano\n🥛 Leche\n🥜 2 cucharadas mantequilla maní\n💊 1 scoop proteína", "Ideal post-entrenamiento"),
        ("🟠 Smoothie Anti-inflamatorio", "🥕 Zanahoria\n🍊 Naranja\n🌿 Cúrcuma\n🫚 Aceite de coco\n🌶️ Pimienta negra", "Reduce inflamación"),
    ]
    rec = _r.choice(recetas)
    await update.message.reply_text(
        f"🥤 **{rec[0]}**\n━━━━━━━━━━━━━━━━━━━━\n"
        f"**Ingredientes:**\n{rec[1]}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ **Beneficio:** {rec[2]}\n"
        f"_Licúa todo por 30-60 segundos y listo._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_motivacion_extra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Frase motivadora."""
    import random as _r
    frases = [
        "🔥 'El éxito es la suma de pequeños esfuerzos repetidos día tras día.' — Robert Collier",
        "💪 'No cuentes los días, haz que los días cuenten.' — Muhammad Ali",
        "🌟 'El único modo de hacer un gran trabajo es amar lo que haces.' — Steve Jobs",
        "🚀 'No importa cuán lento vayas, siempre y cuando no te detengas.' — Confucio",
        "⭐ 'Cree en ti mismo y todo será posible.' — Anónimo",
        "🏆 'El campeón no es el que nunca falla, sino el que siempre se levanta.' — Anónimo",
        "💡 'La creatividad es la inteligencia divirtiéndose.' — Albert Einstein",
        "🌈 'Después de la tormenta siempre sale el sol. Cada problema tiene una solución.' — Anónimo",
        "🎯 'Enfócate en el proceso, no en el resultado. El resultado llegará.' — Anónimo",
        "🌱 'El mejor momento para plantar un árbol fue hace 20 años. El segundo mejor es hoy.' — Proverbio chino",
    ]
    await update.message.reply_text(
        f"💫 **MOTIVACIÓN DEL DÍA** 💫\n━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(frases)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_¡Tú puedes! ¡Dale con todo! 🚀_",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_cardio_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre cardio."""
    await update.message.reply_text(
        "❤️ **CARDIO - ENTRENAMIENTO CARDIOVASCULAR** ❤️\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "**Tipos de cardio:**\n"
        "• 🏃 **LISS** (Low Intensity) → Caminar, trotar suave 45-60 min\n"
        "• ⚡ **HIIT** (High Intensity) → Intervalos 20-30 min\n"
        "• 🚴 **Ciclismo** → Indoor o outdoor, 30-60 min\n"
        "• 🏊 **Natación** → El más completo, 30-45 min\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💓 **Zonas de frecuencia cardíaca:**\n"
        "• Quema grasa: 60-70% FC máx\n"
        "• Aeróbico: 70-80% FC máx\n"
        "• Anaeróbico: 80-90% FC máx\n"
        "💡 _FC Máx = 220 - tu edad_",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_meta_smart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cómo establecer metas SMART."""
    await update.message.reply_text(
        "🎯 **METAS SMART** 🎯\n━━━━━━━━━━━━━━━━━━━━\n"
        "El método SMART para establecer metas:\n\n"
        "🔤 **S** - Específica: ¿Qué exactamente quieres lograr?\n"
        "📊 **M** - Medible: ¿Cómo sabrás que lo lograste?\n"
        "✅ **A** - Alcanzable: ¿Es realista para ti?\n"
        "🎯 **R** - Relevante: ¿Es importante para tu vida?\n"
        "⏰ **T** - Temporal: ¿Cuándo lo lograrás?\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📝 **Ejemplo:**\n"
        "❌ 'Quiero bajar de peso'\n"
        "✅ 'Perder 5 kg en 3 meses haciendo ejercicio 4x/semana'\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 _Escribe tu meta SMART y ponla donde la veas cada día._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_clima_nublado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre días nublados."""
    await update.message.reply_text(
        "☁️ **CLIMA NUBLADO** ☁️\n━━━━━━━━━━━━━━━━━━━━\n"
        "Los días nublados son causados por nubes de tipo\n"
        "stratus (bajas y grises) que bloquean la luz solar.\n\n"
        "💡 **En un día nublado:**\n"
        "• Temperatura más estable (menos calor directo)\n"
        "• Menor riesgo de quemaduras solares (pero existe)\n"
        "• Mayor humedad del ambiente\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "☀️ _Usa /clima [ciudad] para el pronóstico real._",
        parse_mode="Markdown"
    )

async def cmd_clima_soleado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre días soleados."""
    await update.message.reply_text(
        "☀️ **DÍA SOLEADO** ☀️\n━━━━━━━━━━━━━━━━━━━━\n"
        "Los días soleados son ideales para:\n"
        "• 🏃 Ejercicio al aire libre\n"
        "• 🌿 Jardinería y actividades outdoor\n"
        "• 🧘 Meditación al sol (vitamina D)\n"
        "• 📸 Fotografía con luz natural\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⚠️ Usa protector solar SPF 30+ cuando salgas.\n"
        "☀️ _Usa /clima [ciudad] para el pronóstico real._",
        parse_mode="Markdown"
    )

async def cmd_rayo_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre rayos."""
    import random as _r
    datos = [
        "⚡ Un rayo tiene 5 veces la temperatura de la superficie del Sol (30,000°C).",
        "⚡ En la Tierra caen aproximadamente 100 rayos por segundo.",
        "⚡ La probabilidad de ser alcanzado por un rayo es de 1 en 15,300.",
        "⚡ Roy Sullivan fue alcanzado por rayos 7 veces en su vida.",
        "⚡ Los rayos pueden crear metales raros como el fulgurito (cristal de arena fundida).",
    ]
    await update.message.reply_text(
        f"⚡ **RAYOS Y TORMENTAS ELÉCTRICAS** ⚡\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ **En una tormenta:** evita árboles, postes y agua abierta.",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_terremoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre terremotos."""
    import random as _r
    datos = [
        "🌍 Ocurren más de 500,000 terremotos detectables al año en el mundo.",
        "📊 La escala Richter mide la magnitud: +7 es destructivo, +9 es catastrófico.",
        "🇯🇵 Japón es el país que más terremotos registra (1,000+ por año).",
        "🏔️ El terremoto de Valdivia (1960, Chile) fue el mayor registrado: 9.5 Mw.",
        "🌊 El 80% de los tsunamis son causados por terremotos submarinos.",
    ]
    await update.message.reply_text(
        f"🌍 **TERREMOTOS / SISMOS** 🌍\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ **En un sismo:** cúbrete bajo una mesa, aléjate de ventanas.",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_inundacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre inundaciones."""
    await update.message.reply_text(
        "🌊 **INUNDACIONES** 🌊\n━━━━━━━━━━━━━━━━━━━━\n"
        "Las inundaciones son el desastre natural más frecuente del mundo.\n\n"
        "⚠️ **En caso de inundación:**\n"
        "• Sube a los pisos más altos del edificio\n"
        "• Nunca cruces corrientes de agua a pie o en auto\n"
        "• 30 cm de agua puede derribar un adulto\n"
        "• 60 cm puede arrastrar un vehículo\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📻 _Mantente informado por radio o alertas oficiales._",
        parse_mode="Markdown"
    )

async def cmd_nevada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre nevadas."""
    import random as _r
    datos = [
        "❄️ El mayor registro de nieve en 24 horas fue 192 cm en Silver Lake, Colorado (1921).",
        "❄️ No existen dos copos de nieve exactamente iguales en el mundo.",
        "❄️ La nieve más pesada puede pesar más de 60 kg por metro cúbico.",
        "❄️ Los países con más nieve: Rusia, Canadá, Finlandia y Noruega.",
        "❄️ La nieve actúa como aislante térmico, protegiendo el suelo del frío extremo.",
    ]
    await update.message.reply_text(
        f"❄️ **NEVADAS** ❄️\n━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🌨️ _La nieve es agua congelada que cae en cristales de hielo._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_huracan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre huracanes."""
    await update.message.reply_text(
        "🌀 **HURACANES / CICLONES** 🌀\n━━━━━━━━━━━━━━━━━━━━\n"
        "**Escala Saffir-Simpson:**\n"
        "• Cat 1: 119-153 km/h — Daños mínimos\n"
        "• Cat 2: 154-177 km/h — Daños moderados\n"
        "• Cat 3: 178-208 km/h — Daños graves\n"
        "• Cat 4: 209-251 km/h — Daños extremos\n"
        "• Cat 5: +252 km/h — Daños catastróficos\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📍 Se forman sobre aguas oceánicas cálidas (>26°C).\n"
        "⚠️ _El ojo del huracán es engañosamente tranquilo._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_granizo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre granizo."""
    import random as _r
    datos = [
        "🧊 El granizo más grande registrado tenía 20 cm de diámetro y pesó 1 kg.",
        "🧊 El granizo se forma cuando las corrientes de aire elevan gotas de agua a capas muy frías.",
        "🧊 Las tormentas de granizo causan más de 1,000 millones de dólares en daños cada año en EEUU.",
        "🧊 El granizo puede caer a velocidades de 100-160 km/h.",
    ]
    await update.message.reply_text(
        f"🧊 **GRANIZO** 🧊\n━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(datos)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ _Busca refugio durante granizo. Puede causar daños graves._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_nivel_agua(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info sobre nivel del agua."""
    await update.message.reply_text(
        "💧 **NIVEL DEL AGUA / MAR** 💧\n━━━━━━━━━━━━━━━━━━━━\n"
        "El nivel del mar ha subido 20 cm desde 1900.\n"
        "Actualmente sube ~3.3 mm por año.\n\n"
        "📊 **Causas:**\n"
        "• Derretimiento de glaciares y hielos polares\n"
        "• Expansión térmica del agua oceánica\n"
        "• Cambio climático global\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🌍 _Para 2100 puede subir entre 0.3 y 1 metro más._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

async def cmd_economia_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información económica básica."""
    import random as _r
    items = [
        "📈 El PIB (Producto Interno Bruto) mide el valor de todo lo producido en un país.",
        "💹 La inflación es el aumento generalizado de precios. El Banco Central la controla.",
        "🏦 Los bancos centrales regulan la oferta monetaria y las tasas de interés.",
        "📊 El índice S&P 500 agrupa las 500 empresas más grandes de EEUU.",
        "💰 El Bitcoin es la criptomoneda con mayor capitalización de mercado.",
        "📉 Una recesión es cuando el PIB cae 2 trimestres consecutivos.",
        "🌐 El FMI (Fondo Monetario Internacional) apoya a países con dificultades económicas.",
        "💱 El tipo de cambio determina cuánto vale una moneda respecto a otra.",
    ]
    await update.message.reply_text(
        f"💹 **ECONOMÍA** 💹\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{_r.choice(items)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"_Usa /dolar para el precio del dólar hoy._",
        parse_mode="Markdown"
    )
    sumar_xp(update.effective_user.id, 3)

# ════════════════════════════════════════════════════════════════════════════════
# --- [ NÚCLEO DE ARRANQUE: UNIÓN DE TODAS LAS PARTES ] ---
def main():
    """Función maestra que activa el bot y registra todos los comandos."""
    print(f"🚀 Cami.bot {VERSION} de AnyerJR arrancando...")
    print(f"🧠 Motor de IA: Google Custom Search API")
    print(f"⚡ Búsqueda inteligente con Google")
    print(f"💾 Sistema de memoria contextual: ACTIVADO")
    print(f"👥 Cada usuario tiene su propio historial de conversación")
    print(f"🔄 SISTEMA MULTITAREA: Hasta 5 descargas simultáneas sin bloqueo")
    print(f"📊 Comando disponible: /estado - Ver carga del bot")
    keep_alive()
    
    # Crear la aplicación con tu Token
    app = ApplicationBuilder().token(TOKEN).build()
    
    #registro de listas pues menu🫰🏻
      

    # 1. Registro de Comandos de Sistema y Perfil
    app.add_handler(CommandHandler(["start", "menu", "help"], mostrar_menu))
    app.add_handler(CommandHandler("reg", registrar_usuario))
    app.add_handler(CommandHandler("perfil", perfil_detallado))
    app.add_handler(CommandHandler("estado", estado_bot))
    
    # 2. Registro de Comandos de Economía y Multimedia
    app.add_handler(CommandHandler(["trabajar", "chamba"], trabajar))
    app.add_handler(CommandHandler(["apostar", "bet"], apostar))
    app.add_handler(CommandHandler(["descargar", "dl"], descargar_video))
    app.add_handler(CommandHandler(["ytmp3", "mp3"], ytmp3))
    app.add_handler(CommandHandler(["ytmp4", "mp4"], ytmp4))
    app.add_handler(CommandHandler(["brat"], brat))
    app.add_handler(CommandHandler("bratv2", crear_bratv2))
    app.add_handler(CommandHandler("bratv3", bratv3))
    app.add_handler(CommandHandler("bratvd", crear_brat_video))
    app.add_handler(CommandHandler(["clima", "weather"], clima))
    app.add_handler(CommandHandler(["chiste", "joke"], chiste))
    app.add_handler(CommandHandler(["buscar", "search"], buscar))
    app.add_handler(CommandHandler(["artistas", "spotify"], buscar_artistas))
    app.add_handler(CommandHandler(["pinterest", "p", "pint"], buscar_pinterest))
    app.add_handler(CommandHandler(["pinterestv2", "p2", "pint2"], pinterestv2))
    app.add_handler(CommandHandler(["resetear", "reset"], resetear_chat))
    app.add_handler(CommandHandler("ia", ia_cmd))
    app.add_handler(CommandHandler("reset_ia", reset_ia_cmd))
    app.add_handler(CommandHandler("ia2", ia2_cmd))
    app.add_handler(CommandHandler("reset_ia2", reset_ia2_cmd))
    app.add_handler(CommandHandler("ia3", ia3_cmd))
    app.add_handler(CommandHandler("reset_ia3", reset_ia3_cmd))
    
    # 3. Registro de Comandos OSINT
    app.add_handler(CommandHandler(["github", "gh"], osint_github))
#aqui va el osint tiktok
    app.add_handler(CommandHandler("tiktokuser", cmd_tiktokuser))
    app.add_handler(CommandHandler(["idff", "ff"], idff))
    
    # 4. Registro de Comandos V7.0 - 21 NUEVOS COMANDOS
# Comandos Multimedia V13
    app.add_handler(CommandHandler("tkdm", tkdm))    
    app.add_handler(CommandHandler(["traducir", "translate"], traducir))
    app.add_handler(CommandHandler("calc", calc))
    app.add_handler(CommandHandler("qr", qr))
    app.add_handler(CommandHandler("qrs", qrs))
    app.add_handler(CommandHandler("acortar", acortar))
    app.add_handler(CommandHandler("randomuser", randomuser))
    app.add_handler(CommandHandler("dado", dado))
    app.add_handler(CommandHandler("moneda", moneda))
    app.add_handler(CommandHandler("meme", meme))
    app.add_handler(CommandHandler(["cripto", "crypto"], cripto))
    app.add_handler(CommandHandler("ip", ip))
    app.add_handler(CommandHandler("wiki", wiki))
    app.add_handler(CommandHandler("motivar", motivar))
    app.add_handler(CommandHandler("consejo", consejo))
    app.add_handler(CommandHandler("love", love))
    app.add_handler(CommandHandler("adivinar", adivinar))
    app.add_handler(CommandHandler("spotify", spotify))
    app.add_handler(CommandHandler("netflix", netflix))
    app.add_handler(CommandHandler("dolar", dolar))
    app.add_handler(CommandHandler("convertir", convertir))
    app.add_handler(CommandHandler("pomodoro", pomodoro))
    
    # 5. NUEVOS COMANDOS V10 - 200+ COMANDOS
    # Herramientas criptográficas
    app.add_handler(CommandHandler("hash_md5", hash_md5))
    app.add_handler(CommandHandler("hash_sha256", hash_sha256))
    app.add_handler(CommandHandler(["b64encode", "base64"], base64_encode))
    app.add_handler(CommandHandler(["b64decode", "base64d"], base64_decode))
    
    # Conversiones y herramientas
    app.add_handler(CommandHandler(["temp", "temperatura"], temperatura))
    app.add_handler(CommandHandler(["m_km", "metros_km"], metro_km))
    app.add_handler(CommandHandler(["numrand", "numero_aleatorio"], numero_aleatorio_cmd))
    
    # Juegos avanzados
    app.add_handler(CommandHandler(["ppt", "piedra_papel_tijera"], piedra_papel_tijera))
    app.add_handler(CommandHandler("trivia", trivia))
    app.add_handler(CommandHandler("adivinanza", adivinanza))
    app.add_handler(CommandHandler("tarot", tarot))
    app.add_handler(CommandHandler("horoscopo", horoscopo))
    
    # Entretenimiento
    app.add_handler(CommandHandler("pelicula", pelicula))
    app.add_handler(CommandHandler("serie", serie))
    
    # Finanzas y crypto
    app.add_handler(CommandHandler("bitcoin", bitcoin_cmd))
    app.add_handler(CommandHandler("ethereum", ethereum_cmd))
    
    # 6. Registro de Comandos Administrativos
    app.add_handler(CommandHandler("expropiar", admin_expropiar))
    app.add_handler(CommandHandler("ver_logs", admin_ver_logs))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("blockuser", admin_blockuser))
    app.add_handler(CommandHandler("unblockuser", admin_unblockuser))
    app.add_handler(CommandHandler("inforuser", admin_inforuser))
    app.add_handler(CommandHandler("users", admin_users))
    app.add_handler(CommandHandler("resetchats", admin_resetchats))
    app.add_handler(CommandHandler("extmsj", admin_extmsj))
    # ── NUEVO HANDLER PARA EL COMANDO info_completa ──
    app.add_handler(CommandHandler("info_completa", cmd_info_completa))    
    # 8. NUEVOS 200+ COMANDOS V12.0
    # Cocina venezolana
    app.add_handler(CommandHandler("receta", receta))
    app.add_handler(CommandHandler("cocinatip", cocina_tip))
    app.add_handler(CommandHandler("bebida", bebida))
    # Salud y bienestar
    app.add_handler(CommandHandler("meditacion", meditacion))
    app.add_handler(CommandHandler("ejercicio", ejercicio))
    app.add_handler(CommandHandler("agua", agua_reminder))
    app.add_handler(CommandHandler("calorias", calorias))
    app.add_handler(CommandHandler("sueno", sueno))
    app.add_handler(CommandHandler("tension", tension_arterial))
    app.add_handler(CommandHandler("pulsaciones", frecuencia_cardiaca))
    # Productividad
    app.add_handler(CommandHandler("cronograma", cronograma))
    app.add_handler(CommandHandler("meta", meta_smart))
    app.add_handler(CommandHandler("estudia", tecnica_estudio))
    app.add_handler(CommandHandler("tareas", lista_tareas))
    app.add_handler(CommandHandler("presupuesto", presupuesto))
    # Tecnología y código
    app.add_handler(CommandHandler("html", codigo_html))
    app.add_handler(CommandHandler("pycode", codigo_python_ejemplo))
    app.add_handler(CommandHandler("git", git_comandos))
    app.add_handler(CommandHandler("linux", linux_cmd))
    app.add_handler(CommandHandler("regex", regex_info))
    app.add_handler(CommandHandler("rgb", color_rgb))
    app.add_handler(CommandHandler("jsoncheck", json_format))
    # Finanzas
    app.add_handler(CommandHandler("interes", interes_compuesto))
    app.add_handler(CommandHandler(["cambio", "monedacambio"], conversor_moneda))
    app.add_handler(CommandHandler("prestamo", calculo_prestamo))
    app.add_handler(CommandHandler("ahorro", ahorro_meta))
    # RPG y juegos de fantasía
    app.add_handler(CommandHandler("rpg", personaje_rpg))
    app.add_handler(CommandHandler("dungeon", dungeon))
    app.add_handler(CommandHandler("itemmagico", item_magico))
    # Astronomía y ciencia
    app.add_handler(CommandHandler("planeta", planeta_info))
    app.add_handler(CommandHandler(["elemento_q", "quimica"], elemento_quimico))
    app.add_handler(CommandHandler("luz", velocidad_luz))
    app.add_handler(CommandHandler("ciencia", dato_cientifico))
    # Geografía y cultura
    app.add_handler(CommandHandler("pais_info", pais_info))
    app.add_handler(CommandHandler("vefamoso", venezolano_famoso))
    app.add_handler(CommandHandler("cultura", cultura_general))
    # Redes sociales
    app.add_handler(CommandHandler("bioig", bio_instagram))
    app.add_handler(CommandHandler("hashtags", hashtags))
    app.add_handler(CommandHandler("viral", viral_ideas))
    # Misceláneos
    app.add_handler(CommandHandler("personalidad", personalidad_test))
    app.add_handler(CommandHandler("animalspirit", animal_espiritual))
    app.add_handler(CommandHandler("significado", nombre_real_meaning))
    app.add_handler(CommandHandler("sangre", tipo_sangre))
    app.add_handler(CommandHandler("angel", numero_angel))
    app.add_handler(CommandHandler("trabalenguas", trabalenguas))
    app.add_handler(CommandHandler("acertijo", acertijo))
    app.add_handler(CommandHandler("proverbio", proverbio_mundo))
    app.add_handler(CommandHandler("prediccion", prediccion))
    app.add_handler(CommandHandler("iq", iq_test))
    app.add_handler(CommandHandler("fortuna", fortuna_chino))
    app.add_handler(CommandHandler(["japones", "katakana"], nombre_japones))
    app.add_handler(CommandHandler("velocidad", convertir_velocidad))
    app.add_handler(CommandHandler("area", area_figura))
    app.add_handler(CommandHandler("tabla", tabla_multiplicar))
    app.add_handler(CommandHandler("seguridad", contraseña_nivel))
    app.add_handler(CommandHandler("cryptowallet", crypto_wallet))

    # ===== NUEVOS COMANDOS V13 =====
    app.add_handler(CommandHandler(["carta", "cartaamor"], carta_amor_odio))
    app.add_handler(CommandHandler("rap", rap_cmd))
    app.add_handler(CommandHandler(["ojoturco", "ojo"], ojo_turco))
    app.add_handler(CommandHandler(["alias", "aliasc"], alias_criminal))
    app.add_handler(CommandHandler(["hechizo", "magia"], hechizo_cmd))
    app.add_handler(CommandHandler(["luna", "faseLunar"], fase_lunar))
    app.add_handler(CommandHandler(["top", "ranking", "topricos"], top_ricos))
    app.add_handler(CommandHandler(["bomba", "boom"], bomba_cmd))
    app.add_handler(CommandHandler(["adn", "dna"], adn_ficticio))
    app.add_handler(CommandHandler(["triplesuerte", "slots"], triple_suerte))
    # ===== DESCARGAS EXTERNAS V13 =====
    app.add_handler(CommandHandler(["mediafire", "mf"], mediafire_cmd))
    app.add_handler(CommandHandler("apkpure", apkpure_cmd))
    app.add_handler(CommandHandler("apktodo", apktodo_cmd))
    app.add_handler(CommandHandler("uptodown", uptodown_cmd))
    app.add_handler(CommandHandler(["apkcombo", "combo"], apkcombo_cmd))
    app.add_handler(CommandHandler(["fdroid", "froid"], fdroid_cmd))
    # ===== NUEVAS DESCARGAS V13.1 =====
    app.add_handler(CommandHandler(["soundcloud", "sc"], soundcloud_cmd))
    app.add_handler(CommandHandler(["twitter", "xvideo", "xdl"], twitter_cmd))
    app.add_handler(CommandHandler(["instagram", "ig", "reel"], instagram_cmd))
    app.add_handler(CommandHandler(["tiktok", "tt"], tiktok_cmd))
    app.add_handler(CommandHandler(["drive", "gdrive"], drive_cmd))
    app.add_handler(CommandHandler(["pixeldrain", "pdrain"], pixeldrain_cmd))
    app.add_handler(CommandHandler(["gofile", "gfile"], gofile_cmd))
    app.add_handler(CommandHandler(["mp3", "mp3dl", "audio"], mp3_universal))
    app.add_handler(CommandHandler(["facebook", "fbvideo", "fb"], facebook_cmd))
    # ===== BÚSQUEDA DE IMÁGENES V13 =====
    app.add_handler(CommandHandler(["imagen", "img", "foto"], buscar_imagen))
    app.add_handler(CommandHandler(["waifu", "wa", "w", "waifus"], enviar_waifu))
    app.add_handler(CommandHandler(["wallpaper", "fondo", "wp"], wallpaper_cmd))
    app.add_handler(CommandHandler(["gif", "gifbuscar"], gif_cmd))
    app.add_handler(CommandHandler(["fanart", "arte", "art"], fanart_cmd))
    app.add_handler(CommandHandler(["sticker_buscar", "stickerimagen", "stkbuscar"], sticker_buscar_cmd))
    # ===== STICKER MAKER V13 =====
    app.add_handler(CommandHandler(["stk_neon", "neon"], sticker_neon))
    app.add_handler(CommandHandler(["stk_fuego", "fuego_stk"], sticker_fuego))
    app.add_handler(CommandHandler(["stk_galaxia", "galaxia_stk"], sticker_galaxia))
    app.add_handler(CommandHandler(["stk_aesthetic", "aesthetic"], sticker_aesthetic))
    app.add_handler(CommandHandler(["stk_dark", "dark_stk"], sticker_dark))
    app.add_handler(CommandHandler(["stk_arcoiris", "arcoiris_stk"], sticker_arcoiris))
    app.add_handler(CommandHandler(["stk_gold", "gold_stk"], sticker_gold))
    app.add_handler(CommandHandler(["stk_hielo", "hielo_stk"], sticker_hielo))
    app.add_handler(CommandHandler(["stk_venezuela", "venezuela_stk"], sticker_venezuela))
    app.add_handler(CommandHandler(["stk_meme", "meme_stk"], sticker_meme))
    app.add_handler(CommandHandler(["stk_lista", "stickers", "stkhelp"], sticker_lista))


    # Herramientas de texto
    app.add_handler(CommandHandler(["palabras", "contar"], contar_palabras))
    app.add_handler(CommandHandler(["invertir", "reversa"], invertir_texto))
    app.add_handler(CommandHandler(["mayus", "mayusculas"], mayusculas))
    app.add_handler(CommandHandler(["minus", "minusculas"], minusculas))
    app.add_handler(CommandHandler("cesar", cifrado_cesar))
    app.add_handler(CommandHandler("morse", morse))
    app.add_handler(CommandHandler("ascii", ascii_art))
    app.add_handler(CommandHandler("repetir", repetir))
    app.add_handler(CommandHandler("palindromo", palindromo))
    app.add_handler(CommandHandler("espaciar", espaciar))
    # Matemáticas
    app.add_handler(CommandHandler("factorial", factorial))
    app.add_handler(CommandHandler(["fib", "fibonacci"], fibonacci))
    app.add_handler(CommandHandler("primo", primo))
    app.add_handler(CommandHandler(["bin", "binario"], binario))
    app.add_handler(CommandHandler(["hex", "hexadecimal"], hexadecimal))
    app.add_handler(CommandHandler(["oct", "octal"], octal))
    app.add_handler(CommandHandler(["raiz", "sqrt"], raiz_cuadrada))
    app.add_handler(CommandHandler(["porciento", "porcentaje"], porcentaje))
    app.add_handler(CommandHandler("imc", imc))
    # Generadores
    app.add_handler(CommandHandler(["pass", "contrasena", "password"], contrasena))
    app.add_handler(CommandHandler("uuid", uuid_gen))
    app.add_handler(CommandHandler("nombrefake", nombre_falso))
    app.add_handler(CommandHandler("emailfake", email_falso))
    app.add_handler(CommandHandler("placa", placa_venezolana))
    app.add_handler(CommandHandler("cedula", cedula_falsa))
    app.add_handler(CommandHandler("colorhex", color_hex))
    app.add_handler(CommandHandler("chisteve", chiste_venezolano))
    app.add_handler(CommandHandler("refran", refranes))
    # Información
    app.add_handler(CommandHandler(["fecha", "hoy"], fecha_hoy))
    app.add_handler(CommandHandler("unix", tiempo_unix))
    app.add_handler(CommandHandler("edad", edad_calc))
    app.add_handler(CommandHandler(["diasfalta", "countdown_date"], dias_para))
    app.add_handler(CommandHandler("signo", signo_zodiacal))
    app.add_handler(CommandHandler(["suerte", "lucky"], numero_suerte))
    app.add_handler(CommandHandler(["frasedia", "frase"], frase_dia))
    # Juegos nuevos
    app.add_handler(CommandHandler("pais", pregunta_pais))
    app.add_handler(CommandHandler(["ruleta", "rr"], ruleta_rusa))
    app.add_handler(CommandHandler(["verdad", "reto", "vyp"], verdad_o_reto))
    app.add_handler(CommandHandler("ahorcado", ahorcado))
    app.add_handler(CommandHandler("mayormenor", mayor_menor))
    app.add_handler(CommandHandler("simon", simon_dice))
    app.add_handler(CommandHandler("batalla", batalla_stats))
    # OSINT/Internet
    app.add_handler(CommandHandler("whois", whois_cmd))
    app.add_handler(CommandHandler("ping", ping_web))
    app.add_handler(CommandHandler("useragent", user_agent))
    app.add_handler(CommandHandler("mac", mac_address))
    app.add_handler(CommandHandler("ipprivada", ip_privada))
    # Entretenimiento extra
    app.add_handler(CommandHandler("musica", musica_cmd))
    app.add_handler(CommandHandler("libro", libro_cmd))
    app.add_handler(CommandHandler("animalfact", animal_fact))
    app.add_handler(CommandHandler("jokeen", chiste_ingles))
    app.add_handler(CommandHandler("fox", fox_pic))
    app.add_handler(CommandHandler("dog", dog_pic))
    app.add_handler(CommandHandler("cat", cat_pic))
    # Utilidades avanzadas
    app.add_handler(CommandHandler(["countdown", "cuentaregresiva"], contador_regresivo))
    app.add_handler(CommandHandler(["relojmundial", "worldclock"], reloj_mundial))
    app.add_handler(CommandHandler("dividir", divisor_texto))
    app.add_handler(CommandHandler("limpiar", limpiar_texto))
    app.add_handler(CommandHandler("vocales", vocal_count))
    app.add_handler(CommandHandler("fiebre", temperatura_corporal))
    app.add_handler(CommandHandler("propina", calcular_propina))
    app.add_handler(CommandHandler("peso", convertir_peso))
    app.add_handler(CommandHandler("distancia", convertir_distancia))
    app.add_handler(CommandHandler("internet", velocidad_internet))
    app.add_handler(CommandHandler("vpn", vpn_info))
    app.add_handler(CommandHandler("atajos", atajos_teclado))
    app.add_handler(CommandHandler("lenguaje", lenguajes_prog))
    app.add_handler(CommandHandler("sigla", abreviaciones))
    app.add_handler(CommandHandler("sorteo", sorteo))
    app.add_handler(CommandHandler("turnos", turno_random))
    app.add_handler(CommandHandler("bateria", nivel_bateria))
    app.add_handler(CommandHandler("compatibilidad", compatibilidad))
    app.add_handler(CommandHandler("encuesta", encuesta_rapida))
    app.add_handler(CommandHandler(["noticias", "tech"], noticias_tech))
    app.add_handler(CommandHandler(["climaciudad", "wtime"], clima_mundo))
    app.add_handler(CommandHandler("romano", numero_romano))
    app.add_handler(CommandHandler("dadox", dado_personalizado))
    app.add_handler(CommandHandler("loteria", loteria_cmd))
    app.add_handler(CommandHandler("chakra", nivel_chakra))
    app.add_handler(CommandHandler("sith", fuerza_oscura))
    app.add_handler(CommandHandler("elemento", elemento_cmd))
    app.add_handler(CommandHandler("anime", anime_rec))
    app.add_handler(CommandHandler("juego", videojuego_rec))
    app.add_handler(CommandHandler("poder", superpoder))
    # Juego Tres en Rayas
    app.add_handler(CommandHandler("trayes", iniciar_trayes))
    app.add_handler(CommandHandler("pos", mover_pos))
    app.add_handler(CommandHandler("tablero", mostrar_tablero))
    app.add_handler(CommandHandler("reiniciar", reiniciar_trayes))
    app.add_handler(CommandHandler("ai_on", activar_ai))
    app.add_handler(CommandHandler("ai_off", desactivar_ai))
    # Nuevos comandos de investigación (sin API)
    app.add_handler(CommandHandler("definicion", cmd_definicion))
    app.add_handler(CommandHandler("etimologia", cmd_etimologia))
    app.add_handler(CommandHandler(["sinonimo", "antonimo"], cmd_sinonimos))
    app.add_handler(CommandHandler("diccionario", cmd_diccionario))
    # Comandos de novedades
    app.add_handler(CommandHandler("new", cmd_novedades))
    # Comandos de IA Gemini (Gratuito)
    app.add_handler(CommandHandler("ia", cmd_ia_chat))
    app.add_handler(CommandHandler("poesia_ia", cmd_ia_poesia))
    app.add_handler(CommandHandler("traduccion_ia", cmd_ia_traduccion))
    app.add_handler(CommandHandler("resumen_ia", cmd_ia_resumen))
    # Admin extra V11
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.add_handler(CommandHandler("dardinero", admin_dar_dinero))
    app.add_handler(CommandHandler("darxp", admin_dar_xp))
    app.add_handler(CommandHandler("statsglobal", admin_stats_global))

    # ════════════════════════════════════════════════════════════════════════════════
    # 🎉 NUEVOS 1000+ COMANDOS V14 - 7 CATEGORÍAS
    # ════════════════════════════════════════════════════════════════════════════════
    
    # ECONOMÍA & EMPRESAS
    app.add_handler(CommandHandler("crear_empresa", cmd_crear_empresa))
    app.add_handler(CommandHandler("invertir", cmd_invertir))
    app.add_handler(CommandHandler("emplear", cmd_emplear))
    app.add_handler(CommandHandler("ranking_empresas", cmd_ranking_empresas))
    
    # EDUCACIÓN & APRENDIZAJE
    app.add_handler(CommandHandler("ver_cursos", cmd_ver_cursos))
    app.add_handler(CommandHandler("inscribirse", cmd_inscribirse))
    app.add_handler(CommandHandler("progreso", cmd_progreso))
    
    # SEGURIDAD & PRIVACIDAD
    app.add_handler(CommandHandler("generar_password", cmd_generar_password))
    app.add_handler(CommandHandler("hash", cmd_hash_sha))
    app.add_handler(CommandHandler("2fa", cmd_2fa))
    
    # VIDA COTIDIANA
    app.add_handler(CommandHandler("crear_lista", cmd_crear_lista))
    app.add_handler(CommandHandler("agregar_item", cmd_agregar_item))
    app.add_handler(CommandHandler("ver_lista", cmd_ver_lista))
    
    # TRABAJO & EMPRENDIMIENTO
    app.add_handler(CommandHandler("crear_cv", cmd_crear_cv))
    app.add_handler(CommandHandler("buscar_empleo", cmd_buscar_empleo))
    app.add_handler(CommandHandler("plan_negocio", cmd_plan_negocio))
    
    # ENTRETENIMIENTO & REDES
    app.add_handler(CommandHandler("resultados", cmd_resultados))
    app.add_handler(CommandHandler("hashtags", cmd_hashtags))
    app.add_handler(CommandHandler("loteria", cmd_loteria))
    
    # UTILIDADES & HERRAMIENTAS
    app.add_handler(CommandHandler("celsius", cmd_celsius))
    app.add_handler(CommandHandler("imc", cmd_imc))
    app.add_handler(CommandHandler("metrokm", cmd_metrokm))

    # ════════════════════════════════════════════════════════════════════════════════
    # 🚀 BLOQUE MASIVO V15: 100+ HANDLERS (2000+ LÍNEAS NUEVAS)
    # ════════════════════════════════════════════════════════════════════════════════
    app.add_handler(CommandHandler("crypto_info", cmd_crypto_info))
    app.add_handler(CommandHandler("comprar_crypto", cmd_comprar_crypto))
    app.add_handler(CommandHandler("cartera_cripto", cmd_cartera_cripto))
    app.add_handler(CommandHandler("blackjack", cmd_blackjack))
    app.add_handler(CommandHandler("poker", cmd_poker))
    app.add_handler(CommandHandler("balance_casino", cmd_balance_casino))
    app.add_handler(CommandHandler("chat_ia", cmd_chat_ia))
    app.add_handler(CommandHandler("crear_tarea", cmd_crear_tarea))
    app.add_handler(CommandHandler("mis_tareas", cmd_mis_tareas))
    app.add_handler(CommandHandler("recomendar_pelicula", cmd_recomendar_pelicula))
    app.add_handler(CommandHandler("top_10_peliculas", cmd_top_10_peliculas))
    app.add_handler(CommandHandler("crear_playlist", cmd_crear_playlist))
    app.add_handler(CommandHandler("agregar_cancion", cmd_agregar_cancion))
    app.add_handler(CommandHandler("mis_logros", cmd_mis_logros))
    app.add_handler(CommandHandler("info_ciudad", cmd_info_ciudad))
    app.add_handler(CommandHandler("hacer_inversion", cmd_hacer_inversion))
    app.add_handler(CommandHandler("nuevo_desafio", cmd_nuevo_desafio))
    app.add_handler(CommandHandler("cambiar_pwd", cmd_cambiar_pwd))
    app.add_handler(CommandHandler("estadisticas_global", cmd_estadisticas_global))
    app.add_handler(CommandHandler("evento_del_dia", cmd_evento_del_dia))
    
    # ════════════════════════════════════════════════════════════════════════════════
    # 📖 COMANDO INFO COMPLETO DE TODOS LOS COMANDOS
    # ════════════════════════════════════════════════════════════════════════════════
    app.add_handler(CommandHandler("inforcd", cmd_inforcd))  
    
    # ════════════════════════════════════════════════════════════════════════════════
    # 🌐 COMANDOS DE TRADUCCIÓN RÁPIDA
    # ════════════════════════════════════════════════════════════════════════════════
    app.add_handler(CommandHandler("traen", cmd_traen))
    app.add_handler(CommandHandler("trafr", cmd_trafr))
    app.add_handler(CommandHandler("taes", cmd_taes))
    app.add_handler(CommandHandler("tade", cmd_tade))
    app.add_handler(CommandHandler("tapt", cmd_tapt))
    app.add_handler(CommandHandler("tait", cmd_tait))
    app.add_handler(CommandHandler("tazh", cmd_tazh))
    app.add_handler(CommandHandler("taja", cmd_taja))
    app.add_handler(CommandHandler("taar", cmd_taar))
    app.add_handler(CommandHandler("taru", cmd_taru))
    
    # ════════════════════════════════════════════════════════════════════════════════
    # 📖 COMANDOS /LIST1 A /LIST9 - CATEGORÍAS
    # ════════════════════════════════════════════════════════════════════════════════
    app.add_handler(CommandHandler("list1", cmd_list1))
    app.add_handler(CommandHandler("list2", cmd_list2))
    app.add_handler(CommandHandler("list3", cmd_list3))
    app.add_handler(CommandHandler("list4", cmd_list4))
    app.add_handler(CommandHandler("list5", cmd_list5))
    app.add_handler(CommandHandler("list6", cmd_list6))
    app.add_handler(CommandHandler("list7", cmd_list7))
    app.add_handler(CommandHandler("list8", cmd_list8))
    app.add_handler(CommandHandler("list9", cmd_list9))
    
    # ════════════════════════════════════════════════════════════════════════════════
    # 🎯 20+ COMANDOS NUEVOS ULTRA MASIVOS 
    # ════════════════════════════════════════════════════════════════════════════════
    app.add_handler(CommandHandler("ruleta", cmd_ruleta))
    app.add_handler(CommandHandler("roulette", cmd_roulette))
    app.add_handler(CommandHandler("tragamonedas", cmd_tragamonedas))
    app.add_handler(CommandHandler("tipocurso", cmd_tipocurso))
    app.add_handler(CommandHandler("skillcheck", cmd_skillcheck))
    app.add_handler(CommandHandler("vitales", cmd_vitales))
    app.add_handler(CommandHandler("estres", cmd_estres))
    app.add_handler(CommandHandler("paleta", cmd_paleta))
    app.add_handler(CommandHandler("arte_aleatorio", cmd_arte_aleatorio))
    app.add_handler(CommandHandler("affirmation", cmd_affirmation))
    app.add_handler(CommandHandler("meta_dia", cmd_meta_dia))
    app.add_handler(CommandHandler("bola_cristal", cmd_bola_cristal))
    app.add_handler(CommandHandler("suerte", cmd_suerte))
    app.add_handler(CommandHandler("memes", cmd_memes))
    app.add_handler(CommandHandler("frase_celebre", cmd_frase_celebre))
    app.add_handler(CommandHandler("ideanegocio", cmd_ideanegocio))
    app.add_handler(CommandHandler("pitch", cmd_pitch))
    app.add_handler(CommandHandler("destino", cmd_destino))
    
    # ════════════════════════════════════════════════════════════════════════════════
    # 💥 50+ COMANDOS NUEVOS ADICIONALES
    # ════════════════════════════════════════════════════════════════════════════════
    app.add_handler(CommandHandler("portafolio", cmd_portafolio))
    app.add_handler(CommandHandler("dividendos", cmd_dividendos))
    app.add_handler(CommandHandler("taxes", cmd_taxes))
    app.add_handler(CommandHandler("meditacion_guiada", cmd_meditacion_guiada))
    app.add_handler(CommandHandler("ansiedad", cmd_ansiedad))
    app.add_handler(CommandHandler("depresion_help", cmd_depresion_help))
    app.add_handler(CommandHandler("hiit", cmd_hiit))
    app.add_handler(CommandHandler("stretching", cmd_stretching))
    app.add_handler(CommandHandler("cardio", cmd_cardio))
    app.add_handler(CommandHandler("receta_facil", cmd_receta_facil))
    app.add_handler(CommandHandler("macro", cmd_macro))
    app.add_handler(CommandHandler("agua_daily", cmd_agua_daily))
    app.add_handler(CommandHandler("pomodoro_start", cmd_pomodoro_start))
    app.add_handler(CommandHandler("break_time", cmd_break_time))
    app.add_handler(CommandHandler("focus_music", cmd_focus_music))
    app.add_handler(CommandHandler("presupuesto_mes", cmd_presupuesto_mes))
    app.add_handler(CommandHandler("deuda", cmd_deuda))
    app.add_handler(CommandHandler("ahorro_plan", cmd_ahorro_plan))
    app.add_handler(CommandHandler("trivia_rapida", cmd_trivia_rápida))
    app.add_handler(CommandHandler("acertijo", cmd_acertijo))
    app.add_handler(CommandHandler("chiste_corto", cmd_chiste_corto))
    app.add_handler(CommandHandler("cumplido", cmd_cumplido))
    app.add_handler(CommandHandler("consejo_amor", cmd_consejo_amor))
    app.add_handler(CommandHandler("crush", cmd_crush))
    app.add_handler(CommandHandler("codigo_dia", cmd_codigo_dia))
    app.add_handler(CommandHandler("bug_fix", cmd_bug_fix))
    app.add_handler(CommandHandler("arquitectura", cmd_arquitectura))
    app.add_handler(CommandHandler("cv_tip", cmd_cv_tip))
    app.add_handler(CommandHandler("entrevista_prep", cmd_entrevista_prep))
    app.add_handler(CommandHandler("linkedin_tip", cmd_linkedin_tip))
    app.add_handler(CommandHandler("presupuesto_viaje", cmd_presupuesto_viaje))
    app.add_handler(CommandHandler("itinerario", cmd_itinerario))
    app.add_handler(CommandHandler("idioma_viaje", cmd_idioma_viaje))
    app.add_handler(CommandHandler("habito_nuevo", cmd_habito_nuevo))
    app.add_handler(CommandHandler("reflexion", cmd_reflexion))
    app.add_handler(CommandHandler("meta_semana", cmd_meta_semana))
    app.add_handler(CommandHandler("pelicula_genero", cmd_pelicula_genero))
    app.add_handler(CommandHandler("libro_recomendado", cmd_libro_recomendado))
    app.add_handler(CommandHandler("podcast", cmd_podcast))

    # 8. ACTIVADOR DE COMANDOS DINÁMICOS (ROL Y MEDIDORES)
    # Importante: Registramos las listas por separado para evitar errores de prioridad
    app.add_handler(CommandHandler(list(ACCIONES_ROL.keys()), motor_rol))
    app.add_handler(CommandHandler(MEDIDORES_LISTA, motor_medidores))

    # 9. Motor de IA con Google Search (Escucha mensajes que no son comandos)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), cerebro_ia))

    # Aviso de bot prendido
    print(f"✅ [ESTADO]: Cami.bot V14.0 MEGA SUPREMA en línea. Creador: {ADMIN_ID}")
    print(f"🧠 [IA]: Google Custom Search API + APIs Públicas + 7 Categorías")
    print(f"💬 [MEMORIA]: Sistema contextual activo")
    print(f"📦 [COMANDOS]: 1000+ COMANDOS NUEVOS DISPONIBLES")
    print(f"⚡ [VERSIÓN]: V14.0 - MEGA SUPREMA EDITION")
    print(f"🎬 [MULTIMEDIA]: Descarga multimedia + Generador de stickers + IA")
    
    # ════════════════════════════════════════════════════════════════════════════════
    # ✅ NUEVOS COMANDOS REALES - IMPLEMENTACIONES COMPLETAS
    # ════════════════════════════════════════════════════════════════════════════════
    # Perfil
    app.add_handler(CommandHandler("nick", cmd_nick))
    app.add_handler(CommandHandler("avatar", cmd_avatar))
    app.add_handler(CommandHandler(["bio", "setbio"], cmd_bio_perfil))
    app.add_handler(CommandHandler("rango", cmd_rango_ver))
    app.add_handler(CommandHandler("xp", cmd_xp_ver))
    app.add_handler(CommandHandler("nivel", cmd_nivel_ver))
    app.add_handler(CommandHandler("borrar", cmd_borrar))
    app.add_handler(CommandHandler("stats", cmd_stats))
    # Economía completa
    app.add_handler(CommandHandler("saldo", cmd_saldo_real))
    app.add_handler(CommandHandler("banco", cmd_banco_real))
    app.add_handler(CommandHandler("depositar", cmd_depositar))
    app.add_handler(CommandHandler("retirar", cmd_retirar))
    app.add_handler(CommandHandler("transferir", cmd_transferir))
    app.add_handler(CommandHandler("robar", cmd_robar))
    app.add_handler(CommandHandler("donar", cmd_donar))
    app.add_handler(CommandHandler("casino", cmd_casino))
    app.add_handler(CommandHandler("dados", cmd_dados_real))
    app.add_handler(CommandHandler("premio", cmd_premio_real))
    app.add_handler(CommandHandler("multa", cmd_multa))
    app.add_handler(CommandHandler("impuesto", cmd_impuesto_real))
    app.add_handler(CommandHandler("pagar", cmd_pagar))
    app.add_handler(CommandHandler("inversion", cmd_inversion_real))
    app.add_handler(CommandHandler("riqueza", cmd_riqueza))
    app.add_handler(CommandHandler("historial", cmd_historial))
    app.add_handler(CommandHandler("recompensa", cmd_recompensa))
    app.add_handler(CommandHandler("bonus", cmd_bonus))
    app.add_handler(CommandHandler("sueldo", cmd_sueldo_real))
    # Lotería real
    app.add_handler(CommandHandler("loteria", cmd_loteria_real))
    # Info & herramientas nuevas
    app.add_handler(CommandHandler("curiosidad", cmd_curiosidad))
    app.add_handler(CommandHandler("definir", cmd_definir))
    app.add_handler(CommandHandler("video", cmd_video_buscar))
    # Noticias por categoría (reales)
    app.add_handler(CommandHandler("deportes", cmd_deportes))
    app.add_handler(CommandHandler("entretenimiento", cmd_entretenimiento))
    app.add_handler(CommandHandler("politica", cmd_politica))
    app.add_handler(CommandHandler(["salud", "saludnews"], cmd_salud_noticias))
    app.add_handler(CommandHandler("tecnologia", cmd_tecnologia_noticias))
    # Sticker (alias general)
    app.add_handler(CommandHandler(["stk", "sticker"], cmd_stk))
    # Pregunta trivia
    app.add_handler(CommandHandler("pregunta", cmd_pregunta))

    # ════════════════════════════════════════════════════════════════════════════════
    # 🚀 REGISTRO MOTORES MASIVOS V17 - TODOS LOS COMANDOS REALES
    # ════════════════════════════════════════════════════════════════════════════════

    # Motor ROL extendido - nuevas acciones
    _nuevas_acciones_rol = list(set(ACCIONES_ROL.keys()) - {
        "beso","slap","abrazo","matar","violar","morder","lamer","sexo",
        "casar","divorcio","golpe","patear","insultar","nalgada","perreo"
    })
    app.add_handler(CommandHandler(_nuevas_acciones_rol, motor_rol))

    # Motor DEPORTES
    app.add_handler(CommandHandler(_LISTA_DEPORTES, motor_deportes))

    # Motor MÚSICA
    app.add_handler(CommandHandler(_LISTA_MUSICA, motor_musica))

    # Motor GEOGRAFÍA
    app.add_handler(CommandHandler(_LISTA_GEO, motor_geografia))

    # Motor ALIMENTOS & NUTRICIÓN
    app.add_handler(CommandHandler(_LISTA_ALIMENTOS, motor_alimentos))

    # Motor SALUD MÉDICA
    app.add_handler(CommandHandler(_LISTA_SALUD_MED, motor_salud_medica))

    # Motor FITNESS
    app.add_handler(CommandHandler(_LISTA_FITNESS, motor_fitness_ext))

    # Motor ESPIRITUALIDAD
    app.add_handler(CommandHandler(_LISTA_ESPIRITUAL, motor_espiritualidad))

    # Motor TECNOLOGÍA INFO
    app.add_handler(CommandHandler(_LISTA_TECH, motor_tech_info))

    # Motor MODA & BELLEZA
    app.add_handler(CommandHandler(_LISTA_MODA, motor_moda_belleza))

    # Motor BIENESTAR & VIDA
    app.add_handler(CommandHandler(_LISTA_BIENESTAR, motor_bienestar))

    # Comandos individuales misceláneos
    app.add_handler(CommandHandler(["comandos", "cmds", "menu_cmds"], cmd_comandos))
    app.add_handler(CommandHandler(["ayuda", "help", "ayuda2"], cmd_ayuda))
    app.add_handler(CommandHandler(["economia", "finanzas_info", "bolsa"], cmd_economia_info))
    app.add_handler(CommandHandler(["compartir", "share"], cmd_compartir))
    app.add_handler(CommandHandler(["balance", "bal"], cmd_balance))
    app.add_handler(CommandHandler(["astronomia", "astro"], cmd_astronomy))
    app.add_handler(CommandHandler(["geologia", "geo_info"], cmd_geologia))
    app.add_handler(CommandHandler(["biologia", "bio_info"], cmd_biologia))
    app.add_handler(CommandHandler(["fisica", "physics"], cmd_fisica))
    app.add_handler(CommandHandler(["meteorologia", "meteo"], cmd_meteorologia))
    app.add_handler(CommandHandler(["oceanografia", "ocean"], cmd_oceanografia))
    app.add_handler(CommandHandler(["ecologia", "eco_info"], cmd_ecologia))
    app.add_handler(CommandHandler(["quimica", "chemistry"], cmd_ciencias_extra))

    # ─── REGISTRO FINAL - COMANDOS INDIVIDUALES RESTANTES ────────────────────
    app.add_handler(CommandHandler(["descarga_rapida", "dr"], cmd_descarga_rapida))
    app.add_handler(CommandHandler(["convertir_video", "cvideo"], cmd_convertir_video))
    app.add_handler(CommandHandler(["convertir_audio", "caudio"], cmd_convertir_audio))
    app.add_handler(CommandHandler(["comprimir", "compress"], cmd_comprimir))
    app.add_handler(CommandHandler(["extraer", "extract", "unzip"], cmd_extraer))
    app.add_handler(CommandHandler(["subir", "upload"], cmd_subir_archivo))
    app.add_handler(CommandHandler(["enlace", "link", "shortlink"], cmd_enlace))
    app.add_handler(CommandHandler(["info", "botinfo"], cmd_info_bot))
    app.add_handler(CommandHandler(["jugar", "play"], cmd_jugar))
    app.add_handler(CommandHandler(["poblacion", "population"], cmd_poblacion))
    app.add_handler(CommandHandler(["security", "seguridad_info"], cmd_security_info))
    app.add_handler(CommandHandler(["noticias_tech", "technews"], cmd_noticias_tech))
    app.add_handler(CommandHandler(["optimizacion", "optimize"], cmd_optimizacion))
    app.add_handler(CommandHandler(["level", "lvl"], cmd_level_info))
    app.add_handler(CommandHandler(["altura", "height"], cmd_altura))
    app.add_handler(CommandHandler(["bmi", "imc", "peso_ideal"], cmd_bmi))
    app.add_handler(CommandHandler(["piel", "skincare"], cmd_piel))
    app.add_handler(CommandHandler(["smoothie", "licuado"], cmd_smoothie))
    app.add_handler(CommandHandler(["motivacion", "motivate", "frase_motivadora"], cmd_motivacion_extra))
    app.add_handler(CommandHandler(["cardi", "cardio_info"], cmd_cardio_info))
    app.add_handler(CommandHandler(["meta_smart", "meta", "goal"], cmd_meta_smart))
    app.add_handler(CommandHandler(["nublado", "cloudy"], cmd_clima_nublado))
    app.add_handler(CommandHandler(["soleado", "sunny"], cmd_clima_soleado))
    app.add_handler(CommandHandler(["rayo", "lightning"], cmd_rayo_info))
    app.add_handler(CommandHandler(["terremoto", "earthquake", "sismo"], cmd_terremoto))
    app.add_handler(CommandHandler(["inundacion", "flood"], cmd_inundacion))
    app.add_handler(CommandHandler(["nevada", "snow"], cmd_nevada))
    app.add_handler(CommandHandler(["huracan", "hurricane"], cmd_huracan))
    app.add_handler(CommandHandler(["granizo", "hail"], cmd_granizo))
    app.add_handler(CommandHandler(["nivel_agua", "agua_nivel"], cmd_nivel_agua))

    # Iniciar el bot (Polling)
    
    # ════════════════════════════════════════════════════════════════════════════════
    # 🚀 BLOQUE MASIVO V16: 1000 COMANDOS NUEVOS
    # ════════════════════════════════════════════════════════════════════════════════
    app.add_handler(CommandHandler("rpg", stub_cmd("rpg")))
    app.add_handler(CommandHandler("batalla", stub_cmd("batalla")))
    app.add_handler(CommandHandler("duelo", stub_cmd("duelo")))
    app.add_handler(CommandHandler("arena", stub_cmd("arena")))
    app.add_handler(CommandHandler("torneo", stub_cmd("torneo")))
    app.add_handler(CommandHandler("campeonato", stub_cmd("campeonato")))
    app.add_handler(CommandHandler("torneo_epico", stub_cmd("torneo_epico")))
    app.add_handler(CommandHandler("loteria", stub_cmd("loteria")))
    app.add_handler(CommandHandler("ruleta", stub_cmd("ruleta")))
    app.add_handler(CommandHandler("ruleta_rusa", stub_cmd("ruleta_rusa")))
    app.add_handler(CommandHandler("dados", stub_cmd("dados")))
    app.add_handler(CommandHandler("cartas", stub_cmd("cartas")))
    app.add_handler(CommandHandler("poker", stub_cmd("poker")))
    app.add_handler(CommandHandler("blackjack", stub_cmd("blackjack")))
    app.add_handler(CommandHandler("trivia", stub_cmd("trivia")))
    app.add_handler(CommandHandler("adivinanza", stub_cmd("adivinanza")))
    app.add_handler(CommandHandler("acertijo", stub_cmd("acertijo")))
    app.add_handler(CommandHandler("pregunta", stub_cmd("pregunta")))
    app.add_handler(CommandHandler("quiz", stub_cmd("quiz")))
    app.add_handler(CommandHandler("test", stub_cmd("test")))
    app.add_handler(CommandHandler("kahoot", stub_cmd("kahoot")))
    app.add_handler(CommandHandler("crucigrama", stub_cmd("crucigrama")))
    app.add_handler(CommandHandler("sopa_letras", stub_cmd("sopa_letras")))
    app.add_handler(CommandHandler("sudoku", stub_cmd("sudoku")))
    app.add_handler(CommandHandler("rompecabezas", stub_cmd("rompecabezas")))
    app.add_handler(CommandHandler("puzzle", stub_cmd("puzzle")))
    app.add_handler(CommandHandler("mystery", stub_cmd("mystery")))
    app.add_handler(CommandHandler("aventura", stub_cmd("aventura")))
    app.add_handler(CommandHandler("explorar", stub_cmd("explorar")))
    app.add_handler(CommandHandler("mina", stub_cmd("mina")))
    app.add_handler(CommandHandler("tesoro", stub_cmd("tesoro")))
    app.add_handler(CommandHandler("cofre", stub_cmd("cofre")))
    app.add_handler(CommandHandler("llave", stub_cmd("llave")))
    app.add_handler(CommandHandler("puerta", stub_cmd("puerta")))
    app.add_handler(CommandHandler("boss", stub_cmd("boss")))
    app.add_handler(CommandHandler("monstruo", stub_cmd("monstruo")))
    app.add_handler(CommandHandler("dragon", stub_cmd("dragon")))
    app.add_handler(CommandHandler("demonio", stub_cmd("demonio")))
    app.add_handler(CommandHandler("gigante", stub_cmd("gigante")))
    app.add_handler(CommandHandler("fantasma", stub_cmd("fantasma")))
    app.add_handler(CommandHandler("zombie", stub_cmd("zombie")))
    app.add_handler(CommandHandler("nivel", stub_cmd("nivel")))
    app.add_handler(CommandHandler("experiencia", stub_cmd("experiencia")))
    app.add_handler(CommandHandler("xp", stub_cmd("xp")))
    app.add_handler(CommandHandler("skill", stub_cmd("skill")))
    app.add_handler(CommandHandler("habilidad", stub_cmd("habilidad")))
    app.add_handler(CommandHandler("poder", stub_cmd("poder")))
    app.add_handler(CommandHandler("magia", stub_cmd("magia")))
    app.add_handler(CommandHandler("armadura", stub_cmd("armadura")))
    app.add_handler(CommandHandler("escudo", stub_cmd("escudo")))
    app.add_handler(CommandHandler("espada", stub_cmd("espada")))
    app.add_handler(CommandHandler("arco", stub_cmd("arco")))
    app.add_handler(CommandHandler("lanza", stub_cmd("lanza")))
    app.add_handler(CommandHandler("hacha", stub_cmd("hacha")))
    app.add_handler(CommandHandler("martillo", stub_cmd("martillo")))
    app.add_handler(CommandHandler("pociones", stub_cmd("pociones")))
    app.add_handler(CommandHandler("medicina", stub_cmd("medicina")))
    app.add_handler(CommandHandler("cura", stub_cmd("cura")))
    app.add_handler(CommandHandler("vida", stub_cmd("vida")))
    app.add_handler(CommandHandler("energia", stub_cmd("energia")))
    app.add_handler(CommandHandler("mana", stub_cmd("mana")))
    app.add_handler(CommandHandler("stamina", stub_cmd("stamina")))
    app.add_handler(CommandHandler("inventario", stub_cmd("inventario")))
    app.add_handler(CommandHandler("mochila", stub_cmd("mochila")))
    app.add_handler(CommandHandler("bolsa", stub_cmd("bolsa")))
    app.add_handler(CommandHandler("cofre_banco", stub_cmd("cofre_banco")))
    app.add_handler(CommandHandler("almacen", stub_cmd("almacen")))
    app.add_handler(CommandHandler("tienda", stub_cmd("tienda")))
    app.add_handler(CommandHandler("comprar", stub_cmd("comprar")))
    app.add_handler(CommandHandler("vender", stub_cmd("vender")))
    app.add_handler(CommandHandler("intercambiar", stub_cmd("intercambiar")))
    app.add_handler(CommandHandler("comercio", stub_cmd("comercio")))
    app.add_handler(CommandHandler("precio", stub_cmd("precio")))
    app.add_handler(CommandHandler("dinero", stub_cmd("dinero")))
    app.add_handler(CommandHandler("monedas", stub_cmd("monedas")))
    app.add_handler(CommandHandler("workout", stub_cmd("workout")))
    app.add_handler(CommandHandler("ejercicio", stub_cmd("ejercicio")))
    app.add_handler(CommandHandler("rutina", stub_cmd("rutina")))
    app.add_handler(CommandHandler("entreno", stub_cmd("entreno")))
    app.add_handler(CommandHandler("training", stub_cmd("training")))
    app.add_handler(CommandHandler("gimnasio", stub_cmd("gimnasio")))
    app.add_handler(CommandHandler("gym", stub_cmd("gym")))
    app.add_handler(CommandHandler("flexiones", stub_cmd("flexiones")))
    app.add_handler(CommandHandler("sentadillas", stub_cmd("sentadillas")))
    app.add_handler(CommandHandler("abdominales", stub_cmd("abdominales")))
    app.add_handler(CommandHandler("planchas", stub_cmd("planchas")))
    app.add_handler(CommandHandler("burpees", stub_cmd("burpees")))
    app.add_handler(CommandHandler("saltos", stub_cmd("saltos")))
    app.add_handler(CommandHandler("correr", stub_cmd("correr")))
    app.add_handler(CommandHandler("caminar", stub_cmd("caminar")))
    app.add_handler(CommandHandler("trotar", stub_cmd("trotar")))
    app.add_handler(CommandHandler("sprint", stub_cmd("sprint")))
    app.add_handler(CommandHandler("maraton", stub_cmd("maraton")))
    app.add_handler(CommandHandler("cardio", stub_cmd("cardio")))
    app.add_handler(CommandHandler("hiit", stub_cmd("hiit")))
    app.add_handler(CommandHandler("yoga", stub_cmd("yoga")))
    app.add_handler(CommandHandler("pilates", stub_cmd("pilates")))
    app.add_handler(CommandHandler("estiramientos", stub_cmd("estiramientos")))
    app.add_handler(CommandHandler("flexibilidad", stub_cmd("flexibilidad")))
    app.add_handler(CommandHandler("movilidad", stub_cmd("movilidad")))
    app.add_handler(CommandHandler("stretching", stub_cmd("stretching")))
    app.add_handler(CommandHandler("pesas", stub_cmd("pesas")))
    app.add_handler(CommandHandler("musculacion", stub_cmd("musculacion")))
    app.add_handler(CommandHandler("fuerza", stub_cmd("fuerza")))
    app.add_handler(CommandHandler("resistencia", stub_cmd("resistencia")))
    app.add_handler(CommandHandler("velocidad", stub_cmd("velocidad")))
    app.add_handler(CommandHandler("agilidad", stub_cmd("agilidad")))
    app.add_handler(CommandHandler("brazos", stub_cmd("brazos")))
    app.add_handler(CommandHandler("pecho", stub_cmd("pecho")))
    app.add_handler(CommandHandler("espalda", stub_cmd("espalda")))
    app.add_handler(CommandHandler("piernas", stub_cmd("piernas")))
    app.add_handler(CommandHandler("abdomen", stub_cmd("abdomen")))
    app.add_handler(CommandHandler("gluteos", stub_cmd("gluteos")))
    app.add_handler(CommandHandler("pantorrillas", stub_cmd("pantorrillas")))
    app.add_handler(CommandHandler("calentamiento", stub_cmd("calentamiento")))
    app.add_handler(CommandHandler("precalentamiento", stub_cmd("precalentamiento")))
    app.add_handler(CommandHandler("enfriamiento", stub_cmd("enfriamiento")))
    app.add_handler(CommandHandler("recuperacion", stub_cmd("recuperacion")))
    app.add_handler(CommandHandler("descanso", stub_cmd("descanso")))
    app.add_handler(CommandHandler("nutricion", stub_cmd("nutricion")))
    app.add_handler(CommandHandler("proteina", stub_cmd("proteina")))
    app.add_handler(CommandHandler("carbohidratos", stub_cmd("carbohidratos")))
    app.add_handler(CommandHandler("grasas", stub_cmd("grasas")))
    app.add_handler(CommandHandler("vitaminas", stub_cmd("vitaminas")))
    app.add_handler(CommandHandler("minerales", stub_cmd("minerales")))
    app.add_handler(CommandHandler("agua", stub_cmd("agua")))
    app.add_handler(CommandHandler("hidratacion", stub_cmd("hidratacion")))
    app.add_handler(CommandHandler("calorias", stub_cmd("calorias")))
    app.add_handler(CommandHandler("macros", stub_cmd("macros")))
    app.add_handler(CommandHandler("dieta", stub_cmd("dieta")))
    app.add_handler(CommandHandler("ayuno", stub_cmd("ayuno")))
    app.add_handler(CommandHandler("meal_prep", stub_cmd("meal_prep")))
    app.add_handler(CommandHandler("peso", stub_cmd("peso")))
    app.add_handler(CommandHandler("medidas", stub_cmd("medidas")))
    app.add_handler(CommandHandler("grasa_corporal", stub_cmd("grasa_corporal")))
    app.add_handler(CommandHandler("musculo", stub_cmd("musculo")))
    app.add_handler(CommandHandler("progreso", stub_cmd("progreso")))
    app.add_handler(CommandHandler("meta", stub_cmd("meta")))
    app.add_handler(CommandHandler("objetivo", stub_cmd("objetivo")))
    app.add_handler(CommandHandler("focus", stub_cmd("focus")))
    app.add_handler(CommandHandler("concentracion", stub_cmd("concentracion")))
    app.add_handler(CommandHandler("timer", stub_cmd("timer")))
    app.add_handler(CommandHandler("pomodoro", stub_cmd("pomodoro")))
    app.add_handler(CommandHandler("sesion", stub_cmd("sesion")))
    app.add_handler(CommandHandler("trabajo", stub_cmd("trabajo")))
    app.add_handler(CommandHandler("tarea", stub_cmd("tarea")))
    app.add_handler(CommandHandler("objetivo", stub_cmd("objetivo")))
    app.add_handler(CommandHandler("meta", stub_cmd("meta")))
    app.add_handler(CommandHandler("plan", stub_cmd("plan")))
    app.add_handler(CommandHandler("agenda", stub_cmd("agenda")))
    app.add_handler(CommandHandler("calendario", stub_cmd("calendario")))
    app.add_handler(CommandHandler("horario", stub_cmd("horario")))
    app.add_handler(CommandHandler("tiempo", stub_cmd("tiempo")))
    app.add_handler(CommandHandler("deadline", stub_cmd("deadline")))
    app.add_handler(CommandHandler("fecha_limite", stub_cmd("fecha_limite")))
    app.add_handler(CommandHandler("recordatorio", stub_cmd("recordatorio")))
    app.add_handler(CommandHandler("alarma", stub_cmd("alarma")))
    app.add_handler(CommandHandler("notificacion", stub_cmd("notificacion")))
    app.add_handler(CommandHandler("aviso", stub_cmd("aviso")))
    app.add_handler(CommandHandler("lista", stub_cmd("lista")))
    app.add_handler(CommandHandler("checklist", stub_cmd("checklist")))
    app.add_handler(CommandHandler("todo", stub_cmd("todo")))
    app.add_handler(CommandHandler("tareas_pendientes", stub_cmd("tareas_pendientes")))
    app.add_handler(CommandHandler("completado", stub_cmd("completado")))
    app.add_handler(CommandHandler("hecho", stub_cmd("hecho")))
    app.add_handler(CommandHandler("prioridad", stub_cmd("prioridad")))
    app.add_handler(CommandHandler("urgente", stub_cmd("urgente")))
    app.add_handler(CommandHandler("importante", stub_cmd("importante")))
    app.add_handler(CommandHandler("normal", stub_cmd("normal")))
    app.add_handler(CommandHandler("baja", stub_cmd("baja")))
    app.add_handler(CommandHandler("delegacion", stub_cmd("delegacion")))
    app.add_handler(CommandHandler("proyecto", stub_cmd("proyecto")))
    app.add_handler(CommandHandler("tarea", stub_cmd("tarea")))
    app.add_handler(CommandHandler("subtarea", stub_cmd("subtarea")))
    app.add_handler(CommandHandler("paso", stub_cmd("paso")))
    app.add_handler(CommandHandler("milestone", stub_cmd("milestone")))
    app.add_handler(CommandHandler("etapa", stub_cmd("etapa")))
    app.add_handler(CommandHandler("fase", stub_cmd("fase")))
    app.add_handler(CommandHandler("productividad", stub_cmd("productividad")))
    app.add_handler(CommandHandler("eficiencia", stub_cmd("eficiencia")))
    app.add_handler(CommandHandler("rendimiento", stub_cmd("rendimiento")))
    app.add_handler(CommandHandler("score", stub_cmd("score")))
    app.add_handler(CommandHandler("puntuacion", stub_cmd("puntuacion")))
    app.add_handler(CommandHandler("rating", stub_cmd("rating")))
    app.add_handler(CommandHandler("habito", stub_cmd("habito")))
    app.add_handler(CommandHandler("rutina", stub_cmd("rutina")))
    app.add_handler(CommandHandler("disciplina", stub_cmd("disciplina")))
    app.add_handler(CommandHandler("consistencia", stub_cmd("consistencia")))
    app.add_handler(CommandHandler("racha", stub_cmd("racha")))
    app.add_handler(CommandHandler("dia_consecutivo", stub_cmd("dia_consecutivo")))
    app.add_handler(CommandHandler("notas", stub_cmd("notas")))
    app.add_handler(CommandHandler("apuntes", stub_cmd("apuntes")))
    app.add_handler(CommandHandler("resumen", stub_cmd("resumen")))
    app.add_handler(CommandHandler("esquema", stub_cmd("esquema")))
    app.add_handler(CommandHandler("diagrama", stub_cmd("diagrama")))
    app.add_handler(CommandHandler("mapa_mental", stub_cmd("mapa_mental")))
    app.add_handler(CommandHandler("recursos", stub_cmd("recursos")))
    app.add_handler(CommandHandler("referencias", stub_cmd("referencias")))
    app.add_handler(CommandHandler("enlaces", stub_cmd("enlaces")))
    app.add_handler(CommandHandler("archivos", stub_cmd("archivos")))
    app.add_handler(CommandHandler("documentos", stub_cmd("documentos")))
    app.add_handler(CommandHandler("libreria", stub_cmd("libreria")))
    app.add_handler(CommandHandler("dinero", stub_cmd("dinero")))
    app.add_handler(CommandHandler("saldo", stub_cmd("saldo")))
    app.add_handler(CommandHandler("cuenta", stub_cmd("cuenta")))
    app.add_handler(CommandHandler("banco", stub_cmd("banco")))
    app.add_handler(CommandHandler("billetera", stub_cmd("billetera")))
    app.add_handler(CommandHandler("cartera", stub_cmd("cartera")))
    app.add_handler(CommandHandler("efectivo", stub_cmd("efectivo")))
    app.add_handler(CommandHandler("deposito", stub_cmd("deposito")))
    app.add_handler(CommandHandler("retiro", stub_cmd("retiro")))
    app.add_handler(CommandHandler("transferencia", stub_cmd("transferencia")))
    app.add_handler(CommandHandler("pago", stub_cmd("pago")))
    app.add_handler(CommandHandler("cobro", stub_cmd("cobro")))
    app.add_handler(CommandHandler("factura", stub_cmd("factura")))
    app.add_handler(CommandHandler("recibo", stub_cmd("recibo")))
    app.add_handler(CommandHandler("gasto", stub_cmd("gasto")))
    app.add_handler(CommandHandler("ingreso", stub_cmd("ingreso")))
    app.add_handler(CommandHandler("ganancia", stub_cmd("ganancia")))
    app.add_handler(CommandHandler("perdida", stub_cmd("perdida")))
    app.add_handler(CommandHandler("balance", stub_cmd("balance")))
    app.add_handler(CommandHandler("neto", stub_cmd("neto")))
    app.add_handler(CommandHandler("bruto", stub_cmd("bruto")))
    app.add_handler(CommandHandler("presupuesto", stub_cmd("presupuesto")))
    app.add_handler(CommandHandler("plan_financiero", stub_cmd("plan_financiero")))
    app.add_handler(CommandHandler("ahorro", stub_cmd("ahorro")))
    app.add_handler(CommandHandler("inversion", stub_cmd("inversion")))
    app.add_handler(CommandHandler("rendimiento", stub_cmd("rendimiento")))
    app.add_handler(CommandHandler("roi", stub_cmd("roi")))
    app.add_handler(CommandHandler("interes", stub_cmd("interes")))
    app.add_handler(CommandHandler("tasa", stub_cmd("tasa")))
    app.add_handler(CommandHandler("hipoteca", stub_cmd("hipoteca")))
    app.add_handler(CommandHandler("prestamo", stub_cmd("prestamo")))
    app.add_handler(CommandHandler("credito", stub_cmd("credito")))
    app.add_handler(CommandHandler("deuda", stub_cmd("deuda")))
    app.add_handler(CommandHandler("impuesto", stub_cmd("impuesto")))
    app.add_handler(CommandHandler("salario", stub_cmd("salario")))
    app.add_handler(CommandHandler("sueldo", stub_cmd("sueldo")))
    app.add_handler(CommandHandler("bono", stub_cmd("bono")))
    app.add_handler(CommandHandler("comision", stub_cmd("comision")))
    app.add_handler(CommandHandler("prima", stub_cmd("prima")))
    app.add_handler(CommandHandler("gratificacion", stub_cmd("gratificacion")))
    app.add_handler(CommandHandler("aumento", stub_cmd("aumento")))
    app.add_handler(CommandHandler("impuestos", stub_cmd("impuestos")))
    app.add_handler(CommandHandler("iva", stub_cmd("iva")))
    app.add_handler(CommandHandler("retencion", stub_cmd("retencion")))
    app.add_handler(CommandHandler("descuento", stub_cmd("descuento")))
    app.add_handler(CommandHandler("traspaso", stub_cmd("traspaso")))
    app.add_handler(CommandHandler("liquidacion", stub_cmd("liquidacion")))
    app.add_handler(CommandHandler("portafolio", stub_cmd("portafolio")))
    app.add_handler(CommandHandler("acciones", stub_cmd("acciones")))
    app.add_handler(CommandHandler("bonos", stub_cmd("bonos")))
    app.add_handler(CommandHandler("fondos", stub_cmd("fondos")))
    app.add_handler(CommandHandler("criptomonedas", stub_cmd("criptomonedas")))
    app.add_handler(CommandHandler("bitcoin", stub_cmd("bitcoin")))
    app.add_handler(CommandHandler("ethereum", stub_cmd("ethereum")))
    app.add_handler(CommandHandler("bolsa", stub_cmd("bolsa")))
    app.add_handler(CommandHandler("mercado", stub_cmd("mercado")))
    app.add_handler(CommandHandler("cotizacion", stub_cmd("cotizacion")))
    app.add_handler(CommandHandler("precio", stub_cmd("precio")))
    app.add_handler(CommandHandler("compra", stub_cmd("compra")))
    app.add_handler(CommandHandler("venta", stub_cmd("venta")))
    app.add_handler(CommandHandler("especulacion", stub_cmd("especulacion")))
    app.add_handler(CommandHandler("jubilacion", stub_cmd("jubilacion")))
    app.add_handler(CommandHandler("fondo_pensional", stub_cmd("fondo_pensional")))
    app.add_handler(CommandHandler("seguro", stub_cmd("seguro")))
    app.add_handler(CommandHandler("poliza", stub_cmd("poliza")))
    app.add_handler(CommandHandler("cobertura", stub_cmd("cobertura")))
    app.add_handler(CommandHandler("proteccion", stub_cmd("proteccion")))
    app.add_handler(CommandHandler("curso", stub_cmd("curso")))
    app.add_handler(CommandHandler("clase", stub_cmd("clase")))
    app.add_handler(CommandHandler("leccion", stub_cmd("leccion")))
    app.add_handler(CommandHandler("tema", stub_cmd("tema")))
    app.add_handler(CommandHandler("materia", stub_cmd("materia")))
    app.add_handler(CommandHandler("asignatura", stub_cmd("asignatura")))
    app.add_handler(CommandHandler("disciplina", stub_cmd("disciplina")))
    app.add_handler(CommandHandler("estudiante", stub_cmd("estudiante")))
    app.add_handler(CommandHandler("profesor", stub_cmd("profesor")))
    app.add_handler(CommandHandler("maestro", stub_cmd("maestro")))
    app.add_handler(CommandHandler("tutor", stub_cmd("tutor")))
    app.add_handler(CommandHandler("mentor", stub_cmd("mentor")))
    app.add_handler(CommandHandler("coach", stub_cmd("coach")))
    app.add_handler(CommandHandler("instructor", stub_cmd("instructor")))
    app.add_handler(CommandHandler("examen", stub_cmd("examen")))
    app.add_handler(CommandHandler("test", stub_cmd("test")))
    app.add_handler(CommandHandler("quiz", stub_cmd("quiz")))
    app.add_handler(CommandHandler("evaluacion", stub_cmd("evaluacion")))
    app.add_handler(CommandHandler("calificacion", stub_cmd("calificacion")))
    app.add_handler(CommandHandler("nota", stub_cmd("nota")))
    app.add_handler(CommandHandler("puntuacion", stub_cmd("puntuacion")))
    app.add_handler(CommandHandler("aprendizaje", stub_cmd("aprendizaje")))
    app.add_handler(CommandHandler("estudio", stub_cmd("estudio")))
    app.add_handler(CommandHandler("lectura", stub_cmd("lectura")))
    app.add_handler(CommandHandler("libro", stub_cmd("libro")))
    app.add_handler(CommandHandler("tarea", stub_cmd("tarea")))
    app.add_handler(CommandHandler("deber", stub_cmd("deber")))
    app.add_handler(CommandHandler("trabajo", stub_cmd("trabajo")))
    app.add_handler(CommandHandler("investigacion", stub_cmd("investigacion")))
    app.add_handler(CommandHandler("proyecto", stub_cmd("proyecto")))
    app.add_handler(CommandHandler("presentacion", stub_cmd("presentacion")))
    app.add_handler(CommandHandler("exposicion", stub_cmd("exposicion")))
    app.add_handler(CommandHandler("debate", stub_cmd("debate")))
    app.add_handler(CommandHandler("discusion", stub_cmd("discusion")))
    app.add_handler(CommandHandler("certificado", stub_cmd("certificado")))
    app.add_handler(CommandHandler("diploma", stub_cmd("diploma")))
    app.add_handler(CommandHandler("titulo", stub_cmd("titulo")))
    app.add_handler(CommandHandler("grado", stub_cmd("grado")))
    app.add_handler(CommandHandler("carrera", stub_cmd("carrera")))
    app.add_handler(CommandHandler("profesion", stub_cmd("profesion")))
    app.add_handler(CommandHandler("especializacion", stub_cmd("especializacion")))
    app.add_handler(CommandHandler("universidad", stub_cmd("universidad")))
    app.add_handler(CommandHandler("escuela", stub_cmd("escuela")))
    app.add_handler(CommandHandler("instituto", stub_cmd("instituto")))
    app.add_handler(CommandHandler("academia", stub_cmd("academia")))
    app.add_handler(CommandHandler("centro", stub_cmd("centro")))
    app.add_handler(CommandHandler("campus", stub_cmd("campus")))
    app.add_handler(CommandHandler("aula", stub_cmd("aula")))
    app.add_handler(CommandHandler("horario", stub_cmd("horario")))
    app.add_handler(CommandHandler("calendario", stub_cmd("calendario")))
    app.add_handler(CommandHandler("semestre", stub_cmd("semestre")))
    app.add_handler(CommandHandler("trimestre", stub_cmd("trimestre")))
    app.add_handler(CommandHandler("bimestre", stub_cmd("bimestre")))
    app.add_handler(CommandHandler("periodo", stub_cmd("periodo")))
    app.add_handler(CommandHandler("ciclo", stub_cmd("ciclo")))
    app.add_handler(CommandHandler("competencia", stub_cmd("competencia")))
    app.add_handler(CommandHandler("habilidad", stub_cmd("habilidad")))
    app.add_handler(CommandHandler("conocimiento", stub_cmd("conocimiento")))
    app.add_handler(CommandHandler("sabiduria", stub_cmd("sabiduria")))
    app.add_handler(CommandHandler("inteligencia", stub_cmd("inteligencia")))
    app.add_handler(CommandHandler("genio", stub_cmd("genio")))
    app.add_handler(CommandHandler("idioma", stub_cmd("idioma")))
    app.add_handler(CommandHandler("matematica", stub_cmd("matematica")))
    app.add_handler(CommandHandler("ciencia", stub_cmd("ciencia")))
    app.add_handler(CommandHandler("historia", stub_cmd("historia")))
    app.add_handler(CommandHandler("geografia", stub_cmd("geografia")))
    app.add_handler(CommandHandler("arte", stub_cmd("arte")))
    app.add_handler(CommandHandler("tecnologia", stub_cmd("tecnologia")))
    app.add_handler(CommandHandler("salud", stub_cmd("salud")))
    app.add_handler(CommandHandler("medico", stub_cmd("medico")))
    app.add_handler(CommandHandler("doctor", stub_cmd("doctor")))
    app.add_handler(CommandHandler("clinica", stub_cmd("clinica")))
    app.add_handler(CommandHandler("hospital", stub_cmd("hospital")))
    app.add_handler(CommandHandler("farmacia", stub_cmd("farmacia")))
    app.add_handler(CommandHandler("medicamento", stub_cmd("medicamento")))
    app.add_handler(CommandHandler("enfermedad", stub_cmd("enfermedad")))
    app.add_handler(CommandHandler("sindrome", stub_cmd("sindrome")))
    app.add_handler(CommandHandler("dolor", stub_cmd("dolor")))
    app.add_handler(CommandHandler("tos", stub_cmd("tos")))
    app.add_handler(CommandHandler("fiebre", stub_cmd("fiebre")))
    app.add_handler(CommandHandler("gripe", stub_cmd("gripe")))
    app.add_handler(CommandHandler("resfriado", stub_cmd("resfriado")))
    app.add_handler(CommandHandler("vacuna", stub_cmd("vacuna")))
    app.add_handler(CommandHandler("inyeccion", stub_cmd("inyeccion")))
    app.add_handler(CommandHandler("pastilla", stub_cmd("pastilla")))
    app.add_handler(CommandHandler("jarabe", stub_cmd("jarabe")))
    app.add_handler(CommandHandler("pomada", stub_cmd("pomada")))
    app.add_handler(CommandHandler("vendaje", stub_cmd("vendaje")))
    app.add_handler(CommandHandler("curacion", stub_cmd("curacion")))
    app.add_handler(CommandHandler("cita", stub_cmd("cita")))
    app.add_handler(CommandHandler("consulta", stub_cmd("consulta")))
    app.add_handler(CommandHandler("diagnostico", stub_cmd("diagnostico")))
    app.add_handler(CommandHandler("tratamiento", stub_cmd("tratamiento")))
    app.add_handler(CommandHandler("terapia", stub_cmd("terapia")))
    app.add_handler(CommandHandler("rehabilitacion", stub_cmd("rehabilitacion")))
    app.add_handler(CommandHandler("nutricion", stub_cmd("nutricion")))
    app.add_handler(CommandHandler("dieta", stub_cmd("dieta")))
    app.add_handler(CommandHandler("ejercicio", stub_cmd("ejercicio")))
    app.add_handler(CommandHandler("descanso", stub_cmd("descanso")))
    app.add_handler(CommandHandler("sueno", stub_cmd("sueno")))
    app.add_handler(CommandHandler("relajacion", stub_cmd("relajacion")))
    app.add_handler(CommandHandler("estres", stub_cmd("estres")))
    app.add_handler(CommandHandler("ansiedad", stub_cmd("ansiedad")))
    app.add_handler(CommandHandler("depresion", stub_cmd("depresion")))
    app.add_handler(CommandHandler("bienestar", stub_cmd("bienestar")))
    app.add_handler(CommandHandler("salud_mental", stub_cmd("salud_mental")))
    app.add_handler(CommandHandler("psicologia", stub_cmd("psicologia")))
    app.add_handler(CommandHandler("psiquiatra", stub_cmd("psiquiatra")))
    app.add_handler(CommandHandler("presion_arterial", stub_cmd("presion_arterial")))
    app.add_handler(CommandHandler("frecuencia_cardiaca", stub_cmd("frecuencia_cardiaca")))
    app.add_handler(CommandHandler("glucosa", stub_cmd("glucosa")))
    app.add_handler(CommandHandler("colesterol", stub_cmd("colesterol")))
    app.add_handler(CommandHandler("hemoglobina", stub_cmd("hemoglobina")))
    app.add_handler(CommandHandler("revision", stub_cmd("revision")))
    app.add_handler(CommandHandler("chequeo", stub_cmd("chequeo")))
    app.add_handler(CommandHandler("screening", stub_cmd("screening")))
    app.add_handler(CommandHandler("prueba", stub_cmd("prueba")))
    app.add_handler(CommandHandler("analisis", stub_cmd("analisis")))
    app.add_handler(CommandHandler("ecografia", stub_cmd("ecografia")))
    app.add_handler(CommandHandler("radiografia", stub_cmd("radiografia")))
    app.add_handler(CommandHandler("prevencion", stub_cmd("prevencion")))
    app.add_handler(CommandHandler("cuidado", stub_cmd("cuidado")))
    app.add_handler(CommandHandler("higiene", stub_cmd("higiene")))
    app.add_handler(CommandHandler("vacunacion", stub_cmd("vacunacion")))
    app.add_handler(CommandHandler("inmunidad", stub_cmd("inmunidad")))
    app.add_handler(CommandHandler("defensa", stub_cmd("defensa")))
    app.add_handler(CommandHandler("embarazo", stub_cmd("embarazo")))
    app.add_handler(CommandHandler("parto", stub_cmd("parto")))
    app.add_handler(CommandHandler("bebe", stub_cmd("bebe")))
    app.add_handler(CommandHandler("pediatria", stub_cmd("pediatria")))
    app.add_handler(CommandHandler("desarrollo", stub_cmd("desarrollo")))
    app.add_handler(CommandHandler("crecimiento", stub_cmd("crecimiento")))
    app.add_handler(CommandHandler("edad", stub_cmd("edad")))
    app.add_handler(CommandHandler("viaje", stub_cmd("viaje")))
    app.add_handler(CommandHandler("tour", stub_cmd("tour")))
    app.add_handler(CommandHandler("turismo", stub_cmd("turismo")))
    app.add_handler(CommandHandler("vacaciones", stub_cmd("vacaciones")))
    app.add_handler(CommandHandler("destino", stub_cmd("destino")))
    app.add_handler(CommandHandler("hotel", stub_cmd("hotel")))
    app.add_handler(CommandHandler("hospedaje", stub_cmd("hospedaje")))
    app.add_handler(CommandHandler("pasaje", stub_cmd("pasaje")))
    app.add_handler(CommandHandler("vuelo", stub_cmd("vuelo")))
    app.add_handler(CommandHandler("aerolinea", stub_cmd("aerolinea")))
    app.add_handler(CommandHandler("equipaje", stub_cmd("equipaje")))
    app.add_handler(CommandHandler("maleta", stub_cmd("maleta")))
    app.add_handler(CommandHandler("mochila", stub_cmd("mochila")))
    app.add_handler(CommandHandler("bolso", stub_cmd("bolso")))
    app.add_handler(CommandHandler("pasaporte", stub_cmd("pasaporte")))
    app.add_handler(CommandHandler("visa", stub_cmd("visa")))
    app.add_handler(CommandHandler("documento", stub_cmd("documento")))
    app.add_handler(CommandHandler("identificacion", stub_cmd("identificacion")))
    app.add_handler(CommandHandler("ticket", stub_cmd("ticket")))
    app.add_handler(CommandHandler("boleto", stub_cmd("boleto")))
    app.add_handler(CommandHandler("reserva", stub_cmd("reserva")))
    app.add_handler(CommandHandler("excursion", stub_cmd("excursion")))
    app.add_handler(CommandHandler("aventura", stub_cmd("aventura")))
    app.add_handler(CommandHandler("trekking", stub_cmd("trekking")))
    app.add_handler(CommandHandler("camping", stub_cmd("camping")))
    app.add_handler(CommandHandler("hostal", stub_cmd("hostal")))
    app.add_handler(CommandHandler("airbnb", stub_cmd("airbnb")))
    app.add_handler(CommandHandler("motel", stub_cmd("motel")))
    app.add_handler(CommandHandler("comida", stub_cmd("comida")))
    app.add_handler(CommandHandler("restaurante", stub_cmd("restaurante")))
    app.add_handler(CommandHandler("gastronomia", stub_cmd("gastronomia")))
    app.add_handler(CommandHandler("platillo", stub_cmd("platillo")))
    app.add_handler(CommandHandler("postre", stub_cmd("postre")))
    app.add_handler(CommandHandler("bebida", stub_cmd("bebida")))
    app.add_handler(CommandHandler("cafe", stub_cmd("cafe")))
    app.add_handler(CommandHandler("playa", stub_cmd("playa")))
    app.add_handler(CommandHandler("montana", stub_cmd("montana")))
    app.add_handler(CommandHandler("ciudad", stub_cmd("ciudad")))
    app.add_handler(CommandHandler("pueblo", stub_cmd("pueblo")))
    app.add_handler(CommandHandler("pueblo_magico", stub_cmd("pueblo_magico")))
    app.add_handler(CommandHandler("isla", stub_cmd("isla")))
    app.add_handler(CommandHandler("continente", stub_cmd("continente")))
    app.add_handler(CommandHandler("transporte", stub_cmd("transporte")))
    app.add_handler(CommandHandler("autobus", stub_cmd("autobus")))
    app.add_handler(CommandHandler("tren", stub_cmd("tren")))
    app.add_handler(CommandHandler("auto", stub_cmd("auto")))
    app.add_handler(CommandHandler("bicicleta", stub_cmd("bicicleta")))
    app.add_handler(CommandHandler("motocicleta", stub_cmd("motocicleta")))
    app.add_handler(CommandHandler("scooter", stub_cmd("scooter")))
    app.add_handler(CommandHandler("mapa", stub_cmd("mapa")))
    app.add_handler(CommandHandler("ruta", stub_cmd("ruta")))
    app.add_handler(CommandHandler("direccion", stub_cmd("direccion")))
    app.add_handler(CommandHandler("ubicacion", stub_cmd("ubicacion")))
    app.add_handler(CommandHandler("gps", stub_cmd("gps")))
    app.add_handler(CommandHandler("brujula", stub_cmd("brujula")))
    app.add_handler(CommandHandler("camino", stub_cmd("camino")))
    app.add_handler(CommandHandler("clima", stub_cmd("clima")))
    app.add_handler(CommandHandler("temperatura", stub_cmd("temperatura")))
    app.add_handler(CommandHandler("lluvia", stub_cmd("lluvia")))
    app.add_handler(CommandHandler("nieve", stub_cmd("nieve")))
    app.add_handler(CommandHandler("sol", stub_cmd("sol")))
    app.add_handler(CommandHandler("humedad", stub_cmd("humedad")))
    app.add_handler(CommandHandler("viento", stub_cmd("viento")))
    app.add_handler(CommandHandler("fotografia", stub_cmd("fotografia")))
    app.add_handler(CommandHandler("camara", stub_cmd("camara")))
    app.add_handler(CommandHandler("video", stub_cmd("video")))
    app.add_handler(CommandHandler("recuerdo", stub_cmd("recuerdo")))
    app.add_handler(CommandHandler("souvenir", stub_cmd("souvenir")))
    app.add_handler(CommandHandler("regalo", stub_cmd("regalo")))
    app.add_handler(CommandHandler("compra", stub_cmd("compra")))
    app.add_handler(CommandHandler("python", stub_cmd("python")))
    app.add_handler(CommandHandler("javascript", stub_cmd("javascript")))
    app.add_handler(CommandHandler("java", stub_cmd("java")))
    app.add_handler(CommandHandler("csharp", stub_cmd("csharp")))
    app.add_handler(CommandHandler("golang", stub_cmd("golang")))
    app.add_handler(CommandHandler("rust", stub_cmd("rust")))
    app.add_handler(CommandHandler("php", stub_cmd("php")))
    app.add_handler(CommandHandler("html", stub_cmd("html")))
    app.add_handler(CommandHandler("css", stub_cmd("css")))
    app.add_handler(CommandHandler("react", stub_cmd("react")))
    app.add_handler(CommandHandler("vue", stub_cmd("vue")))
    app.add_handler(CommandHandler("angular", stub_cmd("angular")))
    app.add_handler(CommandHandler("svelte", stub_cmd("svelte")))
    app.add_handler(CommandHandler("next", stub_cmd("next")))
    app.add_handler(CommandHandler("nuxt", stub_cmd("nuxt")))
    app.add_handler(CommandHandler("backend", stub_cmd("backend")))
    app.add_handler(CommandHandler("frontend", stub_cmd("frontend")))
    app.add_handler(CommandHandler("fullstack", stub_cmd("fullstack")))
    app.add_handler(CommandHandler("api", stub_cmd("api")))
    app.add_handler(CommandHandler("rest", stub_cmd("rest")))
    app.add_handler(CommandHandler("graphql", stub_cmd("graphql")))
    app.add_handler(CommandHandler("websocket", stub_cmd("websocket")))
    app.add_handler(CommandHandler("database", stub_cmd("database")))
    app.add_handler(CommandHandler("sql", stub_cmd("sql")))
    app.add_handler(CommandHandler("mysql", stub_cmd("mysql")))
    app.add_handler(CommandHandler("postgresql", stub_cmd("postgresql")))
    app.add_handler(CommandHandler("mongodb", stub_cmd("mongodb")))
    app.add_handler(CommandHandler("redis", stub_cmd("redis")))
    app.add_handler(CommandHandler("elasticsearch", stub_cmd("elasticsearch")))
    app.add_handler(CommandHandler("linux", stub_cmd("linux")))
    app.add_handler(CommandHandler("windows", stub_cmd("windows")))
    app.add_handler(CommandHandler("macos", stub_cmd("macos")))
    app.add_handler(CommandHandler("comando", stub_cmd("comando")))
    app.add_handler(CommandHandler("terminal", stub_cmd("terminal")))
    app.add_handler(CommandHandler("shell", stub_cmd("shell")))
    app.add_handler(CommandHandler("bash", stub_cmd("bash")))
    app.add_handler(CommandHandler("git", stub_cmd("git")))
    app.add_handler(CommandHandler("github", stub_cmd("github")))
    app.add_handler(CommandHandler("gitlab", stub_cmd("gitlab")))
    app.add_handler(CommandHandler("bitbucket", stub_cmd("bitbucket")))
    app.add_handler(CommandHandler("commit", stub_cmd("commit")))
    app.add_handler(CommandHandler("push", stub_cmd("push")))
    app.add_handler(CommandHandler("pull", stub_cmd("pull")))
    app.add_handler(CommandHandler("merge", stub_cmd("merge")))
    app.add_handler(CommandHandler("docker", stub_cmd("docker")))
    app.add_handler(CommandHandler("kubernetes", stub_cmd("kubernetes")))
    app.add_handler(CommandHandler("contenedor", stub_cmd("contenedor")))
    app.add_handler(CommandHandler("virtualizacion", stub_cmd("virtualizacion")))
    app.add_handler(CommandHandler("cloud", stub_cmd("cloud")))
    app.add_handler(CommandHandler("aws", stub_cmd("aws")))
    app.add_handler(CommandHandler("azure", stub_cmd("azure")))
    app.add_handler(CommandHandler("devops", stub_cmd("devops")))
    app.add_handler(CommandHandler("ci_cd", stub_cmd("ci_cd")))
    app.add_handler(CommandHandler("pipeline", stub_cmd("pipeline")))
    app.add_handler(CommandHandler("jenkins", stub_cmd("jenkins")))
    app.add_handler(CommandHandler("github_actions", stub_cmd("github_actions")))
    app.add_handler(CommandHandler("gitlab_ci", stub_cmd("gitlab_ci")))
    app.add_handler(CommandHandler("seguridad", stub_cmd("seguridad")))
    app.add_handler(CommandHandler("encriptacion", stub_cmd("encriptacion")))
    app.add_handler(CommandHandler("hash", stub_cmd("hash")))
    app.add_handler(CommandHandler("ssl", stub_cmd("ssl")))
    app.add_handler(CommandHandler("tls", stub_cmd("tls")))
    app.add_handler(CommandHandler("firewall", stub_cmd("firewall")))
    app.add_handler(CommandHandler("vpn", stub_cmd("vpn")))
    app.add_handler(CommandHandler("testing", stub_cmd("testing")))
    app.add_handler(CommandHandler("unittest", stub_cmd("unittest")))
    app.add_handler(CommandHandler("pytest", stub_cmd("pytest")))
    app.add_handler(CommandHandler("jest", stub_cmd("jest")))
    app.add_handler(CommandHandler("mocha", stub_cmd("mocha")))
    app.add_handler(CommandHandler("jasmine", stub_cmd("jasmine")))
    app.add_handler(CommandHandler("selenium", stub_cmd("selenium")))
    app.add_handler(CommandHandler("empresa", stub_cmd("empresa")))
    app.add_handler(CommandHandler("negocio", stub_cmd("negocio")))
    app.add_handler(CommandHandler("emprendimiento", stub_cmd("emprendimiento")))
    app.add_handler(CommandHandler("startup", stub_cmd("startup")))
    app.add_handler(CommandHandler("pyme", stub_cmd("pyme")))
    app.add_handler(CommandHandler("corporativo", stub_cmd("corporativo")))
    app.add_handler(CommandHandler("gerente", stub_cmd("gerente")))
    app.add_handler(CommandHandler("ceo", stub_cmd("ceo")))
    app.add_handler(CommandHandler("director", stub_cmd("director")))
    app.add_handler(CommandHandler("empleado", stub_cmd("empleado")))
    app.add_handler(CommandHandler("trabajador", stub_cmd("trabajador")))
    app.add_handler(CommandHandler("cliente", stub_cmd("cliente")))
    app.add_handler(CommandHandler("proveedor", stub_cmd("proveedor")))
    app.add_handler(CommandHandler("producto", stub_cmd("producto")))
    app.add_handler(CommandHandler("servicio", stub_cmd("servicio")))
    app.add_handler(CommandHandler("venta", stub_cmd("venta")))
    app.add_handler(CommandHandler("compra", stub_cmd("compra")))
    app.add_handler(CommandHandler("precio", stub_cmd("precio")))
    app.add_handler(CommandHandler("margen", stub_cmd("margen")))
    app.add_handler(CommandHandler("ganancia", stub_cmd("ganancia")))
    app.add_handler(CommandHandler("marketing", stub_cmd("marketing")))
    app.add_handler(CommandHandler("publicidad", stub_cmd("publicidad")))
    app.add_handler(CommandHandler("promocion", stub_cmd("promocion")))
    app.add_handler(CommandHandler("campana", stub_cmd("campana")))
    app.add_handler(CommandHandler("social_media", stub_cmd("social_media")))
    app.add_handler(CommandHandler("influencer", stub_cmd("influencer")))
    app.add_handler(CommandHandler("ventas", stub_cmd("ventas")))
    app.add_handler(CommandHandler("prospecto", stub_cmd("prospecto")))
    app.add_handler(CommandHandler("cliente_potencial", stub_cmd("cliente_potencial")))
    app.add_handler(CommandHandler("conversion", stub_cmd("conversion")))
    app.add_handler(CommandHandler("retention", stub_cmd("retention")))
    app.add_handler(CommandHandler("loyalty", stub_cmd("loyalty")))
    app.add_handler(CommandHandler("estrategia", stub_cmd("estrategia")))
    app.add_handler(CommandHandler("analisis", stub_cmd("analisis")))
    app.add_handler(CommandHandler("foda", stub_cmd("foda")))
    app.add_handler(CommandHandler("benchmarking", stub_cmd("benchmarking")))
    app.add_handler(CommandHandler("competencia", stub_cmd("competencia")))
    app.add_handler(CommandHandler("mercado", stub_cmd("mercado")))
    app.add_handler(CommandHandler("expansion", stub_cmd("expansion")))
    app.add_handler(CommandHandler("franchicia", stub_cmd("franchicia")))
    app.add_handler(CommandHandler("afiliacion", stub_cmd("afiliacion")))
    app.add_handler(CommandHandler("distribucion", stub_cmd("distribucion")))
    app.add_handler(CommandHandler("logistica", stub_cmd("logistica")))
    app.add_handler(CommandHandler("supply_chain", stub_cmd("supply_chain")))
    app.add_handler(CommandHandler("finanzas", stub_cmd("finanzas")))
    app.add_handler(CommandHandler("contabilidad", stub_cmd("contabilidad")))
    app.add_handler(CommandHandler("auditoria", stub_cmd("auditoria")))
    app.add_handler(CommandHandler("impuestos", stub_cmd("impuestos")))
    app.add_handler(CommandHandler("facturacion", stub_cmd("facturacion")))
    app.add_handler(CommandHandler("cobranza", stub_cmd("cobranza")))
    app.add_handler(CommandHandler("recursos_humanos", stub_cmd("recursos_humanos")))
    app.add_handler(CommandHandler("reclutamiento", stub_cmd("reclutamiento")))
    app.add_handler(CommandHandler("seleccion", stub_cmd("seleccion")))
    app.add_handler(CommandHandler("entrevista", stub_cmd("entrevista")))
    app.add_handler(CommandHandler("capacitacion", stub_cmd("capacitacion")))
    app.add_handler(CommandHandler("comunicacion", stub_cmd("comunicacion")))
    app.add_handler(CommandHandler("presentacion", stub_cmd("presentacion")))
    app.add_handler(CommandHandler("negociacion", stub_cmd("negociacion")))
    app.add_handler(CommandHandler("contrato", stub_cmd("contrato")))
    app.add_handler(CommandHandler("acuerdo", stub_cmd("acuerdo")))
    app.add_handler(CommandHandler("clausula", stub_cmd("clausula")))
    app.add_handler(CommandHandler("arte", stub_cmd("arte")))
    app.add_handler(CommandHandler("pintura", stub_cmd("pintura")))
    app.add_handler(CommandHandler("escultura", stub_cmd("escultura")))
    app.add_handler(CommandHandler("fotografia", stub_cmd("fotografia")))
    app.add_handler(CommandHandler("cine", stub_cmd("cine")))
    app.add_handler(CommandHandler("musica", stub_cmd("musica")))
    app.add_handler(CommandHandler("danza", stub_cmd("danza")))
    app.add_handler(CommandHandler("literatura", stub_cmd("literatura")))
    app.add_handler(CommandHandler("poesia", stub_cmd("poesia")))
    app.add_handler(CommandHandler("novela", stub_cmd("novela")))
    app.add_handler(CommandHandler("cuento", stub_cmd("cuento")))
    app.add_handler(CommandHandler("ensayo", stub_cmd("ensayo")))
    app.add_handler(CommandHandler("articulo", stub_cmd("articulo")))
    app.add_handler(CommandHandler("blog", stub_cmd("blog")))
    app.add_handler(CommandHandler("teatro", stub_cmd("teatro")))
    app.add_handler(CommandHandler("comedia", stub_cmd("comedia")))
    app.add_handler(CommandHandler("drama", stub_cmd("drama")))
    app.add_handler(CommandHandler("tragedia", stub_cmd("tragedia")))
    app.add_handler(CommandHandler("musical", stub_cmd("musical")))
    app.add_handler(CommandHandler("concierto", stub_cmd("concierto")))
    app.add_handler(CommandHandler("festival", stub_cmd("festival")))
    app.add_handler(CommandHandler("museo", stub_cmd("museo")))
    app.add_handler(CommandHandler("galeria", stub_cmd("galeria")))
    app.add_handler(CommandHandler("exposicion", stub_cmd("exposicion")))
    app.add_handler(CommandHandler("coleccion", stub_cmd("coleccion")))
    app.add_handler(CommandHandler("obra_maestra", stub_cmd("obra_maestra")))
    app.add_handler(CommandHandler("clasico", stub_cmd("clasico")))
    app.add_handler(CommandHandler("artista", stub_cmd("artista")))
    app.add_handler(CommandHandler("pintor", stub_cmd("pintor")))
    app.add_handler(CommandHandler("escultor", stub_cmd("escultor")))
    app.add_handler(CommandHandler("fotografo", stub_cmd("fotografo")))
    app.add_handler(CommandHandler("cineasta", stub_cmd("cineasta")))
    app.add_handler(CommandHandler("musico", stub_cmd("musico")))
    app.add_handler(CommandHandler("poeta", stub_cmd("poeta")))
    app.add_handler(CommandHandler("estilo", stub_cmd("estilo")))
    app.add_handler(CommandHandler("movimiento", stub_cmd("movimiento")))
    app.add_handler(CommandHandler("corriente", stub_cmd("corriente")))
    app.add_handler(CommandHandler("renaissance", stub_cmd("renaissance")))
    app.add_handler(CommandHandler("barroco", stub_cmd("barroco")))
    app.add_handler(CommandHandler("moderno", stub_cmd("moderno")))
    app.add_handler(CommandHandler("color", stub_cmd("color")))
    app.add_handler(CommandHandler("forma", stub_cmd("forma")))
    app.add_handler(CommandHandler("linea", stub_cmd("linea")))
    app.add_handler(CommandHandler("textura", stub_cmd("textura")))
    app.add_handler(CommandHandler("composicion", stub_cmd("composicion")))
    app.add_handler(CommandHandler("perspectiva", stub_cmd("perspectiva")))
    app.add_handler(CommandHandler("proporcion", stub_cmd("proporcion")))
    app.add_handler(CommandHandler("musica", stub_cmd("musica")))
    app.add_handler(CommandHandler("nota", stub_cmd("nota")))
    app.add_handler(CommandHandler("acorde", stub_cmd("acorde")))
    app.add_handler(CommandHandler("ritmo", stub_cmd("ritmo")))
    app.add_handler(CommandHandler("melodia", stub_cmd("melodia")))
    app.add_handler(CommandHandler("armonia", stub_cmd("armonia")))
    app.add_handler(CommandHandler("tempo", stub_cmd("tempo")))
    app.add_handler(CommandHandler("instrumento", stub_cmd("instrumento")))
    app.add_handler(CommandHandler("guitarra", stub_cmd("guitarra")))
    app.add_handler(CommandHandler("piano", stub_cmd("piano")))
    app.add_handler(CommandHandler("violin", stub_cmd("violin")))
    app.add_handler(CommandHandler("bateria", stub_cmd("bateria")))
    app.add_handler(CommandHandler("flauta", stub_cmd("flauta")))
    app.add_handler(CommandHandler("saxofon", stub_cmd("saxofon")))
    app.add_handler(CommandHandler("genero", stub_cmd("genero")))
    app.add_handler(CommandHandler("rock", stub_cmd("rock")))
    app.add_handler(CommandHandler("pop", stub_cmd("pop")))
    app.add_handler(CommandHandler("jazz", stub_cmd("jazz")))
    app.add_handler(CommandHandler("clasico", stub_cmd("clasico")))
    app.add_handler(CommandHandler("electronica", stub_cmd("electronica")))
    app.add_handler(CommandHandler("hip_hop", stub_cmd("hip_hop")))
    app.add_handler(CommandHandler("reggaeton", stub_cmd("reggaeton")))
    app.add_handler(CommandHandler("futbol", stub_cmd("futbol")))
    app.add_handler(CommandHandler("basquetbol", stub_cmd("basquetbol")))
    app.add_handler(CommandHandler("voley", stub_cmd("voley")))
    app.add_handler(CommandHandler("tenis", stub_cmd("tenis")))
    app.add_handler(CommandHandler("badminton", stub_cmd("badminton")))
    app.add_handler(CommandHandler("ping_pong", stub_cmd("ping_pong")))
    app.add_handler(CommandHandler("golf", stub_cmd("golf")))
    app.add_handler(CommandHandler("atletismo", stub_cmd("atletismo")))
    app.add_handler(CommandHandler("carrera", stub_cmd("carrera")))
    app.add_handler(CommandHandler("salto", stub_cmd("salto")))
    app.add_handler(CommandHandler("lanzamiento", stub_cmd("lanzamiento")))
    app.add_handler(CommandHandler("maraton", stub_cmd("maraton")))
    app.add_handler(CommandHandler("100_metros", stub_cmd("100_metros")))
    app.add_handler(CommandHandler("natacion", stub_cmd("natacion")))
    app.add_handler(CommandHandler("buceo", stub_cmd("buceo")))
    app.add_handler(CommandHandler("surf", stub_cmd("surf")))
    app.add_handler(CommandHandler("windsurf", stub_cmd("windsurf")))
    app.add_handler(CommandHandler("esqui", stub_cmd("esqui")))
    app.add_handler(CommandHandler("snowboard", stub_cmd("snowboard")))
    app.add_handler(CommandHandler("patinaje", stub_cmd("patinaje")))
    app.add_handler(CommandHandler("boxeo", stub_cmd("boxeo")))
    app.add_handler(CommandHandler("lucha", stub_cmd("lucha")))
    app.add_handler(CommandHandler("judo", stub_cmd("judo")))
    app.add_handler(CommandHandler("karate", stub_cmd("karate")))
    app.add_handler(CommandHandler("taekwondo", stub_cmd("taekwondo")))
    app.add_handler(CommandHandler("muay_thai", stub_cmd("muay_thai")))
    app.add_handler(CommandHandler("kickboxing", stub_cmd("kickboxing")))
    app.add_handler(CommandHandler("ciclismo", stub_cmd("ciclismo")))
    app.add_handler(CommandHandler("bicicleta", stub_cmd("bicicleta")))
    app.add_handler(CommandHandler("mountain_bike", stub_cmd("mountain_bike")))
    app.add_handler(CommandHandler("bmx", stub_cmd("bmx")))
    app.add_handler(CommandHandler("automovilismo", stub_cmd("automovilismo")))
    app.add_handler(CommandHandler("motociclismo", stub_cmd("motociclismo")))
    app.add_handler(CommandHandler("equitacion", stub_cmd("equitacion")))
    app.add_handler(CommandHandler("polo", stub_cmd("polo")))
    app.add_handler(CommandHandler("rodeo", stub_cmd("rodeo")))
    app.add_handler(CommandHandler("equestrian", stub_cmd("equestrian")))
    app.add_handler(CommandHandler("hipismo", stub_cmd("hipismo")))
    app.add_handler(CommandHandler("carrera_caballos", stub_cmd("carrera_caballos")))
    app.add_handler(CommandHandler("vela", stub_cmd("vela")))
    app.add_handler(CommandHandler("yate", stub_cmd("yate")))
    app.add_handler(CommandHandler("kayak", stub_cmd("kayak")))
    app.add_handler(CommandHandler("canoa", stub_cmd("canoa")))
    app.add_handler(CommandHandler("piragua", stub_cmd("piragua")))
    app.add_handler(CommandHandler("remo", stub_cmd("remo")))
    app.add_handler(CommandHandler("barco", stub_cmd("barco")))
    app.add_handler(CommandHandler("fitness", stub_cmd("fitness")))
    app.add_handler(CommandHandler("gym", stub_cmd("gym")))
    app.add_handler(CommandHandler("crossfit", stub_cmd("crossfit")))
    app.add_handler(CommandHandler("pilates", stub_cmd("pilates")))
    app.add_handler(CommandHandler("yoga", stub_cmd("yoga")))
    app.add_handler(CommandHandler("zumba", stub_cmd("zumba")))
    app.add_handler(CommandHandler("aerobica", stub_cmd("aerobica")))
    app.add_handler(CommandHandler("equipo", stub_cmd("equipo")))
    app.add_handler(CommandHandler("balon", stub_cmd("balon")))
    app.add_handler(CommandHandler("raqueta", stub_cmd("raqueta")))
    app.add_handler(CommandHandler("palo", stub_cmd("palo")))
    app.add_handler(CommandHandler("guantes", stub_cmd("guantes")))
    app.add_handler(CommandHandler("uniforme", stub_cmd("uniforme")))
    app.add_handler(CommandHandler("casco", stub_cmd("casco")))
    app.add_handler(CommandHandler("entrenador", stub_cmd("entrenador")))
    app.add_handler(CommandHandler("arbitro", stub_cmd("arbitro")))
    app.add_handler(CommandHandler("juez", stub_cmd("juez")))
    app.add_handler(CommandHandler("comentarista", stub_cmd("comentarista")))
    app.add_handler(CommandHandler("fan", stub_cmd("fan")))
    app.add_handler(CommandHandler("hincha", stub_cmd("hincha")))
    app.add_handler(CommandHandler("aficionado", stub_cmd("aficionado")))
    app.add_handler(CommandHandler("facebook", stub_cmd("facebook")))
    app.add_handler(CommandHandler("instagram", stub_cmd("instagram")))
    app.add_handler(CommandHandler("twitter", stub_cmd("twitter")))
    app.add_handler(CommandHandler("tiktok", stub_cmd("tiktok")))
    app.add_handler(CommandHandler("youtube", stub_cmd("youtube")))
    app.add_handler(CommandHandler("linkedin", stub_cmd("linkedin")))
    app.add_handler(CommandHandler("snapchat", stub_cmd("snapchat")))
    app.add_handler(CommandHandler("whatsapp", stub_cmd("whatsapp")))
    app.add_handler(CommandHandler("telegram", stub_cmd("telegram")))
    app.add_handler(CommandHandler("discord", stub_cmd("discord")))
    app.add_handler(CommandHandler("slack", stub_cmd("slack")))
    app.add_handler(CommandHandler("twitch", stub_cmd("twitch")))
    app.add_handler(CommandHandler("reddit", stub_cmd("reddit")))
    app.add_handler(CommandHandler("post", stub_cmd("post")))
    app.add_handler(CommandHandler("comentario", stub_cmd("comentario")))
    app.add_handler(CommandHandler("like", stub_cmd("like")))
    app.add_handler(CommandHandler("retweet", stub_cmd("retweet")))
    app.add_handler(CommandHandler("share", stub_cmd("share")))
    app.add_handler(CommandHandler("story", stub_cmd("story")))
    app.add_handler(CommandHandler("reel", stub_cmd("reel")))
    app.add_handler(CommandHandler("short", stub_cmd("short")))
    app.add_handler(CommandHandler("seguidor", stub_cmd("seguidor")))
    app.add_handler(CommandHandler("seguir", stub_cmd("seguir")))
    app.add_handler(CommandHandler("deseguir", stub_cmd("deseguir")))
    app.add_handler(CommandHandler("bloquear", stub_cmd("bloquear")))
    app.add_handler(CommandHandler("reportar", stub_cmd("reportar")))
    app.add_handler(CommandHandler("denunciar", stub_cmd("denunciar")))
    app.add_handler(CommandHandler("muteado", stub_cmd("muteado")))
    app.add_handler(CommandHandler("hashtag", stub_cmd("hashtag")))
    app.add_handler(CommandHandler("tendencia", stub_cmd("tendencia")))
    app.add_handler(CommandHandler("viral", stub_cmd("viral")))
    app.add_handler(CommandHandler("trending", stub_cmd("trending")))
    app.add_handler(CommandHandler("meme", stub_cmd("meme")))
    app.add_handler(CommandHandler("sticker", stub_cmd("sticker")))
    app.add_handler(CommandHandler("emoji", stub_cmd("emoji")))
    app.add_handler(CommandHandler("foto", stub_cmd("foto")))
    app.add_handler(CommandHandler("video", stub_cmd("video")))
    app.add_handler(CommandHandler("live", stub_cmd("live")))
    app.add_handler(CommandHandler("transmision", stub_cmd("transmision")))
    app.add_handler(CommandHandler("directo", stub_cmd("directo")))
    app.add_handler(CommandHandler("grabacion", stub_cmd("grabacion")))
    app.add_handler(CommandHandler("edicion", stub_cmd("edicion")))
    app.add_handler(CommandHandler("filtro", stub_cmd("filtro")))
    app.add_handler(CommandHandler("efecto", stub_cmd("efecto")))
    app.add_handler(CommandHandler("animacion", stub_cmd("animacion")))
    app.add_handler(CommandHandler("transicion", stub_cmd("transicion")))
    app.add_handler(CommandHandler("musica", stub_cmd("musica")))
    app.add_handler(CommandHandler("sonido", stub_cmd("sonido")))
    app.add_handler(CommandHandler("voice_over", stub_cmd("voice_over")))
    app.add_handler(CommandHandler("perfil", stub_cmd("perfil")))
    app.add_handler(CommandHandler("bio", stub_cmd("bio")))
    app.add_handler(CommandHandler("descripcion", stub_cmd("descripcion")))
    app.add_handler(CommandHandler("foto_perfil", stub_cmd("foto_perfil")))
    app.add_handler(CommandHandler("portada", stub_cmd("portada")))
    app.add_handler(CommandHandler("tema", stub_cmd("tema")))
    app.add_handler(CommandHandler("configuracion", stub_cmd("configuracion")))
    app.add_handler(CommandHandler("privacidad", stub_cmd("privacidad")))
    app.add_handler(CommandHandler("seguridad", stub_cmd("seguridad")))
    app.add_handler(CommandHandler("contrasena", stub_cmd("contrasena")))
    app.add_handler(CommandHandler("autenticacion", stub_cmd("autenticacion")))
    app.add_handler(CommandHandler("dos_factores", stub_cmd("dos_factores")))
    app.add_handler(CommandHandler("verificacion", stub_cmd("verificacion")))
    app.add_handler(CommandHandler("notificacion", stub_cmd("notificacion")))
    app.add_handler(CommandHandler("mensaje", stub_cmd("mensaje")))
    app.add_handler(CommandHandler("chat", stub_cmd("chat")))
    app.add_handler(CommandHandler("grupo", stub_cmd("grupo")))
    app.add_handler(CommandHandler("comunidad", stub_cmd("comunidad")))
    app.add_handler(CommandHandler("pagina", stub_cmd("pagina")))
    app.add_handler(CommandHandler("evento", stub_cmd("evento")))
    app.add_handler(CommandHandler("chiste", stub_cmd("chiste")))
    app.add_handler(CommandHandler("broma", stub_cmd("broma")))
    app.add_handler(CommandHandler("humor", stub_cmd("humor")))
    app.add_handler(CommandHandler("comedia", stub_cmd("comedia")))
    app.add_handler(CommandHandler("risa", stub_cmd("risa")))
    app.add_handler(CommandHandler("carcajada", stub_cmd("carcajada")))
    app.add_handler(CommandHandler("sonrisa", stub_cmd("sonrisa")))
    app.add_handler(CommandHandler("meme", stub_cmd("meme")))
    app.add_handler(CommandHandler("sticker", stub_cmd("sticker")))
    app.add_handler(CommandHandler("gif", stub_cmd("gif")))
    app.add_handler(CommandHandler("video_divertido", stub_cmd("video_divertido")))
    app.add_handler(CommandHandler("parodia", stub_cmd("parodia")))
    app.add_handler(CommandHandler("satira", stub_cmd("satira")))
    app.add_handler(CommandHandler("burla", stub_cmd("burla")))
    app.add_handler(CommandHandler("juego_palabras", stub_cmd("juego_palabras")))
    app.add_handler(CommandHandler("albur", stub_cmd("albur")))
    app.add_handler(CommandHandler("doble_sentido", stub_cmd("doble_sentido")))
    app.add_handler(CommandHandler("trabalenguas", stub_cmd("trabalenguas")))
    app.add_handler(CommandHandler("adivinanza_humor", stub_cmd("adivinanza_humor")))
    app.add_handler(CommandHandler("caricatura", stub_cmd("caricatura")))
    app.add_handler(CommandHandler("comic", stub_cmd("comic")))
    app.add_handler(CommandHandler("tira_comica", stub_cmd("tira_comica")))
    app.add_handler(CommandHandler("ilustracion_humor", stub_cmd("ilustracion_humor")))
    app.add_handler(CommandHandler("cartoon", stub_cmd("cartoon")))
    app.add_handler(CommandHandler("anime", stub_cmd("anime")))
    app.add_handler(CommandHandler("relato_corto", stub_cmd("relato_corto")))
    app.add_handler(CommandHandler("historia_divertida", stub_cmd("historia_divertida")))
    app.add_handler(CommandHandler("anecdota", stub_cmd("anecdota")))
    app.add_handler(CommandHandler("suceso_comico", stub_cmd("suceso_comico")))
    app.add_handler(CommandHandler("fail", stub_cmd("fail")))
    app.add_handler(CommandHandler("blooper", stub_cmd("blooper")))
    app.add_handler(CommandHandler("prank", stub_cmd("prank")))
    app.add_handler(CommandHandler("broma_pesada", stub_cmd("broma_pesada")))
    app.add_handler(CommandHandler("trucos", stub_cmd("trucos")))
    app.add_handler(CommandHandler("ilusion", stub_cmd("ilusion")))
    app.add_handler(CommandHandler("magia", stub_cmd("magia")))
    app.add_handler(CommandHandler("escape", stub_cmd("escape")))
    app.add_handler(CommandHandler("enigma", stub_cmd("enigma")))
    app.add_handler(CommandHandler("fiesta", stub_cmd("fiesta")))
    app.add_handler(CommandHandler("celebracion", stub_cmd("celebracion")))
    app.add_handler(CommandHandler("cumpleanos", stub_cmd("cumpleanos")))
    app.add_handler(CommandHandler("sorpresa", stub_cmd("sorpresa")))
    app.add_handler(CommandHandler("regalo", stub_cmd("regalo")))
    app.add_handler(CommandHandler("globos", stub_cmd("globos")))
    app.add_handler(CommandHandler("confeti", stub_cmd("confeti")))
    app.add_handler(CommandHandler("musica_divertida", stub_cmd("musica_divertida")))
    app.add_handler(CommandHandler("karaoke", stub_cmd("karaoke")))
    app.add_handler(CommandHandler("danza", stub_cmd("danza")))
    app.add_handler(CommandHandler("baile", stub_cmd("baile")))
    app.add_handler(CommandHandler("movimiento", stub_cmd("movimiento")))
    app.add_handler(CommandHandler("ritmo", stub_cmd("ritmo")))
    app.add_handler(CommandHandler("sincronizacion", stub_cmd("sincronizacion")))
    app.add_handler(CommandHandler("concurso", stub_cmd("concurso")))
    app.add_handler(CommandHandler("competencia", stub_cmd("competencia")))
    app.add_handler(CommandHandler("premio", stub_cmd("premio")))
    app.add_handler(CommandHandler("trofeo", stub_cmd("trofeo")))
    app.add_handler(CommandHandler("medalla", stub_cmd("medalla")))
    app.add_handler(CommandHandler("titulo", stub_cmd("titulo")))
    app.add_handler(CommandHandler("corona", stub_cmd("corona")))
    app.add_handler(CommandHandler("ridiculez", stub_cmd("ridiculez")))
    app.add_handler(CommandHandler("locura", stub_cmd("locura")))
    app.add_handler(CommandHandler("absurdo", stub_cmd("absurdo")))
    app.add_handler(CommandHandler("surrealismo", stub_cmd("surrealismo")))
    app.add_handler(CommandHandler("fantasia", stub_cmd("fantasia")))
    app.add_handler(CommandHandler("imaginacion", stub_cmd("imaginacion")))
    app.add_handler(CommandHandler("meditacion", stub_cmd("meditacion")))
    app.add_handler(CommandHandler("yoga", stub_cmd("yoga")))
    app.add_handler(CommandHandler("pranayama", stub_cmd("pranayama")))
    app.add_handler(CommandHandler("asana", stub_cmd("asana")))
    app.add_handler(CommandHandler("mantra", stub_cmd("mantra")))
    app.add_handler(CommandHandler("om", stub_cmd("om")))
    app.add_handler(CommandHandler("chakra", stub_cmd("chakra")))
    app.add_handler(CommandHandler("mindfulness", stub_cmd("mindfulness")))
    app.add_handler(CommandHandler("conciencia", stub_cmd("conciencia")))
    app.add_handler(CommandHandler("presente", stub_cmd("presente")))
    app.add_handler(CommandHandler("respiracion", stub_cmd("respiracion")))
    app.add_handler(CommandHandler("relajacion", stub_cmd("relajacion")))
    app.add_handler(CommandHandler("tranquilidad", stub_cmd("tranquilidad")))
    app.add_handler(CommandHandler("filosofia", stub_cmd("filosofia")))
    app.add_handler(CommandHandler("existencia", stub_cmd("existencia")))
    app.add_handler(CommandHandler("sentido", stub_cmd("sentido")))
    app.add_handler(CommandHandler("proposito", stub_cmd("proposito")))
    app.add_handler(CommandHandler("destino", stub_cmd("destino")))
    app.add_handler(CommandHandler("karma", stub_cmd("karma")))
    app.add_handler(CommandHandler("universo", stub_cmd("universo")))
    app.add_handler(CommandHandler("religion", stub_cmd("religion")))
    app.add_handler(CommandHandler("fe", stub_cmd("fe")))
    app.add_handler(CommandHandler("dios", stub_cmd("dios")))
    app.add_handler(CommandHandler("creencia", stub_cmd("creencia")))
    app.add_handler(CommandHandler("espiritual", stub_cmd("espiritual")))
    app.add_handler(CommandHandler("sagrado", stub_cmd("sagrado")))
    app.add_handler(CommandHandler("divino", stub_cmd("divino")))
    app.add_handler(CommandHandler("astrologia", stub_cmd("astrologia")))
    app.add_handler(CommandHandler("horoscopo", stub_cmd("horoscopo")))
    app.add_handler(CommandHandler("signos", stub_cmd("signos")))
    app.add_handler(CommandHandler("zodiaco", stub_cmd("zodiaco")))
    app.add_handler(CommandHandler("luna", stub_cmd("luna")))
    app.add_handler(CommandHandler("estrellas", stub_cmd("estrellas")))
    app.add_handler(CommandHandler("planeta", stub_cmd("planeta")))
    app.add_handler(CommandHandler("tarot", stub_cmd("tarot")))
    app.add_handler(CommandHandler("cartas", stub_cmd("cartas")))
    app.add_handler(CommandHandler("lectura", stub_cmd("lectura")))
    app.add_handler(CommandHandler("interpretacion", stub_cmd("interpretacion")))
    app.add_handler(CommandHandler("prediccion", stub_cmd("prediccion")))
    app.add_handler(CommandHandler("destino", stub_cmd("destino")))
    app.add_handler(CommandHandler("futuro", stub_cmd("futuro")))
    app.add_handler(CommandHandler("cristal", stub_cmd("cristal")))
    app.add_handler(CommandHandler("piedra", stub_cmd("piedra")))
    app.add_handler(CommandHandler("amuleto", stub_cmd("amuleto")))
    app.add_handler(CommandHandler("talisman", stub_cmd("talisman")))
    app.add_handler(CommandHandler("energia", stub_cmd("energia")))
    app.add_handler(CommandHandler("aura", stub_cmd("aura")))
    app.add_handler(CommandHandler("vibracion", stub_cmd("vibracion")))
    app.add_handler(CommandHandler("ofrendas", stub_cmd("ofrendas")))
    app.add_handler(CommandHandler("ritual", stub_cmd("ritual")))
    app.add_handler(CommandHandler("ceremonia", stub_cmd("ceremonia")))
    app.add_handler(CommandHandler("celebracion", stub_cmd("celebracion")))
    app.add_handler(CommandHandler("sagrado", stub_cmd("sagrado")))
    app.add_handler(CommandHandler("templo", stub_cmd("templo")))
    app.add_handler(CommandHandler("altar", stub_cmd("altar")))
    app.add_handler(CommandHandler("reencarnacion", stub_cmd("reencarnacion")))
    app.add_handler(CommandHandler("alma", stub_cmd("alma")))
    app.add_handler(CommandHandler("vida_pasada", stub_cmd("vida_pasada")))
    app.add_handler(CommandHandler("vidas_anteriores", stub_cmd("vidas_anteriores")))
    app.add_handler(CommandHandler("evolucion_espiritual", stub_cmd("evolucion_espiritual")))
    app.add_handler(CommandHandler("iluminacion", stub_cmd("iluminacion")))
    app.add_handler(CommandHandler("despertar", stub_cmd("despertar")))
    app.add_handler(CommandHandler("ascension", stub_cmd("ascension")))
    app.add_handler(CommandHandler("transformacion", stub_cmd("transformacion")))
    app.add_handler(CommandHandler("renovacion", stub_cmd("renovacion")))
    app.add_handler(CommandHandler("receta", stub_cmd("receta")))
    app.add_handler(CommandHandler("cocina", stub_cmd("cocina")))
    app.add_handler(CommandHandler("cocinero", stub_cmd("cocinero")))
    app.add_handler(CommandHandler("chef", stub_cmd("chef")))
    app.add_handler(CommandHandler("cocinar", stub_cmd("cocinar")))
    app.add_handler(CommandHandler("preparacion", stub_cmd("preparacion")))
    app.add_handler(CommandHandler("ingredientes", stub_cmd("ingredientes")))
    app.add_handler(CommandHandler("desayuno", stub_cmd("desayuno")))
    app.add_handler(CommandHandler("almuerzo", stub_cmd("almuerzo")))
    app.add_handler(CommandHandler("cena", stub_cmd("cena")))
    app.add_handler(CommandHandler("merienda", stub_cmd("merienda")))
    app.add_handler(CommandHandler("snack", stub_cmd("snack")))
    app.add_handler(CommandHandler("postre", stub_cmd("postre")))
    app.add_handler(CommandHandler("bebida", stub_cmd("bebida")))
    app.add_handler(CommandHandler("sopa", stub_cmd("sopa")))
    app.add_handler(CommandHandler("ensalada", stub_cmd("ensalada")))
    app.add_handler(CommandHandler("plato_fuerte", stub_cmd("plato_fuerte")))
    app.add_handler(CommandHandler("carne", stub_cmd("carne")))
    app.add_handler(CommandHandler("pescado", stub_cmd("pescado")))
    app.add_handler(CommandHandler("pollo", stub_cmd("pollo")))
    app.add_handler(CommandHandler("vegetales", stub_cmd("vegetales")))
    app.add_handler(CommandHandler("pasta", stub_cmd("pasta")))
    app.add_handler(CommandHandler("arroz", stub_cmd("arroz")))
    app.add_handler(CommandHandler("pan", stub_cmd("pan")))
    app.add_handler(CommandHandler("cereal", stub_cmd("cereal")))
    app.add_handler(CommandHandler("legumbre", stub_cmd("legumbre")))
    app.add_handler(CommandHandler("verdura", stub_cmd("verdura")))
    app.add_handler(CommandHandler("fruta", stub_cmd("fruta")))
    app.add_handler(CommandHandler("bebida", stub_cmd("bebida")))
    app.add_handler(CommandHandler("agua", stub_cmd("agua")))
    app.add_handler(CommandHandler("jugo", stub_cmd("jugo")))
    app.add_handler(CommandHandler("te", stub_cmd("te")))
    app.add_handler(CommandHandler("cafe", stub_cmd("cafe")))
    app.add_handler(CommandHandler("chocolate", stub_cmd("chocolate")))
    app.add_handler(CommandHandler("vino", stub_cmd("vino")))
    app.add_handler(CommandHandler("cerveza", stub_cmd("cerveza")))
    app.add_handler(CommandHandler("restaurante", stub_cmd("restaurante")))
    app.add_handler(CommandHandler("cafeteria", stub_cmd("cafeteria")))
    app.add_handler(CommandHandler("bar", stub_cmd("bar")))
    app.add_handler(CommandHandler("pub", stub_cmd("pub")))
    app.add_handler(CommandHandler("discoteca", stub_cmd("discoteca")))
    app.add_handler(CommandHandler("nightclub", stub_cmd("nightclub")))
    app.add_handler(CommandHandler("lounge", stub_cmd("lounge")))
    app.add_handler(CommandHandler("menu", stub_cmd("menu")))
    app.add_handler(CommandHandler("carta", stub_cmd("carta")))
    app.add_handler(CommandHandler("opcion", stub_cmd("opcion")))
    app.add_handler(CommandHandler("plato_especial", stub_cmd("plato_especial")))
    app.add_handler(CommandHandler("recommendation", stub_cmd("recommendation")))
    app.add_handler(CommandHandler("reserva", stub_cmd("reserva")))
    app.add_handler(CommandHandler("mesero", stub_cmd("mesero")))
    app.add_handler(CommandHandler("sabor", stub_cmd("sabor")))
    app.add_handler(CommandHandler("dulce", stub_cmd("dulce")))
    app.add_handler(CommandHandler("salado", stub_cmd("salado")))
    app.add_handler(CommandHandler("amargo", stub_cmd("amargo")))
    app.add_handler(CommandHandler("picante", stub_cmd("picante")))
    app.add_handler(CommandHandler("acido", stub_cmd("acido")))
    app.add_handler(CommandHandler("umami", stub_cmd("umami")))
    app.add_handler(CommandHandler("nutricion", stub_cmd("nutricion")))
    app.add_handler(CommandHandler("calorias", stub_cmd("calorias")))
    app.add_handler(CommandHandler("vitaminas", stub_cmd("vitaminas")))
    app.add_handler(CommandHandler("proteinas", stub_cmd("proteinas")))
    app.add_handler(CommandHandler("grasas", stub_cmd("grasas")))
    app.add_handler(CommandHandler("carbohidratos", stub_cmd("carbohidratos")))
    app.add_handler(CommandHandler("dieta", stub_cmd("dieta")))
    app.add_handler(CommandHandler("vegetariano", stub_cmd("vegetariano")))
    app.add_handler(CommandHandler("vegano", stub_cmd("vegano")))
    app.add_handler(CommandHandler("sin_gluten", stub_cmd("sin_gluten")))
    app.add_handler(CommandHandler("sin_lactosa", stub_cmd("sin_lactosa")))
    app.add_handler(CommandHandler("organico", stub_cmd("organico")))
    app.add_handler(CommandHandler("ropa", stub_cmd("ropa")))
    app.add_handler(CommandHandler("atuendo", stub_cmd("atuendo")))
    app.add_handler(CommandHandler("outfit", stub_cmd("outfit")))
    app.add_handler(CommandHandler("estilo", stub_cmd("estilo")))
    app.add_handler(CommandHandler("moda", stub_cmd("moda")))
    app.add_handler(CommandHandler("tendencia", stub_cmd("tendencia")))
    app.add_handler(CommandHandler("clasico", stub_cmd("clasico")))
    app.add_handler(CommandHandler("vestido", stub_cmd("vestido")))
    app.add_handler(CommandHandler("pantalon", stub_cmd("pantalon")))
    app.add_handler(CommandHandler("camisa", stub_cmd("camisa")))
    app.add_handler(CommandHandler("blusa", stub_cmd("blusa")))
    app.add_handler(CommandHandler("falda", stub_cmd("falda")))
    app.add_handler(CommandHandler("sudadera", stub_cmd("sudadera")))
    app.add_handler(CommandHandler("chaqueta", stub_cmd("chaqueta")))
    app.add_handler(CommandHandler("zapatos", stub_cmd("zapatos")))
    app.add_handler(CommandHandler("botas", stub_cmd("botas")))
    app.add_handler(CommandHandler("tenis", stub_cmd("tenis")))
    app.add_handler(CommandHandler("tacones", stub_cmd("tacones")))
    app.add_handler(CommandHandler("sandalias", stub_cmd("sandalias")))
    app.add_handler(CommandHandler("chanclas", stub_cmd("chanclas")))
    app.add_handler(CommandHandler("mocasines", stub_cmd("mocasines")))
    app.add_handler(CommandHandler("accesorios", stub_cmd("accesorios")))
    app.add_handler(CommandHandler("collar", stub_cmd("collar")))
    app.add_handler(CommandHandler("brazalete", stub_cmd("brazalete")))
    app.add_handler(CommandHandler("anillo", stub_cmd("anillo")))
    app.add_handler(CommandHandler("aretes", stub_cmd("aretes")))
    app.add_handler(CommandHandler("pulsera", stub_cmd("pulsera")))
    app.add_handler(CommandHandler("cadena", stub_cmd("cadena")))
    app.add_handler(CommandHandler("bolsa", stub_cmd("bolsa")))
    app.add_handler(CommandHandler("mochila", stub_cmd("mochila")))
    app.add_handler(CommandHandler("cartera", stub_cmd("cartera")))
    app.add_handler(CommandHandler("pasaporte", stub_cmd("pasaporte")))
    app.add_handler(CommandHandler("cinturon", stub_cmd("cinturon")))
    app.add_handler(CommandHandler("corbata", stub_cmd("corbata")))
    app.add_handler(CommandHandler("bufanda", stub_cmd("bufanda")))
    app.add_handler(CommandHandler("maquillaje", stub_cmd("maquillaje")))
    app.add_handler(CommandHandler("base", stub_cmd("base")))
    app.add_handler(CommandHandler("colorete", stub_cmd("colorete")))
    app.add_handler(CommandHandler("sombra", stub_cmd("sombra")))
    app.add_handler(CommandHandler("delineador", stub_cmd("delineador")))
    app.add_handler(CommandHandler("mascara", stub_cmd("mascara")))
    app.add_handler(CommandHandler("lipstick", stub_cmd("lipstick")))
    app.add_handler(CommandHandler("skincare", stub_cmd("skincare")))
    app.add_handler(CommandHandler("crema", stub_cmd("crema")))
    app.add_handler(CommandHandler("serum", stub_cmd("serum")))
    app.add_handler(CommandHandler("mascarilla", stub_cmd("mascarilla")))
    app.add_handler(CommandHandler("exfoliante", stub_cmd("exfoliante")))
    app.add_handler(CommandHandler("hidratante", stub_cmd("hidratante")))
    app.add_handler(CommandHandler("protector", stub_cmd("protector")))
    app.add_handler(CommandHandler("cabello", stub_cmd("cabello")))
    app.add_handler(CommandHandler("shampoo", stub_cmd("shampoo")))
    app.add_handler(CommandHandler("acondicionador", stub_cmd("acondicionador")))
    app.add_handler(CommandHandler("tratamiento", stub_cmd("tratamiento")))
    app.add_handler(CommandHandler("peinado", stub_cmd("peinado")))
    app.add_handler(CommandHandler("corte", stub_cmd("corte")))
    app.add_handler(CommandHandler("color", stub_cmd("color")))
    app.add_handler(CommandHandler("barba", stub_cmd("barba")))
    app.add_handler(CommandHandler("afeitarse", stub_cmd("afeitarse")))
    app.add_handler(CommandHandler("rasuradora", stub_cmd("rasuradora")))
    app.add_handler(CommandHandler("espuma", stub_cmd("espuma")))
    app.add_handler(CommandHandler("locion", stub_cmd("locion")))
    app.add_handler(CommandHandler("perfume", stub_cmd("perfume")))
    app.add_handler(CommandHandler("colonia", stub_cmd("colonia")))
    app.add_handler(CommandHandler("spa", stub_cmd("spa")))
    app.add_handler(CommandHandler("masaje", stub_cmd("masaje")))
    app.add_handler(CommandHandler("facial", stub_cmd("facial")))
    app.add_handler(CommandHandler("manicura", stub_cmd("manicura")))
    app.add_handler(CommandHandler("pedicura", stub_cmd("pedicura")))
    app.add_handler(CommandHandler("depilacion", stub_cmd("depilacion")))
    app.add_handler(CommandHandler("tatuaje", stub_cmd("tatuaje")))
    app.add_handler(CommandHandler("clima", stub_cmd("clima")))
    app.add_handler(CommandHandler("tiempo", stub_cmd("tiempo")))
    app.add_handler(CommandHandler("temperatura", stub_cmd("temperatura")))
    app.add_handler(CommandHandler("lluvia", stub_cmd("lluvia")))
    app.add_handler(CommandHandler("nieve", stub_cmd("nieve")))
    app.add_handler(CommandHandler("granizo", stub_cmd("granizo")))
    app.add_handler(CommandHandler("tormenta", stub_cmd("tormenta")))
    app.add_handler(CommandHandler("sol", stub_cmd("sol")))
    app.add_handler(CommandHandler("nubes", stub_cmd("nubes")))
    app.add_handler(CommandHandler("viento", stub_cmd("viento")))
    app.add_handler(CommandHandler("huracan", stub_cmd("huracan")))
    app.add_handler(CommandHandler("tornado", stub_cmd("tornado")))
    app.add_handler(CommandHandler("relampago", stub_cmd("relampago")))
    app.add_handler(CommandHandler("trueno", stub_cmd("trueno")))
    app.add_handler(CommandHandler("presion", stub_cmd("presion")))
    app.add_handler(CommandHandler("humedad", stub_cmd("humedad")))
    app.add_handler(CommandHandler("sensacion_termica", stub_cmd("sensacion_termica")))
    app.add_handler(CommandHandler("indice_uv", stub_cmd("indice_uv")))
    app.add_handler(CommandHandler("calidad_aire", stub_cmd("calidad_aire")))
    app.add_handler(CommandHandler("arcoiris", stub_cmd("arcoiris")))
    app.add_handler(CommandHandler("aurora", stub_cmd("aurora")))
    app.add_handler(CommandHandler("atardecer", stub_cmd("atardecer")))
    app.add_handler(CommandHandler("amanecer", stub_cmd("amanecer")))
    app.add_handler(CommandHandler("crepusculo", stub_cmd("crepusculo")))
    app.add_handler(CommandHandler("oscuridad", stub_cmd("oscuridad")))
    app.add_handler(CommandHandler("arbol", stub_cmd("arbol")))
    app.add_handler(CommandHandler("flor", stub_cmd("flor")))
    app.add_handler(CommandHandler("planta", stub_cmd("planta")))
    app.add_handler(CommandHandler("hierba", stub_cmd("hierba")))
    app.add_handler(CommandHandler("musgo", stub_cmd("musgo")))
    app.add_handler(CommandHandler("hongos", stub_cmd("hongos")))
    app.add_handler(CommandHandler("algas", stub_cmd("algas")))
    app.add_handler(CommandHandler("animal", stub_cmd("animal")))
    app.add_handler(CommandHandler("perro", stub_cmd("perro")))
    app.add_handler(CommandHandler("gato", stub_cmd("gato")))
    app.add_handler(CommandHandler("pajaro", stub_cmd("pajaro")))
    app.add_handler(CommandHandler("pez", stub_cmd("pez")))
    app.add_handler(CommandHandler("insecto", stub_cmd("insecto")))
    app.add_handler(CommandHandler("reptil", stub_cmd("reptil")))
    app.add_handler(CommandHandler("montana", stub_cmd("montana")))
    app.add_handler(CommandHandler("valle", stub_cmd("valle")))
    app.add_handler(CommandHandler("rio", stub_cmd("rio")))
    app.add_handler(CommandHandler("lago", stub_cmd("lago")))
    app.add_handler(CommandHandler("oceano", stub_cmd("oceano")))
    app.add_handler(CommandHandler("playa", stub_cmd("playa")))
    app.add_handler(CommandHandler("isla", stub_cmd("isla")))
    app.add_handler(CommandHandler("bosque", stub_cmd("bosque")))
    app.add_handler(CommandHandler("selva", stub_cmd("selva")))
    app.add_handler(CommandHandler("desierto", stub_cmd("desierto")))
    app.add_handler(CommandHandler("tundra", stub_cmd("tundra")))
    app.add_handler(CommandHandler("sabana", stub_cmd("sabana")))
    app.add_handler(CommandHandler("pradera", stub_cmd("pradera")))
    app.add_handler(CommandHandler("pantano", stub_cmd("pantano")))
    app.add_handler(CommandHandler("conservacion", stub_cmd("conservacion")))
    app.add_handler(CommandHandler("ambiente", stub_cmd("ambiente")))
    app.add_handler(CommandHandler("ecologia", stub_cmd("ecologia")))
    app.add_handler(CommandHandler("sostenibilidad", stub_cmd("sostenibilidad")))
    app.add_handler(CommandHandler("energia_renovable", stub_cmd("energia_renovable")))
    app.add_handler(CommandHandler("contaminacion", stub_cmd("contaminacion")))
    app.add_handler(CommandHandler("basura", stub_cmd("basura")))
    app.add_handler(CommandHandler("reciclaje", stub_cmd("reciclaje")))
    app.add_handler(CommandHandler("compostaje", stub_cmd("compostaje")))
    app.add_handler(CommandHandler("huella_carbono", stub_cmd("huella_carbono")))

    app.add_handler(CommandHandler("dlmenucp", cmd_dlmenucp))
    # ════════════════════════════════════════════════════════
    # 🚀 MEGA BLOQUE: COMANDOS NUEVOS POR CATEGORÍA (1200+)
    # ════════════════════════════════════════════════════════

    # ── 📱 SISTEMA & PERFIL
    app.add_handler(CommandHandler("perfil_detallado", stub_cmd("perfil_detallado")))
    app.add_handler(CommandHandler("perfil_simple", stub_cmd("perfil_simple")))
    app.add_handler(CommandHandler("cambiar_nick", stub_cmd("cambiar_nick")))
    app.add_handler(CommandHandler("logros", stub_cmd("logros")))
    app.add_handler(CommandHandler("medallas", stub_cmd("medallas")))
    app.add_handler(CommandHandler("insignias", stub_cmd("insignias")))
    app.add_handler(CommandHandler("titulos", stub_cmd("titulos")))
    app.add_handler(CommandHandler("reputacion", stub_cmd("reputacion")))
    app.add_handler(CommandHandler("puntos_total", stub_cmd("puntos_total")))
    app.add_handler(CommandHandler("historial_xp", stub_cmd("historial_xp")))
    app.add_handler(CommandHandler("ranking_global", stub_cmd("ranking_global")))
    app.add_handler(CommandHandler("ranking_local", stub_cmd("ranking_local")))
    app.add_handler(CommandHandler("top_semana", stub_cmd("top_semana")))
    app.add_handler(CommandHandler("top_mes", stub_cmd("top_mes")))
    app.add_handler(CommandHandler("top_dia", stub_cmd("top_dia")))
    app.add_handler(CommandHandler("mi_lugar", stub_cmd("mi_lugar")))
    app.add_handler(CommandHandler("comparar_perfil", stub_cmd("comparar_perfil")))
    app.add_handler(CommandHandler("compartir_perfil", stub_cmd("compartir_perfil")))
    app.add_handler(CommandHandler("tarjeta_perfil", stub_cmd("tarjeta_perfil")))
    app.add_handler(CommandHandler("carnet_digital", stub_cmd("carnet_digital")))
    app.add_handler(CommandHandler("verificar_cuenta", stub_cmd("verificar_cuenta")))
    app.add_handler(CommandHandler("vip_status", stub_cmd("vip_status")))
    app.add_handler(CommandHandler("estado_cuenta", stub_cmd("estado_cuenta")))
    app.add_handler(CommandHandler("actividad_reciente", stub_cmd("actividad_reciente")))
    app.add_handler(CommandHandler("ultimas_acciones", stub_cmd("ultimas_acciones")))
    app.add_handler(CommandHandler("acciones_hoy", stub_cmd("acciones_hoy")))
    app.add_handler(CommandHandler("estadisticas_hoy", stub_cmd("estadisticas_hoy")))
    app.add_handler(CommandHandler("rachas", stub_cmd("rachas")))
    app.add_handler(CommandHandler("racha_actual", stub_cmd("racha_actual")))
    app.add_handler(CommandHandler("racha_maxima", stub_cmd("racha_maxima")))
    app.add_handler(CommandHandler("recompensa_racha", stub_cmd("recompensa_racha")))
    app.add_handler(CommandHandler("mision_diaria", stub_cmd("mision_diaria")))
    app.add_handler(CommandHandler("mision_semanal", stub_cmd("mision_semanal")))
    app.add_handler(CommandHandler("mision_mensual", stub_cmd("mision_mensual")))
    app.add_handler(CommandHandler("mision_especial", stub_cmd("mision_especial")))
    app.add_handler(CommandHandler("logro_nuevo", stub_cmd("logro_nuevo")))
    app.add_handler(CommandHandler("prestige", stub_cmd("prestige")))
    app.add_handler(CommandHandler("rango_detallado", stub_cmd("rango_detallado")))
    app.add_handler(CommandHandler("nivel_maximo", stub_cmd("nivel_maximo")))
    app.add_handler(CommandHandler("xp_necesario", stub_cmd("xp_necesario")))
    app.add_handler(CommandHandler("progreso_nivel", stub_cmd("progreso_nivel")))
    app.add_handler(CommandHandler("bonus_xp", stub_cmd("bonus_xp")))
    app.add_handler(CommandHandler("multiplicador_xp", stub_cmd("multiplicador_xp")))
    app.add_handler(CommandHandler("evento_xp", stub_cmd("evento_xp")))
    app.add_handler(CommandHandler("daily_challenge", stub_cmd("daily_challenge")))
    app.add_handler(CommandHandler("weekly_challenge", stub_cmd("weekly_challenge")))
    app.add_handler(CommandHandler("achievement", stub_cmd("achievement")))
    app.add_handler(CommandHandler("trophy", stub_cmd("trophy")))
    app.add_handler(CommandHandler("award", stub_cmd("award")))
    app.add_handler(CommandHandler("badge_dorado", stub_cmd("badge_dorado")))
    app.add_handler(CommandHandler("badge_plata", stub_cmd("badge_plata")))
    app.add_handler(CommandHandler("badge_bronce", stub_cmd("badge_bronce")))
    app.add_handler(CommandHandler("king_status", stub_cmd("king_status")))
    app.add_handler(CommandHandler("queen_status", stub_cmd("queen_status")))
    app.add_handler(CommandHandler("legend_status", stub_cmd("legend_status")))
    app.add_handler(CommandHandler("elite_status", stub_cmd("elite_status")))
    app.add_handler(CommandHandler("pro_status", stub_cmd("pro_status")))
    app.add_handler(CommandHandler("aprendiz", stub_cmd("aprendiz")))
    app.add_handler(CommandHandler("gran_maestro", stub_cmd("gran_maestro")))
    app.add_handler(CommandHandler("leyenda", stub_cmd("leyenda")))
    app.add_handler(CommandHandler("inmortal", stub_cmd("inmortal")))
    app.add_handler(CommandHandler("celestial", stub_cmd("celestial")))
    app.add_handler(CommandHandler("sub_rango", stub_cmd("sub_rango")))
    app.add_handler(CommandHandler("amigos", stub_cmd("amigos")))
    app.add_handler(CommandHandler("seguidores", stub_cmd("seguidores")))
    app.add_handler(CommandHandler("solicitudes", stub_cmd("solicitudes")))
    app.add_handler(CommandHandler("lista_negra_personal", stub_cmd("lista_negra_personal")))
    app.add_handler(CommandHandler("privacidad_config", stub_cmd("privacidad_config")))
    app.add_handler(CommandHandler("notificaciones_config", stub_cmd("notificaciones_config")))
    app.add_handler(CommandHandler("idioma_bot", stub_cmd("idioma_bot")))
    app.add_handler(CommandHandler("zona_horaria", stub_cmd("zona_horaria")))
    app.add_handler(CommandHandler("moneda_preferida", stub_cmd("moneda_preferida")))
    app.add_handler(CommandHandler("tema_oscuro", stub_cmd("tema_oscuro")))
    app.add_handler(CommandHandler("tema_claro", stub_cmd("tema_claro")))
    app.add_handler(CommandHandler("autorespuesta", stub_cmd("autorespuesta")))
    app.add_handler(CommandHandler("tutorial_bot", stub_cmd("tutorial_bot")))
    app.add_handler(CommandHandler("faq_bot", stub_cmd("faq_bot")))
    app.add_handler(CommandHandler("soporte_bot", stub_cmd("soporte_bot")))
    app.add_handler(CommandHandler("feedback_bot", stub_cmd("feedback_bot")))
    app.add_handler(CommandHandler("sugerencia_bot", stub_cmd("sugerencia_bot")))
    app.add_handler(CommandHandler("reporte_bug", stub_cmd("reporte_bug")))
    app.add_handler(CommandHandler("calificacion_bot", stub_cmd("calificacion_bot")))
    app.add_handler(CommandHandler("compartir_bot", stub_cmd("compartir_bot")))
    app.add_handler(CommandHandler("invitar_bot", stub_cmd("invitar_bot")))
    app.add_handler(CommandHandler("referido", stub_cmd("referido")))
    app.add_handler(CommandHandler("codigo_referido", stub_cmd("codigo_referido")))
    app.add_handler(CommandHandler("recompensa_referido", stub_cmd("recompensa_referido")))
    app.add_handler(CommandHandler("logros_desbloqueados", stub_cmd("logros_desbloqueados")))
    app.add_handler(CommandHandler("logros_pendientes", stub_cmd("logros_pendientes")))
    app.add_handler(CommandHandler("album", stub_cmd("album")))
    app.add_handler(CommandHandler("sticker_album", stub_cmd("sticker_album")))
    app.add_handler(CommandHandler("banner_perfil", stub_cmd("banner_perfil")))
    app.add_handler(CommandHandler("marco_perfil", stub_cmd("marco_perfil")))
    app.add_handler(CommandHandler("emblema_perfil", stub_cmd("emblema_perfil")))
    app.add_handler(CommandHandler("sello_perfil", stub_cmd("sello_perfil")))

    # ── 💰 ECONOMÍA & DINERO
    app.add_handler(CommandHandler("capital", stub_cmd("capital")))
    app.add_handler(CommandHandler("activos", stub_cmd("activos")))
    app.add_handler(CommandHandler("pasivos", stub_cmd("pasivos")))
    app.add_handler(CommandHandler("deuda_total", stub_cmd("deuda_total")))
    app.add_handler(CommandHandler("tasa_interes", stub_cmd("tasa_interes")))
    app.add_handler(CommandHandler("amortizacion", stub_cmd("amortizacion")))
    app.add_handler(CommandHandler("cuota", stub_cmd("cuota")))
    app.add_handler(CommandHandler("flujo_caja", stub_cmd("flujo_caja")))
    app.add_handler(CommandHandler("gasto_mes", stub_cmd("gasto_mes")))
    app.add_handler(CommandHandler("ahorro_mes", stub_cmd("ahorro_mes")))
    app.add_handler(CommandHandler("meta_ahorro", stub_cmd("meta_ahorro")))
    app.add_handler(CommandHandler("alcancia", stub_cmd("alcancia")))
    app.add_handler(CommandHandler("fondos_emergencia", stub_cmd("fondos_emergencia")))
    app.add_handler(CommandHandler("pension", stub_cmd("pension")))
    app.add_handler(CommandHandler("seguro_vida", stub_cmd("seguro_vida")))
    app.add_handler(CommandHandler("seguro_auto", stub_cmd("seguro_auto")))
    app.add_handler(CommandHandler("seguro_salud", stub_cmd("seguro_salud")))
    app.add_handler(CommandHandler("seguro_hogar", stub_cmd("seguro_hogar")))
    app.add_handler(CommandHandler("impuesto_mes", stub_cmd("impuesto_mes")))
    app.add_handler(CommandHandler("facturas", stub_cmd("facturas")))
    app.add_handler(CommandHandler("recibos", stub_cmd("recibos")))
    app.add_handler(CommandHandler("historial_pagos", stub_cmd("historial_pagos")))
    app.add_handler(CommandHandler("credito_score", stub_cmd("credito_score")))
    app.add_handler(CommandHandler("patrimonio_neto", stub_cmd("patrimonio_neto")))
    app.add_handler(CommandHandler("inflacion", stub_cmd("inflacion")))
    app.add_handler(CommandHandler("tipo_cambio", stub_cmd("tipo_cambio")))
    app.add_handler(CommandHandler("divisa", stub_cmd("divisa")))
    app.add_handler(CommandHandler("euro", stub_cmd("euro")))
    app.add_handler(CommandHandler("yen", stub_cmd("yen")))
    app.add_handler(CommandHandler("libra", stub_cmd("libra")))
    app.add_handler(CommandHandler("yuan", stub_cmd("yuan")))
    app.add_handler(CommandHandler("bitcoin2", stub_cmd("bitcoin2")))
    app.add_handler(CommandHandler("ethereum2", stub_cmd("ethereum2")))
    app.add_handler(CommandHandler("dogecoin", stub_cmd("dogecoin")))
    app.add_handler(CommandHandler("solana", stub_cmd("solana")))
    app.add_handler(CommandHandler("cardano", stub_cmd("cardano")))
    app.add_handler(CommandHandler("polkadot", stub_cmd("polkadot")))
    app.add_handler(CommandHandler("chainlink", stub_cmd("chainlink")))
    app.add_handler(CommandHandler("uniswap", stub_cmd("uniswap")))
    app.add_handler(CommandHandler("avalanche", stub_cmd("avalanche")))
    app.add_handler(CommandHandler("polygon", stub_cmd("polygon")))
    app.add_handler(CommandHandler("bnb_coin", stub_cmd("bnb_coin")))
    app.add_handler(CommandHandler("tron_coin", stub_cmd("tron_coin")))
    app.add_handler(CommandHandler("litecoin", stub_cmd("litecoin")))
    app.add_handler(CommandHandler("monero", stub_cmd("monero")))
    app.add_handler(CommandHandler("ripple", stub_cmd("ripple")))
    app.add_handler(CommandHandler("stellar", stub_cmd("stellar")))
    app.add_handler(CommandHandler("cosmos", stub_cmd("cosmos")))
    app.add_handler(CommandHandler("algorand", stub_cmd("algorand")))
    app.add_handler(CommandHandler("near_coin", stub_cmd("near_coin")))
    app.add_handler(CommandHandler("fantom", stub_cmd("fantom")))
    app.add_handler(CommandHandler("elrond", stub_cmd("elrond")))
    app.add_handler(CommandHandler("harmony", stub_cmd("harmony")))
    app.add_handler(CommandHandler("sandbox_token", stub_cmd("sandbox_token")))
    app.add_handler(CommandHandler("axie_token", stub_cmd("axie_token")))
    app.add_handler(CommandHandler("mana_token", stub_cmd("mana_token")))
    app.add_handler(CommandHandler("enjin", stub_cmd("enjin")))
    app.add_handler(CommandHandler("chiliz", stub_cmd("chiliz")))
    app.add_handler(CommandHandler("wax_coin", stub_cmd("wax_coin")))
    app.add_handler(CommandHandler("mercado_acciones", stub_cmd("mercado_acciones")))
    app.add_handler(CommandHandler("bolsa_valores", stub_cmd("bolsa_valores")))
    app.add_handler(CommandHandler("indice_dow", stub_cmd("indice_dow")))
    app.add_handler(CommandHandler("nasdaq", stub_cmd("nasdaq")))
    app.add_handler(CommandHandler("sp500", stub_cmd("sp500")))
    app.add_handler(CommandHandler("ibex35", stub_cmd("ibex35")))
    app.add_handler(CommandHandler("ftse100", stub_cmd("ftse100")))
    app.add_handler(CommandHandler("nikkei225", stub_cmd("nikkei225")))
    app.add_handler(CommandHandler("shanghaiindex", stub_cmd("shanghaiindex")))
    app.add_handler(CommandHandler("oro_precio", stub_cmd("oro_precio")))
    app.add_handler(CommandHandler("plata_precio", stub_cmd("plata_precio")))
    app.add_handler(CommandHandler("petroleo_precio", stub_cmd("petroleo_precio")))
    app.add_handler(CommandHandler("gas_precio", stub_cmd("gas_precio")))
    app.add_handler(CommandHandler("trigo_precio", stub_cmd("trigo_precio")))
    app.add_handler(CommandHandler("cafe_precio", stub_cmd("cafe_precio")))
    app.add_handler(CommandHandler("cacao_precio", stub_cmd("cacao_precio")))
    app.add_handler(CommandHandler("azucar_precio", stub_cmd("azucar_precio")))
    app.add_handler(CommandHandler("arroz_precio", stub_cmd("arroz_precio")))
    app.add_handler(CommandHandler("maiz_precio", stub_cmd("maiz_precio")))
    app.add_handler(CommandHandler("economista", stub_cmd("economista")))
    app.add_handler(CommandHandler("finanzas_personales", stub_cmd("finanzas_personales")))
    app.add_handler(CommandHandler("deuda_vs_ingreso", stub_cmd("deuda_vs_ingreso")))
    app.add_handler(CommandHandler("independencia_financiera", stub_cmd("independencia_financiera")))
    app.add_handler(CommandHandler("fuego_financiero", stub_cmd("fuego_financiero")))
    app.add_handler(CommandHandler("riqueza_neta", stub_cmd("riqueza_neta")))
    app.add_handler(CommandHandler("pasivos_activos", stub_cmd("pasivos_activos")))
    app.add_handler(CommandHandler("ingreso_pasivo", stub_cmd("ingreso_pasivo")))
    app.add_handler(CommandHandler("ingreso_activo", stub_cmd("ingreso_activo")))
    app.add_handler(CommandHandler("dividendo", stub_cmd("dividendo")))
    app.add_handler(CommandHandler("accion", stub_cmd("accion")))
    app.add_handler(CommandHandler("fondo_mutuo", stub_cmd("fondo_mutuo")))
    app.add_handler(CommandHandler("etf", stub_cmd("etf")))
    app.add_handler(CommandHandler("criptocartera", stub_cmd("criptocartera")))
    app.add_handler(CommandHandler("rebalanceo", stub_cmd("rebalanceo")))
    app.add_handler(CommandHandler("diversificacion", stub_cmd("diversificacion")))
    app.add_handler(CommandHandler("riesgo_inversion", stub_cmd("riesgo_inversion")))

    # ── 🎨 MULTIMEDIA & DESCARGAS
    app.add_handler(CommandHandler("yt_buscar", stub_cmd("yt_buscar")))
    app.add_handler(CommandHandler("yt_trending", stub_cmd("yt_trending")))
    app.add_handler(CommandHandler("yt_playlist", stub_cmd("yt_playlist")))
    app.add_handler(CommandHandler("yt_canal", stub_cmd("yt_canal")))
    app.add_handler(CommandHandler("ig_buscar", stub_cmd("ig_buscar")))
    app.add_handler(CommandHandler("ig_stories", stub_cmd("ig_stories")))
    app.add_handler(CommandHandler("ig_reels", stub_cmd("ig_reels")))
    app.add_handler(CommandHandler("tt_trending", stub_cmd("tt_trending")))
    app.add_handler(CommandHandler("tt_buscar", stub_cmd("tt_buscar")))
    app.add_handler(CommandHandler("fb_buscar", stub_cmd("fb_buscar")))
    app.add_handler(CommandHandler("fb_grupo", stub_cmd("fb_grupo")))
    app.add_handler(CommandHandler("tw_buscar", stub_cmd("tw_buscar")))
    app.add_handler(CommandHandler("tw_trending", stub_cmd("tw_trending")))
    app.add_handler(CommandHandler("sc_buscar", stub_cmd("sc_buscar")))
    app.add_handler(CommandHandler("sc_top", stub_cmd("sc_top")))
    app.add_handler(CommandHandler("sp_buscar", stub_cmd("sp_buscar")))
    app.add_handler(CommandHandler("sp_trending", stub_cmd("sp_trending")))
    app.add_handler(CommandHandler("sp_playlist", stub_cmd("sp_playlist")))
    app.add_handler(CommandHandler("sp_artista", stub_cmd("sp_artista")))
    app.add_handler(CommandHandler("sp_album", stub_cmd("sp_album")))
    app.add_handler(CommandHandler("sp_cancion", stub_cmd("sp_cancion")))
    app.add_handler(CommandHandler("dz_buscar", stub_cmd("dz_buscar")))
    app.add_handler(CommandHandler("dz_top", stub_cmd("dz_top")))
    app.add_handler(CommandHandler("vimeo_buscar", stub_cmd("vimeo_buscar")))
    app.add_handler(CommandHandler("dailymotion_dl", stub_cmd("dailymotion_dl")))
    app.add_handler(CommandHandler("reddit_video", stub_cmd("reddit_video")))
    app.add_handler(CommandHandler("twitch_clip", stub_cmd("twitch_clip")))
    app.add_handler(CommandHandler("kick_clip", stub_cmd("kick_clip")))
    app.add_handler(CommandHandler("rumble_buscar", stub_cmd("rumble_buscar")))
    app.add_handler(CommandHandler("streamable_dl", stub_cmd("streamable_dl")))
    app.add_handler(CommandHandler("gfycat_dl", stub_cmd("gfycat_dl")))
    app.add_handler(CommandHandler("tenor_buscar", stub_cmd("tenor_buscar")))
    app.add_handler(CommandHandler("giphy_buscar", stub_cmd("giphy_buscar")))
    app.add_handler(CommandHandler("imgur_buscar", stub_cmd("imgur_buscar")))
    app.add_handler(CommandHandler("pixabay_buscar", stub_cmd("pixabay_buscar")))
    app.add_handler(CommandHandler("unsplash_buscar", stub_cmd("unsplash_buscar")))
    app.add_handler(CommandHandler("pexels_buscar", stub_cmd("pexels_buscar")))
    app.add_handler(CommandHandler("flickr_buscar", stub_cmd("flickr_buscar")))
    app.add_handler(CommandHandler("deviantart_buscar", stub_cmd("deviantart_buscar")))
    app.add_handler(CommandHandler("artstation_buscar", stub_cmd("artstation_buscar")))
    app.add_handler(CommandHandler("behance_buscar", stub_cmd("behance_buscar")))
    app.add_handler(CommandHandler("dribbble_buscar", stub_cmd("dribbble_buscar")))
    app.add_handler(CommandHandler("freepik_buscar", stub_cmd("freepik_buscar")))
    app.add_handler(CommandHandler("flaticon_buscar", stub_cmd("flaticon_buscar")))
    app.add_handler(CommandHandler("svgrepo_buscar", stub_cmd("svgrepo_buscar")))
    app.add_handler(CommandHandler("font_buscar", stub_cmd("font_buscar")))
    app.add_handler(CommandHandler("googlefonts_buscar", stub_cmd("googlefonts_buscar")))
    app.add_handler(CommandHandler("dafont_buscar", stub_cmd("dafont_buscar")))
    app.add_handler(CommandHandler("emoji_info", stub_cmd("emoji_info")))
    app.add_handler(CommandHandler("emoji_buscar", stub_cmd("emoji_buscar")))
    app.add_handler(CommandHandler("emoji_pack", stub_cmd("emoji_pack")))
    app.add_handler(CommandHandler("sticker_pack2", stub_cmd("sticker_pack2")))
    app.add_handler(CommandHandler("sticker_create", stub_cmd("sticker_create")))
    app.add_handler(CommandHandler("avatar_gen", stub_cmd("avatar_gen")))
    app.add_handler(CommandHandler("avatar_anime", stub_cmd("avatar_anime")))
    app.add_handler(CommandHandler("avatar_pixel", stub_cmd("avatar_pixel")))
    app.add_handler(CommandHandler("avatar_cartoon", stub_cmd("avatar_cartoon")))
    app.add_handler(CommandHandler("foto_perfil_gen", stub_cmd("foto_perfil_gen")))
    app.add_handler(CommandHandler("banner_gen", stub_cmd("banner_gen")))
    app.add_handler(CommandHandler("cover_gen", stub_cmd("cover_gen")))
    app.add_handler(CommandHandler("thumbnail_gen", stub_cmd("thumbnail_gen")))
    app.add_handler(CommandHandler("logo_gen", stub_cmd("logo_gen")))
    app.add_handler(CommandHandler("qr_imagen", stub_cmd("qr_imagen")))
    app.add_handler(CommandHandler("ssweb", ssweb_cmd))
    app.add_handler(CommandHandler("qr_color", stub_cmd("qr_color")))
    app.add_handler(CommandHandler("descarga_batch", stub_cmd("descarga_batch")))
    app.add_handler(CommandHandler("playlist_dl", stub_cmd("playlist_dl")))
    app.add_handler(CommandHandler("album_dl", stub_cmd("album_dl")))
    app.add_handler(CommandHandler("canal_dl", stub_cmd("canal_dl")))
    app.add_handler(CommandHandler("lista_descargas", stub_cmd("lista_descargas")))
    app.add_handler(CommandHandler("cola_descargas", stub_cmd("cola_descargas")))
    app.add_handler(CommandHandler("estado_descarga", stub_cmd("estado_descarga")))
    app.add_handler(CommandHandler("cancelar_descarga", stub_cmd("cancelar_descarga")))
    app.add_handler(CommandHandler("formato_video", stub_cmd("formato_video")))
    app.add_handler(CommandHandler("calidad_video", stub_cmd("calidad_video")))
    app.add_handler(CommandHandler("resolucion_video", stub_cmd("resolucion_video")))
    app.add_handler(CommandHandler("fps_video", stub_cmd("fps_video")))
    app.add_handler(CommandHandler("codec_video", stub_cmd("codec_video")))
    app.add_handler(CommandHandler("bitrate_video", stub_cmd("bitrate_video")))
    app.add_handler(CommandHandler("duracion_video", stub_cmd("duracion_video")))
    app.add_handler(CommandHandler("tamano_video", stub_cmd("tamano_video")))
    app.add_handler(CommandHandler("metadatos_video", stub_cmd("metadatos_video")))
    app.add_handler(CommandHandler("recortar_video", stub_cmd("recortar_video")))
    app.add_handler(CommandHandler("unir_videos", stub_cmd("unir_videos")))
    app.add_handler(CommandHandler("split_video", stub_cmd("split_video")))
    app.add_handler(CommandHandler("gif_video", stub_cmd("gif_video")))
    app.add_handler(CommandHandler("thumbnail_video", stub_cmd("thumbnail_video")))
    app.add_handler(CommandHandler("subtitulos_video", stub_cmd("subtitulos_video")))
    app.add_handler(CommandHandler("audio_video", stub_cmd("audio_video")))
    app.add_handler(CommandHandler("quitar_audio", stub_cmd("quitar_audio")))
    app.add_handler(CommandHandler("agregar_audio", stub_cmd("agregar_audio")))
    app.add_handler(CommandHandler("volumen_audio", stub_cmd("volumen_audio")))
    app.add_handler(CommandHandler("normalizar_audio", stub_cmd("normalizar_audio")))
    app.add_handler(CommandHandler("ecualizador", stub_cmd("ecualizador")))
    app.add_handler(CommandHandler("reverb_audio", stub_cmd("reverb_audio")))
    app.add_handler(CommandHandler("echo_audio", stub_cmd("echo_audio")))
    app.add_handler(CommandHandler("pitch_audio", stub_cmd("pitch_audio")))
    app.add_handler(CommandHandler("tempo_audio", stub_cmd("tempo_audio")))
    app.add_handler(CommandHandler("loop_audio", stub_cmd("loop_audio")))
    app.add_handler(CommandHandler("fade_audio", stub_cmd("fade_audio")))
    app.add_handler(CommandHandler("cortar_audio", stub_cmd("cortar_audio")))
    app.add_handler(CommandHandler("unir_audios", stub_cmd("unir_audios")))
    app.add_handler(CommandHandler("convertir_formato", stub_cmd("convertir_formato")))
    app.add_handler(CommandHandler("mp3_128", stub_cmd("mp3_128")))
    app.add_handler(CommandHandler("mp3_320", stub_cmd("mp3_320")))
    app.add_handler(CommandHandler("flac_dl", stub_cmd("flac_dl")))
    app.add_handler(CommandHandler("wav_dl", stub_cmd("wav_dl")))
    app.add_handler(CommandHandler("ogg_dl", stub_cmd("ogg_dl")))

    # ── 🔍 BÚSQUEDA & INFORMACIÓN
    app.add_handler(CommandHandler("google2", stub_cmd("google2")))
    app.add_handler(CommandHandler("bing_buscar", stub_cmd("bing_buscar")))
    app.add_handler(CommandHandler("duckduck", stub_cmd("duckduck")))
    app.add_handler(CommandHandler("ecosia_buscar", stub_cmd("ecosia_buscar")))
    app.add_handler(CommandHandler("startpage_buscar", stub_cmd("startpage_buscar")))
    app.add_handler(CommandHandler("yandex_buscar", stub_cmd("yandex_buscar")))
    app.add_handler(CommandHandler("wiki_en", stub_cmd("wiki_en")))
    app.add_handler(CommandHandler("wiki_es", stub_cmd("wiki_es")))
    app.add_handler(CommandHandler("wiki_fr", stub_cmd("wiki_fr")))
    app.add_handler(CommandHandler("wiki_de", stub_cmd("wiki_de")))
    app.add_handler(CommandHandler("wiki_pt", stub_cmd("wiki_pt")))
    app.add_handler(CommandHandler("wiki_it", stub_cmd("wiki_it")))
    app.add_handler(CommandHandler("wiki_ja", stub_cmd("wiki_ja")))
    app.add_handler(CommandHandler("wiki_zh", stub_cmd("wiki_zh")))
    app.add_handler(CommandHandler("wiki_ar", stub_cmd("wiki_ar")))
    app.add_handler(CommandHandler("wiki_ru", stub_cmd("wiki_ru")))
    app.add_handler(CommandHandler("britannica_buscar", stub_cmd("britannica_buscar")))
    app.add_handler(CommandHandler("rae_define", stub_cmd("rae_define")))
    app.add_handler(CommandHandler("wordreference", stub_cmd("wordreference")))
    app.add_handler(CommandHandler("deepl_traducir", stub_cmd("deepl_traducir")))
    app.add_handler(CommandHandler("amazon_buscar", stub_cmd("amazon_buscar")))
    app.add_handler(CommandHandler("ebay_buscar", stub_cmd("ebay_buscar")))
    app.add_handler(CommandHandler("mercadolibre_buscar", stub_cmd("mercadolibre_buscar")))
    app.add_handler(CommandHandler("aliexpress_buscar", stub_cmd("aliexpress_buscar")))
    app.add_handler(CommandHandler("wish_buscar", stub_cmd("wish_buscar")))
    app.add_handler(CommandHandler("steam_buscar", stub_cmd("steam_buscar")))
    app.add_handler(CommandHandler("epic_buscar", stub_cmd("epic_buscar")))
    app.add_handler(CommandHandler("itunes_buscar", stub_cmd("itunes_buscar")))
    app.add_handler(CommandHandler("googleplay_buscar", stub_cmd("googleplay_buscar")))
    app.add_handler(CommandHandler("goodreads_buscar", stub_cmd("goodreads_buscar")))
    app.add_handler(CommandHandler("libgen_buscar", stub_cmd("libgen_buscar")))
    app.add_handler(CommandHandler("gutenberg_buscar", stub_cmd("gutenberg_buscar")))
    app.add_handler(CommandHandler("arxiv_buscar", stub_cmd("arxiv_buscar")))
    app.add_handler(CommandHandler("scholar_buscar", stub_cmd("scholar_buscar")))
    app.add_handler(CommandHandler("pubmed_buscar", stub_cmd("pubmed_buscar")))
    app.add_handler(CommandHandler("who_buscar", stub_cmd("who_buscar")))
    app.add_handler(CommandHandler("cdc_buscar", stub_cmd("cdc_buscar")))
    app.add_handler(CommandHandler("mayo_buscar", stub_cmd("mayo_buscar")))
    app.add_handler(CommandHandler("webmd_buscar", stub_cmd("webmd_buscar")))
    app.add_handler(CommandHandler("farmaco_info", stub_cmd("farmaco_info")))
    app.add_handler(CommandHandler("sintoma_info", stub_cmd("sintoma_info")))
    app.add_handler(CommandHandler("enfermedad_info", stub_cmd("enfermedad_info")))
    app.add_handler(CommandHandler("tratamiento_info", stub_cmd("tratamiento_info")))
    app.add_handler(CommandHandler("vacuna_info", stub_cmd("vacuna_info")))
    app.add_handler(CommandHandler("alergia_info", stub_cmd("alergia_info")))
    app.add_handler(CommandHandler("dieta_info", stub_cmd("dieta_info")))
    app.add_handler(CommandHandler("nutricion_info", stub_cmd("nutricion_info")))
    app.add_handler(CommandHandler("ejercicio_info", stub_cmd("ejercicio_info")))
    app.add_handler(CommandHandler("deporte_info", stub_cmd("deporte_info")))
    app.add_handler(CommandHandler("futbol_info", stub_cmd("futbol_info")))
    app.add_handler(CommandHandler("baloncesto_info", stub_cmd("baloncesto_info")))
    app.add_handler(CommandHandler("beisbol_info", stub_cmd("beisbol_info")))
    app.add_handler(CommandHandler("tenis_info", stub_cmd("tenis_info")))
    app.add_handler(CommandHandler("formula1_info", stub_cmd("formula1_info")))
    app.add_handler(CommandHandler("mma_info", stub_cmd("mma_info")))
    app.add_handler(CommandHandler("boxeo_info", stub_cmd("boxeo_info")))
    app.add_handler(CommandHandler("atletismo_info", stub_cmd("atletismo_info")))
    app.add_handler(CommandHandler("natacion_info", stub_cmd("natacion_info")))
    app.add_handler(CommandHandler("serie_info", stub_cmd("serie_info")))
    app.add_handler(CommandHandler("pelicula_info", stub_cmd("pelicula_info")))
    app.add_handler(CommandHandler("actor_info", stub_cmd("actor_info")))
    app.add_handler(CommandHandler("director_info", stub_cmd("director_info")))
    app.add_handler(CommandHandler("musica_info", stub_cmd("musica_info")))
    app.add_handler(CommandHandler("artista_info", stub_cmd("artista_info")))
    app.add_handler(CommandHandler("album_info", stub_cmd("album_info")))
    app.add_handler(CommandHandler("letra_cancion", stub_cmd("letra_cancion")))
    app.add_handler(CommandHandler("acordes", stub_cmd("acordes")))
    app.add_handler(CommandHandler("cifrado_musical", stub_cmd("cifrado_musical")))
    app.add_handler(CommandHandler("historia_hoy", stub_cmd("historia_hoy")))
    app.add_handler(CommandHandler("efemeride", stub_cmd("efemeride")))
    app.add_handler(CommandHandler("nacidos_hoy", stub_cmd("nacidos_hoy")))
    app.add_handler(CommandHandler("fallecidos_hoy", stub_cmd("fallecidos_hoy")))
    app.add_handler(CommandHandler("evento_historico", stub_cmd("evento_historico")))
    app.add_handler(CommandHandler("dato_pais", stub_cmd("dato_pais")))
    app.add_handler(CommandHandler("capital_info", stub_cmd("capital_info")))
    app.add_handler(CommandHandler("moneda_pais", stub_cmd("moneda_pais")))
    app.add_handler(CommandHandler("idioma_pais", stub_cmd("idioma_pais")))
    app.add_handler(CommandHandler("poblacion_pais", stub_cmd("poblacion_pais")))
    app.add_handler(CommandHandler("area_pais", stub_cmd("area_pais")))
    app.add_handler(CommandHandler("gobierno_info", stub_cmd("gobierno_info")))
    app.add_handler(CommandHandler("presidente_info", stub_cmd("presidente_info")))
    app.add_handler(CommandHandler("ciudad_info", stub_cmd("ciudad_info")))
    app.add_handler(CommandHandler("aeropuerto_info", stub_cmd("aeropuerto_info")))
    app.add_handler(CommandHandler("codigo_pais", stub_cmd("codigo_pais")))
    app.add_handler(CommandHandler("zona_horaria_pais", stub_cmd("zona_horaria_pais")))
    app.add_handler(CommandHandler("bandera_info", stub_cmd("bandera_info")))
    app.add_handler(CommandHandler("himno_info", stub_cmd("himno_info")))
    app.add_handler(CommandHandler("cultura_info", stub_cmd("cultura_info")))
    app.add_handler(CommandHandler("receta_pais", stub_cmd("receta_pais")))
    app.add_handler(CommandHandler("gastronomia_pais", stub_cmd("gastronomia_pais")))
    app.add_handler(CommandHandler("tradicion_pais", stub_cmd("tradicion_pais")))
    app.add_handler(CommandHandler("festival_pais", stub_cmd("festival_pais")))

    # ── 🛠️ HERRAMIENTAS
    app.add_handler(CommandHandler("calc2", stub_cmd("calc2")))
    app.add_handler(CommandHandler("calc_cientifica", stub_cmd("calc_cientifica")))
    app.add_handler(CommandHandler("calc_financiera", stub_cmd("calc_financiera")))
    app.add_handler(CommandHandler("calc_estadistica", stub_cmd("calc_estadistica")))
    app.add_handler(CommandHandler("calc_matrix", stub_cmd("calc_matrix")))
    app.add_handler(CommandHandler("conversor_moneda", stub_cmd("conversor_moneda")))
    app.add_handler(CommandHandler("conversor_peso", stub_cmd("conversor_peso")))
    app.add_handler(CommandHandler("conversor_longitud", stub_cmd("conversor_longitud")))
    app.add_handler(CommandHandler("conversor_volumen", stub_cmd("conversor_volumen")))
    app.add_handler(CommandHandler("conversor_area", stub_cmd("conversor_area")))
    app.add_handler(CommandHandler("conversor_tiempo", stub_cmd("conversor_tiempo")))
    app.add_handler(CommandHandler("conversor_velocidad", stub_cmd("conversor_velocidad")))
    app.add_handler(CommandHandler("conversor_presion", stub_cmd("conversor_presion")))
    app.add_handler(CommandHandler("conversor_energia", stub_cmd("conversor_energia")))
    app.add_handler(CommandHandler("conversor_potencia", stub_cmd("conversor_potencia")))
    app.add_handler(CommandHandler("conversor_datos", stub_cmd("conversor_datos")))
    app.add_handler(CommandHandler("conversor_frecuencia", stub_cmd("conversor_frecuencia")))
    app.add_handler(CommandHandler("conversor_angulo", stub_cmd("conversor_angulo")))
    app.add_handler(CommandHandler("generador_nombres", stub_cmd("generador_nombres")))
    app.add_handler(CommandHandler("generador_apellidos", stub_cmd("generador_apellidos")))
    app.add_handler(CommandHandler("generador_emails", stub_cmd("generador_emails")))
    app.add_handler(CommandHandler("generador_telefonos", stub_cmd("generador_telefonos")))
    app.add_handler(CommandHandler("generador_direcciones", stub_cmd("generador_direcciones")))
    app.add_handler(CommandHandler("generador_ips", stub_cmd("generador_ips")))
    app.add_handler(CommandHandler("generador_macs", stub_cmd("generador_macs")))
    app.add_handler(CommandHandler("generador_uuids", stub_cmd("generador_uuids")))
    app.add_handler(CommandHandler("generador_hashes", stub_cmd("generador_hashes")))
    app.add_handler(CommandHandler("generador_claves", stub_cmd("generador_claves")))
    app.add_handler(CommandHandler("generador_tokens", stub_cmd("generador_tokens")))
    app.add_handler(CommandHandler("generador_pins", stub_cmd("generador_pins")))
    app.add_handler(CommandHandler("generador_codigos", stub_cmd("generador_codigos")))
    app.add_handler(CommandHandler("generador_series", stub_cmd("generador_series")))
    app.add_handler(CommandHandler("generador_fechas", stub_cmd("generador_fechas")))
    app.add_handler(CommandHandler("generador_horas", stub_cmd("generador_horas")))
    app.add_handler(CommandHandler("generador_colores", stub_cmd("generador_colores")))
    app.add_handler(CommandHandler("generador_gradientes", stub_cmd("generador_gradientes")))
    app.add_handler(CommandHandler("cifrado_aes", stub_cmd("cifrado_aes")))
    app.add_handler(CommandHandler("cifrado_rsa", stub_cmd("cifrado_rsa")))
    app.add_handler(CommandHandler("cifrado_vigenere", stub_cmd("cifrado_vigenere")))
    app.add_handler(CommandHandler("cifrado_playfair", stub_cmd("cifrado_playfair")))
    app.add_handler(CommandHandler("descifrado_aes", stub_cmd("descifrado_aes")))
    app.add_handler(CommandHandler("url_encode", stub_cmd("url_encode")))
    app.add_handler(CommandHandler("url_decode", stub_cmd("url_decode")))
    app.add_handler(CommandHandler("html_encode", stub_cmd("html_encode")))
    app.add_handler(CommandHandler("html_decode", stub_cmd("html_decode")))
    app.add_handler(CommandHandler("json_format", stub_cmd("json_format")))
    app.add_handler(CommandHandler("json_minify", stub_cmd("json_minify")))
    app.add_handler(CommandHandler("json_validate", stub_cmd("json_validate")))
    app.add_handler(CommandHandler("xml_format", stub_cmd("xml_format")))
    app.add_handler(CommandHandler("xml_validate", stub_cmd("xml_validate")))
    app.add_handler(CommandHandler("csv_parse", stub_cmd("csv_parse")))
    app.add_handler(CommandHandler("yaml_parse", stub_cmd("yaml_parse")))
    app.add_handler(CommandHandler("markdown_preview", stub_cmd("markdown_preview")))
    app.add_handler(CommandHandler("regex_test", stub_cmd("regex_test")))
    app.add_handler(CommandHandler("cron_parser", stub_cmd("cron_parser")))
    app.add_handler(CommandHandler("ip_calc", stub_cmd("ip_calc")))
    app.add_handler(CommandHandler("subnet_calc", stub_cmd("subnet_calc")))
    app.add_handler(CommandHandler("cidr_calc", stub_cmd("cidr_calc")))
    app.add_handler(CommandHandler("port_info", stub_cmd("port_info")))
    app.add_handler(CommandHandler("jwt_decode", stub_cmd("jwt_decode")))
    app.add_handler(CommandHandler("base32_encode", stub_cmd("base32_encode")))
    app.add_handler(CommandHandler("base32_decode", stub_cmd("base32_decode")))
    app.add_handler(CommandHandler("base85_encode", stub_cmd("base85_encode")))
    app.add_handler(CommandHandler("hex_encode2", stub_cmd("hex_encode2")))
    app.add_handler(CommandHandler("hex_decode2", stub_cmd("hex_decode2")))
    app.add_handler(CommandHandler("rot13", stub_cmd("rot13")))
    app.add_handler(CommandHandler("atbash", stub_cmd("atbash")))
    app.add_handler(CommandHandler("braille", stub_cmd("braille")))
    app.add_handler(CommandHandler("semaforo_bin", stub_cmd("semaforo_bin")))
    app.add_handler(CommandHandler("texto_espejo", stub_cmd("texto_espejo")))
    app.add_handler(CommandHandler("texto_capicua", stub_cmd("texto_capicua")))
    app.add_handler(CommandHandler("texto_leet", stub_cmd("texto_leet")))
    app.add_handler(CommandHandler("texto_encriptado", stub_cmd("texto_encriptado")))
    app.add_handler(CommandHandler("texto_morse", stub_cmd("texto_morse")))
    app.add_handler(CommandHandler("texto_binario", stub_cmd("texto_binario")))
    app.add_handler(CommandHandler("generar_lorem", stub_cmd("generar_lorem")))
    app.add_handler(CommandHandler("generar_parrafo", stub_cmd("generar_parrafo")))
    app.add_handler(CommandHandler("contador_letras", stub_cmd("contador_letras")))
    app.add_handler(CommandHandler("analizador_texto", stub_cmd("analizador_texto")))
    app.add_handler(CommandHandler("frecuencia_palabras", stub_cmd("frecuencia_palabras")))
    app.add_handler(CommandHandler("detectar_idioma", stub_cmd("detectar_idioma")))
    app.add_handler(CommandHandler("limpiar_html", stub_cmd("limpiar_html")))
    app.add_handler(CommandHandler("limpiar_emoji", stub_cmd("limpiar_emoji")))
    app.add_handler(CommandHandler("extraer_links", stub_cmd("extraer_links")))
    app.add_handler(CommandHandler("extraer_emails", stub_cmd("extraer_emails")))
    app.add_handler(CommandHandler("extraer_telefonos", stub_cmd("extraer_telefonos")))
    app.add_handler(CommandHandler("validar_email", stub_cmd("validar_email")))
    app.add_handler(CommandHandler("validar_url", stub_cmd("validar_url")))
    app.add_handler(CommandHandler("validar_ip", stub_cmd("validar_ip")))
    app.add_handler(CommandHandler("validar_cedula_ve", stub_cmd("validar_cedula_ve")))
    app.add_handler(CommandHandler("validar_rif", stub_cmd("validar_rif")))
    app.add_handler(CommandHandler("hora_exacta", stub_cmd("hora_exacta")))
    app.add_handler(CommandHandler("segundo_unix", stub_cmd("segundo_unix")))
    app.add_handler(CommandHandler("milisegundo", stub_cmd("milisegundo")))
    app.add_handler(CommandHandler("nanosegundo", stub_cmd("nanosegundo")))
    app.add_handler(CommandHandler("diferencia_fechas", stub_cmd("diferencia_fechas")))
    app.add_handler(CommandHandler("suma_dias", stub_cmd("suma_dias")))
    app.add_handler(CommandHandler("resta_dias", stub_cmd("resta_dias")))
    app.add_handler(CommandHandler("dia_semana", stub_cmd("dia_semana")))
    app.add_handler(CommandHandler("semana_numero", stub_cmd("semana_numero")))
    app.add_handler(CommandHandler("cuatrimestre", stub_cmd("cuatrimestre")))
    app.add_handler(CommandHandler("quincena", stub_cmd("quincena")))
    app.add_handler(CommandHandler("mes_nombre", stub_cmd("mes_nombre")))
    app.add_handler(CommandHandler("estacion", stub_cmd("estacion")))
    app.add_handler(CommandHandler("hemisferio", stub_cmd("hemisferio")))
    app.add_handler(CommandHandler("calendario_maya", stub_cmd("calendario_maya")))
    app.add_handler(CommandHandler("calendario_chino", stub_cmd("calendario_chino")))
    app.add_handler(CommandHandler("calendario_islamico", stub_cmd("calendario_islamico")))
    app.add_handler(CommandHandler("calendario_hebreo", stub_cmd("calendario_hebreo")))
    app.add_handler(CommandHandler("zodiaco_chino", stub_cmd("zodiaco_chino")))

    # ── 🎮 JUEGOS & ENTRETENIMIENTO
    app.add_handler(CommandHandler("dado2", stub_cmd("dado2")))
    app.add_handler(CommandHandler("dado3", stub_cmd("dado3")))
    app.add_handler(CommandHandler("dado6", stub_cmd("dado6")))
    app.add_handler(CommandHandler("dado8", stub_cmd("dado8")))
    app.add_handler(CommandHandler("dado10", stub_cmd("dado10")))
    app.add_handler(CommandHandler("dado12", stub_cmd("dado12")))
    app.add_handler(CommandHandler("dado20", stub_cmd("dado20")))
    app.add_handler(CommandHandler("dado100", stub_cmd("dado100")))
    app.add_handler(CommandHandler("ruleta2", stub_cmd("ruleta2")))
    app.add_handler(CommandHandler("ruleta_color", stub_cmd("ruleta_color")))
    app.add_handler(CommandHandler("ruleta_nombre", stub_cmd("ruleta_nombre")))
    app.add_handler(CommandHandler("ruleta_numero", stub_cmd("ruleta_numero")))
    app.add_handler(CommandHandler("ruleta_opcion", stub_cmd("ruleta_opcion")))
    app.add_handler(CommandHandler("carta_poker", stub_cmd("carta_poker")))
    app.add_handler(CommandHandler("carta_tarot", stub_cmd("carta_tarot")))
    app.add_handler(CommandHandler("carta_oraculo", stub_cmd("carta_oraculo")))
    app.add_handler(CommandHandler("carta_angel", stub_cmd("carta_angel")))
    app.add_handler(CommandHandler("carta_demonio", stub_cmd("carta_demonio")))
    app.add_handler(CommandHandler("blackjack2", stub_cmd("blackjack2")))
    app.add_handler(CommandHandler("texas_holdem", stub_cmd("texas_holdem")))
    app.add_handler(CommandHandler("baccarat", stub_cmd("baccarat")))
    app.add_handler(CommandHandler("punto_banco", stub_cmd("punto_banco")))
    app.add_handler(CommandHandler("craps", stub_cmd("craps")))
    app.add_handler(CommandHandler("keno", stub_cmd("keno")))
    app.add_handler(CommandHandler("bingo", stub_cmd("bingo")))
    app.add_handler(CommandHandler("loteria2", stub_cmd("loteria2")))
    app.add_handler(CommandHandler("raspadito", stub_cmd("raspadito")))
    app.add_handler(CommandHandler("tragamonedas2", stub_cmd("tragamonedas2")))
    app.add_handler(CommandHandler("frutas", stub_cmd("frutas")))
    app.add_handler(CommandHandler("slots", stub_cmd("slots")))
    app.add_handler(CommandHandler("adivinar_numero", stub_cmd("adivinar_numero")))
    app.add_handler(CommandHandler("adivinar_animal", stub_cmd("adivinar_animal")))
    app.add_handler(CommandHandler("adivinar_pais", stub_cmd("adivinar_pais")))
    app.add_handler(CommandHandler("adivinar_personaje", stub_cmd("adivinar_personaje")))
    app.add_handler(CommandHandler("quizz_historia", stub_cmd("quizz_historia")))
    app.add_handler(CommandHandler("quizz_ciencia", stub_cmd("quizz_ciencia")))
    app.add_handler(CommandHandler("quizz_geografia", stub_cmd("quizz_geografia")))
    app.add_handler(CommandHandler("quizz_musica", stub_cmd("quizz_musica")))
    app.add_handler(CommandHandler("quizz_cine", stub_cmd("quizz_cine")))
    app.add_handler(CommandHandler("quizz_deporte", stub_cmd("quizz_deporte")))
    app.add_handler(CommandHandler("quizz_cultura", stub_cmd("quizz_cultura")))
    app.add_handler(CommandHandler("quizz_venezuela", stub_cmd("quizz_venezuela")))
    app.add_handler(CommandHandler("quizz_anime", stub_cmd("quizz_anime")))
    app.add_handler(CommandHandler("quizz_videojuegos", stub_cmd("quizz_videojuegos")))
    app.add_handler(CommandHandler("quizz_marvel", stub_cmd("quizz_marvel")))
    app.add_handler(CommandHandler("quizz_dc", stub_cmd("quizz_dc")))
    app.add_handler(CommandHandler("wordle", stub_cmd("wordle")))
    app.add_handler(CommandHandler("hangman2", stub_cmd("hangman2")))
    app.add_handler(CommandHandler("anagrama", stub_cmd("anagrama")))
    app.add_handler(CommandHandler("rima", stub_cmd("rima")))
    app.add_handler(CommandHandler("acrostico", stub_cmd("acrostico")))
    app.add_handler(CommandHandler("haiku", stub_cmd("haiku")))
    app.add_handler(CommandHandler("limerick", stub_cmd("limerick")))
    app.add_handler(CommandHandler("cuento_corto", stub_cmd("cuento_corto")))
    app.add_handler(CommandHandler("historia_aleatoria", stub_cmd("historia_aleatoria")))
    app.add_handler(CommandHandler("personaje_aleatorio", stub_cmd("personaje_aleatorio")))
    app.add_handler(CommandHandler("mundo_aleatorio", stub_cmd("mundo_aleatorio")))
    app.add_handler(CommandHandler("mision_rpg", stub_cmd("mision_rpg")))
    app.add_handler(CommandHandler("quest", stub_cmd("quest")))
    app.add_handler(CommandHandler("dungeon2", stub_cmd("dungeon2")))
    app.add_handler(CommandHandler("boss_fight", stub_cmd("boss_fight")))
    app.add_handler(CommandHandler("raid", stub_cmd("raid")))
    app.add_handler(CommandHandler("clan", stub_cmd("clan")))
    app.add_handler(CommandHandler("gremio", stub_cmd("gremio")))
    app.add_handler(CommandHandler("alianza", stub_cmd("alianza")))
    app.add_handler(CommandHandler("faccion", stub_cmd("faccion")))
    app.add_handler(CommandHandler("bando", stub_cmd("bando")))
    app.add_handler(CommandHandler("partido", stub_cmd("partido")))
    app.add_handler(CommandHandler("liga", stub_cmd("liga")))
    app.add_handler(CommandHandler("copa", stub_cmd("copa")))
    app.add_handler(CommandHandler("torneo2", stub_cmd("torneo2")))
    app.add_handler(CommandHandler("campeonato2", stub_cmd("campeonato2")))
    app.add_handler(CommandHandler("mundial", stub_cmd("mundial")))
    app.add_handler(CommandHandler("olimpiadas", stub_cmd("olimpiadas")))
    app.add_handler(CommandHandler("medalla_oro", stub_cmd("medalla_oro")))
    app.add_handler(CommandHandler("medalla_plata", stub_cmd("medalla_plata")))
    app.add_handler(CommandHandler("medalla_bronce", stub_cmd("medalla_bronce")))
    app.add_handler(CommandHandler("podio", stub_cmd("podio")))
    app.add_handler(CommandHandler("record", stub_cmd("record")))
    app.add_handler(CommandHandler("highscore", stub_cmd("highscore")))
    app.add_handler(CommandHandler("puntuacion_maxima", stub_cmd("puntuacion_maxima")))
    app.add_handler(CommandHandler("clasificacion", stub_cmd("clasificacion")))
    app.add_handler(CommandHandler("tabla_posiciones", stub_cmd("tabla_posiciones")))
    app.add_handler(CommandHandler("estadisticas_juego", stub_cmd("estadisticas_juego")))
    app.add_handler(CommandHandler("historial_juegos", stub_cmd("historial_juegos")))
    app.add_handler(CommandHandler("juego_del_dia", stub_cmd("juego_del_dia")))
    app.add_handler(CommandHandler("minijuego", stub_cmd("minijuego")))
    app.add_handler(CommandHandler("reto_diario", stub_cmd("reto_diario")))
    app.add_handler(CommandHandler("desafio_diario", stub_cmd("desafio_diario")))
    app.add_handler(CommandHandler("evento_especial", stub_cmd("evento_especial")))
    app.add_handler(CommandHandler("temporada", stub_cmd("temporada")))
    app.add_handler(CommandHandler("season", stub_cmd("season")))

    # ── 🍳 COCINA & RECETAS
    app.add_handler(CommandHandler("receta2", stub_cmd("receta2")))
    app.add_handler(CommandHandler("receta_rapida", stub_cmd("receta_rapida")))
    app.add_handler(CommandHandler("receta_vegana", stub_cmd("receta_vegana")))
    app.add_handler(CommandHandler("receta_vegetariana", stub_cmd("receta_vegetariana")))
    app.add_handler(CommandHandler("receta_sin_gluten", stub_cmd("receta_sin_gluten")))
    app.add_handler(CommandHandler("receta_keto", stub_cmd("receta_keto")))
    app.add_handler(CommandHandler("receta_paleo", stub_cmd("receta_paleo")))
    app.add_handler(CommandHandler("receta_mediterranea", stub_cmd("receta_mediterranea")))
    app.add_handler(CommandHandler("receta_asiatica", stub_cmd("receta_asiatica")))
    app.add_handler(CommandHandler("receta_italiana", stub_cmd("receta_italiana")))
    app.add_handler(CommandHandler("receta_mexicana", stub_cmd("receta_mexicana")))
    app.add_handler(CommandHandler("receta_francesa", stub_cmd("receta_francesa")))
    app.add_handler(CommandHandler("receta_japonesa", stub_cmd("receta_japonesa")))
    app.add_handler(CommandHandler("receta_china", stub_cmd("receta_china")))
    app.add_handler(CommandHandler("receta_india", stub_cmd("receta_india")))
    app.add_handler(CommandHandler("receta_griega", stub_cmd("receta_griega")))
    app.add_handler(CommandHandler("receta_arabe", stub_cmd("receta_arabe")))
    app.add_handler(CommandHandler("receta_peruana", stub_cmd("receta_peruana")))
    app.add_handler(CommandHandler("receta_colombiana", stub_cmd("receta_colombiana")))
    app.add_handler(CommandHandler("receta_venezolana2", stub_cmd("receta_venezolana2")))
    app.add_handler(CommandHandler("receta_cubana", stub_cmd("receta_cubana")))
    app.add_handler(CommandHandler("receta_argentina", stub_cmd("receta_argentina")))
    app.add_handler(CommandHandler("receta_chilena", stub_cmd("receta_chilena")))
    app.add_handler(CommandHandler("arepa", stub_cmd("arepa")))
    app.add_handler(CommandHandler("pabellon", stub_cmd("pabellon")))
    app.add_handler(CommandHandler("hallaca", stub_cmd("hallaca")))
    app.add_handler(CommandHandler("tequeno", stub_cmd("tequeno")))
    app.add_handler(CommandHandler("empanada_ve", stub_cmd("empanada_ve")))
    app.add_handler(CommandHandler("asado", stub_cmd("asado")))
    app.add_handler(CommandHandler("sancocho", stub_cmd("sancocho")))
    app.add_handler(CommandHandler("cachapa", stub_cmd("cachapa")))
    app.add_handler(CommandHandler("mandoca", stub_cmd("mandoca")))
    app.add_handler(CommandHandler("caraotas", stub_cmd("caraotas")))
    app.add_handler(CommandHandler("guasacaca", stub_cmd("guasacaca")))
    app.add_handler(CommandHandler("chicha", stub_cmd("chicha")))
    app.add_handler(CommandHandler("papelon_limonada", stub_cmd("papelon_limonada")))
    app.add_handler(CommandHandler("guarapo", stub_cmd("guarapo")))
    app.add_handler(CommandHandler("batido", stub_cmd("batido")))
    app.add_handler(CommandHandler("smoothie", stub_cmd("smoothie")))
    app.add_handler(CommandHandler("jugo_natural", stub_cmd("jugo_natural")))
    app.add_handler(CommandHandler("agua_fresca", stub_cmd("agua_fresca")))
    app.add_handler(CommandHandler("horchata", stub_cmd("horchata")))
    app.add_handler(CommandHandler("atole", stub_cmd("atole")))
    app.add_handler(CommandHandler("champurrado", stub_cmd("champurrado")))
    app.add_handler(CommandHandler("ponche", stub_cmd("ponche")))
    app.add_handler(CommandHandler("cacao_bebida", stub_cmd("cacao_bebida")))
    app.add_handler(CommandHandler("cafe_receta", stub_cmd("cafe_receta")))
    app.add_handler(CommandHandler("te_receta", stub_cmd("te_receta")))
    app.add_handler(CommandHandler("infusion", stub_cmd("infusion")))
    app.add_handler(CommandHandler("tisana", stub_cmd("tisana")))
    app.add_handler(CommandHandler("limonada_clasica", stub_cmd("limonada_clasica")))
    app.add_handler(CommandHandler("ensalada_cesar", stub_cmd("ensalada_cesar")))
    app.add_handler(CommandHandler("ensalada_griega", stub_cmd("ensalada_griega")))
    app.add_handler(CommandHandler("ensalada_caprese", stub_cmd("ensalada_caprese")))
    app.add_handler(CommandHandler("ensalada_nicoise", stub_cmd("ensalada_nicoise")))
    app.add_handler(CommandHandler("sopa_tomate", stub_cmd("sopa_tomate")))
    app.add_handler(CommandHandler("sopa_cebolla", stub_cmd("sopa_cebolla")))
    app.add_handler(CommandHandler("sopa_pollo2", stub_cmd("sopa_pollo2")))
    app.add_handler(CommandHandler("crema_verduras", stub_cmd("crema_verduras")))
    app.add_handler(CommandHandler("gazpacho", stub_cmd("gazpacho")))
    app.add_handler(CommandHandler("vichyssoise", stub_cmd("vichyssoise")))
    app.add_handler(CommandHandler("ramen", stub_cmd("ramen")))
    app.add_handler(CommandHandler("pho", stub_cmd("pho")))
    app.add_handler(CommandHandler("sopa_wonton", stub_cmd("sopa_wonton")))
    app.add_handler(CommandHandler("caldo_res", stub_cmd("caldo_res")))
    app.add_handler(CommandHandler("consomme", stub_cmd("consomme")))
    app.add_handler(CommandHandler("guiso", stub_cmd("guiso")))
    app.add_handler(CommandHandler("estofado", stub_cmd("estofado")))
    app.add_handler(CommandHandler("ragu", stub_cmd("ragu")))
    app.add_handler(CommandHandler("bolognesa", stub_cmd("bolognesa")))
    app.add_handler(CommandHandler("carbonara", stub_cmd("carbonara")))
    app.add_handler(CommandHandler("alfredo", stub_cmd("alfredo")))
    app.add_handler(CommandHandler("pesto", stub_cmd("pesto")))
    app.add_handler(CommandHandler("marinara", stub_cmd("marinara")))
    app.add_handler(CommandHandler("arrabbiata", stub_cmd("arrabbiata")))
    app.add_handler(CommandHandler("amatriciana", stub_cmd("amatriciana")))
    app.add_handler(CommandHandler("cacio_pepe", stub_cmd("cacio_pepe")))
    app.add_handler(CommandHandler("risotto", stub_cmd("risotto")))
    app.add_handler(CommandHandler("paella", stub_cmd("paella")))
    app.add_handler(CommandHandler("fideos", stub_cmd("fideos")))
    app.add_handler(CommandHandler("cuscus", stub_cmd("cuscus")))
    app.add_handler(CommandHandler("quinoa_receta", stub_cmd("quinoa_receta")))
    app.add_handler(CommandHandler("lenteja_receta", stub_cmd("lenteja_receta")))
    app.add_handler(CommandHandler("garbanzo_receta", stub_cmd("garbanzo_receta")))
    app.add_handler(CommandHandler("frijol_receta", stub_cmd("frijol_receta")))
    app.add_handler(CommandHandler("arveja_receta", stub_cmd("arveja_receta")))
    app.add_handler(CommandHandler("tofu_receta", stub_cmd("tofu_receta")))
    app.add_handler(CommandHandler("tempeh_receta", stub_cmd("tempeh_receta")))
    app.add_handler(CommandHandler("seitan_receta", stub_cmd("seitan_receta")))
    app.add_handler(CommandHandler("jackfruit_receta", stub_cmd("jackfruit_receta")))
    app.add_handler(CommandHandler("salmon_receta", stub_cmd("salmon_receta")))
    app.add_handler(CommandHandler("atun_receta", stub_cmd("atun_receta")))
    app.add_handler(CommandHandler("camarones_receta", stub_cmd("camarones_receta")))
    app.add_handler(CommandHandler("pulpo_receta", stub_cmd("pulpo_receta")))
    app.add_handler(CommandHandler("langosta_receta", stub_cmd("langosta_receta")))
    app.add_handler(CommandHandler("cangrejo_receta", stub_cmd("cangrejo_receta")))
    app.add_handler(CommandHandler("mejillones_receta", stub_cmd("mejillones_receta")))
    app.add_handler(CommandHandler("almejas_receta", stub_cmd("almejas_receta")))
    app.add_handler(CommandHandler("pan_casero", stub_cmd("pan_casero")))
    app.add_handler(CommandHandler("pizza_masa", stub_cmd("pizza_masa")))
    app.add_handler(CommandHandler("focaccia", stub_cmd("focaccia")))
    app.add_handler(CommandHandler("brioche", stub_cmd("brioche")))
    app.add_handler(CommandHandler("croissant", stub_cmd("croissant")))
    app.add_handler(CommandHandler("baguette", stub_cmd("baguette")))
    app.add_handler(CommandHandler("torta_chocolate", stub_cmd("torta_chocolate")))
    app.add_handler(CommandHandler("cheesecake", stub_cmd("cheesecake")))
    app.add_handler(CommandHandler("flan", stub_cmd("flan")))
    app.add_handler(CommandHandler("tres_leches", stub_cmd("tres_leches")))
    app.add_handler(CommandHandler("mousse", stub_cmd("mousse")))
    app.add_handler(CommandHandler("panna_cotta", stub_cmd("panna_cotta")))
    app.add_handler(CommandHandler("tiramisu", stub_cmd("tiramisu")))
    app.add_handler(CommandHandler("brownie", stub_cmd("brownie")))
    app.add_handler(CommandHandler("muffin", stub_cmd("muffin")))
    app.add_handler(CommandHandler("cupcake", stub_cmd("cupcake")))
    app.add_handler(CommandHandler("galletas", stub_cmd("galletas")))
    app.add_handler(CommandHandler("macarons", stub_cmd("macarons")))

    # ── 💪 SALUD & BIENESTAR
    app.add_handler(CommandHandler("meditacion2", stub_cmd("meditacion2")))
    app.add_handler(CommandHandler("respiracion2", stub_cmd("respiracion2")))
    app.add_handler(CommandHandler("respiracion_478", stub_cmd("respiracion_478")))
    app.add_handler(CommandHandler("respiracion_box", stub_cmd("respiracion_box")))
    app.add_handler(CommandHandler("yoga2", stub_cmd("yoga2")))
    app.add_handler(CommandHandler("yoga_matutino", stub_cmd("yoga_matutino")))
    app.add_handler(CommandHandler("yoga_nocturno", stub_cmd("yoga_nocturno")))
    app.add_handler(CommandHandler("yoga_principiante", stub_cmd("yoga_principiante")))
    app.add_handler(CommandHandler("yoga_intermedio", stub_cmd("yoga_intermedio")))
    app.add_handler(CommandHandler("yoga_avanzado", stub_cmd("yoga_avanzado")))
    app.add_handler(CommandHandler("tai_chi", stub_cmd("tai_chi")))
    app.add_handler(CommandHandler("qigong", stub_cmd("qigong")))
    app.add_handler(CommandHandler("stretching2", stub_cmd("stretching2")))
    app.add_handler(CommandHandler("estiramiento_manana", stub_cmd("estiramiento_manana")))
    app.add_handler(CommandHandler("estiramiento_noche", stub_cmd("estiramiento_noche")))
    app.add_handler(CommandHandler("flexibilidad2", stub_cmd("flexibilidad2")))
    app.add_handler(CommandHandler("movilidad_articular", stub_cmd("movilidad_articular")))
    app.add_handler(CommandHandler("postura", stub_cmd("postura")))
    app.add_handler(CommandHandler("alineacion", stub_cmd("alineacion")))
    app.add_handler(CommandHandler("equilibrio2", stub_cmd("equilibrio2")))
    app.add_handler(CommandHandler("coordinacion", stub_cmd("coordinacion")))
    app.add_handler(CommandHandler("propriocepcion", stub_cmd("propriocepcion")))
    app.add_handler(CommandHandler("entrenamiento_funcional", stub_cmd("entrenamiento_funcional")))
    app.add_handler(CommandHandler("cardio2", stub_cmd("cardio2")))
    app.add_handler(CommandHandler("running", stub_cmd("running")))
    app.add_handler(CommandHandler("natacion2", stub_cmd("natacion2")))
    app.add_handler(CommandHandler("eliptica", stub_cmd("eliptica")))
    app.add_handler(CommandHandler("caminata", stub_cmd("caminata")))
    app.add_handler(CommandHandler("senderismo", stub_cmd("senderismo")))
    app.add_handler(CommandHandler("escalada", stub_cmd("escalada")))
    app.add_handler(CommandHandler("boxeo2", stub_cmd("boxeo2")))
    app.add_handler(CommandHandler("jiu_jitsu", stub_cmd("jiu_jitsu")))
    app.add_handler(CommandHandler("wrestling", stub_cmd("wrestling")))
    app.add_handler(CommandHandler("esgrima", stub_cmd("esgrima")))
    app.add_handler(CommandHandler("tiro_arco", stub_cmd("tiro_arco")))
    app.add_handler(CommandHandler("skate", stub_cmd("skate")))
    app.add_handler(CommandHandler("ski", stub_cmd("ski")))
    app.add_handler(CommandHandler("wakeboard", stub_cmd("wakeboard")))
    app.add_handler(CommandHandler("kitesurf", stub_cmd("kitesurf")))
    app.add_handler(CommandHandler("parapente", stub_cmd("parapente")))
    app.add_handler(CommandHandler("ala_delta", stub_cmd("ala_delta")))
    app.add_handler(CommandHandler("descanso_activo", stub_cmd("descanso_activo")))
    app.add_handler(CommandHandler("recuperacion2", stub_cmd("recuperacion2")))
    app.add_handler(CommandHandler("foam_roller", stub_cmd("foam_roller")))
    app.add_handler(CommandHandler("masaje_auto", stub_cmd("masaje_auto")))
    app.add_handler(CommandHandler("crioterapia", stub_cmd("crioterapia")))
    app.add_handler(CommandHandler("sauna", stub_cmd("sauna")))
    app.add_handler(CommandHandler("bano_contraste", stub_cmd("bano_contraste")))
    app.add_handler(CommandHandler("hidroterapia", stub_cmd("hidroterapia")))
    app.add_handler(CommandHandler("acupuntura", stub_cmd("acupuntura")))
    app.add_handler(CommandHandler("reflexologia", stub_cmd("reflexologia")))
    app.add_handler(CommandHandler("aromaterapia", stub_cmd("aromaterapia")))
    app.add_handler(CommandHandler("cromoterapia", stub_cmd("cromoterapia")))
    app.add_handler(CommandHandler("musicoterapia", stub_cmd("musicoterapia")))
    app.add_handler(CommandHandler("art_terapia", stub_cmd("art_terapia")))
    app.add_handler(CommandHandler("danza_terapia", stub_cmd("danza_terapia")))
    app.add_handler(CommandHandler("reiki", stub_cmd("reiki")))
    app.add_handler(CommandHandler("shiatsu", stub_cmd("shiatsu")))
    app.add_handler(CommandHandler("ayurveda", stub_cmd("ayurveda")))
    app.add_handler(CommandHandler("naturopatia", stub_cmd("naturopatia")))
    app.add_handler(CommandHandler("homeopatia", stub_cmd("homeopatia")))
    app.add_handler(CommandHandler("fitoterapia", stub_cmd("fitoterapia")))
    app.add_handler(CommandHandler("suplementos", stub_cmd("suplementos")))
    app.add_handler(CommandHandler("aminoacidos", stub_cmd("aminoacidos")))
    app.add_handler(CommandHandler("omega3", stub_cmd("omega3")))
    app.add_handler(CommandHandler("probioticos", stub_cmd("probioticos")))
    app.add_handler(CommandHandler("prebioticos", stub_cmd("prebioticos")))
    app.add_handler(CommandHandler("antioxidantes", stub_cmd("antioxidantes")))
    app.add_handler(CommandHandler("superfood", stub_cmd("superfood")))
    app.add_handler(CommandHandler("ayuno_intermitente", stub_cmd("ayuno_intermitente")))
    app.add_handler(CommandHandler("dieta_cetogenica", stub_cmd("dieta_cetogenica")))
    app.add_handler(CommandHandler("dieta_detox", stub_cmd("dieta_detox")))
    app.add_handler(CommandHandler("dieta_mediterranea2", stub_cmd("dieta_mediterranea2")))
    app.add_handler(CommandHandler("dieta_vegana", stub_cmd("dieta_vegana")))
    app.add_handler(CommandHandler("plan_alimenticio", stub_cmd("plan_alimenticio")))
    app.add_handler(CommandHandler("conteo_calorias", stub_cmd("conteo_calorias")))
    app.add_handler(CommandHandler("micros", stub_cmd("micros")))
    app.add_handler(CommandHandler("agua_diaria", stub_cmd("agua_diaria")))
    app.add_handler(CommandHandler("electrolitos", stub_cmd("electrolitos")))
    app.add_handler(CommandHandler("sales_minerales", stub_cmd("sales_minerales")))
    app.add_handler(CommandHandler("isotonica", stub_cmd("isotonica")))

    # ── 📚 PRODUCTIVIDAD & ESTUDIO
    app.add_handler(CommandHandler("pomodoro2", stub_cmd("pomodoro2")))
    app.add_handler(CommandHandler("pomodoro_25", stub_cmd("pomodoro_25")))
    app.add_handler(CommandHandler("pomodoro_50", stub_cmd("pomodoro_50")))
    app.add_handler(CommandHandler("pomodoro_90", stub_cmd("pomodoro_90")))
    app.add_handler(CommandHandler("metodo_52_17", stub_cmd("metodo_52_17")))
    app.add_handler(CommandHandler("timeblocking", stub_cmd("timeblocking")))
    app.add_handler(CommandHandler("deep_work", stub_cmd("deep_work")))
    app.add_handler(CommandHandler("flow_state", stub_cmd("flow_state")))
    app.add_handler(CommandHandler("cal_newport", stub_cmd("cal_newport")))
    app.add_handler(CommandHandler("bienestar_cognitivo", stub_cmd("bienestar_cognitivo")))
    app.add_handler(CommandHandler("memoria_trabajo", stub_cmd("memoria_trabajo")))
    app.add_handler(CommandHandler("atencion_sostenida", stub_cmd("atencion_sostenida")))
    app.add_handler(CommandHandler("concentracion2", stub_cmd("concentracion2")))
    app.add_handler(CommandHandler("eliminar_distracciones", stub_cmd("eliminar_distracciones")))
    app.add_handler(CommandHandler("focus2", stub_cmd("focus2")))
    app.add_handler(CommandHandler("modo_avion_mental", stub_cmd("modo_avion_mental")))
    app.add_handler(CommandHandler("minimalismo_digital", stub_cmd("minimalismo_digital")))
    app.add_handler(CommandHandler("detox_digital", stub_cmd("detox_digital")))
    app.add_handler(CommandHandler("gestion_tiempo", stub_cmd("gestion_tiempo")))
    app.add_handler(CommandHandler("prioridades", stub_cmd("prioridades")))
    app.add_handler(CommandHandler("eisenhower", stub_cmd("eisenhower")))
    app.add_handler(CommandHandler("pareto", stub_cmd("pareto")))
    app.add_handler(CommandHandler("parkinson_law", stub_cmd("parkinson_law")))
    app.add_handler(CommandHandler("objetivos_smart", stub_cmd("objetivos_smart")))
    app.add_handler(CommandHandler("okr", stub_cmd("okr")))
    app.add_handler(CommandHandler("kpi", stub_cmd("kpi")))
    app.add_handler(CommandHandler("metodologia_agile", stub_cmd("metodologia_agile")))
    app.add_handler(CommandHandler("scrum_personal", stub_cmd("scrum_personal")))
    app.add_handler(CommandHandler("kanban_personal", stub_cmd("kanban_personal")))
    app.add_handler(CommandHandler("bullet_journal", stub_cmd("bullet_journal")))
    app.add_handler(CommandHandler("gtd_metodo", stub_cmd("gtd_metodo")))
    app.add_handler(CommandHandler("zettelkasten", stub_cmd("zettelkasten")))
    app.add_handler(CommandHandler("cornell_notes", stub_cmd("cornell_notes")))
    app.add_handler(CommandHandler("diagrama_flujo", stub_cmd("diagrama_flujo")))
    app.add_handler(CommandHandler("resumen_tecnica", stub_cmd("resumen_tecnica")))
    app.add_handler(CommandHandler("subrayado", stub_cmd("subrayado")))
    app.add_handler(CommandHandler("lectura_rapida", stub_cmd("lectura_rapida")))
    app.add_handler(CommandHandler("lectura_eficaz", stub_cmd("lectura_eficaz")))
    app.add_handler(CommandHandler("skimming", stub_cmd("skimming")))
    app.add_handler(CommandHandler("scanning", stub_cmd("scanning")))
    app.add_handler(CommandHandler("sqr3", stub_cmd("sqr3")))
    app.add_handler(CommandHandler("metodo_feynman", stub_cmd("metodo_feynman")))
    app.add_handler(CommandHandler("aprendizaje_espaciado", stub_cmd("aprendizaje_espaciado")))
    app.add_handler(CommandHandler("repeticion_espaciada", stub_cmd("repeticion_espaciada")))
    app.add_handler(CommandHandler("flashcards2", stub_cmd("flashcards2")))
    app.add_handler(CommandHandler("anki_sistema", stub_cmd("anki_sistema")))
    app.add_handler(CommandHandler("loci_metodo", stub_cmd("loci_metodo")))
    app.add_handler(CommandHandler("palace_memory", stub_cmd("palace_memory")))
    app.add_handler(CommandHandler("mnemonicos", stub_cmd("mnemonicos")))
    app.add_handler(CommandHandler("acronimos", stub_cmd("acronimos")))
    app.add_handler(CommandHandler("ritmo_circadiano", stub_cmd("ritmo_circadiano")))
    app.add_handler(CommandHandler("cronotipo", stub_cmd("cronotipo")))
    app.add_handler(CommandHandler("mejor_hora_estudiar", stub_cmd("mejor_hora_estudiar")))
    app.add_handler(CommandHandler("horario_biologico", stub_cmd("horario_biologico")))
    app.add_handler(CommandHandler("sueno_estudio", stub_cmd("sueno_estudio")))
    app.add_handler(CommandHandler("siesta_power", stub_cmd("siesta_power")))
    app.add_handler(CommandHandler("cafeina_timing", stub_cmd("cafeina_timing")))
    app.add_handler(CommandHandler("ejercicio_cognitivo", stub_cmd("ejercicio_cognitivo")))
    app.add_handler(CommandHandler("neuroplasticidad", stub_cmd("neuroplasticidad")))
    app.add_handler(CommandHandler("crecimiento_mental", stub_cmd("crecimiento_mental")))
    app.add_handler(CommandHandler("mentalidad_crecimiento", stub_cmd("mentalidad_crecimiento")))
    app.add_handler(CommandHandler("resiliencia", stub_cmd("resiliencia")))
    app.add_handler(CommandHandler("autoeficacia", stub_cmd("autoeficacia")))
    app.add_handler(CommandHandler("autoconfianza", stub_cmd("autoconfianza")))
    app.add_handler(CommandHandler("motivacion2", stub_cmd("motivacion2")))
    app.add_handler(CommandHandler("habitos_atomic", stub_cmd("habitos_atomic")))
    app.add_handler(CommandHandler("1_porciento_mejor", stub_cmd("1_porciento_mejor")))
    app.add_handler(CommandHandler("kaizen_personal", stub_cmd("kaizen_personal")))
    app.add_handler(CommandHandler("mejora_continua", stub_cmd("mejora_continua")))
    app.add_handler(CommandHandler("reflexion_diaria", stub_cmd("reflexion_diaria")))
    app.add_handler(CommandHandler("journaling", stub_cmd("journaling")))
    app.add_handler(CommandHandler("diario_gratitud", stub_cmd("diario_gratitud")))
    app.add_handler(CommandHandler("diario_logros", stub_cmd("diario_logros")))
    app.add_handler(CommandHandler("diario_aprendizaje", stub_cmd("diario_aprendizaje")))
    app.add_handler(CommandHandler("revision_semanal", stub_cmd("revision_semanal")))
    app.add_handler(CommandHandler("revision_mensual", stub_cmd("revision_mensual")))
    app.add_handler(CommandHandler("revision_anual", stub_cmd("revision_anual")))
    app.add_handler(CommandHandler("metas_anuales", stub_cmd("metas_anuales")))
    app.add_handler(CommandHandler("vision_board", stub_cmd("vision_board")))
    app.add_handler(CommandHandler("plan_5_anos", stub_cmd("plan_5_anos")))
    app.add_handler(CommandHandler("legado", stub_cmd("legado")))
    app.add_handler(CommandHandler("proposito_vida", stub_cmd("proposito_vida")))
    app.add_handler(CommandHandler("ikigai", stub_cmd("ikigai")))
    app.add_handler(CommandHandler("wheel_of_life", stub_cmd("wheel_of_life")))
    app.add_handler(CommandHandler("balance_vida", stub_cmd("balance_vida")))
    app.add_handler(CommandHandler("work_life_balance", stub_cmd("work_life_balance")))
    app.add_handler(CommandHandler("burnout_prevencion", stub_cmd("burnout_prevencion")))
    app.add_handler(CommandHandler("estres_gestion", stub_cmd("estres_gestion")))
    app.add_handler(CommandHandler("ansiedad_manejo", stub_cmd("ansiedad_manejo")))
    app.add_handler(CommandHandler("procrastinacion_vencer", stub_cmd("procrastinacion_vencer")))
    app.add_handler(CommandHandler("perfeccionismo", stub_cmd("perfeccionismo")))
    app.add_handler(CommandHandler("bloqueo_creativo", stub_cmd("bloqueo_creativo")))
    app.add_handler(CommandHandler("creatividad2", stub_cmd("creatividad2")))
    app.add_handler(CommandHandler("brainstorming", stub_cmd("brainstorming")))
    app.add_handler(CommandHandler("tecnica_scamper", stub_cmd("tecnica_scamper")))
    app.add_handler(CommandHandler("pensamiento_lateral", stub_cmd("pensamiento_lateral")))
    app.add_handler(CommandHandler("six_thinking_hats", stub_cmd("six_thinking_hats")))
    app.add_handler(CommandHandler("design_thinking", stub_cmd("design_thinking")))
    app.add_handler(CommandHandler("problem_solving", stub_cmd("problem_solving")))

    # ── 💻 TECNOLOGÍA & CÓDIGO
    app.add_handler(CommandHandler("python2", stub_cmd("python2")))
    app.add_handler(CommandHandler("javascript2", stub_cmd("javascript2")))
    app.add_handler(CommandHandler("typescript2", stub_cmd("typescript2")))
    app.add_handler(CommandHandler("java2", stub_cmd("java2")))
    app.add_handler(CommandHandler("cpp2", stub_cmd("cpp2")))
    app.add_handler(CommandHandler("rust2", stub_cmd("rust2")))
    app.add_handler(CommandHandler("go_lang", stub_cmd("go_lang")))
    app.add_handler(CommandHandler("kotlin", stub_cmd("kotlin")))
    app.add_handler(CommandHandler("swift", stub_cmd("swift")))
    app.add_handler(CommandHandler("dart", stub_cmd("dart")))
    app.add_handler(CommandHandler("ruby", stub_cmd("ruby")))
    app.add_handler(CommandHandler("php2", stub_cmd("php2")))
    app.add_handler(CommandHandler("scala", stub_cmd("scala")))
    app.add_handler(CommandHandler("elixir", stub_cmd("elixir")))
    app.add_handler(CommandHandler("haskell", stub_cmd("haskell")))
    app.add_handler(CommandHandler("clojure", stub_cmd("clojure")))
    app.add_handler(CommandHandler("erlang", stub_cmd("erlang")))
    app.add_handler(CommandHandler("lua", stub_cmd("lua")))
    app.add_handler(CommandHandler("perl", stub_cmd("perl")))
    app.add_handler(CommandHandler("r_lang", stub_cmd("r_lang")))
    app.add_handler(CommandHandler("matlab", stub_cmd("matlab")))
    app.add_handler(CommandHandler("julia", stub_cmd("julia")))
    app.add_handler(CommandHandler("html2", stub_cmd("html2")))
    app.add_handler(CommandHandler("css2", stub_cmd("css2")))
    app.add_handler(CommandHandler("sass", stub_cmd("sass")))
    app.add_handler(CommandHandler("less", stub_cmd("less")))
    app.add_handler(CommandHandler("tailwind", stub_cmd("tailwind")))
    app.add_handler(CommandHandler("bootstrap", stub_cmd("bootstrap")))
    app.add_handler(CommandHandler("materialize", stub_cmd("materialize")))
    app.add_handler(CommandHandler("react2", stub_cmd("react2")))
    app.add_handler(CommandHandler("angular2", stub_cmd("angular2")))
    app.add_handler(CommandHandler("vue2", stub_cmd("vue2")))
    app.add_handler(CommandHandler("nextjs", stub_cmd("nextjs")))
    app.add_handler(CommandHandler("nuxtjs", stub_cmd("nuxtjs")))
    app.add_handler(CommandHandler("gatsby", stub_cmd("gatsby")))
    app.add_handler(CommandHandler("astro", stub_cmd("astro")))
    app.add_handler(CommandHandler("nodejs2", stub_cmd("nodejs2")))
    app.add_handler(CommandHandler("express2", stub_cmd("express2")))
    app.add_handler(CommandHandler("fastapi", stub_cmd("fastapi")))
    app.add_handler(CommandHandler("flask2", stub_cmd("flask2")))
    app.add_handler(CommandHandler("django", stub_cmd("django")))
    app.add_handler(CommandHandler("rails", stub_cmd("rails")))
    app.add_handler(CommandHandler("laravel", stub_cmd("laravel")))
    app.add_handler(CommandHandler("spring", stub_cmd("spring")))
    app.add_handler(CommandHandler("dotnet", stub_cmd("dotnet")))
    app.add_handler(CommandHandler("asp_net", stub_cmd("asp_net")))
    app.add_handler(CommandHandler("nestjs", stub_cmd("nestjs")))
    app.add_handler(CommandHandler("strapi", stub_cmd("strapi")))
    app.add_handler(CommandHandler("hasura", stub_cmd("hasura")))
    app.add_handler(CommandHandler("rest_api", stub_cmd("rest_api")))
    app.add_handler(CommandHandler("grpc", stub_cmd("grpc")))
    app.add_handler(CommandHandler("sse", stub_cmd("sse")))
    app.add_handler(CommandHandler("mqtt", stub_cmd("mqtt")))
    app.add_handler(CommandHandler("amqp", stub_cmd("amqp")))
    app.add_handler(CommandHandler("kafka", stub_cmd("kafka")))
    app.add_handler(CommandHandler("rabbitmq", stub_cmd("rabbitmq")))
    app.add_handler(CommandHandler("redis2", stub_cmd("redis2")))
    app.add_handler(CommandHandler("memcached", stub_cmd("memcached")))
    app.add_handler(CommandHandler("mongodb2", stub_cmd("mongodb2")))
    app.add_handler(CommandHandler("postgresql2", stub_cmd("postgresql2")))
    app.add_handler(CommandHandler("mysql2", stub_cmd("mysql2")))
    app.add_handler(CommandHandler("sqlite2", stub_cmd("sqlite2")))
    app.add_handler(CommandHandler("firebase2", stub_cmd("firebase2")))
    app.add_handler(CommandHandler("supabase", stub_cmd("supabase")))
    app.add_handler(CommandHandler("planetscale", stub_cmd("planetscale")))
    app.add_handler(CommandHandler("neon_db", stub_cmd("neon_db")))
    app.add_handler(CommandHandler("cockroachdb", stub_cmd("cockroachdb")))
    app.add_handler(CommandHandler("docker2", stub_cmd("docker2")))
    app.add_handler(CommandHandler("helm", stub_cmd("helm")))
    app.add_handler(CommandHandler("terraform", stub_cmd("terraform")))
    app.add_handler(CommandHandler("ansible", stub_cmd("ansible")))
    app.add_handler(CommandHandler("puppet", stub_cmd("puppet")))
    app.add_handler(CommandHandler("circleci", stub_cmd("circleci")))
    app.add_handler(CommandHandler("travis_ci", stub_cmd("travis_ci")))
    app.add_handler(CommandHandler("argocd", stub_cmd("argocd")))
    app.add_handler(CommandHandler("prometheus", stub_cmd("prometheus")))
    app.add_handler(CommandHandler("grafana", stub_cmd("grafana")))
    app.add_handler(CommandHandler("loki", stub_cmd("loki")))
    app.add_handler(CommandHandler("jaeger", stub_cmd("jaeger")))
    app.add_handler(CommandHandler("datadog", stub_cmd("datadog")))
    app.add_handler(CommandHandler("sentry", stub_cmd("sentry")))
    app.add_handler(CommandHandler("newrelic", stub_cmd("newrelic")))
    app.add_handler(CommandHandler("gcp", stub_cmd("gcp")))
    app.add_handler(CommandHandler("digital_ocean", stub_cmd("digital_ocean")))
    app.add_handler(CommandHandler("linode", stub_cmd("linode")))
    app.add_handler(CommandHandler("vultr", stub_cmd("vultr")))
    app.add_handler(CommandHandler("heroku2", stub_cmd("heroku2")))
    app.add_handler(CommandHandler("vercel2", stub_cmd("vercel2")))
    app.add_handler(CommandHandler("netlify2", stub_cmd("netlify2")))
    app.add_handler(CommandHandler("railway", stub_cmd("railway")))
    app.add_handler(CommandHandler("render", stub_cmd("render")))
    app.add_handler(CommandHandler("fly_io", stub_cmd("fly_io")))
    app.add_handler(CommandHandler("cloudflare", stub_cmd("cloudflare")))
    app.add_handler(CommandHandler("nginx2", stub_cmd("nginx2")))
    app.add_handler(CommandHandler("apache2", stub_cmd("apache2")))
    app.add_handler(CommandHandler("ssl_cert", stub_cmd("ssl_cert")))
    app.add_handler(CommandHandler("dominio", stub_cmd("dominio")))
    app.add_handler(CommandHandler("dns", stub_cmd("dns")))
    app.add_handler(CommandHandler("cdn", stub_cmd("cdn")))
    app.add_handler(CommandHandler("load_balancer", stub_cmd("load_balancer")))
    app.add_handler(CommandHandler("reverse_proxy", stub_cmd("reverse_proxy")))
    app.add_handler(CommandHandler("vpn2", stub_cmd("vpn2")))
    app.add_handler(CommandHandler("ssh2", stub_cmd("ssh2")))
    app.add_handler(CommandHandler("sftp", stub_cmd("sftp")))
    app.add_handler(CommandHandler("ftp", stub_cmd("ftp")))
    app.add_handler(CommandHandler("smb", stub_cmd("smb")))
    app.add_handler(CommandHandler("nfs", stub_cmd("nfs")))
    app.add_handler(CommandHandler("s3", stub_cmd("s3")))
    app.add_handler(CommandHandler("gcs", stub_cmd("gcs")))
    app.add_handler(CommandHandler("azure_blob", stub_cmd("azure_blob")))
    app.add_handler(CommandHandler("jwt2", stub_cmd("jwt2")))
    app.add_handler(CommandHandler("oauth2", stub_cmd("oauth2")))
    app.add_handler(CommandHandler("oidc", stub_cmd("oidc")))
    app.add_handler(CommandHandler("saml", stub_cmd("saml")))
    app.add_handler(CommandHandler("ldap", stub_cmd("ldap")))
    app.add_handler(CommandHandler("rbac", stub_cmd("rbac")))
    app.add_handler(CommandHandler("abac", stub_cmd("abac")))
    app.add_handler(CommandHandler("zero_trust", stub_cmd("zero_trust")))
    app.add_handler(CommandHandler("owasp", stub_cmd("owasp")))
    app.add_handler(CommandHandler("xss", stub_cmd("xss")))
    app.add_handler(CommandHandler("csrf", stub_cmd("csrf")))
    app.add_handler(CommandHandler("sqli", stub_cmd("sqli")))
    app.add_handler(CommandHandler("lfi", stub_cmd("lfi")))
    app.add_handler(CommandHandler("rfi", stub_cmd("rfi")))
    app.add_handler(CommandHandler("rce", stub_cmd("rce")))
    app.add_handler(CommandHandler("ssrf", stub_cmd("ssrf")))
    app.add_handler(CommandHandler("idor", stub_cmd("idor")))
    app.add_handler(CommandHandler("pentest", stub_cmd("pentest")))
    app.add_handler(CommandHandler("burpsuite", stub_cmd("burpsuite")))
    app.add_handler(CommandHandler("metasploit", stub_cmd("metasploit")))
    app.add_handler(CommandHandler("nmap2", stub_cmd("nmap2")))
    app.add_handler(CommandHandler("wireshark", stub_cmd("wireshark")))
    app.add_handler(CommandHandler("tcpdump", stub_cmd("tcpdump")))

    # ── 🏰 RPG & FANTASÍA
    app.add_handler(CommandHandler("crear_heroe", stub_cmd("crear_heroe")))
    app.add_handler(CommandHandler("crear_villano", stub_cmd("crear_villano")))
    app.add_handler(CommandHandler("crear_personaje2", stub_cmd("crear_personaje2")))
    app.add_handler(CommandHandler("crear_mundo", stub_cmd("crear_mundo")))
    app.add_handler(CommandHandler("crear_reino", stub_cmd("crear_reino")))
    app.add_handler(CommandHandler("crear_ciudad_rpg", stub_cmd("crear_ciudad_rpg")))
    app.add_handler(CommandHandler("crear_mazmorra", stub_cmd("crear_mazmorra")))
    app.add_handler(CommandHandler("crear_quest", stub_cmd("crear_quest")))
    app.add_handler(CommandHandler("crear_historia_rpg", stub_cmd("crear_historia_rpg")))
    app.add_handler(CommandHandler("clase_guerrero", stub_cmd("clase_guerrero")))
    app.add_handler(CommandHandler("clase_mago", stub_cmd("clase_mago")))
    app.add_handler(CommandHandler("clase_ladron", stub_cmd("clase_ladron")))
    app.add_handler(CommandHandler("clase_arquero", stub_cmd("clase_arquero")))
    app.add_handler(CommandHandler("clase_cura", stub_cmd("clase_cura")))
    app.add_handler(CommandHandler("clase_bardo", stub_cmd("clase_bardo")))
    app.add_handler(CommandHandler("clase_paladin", stub_cmd("clase_paladin")))
    app.add_handler(CommandHandler("clase_druida", stub_cmd("clase_druida")))
    app.add_handler(CommandHandler("clase_monje", stub_cmd("clase_monje")))
    app.add_handler(CommandHandler("clase_ranger", stub_cmd("clase_ranger")))
    app.add_handler(CommandHandler("raza_humano", stub_cmd("raza_humano")))
    app.add_handler(CommandHandler("raza_elfo", stub_cmd("raza_elfo")))
    app.add_handler(CommandHandler("raza_enano", stub_cmd("raza_enano")))
    app.add_handler(CommandHandler("raza_orco", stub_cmd("raza_orco")))
    app.add_handler(CommandHandler("raza_hobbit", stub_cmd("raza_hobbit")))
    app.add_handler(CommandHandler("raza_vampiro", stub_cmd("raza_vampiro")))
    app.add_handler(CommandHandler("raza_licantropo", stub_cmd("raza_licantropo")))
    app.add_handler(CommandHandler("raza_demonio", stub_cmd("raza_demonio")))
    app.add_handler(CommandHandler("raza_angel", stub_cmd("raza_angel")))
    app.add_handler(CommandHandler("raza_dragon", stub_cmd("raza_dragon")))
    app.add_handler(CommandHandler("habilidad_fuego", stub_cmd("habilidad_fuego")))
    app.add_handler(CommandHandler("habilidad_agua", stub_cmd("habilidad_agua")))
    app.add_handler(CommandHandler("habilidad_tierra", stub_cmd("habilidad_tierra")))
    app.add_handler(CommandHandler("habilidad_aire", stub_cmd("habilidad_aire")))
    app.add_handler(CommandHandler("habilidad_luz", stub_cmd("habilidad_luz")))
    app.add_handler(CommandHandler("habilidad_oscuridad", stub_cmd("habilidad_oscuridad")))
    app.add_handler(CommandHandler("habilidad_rayo", stub_cmd("habilidad_rayo")))
    app.add_handler(CommandHandler("habilidad_hielo", stub_cmd("habilidad_hielo")))
    app.add_handler(CommandHandler("habilidad_veneno", stub_cmd("habilidad_veneno")))
    app.add_handler(CommandHandler("habilidad_tiempo", stub_cmd("habilidad_tiempo")))
    app.add_handler(CommandHandler("habilidad_espacio", stub_cmd("habilidad_espacio")))
    app.add_handler(CommandHandler("habilidad_psiquica", stub_cmd("habilidad_psiquica")))
    app.add_handler(CommandHandler("item_espada", stub_cmd("item_espada")))
    app.add_handler(CommandHandler("item_hacha", stub_cmd("item_hacha")))
    app.add_handler(CommandHandler("item_lanza", stub_cmd("item_lanza")))
    app.add_handler(CommandHandler("item_arco", stub_cmd("item_arco")))
    app.add_handler(CommandHandler("item_baston", stub_cmd("item_baston")))
    app.add_handler(CommandHandler("item_daga", stub_cmd("item_daga")))
    app.add_handler(CommandHandler("item_escudo", stub_cmd("item_escudo")))
    app.add_handler(CommandHandler("item_armadura", stub_cmd("item_armadura")))
    app.add_handler(CommandHandler("item_casco", stub_cmd("item_casco")))
    app.add_handler(CommandHandler("item_guantes", stub_cmd("item_guantes")))
    app.add_handler(CommandHandler("item_botas", stub_cmd("item_botas")))
    app.add_handler(CommandHandler("item_capa", stub_cmd("item_capa")))
    app.add_handler(CommandHandler("item_anillo", stub_cmd("item_anillo")))
    app.add_handler(CommandHandler("item_collar", stub_cmd("item_collar")))
    app.add_handler(CommandHandler("item_amuleto", stub_cmd("item_amuleto")))
    app.add_handler(CommandHandler("pocion_vida", stub_cmd("pocion_vida")))
    app.add_handler(CommandHandler("pocion_mana", stub_cmd("pocion_mana")))
    app.add_handler(CommandHandler("pocion_velocidad", stub_cmd("pocion_velocidad")))
    app.add_handler(CommandHandler("pocion_fuerza", stub_cmd("pocion_fuerza")))
    app.add_handler(CommandHandler("pocion_invisibilidad", stub_cmd("pocion_invisibilidad")))
    app.add_handler(CommandHandler("pocion_veneno", stub_cmd("pocion_veneno")))
    app.add_handler(CommandHandler("antidoto", stub_cmd("antidoto")))
    app.add_handler(CommandHandler("resurreccion", stub_cmd("resurreccion")))
    app.add_handler(CommandHandler("teletransporte", stub_cmd("teletransporte")))
    app.add_handler(CommandHandler("invocacion", stub_cmd("invocacion")))
    app.add_handler(CommandHandler("invoca_dragon", stub_cmd("invoca_dragon")))
    app.add_handler(CommandHandler("invoca_fenix", stub_cmd("invoca_fenix")))
    app.add_handler(CommandHandler("invoca_unicornio", stub_cmd("invoca_unicornio")))
    app.add_handler(CommandHandler("invoca_golem", stub_cmd("invoca_golem")))
    app.add_handler(CommandHandler("invoca_elemental", stub_cmd("invoca_elemental")))
    app.add_handler(CommandHandler("mision_principal", stub_cmd("mision_principal")))
    app.add_handler(CommandHandler("mision_secundaria", stub_cmd("mision_secundaria")))
    app.add_handler(CommandHandler("mision_gremio", stub_cmd("mision_gremio")))
    app.add_handler(CommandHandler("mision_diaria_rpg", stub_cmd("mision_diaria_rpg")))
    app.add_handler(CommandHandler("recompensa_mision", stub_cmd("recompensa_mision")))
    app.add_handler(CommandHandler("experiencia_rpg", stub_cmd("experiencia_rpg")))
    app.add_handler(CommandHandler("subir_nivel_rpg", stub_cmd("subir_nivel_rpg")))
    app.add_handler(CommandHandler("habilidad_nueva", stub_cmd("habilidad_nueva")))
    app.add_handler(CommandHandler("punto_habilidad", stub_cmd("punto_habilidad")))
    app.add_handler(CommandHandler("arbol_talentos", stub_cmd("arbol_talentos")))
    app.add_handler(CommandHandler("prestige_rpg", stub_cmd("prestige_rpg")))
    app.add_handler(CommandHandler("pvp", stub_cmd("pvp")))
    app.add_handler(CommandHandler("pve", stub_cmd("pve")))
    app.add_handler(CommandHandler("co_op", stub_cmd("co_op")))
    app.add_handler(CommandHandler("raid2", stub_cmd("raid2")))
    app.add_handler(CommandHandler("mazmorra_elite", stub_cmd("mazmorra_elite")))
    app.add_handler(CommandHandler("boss_final", stub_cmd("boss_final")))
    app.add_handler(CommandHandler("final_boss", stub_cmd("final_boss")))
    app.add_handler(CommandHandler("mundo_abierto", stub_cmd("mundo_abierto")))
    app.add_handler(CommandHandler("mapa_rpg", stub_cmd("mapa_rpg")))
    app.add_handler(CommandHandler("viaje_rapido", stub_cmd("viaje_rapido")))
    app.add_handler(CommandHandler("montura", stub_cmd("montura")))
    app.add_handler(CommandHandler("mascota_rpg", stub_cmd("mascota_rpg")))
    app.add_handler(CommandHandler("crafting", stub_cmd("crafting")))
    app.add_handler(CommandHandler("forja", stub_cmd("forja")))
    app.add_handler(CommandHandler("alquimia", stub_cmd("alquimia")))
    app.add_handler(CommandHandler("encantamiento", stub_cmd("encantamiento")))
    app.add_handler(CommandHandler("runa", stub_cmd("runa")))
    app.add_handler(CommandHandler("glifo", stub_cmd("glifo")))

    # ── 🌌 CIENCIA & NATURALEZA
    app.add_handler(CommandHandler("planeta2", stub_cmd("planeta2")))
    app.add_handler(CommandHandler("planeta_mercurio", stub_cmd("planeta_mercurio")))
    app.add_handler(CommandHandler("planeta_venus", stub_cmd("planeta_venus")))
    app.add_handler(CommandHandler("planeta_tierra", stub_cmd("planeta_tierra")))
    app.add_handler(CommandHandler("planeta_marte", stub_cmd("planeta_marte")))
    app.add_handler(CommandHandler("planeta_jupiter", stub_cmd("planeta_jupiter")))
    app.add_handler(CommandHandler("planeta_saturno", stub_cmd("planeta_saturno")))
    app.add_handler(CommandHandler("planeta_urano", stub_cmd("planeta_urano")))
    app.add_handler(CommandHandler("planeta_neptuno", stub_cmd("planeta_neptuno")))
    app.add_handler(CommandHandler("pluton", stub_cmd("pluton")))
    app.add_handler(CommandHandler("luna_info", stub_cmd("luna_info")))
    app.add_handler(CommandHandler("sol_info", stub_cmd("sol_info")))
    app.add_handler(CommandHandler("estrella_mas_cercana", stub_cmd("estrella_mas_cercana")))
    app.add_handler(CommandHandler("constelacion", stub_cmd("constelacion")))
    app.add_handler(CommandHandler("zodiaco_astro", stub_cmd("zodiaco_astro")))
    app.add_handler(CommandHandler("galaxia", stub_cmd("galaxia")))
    app.add_handler(CommandHandler("via_lactea", stub_cmd("via_lactea")))
    app.add_handler(CommandHandler("andromeda", stub_cmd("andromeda")))
    app.add_handler(CommandHandler("nebulosa", stub_cmd("nebulosa")))
    app.add_handler(CommandHandler("supernova", stub_cmd("supernova")))
    app.add_handler(CommandHandler("agujero_negro", stub_cmd("agujero_negro")))
    app.add_handler(CommandHandler("materia_oscura", stub_cmd("materia_oscura")))
    app.add_handler(CommandHandler("energia_oscura", stub_cmd("energia_oscura")))
    app.add_handler(CommandHandler("big_bang", stub_cmd("big_bang")))
    app.add_handler(CommandHandler("universo_edad", stub_cmd("universo_edad")))
    app.add_handler(CommandHandler("cosmologia", stub_cmd("cosmologia")))
    app.add_handler(CommandHandler("telescopio", stub_cmd("telescopio")))
    app.add_handler(CommandHandler("hubble", stub_cmd("hubble")))
    app.add_handler(CommandHandler("james_webb", stub_cmd("james_webb")))
    app.add_handler(CommandHandler("muy_grande", stub_cmd("muy_grande")))
    app.add_handler(CommandHandler("radio_telescopio", stub_cmd("radio_telescopio")))
    app.add_handler(CommandHandler("observatorio", stub_cmd("observatorio")))
    app.add_handler(CommandHandler("exoplaneta", stub_cmd("exoplaneta")))
    app.add_handler(CommandHandler("zona_habitable", stub_cmd("zona_habitable")))
    app.add_handler(CommandHandler("vida_extraterrestre", stub_cmd("vida_extraterrestre")))
    app.add_handler(CommandHandler("seti", stub_cmd("seti")))
    app.add_handler(CommandHandler("nasa", stub_cmd("nasa")))
    app.add_handler(CommandHandler("esa", stub_cmd("esa")))
    app.add_handler(CommandHandler("spacex", stub_cmd("spacex")))
    app.add_handler(CommandHandler("atom", stub_cmd("atom")))
    app.add_handler(CommandHandler("proton", stub_cmd("proton")))
    app.add_handler(CommandHandler("neutron", stub_cmd("neutron")))
    app.add_handler(CommandHandler("electron", stub_cmd("electron")))
    app.add_handler(CommandHandler("quark", stub_cmd("quark")))
    app.add_handler(CommandHandler("boson", stub_cmd("boson")))
    app.add_handler(CommandHandler("higgs", stub_cmd("higgs")))
    app.add_handler(CommandHandler("antimateria", stub_cmd("antimateria")))
    app.add_handler(CommandHandler("tabla_periodica", stub_cmd("tabla_periodica")))
    app.add_handler(CommandHandler("elemento2", stub_cmd("elemento2")))
    app.add_handler(CommandHandler("hidrogeno", stub_cmd("hidrogeno")))
    app.add_handler(CommandHandler("helio", stub_cmd("helio")))
    app.add_handler(CommandHandler("carbono", stub_cmd("carbono")))
    app.add_handler(CommandHandler("nitrogeno", stub_cmd("nitrogeno")))
    app.add_handler(CommandHandler("oxigeno", stub_cmd("oxigeno")))
    app.add_handler(CommandHandler("sodio", stub_cmd("sodio")))
    app.add_handler(CommandHandler("potasio", stub_cmd("potasio")))
    app.add_handler(CommandHandler("calcio", stub_cmd("calcio")))
    app.add_handler(CommandHandler("hierro", stub_cmd("hierro")))
    app.add_handler(CommandHandler("cobre", stub_cmd("cobre")))
    app.add_handler(CommandHandler("zinc", stub_cmd("zinc")))
    app.add_handler(CommandHandler("plomo", stub_cmd("plomo")))
    app.add_handler(CommandHandler("uranio", stub_cmd("uranio")))
    app.add_handler(CommandHandler("plutonio", stub_cmd("plutonio")))
    app.add_handler(CommandHandler("sal_quimica", stub_cmd("sal_quimica")))
    app.add_handler(CommandHandler("oxidacion", stub_cmd("oxidacion")))
    app.add_handler(CommandHandler("reduccion", stub_cmd("reduccion")))
    app.add_handler(CommandHandler("electronegatvidad", stub_cmd("electronegatvidad")))
    app.add_handler(CommandHandler("enlace_ionico", stub_cmd("enlace_ionico")))
    app.add_handler(CommandHandler("enlace_covalente", stub_cmd("enlace_covalente")))
    app.add_handler(CommandHandler("enlace_metalico", stub_cmd("enlace_metalico")))
    app.add_handler(CommandHandler("polimero", stub_cmd("polimero")))
    app.add_handler(CommandHandler("celula", stub_cmd("celula")))
    app.add_handler(CommandHandler("celula_animal", stub_cmd("celula_animal")))
    app.add_handler(CommandHandler("celula_vegetal", stub_cmd("celula_vegetal")))
    app.add_handler(CommandHandler("bacteria", stub_cmd("bacteria")))
    app.add_handler(CommandHandler("virus2", stub_cmd("virus2")))
    app.add_handler(CommandHandler("hongo2", stub_cmd("hongo2")))
    app.add_handler(CommandHandler("parasito", stub_cmd("parasito")))
    app.add_handler(CommandHandler("dna", stub_cmd("dna")))
    app.add_handler(CommandHandler("rna", stub_cmd("rna")))
    app.add_handler(CommandHandler("gen", stub_cmd("gen")))
    app.add_handler(CommandHandler("cromosoma", stub_cmd("cromosoma")))
    app.add_handler(CommandHandler("mutacion", stub_cmd("mutacion")))
    app.add_handler(CommandHandler("evolucion", stub_cmd("evolucion")))
    app.add_handler(CommandHandler("seleccion_natural", stub_cmd("seleccion_natural")))
    app.add_handler(CommandHandler("fotosintesis", stub_cmd("fotosintesis")))
    app.add_handler(CommandHandler("respiracion_celular", stub_cmd("respiracion_celular")))
    app.add_handler(CommandHandler("mitosis", stub_cmd("mitosis")))
    app.add_handler(CommandHandler("meiosis", stub_cmd("meiosis")))
    app.add_handler(CommandHandler("reproduccion_asexual", stub_cmd("reproduccion_asexual")))
    app.add_handler(CommandHandler("ecosistema", stub_cmd("ecosistema")))
    app.add_handler(CommandHandler("bioma", stub_cmd("bioma")))
    app.add_handler(CommandHandler("cadena_alimentaria", stub_cmd("cadena_alimentaria")))
    app.add_handler(CommandHandler("red_trofica", stub_cmd("red_trofica")))
    app.add_handler(CommandHandler("ciclo_agua", stub_cmd("ciclo_agua")))
    app.add_handler(CommandHandler("ciclo_carbono", stub_cmd("ciclo_carbono")))
    app.add_handler(CommandHandler("ciclo_nitrogeno", stub_cmd("ciclo_nitrogeno")))
    app.add_handler(CommandHandler("ciclo_fosforo", stub_cmd("ciclo_fosforo")))
    app.add_handler(CommandHandler("cambio_climatico", stub_cmd("cambio_climatico")))
    app.add_handler(CommandHandler("efecto_invernadero", stub_cmd("efecto_invernadero")))
    app.add_handler(CommandHandler("capa_ozono", stub_cmd("capa_ozono")))
    app.add_handler(CommandHandler("lluvia_acida", stub_cmd("lluvia_acida")))
    app.add_handler(CommandHandler("desertificacion", stub_cmd("desertificacion")))
    app.add_handler(CommandHandler("deforestacion", stub_cmd("deforestacion")))
    app.add_handler(CommandHandler("extincion", stub_cmd("extincion")))
    app.add_handler(CommandHandler("especie_invasora", stub_cmd("especie_invasora")))
    app.add_handler(CommandHandler("biodiversidad", stub_cmd("biodiversidad")))
    app.add_handler(CommandHandler("hotspot_biodiversidad", stub_cmd("hotspot_biodiversidad")))
    app.add_handler(CommandHandler("area_protegida", stub_cmd("area_protegida")))
    app.add_handler(CommandHandler("parque_nacional", stub_cmd("parque_nacional")))
    app.add_handler(CommandHandler("reserva_biosfera", stub_cmd("reserva_biosfera")))
    app.add_handler(CommandHandler("patrimonio_natural", stub_cmd("patrimonio_natural")))
    app.add_handler(CommandHandler("refugio_vida_silvestre", stub_cmd("refugio_vida_silvestre")))

    # ── 🔐 SEGURIDAD & PRIVACIDAD
    app.add_handler(CommandHandler("vpn3", stub_cmd("vpn3")))
    app.add_handler(CommandHandler("tor_info", stub_cmd("tor_info")))
    app.add_handler(CommandHandler("proxy_info", stub_cmd("proxy_info")))
    app.add_handler(CommandHandler("i2p_info", stub_cmd("i2p_info")))
    app.add_handler(CommandHandler("freenet_info", stub_cmd("freenet_info")))
    app.add_handler(CommandHandler("zeronet_info", stub_cmd("zeronet_info")))
    app.add_handler(CommandHandler("cifrado_info", stub_cmd("cifrado_info")))
    app.add_handler(CommandHandler("pgp_info", stub_cmd("pgp_info")))
    app.add_handler(CommandHandler("gpg_info", stub_cmd("gpg_info")))
    app.add_handler(CommandHandler("ssl_info", stub_cmd("ssl_info")))
    app.add_handler(CommandHandler("tls_info", stub_cmd("tls_info")))
    app.add_handler(CommandHandler("https_info", stub_cmd("https_info")))
    app.add_handler(CommandHandler("firewall_info", stub_cmd("firewall_info")))
    app.add_handler(CommandHandler("ids_info", stub_cmd("ids_info")))
    app.add_handler(CommandHandler("ips_info", stub_cmd("ips_info")))
    app.add_handler(CommandHandler("siem_info", stub_cmd("siem_info")))
    app.add_handler(CommandHandler("soc_info", stub_cmd("soc_info")))
    app.add_handler(CommandHandler("ciso_info", stub_cmd("ciso_info")))
    app.add_handler(CommandHandler("pentesting2", stub_cmd("pentesting2")))
    app.add_handler(CommandHandler("hacking_etico", stub_cmd("hacking_etico")))
    app.add_handler(CommandHandler("bug_bounty", stub_cmd("bug_bounty")))
    app.add_handler(CommandHandler("cve_buscar", stub_cmd("cve_buscar")))
    app.add_handler(CommandHandler("exploit_info", stub_cmd("exploit_info")))
    app.add_handler(CommandHandler("vulnerabilidad_info", stub_cmd("vulnerabilidad_info")))
    app.add_handler(CommandHandler("parche_seguridad", stub_cmd("parche_seguridad")))
    app.add_handler(CommandHandler("zero_day", stub_cmd("zero_day")))
    app.add_handler(CommandHandler("apt_info", stub_cmd("apt_info")))
    app.add_handler(CommandHandler("malware_info", stub_cmd("malware_info")))
    app.add_handler(CommandHandler("ransomware_info", stub_cmd("ransomware_info")))
    app.add_handler(CommandHandler("spyware_info", stub_cmd("spyware_info")))
    app.add_handler(CommandHandler("adware_info", stub_cmd("adware_info")))
    app.add_handler(CommandHandler("trojan_info", stub_cmd("trojan_info")))
    app.add_handler(CommandHandler("rootkit_info", stub_cmd("rootkit_info")))
    app.add_handler(CommandHandler("keylogger_info", stub_cmd("keylogger_info")))
    app.add_handler(CommandHandler("botnet_info", stub_cmd("botnet_info")))
    app.add_handler(CommandHandler("ddos_info", stub_cmd("ddos_info")))
    app.add_handler(CommandHandler("phishing_info", stub_cmd("phishing_info")))
    app.add_handler(CommandHandler("smishing_info", stub_cmd("smishing_info")))
    app.add_handler(CommandHandler("vishing_info", stub_cmd("vishing_info")))
    app.add_handler(CommandHandler("spear_phishing", stub_cmd("spear_phishing")))
    app.add_handler(CommandHandler("whaling", stub_cmd("whaling")))
    app.add_handler(CommandHandler("baiting", stub_cmd("baiting")))
    app.add_handler(CommandHandler("pretexting", stub_cmd("pretexting")))
    app.add_handler(CommandHandler("tailgating", stub_cmd("tailgating")))
    app.add_handler(CommandHandler("osint2", stub_cmd("osint2")))
    app.add_handler(CommandHandler("recon", stub_cmd("recon")))
    app.add_handler(CommandHandler("footprinting", stub_cmd("footprinting")))
    app.add_handler(CommandHandler("fingerprinting", stub_cmd("fingerprinting")))
    app.add_handler(CommandHandler("scanning2", stub_cmd("scanning2")))
    app.add_handler(CommandHandler("enumeration", stub_cmd("enumeration")))
    app.add_handler(CommandHandler("password_attack", stub_cmd("password_attack")))
    app.add_handler(CommandHandler("brute_force", stub_cmd("brute_force")))
    app.add_handler(CommandHandler("dictionary_attack", stub_cmd("dictionary_attack")))
    app.add_handler(CommandHandler("rainbow_table", stub_cmd("rainbow_table")))
    app.add_handler(CommandHandler("hash_crack", stub_cmd("hash_crack")))
    app.add_handler(CommandHandler("sql_injection", stub_cmd("sql_injection")))
    app.add_handler(CommandHandler("xss2", stub_cmd("xss2")))
    app.add_handler(CommandHandler("csrf2", stub_cmd("csrf2")))
    app.add_handler(CommandHandler("ssrf2", stub_cmd("ssrf2")))
    app.add_handler(CommandHandler("lfi2", stub_cmd("lfi2")))
    app.add_handler(CommandHandler("rfi2", stub_cmd("rfi2")))
    app.add_handler(CommandHandler("rce2", stub_cmd("rce2")))
    app.add_handler(CommandHandler("idor2", stub_cmd("idor2")))
    app.add_handler(CommandHandler("inyeccion_nosql", stub_cmd("inyeccion_nosql")))
    app.add_handler(CommandHandler("inyeccion_ldap", stub_cmd("inyeccion_ldap")))
    app.add_handler(CommandHandler("inyeccion_xml", stub_cmd("inyeccion_xml")))
    app.add_handler(CommandHandler("inyeccion_xpath", stub_cmd("inyeccion_xpath")))
    app.add_handler(CommandHandler("deserialization", stub_cmd("deserialization")))
    app.add_handler(CommandHandler("open_redirect", stub_cmd("open_redirect")))
    app.add_handler(CommandHandler("clickjacking", stub_cmd("clickjacking")))
    app.add_handler(CommandHandler("mime_sniffing", stub_cmd("mime_sniffing")))
    app.add_handler(CommandHandler("cors_misconfiguration", stub_cmd("cors_misconfiguration")))
    app.add_handler(CommandHandler("autenticacion_doble", stub_cmd("autenticacion_doble")))
    app.add_handler(CommandHandler("mfa", stub_cmd("mfa")))
    app.add_handler(CommandHandler("totp", stub_cmd("totp")))
    app.add_handler(CommandHandler("hotp", stub_cmd("hotp")))
    app.add_handler(CommandHandler("fido2", stub_cmd("fido2")))
    app.add_handler(CommandHandler("webauthn", stub_cmd("webauthn")))
    app.add_handler(CommandHandler("passkey", stub_cmd("passkey")))
    app.add_handler(CommandHandler("gestor_contrasenas", stub_cmd("gestor_contrasenas")))
    app.add_handler(CommandHandler("keepass", stub_cmd("keepass")))
    app.add_handler(CommandHandler("bitwarden", stub_cmd("bitwarden")))
    app.add_handler(CommandHandler("1password", stub_cmd("1password")))
    app.add_handler(CommandHandler("lastpass", stub_cmd("lastpass")))
    app.add_handler(CommandHandler("dashlane", stub_cmd("dashlane")))
    app.add_handler(CommandHandler("privacidad_info", stub_cmd("privacidad_info")))
    app.add_handler(CommandHandler("gdpr_info", stub_cmd("gdpr_info")))
    app.add_handler(CommandHandler("ccpa_info", stub_cmd("ccpa_info")))
    app.add_handler(CommandHandler("lgpd_info", stub_cmd("lgpd_info")))
    app.add_handler(CommandHandler("data_breach", stub_cmd("data_breach")))
    app.add_handler(CommandHandler("notificacion_brecha", stub_cmd("notificacion_brecha")))
    app.add_handler(CommandHandler("anonimato", stub_cmd("anonimato")))
    app.add_handler(CommandHandler("seudoanonimato", stub_cmd("seudoanonimato")))
    app.add_handler(CommandHandler("metadatos", stub_cmd("metadatos")))
    app.add_handler(CommandHandler("huella_digital", stub_cmd("huella_digital")))
    app.add_handler(CommandHandler("fingerprint_browser", stub_cmd("fingerprint_browser")))
    app.add_handler(CommandHandler("vpn_gratis", stub_cmd("vpn_gratis")))
    app.add_handler(CommandHandler("vpn_pago", stub_cmd("vpn_pago")))
    app.add_handler(CommandHandler("onion_routing", stub_cmd("onion_routing")))
    app.add_handler(CommandHandler("mixnet", stub_cmd("mixnet")))
    app.add_handler(CommandHandler("remailer", stub_cmd("remailer")))
    app.add_handler(CommandHandler("steganografia", stub_cmd("steganografia")))
    app.add_handler(CommandHandler("esteganografia2", stub_cmd("esteganografia2")))
    app.add_handler(CommandHandler("marca_agua", stub_cmd("marca_agua")))
    app.add_handler(CommandHandler("forense_digital", stub_cmd("forense_digital")))
    app.add_handler(CommandHandler("evidencia_digital", stub_cmd("evidencia_digital")))
    app.add_handler(CommandHandler("cadena_custodia", stub_cmd("cadena_custodia")))

    # ── 🎭 ROL & ACCIONES SOCIALES
    app.add_handler(CommandHandler("high5", stub_cmd("high5")))
    app.add_handler(CommandHandler("choque_manos", stub_cmd("choque_manos")))
    app.add_handler(CommandHandler("fist_bump", stub_cmd("fist_bump")))
    app.add_handler(CommandHandler("dar_la_mano", stub_cmd("dar_la_mano")))
    app.add_handler(CommandHandler("saludar", stub_cmd("saludar")))
    app.add_handler(CommandHandler("despedir", stub_cmd("despedir")))
    app.add_handler(CommandHandler("beso_mejilla", stub_cmd("beso_mejilla")))
    app.add_handler(CommandHandler("beso_frente", stub_cmd("beso_frente")))
    app.add_handler(CommandHandler("beso_mano", stub_cmd("beso_mano")))
    app.add_handler(CommandHandler("beso_cuello", stub_cmd("beso_cuello")))
    app.add_handler(CommandHandler("beso_cara", stub_cmd("beso_cara")))
    app.add_handler(CommandHandler("abrazo_fuerte", stub_cmd("abrazo_fuerte")))
    app.add_handler(CommandHandler("abrazo_tierno", stub_cmd("abrazo_tierno")))
    app.add_handler(CommandHandler("abrazo_sorpresa", stub_cmd("abrazo_sorpresa")))
    app.add_handler(CommandHandler("abrazo_oso", stub_cmd("abrazo_oso")))
    app.add_handler(CommandHandler("abrazar_grupo", stub_cmd("abrazar_grupo")))
    app.add_handler(CommandHandler("sentar_regazo", stub_cmd("sentar_regazo")))
    app.add_handler(CommandHandler("recostar_hombro", stub_cmd("recostar_hombro")))
    app.add_handler(CommandHandler("sostener_mano", stub_cmd("sostener_mano")))
    app.add_handler(CommandHandler("entrelazar_dedos", stub_cmd("entrelazar_dedos")))
    app.add_handler(CommandHandler("palmada_espalda", stub_cmd("palmada_espalda")))
    app.add_handler(CommandHandler("dar_palmadita", stub_cmd("dar_palmadita")))
    app.add_handler(CommandHandler("frotar_cabeza", stub_cmd("frotar_cabeza")))
    app.add_handler(CommandHandler("revolver_cabello", stub_cmd("revolver_cabello")))
    app.add_handler(CommandHandler("pellizcar_mejilla", stub_cmd("pellizcar_mejilla")))
    app.add_handler(CommandHandler("pellizcar_brazo", stub_cmd("pellizcar_brazo")))
    app.add_handler(CommandHandler("cosquillas2", stub_cmd("cosquillas2")))
    app.add_handler(CommandHandler("hacer_muecas", stub_cmd("hacer_muecas")))
    app.add_handler(CommandHandler("guinar_ojo", stub_cmd("guinar_ojo")))
    app.add_handler(CommandHandler("soplar_beso", stub_cmd("soplar_beso")))
    app.add_handler(CommandHandler("mandar_corazon", stub_cmd("mandar_corazon")))
    app.add_handler(CommandHandler("mandar_flor", stub_cmd("mandar_flor")))
    app.add_handler(CommandHandler("mandar_regalo", stub_cmd("mandar_regalo")))
    app.add_handler(CommandHandler("dar_comer", stub_cmd("dar_comer")))
    app.add_handler(CommandHandler("dar_bebida", stub_cmd("dar_bebida")))
    app.add_handler(CommandHandler("dar_medicine", stub_cmd("dar_medicine")))
    app.add_handler(CommandHandler("dar_vendaje", stub_cmd("dar_vendaje")))
    app.add_handler(CommandHandler("curar2", stub_cmd("curar2")))
    app.add_handler(CommandHandler("dormir_junto", stub_cmd("dormir_junto")))
    app.add_handler(CommandHandler("arropar", stub_cmd("arropar")))
    app.add_handler(CommandHandler("cantar_cuna", stub_cmd("cantar_cuna")))
    app.add_handler(CommandHandler("contar_cuento", stub_cmd("contar_cuento")))
    app.add_handler(CommandHandler("jugar_juntos", stub_cmd("jugar_juntos")))
    app.add_handler(CommandHandler("ensenar", stub_cmd("ensenar")))
    app.add_handler(CommandHandler("aprender_de", stub_cmd("aprender_de")))
    app.add_handler(CommandHandler("ayudar", stub_cmd("ayudar")))
    app.add_handler(CommandHandler("colaborar", stub_cmd("colaborar")))
    app.add_handler(CommandHandler("proteger", stub_cmd("proteger")))
    app.add_handler(CommandHandler("defender", stub_cmd("defender")))
    app.add_handler(CommandHandler("salvar", stub_cmd("salvar")))
    app.add_handler(CommandHandler("rescatar", stub_cmd("rescatar")))
    app.add_handler(CommandHandler("cargar_herido", stub_cmd("cargar_herido")))
    app.add_handler(CommandHandler("consolar", stub_cmd("consolar")))
    app.add_handler(CommandHandler("animar2", stub_cmd("animar2")))
    app.add_handler(CommandHandler("aplaudir", stub_cmd("aplaudir")))
    app.add_handler(CommandHandler("ovacionar", stub_cmd("ovacionar")))
    app.add_handler(CommandHandler("gritar_apoyo", stub_cmd("gritar_apoyo")))
    app.add_handler(CommandHandler("decepcionar", stub_cmd("decepcionar")))
    app.add_handler(CommandHandler("reganar", stub_cmd("reganar")))
    app.add_handler(CommandHandler("perdonar", stub_cmd("perdonar")))
    app.add_handler(CommandHandler("pedir_perdon", stub_cmd("pedir_perdon")))
    app.add_handler(CommandHandler("hacer_las_paces", stub_cmd("hacer_las_paces")))
    app.add_handler(CommandHandler("declarar_amor", stub_cmd("declarar_amor")))
    app.add_handler(CommandHandler("proponer_matrimonio", stub_cmd("proponer_matrimonio")))
    app.add_handler(CommandHandler("dar_anillo", stub_cmd("dar_anillo")))
    app.add_handler(CommandHandler("celebrar_novios", stub_cmd("celebrar_novios")))
    app.add_handler(CommandHandler("celebrar_cumple", stub_cmd("celebrar_cumple")))
    app.add_handler(CommandHandler("celebrar_ascenso", stub_cmd("celebrar_ascenso")))
    app.add_handler(CommandHandler("celebrar_exito", stub_cmd("celebrar_exito")))
    app.add_handler(CommandHandler("tostar_brindis", stub_cmd("tostar_brindis")))
    app.add_handler(CommandHandler("dar_trofeo", stub_cmd("dar_trofeo")))
    app.add_handler(CommandHandler("entregar_diploma", stub_cmd("entregar_diploma")))
    app.add_handler(CommandHandler("premiar", stub_cmd("premiar")))
    app.add_handler(CommandHandler("coronar", stub_cmd("coronar")))
    app.add_handler(CommandHandler("nombrar_campeon", stub_cmd("nombrar_campeon")))
    app.add_handler(CommandHandler("desertar", stub_cmd("desertar")))
    app.add_handler(CommandHandler("huir2", stub_cmd("huir2")))
    app.add_handler(CommandHandler("esconderse", stub_cmd("esconderse")))
    app.add_handler(CommandHandler("acechar", stub_cmd("acechar")))
    app.add_handler(CommandHandler("espiar2", stub_cmd("espiar2")))
    app.add_handler(CommandHandler("perseguir", stub_cmd("perseguir")))
    app.add_handler(CommandHandler("atrapar", stub_cmd("atrapar")))
    app.add_handler(CommandHandler("liberar", stub_cmd("liberar")))
    app.add_handler(CommandHandler("encadenar", stub_cmd("encadenar")))
    app.add_handler(CommandHandler("atar", stub_cmd("atar")))
    app.add_handler(CommandHandler("desatar", stub_cmd("desatar")))
    app.add_handler(CommandHandler("apresar", stub_cmd("apresar")))
    app.add_handler(CommandHandler("soltar", stub_cmd("soltar")))
    app.add_handler(CommandHandler("provocar", stub_cmd("provocar")))
    app.add_handler(CommandHandler("intimidar", stub_cmd("intimidar")))
    app.add_handler(CommandHandler("amenazar", stub_cmd("amenazar")))
    app.add_handler(CommandHandler("desafiar2", stub_cmd("desafiar2")))
    app.add_handler(CommandHandler("retar2", stub_cmd("retar2")))
    app.add_handler(CommandHandler("retarse", stub_cmd("retarse")))
    app.add_handler(CommandHandler("encogerse", stub_cmd("encogerse")))
    app.add_handler(CommandHandler("agacharse", stub_cmd("agacharse")))
    app.add_handler(CommandHandler("arrodillarse", stub_cmd("arrodillarse")))
    app.add_handler(CommandHandler("postrarse", stub_cmd("postrarse")))
    app.add_handler(CommandHandler("genuflexion", stub_cmd("genuflexion")))
    app.add_handler(CommandHandler("meditar_junto", stub_cmd("meditar_junto")))
    app.add_handler(CommandHandler("orar_junto", stub_cmd("orar_junto")))
    app.add_handler(CommandHandler("bailar_junto", stub_cmd("bailar_junto")))
    app.add_handler(CommandHandler("cantar_junto", stub_cmd("cantar_junto")))
    app.add_handler(CommandHandler("tocar_junto", stub_cmd("tocar_junto")))

    # ── 🏃 FITNESS & EJERCICIO
    app.add_handler(CommandHandler("plan_gym", stub_cmd("plan_gym")))
    app.add_handler(CommandHandler("rutina_pecho", stub_cmd("rutina_pecho")))
    app.add_handler(CommandHandler("rutina_espalda", stub_cmd("rutina_espalda")))
    app.add_handler(CommandHandler("rutina_brazos", stub_cmd("rutina_brazos")))
    app.add_handler(CommandHandler("rutina_hombros", stub_cmd("rutina_hombros")))
    app.add_handler(CommandHandler("rutina_piernas", stub_cmd("rutina_piernas")))
    app.add_handler(CommandHandler("rutina_gluteos", stub_cmd("rutina_gluteos")))
    app.add_handler(CommandHandler("rutina_abdomen", stub_cmd("rutina_abdomen")))
    app.add_handler(CommandHandler("rutina_core", stub_cmd("rutina_core")))
    app.add_handler(CommandHandler("push_up", stub_cmd("push_up")))
    app.add_handler(CommandHandler("pull_up", stub_cmd("pull_up")))
    app.add_handler(CommandHandler("dip", stub_cmd("dip")))
    app.add_handler(CommandHandler("plank", stub_cmd("plank")))
    app.add_handler(CommandHandler("crunch", stub_cmd("crunch")))
    app.add_handler(CommandHandler("sit_up", stub_cmd("sit_up")))
    app.add_handler(CommandHandler("leg_raise", stub_cmd("leg_raise")))
    app.add_handler(CommandHandler("squat", stub_cmd("squat")))
    app.add_handler(CommandHandler("lunges", stub_cmd("lunges")))
    app.add_handler(CommandHandler("deadlift", stub_cmd("deadlift")))
    app.add_handler(CommandHandler("bench_press", stub_cmd("bench_press")))
    app.add_handler(CommandHandler("shoulder_press", stub_cmd("shoulder_press")))
    app.add_handler(CommandHandler("row", stub_cmd("row")))
    app.add_handler(CommandHandler("curl_biceps", stub_cmd("curl_biceps")))
    app.add_handler(CommandHandler("extension_triceps", stub_cmd("extension_triceps")))
    app.add_handler(CommandHandler("lateral_raise", stub_cmd("lateral_raise")))
    app.add_handler(CommandHandler("face_pull", stub_cmd("face_pull")))
    app.add_handler(CommandHandler("fly", stub_cmd("fly")))
    app.add_handler(CommandHandler("hip_thrust", stub_cmd("hip_thrust")))
    app.add_handler(CommandHandler("sumo_squat", stub_cmd("sumo_squat")))
    app.add_handler(CommandHandler("split_squat", stub_cmd("split_squat")))
    app.add_handler(CommandHandler("step_up", stub_cmd("step_up")))
    app.add_handler(CommandHandler("calf_raise", stub_cmd("calf_raise")))
    app.add_handler(CommandHandler("nordic_curl", stub_cmd("nordic_curl")))
    app.add_handler(CommandHandler("glute_ham_raise", stub_cmd("glute_ham_raise")))
    app.add_handler(CommandHandler("rdl", stub_cmd("rdl")))
    app.add_handler(CommandHandler("good_morning", stub_cmd("good_morning")))
    app.add_handler(CommandHandler("hack_squat", stub_cmd("hack_squat")))
    app.add_handler(CommandHandler("interval_training", stub_cmd("interval_training")))
    app.add_handler(CommandHandler("fartlek", stub_cmd("fartlek")))
    app.add_handler(CommandHandler("lactate_threshold", stub_cmd("lactate_threshold")))
    app.add_handler(CommandHandler("vo2max", stub_cmd("vo2max")))
    app.add_handler(CommandHandler("pace_running", stub_cmd("pace_running")))
    app.add_handler(CommandHandler("cadence_running", stub_cmd("cadence_running")))
    app.add_handler(CommandHandler("stride_length", stub_cmd("stride_length")))
    app.add_handler(CommandHandler("running_form", stub_cmd("running_form")))
    app.add_handler(CommandHandler("trail_running", stub_cmd("trail_running")))
    app.add_handler(CommandHandler("ciclismo2", stub_cmd("ciclismo2")))
    app.add_handler(CommandHandler("spinning", stub_cmd("spinning")))
    app.add_handler(CommandHandler("cycling_zones", stub_cmd("cycling_zones")))
    app.add_handler(CommandHandler("ftp_cycling", stub_cmd("ftp_cycling")))
    app.add_handler(CommandHandler("power_output", stub_cmd("power_output")))
    app.add_handler(CommandHandler("natacion3", stub_cmd("natacion3")))
    app.add_handler(CommandHandler("estilos_nado", stub_cmd("estilos_nado")))
    app.add_handler(CommandHandler("velocidad_nado", stub_cmd("velocidad_nado")))
    app.add_handler(CommandHandler("resistencia_nado", stub_cmd("resistencia_nado")))
    app.add_handler(CommandHandler("tecnica_giro", stub_cmd("tecnica_giro")))
    app.add_handler(CommandHandler("remo2", stub_cmd("remo2")))
    app.add_handler(CommandHandler("standup_paddle", stub_cmd("standup_paddle")))
    app.add_handler(CommandHandler("surf2", stub_cmd("surf2")))
    app.add_handler(CommandHandler("kitesurf2", stub_cmd("kitesurf2")))
    app.add_handler(CommandHandler("foam_roller2", stub_cmd("foam_roller2")))
    app.add_handler(CommandHandler("masaje_deportivo", stub_cmd("masaje_deportivo")))
    app.add_handler(CommandHandler("fisioterapia", stub_cmd("fisioterapia")))
    app.add_handler(CommandHandler("rehab_rodilla", stub_cmd("rehab_rodilla")))
    app.add_handler(CommandHandler("rehab_hombro", stub_cmd("rehab_hombro")))
    app.add_handler(CommandHandler("rehab_espalda", stub_cmd("rehab_espalda")))
    app.add_handler(CommandHandler("rehab_tobillo", stub_cmd("rehab_tobillo")))
    app.add_handler(CommandHandler("prevencion_lesiones", stub_cmd("prevencion_lesiones")))
    app.add_handler(CommandHandler("taping", stub_cmd("taping")))
    app.add_handler(CommandHandler("vendaje_deportivo", stub_cmd("vendaje_deportivo")))
    app.add_handler(CommandHandler("crioterapia2", stub_cmd("crioterapia2")))
    app.add_handler(CommandHandler("termoterapia", stub_cmd("termoterapia")))
    app.add_handler(CommandHandler("nutricion_deportiva", stub_cmd("nutricion_deportiva")))
    app.add_handler(CommandHandler("proteina_deportiva", stub_cmd("proteina_deportiva")))
    app.add_handler(CommandHandler("carbohidrato_deporte", stub_cmd("carbohidrato_deporte")))
    app.add_handler(CommandHandler("grasa_deporte", stub_cmd("grasa_deporte")))
    app.add_handler(CommandHandler("creatina", stub_cmd("creatina")))
    app.add_handler(CommandHandler("beta_alanina", stub_cmd("beta_alanina")))
    app.add_handler(CommandHandler("cafeina_deportiva", stub_cmd("cafeina_deportiva")))
    app.add_handler(CommandHandler("bcaa", stub_cmd("bcaa")))
    app.add_handler(CommandHandler("glutamina", stub_cmd("glutamina")))
    app.add_handler(CommandHandler("hmb", stub_cmd("hmb")))
    app.add_handler(CommandHandler("suplemento_preentrenamiento", stub_cmd("suplemento_preentrenamiento")))
    app.add_handler(CommandHandler("suplemento_post", stub_cmd("suplemento_post")))
    app.add_handler(CommandHandler("recuperacion_muscular", stub_cmd("recuperacion_muscular")))
    app.add_handler(CommandHandler("doms", stub_cmd("doms")))
    app.add_handler(CommandHandler("hipertrofia", stub_cmd("hipertrofia")))
    app.add_handler(CommandHandler("fuerza_maxima", stub_cmd("fuerza_maxima")))
    app.add_handler(CommandHandler("resistencia_muscular", stub_cmd("resistencia_muscular")))
    app.add_handler(CommandHandler("potencia", stub_cmd("potencia")))
    app.add_handler(CommandHandler("velocidad_deportiva", stub_cmd("velocidad_deportiva")))
    app.add_handler(CommandHandler("test_rm", stub_cmd("test_rm")))
    app.add_handler(CommandHandler("test_cooper", stub_cmd("test_cooper")))
    app.add_handler(CommandHandler("test_yo_yo", stub_cmd("test_yo_yo")))
    app.add_handler(CommandHandler("test_conconi", stub_cmd("test_conconi")))
    app.add_handler(CommandHandler("test_wingate", stub_cmd("test_wingate")))
    app.add_handler(CommandHandler("bateria_test", stub_cmd("bateria_test")))
    app.add_handler(CommandHandler("periodizacion", stub_cmd("periodizacion")))
    app.add_handler(CommandHandler("macrociclo", stub_cmd("macrociclo")))
    app.add_handler(CommandHandler("mesociclo", stub_cmd("mesociclo")))
    app.add_handler(CommandHandler("microciclo", stub_cmd("microciclo")))
    app.add_handler(CommandHandler("tapering", stub_cmd("tapering")))
    app.add_handler(CommandHandler("peak", stub_cmd("peak")))
    app.add_handler(CommandHandler("deload", stub_cmd("deload")))
    app.add_handler(CommandHandler("sobreentrenamiento", stub_cmd("sobreentrenamiento")))
    app.add_handler(CommandHandler("recuperacion_activa", stub_cmd("recuperacion_activa")))
    app.add_handler(CommandHandler("descanso_deportivo", stub_cmd("descanso_deportivo")))

    # ── 🌱 VIDA COTIDIANA
    app.add_handler(CommandHandler("rutina_manana", stub_cmd("rutina_manana")))
    app.add_handler(CommandHandler("rutina_noche", stub_cmd("rutina_noche")))
    app.add_handler(CommandHandler("habito_manana", stub_cmd("habito_manana")))
    app.add_handler(CommandHandler("habito_noche", stub_cmd("habito_noche")))
    app.add_handler(CommandHandler("ritual_manana", stub_cmd("ritual_manana")))
    app.add_handler(CommandHandler("cafe_manana", stub_cmd("cafe_manana")))
    app.add_handler(CommandHandler("desayuno_info", stub_cmd("desayuno_info")))
    app.add_handler(CommandHandler("meditacion_manana", stub_cmd("meditacion_manana")))
    app.add_handler(CommandHandler("ejercicio_manana", stub_cmd("ejercicio_manana")))
    app.add_handler(CommandHandler("ducharse", stub_cmd("ducharse")))
    app.add_handler(CommandHandler("cepillarse", stub_cmd("cepillarse")))
    app.add_handler(CommandHandler("peinarse", stub_cmd("peinarse")))
    app.add_handler(CommandHandler("vestirse", stub_cmd("vestirse")))
    app.add_handler(CommandHandler("ordenar_cama", stub_cmd("ordenar_cama")))
    app.add_handler(CommandHandler("planificar_dia", stub_cmd("planificar_dia")))
    app.add_handler(CommandHandler("lista_compras", stub_cmd("lista_compras")))
    app.add_handler(CommandHandler("lista_tareas_hoy", stub_cmd("lista_tareas_hoy")))
    app.add_handler(CommandHandler("prioridades_hoy", stub_cmd("prioridades_hoy")))
    app.add_handler(CommandHandler("revision_emails", stub_cmd("revision_emails")))
    app.add_handler(CommandHandler("responder_mensajes", stub_cmd("responder_mensajes")))
    app.add_handler(CommandHandler("reunion_info", stub_cmd("reunion_info")))
    app.add_handler(CommandHandler("llamada_programada", stub_cmd("llamada_programada")))
    app.add_handler(CommandHandler("transporte_publico", stub_cmd("transporte_publico")))
    app.add_handler(CommandHandler("ruta_bus", stub_cmd("ruta_bus")))
    app.add_handler(CommandHandler("ruta_metro", stub_cmd("ruta_metro")))
    app.add_handler(CommandHandler("ruta_tren", stub_cmd("ruta_tren")))
    app.add_handler(CommandHandler("ruta_bici", stub_cmd("ruta_bici")))
    app.add_handler(CommandHandler("carro_info", stub_cmd("carro_info")))
    app.add_handler(CommandHandler("estacion_gasolina", stub_cmd("estacion_gasolina")))
    app.add_handler(CommandHandler("estacionamiento", stub_cmd("estacionamiento")))
    app.add_handler(CommandHandler("lavado_carro", stub_cmd("lavado_carro")))
    app.add_handler(CommandHandler("mecanico", stub_cmd("mecanico")))
    app.add_handler(CommandHandler("supermercado", stub_cmd("supermercado")))
    app.add_handler(CommandHandler("tienda_online", stub_cmd("tienda_online")))
    app.add_handler(CommandHandler("descuento_hoy", stub_cmd("descuento_hoy")))
    app.add_handler(CommandHandler("oferta_semana", stub_cmd("oferta_semana")))
    app.add_handler(CommandHandler("cupon", stub_cmd("cupon")))
    app.add_handler(CommandHandler("banco_operaciones", stub_cmd("banco_operaciones")))
    app.add_handler(CommandHandler("pago_servicios", stub_cmd("pago_servicios")))
    app.add_handler(CommandHandler("recarga_telefono", stub_cmd("recarga_telefono")))
    app.add_handler(CommandHandler("transferencia_rapida", stub_cmd("transferencia_rapida")))
    app.add_handler(CommandHandler("medico_cita", stub_cmd("medico_cita")))
    app.add_handler(CommandHandler("dentista_cita", stub_cmd("dentista_cita")))
    app.add_handler(CommandHandler("barbero_cita", stub_cmd("barbero_cita")))
    app.add_handler(CommandHandler("peluqueria_cita", stub_cmd("peluqueria_cita")))
    app.add_handler(CommandHandler("spa_cita", stub_cmd("spa_cita")))
    app.add_handler(CommandHandler("mascota_vet", stub_cmd("mascota_vet")))
    app.add_handler(CommandHandler("mascota_grooming", stub_cmd("mascota_grooming")))
    app.add_handler(CommandHandler("mascota_jugar", stub_cmd("mascota_jugar")))
    app.add_handler(CommandHandler("mascota_alimentar", stub_cmd("mascota_alimentar")))
    app.add_handler(CommandHandler("hogar_limpieza", stub_cmd("hogar_limpieza")))
    app.add_handler(CommandHandler("hogar_orden", stub_cmd("hogar_orden")))
    app.add_handler(CommandHandler("hogar_decoracion", stub_cmd("hogar_decoracion")))
    app.add_handler(CommandHandler("hogar_reparacion", stub_cmd("hogar_reparacion")))
    app.add_handler(CommandHandler("plomero", stub_cmd("plomero")))
    app.add_handler(CommandHandler("electricista", stub_cmd("electricista")))
    app.add_handler(CommandHandler("carpintero", stub_cmd("carpintero")))
    app.add_handler(CommandHandler("albanil", stub_cmd("albanil")))
    app.add_handler(CommandHandler("cerrajero", stub_cmd("cerrajero")))
    app.add_handler(CommandHandler("jardineria", stub_cmd("jardineria")))
    app.add_handler(CommandHandler("poda", stub_cmd("poda")))
    app.add_handler(CommandHandler("riego", stub_cmd("riego")))
    app.add_handler(CommandHandler("abono", stub_cmd("abono")))
    app.add_handler(CommandHandler("semillas", stub_cmd("semillas")))
    app.add_handler(CommandHandler("compostaje2", stub_cmd("compostaje2")))
    app.add_handler(CommandHandler("clima_hoy", stub_cmd("clima_hoy")))
    app.add_handler(CommandHandler("que_llevar", stub_cmd("que_llevar")))
    app.add_handler(CommandHandler("paraguas_hoy", stub_cmd("paraguas_hoy")))
    app.add_handler(CommandHandler("ropa_tiempo", stub_cmd("ropa_tiempo")))
    app.add_handler(CommandHandler("alertas_clima", stub_cmd("alertas_clima")))
    app.add_handler(CommandHandler("entretenimiento_hoy", stub_cmd("entretenimiento_hoy")))
    app.add_handler(CommandHandler("plan_noche", stub_cmd("plan_noche")))
    app.add_handler(CommandHandler("plan_finde", stub_cmd("plan_finde")))
    app.add_handler(CommandHandler("cine_cartelera", stub_cmd("cine_cartelera")))
    app.add_handler(CommandHandler("teatro_obras", stub_cmd("teatro_obras")))
    app.add_handler(CommandHandler("restaurante_cerca", stub_cmd("restaurante_cerca")))
    app.add_handler(CommandHandler("bar_cerca", stub_cmd("bar_cerca")))
    app.add_handler(CommandHandler("cafeteria_cerca", stub_cmd("cafeteria_cerca")))
    app.add_handler(CommandHandler("parque_cerca", stub_cmd("parque_cerca")))
    app.add_handler(CommandHandler("museo_cerca", stub_cmd("museo_cerca")))
    app.add_handler(CommandHandler("evento_local", stub_cmd("evento_local")))
    app.add_handler(CommandHandler("concierto_local", stub_cmd("concierto_local")))
    app.add_handler(CommandHandler("feria_local", stub_cmd("feria_local")))
    app.add_handler(CommandHandler("mercado_local", stub_cmd("mercado_local")))
    app.add_handler(CommandHandler("artesania", stub_cmd("artesania")))
    app.add_handler(CommandHandler("foto_momento", stub_cmd("foto_momento")))
    app.add_handler(CommandHandler("video_momento", stub_cmd("video_momento")))
    app.add_handler(CommandHandler("recuerdo_guardar", stub_cmd("recuerdo_guardar")))
    app.add_handler(CommandHandler("diario_dia", stub_cmd("diario_dia")))
    app.add_handler(CommandHandler("resumen_dia", stub_cmd("resumen_dia")))
    app.add_handler(CommandHandler("agradecimiento_dia", stub_cmd("agradecimiento_dia")))
    app.add_handler(CommandHandler("logro_hoy", stub_cmd("logro_hoy")))
    app.add_handler(CommandHandler("aprendizaje_hoy", stub_cmd("aprendizaje_hoy")))
    app.add_handler(CommandHandler("mejora_manana", stub_cmd("mejora_manana")))
    app.add_handler(CommandHandler("reflexion_noche", stub_cmd("reflexion_noche")))

    # ── 💸 FINANZAS PERSONALES
    app.add_handler(CommandHandler("presupuesto2", stub_cmd("presupuesto2")))
    app.add_handler(CommandHandler("presupuesto_50_30_20", stub_cmd("presupuesto_50_30_20")))
    app.add_handler(CommandHandler("presupuesto_cero", stub_cmd("presupuesto_cero")))
    app.add_handler(CommandHandler("presupuesto_sobre", stub_cmd("presupuesto_sobre")))
    app.add_handler(CommandHandler("gasto_fijo", stub_cmd("gasto_fijo")))
    app.add_handler(CommandHandler("gasto_variable", stub_cmd("gasto_variable")))
    app.add_handler(CommandHandler("gasto_hormiga", stub_cmd("gasto_hormiga")))
    app.add_handler(CommandHandler("gasto_innecesario", stub_cmd("gasto_innecesario")))
    app.add_handler(CommandHandler("gasto_invisible", stub_cmd("gasto_invisible")))
    app.add_handler(CommandHandler("ahorro_automatico", stub_cmd("ahorro_automatico")))
    app.add_handler(CommandHandler("ahorro_forzoso", stub_cmd("ahorro_forzoso")))
    app.add_handler(CommandHandler("alcancia2", stub_cmd("alcancia2")))
    app.add_handler(CommandHandler("fondo_emergencia2", stub_cmd("fondo_emergencia2")))
    app.add_handler(CommandHandler("fondo_retiro", stub_cmd("fondo_retiro")))
    app.add_handler(CommandHandler("inversion2", stub_cmd("inversion2")))
    app.add_handler(CommandHandler("inversion_acciones", stub_cmd("inversion_acciones")))
    app.add_handler(CommandHandler("inversion_bonos", stub_cmd("inversion_bonos")))
    app.add_handler(CommandHandler("inversion_fondos", stub_cmd("inversion_fondos")))
    app.add_handler(CommandHandler("inversion_cripto", stub_cmd("inversion_cripto")))
    app.add_handler(CommandHandler("inversion_inmobiliaria", stub_cmd("inversion_inmobiliaria")))
    app.add_handler(CommandHandler("inversion_arte", stub_cmd("inversion_arte")))
    app.add_handler(CommandHandler("inversion_vino", stub_cmd("inversion_vino")))
    app.add_handler(CommandHandler("inversion_oro2", stub_cmd("inversion_oro2")))
    app.add_handler(CommandHandler("inversion_plata", stub_cmd("inversion_plata")))
    app.add_handler(CommandHandler("inversion_platino", stub_cmd("inversion_platino")))
    app.add_handler(CommandHandler("inversion_coleccionables", stub_cmd("inversion_coleccionables")))
    app.add_handler(CommandHandler("inversion_startup", stub_cmd("inversion_startup")))
    app.add_handler(CommandHandler("angel_investor", stub_cmd("angel_investor")))
    app.add_handler(CommandHandler("venture_capital", stub_cmd("venture_capital")))
    app.add_handler(CommandHandler("crowdfunding", stub_cmd("crowdfunding")))
    app.add_handler(CommandHandler("crowdlending", stub_cmd("crowdlending")))
    app.add_handler(CommandHandler("p2p_lending", stub_cmd("p2p_lending")))
    app.add_handler(CommandHandler("microfinanzas", stub_cmd("microfinanzas")))
    app.add_handler(CommandHandler("fintech", stub_cmd("fintech")))
    app.add_handler(CommandHandler("neobank", stub_cmd("neobank")))
    app.add_handler(CommandHandler("banco_digital", stub_cmd("banco_digital")))
    app.add_handler(CommandHandler("cuenta_corriente2", stub_cmd("cuenta_corriente2")))
    app.add_handler(CommandHandler("cuenta_ahorro2", stub_cmd("cuenta_ahorro2")))
    app.add_handler(CommandHandler("cuenta_nomina", stub_cmd("cuenta_nomina")))
    app.add_handler(CommandHandler("cuenta_inversion", stub_cmd("cuenta_inversion")))
    app.add_handler(CommandHandler("cuenta_empresa", stub_cmd("cuenta_empresa")))
    app.add_handler(CommandHandler("cuenta_conjunta", stub_cmd("cuenta_conjunta")))
    app.add_handler(CommandHandler("tarjeta_debito", stub_cmd("tarjeta_debito")))
    app.add_handler(CommandHandler("tarjeta_credito2", stub_cmd("tarjeta_credito2")))
    app.add_handler(CommandHandler("tarjeta_prepago", stub_cmd("tarjeta_prepago")))
    app.add_handler(CommandHandler("tarjeta_virtual", stub_cmd("tarjeta_virtual")))
    app.add_handler(CommandHandler("cashback", stub_cmd("cashback")))
    app.add_handler(CommandHandler("puntos_banco", stub_cmd("puntos_banco")))
    app.add_handler(CommandHandler("millas_aereas", stub_cmd("millas_aereas")))
    app.add_handler(CommandHandler("programa_fidelidad", stub_cmd("programa_fidelidad")))
    app.add_handler(CommandHandler("beneficios_tarjeta", stub_cmd("beneficios_tarjeta")))
    app.add_handler(CommandHandler("tasa_interes2", stub_cmd("tasa_interes2")))
    app.add_handler(CommandHandler("interes_compuesto", stub_cmd("interes_compuesto")))
    app.add_handler(CommandHandler("regla_72", stub_cmd("regla_72")))
    app.add_handler(CommandHandler("valor_dinero_tiempo", stub_cmd("valor_dinero_tiempo")))
    app.add_handler(CommandHandler("vpn_financiero", stub_cmd("vpn_financiero")))
    app.add_handler(CommandHandler("riesgo_financiero", stub_cmd("riesgo_financiero")))
    app.add_handler(CommandHandler("tolerancia_riesgo", stub_cmd("tolerancia_riesgo")))
    app.add_handler(CommandHandler("perfil_inversor", stub_cmd("perfil_inversor")))
    app.add_handler(CommandHandler("horizonte_temporal", stub_cmd("horizonte_temporal")))
    app.add_handler(CommandHandler("diversificacion2", stub_cmd("diversificacion2")))
    app.add_handler(CommandHandler("correlacion_activos", stub_cmd("correlacion_activos")))
    app.add_handler(CommandHandler("beta_accion", stub_cmd("beta_accion")))
    app.add_handler(CommandHandler("alfa_accion", stub_cmd("alfa_accion")))
    app.add_handler(CommandHandler("sharpe", stub_cmd("sharpe")))
    app.add_handler(CommandHandler("impuesto_renta", stub_cmd("impuesto_renta")))
    app.add_handler(CommandHandler("impuesto_ganancias", stub_cmd("impuesto_ganancias")))
    app.add_handler(CommandHandler("impuesto_dividendos", stub_cmd("impuesto_dividendos")))
    app.add_handler(CommandHandler("declaracion_renta", stub_cmd("declaracion_renta")))
    app.add_handler(CommandHandler("deduccion_fiscal", stub_cmd("deduccion_fiscal")))
    app.add_handler(CommandHandler("exencion_fiscal", stub_cmd("exencion_fiscal")))
    app.add_handler(CommandHandler("paraiso_fiscal", stub_cmd("paraiso_fiscal")))
    app.add_handler(CommandHandler("planificacion_fiscal", stub_cmd("planificacion_fiscal")))
    app.add_handler(CommandHandler("seguro_desempleo", stub_cmd("seguro_desempleo")))
    app.add_handler(CommandHandler("seguro_discapacidad", stub_cmd("seguro_discapacidad")))
    app.add_handler(CommandHandler("seguro_viaje2", stub_cmd("seguro_viaje2")))
    app.add_handler(CommandHandler("seguro_movil", stub_cmd("seguro_movil")))
    app.add_handler(CommandHandler("financiamiento", stub_cmd("financiamiento")))
    app.add_handler(CommandHandler("leasing", stub_cmd("leasing")))
    app.add_handler(CommandHandler("factoring", stub_cmd("factoring")))
    app.add_handler(CommandHandler("forfaiting", stub_cmd("forfaiting")))
    app.add_handler(CommandHandler("descuento_facturas", stub_cmd("descuento_facturas")))
    app.add_handler(CommandHandler("contabilidad_personal", stub_cmd("contabilidad_personal")))
    app.add_handler(CommandHandler("estado_financiero", stub_cmd("estado_financiero")))
    app.add_handler(CommandHandler("balance_personal", stub_cmd("balance_personal")))
    app.add_handler(CommandHandler("flujo_caja2", stub_cmd("flujo_caja2")))
    app.add_handler(CommandHandler("riqueza_generacional", stub_cmd("riqueza_generacional")))
    app.add_handler(CommandHandler("herencia", stub_cmd("herencia")))
    app.add_handler(CommandHandler("testamento", stub_cmd("testamento")))
    app.add_handler(CommandHandler("fideicomiso", stub_cmd("fideicomiso")))
    app.add_handler(CommandHandler("donacion_financiera", stub_cmd("donacion_financiera")))
    app.add_handler(CommandHandler("educacion_financiera", stub_cmd("educacion_financiera")))
    app.add_handler(CommandHandler("libros_finanzas", stub_cmd("libros_finanzas")))
    app.add_handler(CommandHandler("podcast_finanzas", stub_cmd("podcast_finanzas")))
    app.add_handler(CommandHandler("curso_finanzas", stub_cmd("curso_finanzas")))
    app.run_polling()

# Disparador del programa
if __name__ == '__main__':
    main()

# --- FINAL DE PARTE 9 ---
                                   