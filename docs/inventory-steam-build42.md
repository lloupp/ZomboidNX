# Steam Project Zomboid Build 42 — inventário real

**Origem:** resumo de execução enviado pelo usuário em 2026-10-10. Dados informados pelo agente no PC; o JSON completo não foi inspecionado nesta PR.

## Instalação Steam relatada
- Diretório relativo ao home: snap/steam/common/.local/share/Steam/steamapps/common/ProjectZomboid/projectzomboid
- version.txt: 42.20.2 (Build 42)
- ProjectZomboid64: ELF x86_64, 95.976 bytes
- projectzomboid.jar: aproximadamente 64,5 MiB
- Runtime Java: jre64/; dependências compartilhadas: natives/*.so (x86_64)
- Total informado: 47.823 arquivos, ~10,45 GiB, 58 ELF x86_64, 9 ELF AArch64 e 67 arquivos .so.

## Limites das conclusões
1. Identificar nominalmente os nove ELF AArch64: ARM64 por si só não significa compatibilidade com Nintendo Switch/Horizon.
2. ELF x86_64 Linux não é executável nativamente em Horizon/ARM64.
3. Verificar versões de bytecode Java e as dependências de JNI, LWJGL, renderização e áudio antes de escolher uma estratégia de runtime.
4. Não extrapolar dependências da Build 41 para a Build 42 sem confirmação.

## Próximos marcos
- [ ] Extrair metadados (caminhos relativos, arquiteturas, tamanhos) dos nove ELF AArch64, sem publicar arquivos binários.
- [ ] Inventariar JARs, versão de classfiles, JNI, gráficos e áudio.
- [ ] Medir consumo real de RAM da Build 42 no PC e comparar com recursos disponíveis no Switch.
- [ ] Testar fisicamente o diagnóstico NRO no Switch V2 com Atmosphère: inicialização, botões A/B/+, memória de 16 MiB e leitura de SD.
- [ ] Somente então iniciar PoC legal de Java e gráficos compatíveis com o hardware.

## Diagnóstico homebrew já compilado
Compilação GitHub Actions aprovada: https://github.com/lloupp/ZomboidNX/actions/runs/38045678335
Artefato: ZomboidNX-diagnostic-NRO. É um teste independente, **não é Project Zomboid**, não contém arquivos proprietários e não foi validado no console físico.
