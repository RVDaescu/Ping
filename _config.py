import os

cwd = os.getcwd()

sql_path = cwd + '/sql/'
graphs_path = cwd + '/graphs/'
lib_path = cwd + '/lib/'

#compatible for multiple sql databases
#structure: {db:{table: "tb.db", results: "result.db"}
dbs = {'hosts.sqlite': [{'table': 'Internet', 'results': 'res_db.sqlite'}, 
                        {'table': 'Interlan', 'results': 'res_interlan.sqlite'}],
       'proxy.sqlite': [{'table': 'Germany_elite', 'results': 'res_de.sqlite'}, 
                        {'table': 'France_elite', 'results': 'res_fr.sqlite'},
                        {'table': 'Japan_elite', 'results': 'res_jp.sqlite'}, 
                        {'table': 'Russia_elite', 'results': 'res_rs.sqlite'}]
      }
