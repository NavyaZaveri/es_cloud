"""
A REST api hosted on heroku, acting as a wrapper around
the elastic-search dl library.
"""

import es_api

app = es_api.create_app("PRODUCTION")
if __name__ == "__main__":
    app.run()
