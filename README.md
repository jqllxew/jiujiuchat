# jiujiu-chat

## Python 3.11

## Docker
```bash
docker build -t jiujiu-chat:latest .
cp .env.example .env
docker run -d -p 7667:7667 \
  --env-file .env \
  --name jiujiu-chat \
  jiujiu-chat
```

## Alembic
```bash
# 生成变更脚本
alembic revision --autogenerate -m "xxx"
```
