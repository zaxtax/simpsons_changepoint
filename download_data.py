import pandas as pd
import csv
from lxml import html


def pretty_episode(x):
    return "S{}E{}".format(*x.split("."))


url = "http://www.imdb.com/title/tt0096697/epdate"
xpath = "//*[@id=\"tn15content\"]/table[1]"

tree = html.parse(url)
table = tree.xpath(xpath)[0]
raw_html = html.tostring(table)

data = pd.read_html(raw_html,
                    converters={"#": pretty_episode},
                    header=0)[0]

# Clean up
del data["Unnamed: 4"]
data.rename(columns={'#': 'EpisodeID'}, inplace=True)

data.to_csv("simpsons_ratings.csv",
            index=False,
            quoting=csv.QUOTE_NONNUMERIC)
