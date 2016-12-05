import requests, json
import unicodedata
def getsuggestions(question):
    URL = "http://suggestqueries.google.com/complete/search?client=firefox&q=" + question
    print URL
    headers = {'User-agent':'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    result = json.loads(response.content.decode('utf-8'))
    """
    if len(result[1])> 5:
         six = [unicodedata.normalize('NFKD', i).encode('ascii','ignore').replace("i love my", "").lstrip() \
                for i in result[1][5:]]
         app.config['SIX'] = six
         """
    """
    one = [unicodedata.normalize('NFKD', i).encode('ascii','ignore').replace("i love my", "").lstrip() \
                for i in result[1][:5]]
    app.config['ONE'] = one
        """
    return [unicodedata.normalize('NFKD', i).encode('ascii','ignore').replace("i love my", "").lstrip() \
                for i in result[1]]
print getsuggestions("programmers are")