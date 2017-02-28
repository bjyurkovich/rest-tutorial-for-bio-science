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