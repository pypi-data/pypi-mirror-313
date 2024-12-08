#cython: language_level=2


def verifie_mot(mot, set_a_tester, tolerance, max_propositions, dist):
	cdef double ressemble, max_ressemble
	cdef int taille

	if not set_a_tester or not mot:
		return set([mot])
	max_ressemble = 0
	taille = len(mot)
	propositions = set()
	ressemble = 0
	if taille == 1:
		return set([mot])

	corrections = dict()
	for mot_test in set_a_tester:
		if dist == 0:
			ressemble = distance_mai(mot, mot_test)
		elif dist == 1:
			ressemble = distance_jar(mot, mot_test)
		elif dist == 2:
			ressemble = distance_len(mot, mot_test)
		elif dist == 3:
			ressemble = round(1./3*(distance_mai(mot, mot_test) + \
									distance_jar(mot,mot_test) + \
									distance_len(mot,mot_test)),2)
		if ressemble in corrections:
			corrections[ressemble] |= {mot_test}
		else:
			corrections[ressemble] =  {mot_test}
		if max_ressemble < ressemble:
			max_ressemble = ressemble
	if max_ressemble < 0.4:
		return set([mot])
	for ressemble, mots_ressemble in corrections.iteritems():
		if ressemble > max_ressemble-tolerance :
			propositions |= mots_ressemble
	if len(propositions) <= max_propositions:
		return propositions
	else:
		return set([mot])


cdef inline double distance_len(mot, mot_ref):
	cdef int taille, taille_ref, i, substitution

	taille = len(mot)+1
	taille_ref = len(mot_ref)+1
	line1 = range(taille_ref)
	line2 = [1]+[0]*(taille_ref-1)
	for i in xrange(1,taille):
		for j in xrange(1,taille_ref):
			if mot_ref[j-1] == mot[i-1]:
				substitution = 0
			else:
				substitution = 1
			line2[j] = min(line1[j]+1, line2[j-1]+1,line1[j-1]+substitution)
		line1 = line2[:]
		line2 = [i+1]+[0]*(taille_ref-1)

	return  1-float(line1[taille_ref-1])/taille

cdef inline double distance_jar(mot, mot_ref):
	cdef int taille, taille_ref, taille_inter, match, transpose, eloignement, i, j

	taille_ref = len(mot_ref)
	taille = len(mot)

	if taille > taille_ref:
		taille_inter = taille_ref
		mot_inter = mot_ref
		taille_ref = taille
		mot_ref = mot
		taille = taille_inter
		mot = mot_inter

	eloignement = max(taille,taille_ref)/2-1
	match = 0
	transpose = 0
	lettre_match = []
	lettre_match_ref = []
	indice_match_ref = []
	for i,lettre in enumerate(mot):
		for j in xrange(max(0,i-eloignement),min(taille_ref,i+eloignement+1)):
			if lettre == mot_ref[j]:
				if j not in indice_match_ref:
					match += 1
					lettre_match.append(lettre)
					indice_match_ref.append(j)
					break
	indice_match_ref.sort()
	lettre_match_ref = [mot_ref[j] for j in indice_match_ref]

	for i,lettre in enumerate(lettre_match):
		if lettre != lettre_match_ref[i]:
			transpose += 1
	if match:
		return 1.*0.333*(float(match)/taille+float(match)/taille_ref+float(match-transpose)/match)
	else:
		return 0

cdef inline double distance_mai(mot, mot_ref):
	cdef int taille, div, i

	taille = len(mot)
	div = max(taille*2, len(mot_ref)*2) -1

	couples = [mot[i:i+2] for i in xrange(taille-1)]
	lettres = list(mot) + couples

	commun = [lettre for lettre in lettres if lettre in mot_ref]
	return float(len(commun))/div
