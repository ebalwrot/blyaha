{\rtf1\ansi\ansicpg1251\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import logging\
import requests\
from telegram import Update\
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes\
from dotenv import load_dotenv\
\
# \uc0\u1047 \u1072 \u1075 \u1088 \u1091 \u1078 \u1072 \u1077 \u1084  \u1087 \u1077 \u1088 \u1077 \u1084 \u1077 \u1085 \u1085 \u1099 \u1077  \u1086 \u1082 \u1088 \u1091 \u1078 \u1077 \u1085 \u1080 \u1103  \u1080 \u1079  .env\
load_dotenv()\
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")\
API_KEY = os.getenv("API_KEY")\
\
SYMBOLS = \{\
    "sp500": "SPX",\
    "nas100": "NDX"\
\}\
\
logging.basicConfig(level=logging.INFO)\
\
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):\
    await update.message.reply_text(\
        "\uc0\u55357 \u56395  \u1055 \u1088 \u1080 \u1074 \u1077 \u1090 ! \u1071  \u1073 \u1086 \u1090  \u1076 \u1083 \u1103  \u1088 \u1072 \u1089 \u1095 \u1105 \u1090 \u1072  \u1083 \u1086 \u1090 \u1072  \u1087 \u1086  \u1080 \u1085 \u1076 \u1077 \u1082 \u1089 \u1072 \u1084 .\\n\\n"\
        "\uc0\u1048 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1081  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1091 :\\n"\
        "/lot \uc0\u1080 \u1085 \u1076 \u1077 \u1082 \u1089  \u1076 \u1077 \u1087 \u1086 \u1079 \u1080 \u1090  \u1088 \u1080 \u1089 \u1082  \u1089 \u1090 \u1086 \u1087 \u1083 \u1086 \u1089 \u1089 \\n\\n"\
        "\uc0\u1055 \u1088 \u1080 \u1084 \u1077 \u1088 :\\n"\
        "/lot sp500 1000 2 20"\
    )\
\
async def lot(update: Update, context: ContextTypes.DEFAULT_TYPE):\
    try:\
        _, symbol, deposit, risk, stop_loss = update.message.text.strip().split()\
        deposit = float(deposit)\
        risk = float(risk)\
        stop_loss = float(stop_loss)\
\
        if symbol not in SYMBOLS:\
            await update.message.reply_text("\uc0\u9888 \u65039  \u1055 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1080 \u1074 \u1072 \u1102 \u1090 \u1089 \u1103  \u1090 \u1086 \u1083 \u1100 \u1082 \u1086 : sp500 \u1080  nas100")\
            return\
\
        price = get_price(SYMBOLS[symbol])\
        if not price:\
            await update.message.reply_text("\uc0\u10060  \u1054 \u1096 \u1080 \u1073 \u1082 \u1072  \u1087 \u1086 \u1083 \u1091 \u1095 \u1077 \u1085 \u1080 \u1103  \u1094 \u1077 \u1085 \u1099  \u1089  API.")\
            return\
\
        risk_amount = deposit * (risk / 100)\
        point_value = 0.01  # \uc0\u1069 \u1090 \u1086  \u1084 \u1086 \u1078 \u1077 \u1090  \u1084 \u1077 \u1085 \u1103 \u1090 \u1100 \u1089 \u1103  \u1091  \u1088 \u1072 \u1079 \u1085 \u1099 \u1093  \u1073 \u1088 \u1086 \u1082 \u1077 \u1088 \u1086 \u1074 \
        lot = round(risk_amount / (stop_loss * point_value), 2)\
\
        await update.message.reply_text(\
            f"\uc0\u55357 \u56522  \u1048 \u1085 \u1076 \u1077 \u1082 \u1089 : \{symbol.upper()\}\\n"\
            f"\uc0\u55357 \u56496  \u1062 \u1077 \u1085 \u1072 : \{price\}\\n"\
            f"\uc0\u55357 \u56508  \u1044 \u1077 \u1087 \u1086 \u1079 \u1080 \u1090 : $\{deposit\}\\n"\
            f"\uc0\u55357 \u56521  \u1056 \u1080 \u1089 \u1082 : \{risk\}%\\n"\
            f"\uc0\u55357 \u56527  \u1057 \u1090 \u1086 \u1087 -\u1083 \u1086 \u1089 \u1089 : \{stop_loss\} \u1087 \u1091 \u1085 \u1082 \u1090 \u1086 \u1074 \\n"\
            f"\uc0\u9989  \u1056 \u1077 \u1082 \u1086 \u1084 \u1077 \u1085 \u1076 \u1091 \u1077 \u1084 \u1099 \u1081  \u1083 \u1086 \u1090 : \{lot\}"\
        )\
    except Exception as e:\
        logging.error(e)\
        await update.message.reply_text("\uc0\u9888 \u65039  \u1055 \u1088 \u1086 \u1074 \u1077 \u1088 \u1100  \u1092 \u1086 \u1088 \u1084 \u1072 \u1090  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1099 . \u1055 \u1088 \u1080 \u1084 \u1077 \u1088 : /lot sp500 1000 2 20")\
\
def get_price(symbol: str):\
    try:\
        url = f"https://api.twelvedata.com/price?symbol=\{symbol\}&apikey=\{API_KEY\}"\
        response = requests.get(url).json()\
        return float(response['price'])\
    except:\
        return None\
\
if __name__ == '__main__':\
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()\
    app.add_handler(CommandHandler("start", start))\
    app.add_handler(CommandHandler("lot", lot))\
    app.run_polling()}