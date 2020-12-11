* To Run the Project:

Set your directory to the folder called bookmarks

1. Create a virtual environment: 

	$ python3 -m venv my_env
	$ source my_env/bin/activate

(The first command might be python or python3 based on your computer and the version of Python)

2. Install the necessary packages: 

	$ pip install -r requirements.txt

3. Run the server:

	$ python manage.py runserver


* The Architecture of the Project:

- Under the general bookmark directory there are several folders that handle the different apps.
- The second bookmarks folder in here is central folder for the project
- The recipes folder is for the blog app of the project. The main two functionalities this provides is writing recipes and general articles. Other post related features such as liking posts or commenting are also handled here. 
- The account folder is for the user accounts, authentication and the user related activities such as profiles, messaging or following. 
- The common folder is for the general extra elements that would be helpful in multiple locations. Currently this holds the custom decorators.
- The media folder stores the media related files such as pictures. In the database the url routes for the media are stored and the actual content is accessed through this folder. 

* The MVC Structure
Inside every app, there are models.py, views.py, a templates folder and urls.py

- Model: models.py corresponds to the Model in the MVC. This is where our database models are stored.
- View: The templates folder corresponds to the View in the MVC and they handle what the user is supposed to see and interact. Here the html, css and javascript files are stored. 
- Controller: The views.py file corresponds to the Controller in the MVC. Here, basedo n the user input received in the View layer, requests are taken and put into the view functions. These functions perform operations on the input, retrieves relevant information from the database and calls out the relevant views (templates in the case of Django) with the appropriate context variables.
- urls.py: This file is used to configure the urls patterns. It matches which url pattern is responsible for calling which view function.

(The Model-View-Controller architecture is sometimes called Model-Template-View in the context of Django. In terms of the operations each layer in the architecture handles they are equivalent, however, they are called with different names.)
