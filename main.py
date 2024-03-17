import discord
from discord import SyncWebhook
from flask import Flask, request, jsonify
import requests
import urllib.parse
import json

app = Flask(__name__)

# Claves pre-generadas
keys = [
    "Further_ABCDEFGHIJ",
    "Further_KLMNOPQRST",
    "Further_UVWXYZ1234",
    "Further_567890abcd",
    "Further_efghijklmn",
    "Further_opqrstuvwx",
    "Further_yzABCDE567",
    "Further_FGHIJKLMNO",
    "Further_PQRSTU3456",
    "Further_VWXYZ7890",
    "Further_1234abcdEF",
    "Further_GHIJKLMOPQ",
    "Further_RSTUVWXYZ12",
    "Further_34567890ab",
    "Further_cdefghijklm",
    "Further_nopqrstuvw",
    "Further_xyzABCDE34",
    "Further_567890FGHI",
    "Further_JKLMNOPQRS",
    "Further_TUVWXYZ890"
]

# Endpoint para realizar el bypass
@app.route('/api/bypass', methods=['GET'])
def bypass():
    # Obtener la clave del parámetro 'key' en el query string
    key = request.args.get('key', '')

    # Verificar si la clave es válida
    if key not in keys:
        return jsonify({'error': 'Clave inválida'}), 401

    # Obtener la URL codificada del parámetro 'url' en el query string
    encoded_url = request.args.get('url', '')
    decoded_url = urllib.parse.unquote(encoded_url)

    # Hacer un request a la API externa para obtener la URL del bypass
    response = requests.get("https://dlr-api-w.vercel.app")
    if response.status_code == 200:
        data = response.json()
        api_url = data.get('api_url', '')
    else:
        return jsonify({'error': 'No se pudo obtener la API URL'}), 500

    # Construir la URL final para hacer el segundo request
    final_url = f"{api_url}/api/bypass?url={encoded_url}"

    # Hacer el segundo request con el header 'Bearer'
    headers = {'Authorization': 'Bearer Delorean_T90151130355702199092780928792828907U'}
    second_response = requests.get(final_url, headers=headers)

    # Crear el embed para enviar a Discord
    

    owner = request.remote_addr
    responsen = second_response.json().get('result', 'No result')

    embed = discord.Embed(
        title="API Request",
        color=discord.Color.green()
    )
    embed.add_field(name="Ip", value=owner)
    embed.add_field(name="Requested Url", value=decoded_url)
    embed.add_field(name="Response", value=responsen)

    # Enviar el embed a Discord
    webhook_url = "https://discord.com/api/webhooks/1218850890308521994/75cJsf0aMeg96zioXTnZIynPhIbB3VWcUN-N4DQzREXbEm_9z03vFZbn4ijNJgMYaRCd"
    webhook = SyncWebhook.from_url(webhook_url) # Initializing webhook
    webhook.send(embed=embed)

    return jsonify(second_response.json().get('result', 'No result'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
