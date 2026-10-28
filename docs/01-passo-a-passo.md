# 01 — Passo a passo: do zero ao portfólio no ar

## 1. Escolha o tipo de site

- **Site de usuário** (`<usuario>.github.io`): a "home" do seu perfil. Use para o portfólio principal.
- **Site de projeto** (qualquer repo): fica em `/<repo>/`. Use para a documentação de cada lab.

Os dois são grátis em repositórios **públicos**. No plano Free, o Pages não publica a partir de repositório privado.

## 2. Crie o repositório

1. GitHub → **New repository** → nome `<usuario>.github.io` (ou outro nome) → **Public**.
2. Copie a pasta `site/` e o workflow `.github/workflows/pages.yml` deste lab.

## 3. Duas formas de publicar

| | Branch (legado) | **GitHub Actions (recomendado)** |
|---|---|---|
| Como funciona | o GitHub publica uma pasta de uma branch e roda Jekyll | o seu workflow gera o site e publica um artefato |
| Gerador | só Jekyll | qualquer um: Python, Hugo, MkDocs, Astro… |
| Validação antes de publicar | não | sim (testes, lint, link check) |
| Limite de 10 builds/hora | aplica | não se aplica |

Para usar Actions: **Settings → Pages → Build and deployment → Source: GitHub Actions**. Neste lab, o deploy também exige a variável de repositório `ENABLE_PAGES=true` (**Settings → Secrets and variables → Actions → Variables**). Assim, quem faz fork sem querer publicar fica só com a validação.

## 4. Entenda o workflow

```yaml
permissions:
  contents: read     # lê o código
  pages: write       # publica no Pages
  id-token: write    # gera o token OIDC usado pelo deploy-pages
```

1. `build` faz o checkout, roda o `check_site.py` e empacota `site/` com `upload-pages-artifact`.
2. `deploy` só roda na `main` com `ENABLE_PAGES=true` (em PR ele apenas valida). Ele publica com `deploy-pages` no environment `github-pages`, e a URL aparece no resumo do job.
3. `concurrency: pages` evita dois deploys simultâneos.

## 5. Publique

```bash
git add . && git commit -m "feat: portfólio" && git push
```

Acompanhe na aba **Actions**. O site sobe em cerca de 1 minuto.

## 6. Domínio próprio (opcional)

1. Compre o domínio (registro.br, Cloudflare, etc.).
2. **Verifique o domínio** na conta: GitHub → Settings (do perfil) → Pages → *Add a domain*. Isso cria um registro TXT e impede que outra conta "sequestre" o domínio se a configuração ficar órfã (domain takeover).
3. DNS:
   ```text
   @    A      185.199.108.153
   @    A      185.199.109.153
   @    A      185.199.110.153
   @    A      185.199.111.153
   www  CNAME  <usuario>.github.io.
   ```
   Para IPv6, crie os registros AAAA `2606:50c0:8000::153` até `2606:50c0:8003::153`.
4. Repo → Settings → Pages → **Custom domain** → marque **Enforce HTTPS**. O certificado é emitido pelo Let's Encrypt; se o domínio tiver registro CAA, ele precisa autorizar `letsencrypt.org`.
5. Confira:
   ```bash
   dig +short seudominio.com.br
   curl -sI https://seudominio.com.br | head -5
   ```

## 7. O que colocar no portfólio (checklist de recrutador)

- [ ] Uma frase de posicionamento: "Eu automatizo X e reduzo Y".
- [ ] De 3 a 6 projetos **reproduzíveis**, cada um com problema, arquitetura (diagrama), decisões, segurança e resultado medido.
- [ ] Um link do card para o repo, com um README que funcione sozinho (comandos que rodam).
- [ ] Números reais: "drift corrigido em 49s", "deploy de 20 para 4 min", "custo -30%".
- [ ] Contato (LinkedIn e e-mail) e as vagas que você busca.
- [ ] Nada de segredo, IP interno ou nome de cliente.

## 8. Exercícios

1. Troque o tema de cores em `site/style.css` e adicione um projeto seu.
2. Quebre de propósito um link em `index.html` e veja o CI falhar no PR.
3. Configure um domínio e valide o HTTPS com `curl -I`.
4. Substitua o HTML manual por um gerador (MkDocs, Hugo ou Python + Jinja2) sem mudar o job de `deploy`.
