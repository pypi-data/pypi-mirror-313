import requests

class pyrbac:
    def graph_token():
        """
        Retrieves the challenge token from the metadata service.
        """
        graphurl = "http://127.0.0.1:40342/metadata/identity/oauth2/token?api-version=2019-11-01&resource=https%3A%2F%2Fgraph.microsoft.com"
        headers = {"Metadata": "true"}
        response = requests.get(graphurl, headers=headers)
        
        for item, data in response.headers.items():
            if item == "Www-Authenticate":
                challenge_token_path = data.split("=")[1]
        if challenge_token_path is None:
            raise Exception("Failed to retrieve challenge token")
        with open(challenge_token_path, "r") as file:
            header = {"Metadata": "true", "Authorization": f"Basic {file.read()}"}
        response = requests.get(graphurl, headers=header)
        return response.json()['access_token']

    def mgmt_token():
        """
        Retrieves the challenge token from the metadata service.
        """
        mgmturl = "http://127.0.0.1:40342/metadata/identity/oauth2/token?api-version=2019-11-01&resource=https%3A%2F%2Fmanagement.azure.com"
        headers = {"Metadata": "true"}
        response = requests.get(mgmturl, headers=headers)
        
        for item, data in response.headers.items():
            if item == "Www-Authenticate":
                challenge_token_path = data.split("=")[1]
        if challenge_token_path is None:
            raise Exception("Failed to retrieve challenge token")
        with open(challenge_token_path, "r") as file:
            header = {"Metadata": "true", "Authorization": f"Basic {file.read()}"}
        response = requests.get(mgmturl, headers=header)
        return response.json()['access_token']
