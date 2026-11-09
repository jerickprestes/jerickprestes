# Erick Prestes | Portfólio

Site de portfólio pessoal, estático (HTML, CSS e JS), baseado no template [Hyperspace](https://html5up.net/hyperspace) do HTML5 UP (licença CCA 3.0, veja `LICENSE.txt`).

Publicado em: https://jerickprestes.github.io/jerickprestes/

## Estrutura da página

Página única (`index.html`) com sidebar de navegação e três seções:

| Seção | Âncora | Conteúdo |
|---|---|---|
| Início (hero) | `#intro` | Foto, apresentação, botões **Ver currículo** e **Entre em contato**, contato (cidade, e-mail, telefone, LinkedIn, GitHub, WhatsApp) e marquee de tecnologias |
| Trabalho | `#sites-trabalhados` | Cards dos sites em que trabalhei |
| Layouts | `#layouts-produzidos` | Carrossel (Swiper.js) de layouts com lightbox, lupa de ampliação e botão **Acessar projeto** (GitHub) |

## Funcionalidades

- **Currículo:** o botão "Ver currículo" abre `J-Erick-Prestes-2026-v5.pdf` em nova aba. Para atualizar, substitua o PDF e ajuste o `href` do botão na hero.
- **Formulário de contato (off-canvas):** abre pelos botões/ícones com o atributo `data-open-contact` (botão "Entre em contato" e ícone de WhatsApp da hero). Ao enviar, monta uma mensagem e abre `https://wa.me/<número>?text=...` em nova aba. Não há backend. O número fica na variável `whatsappNumber`, no script ao final do `index.html` (atualmente `5512981452330`).
- **Layouts:** clicar na thumbnail (identificada pela lupa no canto superior direito) abre o lightbox, com navegação por setas e teclado (Esc fecha). O botão "Acessar projeto" abre o repositório no GitHub.

## Pendências

- [ ] Trocar o `href` de cada botão "Acessar projeto" pelo repositório correspondente (hoje todos apontam para `https://github.com/jerickprestes/`).

## Estrutura de arquivos

```
index.html                     Página única
J-Erick-Prestes-2026-v5.pdf    Currículo
assets/                        CSS, SASS, JS (jQuery, scrollex/scrolly) e Font Awesome
images/                        Foto, logos (logos/), sites (jpg/) e layouts (screenshots/)
LICENSE.txt                    Licença do template
```

## Dependências externas

- [Swiper.js 11](https://swiperjs.com/) via CDN (jsDelivr), usado no carrossel de layouts.

## Créditos

Template base: Hyperspace por [HTML5 UP](https://html5up.net) (@ajlkn), licença CCA 3.0.
