# Painel Matemático — DPS Sprint 4

Entrega de **Differentiated Problem Solving** do Challenge FIAP + Hospital Moinhos de Vento. Esta versão evolui o painel de limites e derivadas da Sprint 3: acrescenta **integrais**, comparação de cenários e uma **regra de decisão**. O [PDF único para submissão](ENTREGA_DPS_SPRINT4.pdf) apresenta os critérios da Sprint 4 com gráficos e interpretação.

## Relação com o MVP

O [Simulador Clínico publicado](https://simulador-clinico-front.vercel.app) inclui o caso **“Síndrome coronariana - caso didático”**. No código desse caso, a saturação de oxigênio começa em **90%** e o valor crítico configurado é **85%**. Esses dois números são a base coerente usada aqui. O painel Streamlit contém um acesso ao simulador e compara duas trajetórias didáticas para ajudar a explicar a evolução do indicador e uma decisão no exercício.

**Limite da integração:** este painel é um módulo complementar ligado ao MVP pelo caso e pelo acesso à aplicação. Ele não lê o estado de uma tentativa real da API e não altera o resultado clínico do simulador. As curvas exponenciais e o cenário após oxigênio são hipóteses matemáticas, não medições de usuários ou pacientes nem reprodução das regras discretas do backend. A referência de 100% na integral serve apenas para comparar áreas, não é uma meta clínica.

## Modelo e dados usados

Variáveis: `t` é o tempo em minutos (`0 ≤ t ≤ 10` na análise); `S(t)` é a SpO₂ em %; `S'(t)` é a taxa de variação em pontos percentuais por minuto; `D(T)` é o déficit acumulado em pontos percentuais × minuto.

| Cenário | Função `S(t)` | Derivada `S'(t)` | Limite quando `t → ∞` |
| --- | --- | --- | ---: |
| Sem intervenção | `85 + 5e^(-t/6)` | `-(5/6)e^(-t/6)` | 85% |
| Após oxigênio | `97 - 7e^(-t/3)` | `(7/3)e^(-t/3)` | 97% |

Ambos partem de 90%. O limite descreve a tendência matemática se o tempo continuasse; a simulação do produto dura no máximo 10 minutos, então ele não é um desfecho observado.

Para analisar o **acúmulo**, integramos o déficit em relação a uma referência comum:

```text
D(T) = ∫[0,T] (100 - S(t)) dt

Sem intervenção: D(T) = 15T - 30(1 - e^(-T/6))
Após oxigênio:   D(T) =  3T + 21(1 - e^(-T/3))
```

Em `T = 10` minutos, o painel mostra a SpO₂ no instante, a derivada, o limite e o déficit acumulado dos dois cenários. A área menor após a intervenção representa menos déficit **dentro do modelo**. Os dados de entrada são os valores iniciais e críticos do caso do MVP mais parâmetros didáticos explícitos; não houve ajuste a observações clínicas ou a feedback de estudantes.

## Regra de decisão

O painel classifica o cenário selecionado no instante escolhido:

1. **Em atenção:** SpO₂ ≤ 85%, limite ≤ 85% ou derivada < −0,05 pp/min.
2. **Em evolução:** derivada > +0,05 pp/min e déficit acumulado menor que o cenário sem intervenção no mesmo intervalo.
3. **Estável / acompanhar:** demais situações.

Os limiares de derivada são convenções para a visualização didática, não critérios assistenciais. A regra combina tendência, taxa de mudança e acúmulo; sua implementação está em `simulator.py` e sua apresentação está em `app.py`.

## Como executar

Requisitos: Python 3.10 ou superior.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

No Windows, ative o ambiente com `.venv\Scripts\activate`. Abra o endereço local informado pelo Streamlit. O painel permite ajustar período, instante e cenário. Ele não exige credenciais ou chave de API.

Para verificar os cálculos e recriar o PDF:

```bash
python -m unittest -v
python generate_report.py
```

O arquivo gerado é `ENTREGA_DPS_SPRINT4.pdf`. O script usa somente as dependências de `requirements.txt` e os modelos deste repositório.

## Roteiro de apresentação

1. Abra o simulador pelo link do painel e identifique o caso e a SpO₂ inicial de 90%.
2. No painel, compare as duas curvas até 10 minutos. Explique os limites e o sinal das derivadas.
3. Compare as áreas acumuladas `D(10)` e sua unidade `pp·min`.
4. Mostre a classificação de cada cenário e explique a regra.
5. Descreva a limitação: curvas didáticas não são dados clínicos observados e não comandam o backend.

## Arquivos da entrega

| Arquivo | Conteúdo |
| --- | --- |
| `ENTREGA_DPS_SPRINT4.pdf` | Apresentação única para submissão, com equipe, gráficos, cálculos e análise crítica |
| `app.py` | Painel interativo |
| `sample_cases.py` | Curvas e integrais analíticas |
| `simulator.py` | Derivada numérica e regra de decisão |
| `test_simulator.py` | Testes dos modelos, integral e classificação |
| `generate_report.py` | Reprodução do PDF |
| `INTEGRANTES.txt` | Nomes e RMs da equipe |
