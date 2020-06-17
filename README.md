# Share Pixels by NotPixar

## The team
- William Cao (PM)
- Ethan Chen: Frontend and Graphic Design
- Joseph Yusufov: Frontend & Flask/Database

## Description
To create a platform for people to share their artwork similar to Imgur, Tumblr, and Reddit. Users will create pixel arts, which will automatically be shared with others. Most websites are based on creating artwork on an external application then uploaded online. This website will combine those two steps to increase availability and ease to use.

## Video Demo
[Youtube](https://www.youtube.com/watch?v=UgHol6oySg4)

## Instructions to run
We are assuming you have python3 and pip3 installed and working.

Run the following:
1. Clone the repo
    ```bash
    $ git clone https://github.com/WilliamC07/NotPixar.git
    ```
2. Change directory into it
    ```bash
    $ cd NotPixar
    ```
3. Create a python virtual environment
    ```bash
    $ python3 -m venv superhero
    ``` 
4. Use the virtual environment
    ```bash
   # if you are using bash
   $ . superhero/bin/activate
   # if you are using zsh
   $ source superhero/bin/activate
   
   # To deactivate run this
   $ deactivate
   ```
5. Install the required packages
    ```bash
    $ pip3 install -r requirements.txt 
    ```
6. Run make
    ```bash
    $ make
   
    # If this does not work, please run
    $ python3 app/initialize.py
    $ python3 app/__init__.py
    ```
7. Visit ```http://127.0.0.1:5000/``` in your browser to start using!

# Run tests
Please follow steps 1-5 in launch instructions first then run:
```bash
$ python3 app/test.py
```
