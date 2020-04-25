# telegram-dice-maestro

I roll dice.

To roll a dice use the command `/roll` or `/roll 1d20` or `/roll 3d8+5`

## Dockerhub Image

Images are built by Travis to
[`lawliet89/telegram-dice-roller`](https://hub.docker.com/r/lawliet89/telegram-dice-roller).

## Example Docker Compose

```yaml
version: "2.4"
services:
    bot:
        image: lawliet89/telegram-dice-roller:latest
    environment:
        TELEGRAM_TOKEN: "token"
```

## Example Docker

Export your telegram API token with `export TELEGRAM_TOKEN="Your token"`

```
docker run --name telegram_dice_bot -e TELEGRAM_TOKEN telegram_dice_roller:latest
```
If you want to build the container locally you can use `docker build -t telegram_dice_roller .`
