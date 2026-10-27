# Monitor de Mobilidade Urbana em Tempo Real

Projeto full-stack serverless de monitoramento de trânsito urbano integrando a **Overpass API (OpenStreetMap)**, mapa interativo em Leaflet e assistente conversacional local (Suporte aos Dados) para execução na **Vercel**.

## Estrutura do Projeto

```
.
├── api/
│   └── index.py        # Serverless Function Python (Backend)
├── public/
│   └── index.html      # Frontend HTML5 + Leaflet.js + IA Local
├── vercel.json         # Rotas e configurações Vercel
├── requirements.txt    # Dependências do Python
└── README.md
```

## Como Fazer o Deploy na Vercel

1. Instale a Vercel CLI no terminal:
   ```bash
   npm install -g vercel
   ```

2. Faça o deploy direto executando:
   ```bash
   vercel
   ```
