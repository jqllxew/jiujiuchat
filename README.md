# lobe-chat-plugin

```bash
docker build -t lobe-chat-plugin:latest .
docker run -d -p 7667:7667 \
  -e DB_URL=mysql+mysqlconnector://root:root123@127.0.0.1:3306/test \
  -e DOMAIN=127.0.0.1:7667
  --name lobe-chat-plugin \
  lobe-chat-plugin
```
