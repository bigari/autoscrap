from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
import pprint
from tree import *


def fetch(url):
    session = HTMLSession()
    r = session.get(url)
    return r.html.raw_html


def soupify(html):
    soup = BeautifulSoup(html, features="lxml")
    return soup


def compact(soup):
    buyNode = None
    key = 0
    queue = []
    current = soup.find('body')
   # current['id'] = 'id-' + str(key)
    head = Node(key, current.name)
    key += 1
    candidates = {
        'price': [],
        'name': [],
        'description': [],
        'image': [],
        }
    queue.append([head, current.children])  # Children is an iterator which is cool
    buyRegex = '(buy|cart|achète|acheter|ajouter|panier|add)'


    while queue:
        (parent, it) = queue.pop()
        data = ''
        kind = ''
        isBuyNow = False
        for elmt in it:
            insertable = True
            if not elmt.name or elmt.name == 'script':
                continue
            if elmt.string:
                data = elmt.string
                if re.search(buyRegex,
                    elmt.string.lower()) and len(elmt.string) < 17:
                    isBuyNow = True
                    print(elmt)
                elif re.search('\d+(,\d{3})*(\.\d+)? Dhs$', elmt.string):
                    kind = 'price'
                elif re.search('(,|.)', elmt.string):
                    kind = 'description'
                else:
                    kind = 'name'
               

            elif elmt.name == 'img':

                kind = 'image'
                data = elmt['src']
            elif elmt.name == 'input' and elmt.get('type', '') \
                == 'submit' and re.search(buyRegex, elmt.get('value', ''
                    )):

                isBuyNow = True
            else:
                insertable = False
                for child in elmt.children:
                    if not child.name or child.string or child.name == 'img':
                        insertable = True
                        break

            if isBuyNow or insertable:
                current = Node(key, elmt.name, data=data, parent=parent)
                parent.children.append(current)
                if kind != '':
                    candidates[kind].append(current)
                if elmt.children:
                    queue.append([current, elmt.children])
                if isBuyNow:
                    buyNode = current
                    
            else:
                if elmt.children:
                    queue.append([parent, elmt.children])

               # that's where we remove useless divs

            key += 1

         # check if btn is buy btn

    return [buyNode, candidates]


def extract(buyNode, candidates):
    feat = {}
    for (k, nodes) in candidates.items():
        if not nodes:
            continue
        print(k)
        bestdist = 2000000000
        bestnode = nodes[0]
        for node in nodes:
            d = distance(node, buyNode)
            if d < bestdist:
                bestdist = d
                bestnode = node

        feat[k] = bestnode.data

    return feat


def main():

    url = \
        'https://www.jumia.ma/universal-tempered-glass-clear-full-hd-screen-protector-cover-protective-film-guard-for-sony-playstation-psvita-ps-vita-psv-1000-console-28880528.html'

   # url = input()

    (buyNode, candidates) = compact(soupify(fetch(url)))
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(extract(buyNode, candidates))


main()
