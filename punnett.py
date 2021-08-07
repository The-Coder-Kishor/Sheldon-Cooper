import datetime

def headtex():
	head = '\\begin{table}[]\n\\centering\n\\caption{Punnett square}\n\\label{punnettsquare}\n'
	return head
	
def width(c1, c2):
	w = '\\begin{tabular}{l|' + 'l'*max(len(c1), len(c2)) + '}\n\\hline\n'
	return w
	
def freqhead():
	freqhead = '\\begin{table}[]\n\\centering\n\\caption{Genotypes frequencies}\n\\label{genotypesfreq}\n\\begin{tabular}{ll}\n\\hline\nGenotypes & Frequencies \\\ \\hline'
	return freqhead
		
def foottex():
	foot = '\n\\end{tabular}\n\\end{table}'
	return foot
		
	
def get_all_combinations(parent): # Finds all possible combinations of alleles a parent can pass on to their offspring, assuming independen assortment.
	if len(parent) == 1:
		return [parent[0][0], parent[0][1]]
	else:
		genlist = []
		for x in get_all_combinations(parent[1:]):
			genlist.append(parent[0][0] + x)
			genlist.append(parent[0][1] + x)
		return genlist

def make_row(genotype, allele):
	row = []
	for a in genotype:
		row.append(a + allele)
	return row

def make_table(parent1, parent2):
	table = []
	for a in parent1:
		table.append(make_row(parent2, a))
	return table

def print_table(table, c1, c2): # formats and prints Punnett square
	latextable = []
	divlength = (len(c1[0])*2+4)*2**(len(c1[0]))
	t = ''
	for a in c2:
		t = t + str(' '*(len(c1[0])+3) + a + '', end=' ')
		latextable.append('& ' + a + ' ')
	t = t + str('\n' + ' '*(len(c1[0])+1) + '-'*(divlength))
	latextable.append('\\\ \n\\hline\n')
	
	for i, row in enumerate(table):
		t = t + str(c1[table.index(row)], end=' ')
		latextable.append(c1[table.index(row)] + ' & ')
		t = t + str('|', end=' ')
		for j, cell in enumerate(row):
			t = t + str(cell + ' | ', end=' ')
			if j != len(row)-1:
				latextable.append(cell + ' & ')
			else:
				latextable.append(cell + ' ')
		t = t + str('\n' + ' '*(len(c1[0])+1) + '-'*(divlength))
		if i != len(table)-1:
			latextable.append('\\\ \n')	
	return t
	
def print_genotype_frequencies(table): # calculates frequencies for each genotype present in table
	freqtable = []
	freqtable.append('\n')
	calculated = []
	genotypes = [a for b in table for a in b]
	m = ""
	for k, x in enumerate(genotypes):
		count = 0
		for y in genotypes:
			if sorted(x) == sorted(y):
				count += 1
		if sorted(x) not in calculated:
			m = m + ("The frequency of the " + x + " genotype is " + str(float(count)/float((len(genotypes)))*100) + "%." + "\n")
			freqtable.append(x + ' & ' + str(float(count)/float((len(genotypes)))*100) + '\\% \\\ \\hline \n')	
		calculated.append(sorted(x))	
	return m