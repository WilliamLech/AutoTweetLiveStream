import asyncio
import logging

from twitter_api import TwitterAPI
from twitch_api import twitch_api
import twitchStreamInfo

# Configuration des logs
LOG_FILE = "/home/autoTweet/bot.log"
logging.basicConfig(
    level=logging.INFO,  # Niveau des logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format des messages de log
    handlers=[
        logging.FileHandler(LOG_FILE),  # Enregistrement des logs dans un fichier
        logging.StreamHandler()        # Affiche aussi les logs dans la console
    ]
)
logger = logging.getLogger(__name__)

TWITCH_USER = "l3chat_"

async def check_if_live_loop():
    logger.info("🔄 Début de la boucle Twitch")
    was_live = False
    while True:
        logger.info(f"📡 Checking Twitch live status for {TWITCH_USER}...")
        try:
            is_live = twitchStreamInfo.TwitchStreamInfo.from_api_response(
                twitch_api.is_user_live(TWITCH_USER)
            )
            logger.info(f"🎯 Résultat : {'LIVE' if is_live is not None else 'offline'}")
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du statut Twitch : {e}")

        if is_live is not None and not was_live:
            logger.info("✅ L3chat_ vient de lancer son stream !")

            was_live = True
            TwitterAPI().tweet(is_live.data.category, is_live.data.title)

        elif is_live is None and was_live:
            logger.info("❌ L3chat_ a coupé son stream.")
            was_live = False

        else:
            logger.info(f"🔁 Vérif Twitch : {'LIVE' if is_live is not None else 'offline'}")

        await asyncio.sleep(300)  # 5 minutes (en secondes !)

# À démarrer au lancement de ton bot
async def main():
    logger.info("🚀 Le bot démarre !")
    asyncio.create_task(check_if_live_loop())
    # Ton bot peut continuer sa vie ici
    while True:
        await asyncio.sleep(3600)  # Ou ton event loop

if __name__ == "__main__":
    asyncio.run(main())