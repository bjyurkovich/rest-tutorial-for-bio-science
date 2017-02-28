# Accessing Webservices Tutorial for Bio Scientists
A starter tutorial for bio scientists and engineers wanting to access data sources in an automated fashion using web services.

## Introduction
One of the most frustrating things about domain specific research is adopting and developing your concepts leveraging existing tools and datasets.  This tutorial aims to give a general straight-forward tutorial by automating the access of a 3rd party REST API (BiGG).

This tutorial assumes you have a general understanding of programming - primarily in the python programming language.  
It is suggested that you do this tutorial on a linux or OSX (all commands will assume this platform in this tutorial).

### General Concepts Covered in this Tutorial
If you are not familiar with the following concepts, it is highly suggested you take a few minutes a research them to get a general understanding:

1. Python programming language (we will be using python 2.7)
2. REST (Representational State Transfer) - [Wikipedia](https://en.wikipedia.org/wiki/Representational_state_transfer)


## Getting Started

Make sure you create a folder for the work that will do:

```bash
mkdir web-service-bio-tutorial
cd web-service-bio-tutorial
```

To organize our dependencies, you will need set up our `python` environment.  We will use [virtual environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/).  Virtual environments allow us to create a development sandbox for all our project dependencies.

```bash
pip install virtualenv
virtualenv venv
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
```

You may notice now that there is a `(venv)` marker at the beginning of your terminal line.  This means it worked!

Now that we are running in our virtual environment (our sandbox), we need to install a dependency:

> [Requests](http://docs.python-requests.org/en/master/) - a nice HTTP library that will help us access the BiGG API

To install the dependency, we will run:

```bash
pip install requests
```

If you have completed the tutorial this far, it means you are ready to start coding!

## Accessing the BiGG API
While it may be easy to access information on models, reactions, metabolites, and genes by simply using the frontend search engine of [BiGG](bigg.ucsd.edu), the researchers and students and UCSD have also provided us a RESTful webservice to access the data in the BiGG database in an automated fashion.

The information on how to access BiGG via its API can be [found here](http://bigg.ucsd.edu/data_access).  You will notice that they provide `curl` examples.  While it is possible to make system calls through python using `curl`, there is a much cleaner way:  using `requests` library to access data directly.

### First lines of code
Let's begin by creating our `main.py` file:

```bash
touch main.py
```

Opening `main.py` in our favorite text editor or IDE, we will begin by importing `requests`:
```python
# main.py
import requests
```

### Looking at the API Docs First
Now that we have `requests` imported, we can use that to access a specific `HTTP` route provided by BiGG data access API.  From the BiGG Documentation, we know we can use `curl` to access the database version:

`curl 'http://bigg.ucsd.edu/api/v2/database_version'`

and we expect a response to be of the form:

```json
{
    "bigg_models_version": "1.1.0",
    "api_version": "v2",
    "last_updated": "2016-03-21 17:24:11.138365"
}
```

We see that this is a `JSON` based API ([see more about JSON here](json.org)), so we know we can use python dictionaries to represent this data. 

### Doing it in Python
So let's get the info we need in `main.py`:

```python
import requests

res = requests.get("http://bigg.ucsd.edu/api/v2/database_version")
print "HTTP Response Code: ", res.status_code
bigg_info = res.json()
print "BiGG Model Version: ", bigg_info["bigg_models_version"]

```

Our first line `res = requests.get("...")` does an RESTful (HTTP) webservice call to `GET` the information we want (in this case, the model version number).  

The second call `print ... , res.status_code` simply verifies that the call was successful.  You should see a `200` status code.  More on `HTTP` status codes [here](https://httpstatusdogs.com/). 

The third line (`bigg_info = res.json()`) is the most important line.  Here we take the response object from our HTTP request, grab the payload (in this case, the model version and other things), convert that payload from `JSON` to a python dictionary, and assigns it our variable `bigg_info`.

The fourth line simply prints the `bigg_models_version`. 

Awesome!  He have our first RESTful access of the BiGG API (and it only took 5 lines of code)!

### Getting more useful information from BiGG in Python
OK, so we got some basic information, but what if we wanted to get information about a specific reaction such as Adenosine deaminase?  Let's go to the BiGG docs:

Looks like there is a general reaction access route: `curl 'http://bigg.ucsd.edu/api/v2/universal/reactions/ADA'`.  Let's use that.  Notice the print statements removed from getting the `bigg_info`.



```python
import requests

# Get BiGG database info
res = requests.get("http://bigg.ucsd.edu/api/v2/database_version")
bigg_info = res.json()


# Get ADA reaction from BiGG
res_reaction = requests.get("http://bigg.ucsd.edu/api/v2/universal/reactions/ADA")
ada_reaction_info = res_reaction.json()
metabolite_bigg_id = ada_reaction_info["metabolites"][0]["bigg_id"]

## Get a lot of information about all metabolites assocatiated with an ADA reaction
for metabolite in ada_reaction_info["metabolites"]:
    met_url = "http://bigg.ucsd.edu/api/v2/universal/metabolites/{0}".format(metabolite["bigg_id"])
    res_met = requests.get(met_url)
    met = res_met.json()
    print met["name"], met["formulae"][0]

```

You will notice that we first got the `Adenosine deaminase` reaction, and then from that, we looped through, each time requesting more general information about the metabolite based on its `bigg_id`.  In this tutorial, we simply printed the name of the metabolite and the first formula associated with it.  However, in your application, with a little knowledge of python, you can use that information and combine it.


## Finishing up
In this brief (and very basic) tutorial, we showed you how to access a database (BiGG) full of biological information.  You can use this as a starter to add the ability to automate the harvesting of information for your python projects and research.

If you felt like it was too much work to copy and paste the few lines of python code above into your own python environment, don't worry you can always clone this repo with the python file in it and run in a terminal:

```bash
#Clone repo and cd into the cloned folder
git clone https://github.com/bjyurkovich/rest-tutorial-for-bio-science.git
cd https://github.com/bjyurkovich/rest-tutorial-for-bio-science.git

#Set up your env and install requests dependency
pip install virtualenv
virtualenv venv
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
pip install -r requirements.txt

#run it!
python main.py
```

Head over to the Escher Interactive tutorial to see an example of how BiGG API is used in conjunction with KeGG, PDB, and Chebi!

