# Endpoints
### Master Client:
#### /menu (this endpoint render menu of clients)
#### /files_manager (this endpoint render file manager)



# Run
### 1) On your clients run project client
### 2) On your master client run project master_client
### 3) In menu of master client add your clients
### 4) Upload your file


# Run scripts
### 1) you have to write script and following instractions(they will be under)
### 2) compare to zip file
### 3) go to file_manager and choese files which you want to handle
### 4) upload your script and wait. Output will download in txt format in your website



# Instructions to write scripts
### 1) in your folder which has to be called "script" you have to create two files .py. First file is client_setup.py and the Second is master_client_setup.py
### 2) in client_setup.py create function
``` 
def handle(data):
    # data is bytes
    # here is can be any script
    return (anything)
```
### 3) in master_client_setup.py create function
``` 
def compare(result_list):
    # result list is list of results all handle of clients
    # here is can be any script
    return (anything)
```


