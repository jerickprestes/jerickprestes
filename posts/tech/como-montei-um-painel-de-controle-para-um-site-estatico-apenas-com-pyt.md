---
title: Como montei um painel de controle para um site estático apenas com Python
date: 2026-11-12
tags: python,automação,linux,git
summary: Um painel local em Python puro, sem dependências, para gerar o site, publicar artigos e enviar ao GitHub sem expor os scripts no repositório público.
cover: img/posts/captura-de-tela-de-2026-11-12-20-40-07.png
---

## Resposta rápida

Criei um painel que roda na minha máquina (`127.0.0.1`), usa só a biblioteca padrão do Python e deixa eu gerar o site, escrever artigos e enviar tudo ao GitHub pelo navegador. Para não expor os scripts, o projeto ficou em dois repositórios: o site público e as ferramentas privadas. O que você leva daqui é a estrutura, os cuidados de segurança de um servidor local e os erros que me custaram tempo.

## O problema

Meu portfólio é um site estático gerado por scripts Python: o `build.py` monta o HTML, e outros dois scripts baixam as capas do Behance e calculam as cores. Tudo funcionava no terminal, mas eu precisava lembrar da ordem dos comandos e de qual arquivo rodar em cada situação.

Eu uso Linux e queria uma interface gráfica no navegador, incluindo a publicação de artigos. Antes de construir, apareceu uma dúvida: publicar os `.py` no repositório público tem algum risco? Procurei senha, token e chave neles e não achei nada. Mesmo assim, não faz sentido o gerador morar no mesmo lugar do site publicado.

## A abordagem

Considerei três caminhos: continuar no terminal com um `subir.sh`, fazer uma aplicação desktop ou fazer uma página local servida por um script Python. Fiquei com a terceira, porque não exige instalar nada (uso Python 3.12.3 no Linux) e roda em qualquer navegador.

A segunda decisão foi dividir o projeto em duas pastas, cada uma com seu repositório:

| Pasta | Repositório | Conteúdo |
|---|---|---|
| `site/` | público (GitHub Pages) | HTML, CSS, JS, imagens, artigos |
| `ferramentas/` | privado | `build.py`, `painel.py`, scripts auxiliares, README |

Um `config.json` em `ferramentas/` diz onde está a pasta do site (`"site": "../site"`). Assim os scripts funcionam sem caminhos fixos.

## Passo a passo

1. **Servidor local só com a biblioteca padrão.** O painel usa `ThreadingHTTPServer` na porta 8765 e tenta as 20 seguintes se estiver ocupada. Escuta apenas em `127.0.0.1`. Resultado esperado: a página abre sozinha no navegador, sem `pip install`.

2. **Proteção contra acesso indevido.** Servidor local também precisa de cuidado, porque qualquer página aberta no navegador pode tentar chamá-lo. A cada execução o painel gera um token aleatório, e toda chamada de API precisa enviá-lo no cabeçalho `X-Token`. Ele também confere o cabeçalho `Host`. Resultado: chamadas de fora do painel são recusadas.

3. **Tarefas em segundo plano com log.** Cada botão (gerar o site, baixar imagens, calcular cores) cria uma tarefa em uma thread. A página consulta o log da tarefa em intervalos curtos e mostra a saída do script em tempo real. Só uma tarefa roda por vez, para dois comandos não mexerem nos mesmos arquivos.

4. **Editor de artigos.** O painel lista os arquivos de `site/posts/`, abre, salva, mostra uma prévia e aceita upload de imagens para `site/img/posts/`. A prévia reaproveita a função `md_to_html` do próprio `build.py`, então o que eu vejo é o que o site vai gerar. Ao remover um artigo, o arquivo vai para `ferramentas/lixeira/`, não é apagado.

5. **Envio ao GitHub.** Os botões fazem `git add`, `commit` e `push` nos dois repositórios. Esse passo me deu mais trabalho, e conto abaixo.

## Armadilhas e erros que enfrentei

