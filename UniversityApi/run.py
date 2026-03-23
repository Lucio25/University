from app import create_app

# Aquí es donde se conectan los cables:
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)