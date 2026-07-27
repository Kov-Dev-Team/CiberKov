import discord
import utils
import asyncio

from discord import ui

class ccf(ui.LayoutView):
    
    def __init__(self):
        super().__init__()
        
        container = ui.Container(ui.TextDisplay("# REGRAS DA FEDERAÇÃO DA BIAHKOV"),accent_color=discord.Colour.purple())
        container.add_item(ui.TextDisplay(
            "***Rege toda a [Biahkov Federation](https://discord.gg/8k9X2ePPgb) e seus membros. Informe-se pelo ⁠<#1199600888747143168>, para atualizações.***"
            ))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))
        container.add_item(ui.TextDisplay(
            "### Regras Sobre a Moderação <@&1222682880392826910> I:"
            "\n*Regra nº1: A Biah pode banir, remover ou punir de forma livre de justificativa, independente de quem seja."
            "\nRegra nº2: Desrespeito, deboche, ironia contra um aviso de um moderador não será tolerado!"
            "\nRegra nº3: Não crie tickets sem necessidade, verifique antes se você está fazendo o processo corretamente."
            "\nRegra nº4: Todos devem denunciar qualquer um que fuja as regras no ⁠<#1201673224514183228>."
            "\nRegra nº5: Os membros podem apelar uma punição no canal de suporte (apenas **depois** da punição), ou na DM de algum moderador (apenas **durante** a punição)."
            "\nRegra nº6: Os moderadores usarão do juízo para aplicar as regras, caso alguém tente procurar os limites das regras, poderá ser punido."
            "\nRegra nº7: Marcações de moderadores não é permitido, somente para casos extremos, que a moderação é necessária."
            "\nRegra nº8: Para casos omissos nas regras, ficará a juízo do moderador decidir e notificar a decisão ao membro e aos outros moderadores.*"
            ))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))
        container.add_item(ui.TextDisplay(
            "### Regras Gerais para os Cidadãos <@&1162541813819768872> II:"
            "\n*Regra nº1: Não faça marcações de pessoas desconhecidas, brigue, ou seja preconceituoso."
            "\nRegra nº2: Mantenha suas informações pessoais, pessoais!"
            "\nRegra nº3: Evite os Tópicos Sensíveis, faça piadas, mas não perca o respeito!"
            "\nRegra nº4: Autopromoção ou promoção de outras pessoas só podem ser feitas pelos artistas na categoria de Art's Hub."
            "\nRegra Nº5: Não traga brigas externas para o servidor!"
            "\nRegra nº6: Use nomes em caracteres legíveis."
            "\nRegra nº7: Proibido o uso de imagem de personagem que é menor de idade ou aparenta ser menor de idade (Ex.: Lolis, shotacon, infantilização, etc.)."
            "\nRegra nº8: Não é permitida a adição de contas secundárias no servidor!"
            "\nRegra nº9: Só escreva no chat em português! (If you aren't Lusophone, you can speak in English).*"
            ))
        container.add_item(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.small))
        container.add_item(ui.TextDisplay(
            "```Tópicos Seníveis:"
            "\n- Nazismo ou grupos políticos extremistas;"
            "\n- Suicídio;"
            "\n- Qualquer tema religioso"
            "\n- Qualquer tema relacionado a menores de idade;"
            "\n- Qualquer palavra que o automod bloqueie;"
            "\n- Qualquer outro tema que fuja do que pode ser considerado humor.```"
            ))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))
        container.add_item(ui.TextDisplay(
            "### Regras Gerais da Utilização do Servidor III:"
            "\n*Regra nº1: Não utilize canais de forma errada."
            "\nRegra nº2: Não faça spam ou flooding."
            "\nRegra nº3: Não use de falhas da segurança ou qualquer bug ao seu favor, comunique a moderação!"
            "\nRegra nº4: Siga as Diretrizes da Comunidade do Discord!"
            "\nRegra nº5: Não use dos áudios para atrapalhar os canais de voz."
            "\nRegra nº6: Todas as transmissões no servidor precisam estar com a opção de vizualizar prévia."
            "\nRegra nº7: O servidor é para maiores de 18 anos, mas permitiremos menores com 16 ou 17 anos, 15 ou menos será banido.*"
            ))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))
        container.add_item(ui.TextDisplay(
            "### Regras Específicas para Artistas <@&1212941777602875412> IV:"
            "\n*Regra nº1: As artes podem ser sensuais ou eróticas (deve estar em spoiler), mas não podem ser pornográficas."
            "\nRegra nº2: As artes só podem ser postadas se te pertencer ou com a autorização de quem ela pertence."
            "\nRegra nº3: Artes com a técnica de traçagem devem ser indicados junto à postagem, assim como o autor e arte originais."
            "\nRegra nº4: É terminantemente proibido arte com a utilização de Inteligência Artificial.*"
            ))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))
        gb = ui.MediaGallery()
        gb.add_item(media='https://cdn.discordapp.com/attachments/1251434158530756619/1464359138179158218/natal.png?ex=697bc5b9&is=697a7439&hm=3affcae14b6d0df4ae7c0bbf980fb8d41c96952e78eb4a77287e6d80be8b60aa')
        container.add_item(gb)
        container.add_item(ui.TextDisplay(
            "-# Kov Administration Team - Programa de Atualização Unificada (PAU)"
            "\n-# Editado por: Igor Prudov // Outorgado por: Biahkov."
            "\n-# Registre-se. Publique-se. Cumpra-se. \n-# <t:1773025200:R>"
            ))
        bs = ui.Button(
         label="Canal de Suporte",
         style=discord.ButtonStyle.url,
         url="https://discord.com/channels/1162538768394367016/1201673224514183228"
         )
        ars = ui.ActionRow(bs)
        container.add_item(ars)
        self.add_item(container)
        

        
