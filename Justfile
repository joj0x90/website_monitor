default:
    @just --list

# Run locally
run:
        python src/main.py

# builds executable
build:
        pyinstaller --onefile --noconsole src/main.py

# removes all build files
clean:
        rm -rf build/
        rm -rf dist/
        rm -rf src/__pycache__/
        rm main.spec