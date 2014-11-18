# random_idx.py
# creates random index vectors for a number of languages

# libraries
import sys
import numpy as np
import string
import utils
import pandas as pd

alphabet = string.lowercase

def generate_vectors(N, k, cluster_sz, languages=None):

		if languages == None:
				languages = ['english','german','norwegian','finnish']

		clusters = utils.generate_clusters(alphabet,cluster_sz=cluster_sz)
		#print clusters

		M = len(clusters) # number of letter clusters
		num_lang = len(languages)
		num_letters = len(alphabet)

		# build row-wise k-sparse random index matrix
		# each row is random index vector for letter
		RI_letters = np.zeros((num_letters,N))
		for i in xrange(num_letters):
				rand_idx = np.random.permutation(N)
				RI_letters[i,rand_idx[0:k]] = 1
				RI_letters[i,rand_idx[k:2*k]] = -1
		RI = np.zeros((M,N))
		for i in xrange(M):
				# calculate repeats
				cluster = clusters[i]
				first = cluster[0]
				repeats = 0
				for char in cluster:
						if first == char:
								repeats += 1

				if repeats == len(cluster):
						# check if cluster all same letter
						letter_idx = alphabet.find(first)
						#print first, RI_letters[letter_idx,:]
						RI[i,:] = RI_letters[letter_idx,:]
				else:
						letters = list(cluster)
						prod = np.ones((1,N))
						for letter in letters:
								letter_idx = alphabet.find(letter)
								prod = np.multiply(prod, RI_letters[letter_idx,:])
						RI[i,:] = prod
		#				print cluster, RI[i,:]
		#		print cluster, RI[i,:]
		#print RI
		lang_vectors = np.zeros((num_lang,N))
		for i in xrange(num_lang):
				# load text one at a time (to save mem), English, German, Norwegian
				lang_text = utils.load_lang(languages[i])
				for char_num in xrange(len(lang_text)):
						if char_num < cluster_sz:
								continue
						else:
								# build cluster
								cluster = ''
								for j in xrange(cluster_sz):
										cluster = lang_text[char_num - j] + cluster
								if cluster in clusters:
										cluster_idx = clusters.index(cluster)
										lang_vectors[i,:] += RI[cluster_idx,:]

		return lang_vectors