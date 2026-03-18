from flask import Flask, render_template_string, request
import pandas as pd
from IA.Algorithme import recommander

app = Flask(__name__)

data = pd.read_csv("DATA/Achats.csv")
produits = sorted(data["product"].unique())

HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Système IA de recommandation</title>
    <style>
        body { background: #f2f2f2; font-family: Arial; }
        .container { width: 500px; margin: 40px auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }
        h1 { text-align: center; }
        label, select, button { display: block; margin: 15px 0; }
        ul { background: #f9f9f9; padding: 10px; border-radius: 4px; }
    </style>
</head>
<body>
<div class="container">
    <h1>Système de recommandation produits</h1>
    <form method="post">
        <label for="produit">Choisir un produit :</label>
        <select name="produit" id="produit">
            {% for p in produits %}
            <option value="{{p}}" {% if p==selected %}selected{% endif %}>{{p}}</option>
            {% endfor %}
        </select>
        <button type="submit">Obtenir recommandation</button>
    </form>
    <h2>Produits recommandés :</h2>
    <ul>
        {% if recommandations %}
            {% for r in recommandations %}
            <li>{{r}}</li>
            {% endfor %}
        {% else %}
            <li>Aucune recommandation trouvée</li>
        {% endif %}
    </ul>
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    selected = produits[0]
    recommandations = []
    if request.method == 'POST':
        selected = request.form.get('produit', produits[0])
        recommandations = recommander(selected)
    return render_template_string(HTML, produits=produits, recommandations=recommandations, selected=selected)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
