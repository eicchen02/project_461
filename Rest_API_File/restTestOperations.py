import requests

def main():
    
    #* Setup of header for all tests
    header = {'X-Authorization': 'Test'}
    
    #* Testing (Authenticate)
    response = requests.put("http://127.0.0.1:8080/authenticate", json={'Secret': {'password': 'TestTest'},
                                                                        'User': {'isAdmin': True,
                                                                                 'name': 'Test'}})
    print(f'Authentication Test: {response.json()}\n')
    
    #* Testing (Package Create)
    response = requests.post("http://127.0.0.1:8080/package", headers=header, json={'Content': '',
                                                                                    'JSProgram': '', 
                                                                                    'URL': 'https://github.com/cloudinary/cloudinary_npm'})
    print(f'Package Create Test, Grabbing JSON: {response.json()}')
    if(response.status_code == 201):
        data = response.json()['data']
        print(f'Package Create Test, Grabbing data: {data}')
        metadata = response.json()['metadata']
        print(f'Package Create Test, Grabbing metadata: {metadata}\n')
        package = metadata["Name"]
        id = metadata["ID"]
        version = metadata["Vers"]
    else:
        print(f'The package was not uploaded, due to an error code {response.status_code}\n')
    
    #TODO Testing (Package By Name History)
    response = requests.get("http://127.0.0.1:8080/package/byName/" + package, headers=header)
    if(response.status_code == 200):
        print(f'Package By Name History Test: {response.json()}\n')
    else:
        print(f'The package history could not be obtained by name, due to an error code {response.status_code}\n')
    
    # #TODO Testing (Package By RegEx Search)
    # response = requests.get("http://127.0.0.1:8080/package/byRegEx", headers=header, json={'regex': 'testRegEx'})
    # if(response.status_code == 200):
    #     print(f'Package By RegEx Search Test: {response.json()}\n')
    # else:
    #     print(f'The package could not be searched by RegEx, due to an error code {response.status_code}\n')
    
    
    #TODO Testing (Package By ID Retrieve)
    response = requests.get("http://127.0.0.1:8080/package/" + id, headers=header)
    if(response.status_code == 200):
        print(f'Package By ID Retrieve Test: {response.json()}\n')
    else:
        print(f'The package could not be retrieved by ID, due to an error code {response.status_code}\n')
    
    # #TODO Testing (Package By ID Update)
    # response = requests.get("http://127.0.0.1:8080/package/" + id, headers=header)
    # if(response.status_code == 200):
    #     print(f'Package By ID Update Test: {response.json()}\n')
    # else:
    #     print(f'The package could not be retrieved by ID, due to an error code {response.status_code}\n')

    #TODO Testing (Package By ID Rate)
    response = requests.get("http://127.0.0.1:8080/package/" + id + "/rate", headers=header)
    if(response.status_code == 200):
        print(f'Package By ID Rate Test: {response.json()}\n')
    else:
        print(f'The package could not be rated by ID, due to an error code {response.status_code}\n')
    
    #TODO Testing (Packages Fetch)
    response = requests.post("http://127.0.0.1:8080/packages", headers=header)
    if(response.status_code == 200):
        print(f'Packages Fetch Test: {response.json()}\n')
    else:
        print(f'The packages could not be fetched, due to an error code {response.status_code}\n')
    
    #*DELETE ZONE (too spicy, please only use one)

    # #TODO Testing (Package By Name Delete)
    # response = requests.delete("http://127.0.0.1:8080/package/byName/" + package, headers=header)
    # if(response.status_code == 200):
    #     print(f'Package By Name Deletion Test: {response.json()}\n')
    # else:
    #     print(f'The package could not be deleted by name, due to an error code {response.status_code}\n')


    #TODO Testing (Package By ID Delete)
    response = requests.delete("http://127.0.0.1:8080/package/0", headers=header)
    if(response.status_code == 200):
        print(f'Package By ID Delete Test: {response.json()}\n')
    else:
        print(f'The package could not be deleted by ID, due to an error code {response.status_code}\n')
    
    
    # #TODO Testing (Database Reset)
    # response = requests.delete("http://127.0.0.1:8080/reset", headers=header)
    # if(response.status_code == 200):
    #     print(f'Database Reset Test: {response.json()}\n')
    # else:
    #     print(f'The database could not be reset, due to an error code {response.status_code}\n')
    
if __name__ == "__main__":
    main()