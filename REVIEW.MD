```python
# Main function to run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Le fait d'utiliser 0.0.0.0 est une faille de sécurité dans le sens ou n'importe qui peut accéder au server uvicorn

Via 127.x.... seul le poste local peut y accedé.

On peut également mettre l'ip d'un poste bien précis ou de l'ensemble d'un réseau via le masque.

```python
# Main function to run the app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```


