# ⚫⚪ Reversi

![CI](https://github.com/kondej/reversi/actions/workflows/ci.yml/badge.svg)

<p style="text-align:center">
  <img src="https://i.postimg.cc/5tvJB5W2/reversi.png" alt="Reversi" style="width:70%; height:auto;">
</p>

## 🔧 Wymagania
- Zainstalowane biblioteki:
  - **flask**
  - **flask-cors**

## ▶️ Uruchamianie gry

- Uruchamiamy **main.py** w terminalu za pomocą polecenia:

```python main.py```

## 🐳 Użycie Dockera

1. Pobranie z Docker Hub

Obraz gry jest dostępny publicznie na Docker Hub:

```
docker pull kondej/reversi-game
docker run -p 5000:5000 reversi/snake-game
```

2. Budowanie lokalnego obrazu

Możesz też zbudować obraz Dockera lokalnie:

```
docker build -t reversi-game .
docker run -p 5000:5000 reversi-game
```

Aplikacja będzie dostępna pod adresem: `http://localhost:5000`

🌐 Wersja online

Gra jest dostępna również online dzięki użyciu platformy Railway:

- https://reversi-game-production.up.railway.app/

## 🛠️ CI/CD – GitHub Actions

W repozytorium znajduje się pipeline CI/CD oparty na GitHub Actions:

- Uruchamiany automatycznie przy `push` i `pull_request` na gałąź `main`
- Wykonuje:
  - instalację zależności (`pip install -r requirements.txt`)
  - testy jednostkowe (`pytest`)
  - budowanie obrazu Dockera (`docker build`)