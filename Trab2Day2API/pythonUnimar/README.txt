Projeto: Tutor IA

Esse é o trabalho final da disciplina, feito com Python e FastAPI. A ideia é criar uma API REST que funciona como um tutor inteligente, respondendo perguntas. O projeto usa o conceito de Clean Architecture para organizar melhor o código.

Como rodar o projeto:

1. Crie um ambiente virtual (opcional, mas recomendado)

2. Instale as dependências:
pip install -r requirements.txt

3. Rode a aplicação com o comando:
uvicorn main:app --reload

4. Abra no navegador:
http://127.0.0.1:8000/docs

Ali vai aparecer a documentação interativa da API (Swagger), onde dá pra testar as rotas.

Estrutura do Projeto:

- main.py: arquivo principal que inicia a API  
- app/controllers: rotas da API  
- app/services: onde fica a lógica do tutor  
- app/providers: conexão com OpenAI, Anthropic ou um modo fake  
- app/interfaces: interfaces das classes  
- app/models: modelos dos dados usados nas requisições e respostas  
- app/config.py: carrega o .env e escolhe qual IA usar

Arquivo .env:

É necessário criar um arquivo chamado .env na raiz do projeto com essa variável:

LLM_PROVIDER=fake

Com isso o projeto roda no modo fake (não precisa usar nenhuma API externa).  
Se quiser testar com a OpenAI ou Anthropic (com chave válida), é só mudar:

LLM_PROVIDER=openai  
OPENAI_API_KEY=sua-chave-aqui

ou

LLM_PROVIDER=anthropic  
ANTHROPIC_API_KEY=sua-chave-aqui

Exemplo de uso:

Usando curl pra enviar uma pergunta:

curl -X 'POST' \
  'http://127.0.0.1:8000/tutor/perguntar' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "pergunta": "O que é Clean Architecture?"
}'

Observações:

- Não é preciso usar nenhuma chave de API se deixar no modo fake  
- Tudo foi feito usando Python 3 e FastAPI  
- Projeto organizado com base nos conceitos aprendidos na disciplina
