# Functionality

Every important function in the code contains docstrings describing its main purpose and the arguments required.

This application has 2 "layers" of code:

The top layer:

- The functions which are provided to the fire CLI and consequently
- the functions that the users call

This layer solely exists to bridge the habit class and the functions that users call as well as to provide feedback on the actions the user takes. This basically enables the clean commands that the users call to use this application.

The bottom layer:

- The habit class
- The database connection

This layer takes care of the logic and the code for storing habits in the database
