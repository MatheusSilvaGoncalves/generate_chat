## Descrição
Chatbot baseado em interface conversacional e IA Generativa para geraão automática de questionários múltipla escolha
baseados em leitura de arquivos pdf.

O procedimento adotado nesta solução envolve dividir o problema em várias pequenas unidades, cada qual executada por um modelo.
Esse comportamento é flexível, configurado a partir de parâmetros que podem ser modificados pelo usuário. No geral, o fluxo de trabalho permite:
1. Trabalhar diretamente em português ou traduzir os textos para inglês e realizar todo o fluxo em inglês, para apenas traduzir as respostas para o português novamente. Isso se mostrou útil pois muitos modelos são treinados majoritariamente em inglês e funcionam melhor nesse idioma.

2. Processar o texto de entrada (e.g., resumi-lo)

3. Selecionar diferentes modelos e prompts para geração de uma pergunta qualquer, baseada em um dado trecho do texto.

4. Selecionar diferentes modelos e prompts para gerar uma resposta correta para essa pergunta, baseada nesse mesmo trecho do texto.

5. Selecionar diferentes modelos e prompts para gerar alternativas erradas, porém plausíveis (um para cada alternativa errada). Aqui pode-se usar tanto o trecho correto quanto selecionar um trecho aleatório do documento para facilitar a geração de alternativas erradas porém verossímeis.

A metodologia se divide nos seguintes passos:

1. Leitura e processamento do arquivo pdf. Obtém-se aqui uma lista de trechos do documento. Assume-se que este documento está dividido em seções numeradas (e.g., 1.3, 5.4.2).

2. Criação de modelos base para tarefas específicas (e.g., tradução, resumo, geração de perguntas).

3. Criação de gerador de prompts para cada tarefa, de acordo com o contexto (e.g., para gerar respostas, manda-se o texto de referência e a pergunta; para gerar perguntas, apenas o texto de referência)

4. Orquestrador de modelos, responsável por estruturar o fluxo, carregar os modelos definidos pelo usuário e gerar as perguntas/respostas. O orquestrador de modelos garante que não se instancie desnecessariamente um mesmo modelo para tarefas distintas (e.g., mesmo que o modelo "google/flan-t5-small" seja utilizado em diversos pontos do fluxo de trabalho, apenas uma cópia dele precisa ser mantida)

5. Loop principal para gerenciamento do questionário, onde as perguntas são geradas uma a uma e as respostas são avaliadas.

## Como usar?
1. Acesse o notebook através do link: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MatheusSilvaGoncalves/generate_chat/blob/master/chat.ipynb)

2. Execute a primeira célula para instalar o repositório e suas dependências

3. Execute a segunda célula para gerar o chat

4. Responda as perguntas. O chat informará você caso tenha acertado ou errado (comentando, nesse caso, qual a resposta correta)

5. Ao final, você receberá sua nota

## Configurações

O chat foi construído de modo a ser facilmente configurável, a seguir comenta-se as principais opções:

1. Título (title): (str) com o título do questionário.
2. Número de questões (n_questions): (int) com o número total de questões.
4. Configuração do modelo (model_config): (dict) com a configuração do fluxo de trabalho e modelos empregados, dividido nas etapas
                "processing", "question", "correct_answer", "wrong_answer". Cada item 
                pode possuir as seguintes configurações: 

    - "task": (str) com a tarefa (e.g., "text2text-generation").
    - "name": (str) com o nome do modelo (e.g., "google/flan-t5-large").
    - "prompt": (str) com prompts adicionais.
    - "alternative": (bool) indicando qual forma de carregamento do modelo.
    - "distractor": (bool) parâmetro adicional que indica se um trecho diferente de texto deve ser passado (útil na criação de respostas erradas).
    - "kwargs": (dict) com argumentos opcionais para o modelo (e.g., "max_new_tokens", "temperature").
4. Configuração de extração de texto (text_config): (dict) com configurações opcionais para leitura e processamento de texto:
    - "num_pages": (int) com a última página a ser considerada.
    - "max_section_length": (int) with the maximum length of the section.
    - "include_section_title": (bool) indicating whether to include the main
                                        section together or not.
5. Debug (debug): (bool) indicando se o usuário deseja ver o resultado das etapas intermediárias de geração.
6. Trabalhar em inglês (pt_en_pt): (bool) indicando se o usuário prefere que os modelos gerem o questionário em inglês e depois traduzam para português.
7. Número de alternativas (n_alternatives): (int) com o número de alternativas a serem criadas.
8. Número máximo de tentativas (max_tries): (int) com o número máximo de tentativas para gerar respostas diferentes nas alternativas, evitando respostas iguais.

