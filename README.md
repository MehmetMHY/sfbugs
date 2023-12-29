# Scan Files Browser for Uncovering Guarded Sensitive-data (SFBUGS)

<p align="center">
  <img width="150" src="./assets/logo.png">
</p>

## About

CLI tool for listing files that contains sensitive information (phone numbers, emails, & addresses) in a given directory

## Limitations

- Only checks for phone numbers, addresses, and phone numbers
    - Currently only scans for US phone numbers
- Only scans text files (txt, py, css, html, js, md, etc) and PDFs
- Does not scan image, video, and/or audio files
- Currently, the default files/directories sfbugs ignores during a scan are: env, .DS_Store, .git, .env, node_modules, yarn.lock, & package-lock.json
    - Handling ignored files/directories needs to be handled in a better manner

## Setup (With Pip)

1. Install sfbugs:
    
    ```
    pip3 install .
    ```

2. Run it:

    ```
    # format:
    python3 main.py <dir_path> <ignore_list>

    # example:
    python3 main.py /root/ ".git,.env,package.json"
    ```

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

## Checkout (Alternative)

- https://github.com/redhuntlabs/Octopii

## Credit

- [OpenAI ChatGPT (GPT-4)](https://chat.openai.com/)
- [Stack Overflow](https://stackoverflow.com/)

