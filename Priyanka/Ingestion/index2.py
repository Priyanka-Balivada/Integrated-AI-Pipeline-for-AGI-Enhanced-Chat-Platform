from llama_index.core import download_loader

from llama_index.readers.google import GoogleDocsReader

loader = GoogleDocsReader()
documents = loader.load_data(document_ids=["1LaA7pVJyAAwva886C17v4lcK5pypxdQgKLFB7SzrP_k"])

# from requests_oauthlib import OAuth2Session

# client_id = '421151121208-gigho5vrunqpvq51gp41oetdp0efeqc1.apps.googleusercontent.com'
# client_secret = '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'
# redirect_uri = 'http://localhost:8005/'

# authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
# token_url = 'https://oauth2.googleapis.com/token'
# scope = ['https://www.googleapis.com/auth/documents.readonly']

# oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
# authorization_url, state = oauth.authorization_url(authorization_base_url)

# print('Please go to this URL and authorize:', authorization_url)

# redirect_response = input('Paste the full redirect URL here: ')
# oauth.fetch_token(token_url, authorization_response=redirect_response, client_secret=client_secret)

# # Use the OAuth session to access Google Docs API
# response = oauth.get('https://docs.googleapis.com/v1/documents/1LaA7pVJyAAwva886C17v4lcK5pypxdQgKLFB7SzrP_k')
# document_data = response.json()
# print(document_data)
