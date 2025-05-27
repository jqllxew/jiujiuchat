# lobe-chat-plugin

## Docker
```bash
docker build -t lobe-chat-plugin:latest .
cp .env.example .env
docker run -d -p 7667:7667 \
  --env-file .env \
  --name lobe-chat-plugin \
  lobe-chat-plugin
```
