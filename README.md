# telegram-dice-maestro

I roll dice.

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
