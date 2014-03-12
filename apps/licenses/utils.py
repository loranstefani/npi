import json
import urllib2



def compare_license_number_to_mlvsjson(state, number, license_type, mlvsjson):
    d = json.loads(mlvsjson)
    
    print d['state'], state, d['number'], number, d['license_type'], license_type,
    if d['state'] == str(state) and \
       d['number'] == str(number) and \
       d['license_type'] == str(license_type):
        return True
    return False

def compare_license_number_to_mlvsdict(state, number, mlvsdict):
    if mlvsdict['state'] == state and mlvsdict['number'] == number:
        return True
    return False


def get_dict_from_mlvs(mlvsjson):
    d = json.dumps(mlvsjson)
    return d


def build_mlvs_url(base_server_url,  number):
    url = "%s/%s.json" % (base_server_url, number)
    return url


def query_mlvs_server(url):
    """
    Get the resource as a JSON string. If attempts fails due to 404
    or other error, return an empty string.
   """     
    jsonresponse=""
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
        jsonresponse = response.read()
    except urllib2.URLError, e:
        jsonresponse=""
    return jsonresponse
  
  
  

    