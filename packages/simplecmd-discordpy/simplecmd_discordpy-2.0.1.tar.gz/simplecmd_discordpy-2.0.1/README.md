# **simplecmd_discordpy**

**(PT-BR):** Biblioteca simples para criar comandos no `discord.py`, ideal para iniciantes. Não visa substituir outras bibliotecas, mas oferece uma maneira fácil de configurar e organizar comandos para bots no Discord.

**(ENG):** A simple library to create commands for `discord.py`, perfect for beginners. It doesn't aim to replace other libraries, but provides an easier way to set up and organize commands for Discord bots.

---

## **Instalação**

Para instalar a biblioteca, execute o seguinte comando:
```bash
pip install simplecmd_discordpy
```


## Usage example
```python
import simplecmd_discordpy as scmd
import discord

TOKEN = "your_token_here"
scmd.config.set(logs=True, prefix=f"$") # Adiciona as configurações necessárias

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@scmd.command("ping") # Função para criar comandos
async def ping_cmd(msg, client, *args):
    if args:
        await msg.channel.send(f"Pong🏓" + ''.join(args[0]), reference=msg)
    else:
        await msg.channel.send(f"Pong🏓", reference=msg)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id == client.user.id:
        return
    await scmd.load(message) # Carrega Todos Os Comandos
client.run(TOKEN)
```

## Example by Folder
```python
import discord
import simplecmd_discordpy as scmd

TOKEN = "your_token_here"
scmd.config.set(logs=True, prefix="$", folder="commands") # Adiciona as configurações necessárias

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    await scmd.load_files(message, client) # Carrega todos os comandos por arquivo

client.run(TOKEN)
```

* Já no arquivo `commands/say.py`
```python
import discord

async def run(msg, client, *args):
    if args:
        # Se houver argumentos passados para o comando
        argumento = " ".join(args)  # Junta todos os argumentos em uma única string
        await msg.channel.send(argumento)
    else:
        # Se não houver argumentos
        await msg.channel.send("Você precisa mencionar alguma coisa que o bot deve falar")
```