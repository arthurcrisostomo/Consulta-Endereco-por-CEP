# Buscador de CEP

Aplicação desktop em Python (Tkinter + Selenium) que lê um arquivo .txt
com CEPs, consulta o endereço de cada um em buscacep.com.br e exibe os
resultados em uma tabela. O histórico é salvo em `~/historico.txt`.

## Como usar
1. Baixe o `.exe` na aba **Releases**.
2. Clique em "Selecionar Arquivo" e escolha um .txt com um CEP por linha.
3. Clique em "Iniciar".

> Requer o Google Chrome instalado.

## Rodando pelo código
    pip install -r requirements.txt
    python main.py