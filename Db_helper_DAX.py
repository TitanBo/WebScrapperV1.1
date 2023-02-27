import sqlite3
import time
import requests

from bs4 import BeautifulSoup
# get sleep time in sec. and the breakpoint of the loop
sleepTime = int(input("how long shell be the break in seconds???"))
breakPoint = int(input("how often we shell loop???"))
brakePointStr = str(breakPoint)
i = int(0)
loopNr = 0

# DB// connect to db
conn = sqlite3.connect('value.db')
# DB// Create a cursor
c = conn.cursor()

# DB// Create the Table
# c.execute("""CREATE TABLE IF NOT EXISTS mixedValues (
#         idRow integer PRIMARY KEY,
#         dayStart REAL,
#         endLastDay REAL,
#         currentValue REAL
#         )""")

# DB//Insert first DataPackage
# c.execute("INSERT INTO mixedValues VALUES (1, " + firstDayStart + ", " + endLastDay + ", " + currentNumber + ")")

for i in range(0, breakPoint):
    # url + request -> url
    url = "https://www.finanzen.net/index/dax"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # find Index 2 <tbody> -> doc
    allTbody = doc.find_all("tbody")[2]
    # find Index 1 <td> -> tbody
    tdOne = allTbody.find_all("td")[1]
    # find <span> in tdFour
    spanOne = tdOne.find(".snapshot .snapshot--2nd-values .snapshot--big-values .snapshot--show-values > span")
    # find Index 5 <td> -> tbody
    tdFive = allTbody.find_all("td")[5]
    # find Index 7 <td> -> tbody
    tdSeven = allTbody.find_all("td")[7]
    # <td> parse just string
    firstFullNumberStr = str(tdFive.string)
    secondFullNumberStr = str(tdSeven.string)
    # <span> parse just string
    currentNumberStr = str(spanOne.string)
    # delete '.' and turn ',' into '.'
    fNWithoutK = firstFullNumberStr.replace(".", "")
    fNwithPoint = fNWithoutK.replace(",", ".")
    sNWithoutK = secondFullNumberStr.replace(".", "")
    sNwithPoint = sNWithoutK.replace(",", ".")
    currentWithoutK = currentNumberStr.replace(".", "")
    currentNumberwithPoint = currentWithoutK.replace(",", ".")
    # ============================== First Number ===================================== #
    # <start today>
    firstDayStart = str(fNwithPoint[13:-23])
    # ============================== Second Number ===================================== #
    # <stop last day>
    endLastDay = str(fNwithPoint[24:-12])
    # ============================== Third Number ===================================== #
    # <highest current value>
    currentHigh = str(sNwithPoint[13:-23])
    # ============================== Fourth Number ===================================== #
    # <lowest current value>
    currentDown = str(sNwithPoint[24:-12])
    # ============================== Current Value ===================================== #
    # <current Value>
    currentNumber = str(currentNumberwithPoint)
    loopNr = loopNr + 1
    # output
    print("loop: " + f"\033[32;1m{loopNr}\033[0m" + " / " + f"\033[32;1m{brakePointStr}\033[0m")
    print(f"\033[33;1m{sleepTime}\033[0m" + " sec break\n")
    print("DAX Day Start : " + f"\033[31;1m{firstDayStart}\033[0m" + " PKT")
    print("DAX End Last Day : " + f"\033[31;1m{endLastDay}\033[0m" + " PKT")
    print("DAX current High Day Value : " + f"\033[31;1m{currentHigh}\033[0m" + " PKT")
    print("DAX current Down Day Value : " + f"\033[31;1m{currentDown}\033[0m" + " PKT")
    print("DAX Current Value : " + f"\033[32;1m{currentNumber}\033[0m" + " PKT\n")
    # DB// write Data
    c.execute("UPDATE mixedValues SET dayStart = " + firstDayStart + " WHERE idRow = 1 ")
    c.execute("UPDATE mixedValues SET endLastDay = " + endLastDay + " WHERE idRow = 1 ")
    c.execute("UPDATE mixedValues SET currentHigh = " + currentHigh + " WHERE idRow = 1 ")
    c.execute("UPDATE mixedValues SET currentDown = " + currentDown + " WHERE idRow = 1 ")
    c.execute("UPDATE mixedValues SET currentValue = " + currentNumber + " WHERE idRow = 1 ")
    print(c.fetchall())
    conn.commit()
    # brakepoint
    time.sleep(int(sleepTime))
print("Done \033[31;1m!\033[0m\033[33;1m!\033[0m\033[32;1m!\033[0m")
conn.close()

