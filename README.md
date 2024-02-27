# webzero-bot

A simple (yet) Telegram bot that removes messages with crypto/NFT related links. 

# How to set up
## I just want to try it out

```bash
git clone https://github.com/needthisforctf/webzero-bot.git && cd webzero-bot
pip install -r requirements.txt # install dependencies
python bot.py
```

## The proper way - via Docker

Adjust the contents of `docker-compose.yaml` in the cloned directory, paste your token in, give it a `docker-compose up -d` and you're good to go. No ports need to be exposed. 