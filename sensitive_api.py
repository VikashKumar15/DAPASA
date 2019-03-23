import os

def gen_api(sfcg, categ):
	api_used = []
	f = open('Sensitive-{}'.format(categ), 'r')
	g = open('tmp', 'w+')
	for line in f:
		api = line.strip().split('#')
		if sfcg.has_node(api[0]):
			api[1] = str(int(api[1]) + 1)
			api_used.append(api[0])
		g.write('{}\n'.format('#'.join(api)))
	f.close()
	g.close()
	os.remove('Sensitive-{}'.format(categ))
	os.rename('tmp', 'Sensitive-{}'.format(categ))
	return api_used
