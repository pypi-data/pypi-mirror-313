# Welcome to the PCA packaged Add-on project!

This project includes the following Add-on elements:
- PCA





## If this project was created by the [Add-on Example Generator](https://github.com/seeq12/seeq-addon-templates.git):
* The Add-on Example Generator creates a virtual environment in the project folder.
* You will notice that the folder structure matches the elements you selected in the prompts of the Add-on Example
  Generator with their corresponding names.
* You can also see that the `addon.json` configuration has been filled with the answers to the questions you
  provided in the CLI.
* Finally, you will notice a `_dev_tools` folder that hosts all he utility functions that are helpful to develop,
  debug, package and deploy your Add-on. This folder is not meant to be manipulated, but you are welcome to look
  inside for more complex configurations.


# Getting Started
To deploy your Add-on package example to Add-on Manager, follow the steps below:
1. Activate the virtual environment
	* If you are using a Terminal, you can activate the virtual environment by running `source .venv/bin/activate`
	  (Linux/Mac) or `.venv\Scripts\activate` (Windows).
	* If you are using an IDE, you can configure the IDE to use the virtual environment.

2. Run `python addon.py deploy --url https://<my-seeq-server> --username <username> --password <password>` making
   sure you pass the correct URL, username, and password to your Seeq server.
3. Run `python addon.py watch` to make changes to the Add-on package and automatically update the changes to Add-on Manager.



# Development Notes
A global Python environment was created when this project was generated. This environment is located in the `.venv`
folder. If you want work with a specific element, you can run `python addon.py bootstrap --dir <element_folder>` to
create a virtual environment for that specific element. However, you can also
run ` python addon.py bootstrap --dir <element_folder> --global-python-env .` to update the global environment with new
dependencies that you might add to the `requirements.txt` file of each element.

## Logs
You can get the logs of the Add-on Manager from the server you are deploying to. The following commands can be used:
* `python addon.py logs` to get a list of all the logs files from the Add-on Manager.
* `python addon.py logs --file <log_file>` to get the content of a specific log file.
* `python addon.py logs-aom` is a shortcut of `python addon.py logs --file com.seeq.add-on-manager.log`.

Tailing the logs is not currently supported.
