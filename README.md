# Painel Matemático — Crise Asmática

Dashboard interativo desenvolvido para a **Sprint 3 de Differentiated Problem
Solving** do Challenge FIAP + Hospital Moinhos de Vento.

A aplicação usa **limites e derivadas** para analisar a evolução didática da
saturação de oxigênio (SpO₂) de Carlos Mendes, paciente do caso de crise
asmática apresentado no MVP da equipe.

> Os modelos são exclusivamente educacionais. Não representam previsões
> clínicas e não substituem protocolos ou decisões de profissionais da saúde.

## Funcionalidades

- comparação entre piora sem oxigênio e recuperação com oxigênio;
- seleção do período e do instante analisado;
- gráfico interativo da SpO₂ ao longo do tempo;
- visualização da derivada em pontos percentuais por minuto;
- indicação do limite assintótico de cada cenário;
- interpretação automática da tendência e apoio à decisão no exercício.

## Modelo matemático

As variáveis utilizadas são:

- `t`: tempo transcorrido, em minutos, com `t ≥ 0`;
- `S(t)`: saturação de oxigênio no instante `t`, em porcentagem;
- `S'(t)`: taxa de variação da saturação, em pontos percentuais por minuto.

### Sem oxigênio

```text
S(t)  = 82 + 10e^(-t/6)
S'(t) = -(10/6)e^(-t/6)
lim S(t) = 82%, quando t → ∞
```

A derivada negativa indica queda da saturação. A curva começa em 92% e se
aproxima de 82%.

### Com oxigênio

```text
S(t)  = 98 - 6e^(-t/3)
S'(t) = 2e^(-t/3)
lim S(t) = 98%, quando t → ∞
```

A derivada positiva indica recuperação. A curva também começa em 92%, mas se
aproxima de 98%.

A função exponencial foi escolhida porque representa uma mudança mais intensa
no início que desacelera à medida que a variável se aproxima de um valor
estável. Os parâmetros não foram ajustados com dados clínicos reais.

## Relação com os critérios da Sprint 3

| Critério | Aplicação no projeto |
| --- | --- |
| Fenômeno analisado | Evolução da SpO₂ em uma crise asmática |
| Variáveis | Tempo, saturação e taxa de variação |
| Função matemática | Dois modelos exponenciais |
| Limite e derivada | Estabilização e velocidade da mudança |
| Significado | Piora, recuperação ou estabilização |
| Interface | Gráficos, métricas, linha de limite e ponto selecionado |
| Apoio à decisão | O sinal da derivada traduz a tendência do cenário |

## Como executar

Requisitos: Python 3.10 ou superior.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

No Windows, ative o ambiente com:

```powershell
.venv\Scripts\activate
```

Depois, acesse o endereço local exibido pelo Streamlit.

## Testes

```bash
python -m unittest -v
```

Os testes verificam os valores iniciais, a aproximação aos limites, o sinal das
derivadas, o cálculo na borda do domínio e a validação de entradas.

## Deploy

O projeto está pronto para serviços compatíveis com Streamlit. Configure:

- arquivo principal: `app.py`;
- dependências: `requirements.txt`;
- versão do Python: 3.10 ou superior.

## Estrutura

```text
.
├── app.py             # interface, gráficos e apoio à decisão
├── sample_cases.py    # modelos e configuração dos cenários
├── simulator.py       # derivada numérica e interpretação
├── test_simulator.py  # testes automatizados
├── requirements.txt   # dependências do deploy
└── README.md           # documentação da entrega
```

## Roteiro curto para apresentação

1. Abra **Sem oxigênio (piora)** e mostre a curva descendente.
2. Explique que a derivada negativa indica piora e que o limite é 82%.
3. Mude para **Com oxigênio (recuperação)**.
4. Mostre a derivada positiva e a aproximação ao limite de 98%.
5. Conclua: o limite indica a estabilização esperada e a derivada mostra a
   direção e a velocidade da mudança.

