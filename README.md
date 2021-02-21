# Hello and welcome to Geolocation_RESTful_API

## Summary
This simple RESTful API connects to ipstack API (https://ipstack.com/) allowing users to 
learn geolocation data based on IPs and save them to the Postgres db. 


## Running the app
The app is deployed to Heroku: https://geolocation-restful-api.herokuapp.com
To test the app, you can use a platform for API development, e.g. Postman. 
I provide a Postman collection in a file Geolocation_RESTful_API.postman_collection.json.  
  
If you want to use the code with your own ipstack API Key, 
you need to create your own API key. 
To do that, go to ipstack API (https://ipstack.com/signup/free)
and follow the guidelines. Then, add the API key as an os environment variable named 'GEOLOCATION_API_KEY'.  
Next, install all the dependencies (see: requirements.txt).  
Finally, you can run the app from the console by entering: 'python app.py' command.


## API's available endpoints
Again, this is the API URL: https://geolocation-restful-api.herokuapp.com 
  
The API has the following endpoints: 
  
/register (POST)
  
/login (POST)
    
/geolocation (GET, POST)  
  
/geolocation/<string:ip> (GET, DEL)


## API collection
A Postman collection is saved in a file BGeolocation_RESTful_API.postman_collection.json. Feel free to download it to check the API endpoints easily.
