from flask import Blueprint, request, jsonify, render_template, redirect,session
from ..models import ContentIdea, ShortenedLink, ProductFeedback, db,Product
from app.routes import features_bp
import random
from bs4 import BeautifulSoup
import requests
from openai import AzureOpenAI
import os 
import uuid

client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version="2024-07-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def chat(system, user):
    chat_completion = client.chat.completions.create(
        model="gpt-4o",  # Nome do deployment configurado no Azure
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )

    assistant_response = chat_completion.choices[0].message.content

    return assistant_response



# Rota para gerar ideias de conteúdo
@features_bp.route("/api/generate-ideas", methods=["POST"])
def generateIdeas():
    data = request.get_json()
    nome_produto = data['nome']
    preco = data['preco']
    descricao = data["descricao"]
    url = data['url']

    # Pegar analise geral 
    analiseGeral = chat(
        system="Você é uma inteligência artificial, que auxilia afiliados da Shopee, você irá gerar uma análise geral do produto com base nas informações do usuário, você fornecerá informações para ajudar o afiliado a ter mais vendas.",
        user=f"Nome do produto: {nome_produto}. Descrição do produto: {descricao}. Preço do produto: {preco}."
    )
    
    publicoAlvo = chat(
        system="Você é uma inteligência artificial, que auxilia afiliados da Shopee, você deve fornecer sugestões de público alvo com base na análise geral de um produto.",
        user=f"Análise Geral: {analiseGeral}"
    )

    videos = chat(
        system="Você é uma inteligência artificial que auxilia afiliados da Shopee, você deverá gerar legendas para vídeos nas redes sociais para promover produtos,"+
        "as legendas devem ser diferenciadas, que abordem dores do público alvo que será fornecido pelo usuário. Exemplo:"+
        "'Nunca mais vou precisar ir até a cozinha para fazer pipoca' sempre de forma bem descontraída. Gere 10 ideias de legenda(separadas por \\) com base nas informações fornecidas pelo usuário.",
        user=f"Nome do produto: {nome_produto}. Análise Geral: {analiseGeral}. Público Alvo: {publicoAlvo}"
    )


    new_product = Product(
        id=str(uuid.uuid4()),
        user=session["user"],
        title=nome_produto,
        description=descricao,
        price=float(preco),
        analise=analiseGeral,
        publico=publicoAlvo,
        ideias_videos=videos,
        url= url
        urlEncurtado=""
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "msg": "success",
        "id": new_product.id
    })

@features_bp.route("/api/update-product/<id>", methods=["POST"])
def updateProduct(id):
    data = request.get_json()

        # Validação básica dos dados
    if not data or "info" not in data or "newInfo" not in data:
        return jsonify({"msg": "Invalid data"}), 400

    info = data["info"]
    newInfo = data["newInfo"]

    # Busca pelo produto
    product = Product.query.filter_by(id=id).first()
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    # Atualização do atributo de forma dinâmica
    setattr(product, info, newInfo)

    # Tentativa de salvar no banco
    db.session.commit()

    return jsonify({"msg": "success"}), 200
                                                
@features_bp.route("/remove-product/<id>")
def removeProduct(id):
    user = session["user"]
    product = Product.query.filter_by(id=id).first()
    if user == product.user:
        db.session.delete(product)
        db.session.commit()
        return redirect("/")