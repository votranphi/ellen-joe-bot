# How to run on Development
Only run these commands initial time, because GitHub Actions will do the rest.
```bash
cd path/to/folder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.bot
```

# How to run on Production
Only run these commands initial time, because GitHub Actions will do the rest
```bash
cd path/to/folder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nohup python -u -m src.bot > bot_output.log 2>&1 &
```