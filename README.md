# Scan Files Browser for Uncovering Guarded Sensitive-data (SFBUGS)

<p align="center">
  <img width="100" src="./assets/logo.png">
</p>

## About

CLI tool for listing files that contains sensitive information (phone numbers, emails, & addresses) in a given directory

## Setup (Not Though Pip)

1. Make sure you are using a Unix-Based operating system and you have a "modern" Python 3 version installed. Also make sure you have this project's repo cloned and cd-ed into.

2. Setup python environment:

    ```
    python3 -m venv env
    source env/bin/activate
    ```

3. Install dependencies:

    ```
    pip3 install -r requirements.txt
    ```

4. Run script:
    
    ```
    # format:
    python3 main.py <dir_path> <ignore_list>
    
    # example:
    python3 main.py /root/ ".git,.env,package.json"
    ```

5. After you are done, turn off the python environment:

    ```
    deactivate
    ```

## Checkout

- https://github.com/redhuntlabs/Octopii
