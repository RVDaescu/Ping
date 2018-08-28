import os

cwd = os.getcwd()

sql_path = cwd + '/sql/'
graphs_path = cwd + '/graphs/'
lib_path = cwd + '/lib/'

#compatible for multiple sql databases
#structure: {db:{table: "tb.db", results: "result.db"}
dbs = {'hosts.sqlite': [{'table': 'Internet', 'results': 'res_db.sqlite','down_nr': 3}, 
                        {'table': 'Interlan', 'results': 'res_interlan.sqlite', 'down_nr': 1}],
       'proxy.sqlite': [{'table': 'Germany_elite', 'results': 'res_de.sqlite', 'down_nr': 3}, 
                        {'table': 'France_elite', 'results': 'res_fr.sqlite', 'down_nr': 3},
                        {'table': 'Japan_elite', 'results': 'res_jp.sqlite', 'down_nr': 3}]}
#                        {'table': 'Russia_elite', 'results': 'res_rs.sqlite', 'down_nr': 3}]
