import json
import os

from flask import Flask, redirect, render_template, request

app = Flask(__name__)
ARQUIVO = "contatos.json"


def carregar():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, encoding="utf-8") as f:
        return json.load(f)


def salvar(contatos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(contatos, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    busca = request.args.get("busca", "").strip()
    contatos = carregar()
    if busca:
        contatos = [c for c in contatos if busca.lower() in c["nome"].lower()]
    return render_template("index.html", contatos=contatos, busca=busca)


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    contatos = carregar()
    contatos.append({
        "nome": request.form["nome"],
        "telefone": request.form["telefone"],
    })
    salvar(contatos)
    return redirect("/")
