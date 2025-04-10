import json
import urllib3

# Mensagens de Boas-vindas e Problemas
mensagem_inicial = """Olá! Eu sou o HelpDesk bot, seu assistente técnico de hardware... 
Descreva o problema que você está enfrentando, e vou te ajudar a solucioná-lo!... 
Selecione o dispositivo: PC ou Notebook..."""

mensagem_problemas = """Qual desses problemas você está enfrentando? Tela preta, 
super aquecimento, dispositivo não liga, desempenho lento ou dispositivo reiniciando..."""

mensagem_final = """Você tem mais algum problema?... 
Não?... Tudo bem, obrigado por nos escolher. Tenha um ótimo dia!"""

# Inicializa o gerenciador de conexões do urllib3
http = urllib3.PoolManager()

AUDIO_API_URL = "https://rmbshe6lg3.execute-api.us-east-1.amazonaws.com/v1/tts"

# Função para gerar o áudio a partir do texto
def gerar_resposta_audio(historico_conversa):
    payload = json.dumps({"phrase": historico_conversa})
    try:
        response = http.request(
            'POST',
            AUDIO_API_URL,
            body=payload,
            headers={'Content-Type': 'application/json'}
        )
        if response.status == 200:
            return json.loads(response.data.decode('utf-8')).get("url_to_audio")
        else:
            return "Houve um problema ao gerar o áudio."
    except Exception as e:
        return f"Erro na chamada da API: {str(e)}"

def lambda_handler(event, context):
    # Extraindo as informações do intent
    intent_name = event.get('sessionState', {}).get('intent', {}).get('name', None)
    slots = event.get('sessionState', {}).get('intent', {}).get('slots', {})
    session_attributes = event.get('sessionState', {}).get('sessionAttributes', {})

    # Salvar dispositivo no session attributes
    if slots.get('dispositivo'):
        dispositivo = slots.get('dispositivo', {}).get('value', {}).get('interpretedValue', None)
        session_attributes['dispositivo'] = dispositivo
    
    # Entrando nas funções de cada intent
    if intent_name == 'saudacao':
        return problemas_card(event, intent_name, session_attributes)
    elif intent_name in ['problema_tela_preta', 'problema_superaquecimento', 'problema_nao_liga', 'problema_desempenho_lento', 'problema_reiniciando']:
        return processar_problema(event, intent_name, session_attributes)
    else:
        return fallback_response(event, intent_name, session_attributes)

def problemas_card(event, intent_name, session_attributes):
    dispositivo = session_attributes.get('dispositivo', '')

    # Exibe o card com os problemas para o usuário selecionar
    return {
        'messages': [
            {
                "contentType": "ImageResponseCard",
                "imageResponseCard": {
                    "title": "Qual desses problemas você está enfrentando?",
                    "imageUrl": "https://mainbucketjean.s3.amazonaws.com/imgs/pc_problems.jpg",
                    "buttons": [
                        {"text": "Tela preta", "value": "problema_tela_preta"},
                        {"text": "Super Aquecimento", "value": "problema_superaquecimento"},
                        {"text": f"{dispositivo} Não liga", "value": "problema_nao_liga"},
                        {"text": "Desempenho Lento", "value": "problema_desempenho_lento"},
                        {"text": f"{dispositivo} Reiniciando", "value": "problema_reiniciando"}
                    ]
                }
            }
        ],
        'sessionState': {
            'dialogAction': {
                'type': 'Close'
            },
            'intent': {
                'name': intent_name,
                'state': 'Fulfilled'
            },
            'sessionAttributes': session_attributes
        }
    }

