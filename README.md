# Find people that certain twitter account is following.

This is my student project in web development.
This is a web application that provieds you with the ability to find locations of people that the particular twitter account is 
following. It displays them on the map.


# Installation

From now on, every action described should be performed via terminal.

First, clone this repo to your machine.

```bash
git clone 'url'
```

Then, you need install all necessary dependencies from the "requirements.txt" file.
For doing that, use [pip](https://pip.pypa.io/en/stable/) package manager.

```bash
pip install -r requirements.txt
```


# Usage

After you've installed all the dependencies, navigate to the directory where "main.py" is located. Then run it:

```python
python3 main.py
```

You will see web server start running on your computer locally (127.0.0.0:5000).Open this link in your web browser.

You will see this:
![image](https://user-images.githubusercontent.com/91616521/154717002-cfda5e16-bb94-498a-ac12-f59704271367.png)

Then fill the fields of username of the person whose friends you want to find and the number of people to display on the map. After that click the "Find" button, or just hit "Enter" Do not leave the fields empty.

Generation of the map may take some time, since locations have to be accessed via Twitter API and then coordinates have to be located via geopy.geocoders. Thus, the more friends you request, the longer it will take.

If you want to see the fullscreen map on a separate page, click "Show Big Map" button on the right of the page. If you want to go back to the main page and re-enter the username from the big map page, just click the "Back To Main" button. 

This looks like this:
![image](https://user-images.githubusercontent.com/91616521/154717083-bb467ef4-c71f-419c-8386-6b7ec042f9c3.png)

You can also access this web application [here](http://yuriizinchuk.pythonanywhere.com/) for next three moths (till 18 March of 2022).


## Important notice!! 
Don't search people who don't follow anyone, this will result in an error.


# License
[MIT](https://choosealicense.com/licenses/mit/)