**O botão "Abrir" não fazia nada.**
- Sintoma: o painel respondia "ok" e o navegador não abria.
- Causa: `webbrowser.open('file://...')` falha em silêncio em alguns navegadores no Linux.
- Correção: chamar o `xdg-open` com o endereço montado por `pathlib`, e devolver um erro visível se o `index.html` não existir.

```python
url = pathlib.Path(idx).as_uri()
subprocess.Popen(['xdg-open', url], stdout=subprocess.DEVNULL,
                 stderr=subprocess.DEVNULL, start_new_session=True)
```

**O push falhava por causa da autenticação.**
- Sintoma: commit e push pelo painel não funcionavam, mas no terminal funcionavam.
- Causa: o painel roda o Git com `GIT_TERMINAL_PROMPT=0`, para o processo não travar esperando uma senha que ninguém digita. Sem credencial salva, o push simplesmente falha.
- Correção: uma janela no painel pede usuário e token do GitHub. O token vai por variável de ambiente para um auxiliar `GIT_ASKPASS` temporário, que é apagado ao final. Não fica em disco, não vai para o `.git/config` e aparece como `***` no log.

```python
env_push = {'GIT_ASKPASS': helper, 'FS_USER': usuario, 'FS_TOKEN': token}
executar(['git', '-c', 'credential.helper=', 'push', '-u', 'origin', branch],
         pasta, job, extra_env=env_push, segredos=(token,))
```

**Branch chamada `HEAD` antes do primeiro commit.**
- Sintoma: o painel mostrava a branch errada em repositório novo.
- Causa: `git rev-parse --abbrev-ref HEAD` devolve `HEAD` quando não há commits.
- Correção: usar `git symbolic-ref --short HEAD`.

**Repositório criado na pasta errada.**
- Sintoma: o primeiro commit do repositório privado incluiu o site inteiro.
- Causa: rodei `git init` em `~/projetos`, não em `ferramentas/`.
- Correção: apagar o `.git` da pasta errada e refazer dentro de `ferramentas/`.

## Resultado

Não medi tempo, então não vou inventar um número. Em vez disso, comparo o que eu teria de fazer à mão a cada atualização.

**Sem o painel**, publicar um artigo novo era esta sequência:
1. Criar o arquivo `.md` na pasta certa de `posts/`, com o cabeçalho (título, data, tags, resumo) escrito de cabeça.
2. Copiar as imagens para `img/posts/` e ajustar os caminhos no texto.
3. Abrir o terminal e rodar `python3 build.py` para gerar o site.
4. Abrir o `index.html` no navegador para conferir o resultado, e voltar ao passo 1 se algo estivesse errado.
5. Entrar na pasta do site, rodar `git add`, `git commit` e `git push`.
6. Repetir o passo 5 na pasta das ferramentas, se o gerador tivesse mudado, cuidando para não rodar o Git na pasta errada, como já me aconteceu.

**Com o painel**, escrevo o artigo na aba Artigos, vejo a prévia, clico em gerar o site e em enviar. As imagens sobem pelo próprio editor, e o cabeçalho é preenchido por campos. O token do GitHub é pedido na hora do envio e não fica salvo.

Além disso, o gerador saiu do repositório público, e o token só existe na memória durante o push.

Testei o commit e o push contra um repositório local, e a máscara do token no log com um comando de teste. O envio real ao GitHub foi o primeiro teste de verdade.

## Quando não usar essa abordagem

Se mais de uma pessoa mexe no projeto, ou se o site precisa de publicação automática, um fluxo com GitHub Actions é melhor. O painel pressupõe uma pessoa, uma máquina e um servidor local. Se você precisa de um token com acesso amplo, prefira o gerenciador de credenciais do sistema a digitá-lo no painel.

## Próximo passo

O que eu faria a seguir é um botão para conferir os dois repositórios antes do envio, mostrando o que mudou em cada um. Se você montou algo parecido, ou resolveu a autenticação do Git de outro jeito, me conta: tenho interesse em comparar.

---

# Meta description

Painel local em Python puro para gerar um site estático, escrever artigos e enviar ao GitHub, com repositórios separados e token fora do disco.
