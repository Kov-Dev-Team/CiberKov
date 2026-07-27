import utils
import asyncio
import discord
import yt_dlp
from classes import ccf, clp
from typing import Optional
from discord.ext import commands
from discord import app_commands
from discord import ui
from datetime import datetime
from datetime import timedelta


GUILD_IDS = [1162538768394367016, 1469139801365151787]
MY_GUILDS = [discord.Object(id=guild_id) for guild_id in GUILD_IDS]


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        for guild_obj in MY_GUILDS:
            self.tree.copy_global_to(guild=guild_obj)
            await self.tree.sync(guild=guild_obj)

        print(f"Sincronização concluída para {len(MY_GUILDS)} servidores.")


# Em vez de Intents.all(), liste só o que você realmente usa.
# Isso evita que o bot falhe ao logar caso você não tenha habilitado
# os intents privilegiados (presences/members) no Developer Portal.
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True       # descomente se precisar (intent privilegiado)
intents.presences = True     # descomente se precisar (intent privilegiado)

client = MyClient(intents=intents)

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'logtostderr': False,
    'retries': 3,
}

FFMPEG_OPTIONS = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}


def _is_url(text: str) -> bool:
    return text.startswith("http://") or text.startswith("https://")


async def resolve_track(query: str) -> Optional[dict]:
    """
    Aceita tanto uma URL do YouTube quanto um termo de busca livre.
    Se não for uma URL, faz uma busca (ytsearch:) e pega o primeiro resultado.
    Roda em thread separada porque extract_info é bloqueante (I/O).

    Retorna um dict com 'url' (link direto do áudio), 'title' e 'webpage_url',
    ou None se não encontrar/der erro.
    """
    search_target = query if _is_url(query) else f"ytsearch1:{query}"

    def _extract():
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
            info = ydl.extract_info(search_target, download=False)
            # Quando é busca (ytsearch), o resultado vem dentro de 'entries'
            if 'entries' in info:
                if not info['entries']:
                    return None
                info = info['entries'][0]
            return info

    try:
        info = await asyncio.to_thread(_extract)
        if info is None:
            return None
        return {
            'url': info['url'],
            'title': info.get('title', 'Título desconhecido'),
            'webpage_url': info.get('webpage_url', query),
        }
    except Exception as e:
        print(f"Erro ao obter a URL do áudio: {e}")
        return None


async def get_audio_source(track: dict) -> Optional[discord.FFmpegPCMAudio]:
    """Cria o AudioSource do FFmpeg a partir de um track já resolvido por resolve_track."""
    try:
        return discord.FFmpegPCMAudio(track['url'], **FFMPEG_OPTIONS)
    except Exception as e:
        print(f"Erro ao criar o audio source: {e}")
        return None


def after_playback(error, interaction: discord.Interaction, query: str):
    if error:
        print(f"Erro no player: {error}")
        # Bug corrigido: era "bot.loop", mas o client se chama "client".
        asyncio.run_coroutine_threadsafe(
            reconnect_and_play(interaction, query),
            client.loop
        )
    else:
        print("Reprodução concluída com sucesso.")


async def reconnect_and_play(interaction: discord.Interaction, query: str):
    await asyncio.sleep(2)

    voice_client = interaction.guild.voice_client if interaction.guild else None

    if voice_client and voice_client.is_connected() and not voice_client.is_playing():
        await interaction.followup.send(
            "Ocorreu uma interrupção na rede. Tentando reconectar e continuar a reprodução...",
            ephemeral=True
        )

        # Re-resolve do zero: a URL direta de áudio do yt_dlp expira,
        # então não dá pra só tentar tocá-la de novo.
        track = await resolve_track(query)
        new_source = await get_audio_source(track) if track else None

        if new_source:
            voice_client.play(
                new_source,
                after=lambda e: after_playback(e, interaction, query)
            )
            await interaction.followup.send("Reconexão bem-sucedida! Continuando a reprodução.")
        else:
            await interaction.followup.send(
                "Não foi possível obter uma nova URL de áudio. A reprodução foi encerrada.",
                ephemeral=True
            )


