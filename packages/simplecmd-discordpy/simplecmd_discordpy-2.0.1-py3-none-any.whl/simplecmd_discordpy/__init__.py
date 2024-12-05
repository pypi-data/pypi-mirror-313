import discord
import os
import importlib
import shutil

def clear_pycache(folder):
    pycache_path = os.path.join(folder, "__pycache__")
    if os.path.exists(pycache_path):
        shutil.rmtree(pycache_path)
        
commands = {}

def command(cmd):
    def decorator(func):
        commands[cmd] = func
        return func
    return decorator

class ConfigCmd:
    def __init__(self):
        self.settings = {"logs": True, "prefix": "$", "folder": ""}
    def set(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.settings:
                self.settings[key] = value
            else:
                raise KeyError(f"Configuração '{key}' não encontrada.")
    def get(self, key):
        return self.settings.get(key, None)
config = ConfigCmd()

async def load(message):
    content = message.content
    prefix = str(config.get("prefix"))
    normalized_content = content.lower()
    for cmd, func in commands.items():
        normalized_cmd = (prefix + cmd).lower()
        if normalized_content.startswith(normalized_cmd):
            args = content[len(prefix + cmd):].strip().split()
            try:
                if args:
                    if config.get("logs"):
                        print(f"• {prefix}{cmd} Called!! [ {message.author.name} ]")
                    await func(message, *args)
                else:
                    if config.get("logs"):
                        print(f"• {prefix}{cmd} Called!! [ {message.author.name} ]")
                    await func(message)
            except Exception as e:
                print(f"Erro ao executar o comando '{cmd}': {e}")
            return

async def load_files(message, client):
    folder = config.get("folder")
    prefix = str(config.get("prefix"))
    content = message.content
    if not os.path.exists(folder):
        os.makedirs(folder)
        if config.get("logs"):
            print(f"Pasta '{folder}' criada. Adicione seus comandos nesta pasta.")
        return
        
    for filename in os.listdir(folder):
        if filename.endswith(".py"):
            command_name = filename[:-3]
            module_path = f"{folder}.{command_name}"
            try:
                clear_pycache(folder)
                module = importlib.import_module(module_path)
                importlib.reload(module)
                normalized_cmd = (prefix + command_name).lower()
                if content.lower().startswith(normalized_cmd):
                    args = content[len(normalized_cmd):].strip().split()
                    if hasattr(module, "run"): 
                        if config.get("logs"):
                            print(f"• {prefix}{command_name} Called!! [ {message.author.name} ]")
                        if args:
                            await module.run(message, client, *args)
                        else:
                            await module.run(message, client)
            except Exception as e:
                print(f"Erro ao carregar ou executar o comando '{command_name}': {e}")