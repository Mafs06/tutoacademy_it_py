from spyne import Application, rpc, ServiceBase, Integer, Boolean, Unicode, Array, ComplexModel, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import requests

class Profile(ComplexModel):
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
        if (r.status_code==200):
            print(r.status_code)            
            products_json=r.json().get('data', {}).get('allProfiles', [])
            print(r.json().get('data', {}))
            print("Hola mundo")
            
            products = []
            for product_data in products_json:
                products.append(
                    Profile(
                    fullname = product_data['fullname'],
                    gender = product_data['gender'],
                    birthdate = product_data['birthdate'],
                    nationality = product_data['nationality'],
                    degree = product_data['degree'],
                    description = product_data['description'],
                    creationdate = product_data['creationdate'],
                    profilestatus = product_data['profilestatus'],
                    )                    
                )                
                print(f"Products {products}")                
            return products            
        else:
            print("se puteo")
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
    server = make_server('0.0.0.0', 8000, wsgi_app)
    print("Server port 8000")
    server.serve_forever()