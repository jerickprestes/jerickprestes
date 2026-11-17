---
title: Cotação do dólar automática no Notion: PTAX do Banco Central + GitHub Actions
date: 2026-11-17
tags: python,API,automação,linux,git
summary: O Notion não consulta APIs externas sozinho. Resolvi com um script Node que roda uma vez por dia no GitHub Actions, lê a PTAX do Banco Central e grava a cotação numa database do Notion. Sem VPS, sem n8n e sem servidor para manter. O sistema lê o valor por relation e rollup, e uma fórmula avisa quando a cotação fica velha. Neste post estão o código completo, o passo a passo e o erro que me custou tempo.
cover: img/posts/01-fluxo-anotado-2.webp
---

## O problema: o Notion não busca dados de fora

Estamos montando, para um cliente, um sistema inteiro dentro do Notion. Ele precisa usar a cotação do dólar nos cálculos e manter esse valor atualizado todo dia. Fórmula do Notion não faz requisição HTTP, então alguma coisa de fora precisa buscar o valor e gravá-lo lá.

Meu caminho natural seria um n8n no meu VPS. Só que eu não tenho mais VPS. Make ou n8n Cloud resolveriam, mas colocam uma mensalidade na conta do cliente por um fluxo que roda uma vez por dia. Eu precisava de algo que rodasse sem servidor meu e sem assinatura nova.

## A abordagem: script + GitHub Actions, com duas fontes de cotação

Comparei três caminhos. A decisão saiu de custo, manutenção e do que acontece quando algo falha.

| Opção | Custo para rodar | Manutenção | Alerta de falha |
| --- | --- | --- | --- |
| n8n no VPS | VPS próprio (que não tenho mais) | Eu atualizo e cuido | Nativo |
| n8n Cloud ou Make | Mensalidade | Menor | Nativo |
| Script + GitHub Actions | Praticamente zero para uma execução por dia | O código é meu | E-mail do GitHub quando o workflow falha |

Fiquei com o script. O alerta por e-mail vem de graça: se o script lança erro, o workflow fica vermelho e o GitHub avisa o dono do repositório.

Para a cotação, uso duas APIs e gravo cada uma numa coluna:

- **PTAX, do Banco Central:** oficial, gratuita, sem chave. Em fins de semana e feriados a lista vem vazia, então o script volta até 7 dias procurando o último dia com valor.
- **AwesomeAPI:** cotação comercial em tempo real, mais simples de consumir.

O script também é idempotente. Ele procura a linha do dia na database e atualiza se ela existir, então rodar duas vezes não duplica nada. Guardo uma linha por dia para manter histórico.

## Passo a passo

### 1. Criar a integração no Notion

Abri notion.so/profile/integrations, criei uma integração interna no workspace do cliente e copiei o token (começa com `ntn_` ou `secret_`). Resultado: um token guardado para o passo 6.

### 2. Criar a database "Cotação" e conectar a integração

Montei uma database em tela cheia com estas colunas. Os nomes precisam ser idênticos aos que o script usa: `Name` (título), `Data` (tipo Data), `Comercial` (tipo Número) e `PTAX` (tipo Número). Depois, em `...` → Conexões, adicionei a integração. Sem essa conexão a API responde 404.

Copiei o link da database e peguei o ID: são os 32 caracteres antes do `?v=`. O que vem depois é o ID da view, não da database.


![descrição](img/posts/02-database-anotado.webp)


### 3. Criar o repositório

Criei um repositório **privado** no GitHub (usei o nome `cotacao-dolar-notion`). Escolhi privado porque, em repositório público, o GitHub desativa agendamentos depois de 60 dias sem atividade.

### 4. Adicionar o script

Em Add file → Create new file, digitei `scripts/update-cotacao.mjs` no campo do nome (a barra cria a pasta) e colei:

```js
const { NOTION_TOKEN, NOTION_DATABASE_ID } = process.env;
if (!NOTION_TOKEN || !NOTION_DATABASE_ID) {
  throw new Error("Faltam NOTION_TOKEN / NOTION_DATABASE_ID");
}

const TZ = "America/Sao_Paulo";
const hoje = new Date().toLocaleDateString("en-CA", { timeZone: TZ }); // AAAA-MM-DD

async function getJson(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(`${res.status} ${url}: ${await res.text()}`);
  return res.json();
}

async function getComercial() {
  const key = process.env.AWESOMEAPI_KEY;
  const data = await getJson(
    "https://economia.awesomeapi.com.br/json/last/USD-BRL",
    key ? { headers: { "x-api-key": key } } : undefined
  );
  return Number(data.USDBRL.ask);
}

// Volta até 7 dias para pular fins de semana e feriados
async function getPtax() {
  for (let i = 0; i < 7; i++) {
    const d = new Date(`${hoje}T12:00:00-03:00`);
    d.setDate(d.getDate() - i);
    const [y, m, day] = d.toLocaleDateString("en-CA", { timeZone: TZ }).split("-");
    const url =
      `https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/` +
      `CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='${m}-${day}-${y}'&$format=json`;
    const { value } = await getJson(url);
    if (value.length) return Number(value.at(-1).cotacaoVenda);
  }
  return null;
}

const notion = (path, method, body) =>
  getJson(`https://api.notion.com/v1${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${NOTION_TOKEN}`,
      "Notion-Version": "2022-06-28",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

const [com, ptx] = await Promise.allSettled([getComercial(), getPtax()]);
const comercial = com.status === "fulfilled" ? com.value : null;
const ptax = ptx.status === "fulfilled" ? ptx.value : null;

