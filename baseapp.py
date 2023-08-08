from flask import Flask, jsonify, request, render_template, Markup
app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

story = ""
pps = 14
current_paragraph = 0
paragraphs = []
fname = ""
namedict = {}
username = ""
def getParagraphs(username):
    global current_paragraph
    global pps
    f3 = open("pagewnames.txt", "r")
    newsession = False
    if(current_paragraph==0):
        newsession = True
    for line in f3:
        sp = line.split(" ")
        if(sp[0]==username):
            current_paragraph = int(sp[1])
            fname = sp[2].strip()
    f3.close()
    f = open(fname, "r")
    fname = fname + "\n"
    paragraphs = []
    for line in f:
        if(not line=="" and not line==" " and not line=="\n"):
            paragraphs.append(line)
    if(current_paragraph+pps<=len(paragraphs)):
        p = paragraphs[current_paragraph:current_paragraph+pps]
    else:
        p = paragraphs[current_paragraph:len(paragraphs)]
    alpha = "abcdefghijklmopqrstuvwxyz"
    okay = False
    for char in p[0]:
        if(char in alpha or char in alpha.upper()):
            okay=True
    if(not okay):
        p[0]=""
        p = p[1:len(p)]
        print("??")
    #print(p)
    chapter_names = ["ONE",
                    "TWO",
                    "THREE",
                    "FOUR",
                    "FIVE",
                    "SIX",
                    "SEVEN",
                    "EIGHT",
                    "NINE",
                    "TEN",
                    "ELEVEN",
                    "TWELVE",
                    "THIRTEEN",
                    "FOURTEEN",
                    "FIFTEEN"]
    for i in range(len(p)):
        p[i].replace("ï¿½", " - ")
        p[i].replace("�", " - ")
        #p[i].replace("\n\n", "\n")
        p[i].replace("\u00ef", " ")
        p[i].replace("\u00bf", "-")
        p[i].replace("\u00bd", " ")
        p[i].replace("\uFFFD", " - ")
        p[i].replace("\u2014", "&nbsp;")
        if(p[i].strip() in chapter_names):
            p[i] = Markup("<span id='chapter_title'>" + p[i].strip()[0] + p[i].strip()[1:].lower() + "</span>")
    current_paragraph+=pps
    lines = []
    myfile1 = open("pagewnames.txt", "r")
    for line in myfile1:
        lines.append(line)
    myfile = open("pagewnames.txt", "w")
    for line in lines:
        if(not(line=="\n") and not(line.split(" ")[0]==username)):
            myfile.write(line.strip() + "\n")
    myfile.write(username + " " + str(current_paragraph) + " " + fname)
    return (p, current_paragraph, len(paragraphs), fname)

def backParagraphs(username):
    global current_paragraph
    global pps
    f3 = open("pagewnames.txt", "r")
    newsession = False
    if(current_paragraph==0):
        newsession = True
    for line in f3:
        sp = line.split(" ")
        if(sp[0]==username):
            current_paragraph = int(sp[1])
            fname = sp[2].strip()
    f3.close()
    f = open(fname, "r")
    fname = fname + "\n"
    paragraphs = []
    for line in f:
        if(not line=="" and not line==" " and not line=="\n"):
            paragraphs.append(line)
    if(not(current_paragraph<=pps)):
       current_paragraph = current_paragraph - pps - pps
    if(current_paragraph+pps<=len(paragraphs)):
        p = paragraphs[current_paragraph:current_paragraph+pps]
    else:
        p = paragraphs[current_paragraph:len(paragraphs)]
    alpha = "abcdefghijklmopqrstuvwxyz"
    okay = False
    for char in p[0]:
        if(char in alpha or char in alpha.upper()):
            okay=True
    if(not okay):
        p[0]=""
        p = p[1:len(p)]
        print("??")
    print(p[0])
    chapter_names = ["ONE",
                    "TWO",
                    "THREE",
                    "FOUR",
                    "FIVE ",
                    "SIX",
                    "SEVEN",
                    "EIGHT",
                    "NINE",
                    "TEN",
                    "ELEVEN",
                    "TWELVE",
                    "THIRTEEN",
                    "FOURTEEN",
                    "FIFTEEN"]
    for i in range(len(p)):
        p[i].replace("ï¿½", " - ")
        p[i].replace("�", " - ")
        #p[i].replace("\n\n", "\n")
        p[i].replace("\u00ef", " ")
        p[i].replace("\u00bf", "-")
        p[i].replace("\u00bd", " ")
        p[i].replace("\uFFFD", " - ")
        if(p[i].strip() in chapter_names):
            p[i] = Markup("<span id='chapter_title'>" + p[i].strip()[0] + p[i].strip()[1:].lower() + "</span>")
    current_paragraph+=pps
    lines = []
    myfile1 = open("pagewnames.txt", "r")
    for line in myfile1:
        lines.append(line)
    myfile = open("pagewnames.txt", "w")
    for line in lines:
        if(not(line=="\n") and not(line.split(" ")[0]==username)):
            myfile.write(line.strip() + "\n")
    myfile.write(username + " " + str(current_paragraph) + " " + fname)
    return (p, current_paragraph, len(paragraphs), fname)

