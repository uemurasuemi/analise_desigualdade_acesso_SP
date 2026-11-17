# Dashboard Desigualdade Educacional SP

## Como executar no VS Code
1. Extraia o ZIP e abra a pasta `educacao_sp_dashboard` em **Arquivo > Abrir Pasta**.
2. Abra `index.html`.
3. Instale a extensão **Live Server** (Ritwick Dey) no menu Extensões, caso queira usar o servidor local.
4. Clique com o botão direito em `index.html` > **Open with Live Server**. Também funciona abrindo o HTML diretamente no navegador, pois os dados estão embutidos em arquivos JavaScript locais.

Arquivos: `index.html` (estrutura), `style.css` (layout), `app.js` (gráficos, filtros e exportação), `dados/fluxo.js` e `dados/renda.js` (dados consolidados), `gerar_dados.py` (processamento de fontes, para uso no ambiente original), e `dados/*.json` (cópias legíveis dos dados).

## Metodologia e limitações
- Fluxo escolar 2021–2025: médias **simples**, não ponderadas, de APR/REP/ABA por escola e etapa, excluindo valores sem soma próxima a 100%.
- `Etapa 1/2/3`: correspondência dos sufixos originais das colunas. Confirmar no dicionário oficial a nomenclatura dos níveis de ensino.
- O recorte por zona usa apenas diretorias explicitamente identificadas como NORTE, SUL, LESTE ou OESTE da capital. Não equivale a todas as escolas da zona nem a uma classificação georreferenciada por endereço. O grupo Estado inclui Capital e Interior.
- O Top 10 é entre os recortes agregados disponíveis (até 7), não entre escolas. Não há classificação completa de todos os municípios nem de todas as zonas.
- Renda: remuneração média mensal do emprego formal por distrito, não renda domiciliar ou classe social individual.
- Correlação: o abandono municipal por distrito do Mapa da Desigualdade de 2025 é usado **apenas** quando disponível no mesmo distrito/ano. Não combinar a renda distrital diretamente com taxas por escola sem georreferenciamento.
- Ausência de frequência escolar e de evasão longitudinal nas planilhas enviadas. Abandono anual é indicador diferente de evasão.
- Valores publicados em edições anuais do Mapa da Desigualdade podem refletir anos de referência anteriores à edição.

Fontes complementares para contextualização: IBGE Cidades (São Paulo), Fundação Seade e reportagens sobre o Mapa da Desigualdade. A apresentação deve evitar atribuir números a esses links sem consulta e validação específica.

## Alterações solicitadas
- Título superior: Escolaridade x Renda.
- Filtros de ano e etapa dentro da lâmina Panorama.
- Explicação de Pearson na lâmina Renda.
- Removidos os cartões macro do Analítico e os selos do cabeçalho.
- Rodapé com fontes dos dados e links complementares de contextualização.
