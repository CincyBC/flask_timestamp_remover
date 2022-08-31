# flask_timestamp_remover
Migrating the simple Zoom timestamp remover python function as a deployed serverless function with simple web interface.

The function opens up a txt file and looks at the beginning of each line for something that looks like a xx:xx:xx timestamp and stores the index in a list. At the end, it removes the timestamps in reverse order since removing them from the start of the list could impact the index of a down the stream timestamp.