@client.event
async def on_ready():
    print(f'Online como: {client.user} (ID: {client.user.id})')
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name="Comendo o cu de curisoso")
    )
        
        
def e_dono():
    async def predicate(interaction: discord.Interaction) -> bool:
        ID_DONO = 1047129198508113990 
        return interaction.user.id == ID_DONO
    return app_commands.check(predicate)        
        
       
@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
async def cons_fed(interaction: discord.Interaction):
    """
    Comando que mostra a ConstituiÇão Federal da BiahKov Federation
    """
    
    comp = ccf()
    
    m = discord.AllowedMentions(roles=True)
    
    await interaction.response.defer()

    await interaction.followup.send(view=comp, allowed_mentions=m, silent=False)
    
    
@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
async def livepix(interaction: discord.Interaction):
    """
    Comando que Mostra os tipos de doações e valores dos cargos via LivePix
    """

    comp = clp()
    
    m = discord.AllowedMentions(roles=True)
    
    await interaction.response.defer()
    
    await interaction.followup.send(view=comp, allowed_mentions=m, silent=False)


class BOLayout(ui.LayoutView):
    def __init__(
        self,
        usuario,
        descricao,
        regra,
        agravo,
        deliberacao,
        executor,
        fichador):
        super().__init__()
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        
        container = ui.Container(ui.TextDisplay('# 📝 Boletim de Ocorrência'), accent_color=discord.Colour.purple())
        container.add_item
        (ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))
        container.add_item(ui.TextDisplay(
            f"-# ID de Usuário: {usuario.id}"
            ))
        
        container.add_item
        (ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small))
        container.add_item(ui.TextDisplay(
            f"### Descrição da Ocorrência:\n{descricao}"
            ))
        container.add_item
        (ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small))
        container.add_item(ui.TextDisplay(
            f"### Regras infligidas:\n{regra}"
            ))
        if agravo and agravo.strip():
          container.add_item(ui.TextDisplay(
              f"- Agravos:\n {agravo}"
              ))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small))
        container.add_item(ui.TextDisplay(
            f"### Deliberação:\n{deliberacao}"
            ))
        container.add_item(ui.TextDisplay(
            f"-# Moderador executor ({executor})"
            f"\n-# Moderador fichador ({fichador})"
            f"\n-# Kov Secret Archives - {data_hoje}"
        ))
        self.add_item(container)


class TagDropdown(ui.Select):
    def __init__(self, options, parent_view):
        super().__init__(placeholder="Escolha uma tag para a postagem:", options=options)
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.parent_view.autor:
            return await interaction.response.send_message("❌ Apenas quem iniciou o comando pode escolher a tag.", ephemeral=True)

        tag_id = int(self.values[0])
        tag_obj = discord.utils.get(self.parent_view.forum_channel.available_tags, id=tag_id)

        layout_bo = BOLayout(
            self.parent_view.usuario, 
            self.parent_view.descricao, 
            self.parent_view.regra, 
            self.parent_view.agravo, 
            self.parent_view.deliberacao, 
            self.parent_view.executor, 
            self.parent_view.autor
        )


        await self.parent_view.forum_channel.create_thread(
            name=self.parent_view.titulo,
            view=layout_bo, 
            applied_tags=[tag_obj]
        )

        await interaction.response.edit_message(content=f"✅ BO registrado com sucesso!", view=None)

class TagSelectView(ui.View):
    def __init__(self, forum_channel, titulo, autor, usuario, descricao, regra, agravo, deliberacao, executor):
        super().__init__(timeout=60)
        self.forum_channel = forum_channel
        self.titulo = titulo
        self.autor = autor
        self.usuario = usuario
        self.descricao = descricao
        self.regra = regra
        self.agravo = agravo
        self.deliberacao = deliberacao
        self.executor = executor

        
        options = [
            discord.SelectOption(label=tag.name, value=str(tag.id)) 
            for tag in forum_channel.available_tags[:25]
        ]
        
        self.add_item(TagDropdown(options, self))



