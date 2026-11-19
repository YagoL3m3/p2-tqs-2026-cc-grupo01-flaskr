# Execução manual do Flaskr

Turma B, Grupo 1 · Projeto P2 · Etapa 4A

Use o [catálogo da Etapa 3](../04_CASOS_E_RASTREABILIDADE/Requisitos_Casos_e_Rastreabilidade_Flaskr.xlsx) para executar os casos e a [planilha da Etapa 4A](Registro_de_Execucao_Manual_Flaskr.xlsx) para registrar o ocorrido. A versão alvo é Flaskr 1.0.0, do tutorial na tag Flask 3.1.3 e commit de origem `22d9247`.

## Preparar cada caso

Abra um terminal na raiz do repositório e ative um ambiente virtual. Instale o Flaskr uma vez nesse ambiente.

```sh
python -m pip install "Flask==3.1.3" -e ./flaskr-app
```

Encerre o servidor anterior com Ctrl+C e prepare uma base independente para o próximo caso.

```sh
python tools/resetar_banco_etapa4.py --massa vazia
```

O comando imprime a pasta temporária do novo banco. Use `vazia` quando o caso exigir cadastro, listagem vazia ou preparação do zero. Escolha `contas` se a pré-condição permitir as contas A e B previamente cadastradas. Use `publicacoes` se ela permitir as duas contas e os posts A e B da conta A. A [massa fictícia](../../testes_grupo/dados/massa_etapa4.json) traz os nomes, senhas de teste e conteúdo.

Copie o caminho retornado para `FLASKR_QA_DIR`.

- No macOS ou Linux, use `export FLASKR_QA_DIR="/caminho/retornado"`.
- No PowerShell, use `$env:FLASKR_QA_DIR = "C:\caminho\retornado"`.

```sh
python -m flask --app tools.resetar_banco_etapa4:criar_app run --host 127.0.0.1 --port 5001
```

Abra `http://127.0.0.1:5001/` e confirme que a tela **Posts** corresponde à massa escolhida. Use uma sessão limpa no início de cada caso e mantenha a mesma sessão onde o procedimento exigir. Se a porta 5001 estiver ocupada, escolha uma porta local livre e use-a nas URLs do caso. Anote a versão do navegador, do Python e a revisão em teste (`git rev-parse --short HEAD`).

- **CT-026, armazenamento da senha.** Abra outro terminal com o mesmo ambiente e a mesma `FLASKR_QA_DIR`. Execute `python -m flask --app tools.resetar_banco_etapa4:criar_app shell` e siga a consulta da aba Rastreabilidade. Registre os resultados booleanos sem copiar senha ou hash para a evidência.
- **CT-027, reinício.** Encerre o servidor e repita o comando `run` com a mesma `FLASKR_QA_DIR`. Prepare um novo banco somente depois de concluir o caso.

## Registrar resultados

1. Execute os passos do caso e compare o que apareceu com o resultado esperado.
2. Preencha data, versão, executor, resultado observado e situação. Use **Aprovado**, **Reprovado**, **Bloqueado** ou **Não executado**. Registre o motivo em caso de bloqueio.
3. Salve o print com o padrão `CT-XXX_AAAA-MM-DD.png` e informe o caminho na planilha. Se houver várias capturas, acrescente `_01`, `_02` e assim por diante antes de `.png`. Vincule uma nova execução aos registros anteriores se houver reteste.
4. Se houver desvio reproduzível, o grupo valida o diagnóstico e usa o [modelo de defeito](../../.github/ISSUE_TEMPLATE/defeito.md). Relacione o ID `BUG-XXX` à linha da execução depois de registrar a issue.

[PENDENTE-HUMANO: executar os 28 casos no navegador, preencher as 28 linhas e anexar as evidências reais | Grupo 1]
