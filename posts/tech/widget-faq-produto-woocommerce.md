---
title: Widget de FAQ para páginas de produto no WooCommerce
date: 2026-11-10
tags: WordPress, WooCommerce, Elementor
summary: Um widget de perguntas frequentes por produto, editável no painel e integrado ao Elementor.
cover: 
---

Toda loja tem as mesmas dúvidas se repetindo no WhatsApp: prazo, troca, material, como usar. Responder isso dentro da própria página do produto reduz o atendimento repetido e ainda ajuda no SEO. Foi o que construí: um FAQ por produto, editável no painel do WooCommerce e exibido como acordeão.

### A ideia

Cada produto precisa ter a sua lista de perguntas e respostas, e quem edita a loja não deve mexer em código. A solução usa um meta box no cadastro do produto com campos repetíveis (pergunta e resposta), salvos como um único meta do produto (`_product_faqs`). Na página, o widget lê esse meta e desenha o acordeão.

### O que importa na construção

**1. Meta box repetível.** O editor adiciona, remove e reordena perguntas sem sair da tela do produto. Os dados ficam em um array no post meta, então não é preciso criar tabela nem plugin extra.

**2. Interface em acordeão com CSS puro.** A animação de abrir e fechar usa transições de CSS, sem biblioteca. Isso mantém o carregamento leve.

**3. Estilo isolado do tema.** Temas de WooCommerce costumam ter estilos agressivos para listas, botões e títulos, que quebram um widget novo. Usei prefixo próprio nas classes (`wcpfaq-`) e `all: unset` nos elementos do componente, para que o tema não interfira.

```css
.wcpfaq-item button {
  all: unset;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  width: 100%;
}
```

**4. Schema para buscadores.** O mesmo conjunto de perguntas gera a marcação JSON-LD do tipo `FAQPage`. É o que permite aos buscadores entender a seção como perguntas e respostas.

```php
$schema = [
  '@context'   => 'https://schema.org',
  '@type'      => 'FAQPage',
  'mainEntity' => array_map(fn($f) => [
    '@type' => 'Question',
    'name'  => $f['pergunta'],
    'acceptedAnswer' => ['@type' => 'Answer', 'text' => wp_strip_all_tags($f['resposta'])],
  ], $faqs),
];
echo '<script type="application/ld+json">' . wp_json_encode($schema) . '</script>';
```

### Integração com o Elementor

Para quem monta a página no Elementor, o FAQ aparece como widget: o designer posiciona no layout e o conteúdo vem do produto atual. Assim o mesmo template serve para todos os produtos.

### Detalhes que dão trabalho

- Texto longo estourando o container: precisa de regra de quebra de linha e `overflow` tratados.
- Posição do ícone de abrir/fechar: com títulos de duas linhas o ícone sai do lugar se o alinhamento não for pensado.
- Conflito com o estilo do tema: foi o que motivou o isolamento descrito acima.

### Alternativa: ACF PRO

Se o projeto já usa ACF PRO, dá para fazer o mesmo com um campo Repeater (`faq_produto`, com `pergunta` e `resposta`) restrito ao tipo de post `product` e exibir com o hook `woocommerce_after_single_product_summary`. Fica mais rápido de montar; em troca, você depende do plugin.
