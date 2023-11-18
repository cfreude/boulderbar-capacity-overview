from flask import Flask
from flask import render_template_string

from urllib.request import urlopen

start_urls = [
    ('Hannovergasse', 'https://shop.boulderbar.net:8080/modules/bbext/CustomerCapacity.php?gym=han'),
    ('Wienerberg', 'https://shop.boulderbar.net:8080/modules/bbext/CustomerCapacity.php?gym=wb'),
    ('Hauptbahnhof', 'https://shop.boulderbar.net:8080/modules/bbext/CustomerCapacity.php?gym=hbf'),
    ('Seestadt', 'https://shop.boulderbar.net:8080/modules/bbext/CustomerCapacity.php?gym=see'),
]

app = Flask(__name__)

html_template = '''
<!DOCTYPE html>
     <head>
        <style>
        html {
        width: 100%;
        min-width: 0%;        
        max-width: 100%;
        }
        body {
        width: 100%;
        min-width: 0%;  
        }
        div {
        width: 100%;
        min-width: 0%;   
        }
        table {
        width: 100%;
        min-width: 0%; 
        }        
        </style>
     </head> 
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">    
     <body>
         {{ data | safe }}
     </body>
 </html>
'''
#<div class="w3-bar-item" style='background-color:{color}; width:{percent}%'>{percent}%</div>
    
bar = lambda name, percent, color: f'''
    <tr>
    <td style='width:0%'>{name}:</td>
    <td>
    <div class="w3-bar w3-green" style='width:{percent}%'>
    <div class="w3-bar-item">{percent}%</div>
    </div>    
    </td>
    </tr>
    '''


@app.route('/')
def hello_world():

    caps = []

    for name, url in start_urls:
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        cap_index = html.find('capacity_bar')
        h2_index = html.find('<h2>', cap_index)
        h2_end = html.find('</h2>', h2_index+4)
        percent = html[h2_index+4:h2_end-1]
        #print(percent)
        caps.append((name, percent))
        
    bars = '\n'.join([bar(n, p, 'green') for n, p in caps])

    body = f'<table>{bars}</table>'
    
    return render_template_string(html_template, data=body)