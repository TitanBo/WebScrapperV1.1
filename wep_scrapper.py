import time
import requests

from decimal import Decimal
from bs4 import BeautifulSoup

sleepTime = int(input("how long shell be the break in seconds???"))
brakePoint = int(input("how often we shell loop???"))
i = int(0)
loopNr = 0

for i in range(0, brakePoint):
    # DB// url + request -> url
    url = "https://www.finanzen.net/index/dax"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # find Index 2 <tbody> -> doc
    allTbody = doc.find_all("tbody")[2]
    # find Index 1 <td> -> tbody
    tdFour = allTbody.find_all("td")[1]
    # find <span> in tdFour
    spanOne = tdFour.find("span")
    # find Index 5 <td> -> tbody
    tdFive = allTbody.find_all("td")[5]
    # <td> parse just string
    fullNumberStr = str(tdFive.string)
    currentNumberStr = str(spanOne.string)
    # delete all '.' and turn ',' into '.'
    fNWithoutK = fullNumberStr.replace(".", "")
    fNwithPoint = fNWithoutK.replace(",", ".")
    currentWithoutK = currentNumberStr.replace(".", "")
    currentNumberwithPoint = currentWithoutK.replace(",", ".")
    # ============================== First Number ===================================== #
    # <start today>
    firstDayStart = Decimal(fNwithPoint[13:-22])
    # ============================== Second Number ===================================== #
    # <stop last day>
    endLastDay = Decimal(fNwithPoint[24:-11])
    # ============================== Current Value ===================================== #
    # <current Value>
    currentNumber = Decimal(currentNumberwithPoint)
    loopNr = loopNr + 1
    # output
    print("loop: " + f"\033[32;1m{loopNr}\033[0m")
    print(f"\033[33;1m{sleepTime}\033[0m" + " sec break\n")
    print("DAX Day Start : " + f"\033[31;1m{firstDayStart}\033[0m" + " PKT\n")
    print("DAX End Last Day : " + f"\033[31;1m{endLastDay}\033[0m" + " PKT\n")
    if currentNumber < 13340.00:
        print("DAX Current Value : " + f"\033[32;1m{currentNumber}\033[0m" + " PKT\n")
    else:
        print("DAX Current Value : " + f"\033[31;1m{currentNumber}\033[0m" + " PKT\n")

    # brakepoint
    time.sleep(int(sleepTime))
print("Done \033[31;1m!\033[0m\033[33;1m!\033[0m\033[32;1m!\033[0m")

# quellen https://www.delftstack.com/de/howto/python/extract-substring-from-a-string-in-python/
# quellen https://www.youtube.com/watch?v=gRLHr664tXA&t=811s

# https://www.finanzen.net/index/dax/historisch
