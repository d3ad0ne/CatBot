# CatBot

![Last Commit](https://img.shields.io/gitea/last-commit/n0one/CatBot?gitea_url=https%3A%2F%2Fgit.frik.su&color=FFCC00)

This is a simple telegram bot that sends photos of cats to a user, with an option to subscribe for daily cat photos. User also is able to configure subscription cat pictures quantity.


### Bot uses:
- MinIO object storage
- PostgreSQL database
- Telegram API
- Docker container management platform


### Setup:
- Get your telegram API bot token
- Copy compose.yml file and change environment variables as you need
- `docker compose up`
- Enjoy your own instance of the bot!


### Uploading pictures to MinIO:
For more comfortable pictures uploading you can use `minioPopulator.py` script.
