# ACL Dashboard Filter

The following instructions to deploy the Streamlit application on Heroku are taken from the Deploy Using Heroku Git section of Heroku's Deployment Method information and the Deploy your Streamlit App to Heroku in 3 easy steps article on Medium.

## Additional Files 
Add a requirements.txt file that tells Heroku what dependencies to install for your app

For example: 
```bash
pandas==2.2.2
streamlit==1.36.0
openpyxl
```

Add runtime.txt file that tells Heroku what version of python to use

For example:
```bash
python-3.12.1
```


## Deploy using Heroku Git
Use git in the command line or a GUI tool to deploy this app. Install the Heroku CLI

Download and install the Heroku CLI.

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.
```bash
$ heroku login
```
Clone the repository

Use Git to clone baseball-tix-dash's source code to your local machine.

$ heroku git:clone -a baseball-tix-dash 
$ cd baseball-tix-dash
Deploy your changes

Make some changes to the code you just cloned and deploy them to Heroku using Git.

$ git add .
$ git commit -am "make it better"
$ git push heroku master
