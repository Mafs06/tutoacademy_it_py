from spyne import Application, rpc, ServiceBase, Boolean, Array, ComplexModel, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import requests



class userID(ComplexModel):
        googleId = String
        imageUrl = String
        authStatus = Boolean

class Profile(ComplexModel):
        userId = userID
        fullname = String
        gender = String
        birthdate = String
        nationality = String
        degree = String
        description = String
        creationdate = String
        profilestatus = Boolean

class Service(ServiceBase):
            
    @rpc(_returns=Array(Profile))
    def getAllProfiles(self):
        #GraphQL request
        graphql_url = 'http://localhost:4000/graphql/'
        graphql_query = """query {
              allProfiles {
                userID{
                    googleId
                    imageUrl
                    authStatus
                }
                fullname
                gender
                birthdate
                nationality
                degree
                description
                creationdate
                profilestatus
          }
        }"""        
        r = requests.post(graphql_url, json={'query': graphql_query})
        try:        
            profile_json=r.json().get('data', {}).get('allProfiles', [])

            
            profiles = []
            for profile_data in profile_json:
                profiles.append(
                    Profile(
                    userId = userID(
                         googleId = profile_data['userID']['googleId'],
                         imageUrl = profile_data['userID']['imageUrl'],
                         authStatus = profile_data['userID']['authStatus']),
                    fullname = profile_data['fullname'],
                    gender = profile_data['gender'],
                    birthdate = profile_data['birthdate'],
                    nationality = profile_data['nationality'],
                    degree = profile_data['degree'],
                    description = profile_data['description'],
                    creationdate = profile_data['creationdate'],
                    profilestatus = profile_data['profilestatus'],
                    )                    
                )                

            return profiles     
               
        except:
            
            print("Something failed")
            return [];        

soap_app = Application([Service],
                       tns='your-namespace',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

wsgi_app = WsgiApplication(soap_app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    #Se expone en el puerto 8000
    #Se puede ver el archivo wsdl en localhost:8000/?wsdl
    server = make_server('0.0.0.0', 8100, wsgi_app)
    print("Server port 8100")
    server.serve_forever()