@client.tree.command(name="boletim")
@app_commands.default_permissions(manage_messages=True)
async def boletim(
    interaction: discord.Interaction, 
    usuario: discord.User, 
    descricao: str, 
    regra: str,
    deliberacao: str, 
    executor: str,
    agravo: str = None,
):
    """
    Cria um Boletim de Ocorrência e registra ele no fórum da Federação
    """
    FORUM_PUBLICO_ID = 1385039617727922288
    forum = client.get_channel(FORUM_PUBLICO_ID)
    
    if forum is None:
        forum = await client.fetch_channel(FORUM_PUBLICO_ID)

    if not isinstance(forum, discord.ForumChannel):
        return await interaction.response.send_message("❌ Erro: O canal configurado não é um fórum.", ephemeral=True)

    data_titulo = datetime.now().strftime("%d/%m/%Y")
    titulo = f"B.O - {usuario.name} - {data_titulo}"

    view = TagSelectView(
        forum_channel=forum, 
        titulo=titulo, 
        autor=interaction.user,
        usuario=usuario, 
        descricao=descricao, 
        regra=regra, 
        agravo=agravo, 
        deliberacao=deliberacao, 
        executor=executor
    )
    
    await interaction.response.send_message(
        f"📝 Preparando registro para o servidor **{forum.guild.name}**.\nSelecione a Tag:", 
        view=view, 
        ephemeral=True
    )

@client.tree.command(name="conectar")
@app_commands.default_permissions(manage_messages=True)
@discord.app_commands.describe(canal="Canal de interesse")
async def conectar(interaction: discord.Interaction, canal: discord.VoiceChannel):
    """
    Conecta a CiberKov em um canal de voz.
    """
    await interaction.response.defer(ephemeral=True)
    
    if interaction.guild.voice_client:
        voice_client = interaction.guild.voice_client
        await voice_client.disconnect()
        await canal.connect()
        await interaction.followup.send("Saí do canal anterior, conecatdo agora no novo.", ephemeral=True)
        return
    else:    
        await canal.connect()
        await interaction.followup.send("Conectado no canal.", ephemeral=True)

@client.tree.command()
async def desconectar(interaction: discord.Interaction):
    """
    Disconecta o bot do canal
    """
    
    await interaction.response.defer(ephemeral=True)
    
    if interaction.guild.voice_client:
        voice_client = interaction.guild.voice_client
        await voice_client.disconnect()
        await interaction.followup.send("Saí do canal", ephemeral=True)

# ==================== ESTRUTURAS DE FILA ====================

class GuildMusicState:
    def __init__(self):
        self.queue: list[dict] = []
        self.current: dict | None = None
        self.loop_mode: bool = False
        self.now_playing_message: discord.Message | None = None
        self.text_channel: discord.abc.Messageable | None = None
        self.voice_client: discord.VoiceClient | None = None
        self.lock = asyncio.Lock()

    def next_track(self) -> dict | None:
        if self.loop_mode and self.current:
            return self.current
        if self.queue:
            return self.queue.pop(0)
        return None


music_states: dict[int, GuildMusicState] = {}

def get_state(guild_id: int) -> GuildMusicState:
    if guild_id not in music_states:
        music_states[guild_id] = GuildMusicState()
    return music_states[guild_id]


# ==================== HELPER: STATUS DO CANAL DE VOZ ====================

async def set_voice_status(voice_channel: discord.VoiceChannel, text: str):
    try:
        await voice_channel.edit(status=text)
    except discord.HTTPException as e:
        print(f"Não foi possível definir status do canal: {e}")
    except AttributeError:
        print("Sua versão do discord.py não suporta status de canal de voz. Atualize para >= 2.4.")


# ==================== LAYOUT VIEW (COMPONENTS V2) ====================

