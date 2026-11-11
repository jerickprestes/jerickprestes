---
title: Catálogo de produtos com CPT, sem WooCommerce
date: 2026-10-28
tags: WordPress, Performance
summary: Quando o WooCommerce completo é exagero: catálogo leve com post type customizado.
cover: 
---

Nem todo site que mostra produtos precisa vender produtos. Em um projeto, a página precisava de vitrine no estilo e-commerce (grades, carrossel, banners e categorias), mas a venda era negociada fora do site, em lotes para empresas, condomínios e hospitais. Instalar o WooCommerce inteiro para isso seria trazer carrinho, checkout, scripts e tabelas que ninguém ia usar.

### A decisão

Em vez do ecossistema completo, criei um **Custom Post Type** próprio para os produtos, com uma taxonomia de categorias. O CPT dá tudo o que uma vitrine precisa: listagem, página individual, categorias e campos personalizados. O que ele não traz é peso.

### O que ganhei

- **Performance:** menos plugins, menos scripts carregados em cada página e menos consultas ao banco. Em um site cujo objetivo é gerar contato, velocidade de carregamento pesa.
- **Menos superfície de manutenção:** sem atualizações de WooCommerce, extensões de pagamento ou conflitos entre elas.
- **Controle do conteúdo:** o cliente edita produtos como edita qualquer post.

### O que precisou ser reconstruído

Sem o WooCommerce, alguns recursos que o tema espera deixam de existir. Foi preciso:

1. **Integrar o CPT ao tema** que o projeto já usava, para que os grids e carrosséis exibissem os produtos do CPT.
2. **Pequenas compatibilidades via snippets**, carregados por plugin de snippets (como o WPCode), em vez de editar o tema. Assim as mudanças ficam isoladas e são fáceis de desligar.

```php
register_post_type('produto', [
  'label'        => 'Produtos',
  'public'       => true,
  'has_archive'  => true,
  'menu_icon'    => 'dashicons-products',
  'supports'     => ['title', 'editor', 'thumbnail', 'excerpt'],
  'show_in_rest' => true,
]);
register_taxonomy('categoria_produto', 'produto', [
  'label' => 'Categorias de produto', 'hierarchical' => true, 'show_in_rest' => true,
]);
```

### Quando vale (e quando não)

Vale quando o site **apresenta** produtos e o contato fecha a venda por WhatsApp, e-mail ou orçamento. Não vale se você precisa de carrinho, pagamento online, estoque ou frete: aí o WooCommerce é a ferramenta certa, e reinventá-lo custa mais do que usá-lo.
