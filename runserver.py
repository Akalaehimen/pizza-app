# import the create_app function from the api package
from api import create_app

# create an instance of the app
app = create_app()

# run the app
# this is only run if the script is executed directly
# and not if it is imported
if __name__=="__main__":
    app.run()