@app.route('/next/', methods=['GET', 'POST'])
def next():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        js = request.get_json()
        global current_paragraph
        global pps
        current_paragraph = js["current_paragraph"]
        pps = js["pps"]
        return 'OK', 200

    # GET request
    else:
        p = getParagraphs(username)
        pars = p[0]
        global paragraphs
        message = {'paragraphs':pars}
        p1 = int(p[1]/pps) + 1
        p2 = int(p[2]/pps) + 1
        pct1 = int(p1/p2 *1000)
        pct1 = pct1/10
        return render_template('index.html', paragraphs=pars, parnum = p1, pn2 = p2, pct=pct1, user=username, infile=p[3], heading="You're reading: ")

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST': 
        name = request.form.get("name1")
        global username
        username = name 
        f = request.files['file']
        f.save(f.filename) 
        fname = f.filename
        f = open(fname, "r")
        for line in f:
            if(not line=="" and not line==" " and not line=="\n"):
                paragraphs.append(line)
        subp = paragraphs[0:pps]
        current_paragraph = pps
        lines = []
        myfile1 = open("pagewnames.txt", "r")
        for line in myfile1:
            lines.append(line)
        myfile = open("pagewnames.txt", "w")
        for line in lines:
            if(not(line=="\n")):
                myfile.write(line.strip() + "\n")
        myfile.write("\n" + username + " 0 " + fname)
        p1 = 1
        p2 = int(len(paragraphs)/pps) + 1
        pct1 = int(p1/p2 *1000)
        pct1 = pct1/10
        return render_template('index.html', paragraphs=subp, parnum = p1, pn2 = p2, pct=pct1, user=username, infile=fname, heading="You're reading: ")
    
@app.route('/returner', methods=['POST'])
def returner():
    name = request.form.get("name2")
    global username
    username=name
    p = getParagraphs(username)
    print(p)
    pars = p[0]
    global paragraphs
    message = {'paragraphs':pars}
    p1 = int(p[1]/pps) + 1
    p2 = int(p[2]/pps) + 1
    pct1 = int(p1/p2 *1000)
    pct1 = pct1/10
    return render_template('index.html', paragraphs=pars, parnum = p1, pn2 = p2, pct=pct1, user=username, infile=p[3], heading="You're reading: ")  

@app.route('/back', methods=['GET', 'POST'])
def back():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        js = request.get_json()
        global current_paragraph
        global pps
        current_paragraph = js["current_paragraph"]
        pps = js["pps"]
        return 'OK', 200

    # GET request
    else:
        p = backParagraphs(username)
        pars = p[0]
        message = {'paragraphs':pars}
        global paragraphs
        #test_page()
        #return jsonify(message)  # serialize and use JSON headers
        #global pps
        p1 = int(p[1]/pps) + 1
        p2 = int(len(paragraphs)/pps) + 1
        pct1 = int(p1/p2 *1000)
        pct1 = pct1/10
        return render_template('index.html', paragraphs=pars, parnum = p1, pn2 = p2, pct=pct1, user=username, infile=p[3], heading="You're reading: ")

@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')

@app.route('/start')
def start():
    fnames = open("pagewnames.txt", "r")
    n = []
    for line in fnames:
        parts = line.split(" ")
        n.append(parts[0])
        namedict[parts[0]] = int(parts[1])
    return render_template('start.html', names=n, heading="Upload or Login to get started!")

@app.route('/upload/<name>')
def upload():
    return render_template('upload.html', name=request.args.get('name'))