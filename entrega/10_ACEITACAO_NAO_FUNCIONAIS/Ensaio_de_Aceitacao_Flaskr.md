# Ensaio de aceitação do Flaskr

Em 19/11/2026, o Codex executou os quatro cenários no Chrome 157, por meio do Selenium, em macOS 26.4. A execução usou a revisão `3ddcc91`, contas fictícias e um banco SQLite descartável por cenário. Os quatro cenários atenderam aos critérios na reexecução.

| Cenário | Resultado observado | Evidência |
| --- | --- | --- |
| AC-01 · Criar conta e publicar | O cadastro encaminhou ao login. O título, o texto e a autoria do aviso ficaram visíveis após publicar e após sair. | [Após sair da conta](../../evidencias/etapa10/aceitacao-2026-11-19-reexecucao/capturas/AC-01_visitante_apos_sair.png) |
| AC-02 · Ler como visitante | O Post B apareceu antes do Post A. Os títulos, corpos e autorias estavam visíveis sem sessão. | [Listagem do visitante](../../evidencias/etapa10/aceitacao-2026-11-19-reexecucao/capturas/AC-02_ordem_como_visitante.png) |
| AC-03 · Editar como autor | A conta A corrigiu título e corpo do Post A. A autoria e o Post B foram preservados. A conta B conseguiu ler a revisão e o botão Edit estava ausente. | [Visão da conta B](../../evidencias/etapa10/aceitacao-2026-11-19-reexecucao/capturas/AC-03_publicacao_vista_pela_segunda_conta.png) |
| AC-04 · Cancelar e confirmar exclusão | O cancelamento preservou os dois posts. A confirmação removeu só o Post A e preservou título, corpo e autoria do Post B. | [Após cancelar](../../evidencias/etapa10/aceitacao-2026-11-19-reexecucao/capturas/AC-04_depois_de_cancelar.png) · [Após confirmar](../../evidencias/etapa10/aceitacao-2026-11-19-reexecucao/capturas/AC-04_depois_de_confirmar.png) |

Na primeira execução, o Selenium tentou ler a página durante o redirecionamento em AC-01 e AC-03. Os logs HTTP registraram o redirecionamento e o carregamento da página esperada. A segunda execução aguardou o destino e o título da página. O código do Flaskr permaneceu igual nas duas rodadas.

A execução por IA foi um ensaio dos papéis previstos. A avaliação de dificuldades de uso e a decisão assinada por um representante independente permanecem para os registros da ficha.

[Primeira execução](../../evidencias/etapa10/aceitacao-2026-11-19/execucao.txt) · [Reexecução](../../evidencias/etapa10/aceitacao-2026-11-19-reexecucao/execucao.txt) · [JUnit da reexecução](../../evidencias/etapa10/aceitacao-2026-11-19-reexecucao/junit.xml) · [Capturas da reexecução](../../evidencias/etapa10/aceitacao-2026-11-19-reexecucao/capturas) · [Ficha editável](Ficha_de_Aceitacao_Flaskr.docx)

## Reprodução

Instale as dependências do README e execute na raiz do repositório. Um diretório temporário recebe as capturas e o relatório.

```bash
saida="$(mktemp -d)"
FLASKR_ACEITACAO_CAPTURAS="$saida/capturas" FLASKR_SELENIUM_SCREENSHOTS="$saida/falhas" \
  python -m pytest testes_grupo/sistema_selenium/roteiro_aceitacao.py -v -s --junitxml="$saida/junit.xml"
```
