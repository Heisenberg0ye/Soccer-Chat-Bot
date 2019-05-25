# Soccer-Chat-Bot
> A chat bot from which you can get some soccer data when you chat with him on WeChat.

## Display
![display](https://user-images.githubusercontent.com/35055583/58366678-6e63a200-7f08-11e9-90a3-1a2d46549782.gif)

## Installation
The project needs python3.7, rasa_nlu, spacy, en_core_web_md, wxpy to run. Use the following command to build the enviroment.

    git clone
    pip install -r requirements.txt
    
### Run
Use the following command to run the program.

    PYTHONPATH=/Soccer-Chat-Bot python run.py
    
## Explanation

There are two packages in the project, the nlu_process package and the soccer_data_api package. If you have all the requirements installed, run the "run.py" to start the program.  

You may need a token in [football-data](https://www.football-data.org/) website to get the api service. You need to input the token when you run the program for the first time.  

Change the user's name in "run.py" to let the chat bot response to the message send by specific user.

## Meta

Heisenberg – zb_ye@foxmail.com

<a rel="license" href="https://opensource.org/licenses/MIT"><img alt="Creative Commons license" style="border-width:0" src="https://opensource.org/files/OSI_Approved_License.png" width="100"/></a><br />this project is licensed under <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">The MIT License</a>
