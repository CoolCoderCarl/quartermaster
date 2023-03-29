# quartermaster
Search offers in idealista.org and send to telegram

Thanks Idealista team for approve my request which made this bot to live

## Prehistory
I want to find the best flat and do it fast.

> Let the home be found   
> (c) Author

This bot search and show you any offer you ask

Enjoy.

## How to use
You need to pass couple of params in `docker-compose.yaml` envs:  
**APIKEY_SECRET_B64E** - ask the Idealista for it  
**TELEGRAM_BOT_TOKEN** - ask the BotFather for it  
**TELEGRAM_CHAT_ID** - the ID for channel you want to send results  
**PROPERTY_TYPE** - such as "home" or "flat"  
**OPERATION** - "sell" or "rent"  
**LATITUDE** - special digit №1  
**LONGITUDE** - special digit №2  
**DISTANCE** - actually it is the radius whose center is specified using the two previous parameters, in meters  
**MAXITEMS** - how many items per page  

### Example 

Just like this:
```
- APIKEY_SECRET_B64E=qwertyasdfgh1234567890ZXCVBNMHJKLYUIOP
- TELEGRAM_BOT_TOKEN=123456789:QWERTYUIOPASDFGHJKLZXCVBNM
- TELEGRAM_CHAT_ID=-1001234567891011
- PROPERTY_TYPE=homes
- OPERATION=rent
- LATITUDE=34.509143
- LONGITUDE=-41.418267
- DISTANCE=16000
- ITEMS=20
```
