from remindme_bot import __app_name__, ERRORS, discord_cli, database
bot = discord_cli.bot
db = database
import os
from dotenv import load_dotenv

def main():
    try:
        db.init_database()
    except Exception as e:
        print(e)
    try:
        load_dotenv()
    except Exception as e:
        print(e)
    
    token = os.getenv('TOKEN') #change this when running locally
    if token is None:
        raise ValueError("No TOKEN found in environment variables.")

    #Run the bot
    try:
        bot.run(token)
    except Exception as e:
        print(e)
        

if __name__ == "__main__":
    main()