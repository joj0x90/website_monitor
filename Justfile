set dotenv-load := true

default:
    @just --list

# Run locally
run:
        python src/main.py

# builds executable
build-exec:
        pyinstaller --onefile --noconsole src/main.py
        cp example.config.json dist/config.json
        cp .example.env dist/.env 

# builds the executable and packs it together with the config files
build: build-exec
        tar -czf "{{env_var('APP_NAME')}}_v{{env_var('APP_VERSION')}}.tar.gz" dist/

# removes all build files
clean:
        rm -rf build/
        rm -rf build-pkg
        rm -rf dist/
        rm -rf src/__pycache__/
        rm main.spec