def processar_problema(event, intent_name, session_attributes):
    dispositivo = session_attributes.get('dispositivo', '')

    # Resoluções dos problemas
    resolucoes = {
        'problema_tela_preta': "Problema de Tela Preta... Verifique a conexão do monitor: Certifique-se de que o cabo do monitor está bem conectado à placa de vídeo ou à saída de vídeo da placa-mãe.",
        'problema_superaquecimento': "Problema de Super aquecimento... Limpeza interna: Abra o dispositivo e limpe a poeira dos ventiladores, dissipadores de calor e componentes com ar comprimido. Poeira acumulada pode obstruir o fluxo de ar.",
        'problema_nao_liga': f"Problema de {dispositivo} não ligando... Verifique a alimentação: Certifique-se de que o cabo de energia está conectado corretamente e que a tomada está funcionando.",
        'problema_desempenho_lento': "Problema de Desempenho Lento... Verifique o armazenamento: Certifique-se de que o disco rígido (HD ou SSD) não está cheio. Unidades muito cheias podem reduzir o desempenho. Considere usar um SSD se estiver usando um HD.",
        'problema_reiniciando': f"Problema de {dispositivo} reiniciando... Memória RAM: Retire e reinsira os módulos de RAM. Teste um de cada vez em diferentes slots. Use ferramentas como MemTest86 para verificar erros de RAM."
    }

    # Mensagem de resolução do problema
    resolucao = resolucoes.get(intent_name, "Desculpe, não encontrei uma solução para esse problema.")
    
    # Processar a resposta do usuário após resolver o problema
    return processar_resposta(event, resolucao, intent_name, session_attributes)

def processar_resposta(event, resolucao, intent_name, session_attributes):
    # Recuperar histórico de conversas
    historico_conversa = session_attributes.get('historico_conversa', '')

    # Verifica se a resolução já foi adicionada ao histórico
    if resolucao not in historico_conversa:
        historico_conversa += f"{resolucao}... "
    
    # Salva o historico no SessionAttributes
    session_attributes['historico_conversa'] = historico_conversa

    # Aqui será feita a pergunta "Você tem mais algum problema? (Sim ou Não)"
    resposta_slot = None
    slots = event['sessionState']['intent']['slots']
    if slots.get('resposta'):
        resposta_slot = event['sessionState']['intent']['slots'].get('resposta', {}).get('value', {}).get('interpretedValue')

    # Se o usuário responder "sim"
    if resposta_slot and resposta_slot.lower() == 'sim':

        return problemas_card(event, intent_name, session_attributes)  # Mostra novamente o card com problemas

    # Se o usuário responder "não"
    elif resposta_slot and resposta_slot.lower() == 'não':
        # Gera o link do áudio com o histórico completo
        dispositivo = session_attributes.get('dispositivo', '')
        historico_conversa = session_attributes.get('historico_conversa', '')
        audio_final = f"{mensagem_inicial}... Você selecionou: {dispositivo}... {mensagem_problemas}... {historico_conversa}... {mensagem_final}"
        url_audio = gerar_resposta_audio(audio_final)
        session_attributes['historico_conversa'] = ""  # Limpa o histórico

        return {
            'messages': [
                {'contentType': 'PlainText', 'content': "Tudo bem, obrigado por nos escolher. Tenha um ótimo dia!"},
                {'contentType': 'PlainText', 'content': f"Áudio gerado da conversa: {url_audio}"}
            ],
            'sessionState': {
                'dialogAction': {'type': 'Close'},
                'intent': {'name': intent_name, 'state': 'Fulfilled'},
                'sessionAttributes': session_attributes
            }
        }

    # Se o slot 'resposta' não tiver sido preenchido ainda
    else:
        return {
            'messages': [
                {'contentType': 'PlainText', 'content': resolucao},
                {'contentType': 'PlainText', 'content': "Você tem mais algum problema?"}
            ],
            'sessionState': {
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'slotToElicit': 'resposta'  # Pergunta sobre mais problemas
                },
                'intent': {
                    'name': intent_name,
                    'state': 'InProgress'
                },
                'sessionAttributes': session_attributes
            }
        }

def fallback_response(event, intent_name, session_attributes):
    return {
        'messages': [{'contentType': 'PlainText', 'content': "Desculpe, não entendi. Por favor, tente novamente."}],
        'sessionState': {
            'dialogAction': {'type': 'ElicitIntent'},
            'intent': {'name': intent_name, 'state': 'Fulfilled'},
            'sessionAttributes': session_attributes
            }
    }
