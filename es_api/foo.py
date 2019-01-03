from es_api import create_app

app = create_app("TESTING")

if __name__ == "__main__":
    app.run()
