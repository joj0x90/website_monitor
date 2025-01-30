set dotenv-load := true

default:
    @just --list

# Run locally
run:
        python src/main.py

# builds executable
build-exec:
        pyinstaller --onefile --noconsole src/main.py

# builds the executable and packs it together with the config files
build: build-exec
        mkdir -p build-pkg
        cp dist/main build-pkg
        cp example.config.json build-pkg/config.json
        cp .example.env build-pkg/.env 
        tar -czf "{{env_var('APP_NAME')}}_v{{env_var('APP_VERSION')}}.tar.gz" build-pkg

# removes all build files
clean:
        rm -rf build/
        rm -rf build-pkg
        rm -rf dist/
        rm -rf src/__pycache__/
        rm main.spec