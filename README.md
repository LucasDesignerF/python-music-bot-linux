
# Bot de Música para Discord

Este é um bot de música para Discord que permite buscar e tocar músicas diretamente de links do YouTube, além de gerenciar uma fila de reprodução. Ele utiliza a biblioteca `disnake` para a interação com o Discord e o `yt-dlp` para obter as informações e o áudio das músicas do YouTube. **VERSÃO LINUX**

## Funcionalidades

- Tocar músicas do YouTube utilizando o nome ou URL.
- Adicionar músicas a uma fila de reprodução.
- Pausar, retomar, pular músicas e limpar a fila.
- Mostrar a fila atual de músicas.
- Limitar a duração das músicas (configurável).
- Suporte a cookies do YouTube para contornar restrições geográficas.

## Pré-requisitos

Antes de rodar o bot, certifique-se de que você tem as seguintes dependências instaladas:

- Python 3.8 ou superior
- `disnake`
- `yt-dlp`
- `ffmpeg` (binários necessários para a reprodução de áudio)

## Estrutura do Projeto

- **bot.py**: Arquivo principal para execução do bot.
- **cogs/music.py**: Contém a lógica do bot de música.
- **bin/**: Pasta com os binários necessários (ex: `ffmpeg`).
- **ck/**: Pasta contendo o arquivo de cookies (`youtube_cookies.txt`), necessário para contornar restrições geográficas em certos vídeos.

## Como Instalar e Configurar

### 1. Clonar o Repositório

Clone o repositório para sua máquina local:

```bash
git clone https://github.com/LucasDesignerF/python-music-bot-linux.git
cd python-music-bot-linux
```

### 2. Criar um Ambiente Virtual (opcional)

É recomendado criar um ambiente virtual para isolar as dependências do projeto:

```bash
python3 -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate  # Para Windows
```

### 3. Instalar as Dependências

Com o ambiente virtual ativado (se você o criou), instale as dependências:

```bash
pip install -r requirements.txt
```

Certifique-se de que o `ffmpeg` está instalado corretamente. Coloque o binário do `ffmpeg` dentro da pasta `bin/`.

### 4. Configurar o Token do Discord

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo, substituindo `SEU_TOKEN` pelo token do seu bot do Discord:

```
DISCORD_TOKEN=SEU_TOKEN
```

### 5. Configurar os Cookies do YouTube

Coloque o arquivo de cookies do YouTube no formato `.txt` dentro da pasta `ck/` e nomeie-o como `youtube_cookies.txt`. Isso é útil para contornar restrições geográficas de certos vídeos.

## Como Usar o Bot

### 1. Iniciar o Bot

Para iniciar o bot, execute o seguinte comando:

```bash
python bot.py
```

Se tudo estiver configurado corretamente, o bot estará online e pronto para uso no seu servidor do Discord.

### 2. Comandos Disponíveis

Aqui estão os principais comandos que você pode usar com o bot:

- **/play [nome ou URL]**: Toca uma música com base no nome ou na URL fornecida. Se houver uma música tocando, a nova música será adicionada à fila.
- **/queue**: Mostra a fila atual de músicas.
- **/pause**: Pausa a música atual.
- **/resume**: Retoma a música pausada.
- **/skip**: Pula a música atual e toca a próxima da fila.
- **/leave**: O bot sai do canal de voz e limpa a fila de músicas.

### 3. Limitação de Duração de Música

O bot tem uma limitação de duração de música de 2 horas. Se uma música exceder esse limite, ela não será adicionada à fila.

## Exemplo de Uso

1. Digite `/play` seguido do nome ou URL da música. O bot buscará a música no YouTube e a tocará.
2. Para pausar a música, use o comando `/pause`.
3. Para retomar a música, use `/resume`.
4. Para pular a música atual, use `/skip`.
5. Para verificar a fila de músicas, utilize `/queue`.

## Problemas Conhecidos

- **Latency ou heartbeat block**: Ocasionalmente, ao tocar músicas de longa duração (mais de 1 hora), pode ocorrer um erro de "heartbeat blocked". Isso pode ser causado por limitações do servidor ou sobrecarga do loop de eventos.
- **Geoblocking**: Para contornar restrições geográficas de certos vídeos, certifique-se de ter cookies válidos dentro da pasta `ck/`.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir um PR ou relatar problemas na seção de Issues.

## Licença

Este projeto está licenciado sob os termos da licença MIT. Consulte o arquivo LICENSE para obter mais informações.
