from flask import Flask,request,session,render_template,json,redirect,url_for
from graph import Graph

app = Flask(__name__)

distance = 0.0
result = {}

@app.route('/index',methods=['GET', 'POST'])
def index():
    global distance
    global result
    if request.method == 'POST':
        asd = request.json
        print(asd)
        edges = asd['edges']
        geocodes = asd['geocodes']
        points = asd['src_dest']
        vertices = len(geocodes)
        keys = []
        keywords = geocodes.keys()
        for key in keywords:
            keys.append(int(key))
        print(keys)
        
        graph = Graph(vertices,keys)
        for edge in edges:
            graph.addEdge(edge['edge'][0],edge['edge'][1],edge['weight'])
        graph.printGraph()
        graph.shortestPath(points[0],points[1])
        print("Path is: ",graph.path)
        distance=round(graph.distance,2)

        result = {'path':graph.path,'distance':round(graph.distance,2),'geocodes':geocodes,"src_dest":points}
        print(result)
        distance = round(graph.distance,2)

        return json.dumps({'success': True,'path':graph.path,'distance':round(graph.distance,2),'geocodes':geocodes,"src_dest":points}), 200, {'ContentType': 'application/json'}
    
    return render_template('index.html')

@app.route('/display',methods=['GET', 'POST'])
def display():

    return render_template('display.html',result=result)

@app.route('/result',methods=['GET', 'POST'])
def result():
    return "result page"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)