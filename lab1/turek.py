import os
import sys
import re
import codecs


def extractMeta(content):
    result = {}
    regex = r"<meta name=\"(.*?)\".*?content=\"(.*?)\""
    for match in re.finditer(regex, content, re.IGNORECASE):
        # print match.group(0)
        result[match.group(1)] = match.group(2)

    return result


def extractKluczowe(meta):
    result = []
    for entry in meta.iteritems():
        if re.match(r"kluczowe_.*", entry[0], re.IGNORECASE):
            result.append(entry[1])

    return result


def getParagraphs(content):
    result = ""
    for match in re.finditer(r"<p>(.*?)</p>", " ".join(content.split("\n")), re.IGNORECASE | re.MULTILINE):
        result += " " + match.group(1)
    return result


def getSentencesCount(content):
    return len(re.findall(r"[^.]*?\.", content, re.IGNORECASE))


def getAbbreviations(pars):
    matchMap = {}
    for match in re.finditer(r"\s([a-z]{1,3}\.)", pars, re.IGNORECASE):
        matchMap[match.group(1)] = match.group(1)
        pars.replace(match.group(1), "")

    return len(matchMap)


def getInts(pars):
    retList = re.findall(r"[^0-9]((-?(([0-9]{1,4})|([0-2][0-9]{4})|(3[0-1][0-9]{3})|(32[0-6][0-9]{2})|" +
                         r"(327[0-5][0-9])|(3276[0-7])))|(-32768))", pars, re.IGNORECASE)
    # print retList
    return len(retList)


def getDecs(pars):
    pass


def getDates(pars):
    dateMap = {}
    for match in re.finditer(r"(((((0[1-9])|([12][0-9])|(3[01]))(?P<del>[-\.\/])((0[13578])|(1[02])))|"
                             r"(((0[1-9])|([12][0-9])|(30))(?P<del2>[-\.\/])((0[469])|(11)))|"
                             r"(((0[1-9])|([12][0-9]))(?P<del3>[-\.\/])(02)))((?P=del)|(?P=del2)|"
                             r"(?P=del3))(\d{4}))|((\d{4})(?P<del4>[-\.\/])((((0[1-9])|([12][0-9])|"
                             r"(3[01]))(?P=del4)((0[13578])|(1[02])))|(((0[1-9])|([12][0-9])|(30))(?P=del4)((0[469])|"
                             r"(11)))|(((0[1-9])|([12][0-9]))(?P=del4)(02))))", pars, re.IGNORECASE):
        print match.group(0)
    return 0


def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()

    meta = {}

    meta = extractMeta(content)
    pars = getParagraphs(content)
    abbrs = getAbbreviations(pars)
    dates = getDates(pars)
    ints = getInts(pars)
    decs = getDecs(pars)

    fp.close()
    print("nazwa pliku:", filepath)
    print("autor: " + meta["AUTOR"])
    print("dzial:" + meta["DZIAL"])
    print("slowa kluczowe:" + str(extractKluczowe(meta)))
    print("liczba zdan:" + str(getSentencesCount(pars)))
    print("liczba skrotow:" + str(abbrs))
    print("liczba liczb calkowitych z zakresu int:" + str(ints))
    print("liczba liczb zmiennoprzecinkowych:")
    print("liczba dat:" + str(dates))
    print("liczba adresow email:")
    print("\n")



try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)


tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)