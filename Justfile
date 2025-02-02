set dotenv-load := true

default:
    @just --list

# Run locally
run:
        python src/main.py

# builds executable
build-exec-locally:
        pyinstaller --onefile --noconsole src/main.py
        cp example.config.json dist/config.json
        cp .example.env dist/.env 

# builds the executable and packs it together with the config files
build-targz: build-exec-locally
        tar -czf "{{env_var('APP_NAME')}}_v{{env_var('APP_VERSION')}}.tar.gz" dist/

# logs into docker account (specify login credentials in .env-file)
docker_login:
    echo "Logging into Docker..."
    echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USERNAME" --password-stdin

# builds the docker images for the current version and latest
build-images:
         docker build -t "$DOCKER_USERNAME/$(echo "$APP_NAME" | tr '[:upper:]' '[:lower:]'):$APP_VERSION" \
                        -t "$DOCKER_USERNAME/$(echo "$APP_NAME" | tr '[:upper:]' '[:lower:]'):latest" .

# always runs the latest image
run-image: build-images
        docker run "$DOCKER_USERNAME/$(echo "$APP_NAME" | tr '[:upper:]' '[:lower:]'):latest"

# publishes only the image, with the current version tag
publish-current-image: build-images docker_login
        docker push "$DOCKER_USERNAME/$(echo "$APP_NAME" | tr '[:upper:]' '[:lower:]'):$APP_VERSION"

# publishes only the "latest" image.
publish-latest-image: build-images docker_login
        docker push "$DOCKER_USERNAME/$(echo "$APP_NAME" | tr '[:upper:]' '[:lower:]'):latest"

# removes all build files
clean:
        rm -rf build/
        rm -rf build-pkg
        rm -rf dist/
        rm -rf src/__pycache__/
        rm main.spec