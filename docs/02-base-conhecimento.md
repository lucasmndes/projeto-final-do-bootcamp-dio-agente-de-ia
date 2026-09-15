# 2. Base de conhecimento

## Estratégia

A base foi escrita do zero como uma abstração educacional do mercado de pagamentos. Nenhum arquivo corporativo é indexado, publicado, copiado ou enviado ao protótipo. Não há nomes de empresas, pessoas, clientes, fornecedores, sistemas, endereços, valores, limites, métricas, incidentes, fluxos proprietários ou avaliações internas.

O conteúdo está em `data/base_conhecimento.json`; as URLs oficiais ficam em `data/fontes_publicas.json`. Separar conteúdo e fonte facilita revisão, atualização e auditoria.

## Modelo de cada tópico

| Campo | Função |
|---|---|
| `id` e `titulo` | identificação estável e legível |
| `palavras_chave` | recuperação do assunto |
| `resumo` | princípio geral |
| `orientacoes` | ações preventivas genéricas |
| `sinais_alerta` | situações que pedem atenção, sem concluir irregularidade |
| `escalar_quando` | limite da automação e próxima ação humana |
| `fontes` | referências públicas ou categoria de regra aplicável |

## Domínios cobertos

1. Governança, ética e integridade;
2. KYC/KYB, parceiros e colaboradores;
3. PLD/FT, PEP e sanções;
4. Credenciamento e monitoramento de estabelecimentos;
5. Fraude, contestação e chargeback;
6. Recebíveis e liquidação;
7. LGPD e direitos de titulares;
8. Segurança e resposta a incidentes;
9. Continuidade e risco operacional;
10. Desenvolvimento seguro e mudanças.

## Recuperação

A pergunta é normalizada, tokenizada e comparada com palavras-chave, título e resumo. Correspondências explícitas recebem peso maior. O tópico mais aderente compõe a resposta. Se nenhum tópico atingir correspondência mínima, o agente informa insuficiência de evidência e recomenda validação humana.

## Governança do conteúdo

- registrar versão e data de revisão;
- revisar periodicamente vigência, alterações e aplicabilidade das fontes;
- exigir revisão especializada antes de incluir ou alterar conteúdo;
- usar dados fictícios em demonstrações e testes;
- não transformar documentos internos em embeddings ou prompts;
- remover conteúdo obsoleto, preservando histórico de mudança no Git;
- testar vazamento e respostas adversariais antes de cada versão.

## Referências públicas

A seleção inicial usa legislação federal, Banco Central do Brasil e Autoridade Nacional de Proteção de Dados. A Lei nº 12.865/2013 disciplina arranjos e instituições de pagamento; a Circular BCB nº 3.978/2020 trata de controles de PLD/FT para instituições autorizadas; a LGPD disciplina o tratamento de dados pessoais; e a Resolução CD/ANPD nº 15/2024 regulamenta a comunicação de incidentes.

Aplicabilidade não é presumida: obrigações variam conforme papel, autorização, arranjo, produto, contrato e fato concreto. Por isso, referências contratuais e regras de arranjos são indicadas como categorias que exigem consulta à versão vigente e ao instrumento aplicável.
