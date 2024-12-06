# tgbotbase - Universal telegram bot base for bots maded by @abuztrade on aiogram 3.x
### Default settings:
```python
os.environ["LOG_FILENAME"]       = "./logs/bot_{time:DD-MM-YYYY}.log"
os.environ["LOG_FORMAT"]         = "<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <level>{message}</level>"
os.environ["LOG_ROTATION"]       = "2days"
os.environ["LOG_COMPRESSION"]    = "zip"
os.environ["LOG_BACKTRACE_BOOL"] = "True"
os.environ["LOG_DIAGNOSE_BOOL"]  = "True"
os.environ["LOCALES_FOLDER"]     = "locales"
os.environ["LOCALES_STARTSWITH"] = "bot"
os.environ["KEYBOARDS_PATH"]     = "./src/keyboards.yml"
```

## Also should fill SHARED_OBJECTS["dp"] with your root aiogram 3.x dispatcher for keyboord.book works
```python
SHARED_OBJECTS["dp"] = dp
```