# How to run on Development
```bash
pip install -r requirements.txt
python -m src.bot
```

# How to run on Production
```bash
pip install -r requirements.txt
nohup python ellen_joe_bot.py > bot_output.log 2>&1 &
```