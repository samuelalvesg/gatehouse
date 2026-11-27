# Locale pt-BR

Regras de texto de interface em português do Brasil. Carregue junto com `../SKILL.md`.

## Ortografia e formato
- pt-BR com **todos os acentos** e ortografia correta. Nunca substituto sem acento ("nao", "acao").
- Maiúscula só na primeira letra da frase e em nomes próprios. Títulos, rótulos, itens de menu e botões seguem a mesma regra: "Configurações da conta", não "Configurações Da Conta". O uso de maiúscula inicial em itens de menu e rótulos segue a convenção do produto; mantenha a mesma em todas as telas.
- Dois-pontos e ponto e vírgula vão colados à palavra anterior, sem espaço, e a palavra seguinte fica minúscula: "Data: antigas para novas".
- Sem ponto final em títulos, rótulos, links e botões, a não ser que haja mais de uma frase.
- Exclamação: evite. Ela soa como grito. Troque por ponto quando ficar mais natural.
- Use "e" no lugar de "&", salvo em nome de marca.
- Sem espaço antes de pontuação. Use espaço não separável entre número e unidade: "R$ 10", "15 MB".
- Números com vírgula decimal e ponto como separador de milhar. Ano sem separador: "2015".
- Hora no formato de 24 horas: "às 21h25". Data: "dd/mm/aa" quando o espaço for curto.
- Evite abreviações. Abrevie só quando faltar espaço, como em botões pequenos.
- Use vírgula serial em listas de três ou mais itens.

## Tom e forma de falar
- Trate o usuário com **"você"** e "seu/sua". Evite "eu" e "meu" no texto do produto. Não misture primeira e segunda pessoa na mesma frase.
- Use contrações quando soarem naturais ("não é", "pra", "tá" só em tom muito informal e nunca em erro). Sem contração o texto soa robótico.
- Evite o masculino genérico. "Será um prazer ajudar você", não "Será um prazer ajudar".
- Frases curtas, uma ideia por frase. Comece pelo que o usuário quer fazer, depois revele o detalhe necessário.
- Texto de interface se lê de relance: uma ideia por linha ou parágrafo curto. Erro e estado vazio têm no máximo duas frases curtas, com o próximo passo em linha própria. Nunca um bloco único que muda de assunto.
- Use palavras comuns, sem jargão. Use sempre a mesma palavra para o mesmo conceito.
- Descreva o comportamento no presente: "O arquivo será enviado", não "Você vai ver o arquivo enviado".
- Ao citar um controle, use o texto do rótulo, sem dizer o tipo do elemento: "Toque em Salvar", não "Toque no botão Salvar".
- Não traduza literalmente expressões do inglês. "Tente novamente mais tarde", não "Por favor, tente novamente mais tarde".
- Teste em voz alta. Se o texto não é algo que você diria a uma pessoa, reescreva.
- Tom: neutro, cordial e direto. Em erro, o tom é solidário e detalhado. Em celebração ou sucesso, pode ser leve. A voz do produto é a mesma em todas as situações.

## Componentes
- **Botão**: verbo no infinitivo + resultado claro. "Salvar alterações", "Criar equipe", nunca "OK" ou "Enviar" sozinho quando o resultado não é óbvio.
- **Erro**: o que aconteceu + por que (se ajudar) + o que fazer agora. Nunca mostre stack trace, código de exceção ou detalhe interno. Não revele se um e-mail existe.
- **Estado vazio**: o que é a tela + por que está vazia + como começar. Uma ação principal.
- **Confirmação**: título como declaração ou pergunta breve. O texto nomeia a ação e a consequência: "Excluir 3 arquivos? Não dá para desfazer." Botões: "Excluir arquivos" e "Manter".
- **Carregamento**: diga o que está acontecendo. Não prometa tempo exato.
- **Títulos de tela**: substantivo curto ou pergunta. Evite gerúndio: "Geração de chaves", não "Gerando chaves".
- **Nomes de opções separadas por barra**: as duas palavras com maiúscula: "Importar/Exportar arquivo".

## Tamanho
- O texto em pt-BR costuma ficar 20 a 30% maior que o inglês. Planeje quebra de linha e teste em tela estreita.

## Fontes
- Google Assistant, capitalização e pontuação em pt-BR: https://developers.google.com/assistant/conversation-design/capitalization-and-punctuation?hl=pt-br (página traduzida por IA, segundo aviso do próprio site)
- Google Material, princípios de comunicação e escrita de UX: https://codelabs.developers.google.com/codelabs/material-communication-guidance?hl=pt-br
- Proton, guia de localização para português do Brasil: https://localize.proton.me/t/guidance-for-portuguese-brazilian/116 (de 2022)
