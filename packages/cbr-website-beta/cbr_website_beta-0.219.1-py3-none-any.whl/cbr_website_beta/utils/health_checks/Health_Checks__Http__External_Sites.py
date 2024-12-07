import requests


class Health_Checks__Http__External_Sites:

    @staticmethod
    def head__google():
        url = 'https://www.google.com'
        response = requests.head(url)
        if response.status_code != 200:
            raise Exception('head__google status code was not 200')
        return 'google is up'