class clp(ui.LayoutView):
    
    def __init__(self):
        super().__init__()
        
        container = ui.Container(ui.TextDisplay("# Doações e Redes Sociais da Biahkov!"),accent_color=discord.Colour.purple())
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))
        blp = ui.Button(
         label="LivePix",
         style=discord.ButtonStyle.url,
         url="https://livepix.gg/biahkov"
         )
        btw = ui.Button(
         label="Twitch",
         style=discord.ButtonStyle.url,
         url="https://twitch.tv/biahkov"
         )
        byt = ui.Button(
         label="Youtube",
         style=discord.ButtonStyle.url,
         url="https://youtube.com/@BiahKov"
         )
        bdc = ui.Button(
         label="Discord",
         style=discord.ButtonStyle.url,
         url="https://discord.gg/8k9X2ePPgb"
         )
        bis = ui.Button(
         label="Instagram",
         style=discord.ButtonStyle.url,
         url="https://instagram.com/biahkov/"
         )
        container.add_item(ui.TextDisplay("# Seja Doador! Ganhe __Cargos Exclusivos__ no servidor!"))
        l1 = ui.ActionRow(blp, btw, byt, bdc, bis)
        container.add_item(l1)
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small))
        container.add_item(ui.TextDisplay(
            "## Cargos para Membros do Youtube, Twitch e Server Booster:"
            "\nSendo Youtube Member ou Sub na Twitch você ganha acesso aos VODs das lives, na plataforma a qual é apoiante, e ao ter Server Booster você ajuda a melhorar as funcionalidades do servidor, como mais espaço para emojis, figurinhas, áudios e muito mais. Além disso os apoiadores ganham privilégios no servidor como permissão para funcionalidade de integrações (gifs, imagens, vídeos)!"
            "\n\u200b"
            "\n<@&1334263385034063925>"
            "\n<@&1193746862889508975>"
            "\n<@&1198424819184705657>"
            "\n\u200b"
            ))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small))
        container.add_item(ui.TextDisplay(
            "## Cargos para Doações no Livepix:"
            "\nApoiando no Livepix, além de alimentar a Urubia do Pix, você também está ajudando o canal a crescer~~, pagar algumas contas,~~ e financiando para mais conteúdos! Então, doando certas quantias você receberá um cargo especial e tera acesso assim como os outros ao <#1333178275702243551>!"
            "\n\u200b"
            "\n- Médias e Grandes Doações:"
            "\n  * <@&1162541496810098688> Doação de 30 Reais;"
            "\n  * <@&1218546165394571365> Doação de 100 Reais;"
            "\n  * <@&1307834044758888560> Doação de 500 Reais."
            "\n\u200b"
            "\n- Grande e Massivas Doações:"
            "\n  * <@&1251476070184652860> Doação de 1.000 Reais;"
            "\n  * <@&1307835233894273165> Doação de 2.000 Reais;"
            "\n  * <@&1250957159068598423> Doação de 5.000 Reais."
            "\n\u200b"
            "\n- PRENDAM O MÉDICO QUE LIBEROU AHHAHAHA:"
            "\n  * <@&1307843457443958804> Doação de 10.000 Reais!"
            "\n\u200b"
            ))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small))
        container.add_item(ui.TextDisplay(
            "## Doadores Federação <@&1312945753131319386>:"
            "\nOs doadores da Federação são aqueles que ajudam para manter o servidor na ativa, sempre agraciando a menutenção dos eventos.\nFale com o <@1047129198508113990> para apoiar o servidor."
            ))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small))
        container.add_item(ui.TextDisplay(
            "\n***Além disso, os doadores recorentes das lives/servidor podem aparecer em artes oficiais, seja no cenário, thumbs e cenários oficiais de eventos!***"
            ))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))
        gb = ui.MediaGallery()
        gb.add_item(media='https://i.makeagif.com/media/10-23-2024/Pq0stF.gif')
        container.add_item(gb)
        self.add_item(container)
     
print  ("Classes prontas!")