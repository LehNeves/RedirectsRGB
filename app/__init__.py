import json
from sqlalchemy import create_engine 


engine = create_engine('mysql://user:password@host:port/nome_banco')

arquivo = json.load(open("urls.json"))
cont = 0

#regex
# prefixo = "/^\\\/conteudo\\\/"
# sufixo = "(\\.html)?$/"
prefixo = "/^"
sufixo = "(\\\.html)?$/"

#url
#pre = "conteudo/""
#pos = ".html"
pre = ""
suf = ""

for url in arquivo:
	list_from = url['301']['from']

	for each_from in list_from:
		to = ''
		to = url['301']['to']

		with engine.connect() as connection:
			each_from = prefixo + each_from + sufixo
			sql = f'SELECT id from core_redirecionamento where regex like "{each_from}"'
			result = connection.execute(sql)
			if len(result.fetchall()) > 0:
				continue
			to = pre + to + suf

			sql = 'INSERT INTO core_redirecionamento (regex, url, tipo, observacoes, status, insert_data) '
			sql += f'VALUES ("{each_from}", "{to}", "301", "", "a", now())'

			print (sql)
			result = connection.execute(sql)
			connection.close()
			cont += 1
print(cont)
