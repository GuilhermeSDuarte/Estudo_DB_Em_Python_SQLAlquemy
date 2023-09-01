import datetime
import pprint

import pymongo as pyM
# Conexão com o banco em nuvem.
cliente = pyM.MongoClient("Conexão com o banco")

db = cliente.test
collection = db.test_collection

print(db.test_collection)

# Definição de infos para compor o doc.
post = {
    "author": "Mike",
    "text": "My first mongodb application based on python",
    "tags": ["mongodb", "python3", "pymongo"],
    "date": datetime.datetime.utcnow()
}

# Preparando para submeter as infos.
posts = db.posts

post_id = posts.insert_one(post).inserted_id

print(post_id)

print(db.posts)

print(db.list_collection_names())

print(db.posts.find_one())

pprint.pprint(db.posts.find_one())

# bulk inserts
new_posts = [{
    "author": "Mike",
    "text": "Another post",
    "tags": ["bulk", "post", "insert"],
    "date": datetime.datetime.utcnow()
},
             {
    "author": "João",
    "text": "Post from Joao. New post available",
    "title": "Mongo is fun.",
    "date": datetime.datetime.utcnow()
             }]

result = posts.insert_many(new_posts)

print(result.inserted_ids)

print("\nRecuperação final.")
# find_one serve para recuperar apenas uma informação.
pprint.pprint(db.posts.find_one({"author": "João"}))

#  Para recuperar diversas informações dentro de um documento podemos definir um laço de repetição.
print("\nDocumentos presentes na coleção posts")

for post in posts.find():
    pprint.pprint(post)

# Serve para localizar e contar a quantidade de informações presentes nos documentos do banco.
print("\n Localizando informações dentro do arquivo.")
print("\n", posts.count_documents({}))
print(posts.count_documents({"authors": "João"}))
print(posts.count_documents({"tags": "mongodb"}))

# Recuperando informações de forma ordenada
print("\n Localizando informações e ordenando.")
for post in posts.find({}).sort("date"):
    pprint.pprint(post)

# Criando profiles de usuarios.

user_profile_user = [
    {'user_id': 211, 'name': 'Luke'},
    {'user_id': 212, 'name': 'Pedro'}
]

result = db.profiles_user.insert_many(user_profile_user)

print(db.list_collection_names())

# Deleta apenas um documento.
print(posts.delete_one({"author": "Mike"}))

# Abaixo serve para deletar os documentos criados no banco de dados.
db['posts'].drop()

# Abaixo temos um comando que remove o banco de dados, removemos por meio do client do banco pois já estamos acessando ele.

# client.drop_database('test')
