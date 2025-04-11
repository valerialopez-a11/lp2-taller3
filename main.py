from flask import Flask, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt





# Buscar en ThingSpeak estaciones meteorológicas:
# https://thingspeak.mathworks.com/channels/public
# Ejemplos:
# https://thingspeak.mathworks.com/channels/1293177
# https://thingspeak.mathworks.com/channels/12397

URLs = [
  'https://thingspeak.mathworks.com/channels/1293177/feed.csv',
  'https://thingspeak.mathworks.com/channels/12397/feed.csv'
  
]
app = Flask(__name__)

def descargar(url):
  df = pd.read_csv(url)
  df['created_at'] = pd.to_datetime(df['created_at'])
  
  
  df.drop(['entry_id','field5', 'field6', "field8", "field7"], axis=1, inplace=True)
  df.columns = ['fecha', 'Temperatura C°', 'Humedad %', 'Pres. Atmosférica (hPa)', 'Gas']
  return df
    
def graficar(i,df):
  lista = []
  for columna in df.columns[1:]:
    fig= plt.figure(figsize=(8,5))
    plt.plot(df['fecha'], df[columna], label=columna)
    plt.title(f"Historico de {columna} - Estación # {i} ")
    
    plt.savefig(f'static/g{i}_{columna}.png')
    lista.append(f"g{i}_{columna}.png")
    plt.close()
  return lista

def actualizar():
  nombres = []
  for i,url in  enumerate(URLs):    
    df  = descargar(url)
    nombres.extend(graficar(i,df))
  return nombres
    
    
@app.route('/')
def index():
  return render_template('index.html', nombres = nombres)

# Programa Principal

@app.route('/actualizar')
def actualizar_datos():
  global nombres
  nombres = actualizar()
  return redirect('/')
if __name__ == '__main__':   
  # Ejecuta la app 
  nombres = actualizar()
  app.run(host='0.0.0.0', debug=True)
