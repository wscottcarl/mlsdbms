''' 
AUTHOR: WILLIAM SCOTT CARL
PURPOSE: MLS DBMS Implementation, final project CS 457
CTRL+C to quit interpreter
bugs: read() returns one extra '' at the end
'''

import copy

def main():
	table1 = read("t1.txt")
	table2 = read("t2.txt")
	table3 = read("t3.txt")

	while(True):
		query  = readQuery()
		parsed = parse(query)
		execute(parsed,table1,table2,table3)
	
def execute(query, t1, t2, t3):
	''' 
	Takes in a parsed query and tables, then implements joins and 
	security checking before printing final results
	'''
	table1 = list(t1)
	table2 = list(t2)
	table3 = list(t3)
	result = []
	
# when no where clauses
	if len(query[3]) == 0:

		# handle *
		if(query[1][0] == "*"):
			# access correct tables
			for table in query[2]:
				result.append(tableSelect(table,table1,table2,table3))

		# handle projections ALMOST DONE -- just need to zip results
		for table in query[2]:
			result.append(tableSelectProject(tableSelect(table,table1,table2,table3),query[1]))

# handling where clause
	else:
		for i in query[3]:
			
		
# 
#	print "RESULT -----------------------"
#	print result
	printTable(result)

def tableSelectProject(initTable,projects):
	''' Change so only takes in queries and a table, then filters
		out anything that isn't associated with a query column ''' 
	result = []
	col = 0
	for project in projects:
		table = copy.deepcopy(initTable)
		for i in range(0, len(table[0])):
			if table[0][i].lower() == project.lower():
				col = i
		for row in table:
			for entry in range(0,len(row)):
				if entry != col:
					row[entry] = ""
		for row in table:
			for entry in row:
				for thing in entry:
					if thing == '':
						entry.remove(thing)
				if entry == '':
					row.remove(entry)
		result.append(table)
	return zipResult(result)

def zipResult(tables):
	result = []
#	print "TABLES: ------------------"
#	print tables
	for table in tables:
		for row in table:
			result.append(row)
	return result

def tableSelect(table,table1,table2,table3):
	result = []
	if(table == "t1"):
		for row in table1:
			result.append(row)
	if(table == "t2"):
		for row in table2:
			result.append(row)
	if(table == "t3"):
		for row in table3:
			result.append(row)
	return result

def equijoin(t1,t2,cond):
	''' joins 2 tables where condition is true 
		returns table '''
	

	
def printTable(table):
	''' Add new row character to each line in table
		Add tab character to each entry in a line '''
	entries = []
	printer = []
	for tables in table:
		for line in tables:
			for entry in line:
				entry += '\t'
				entries.append(entry)
			line = entries
			line += "\n"
			line = "".join(line)
			printer.append(line)
			entries = []
	
	print "".join(printer)
	

def read(fileName):
	'''
	Reads each file in as a 2D array for easy access later
	'''
	fileOpen   = open(fileName,'r')
	fileText   = fileOpen.read()
	lines      = fileText.split('\n')
	cleanLines = [line.replace('\r', '') for line in lines]
	table      = [line.split('\t') for line in cleanLines]
	table.pop()
	return table
	
		
def readQuery():
	query = ""
	while(len(query) == 0 or query[-2] != ";"):
		query += raw_input(">") 
		query += " "
	return query
	
def parse(query):
	''' 
	Given "select * from t1 where cond"
	Not implemented fully
	'''
	secLvl, noCommas, parsed, select, tables, conds = [], [], [], [], [], []
	split     = query.split(' ')
	for i in split:
#		if(i[-1] == ","):
		if(i[-1:] == ";"):
			tmp  = i.replace(";","")
			semi = ";"
			noCommas.append(tmp)
			noCommas.append(semi)
		i = i.replace(",","")
		if(i != ","):
			noCommas.append(i)
	initTable  = iter(noCommas)
	
	hold = next(initTable)
	secLvl.append(hold)
# handle select
	hold = next(initTable)
	hold = next(initTable)
	while(not hold.lower() == "from"):
		select.append(hold)
		hold = next(initTable)
# handle from
	hold = next(initTable)
	while(not (hold.lower() == "where") and not (hold == ";")):
		tables.append(hold)
		hold = next(initTable)
# handle where
	if(not hold == ";"):
		hold = next(initTable)
		while(not hold.lower() == ";"):
			if(not hold.lower() == "and"):
				conds.append(hold)
			hold = next(initTable)
	if(len(conds) != 0):
		tmp = []
		for i in conds:
			tmp.append(i.split("="))
		conds = tmp
	parsed.append(secLvl)
	parsed.append(select)
	parsed.append(tables)
	parsed.append(conds )
	return parsed 
	
	
    
if __name__ == "__main__":
    main()
