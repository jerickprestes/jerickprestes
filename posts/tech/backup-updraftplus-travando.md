---
title: Backup que trava: diagnóstico do UpdraftPlus em hospedagem compartilhada
date: 2026-10-14
tags: Infra, WordPress
summary: Como investigar um backup que nunca termina e o que ajustar no servidor.
cover: 
---

O backup começava, chegava ao arquivo de uploads e ficava parado. Sem erro, sem aviso, só o processo que nunca termina. O primeiro instinto é culpar o plugin. Neste caso, o problema estava mais embaixo.

### Passo 1: descartar o óbvio

A hospedagem verificou os recursos do servidor: **CPU, memória e processos estavam normais**. Isso eliminou a explicação mais comum (falta de recurso) e apontou para outra direção.

### Passo 2: olhar o disco

O suporte confirmou que o **I/O de disco batia no teto em picos**. Compactar uploads é uma operação de muita leitura e escrita; se o disco já está saturado por outras coisas, o backup é o primeiro a engasgar.

### Passo 3: descobrir quem consome I/O

Nos logs de acesso, os maiores geradores de requisições foram:

- `xmlrpc.php`, quase sempre tráfego automatizado e tentativas de login;
- `admin-ajax.php`, usado por muitos plugins e pelo próprio painel;
- `?wc-ajax=get_refreshed_fragments`, do WooCommerce, que atualiza o mini carrinho e dispara em várias páginas;
- `updraft_ajax`, o próprio backup, competindo consigo mesmo;
- **um único IP com volume alto de requisições**.

### O que costuma resolver

Estas são medidas gerais para esse cenário, não uma receita única:

1. **Bloquear ou limitar o `xmlrpc.php`** se o site não depende dele.
2. **Reduzir o `get_refreshed_fragments`**: em páginas que não mostram carrinho, desativar o script.
3. **Limitar o IP abusivo** com regra de firewall ou bloqueio na hospedagem.
4. **Agendar o backup em horário de menor tráfego** e, se possível, separar arquivos e banco em jobs diferentes, com divisão de arquivos em partes menores.

### Lição

Backup travado raramente é problema do backup. Antes de trocar de plugin, meça o que está ocupando o servidor no momento em que ele falha.
