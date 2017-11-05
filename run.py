from app import app
app.secret_key = 'development_key'
if __name__ == '__main__':
    app.run()