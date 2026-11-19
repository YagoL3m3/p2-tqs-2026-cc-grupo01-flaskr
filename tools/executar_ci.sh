#!/usr/bin/env bash
set -uo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
saida="${1:-artefatos-ci}"
mkdir -p "$saida" || exit 1

python -m pytest flaskr-app/tests testes_grupo/unitarios \
  --junitxml="$saida/junit.xml" \
  --cov --cov-config=.coveragerc --cov-report=term-missing \
  --cov-report="xml:$saida/coverage.xml"
resultado_pytest=$?

python tools/executar_postman.py \
  --relatorio-json "$saida/postman.json" --junitxml "$saida/postman.xml"
resultado_postman=$?

FLASKR_SELENIUM_SCREENSHOTS="$saida/capturas" \
  python -m pytest testes_grupo/sistema_selenium --junitxml="$saida/selenium.xml"
resultado_selenium=$?

printf 'Códigos de saída: pytest=%s, Newman=%s, Selenium=%s\n' \
  "$resultado_pytest" "$resultado_postman" "$resultado_selenium"

(( resultado_pytest == 0 && resultado_postman == 0 && resultado_selenium == 0 ))