class PlayerView(discord.ui.LayoutView):
    def __init__(self, guild_id: int, track: dict, queue_size: int, loop: bool):
        super().__init__(timeout=None)
        self.guild_id = guild_id

        mins, secs = divmod(int(track.get("duration") or 0), 60)
        duration_str = f"{mins}:{secs:02d}" if track.get("duration") else "—"

        header = discord.ui.TextDisplay("### 🎵 Tocando agora")
        title = discord.ui.TextDisplay(f"**{track['title']}**")
        info = discord.ui.TextDisplay(
            f"👤 {track.get('uploader', 'Desconhecido')}  •  "
            f"⏱️ {duration_str}  •  📜 {queue_size} na fila  •  "
            f"🔁 Loop: {'On' if loop else 'Off'}"
        )

        container = discord.ui.Container(accent_colour=discord.Colour.blurple())

        if track.get("thumbnail"):
            section = discord.ui.Section(
                header, title, info,
                accessory=discord.ui.Thumbnail(track["thumbnail"])
            )
            container.add_item(section)
        else:
            container.add_item(header)
            container.add_item(title)
            container.add_item(info)

        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))

        row = discord.ui.ActionRow()

        pause_btn = discord.ui.Button(
            label="Pausar", emoji="⏸️",
            style=discord.ButtonStyle.secondary, custom_id="pause_resume"
        )
        pause_btn.callback = self.pause_resume
        row.add_item(pause_btn)

        skip_btn = discord.ui.Button(
            label="Pular", emoji="⏭️",
            style=discord.ButtonStyle.primary, custom_id="skip"
        )
        skip_btn.callback = self.skip
        row.add_item(skip_btn)

        loop_btn = discord.ui.Button(
            label=f"Loop: {'On' if loop else 'Off'}", emoji="🔁",
            style=discord.ButtonStyle.success if loop else discord.ButtonStyle.secondary,
            custom_id="loop_toggle"
        )
        loop_btn.callback = self.loop_toggle
        row.add_item(loop_btn)

        stop_btn = discord.ui.Button(
            label="Parar", emoji="⏹️",
            style=discord.ButtonStyle.danger, custom_id="stop"
        )
        stop_btn.callback = self.stop_playback
        row.add_item(stop_btn)

        container.add_item(row)
        self.add_item(container)

    async def pause_resume(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        state = get_state(interaction.guild.id)
        if vc is None:
            await interaction.response.send_message("Não estou tocando nada.", ephemeral=True)
            return

        if vc.is_playing():
            vc.pause()
            if state.voice_client and state.voice_client.channel:
                await set_voice_status(state.voice_client.channel, f"⏸️ {state.current['title']}")
        elif vc.is_paused():
            vc.resume()
            if state.voice_client and state.voice_client.channel:
                await set_voice_status(state.voice_client.channel, f"🎵 {state.current['title']}")
        else:
            await interaction.response.send_message("Nada tocando no momento.", ephemeral=True)
            return

        new_view = PlayerView(self.guild_id, state.current, len(state.queue), state.loop_mode)
        await interaction.response.edit_message(view=new_view)

    async def skip(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        state = get_state(interaction.guild.id)

        if vc is None or not (vc.is_playing() or vc.is_paused()):
            await interaction.response.send_message("Nada tocando para pular.", ephemeral=True)
            return

        state.loop_mode = False
        await interaction.response.defer()
        vc.stop()

    async def loop_toggle(self, interaction: discord.Interaction):
        state = get_state(interaction.guild.id)
        state.loop_mode = not state.loop_mode
        new_view = PlayerView(self.guild_id, state.current, len(state.queue), state.loop_mode)
        await interaction.response.edit_message(view=new_view)

    async def stop_playback(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        state = get_state(interaction.guild.id)
        channel = vc.channel if vc else None
        state.queue.clear()
        state.loop_mode = False
        state.current = None

        if vc:
            vc.stop()
            await vc.disconnect()

        if channel:
            await set_voice_status(channel, "")

        stopped_view = discord.ui.LayoutView()
        stopped_container = discord.ui.Container(accent_colour=discord.Colour.red())
        stopped_container.add_item(discord.ui.TextDisplay("⏹️ **Reprodução encerrada.**"))
        stopped_view.add_item(stopped_container)
        await interaction.response.edit_message(view=stopped_view)


# ==================== LÓGICA DE REPRODUÇÃO ====================

async def start_playing(guild: discord.Guild, track: dict):
    state = get_state(guild.id)
    vc = guild.voice_client
    state.current = track

    source = await get_audio_source(track)
    if source is None:
        await play_next(guild)
        return

    def _after(error):
        fut = asyncio.run_coroutine_threadsafe(play_next(guild, error), guild._state.loop)
        try:
            fut.result()
        except Exception as e:
            print(f"Erro no after_playback: {e}")

    vc.play(source, after=_after)

    await set_voice_status(vc.channel, f"🎵 {track['title']}")

    view = PlayerView(guild.id, track, len(state.queue), state.loop_mode)

    if state.now_playing_message:
        try:
            await state.now_playing_message.edit(view=view)
        except discord.NotFound:
            state.now_playing_message = await state.text_channel.send(view=view)
    else:
        state.now_playing_message = await state.text_channel.send(view=view)


async def play_next(guild: discord.Guild, error=None):
    if error:
        print(f"Erro na reprodução anterior: {error}")

    state = get_state(guild.id)
    async with state.lock:
        next_track = state.next_track()

        if next_track is None:
            state.current = None
            vc = guild.voice_client
            if vc and vc.channel:
                await set_voice_status(vc.channel, "")
            if state.now_playing_message:
                try:
                    finished_view = discord.ui.LayoutView()
                    finished_container = discord.ui.Container(accent_colour=discord.Colour.green())
                    finished_container.add_item(discord.ui.TextDisplay("✅ **Fila finalizada.**"))
                    finished_view.add_item(finished_container)
                    await state.now_playing_message.edit(view=finished_view)
                except discord.NotFound:
                    pass
            return

        await start_playing(guild, next_track)


# ==================== COMANDOS ====================

@client.tree.command(name="tocar")
@app_commands.describe(busca="Um link do YouTube OU o nome/artista da música")
async def tocar(interaction: discord.Interaction, busca: str):
    if not interaction.user.voice:
        await interaction.response.send_message(
            "Você precisa estar em um canal de voz para usar este comando.", ephemeral=True
        )
        return

    voice_channel = interaction.user.voice.channel
    voice_client = interaction.guild.voice_client
    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel)

    state = get_state(interaction.guild.id)
    state.text_channel = interaction.channel
    state.voice_client = voice_client

    await interaction.response.send_message("Procurando sua música...", ephemeral=True)

    track = await resolve_track(busca)
    if track is None:
        await interaction.followup.send(
            "Não encontrei nada com esse link/termo de busca. Tente outra palavra-chave ou verifique o link.",
            ephemeral=True
        )
        return

    async with state.lock:
        if voice_client.is_playing() or voice_client.is_paused():
            state.queue.append(track)
            await interaction.followup.send(
                f"➕ **{track['title']}** adicionada à fila (posição {len(state.queue)})."
            )
        else:
            await interaction.followup.send(f"🎶 Preparando: **{track['title']}**")
            await start_playing(interaction.guild, track)    
@client.event    
async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            
            embed = discord.Embed(
                title="Permissão Negada",
                description="Você ou a CiberKov não tem a permissão necessária!",
                color=discord.Color.purple(
                    ))
            
            await interaction.response.send_message(embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="Erro Inesperado",
                description="A CiberKov não conseguiu executar o comando devido um erro inesperado!",
                color=discord.Color.purple(
                    ))
            
            await interaction.response.send_message(embed, ephemeral=True)

@client.tree.command(name="acessar_elite", description="Requisita um cargo especial no servidor parceiro.")
async def acessar_elite(interaction: discord.Interaction):
    # 1. Obter o servidor de destino
    # 1. Trava de segurança extra (caso haja algum bug visual do Discord)
    if interaction.guild_id != (1436139252567248956):
        await interaction.response.send_message("❌ Este comando só pode ser utilizado no servidor oficial de requisições.", ephemeral=True)
        return
    
    
    guild_destino = client.get_guild(1162538768394367016)
    if not guild_destino:
        await interaction.response.send_message("❌ Erro: O bot não está no servidor de destino ou a ID está incorreta.", ephemeral=True)
        return

    # 2. Obter o usuário no servidor de destino
    member_destino = guild_destino.get_member(interaction.user.id)
    if not member_destino:
        await interaction.response.send_message("❌ Você precisa entrar no servidor de destino primeiro para receber o cargo!", ephemeral=True)
        return

    # 3. Obter o cargo pré-selecionado
    cargo = guild_destino.get_role(1475307032415436840)
    if not cargo:
        await interaction.response.send_message("❌ Erro: Cargo não encontrado no servidor de destino. Avise a moderação.", ephemeral=True)
        return

    # 4. Verificar se o usuário já possui o cargo
    if cargo in member_destino.roles:
        await interaction.response.send_message("⚠️ Você já possui este cargo no servidor!", ephemeral=True)
        return

    # 5. Tentar adicionar o cargo
    try:
        await member_destino.add_roles(cargo, reason=f"Cargo requisitado via comando no servidor {interaction.guild.name}")
        await interaction.response.send_message(f"✅ Sucesso! O cargo **{cargo.name}** foi adicionado a você no servidor **{guild_destino.name}**.", ephemeral=True)
    
    except discord.Forbidden:
        await interaction.response.send_message("❌ Erro de permissão: Meu cargo no servidor de destino é menor que o cargo que estou tentando dar, ou não tenho permissão de Gerenciar Cargos.", ephemeral=True)
    except discord.HTTPException:
        await interaction.response.send_message("❌ Ocorreu um erro na API do Discord ao tentar te dar o cargo. Tente novamente mais tarde.", ephemeral=True)
        
@client.tree.command(name="timeout", description="Coloca um membro de castigo (timeout) por tempo determinado.")
@app_commands.describe(
    membro_1="O membro que receberá o timeout",
    membro_2="O membro que receberá o timeout",
    membro_3="O membro que receberá o timeout",
    membro_4="O membro que receberá o timeout",
    membro_5="O membro que receberá o timeout",
    tempo="Duração do timeout",
    motivo="O motivo do timeout (opcional)"
)
@app_commands.choices(tempo=[
    app_commands.Choice(name="1 Minuto", value=1),
    app_commands.Choice(name="5 Minutos", value=5),
    app_commands.Choice(name="15 Minutos", value=15),
    app_commands.Choice(name="30 Minutos", value=30),
    app_commands.Choice(name="60 Minutos", value=60)
])
async def timeout(
    interaction: discord.Interaction, 
    tempo: int, 
    membro_1: discord.Member,
    membro_2: Optional[discord.Member] = None,
    membro_3: Optional[discord.Member] = None,
    membro_4: Optional[discord.Member] = None,
    membro_5: Optional[discord.Member] = None,
    motivo: Optional[str] = None
):
    membros = [membro_1, membro_2, membro_4, membro_4, membro_5]
    ID_PERMITIDO = 1047129198508113990  # Substitua por um número inteiro (sem aspas)
    
    if interaction.user.id != ID_PERMITIDO:
        await interaction.response.send_message(
            "❌ Você não tem permissão exclusiva para usar este comando.", 
            ephemeral=True
        )    
    
    elif interaction.user.id in [membro.id for membro in membros if membro is not None]:
        await interaction.response.send_message(
            "❌ Você não pode dar timeout a si mesmo.", 
            ephemeral=True
        )
        return
    
    # Avisa a API que o bot está processando o comando (evita "A interação falhou")
    await interaction.response.defer()
    
    alvos = [m for m in [membro_1, membro_2, membro_3, membro_4, membro_5] if m is not None]
    
    alvos = list(set(alvos))

    duracao = timedelta(minutes=tempo)
    sucesso = 0
    falha = 0
    membros_punidos = []
    
    for membro in alvos:
        try:
            await membro.timeout(duracao, reason=motivo)
            sucesso += 1
            membros_punidos.append(membro.mention)
            await asyncio.sleep(1) # Pausa para evitar bloqueio da API (Rate Limit)
        except discord.Forbidden:
            falha += 1
        except Exception:
            falha += 1

    lista_mentions = ", ".join(membros_punidos) if membros_punidos else "Nenhum"
    mensagem = (
        f"⏳ **Timeout em Lista Concluído!** ({tempo} minutos)\n"
        f"✅ Aplicado em **{sucesso}** membro(s): {lista_mentions}\n"
    )
    
    if falha > 0:
        mensagem += f"❌ Falhou em **{falha}** membro(s) (Verifique a hierarquia de cargos).\n"

    if motivo:
        mensagem += f"**Motivo:** {motivo}"
        
    await interaction.followup.send(mensagem)
        

@client.tree.command(name="retimeout", description="Remove o castigo (timeout) de um membro.")
@app_commands.describe(membro="O membro que terá o timeout removido")
async def retimeout(interaction: discord.Interaction, membro: discord.Member):
    
    ID_PERMITIDO = 1047129198508113990  # ID do usuário permitido
    
    # 1. Verificação de permissão do usuário
    if interaction.user.id != ID_PERMITIDO:
        await interaction.response.send_message(
            "❌ Você não tem permissão exclusiva para usar este comando.", 
            ephemeral=True
        )
        return
    
    # Usamos defer() para dar tempo ao bot de processar, caso a API do Discord demore
    await interaction.response.defer(ephemeral=True)
    
    try:
        await membro.timeout(None, reason="Timeout removido via comando retimeout.")
            
        await interaction.followup.send(f"✅ Timeout removido com sucesso de {membro.mention}!")
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Eu não tenho permissão para alterar o status desse membro (ele pode ter um cargo maior que o meu).")
    except Exception as e:
        await interaction.followup.send(f"❌ Ocorreu um erro inesperado: {e}")
        
        
@client.tree.command(name="ban", description="Causa um banimento de um membro.")
@app_commands.describe(membro="O membro será banido!")
async def ban(interaction: discord.Interaction, membro: discord.Member, motivo: Optional[str] = None):
    
    ID_PERMITIDO = 1047129198508113990
    
    if interaction.user.id != ID_PERMITIDO:
        await interaction.response.send_message(
            "❌ Você não é o Igor Prudov para usar este comando.", 
            ephemeral=True
        )
    elif membro.id == interaction.user.id:
        await interaction.response.send_message(
            "❌ Você não pode banir a si mesmo.", 
            ephemeral=True
        )
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        await membro.ban(reason=motivo)
        
        mensagem = f"⏳ O membro {membro.mention} recebeu um ban por {interaction.user.mention}."
        
        if motivo:
            mensagem += f"\n**Motivo:** {motivo}"
            
        await interaction.followup.send(mensagem)
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Eu não tenho permissão para alterar o status desse membro (ele pode ter um cargo maior que o meu).")
    except Exception as e:
        await interaction.followup.send(f"❌ Ocorreu um erro inesperado: {e}")
        
# Dicionário global para armazenar temporariamente os overwrites de cada canal
# Estrutura: { id_do_canal: discord.PermissionOverwrite }
lockdown_cache = {}

@client.tree.command(name="lockdown", description="Salva as permissões atuais e bloqueia o servidor (Lockdown).")
@app_commands.default_permissions(administrator=True)
async def lockdown(interaction: discord.Interaction):
    await interaction.response.defer()
    
    ID_PERMITIDO = 1047129198508113990
    
    if interaction.user.id != ID_PERMITIDO:
        await interaction.followup.send(
            "❌ Você não é o Igor Prudov para usar este comando.", 
            ephemeral=True
        )
        return

    guild = interaction.guild
    cargo_everyone = guild.default_role
    
    sucesso = 0
    falhas = 0

    # Limpa o cache anterior para evitar conflitos de lockdowns passados
    lockdown_cache.clear()

    for channel in guild.channels:
        try:
            # Pega as permissões exatas que o @everyone tem NESTE canal agora
            overwrite_antigo = channel.overwrites_for(cargo_everyone)
            
            # Salva uma cópia exata no cache usando o ID do canal como chave
            lockdown_cache[channel.id] = discord.PermissionOverwrite(
                **{perm: val for perm, val in overwrite_antigo if val is not None}
            )
            
            # Cria um novo overwrite baseado no antigo, mas forçando o bloqueio
            novo_overwrite = channel.overwrites_for(cargo_everyone)
            novo_overwrite.send_messages = False
            novo_overwrite.send_messages_in_threads = False
            novo_overwrite.add_reactions = False
            novo_overwrite.speak = False
            
            await channel.set_permissions(cargo_everyone, overwrite=novo_overwrite, reason=f"Lockdown ativado por {interaction.user}")
            sucesso += 1
        except discord.Forbidden:
            falhas += 1
        except Exception as e:
            print(f"Erro ao aplicar lockdown no canal {channel.name}: {e}")
            falhas += 1

    mensagem = f"🔒 **Lockdown Ativado!**\nAs permissões originais de `{sucesso}` canais foram salvas e os acessos foram bloqueados."
    if falhas > 0:
        mensagem += f"\n⚠️ Não foi possível alterar `{falhas}` canais por falta de permissão."
        
    await interaction.followup.send(mensagem)


@client.tree.command(name="unlock", description="Restaura as permissões salvas antes do lockdown.")
@app_commands.default_permissions(administrator=True)
async def unlock(interaction: discord.Interaction):
    await interaction.response.defer()
    
    ID_PERMITIDO = 1047129198508113990
    
    if interaction.user.id != ID_PERMITIDO:
        await interaction.followup.send(
            "❌ Você não é o Igor Prudov para usar este comando.", 
            ephemeral=True
        )
    elif not lockdown_cache:
        await interaction.followup.send("⚠️ Não há nenhum registro de lockdown ativo ou o bot foi reiniciado. Não foi possível restaurar permissões específicas.", ephemeral=True)
        return

    guild = interaction.guild
    cargo_everyone = guild.default_role
    
    sucesso = 0
    falhas = 0

    for channel in guild.channels:
        # Verifica se temos o histórico desse canal guardado no cache
        if channel.id in lockdown_cache:
            try:
                overwrite_original = lockdown_cache[channel.id]
                
                # Se o overwrite original estava completamente zerado/limpo, removemos a linha do @everyone
                if overwrite_original.is_empty():
                    await channel.set_permissions(cargo_everyone, overwrite=None, reason=f"Lockdown desativado por {interaction.user} (Restaurado ao original)")
                else:
                    await channel.set_permissions(cargo_everyone, overwrite=overwrite_original, reason=f"Lockdown desativado por {interaction.user} (Restaurado ao original)")
                
                sucesso += 1
            except discord.Forbidden:
                falhas += 1
            except Exception as e:
                print(f"Erro ao restaurar o canal {channel.name}: {e}")
                falhas += 1
        else:
            # Caso um canal novo tenha sido criado DURANTE o lockdown, apenas limpamos as permissões dele
            try:
                await channel.set_permissions(cargo_everyone, overwrite=None, reason="Lockdown desativado (Canal sem histórico)")
            except:
                pass

    # Limpa o cache após a restauração bem-sucedida
    lockdown_cache.clear()

    mensagem = f"🔓 **Lockdown Desativado!**\nAs permissões originais de `{sucesso}` canais foram restauradas com sucesso."
    if falhas > 0:
        mensagem += f"\n⚠️ Falha ao restaurar `{falhas}` canais."

    await interaction.followup.send(mensagem)

       
client.run('MTM4NDQwNzU0NzQ2MDQ1NjUwOQ.Gx1g83.vYghJBbG4S7MNzijUBI4blv2dlA95pC2ApuepM')
#client.run('MTM4NDQwNzU0NzQ2MDQ1NjUwOQ.GH8WQS.iAuOod_zoBEMkI9Fu5cK2SGwkV7npQ_88bZiUU')
#client.run('MTM2ODEzOTM2NDgwNjE2NDYwMQ.GbE1NI.UhfFMbW_X29JFMZPXtdMjZwS2EwgEBXLfZH8Wk')