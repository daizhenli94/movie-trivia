#import the file being tested
from movie_trivia import *

#import unittest module
import unittest

#define a class of unittest
class Testmovietrivia(unittest.TestCase):

	def test_insert_actor_info(self):
		'''unit test for insert_actor_info'''
		test_dict = {}
		insert_actor_info('Daizhen Li',['I','Am','Awesome'],test_dict)
		self.assertEqual(test_dict,{'Daizhen Li': {'I','Am','Awesome'}})
		test_dict2 = {'Foo':{'Bar','Bar'}}
		insert_actor_info('Foo',['No','Surprise'],test_dict2)
		self.assertEqual(test_dict2,{'Foo':{'Bar','Bar','No','Surprise'}})
		test_dict3 = {'small':{'orange','yuzu'}}
		insert_actor_info('big',['apple','pear'],test_dict3)
		self.assertEqual(test_dict3,{'small':{'orange','yuzu'},'big':{'apple','pear'}})

	def test_insert_rating(self):
		test_dict = {}
		insert_rating('Avatar',['91','99'],test_dict)
		self.assertEqual(test_dict,{'Avatar': ['91','99']})
		test_dict2 = {'Fifty Shades of Grey':['11','15']}
		insert_rating('Fool',['22','33'],test_dict2)
		self.assertEqual(test_dict2,{'Fifty Shades of Grey':['11','15'], 'Fool':['22','33']})
		test_dict3 = {'small':['16','17']}
		insert_rating('small',['19','20'],test_dict3)
		self.assertEqual(test_dict3,{'small':['19','20']})

	def test_select_where_actor_is(self):
		test_dict = {'small':{'orange','yuzu'},'big':{'apple','banana'}}
		self.assertEqual(set(select_where_actor_is('small', test_dict)), set(['orange','yuzu']))


	def test_select_where_movie_is(self):
		test_dict = {'Daizhen Li':{'movie a','movie b','movie c'},'Li Daizhen':{'movie a','movie d'}}
		self.assertEqual(select_where_movie_is('movie a',test_dict),['Daizhen Li','Li Daizhen']) 

	def test_select_where_rating_is(self):
		ratingsdb = {'movie a':['85','90'],'movie b':['99','70'],'movie c':['76','79']}
		self.assertEqual(select_where_rating_is('>',80,True,ratingsdb),['movie a','movie b'])
		self.assertEqual(select_where_rating_is('=',90,False,ratingsdb),['movie a'])
		self.assertEqual(select_where_rating_is('<',90,False,ratingsdb),['movie b','movie c'])

	def test_get_co_actors(self):
		test_dict = {'a':{'movie a','movie b'},'b':{'movie a','movie c'},'c':{'movie d'}}
		self.assertEqual(get_co_actors('a',test_dict),['b'])
		self.assertEqual(get_co_actors('c',test_dict),[])

	def test_get_common_movie(self):
		test_dict = {'a':{'movie a','movie b'},'b':{'movie a','movie c'}}
		self.assertEqual(get_common_movie('a','b',test_dict),['movie a'])
		test_dict2 = {'a':{'movie a','movie b'},'b':{'movie d','movie c'}}
		self.assertEqual(get_common_movie('a','b',test_dict2),[])

	def test_good_movies(self):
		ratingsdb = {'movie a':['86','90'],'movie b':['99','85'],'movie c':['76','86']}
		self.assertEqual(set(good_movies(ratingsdb)),set(['movie a','movie b']))
		ratingsdb2 = {'movie a':['84','90'],'movie b':['99','84'],'movie c':['79','80']}
		self.assertEqual(set(good_movies(ratingsdb2)),set([]))
    
	def test_get_common_actors(self):
		test_dict = {'a':{'apple','tree','friends'},'b':{'this','tree','apple'},'c':{'friends','apple','yes'}}
		self.assertEqual(get_common_actors('apple','tree',test_dict),['a','b'])
		self.assertEqual(get_common_actors('friend','tree',test_dict),[])

	def test_change_to_lower(self):
		test_dict = {'a':{'apple','tree','friends'},'b':{'this','tree','apple'},'c':{'friends','apple','yes'}}
		self.assertEqual(change_to_lower('MoViE A',test_dict),'movie a')
		ratingsdb = {'Movie A':['86','90'],'movie b':['99','85'],'movie c':['76','86']}
		self.assertEqual(change_to_lower('mOVie a',ratingsdb),'Movie A')





if __name__ == '__main__':
	unittest.main()