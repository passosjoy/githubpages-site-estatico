# GitHub Pages: site estático de portfólio para DevOps/SRE

Lab que ensina a montar e publicar um portfólio grátis com **GitHub Pages + GitHub Actions** e discute como o Pages vira uma ferramenta de engenharia no nível sênior: docs-as-code, runbooks, repositório de Helm charts, status page e relatórios de CI.

> Exemplo real: meu portfólio [passosjoy.github.io](https://passosjoy.github.io), gerado em Python a partir dos meus repositórios ([código](https://github.com/passosjoy/passosjoy.github.io)).

## Por que isso importa para quem é DevOps

Um recrutador técnico não vai rodar seu código, mas vai ler seu README. O portfólio é uma **entrevista assíncrona**: mostra como você decide, documenta e automatiza. E publicar o próprio site já é um pequeno projeto de DevOps, porque envolve:

| Prática | Onde aparece neste lab |
|---|---|
| CI/CD | workflow que valida e publica a cada push |
| Segurança de pipeline | deploy por OIDC (`id-token: write`), sem token salvo, com permissões mínimas |
| Infra como código | o site inteiro, a infraestrutura e o pipeline estão versionados no Git |
| Quality gate | `scripts/check_site.py` barra HTML quebrado e links internos inválidos |
| DNS/TLS | domínio próprio, registros A/CNAME e HTTPS |

## Estrutura

```text
.
├── site/                      # o que é publicado (HTML + CSS puros, zero dependências)
│   ├── index.html
│   ├── style.css
│   ├── 404.html
│   └── .nojekyll              # desliga o processamento Jekyll
├── scripts/check_site.py      # validação usada no CI
├── .github/workflows/pages.yml
└── docs/
    ├── 01-passo-a-passo.md    # do zero ao site no ar
    └── 02-discussao-tecnica.md# GitHub Pages no nível DevOps/SRE sênior
```

## Quickstart

```bash
# 1. use este repo como template (ou faça fork) e clone
git clone https://github.com/<seu-usuario>/githubpages-site-estatico.git
cd githubpages-site-estatico

# 2. veja localmente
python3 -m http.server 8000 --directory site   # http://localhost:8000

# 3. valide como o CI valida
python3 scripts/check_site.py site

# 4. na SUA cópia: Settings → Pages → Source: GitHub Actions
#    e Settings → Secrets and variables → Actions → Variables: ENABLE_PAGES=true
git commit -am "meu portfólio" && git push
```

> Este repositório é uma prova técnica e **não publica** o próprio site: o CI só valida. O job `deploy` fica desligado até alguém definir `ENABLE_PAGES=true`, um padrão útil para templates.

O endereço publicado depende do nome do repositório:

| Repositório | URL |
|---|---|
| `<usuario>.github.io` | `https://<usuario>.github.io/` (site de usuário, só um por conta) |
| qualquer outro, ex. `githubpages-site-estatico` | `https://<usuario>.github.io/githubpages-site-estatico/` (site de projeto) |

## Leitura

1. [Passo a passo](docs/01-passo-a-passo.md): criar, publicar, domínio próprio e checklist do conteúdo.
2. [Discussão técnica](docs/02-discussao-tecnica.md): arquitetura, segurança, limites, trade-offs e usos avançados para DevOps/SRE.
