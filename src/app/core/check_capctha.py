import json
import urllib.request


def check_recaptcha(response, secretkey):
        url = (f'https://www.google.com/recaptcha/api/siteverify'
               f'?secret={str(secretkey)}&response={str(response)}')

        jsonobj = json.loads(urllib.request.urlopen(url).read())
        if jsonobj['success']:
            return True
        else:
            return False
