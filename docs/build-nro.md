# Compilação do diagnóstico ZomboidNX (.nro)

O arquivo gerado aqui é um **diagnóstico homebrew independente**, não um port jogável de Project Zomboid.

## Opção A — GitHub Actions (sem instalar devkitPro no PC)

1. Abra a PR #1 e sua aba **Checks**, ou o menu **Actions** > **Build Switch diagnostic NRO**.
2. Confira se o workflow da branch `feasibility-2026-10-09` terminou com status **success**.
3. Na página da execução, seção **Artifacts**, baixe `ZomboidNX-diagnostic-NRO`. Extraia o ZIP.
4. Confirme que existe `zomboidnx.nro`. Se a compilação não concluir com sucesso, **não há build validada**.
5. No computador com o cartão microSD montado, copie o arquivo para `switch/zomboidnx.nro` na raiz do cartão (crie a pasta `switch`, se necessário).
6. No Switch V2 com Atmosphère, abra o hbmenu via **title override** e execute ZomboidNX.
7. Pressione **A** para testar uma alocação de 16 MiB, **B** para checar um manifesto opcional em SD e **+** para sair.

O teste físico deve registrar se o programa inicia, qual resultado é apresentado e se os botões respondem. A compilação por si só **não comprova execução em hardware**.

## Opção B — Linux com Docker

Requer Docker instalado no host. Na raiz do clone ZomboidNX:

```bash
git clone https://github.com/switchbrew/switch-examples.git _switch-examples
docker run --rm -v "$PWD:/workspace" -w /workspace devkitpro/devkita64:20260219 bash scripts/build-nro.sh
ls -lh out/zomboidnx.nro
```

O arquivo será gravado em `out/zomboidnx.nro`. Para Windows com Docker Desktop, execute em um terminal WSL com acesso ao Docker.

## Limites e direitos

- Não colocar conteúdo da instalação comercial de Project Zomboid no GitHub ou no artefato do CI.
- A pasta de saves do usuário `~/Zomboid` **não é** a instalação de Steam que precisamos inventariar. Localize a pasta real via Steam → Propriedades → Arquivos instalados → Explorar.
- Se o build falhar, registre o log da etapa `Build NRO` e corrija o código; não declare sucesso sem artefato verificado.
- O usuário decidirá se faz merge da PR após revisar os resultados.
