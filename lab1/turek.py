import os
import sys
import re
import codecs


def extractMeta(content):
    result = {}
    regex = r"<meta name=\"(.*?)\".*?content=\"(.*?)\""
    for match in re.finditer(regex, content, re.IGNORECASE):
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
    for match in re.finditer(r"<p[^>]*?>(.*?)</p>", " ".join(content.split("\n")), re.IGNORECASE | re.MULTILINE):
        result += " " + match.group(1)
    return result


def getSentencesCount(content):
    return len(re.findall(r"[^.?!]*?[.?!]+", content, re.IGNORECASE))


def getAbbreviations(pars):
    matchMap = {}
    for match in re.finditer(r"\s([a-z]{1,3}\.)", pars, re.IGNORECASE):
        matchMap[match.group(1)] = 1
        pars = pars.replace(match.group(1), "")
    return pars, len(matchMap)


def getInts(pars):
    intersMap = {}
    for match in re.finditer(r"(\s|^|\()(?P<num>(-?(([0-9]{1,4})|([0-2][0-9]{4})|(3[0-1][0-9]{3})|(32[0-6][0-9]{2})|"
                             r"(327[0-5][0-9])|(3276[0-7])))|(-32768))($|\s|\))", pars, re.IGNORECASE):
        intersMap[match.group("num")] = 1
    return len(intersMap)


def getDecs(pars):
    decsMap = {}
    for match in re.finditer(r"(\s|^|\()(-?(?P<left>\d*)\s*\.\s*(?P<right>\d*)(?P<e>e[+-]\d+)?)($|\s|\))", pars, re.IGNORECASE):
        if match.group("left") or match.group("right"):
            pars = pars.replace(match.group(0), "")
            decsMap[(match.group("left"), match.group("right"), match.group("e"))] = 1
    return pars, len(decsMap)


def getDelimiter(match):
    if match.group("del"):
        return match.group("del")
    elif match.group("del2"):
        return match.group("del2")
    elif match.group("del3"):
        return match.group("del3")
    else:
        return match.group("del4")


def normalizeDate(match):
    day = month = ""
    for i in range(1, 6):
        if match.group("day"+str(i)):
            day = match.group("day"+str(i))
            month = match.group("month"+str(i))
    if match.group("year1"):
        year = match.group("year1")
    else:
        year = match.group("year2")
    return day, month, year


def getDates(pars):
    dateMap = {}
    for match in re.finditer(r"((((?P<day1>(0[1-9])|([12][0-9])|(3[01]))(?P<del>[-\.\/])(?P<month1>(0[13578])|(1[02])))|"
                             r"((?P<day2>(0[1-9])|([12][0-9])|(30))(?P<del2>[-\.\/])(?P<month2>(0[469])|(11)))|"
                             r"((?P<day3>(0[1-9])|([12][0-9]))(?P<del3>[-\.\/])(?P<month3>02)))((?P=del)|(?P=del2)|"
                             r"(?P=del3))(?P<year1>\d{4}))|((?P<year2>\d{4})(?P<del4>[-\.\/])(((?P<day4>(0[1-9])|"
                             r"([12][0-9])|(3[01]))(?P=del4)(?P<month4>(0[13578])|(1[02])))|"
                             r"((?P<day5>(0[1-9])|([12][0-9])|(30))(?P=del4)(?P<month5>(0[469])|"
                             r"(11)))|((?P<day6>(0[1-9])|([12][0-9]))(?P=del4)(?P<month6>02))))", pars, re.IGNORECASE):
        dateMap[normalizeDate(match)] = 1
        pars = pars.replace(match.group(0), "")
    return pars, len(dateMap)


def getEmails(pars):
    res = 0
    for match in re.finditer(r"\w+(?:\.\w+)*@\w+(?:\.\w+)+", pars, re.IGNORECASE):
        pars = pars.replace(match.group(0))
        res += 1
    return pars, res

def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()

    meta = {}

    meta = extractMeta(content)
    pars = getParagraphs(content)
    (pars, abbrs) = getAbbreviations(pars)
    (pars, dates) = getDates(pars)
    (pars, decs) = getDecs(pars)
    (pars, mails) = getEmails(pars)
    ints = getInts(pars)

    fp.close()
    print("nazwa pliku:", filepath)
    print("autor: " + meta["AUTOR"])
    print("dzial:" + meta["DZIAL"])
    print("slowa kluczowe:" + str(extractKluczowe(meta)))
    print("liczba zdan:" + str(getSentencesCount(pars)))
    print("liczba skrotow:" + str(abbrs))
    print("liczba liczb calkowitych z zakresu int:" + str(ints))
    print("liczba liczb zmiennoprzecinkowych:" + str(decs))
    print("liczba dat:" + str(dates))
    print("liczba adresow email:" + str(mails))
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