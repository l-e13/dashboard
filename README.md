# ACL Dashboard Filter

The following instructions to deploy the Streamlit application on Heroku are taken from the Deploy Using Heroku Git section of Heroku's Deployment Method information and the Deploy your Streamlit App to Heroku in 3 easy steps article on Medium.

## Log into Heroku Git
Use git in the command line or a GUI tool to deploy this app.

Download and install the Heroku CLI.

In terminal, log into your heroku account

```bash
$ heroku login
```

Clone repository to local machine
```bash
git clone
```

## Additional Files 
Navigate to repository on local machine and: 

Add a **requirements.txt** file that tells Heroku what dependencies to install for your app

For example: 
```bash
pandas==2.2.2
streamlit==1.36.0
openpyxl
```

Add **runtime.txt** file that tells Heroku what version of python to use

For example:
```bash
python-3.12.1
```

Add **Aptfile**
```bash
libjpeg-dev
zlib1g-dev
```

Add **setup.sh** file 
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-heroku@emailid.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```
- Don't forget to replace your-heroku@emailid.com with your Heroku email

Create **Procfile** which specifies the commands executed by the app on startup

In this example, it tells Heroku to run the setup.sh file and then run the streamlit_app.py file:
```bash
web: sh setup.sh && streamlit run streamlit_app.py
```

## Deploy using Heroku Git

Make some changes to the code you just cloned and deploy them to Heroku using Git.

```bash
$ git add .
$ git commit -am "make it better"
$ git push heroku main
```