if (com.status === "rejected") console.warn("AwesomeAPI falhou:", com.reason.message);
if (ptx.status === "rejected") console.warn("PTAX falhou:", ptx.reason.message);

if (comercial == null && ptax == null) {
  throw new Error(`Nenhuma fonte respondeu.\n${com.reason}\n${ptx.reason}`);
}

const properties = {
  Name: { title: [{ text: { content: hoje } }] },
  Data: { date: { start: hoje } },
};
if (comercial != null) properties.Comercial = { number: comercial };
if (ptax != null) properties.PTAX = { number: ptax };

// Upsert: atualiza a linha de hoje se já existir
const { results } = await notion(`/databases/${NOTION_DATABASE_ID}/query`, "POST", {
  filter: { property: "Data", date: { equals: hoje } },
});

if (results.length) {
  await notion(`/pages/${results[0].id}`, "PATCH", { properties });
  console.log(`Atualizado: ${hoje} | comercial=${comercial} | ptax=${ptax}`);
} else {
  await notion("/pages", "POST", {
    parent: { database_id: NOTION_DATABASE_ID },
    properties,
  });
  console.log(`Criado: ${hoje} | comercial=${comercial} | ptax=${ptax}`);
}
```

### 5. Adicionar o workflow

Repeti o processo com o nome `.github/workflows/cotacao.yml`. O cron do GitHub é em UTC, então configurei `12:00` UTC, que são 9h em Brasília.

```yaml
name: Atualizar cotação do dólar

on:
  schedule:
    - cron: "0 12 * * *" # 09:00 em Brasília
  workflow_dispatch: # permite rodar manualmente

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: node scripts/update-cotacao.mjs
        env:
          NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
          NOTION_DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
          AWESOMEAPI_KEY: ${{ secrets.AWESOMEAPI_KEY }}
```


![descrição](img/posts/03-pastas-anotado.webp)


### 6. Cadastrar os secrets

Em Settings → Secrets and variables → Actions, criei `NOTION_TOKEN` e `NOTION_DATABASE_ID`. Criei também `AWESOMEAPI_KEY`, com a chave gratuita do cadastro em awesomeapi.com.br (explico o motivo nas armadilhas, abaixo).


![descrição](img/posts/04-secrets-anotado.svg)


### 7. Rodar na mão

Rodei na mão em Actions → Atualizar cotação do dólar → Run workflow. O esperado é um check verde e uma linha nova na database. O log termina com `Criado: AAAA-MM-DD | comercial=... | ptax=...`, ou `Atualizado` se a linha do dia já existia.


![descrição](img/posts/05-workflow-anotado.webp)


### 8. Ligar ao sistema do cliente

Na database que usa o dólar, criei uma relation com "Cotação" e um rollup chamado `Última cotação` (relation, propriedade `Data`, cálculo Latest date). Depois criei a fórmula `Status da cotação`, que me avisa quando o dado está velho:

```text
if(empty(prop("Última cotação")),
  "Sem cotação",
  if(dateBetween(now(), prop("Última cotação"), "days") > 2,
    "Cotação desatualizada",
    "Cotação em dia"
  )
)
```

Usei o limite de 2 dias porque o script roda todos os dias, inclusive nos fins de semana. Duas execuções seguidas sem gravar já indicam falha.

## Armadilhas e erros que enfrentei

### PTAX entrou MAS o Comercial ficou em branco

Fui até a database e a PTAX estava lá, mas a coluna Comercial estava vazia. Como o workflow não falhou, não havia nenhum erro para ler.

O culpado era meu próprio código. Uso `Promise.allSettled`, então, se uma fonte responde, o script segue em frente sem reclamar da outra. Acrescentei dois `console.warn` e rodei outra vez. O log entregou o motivo: `429 QuotaExceeded`, da AwesomeAPI. As chamadas sem chave que saem do GitHub tinham estourado a cota.



![descrição](img/posts/06-erro-429-anotado.webp)



Cadastrei uma chave gratuita em awesomeapi.com.br e passei a mandá-la no cabeçalho `x-api-key`. Rodei de novo e deu certo: o valor do Comercial passou a aparecer na database.

A lição que levei: quando duas fontes alimentam o mesmo dado, o log precisa dizer qual delas falhou.

## Resultado

O workflow rodou com sucesso em 21 segundos. Depois da chave, rodei outra vez e a linha passou a mostrar `Comercial 5,7871` e `PTAX 5,7324`&#32;


![descrição](img/posts/07-resultado-anotado-2.webp)


O desenho final é uma cotação oficial gravada todo dia às 9h, com uma linha por dia de histórico e sem servidor meu. Se a cotação parar de entrar, a fórmula de status avisa e o GitHub manda e-mail de falha. Antes do sistema no Notion, tudo na empresa do cliente era feito em planilhas, e a cotação era consultada todo dia, o tempo todo, em plataformas externas. Isso dava dor de cabeça. Agora o script grava o valor na database sem ninguém precisar ir buscar.

## Próximo passo

O que eu faria a seguir: manter uma única página "Cotação atual", atualizada todo dia pelo script, e ligar as databases do sistema a ela. Assim os cálculos não dependem de escolher a linha mais recente dentro de um rollup. O histórico continua na database diária. Também vale subir o `node-version` do workflow para uma versão mais nova, porque o GitHub já avisa que o Node 20 está sendo descontinuado.

Você usa outra fonte de cotação, ou resolveu isso de outro jeito no Notion? Me conta.

## Meta description

Como atualizei a cotação do dólar no Notion todo dia com a PTAX do Banco Central, um script Node e GitHub Actions, sem servidor.
