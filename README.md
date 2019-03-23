# DAPASA
We detect Android piggybacked apps by utilizing the distinguishable invocation patterns of sensitive APIs between the rider and carrier.

# Dependancies

    • Apktool
    • Networkx
    • Matplotlib
    • Numpy
    • Pandas
    • Scikit-learn
      
# Running 
	This program can be started by running main.py and passing the file name(if in the current directory) or the relative path of the android app as command-line argument.
	
	python main.py sample.apk

# Working
    • It first disassemble the app using apktool.
    • Then parses all the small files and make a directed-call-graph of functions in the app, where an edge originate from callee method and point to call method.
    • Then based on sensitive api list, the call graph is divided into mutually exclusive(sensitive-api) subgraph, each consisting of sensitive api(s) and neighbouring node withing depth ofmore than level-3
    • The subgraph with highest sensitive score(pre calculated from the Dataset) is selected and some features are selected from it.
    • At last the Random forest classification algorithm is used for building the predicting model.
