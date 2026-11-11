---
title: Fotos de produto com IA: como evitar rótulos distorcidos
date: 2026-11-08
tags: Geração de imagem, Prompts
summary: IA gera luz e cenário bonitos, mas estraga o texto do rótulo. A saída é não pedir isso para ela.
cover: 
---

Gerar foto de produto com IA tem um problema conhecido: a luz, o fundo e a sombra saem ótimos, mas **o texto do rótulo sai deformado**. Letras trocadas, marca ilegível, detalhes inventados. Para um produto real, isso é inaceitável: o rótulo é justamente o que não pode mudar.

### Por que acontece

Modelos de imagem recriam a cena inteira, inclusive o texto, e texto pequeno e curvo é onde eles mais erram. Insistir no prompt ("preserve o rótulo fielmente") ajuda um pouco, mas não resolve de forma confiável.

### A mudança de abordagem

Em vez de brigar com o rótulo, **tirei o rótulo da equação**:

1. **Gerar a cena sem rótulo.** Com a foto do produto como referência, peço no prompt para remover o rótulo. Isso funcionou bem: sai um frasco limpo, na iluminação e no cenário desejados.
2. **Usar a imagem gerada como camada de luz.** No Photoshop, a imagem sem rótulo entra por cima da foto original do produto em **modo de mesclagem** (blending mode), transferindo iluminação e sombra.
3. **O rótulo real continua o original.** Como a camada é só luz, o texto vem da foto verdadeira, intacto.

### O que o prompt precisa dizer

Um bom prompt de cena descreve o essencial e deixa o resto para a foto real:

- fundo e superfície (por exemplo, fundo liso e mesa clara);
- direção e suavidade da luz e onde cai a sombra;
- ângulo da câmera e enquadramento;
- **sem texto, sem rótulo**, para não gerar o que vai ser descartado.

### Resultado

Iluminação de estúdio sem fotógrafo, com o rótulo 100% fiel. A IA faz o que ela faz bem (luz e atmosfera) e a foto real faz o que só ela pode fazer (a marca).
