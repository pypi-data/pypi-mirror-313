import os
import webbrowser
from ciocore.auth import server
import logging


def run(creds_file, base_url):
    port = int(os.environ.get('CONDUCTOR_AUTH_PORT', 8085))
    logging.debug("Base URL is %s" % base_url)
    url =  "{}/api/oauth_jwt?redirect_uri=http://localhost:{}/index.html&scope=user&response_type=client_token".format(base_url, port)
    if webbrowser.open_new(url):
        server.run(port=port, creds_file=creds_file)
    else:
        raise RuntimeError("Unable to open web browser on port {}. Try setting the CONDUCTOR_AUTH_PORT environment variable to a different port.".format(port))
