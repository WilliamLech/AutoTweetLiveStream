import asyncio

from twitter_api import TwitterAPI
from twitch_api import twitch_api
import twitchStreamInfo

TWITCH_USER = "l3chat_"

async def check_if_live_loop():
    print("🔄 Début de la boucle Twitch")
    was_live = False
    while True:
        print(f"📡 Checking Twitch live status for {TWITCH_USER}...")
        try:
         is_live =  twitchStreamInfo.TwitchStreamInfo.from_api_response(twitch_api.is_user_live(TWITCH_USER))
         print(f"🎯 Résultat : {'LIVE' if is_live is not None else 'offline'}")
        except Exception as e:
            print({e})

        if is_live is not None and not was_live:
            print("✅ L3chat_ vient de lancer son stream !")

            was_live = True
            TwitterAPI().tweet(is_live.data.category, is_live.data.title)

        elif is_live is None and was_live:
            print("❌ L3chat_ a coupé son stream.")
            was_live = False

        else:
            print(f"🔁 Vérif Twitch : {'LIVE' if is_live is not None else 'offline'}")

        await asyncio.sleep(300000)  # ⏱️ toutes les 5 minutes

# À démarrer au lancement de ton bot
async def main():
    print("🚀 Le bot démarre !")
    asyncio.create_task(check_if_live_loop())
    # Ton bot peut continuer sa vie ici
    while True:
        await asyncio.sleep(3600)  # Ou ton event loop

if __name__ == "__main__":
    asyncio.run(main())
