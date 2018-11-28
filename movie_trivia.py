#use these first 2 functions to create your 2 dictionaries
import csv
def create_actors_DB(actor_file):
    '''Create a dictionary keyed on actors from a text file'''
    f = open(actor_file)
    movieInfo = {}
    for line in f:
        line = line.rstrip().lstrip()
        actorAndMovies = line.split(',')
        actor = actorAndMovies[0]
        movies = [x.lstrip().rstrip() for x in actorAndMovies[1:]]
        movieInfo[actor] = set(movies)
    f.close()
    return movieInfo

def create_ratings_DB(ratings_file):
    '''make a dictionary from the rotten tomatoes csv file'''
    scores_dict = {}
    with open(ratings_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__()
        for row in reader:
            scores_dict[row[0]] = [row[1], row[2]]
    return scores_dict


def insert_actor_info(actor, movies,actordb):
    '''Insert actor name and his or her movies to dictionary actordb if actor is
    not previously in actordb, else update the movies under the actor's name'''

    #Concatenate the sets if actor in actordb, otherwise add the actor and movies into the dictionary. 
    actordb[actor] = actordb[actor] | set(movies) if actor in actordb else set(movies)

def insert_rating(movie, rating, ratingsdb): 
    '''Insert movie name and the movie's ratings to dictionary ratingsdb if the movie is
    not previously in ratingsdb, else update the rating under the movie's name''' 

    #Insert or update movie rating 
    ratingsdb[movie] = rating

def select_where_actor_is(actor_name, actordb):
    '''return the list of movies stared by a given actor'''

    #get movies from the dictionary actordb using actor_name as the key
    movies = list(actordb[actor_name])
    #the function return the list of all movies
    return movies


def select_where_movie_is(movie_name, actordb):
    '''given a movie name, return the list of all actors in the movie'''

    #declare an empty list of actors
    actors = []
    #iterate throuth the key and values in dictionary actordb
    for actor, movies in actordb.items():
        #if movie_name is in values 
        if movie_name in movies:
            #the actor(key) is in the target movie, add the actor to the actor list
            actors.append(actor)
    #return the set of actors
    return actors


def select_where_rating_is(comparison, targeted_rating, is_critic, ratingsdb):
    '''return the list of movies that satisfy the specified condition of ratings'''

    #declare an empty list to store movies 
    movies = []
    #declare an empty list to store the target_ratings(critic or audience)
    target_ratings = []
   
    #if value of is_critic is True, take the critic ratings into audience rating
    if is_critic == True:
        for movie in ratingsdb:
            target_ratings.append(ratingsdb[movie][0])
    #otherwise, take the audience ratings into target_ratings
    else:
        for movie in ratingsdb:
            target_ratings.append(ratingsdb[movie][1])
    
    #inspect all the ratings in target_ratings 
    for i in range(len(target_ratings)):
        #if the comparison is >, 
        if comparison == '>' and int(target_ratings[i]) > targeted_rating:
            #add all movies whose target_ratings is greater than targeted rating to movies
            movies.append(list(ratingsdb.keys())[i])
        #if the comparison is =
        elif comparison == '=' and int(target_ratings[i]) == targeted_rating:
            #add all movies whose target_ratings is equal to targeted rating to movies
            movies.append(list(ratingsdb.keys())[i])
        #if the comparison is <
        elif comparison == '<' and int(target_ratings[i]) < targeted_rating:
            #add all movies whose target_ratings is smaller than targeted rating to moveis
            movies.append(list(ratingsdb.keys())[i])
    #return the list of movies
    return movies
        

def get_co_actors(actor_name,actor_db):
    '''given an actor name, return a list of 
    all actors that the given actor has ever worked with'''

    #declear an empty list to store actor names 
    actors = []
    #iterate the actors(keys) in actor_db
    for actor in actor_db:
        #iterate through all the movie that the given actor is in
        for i in range(len(actor_db[actor_name])):
            #if an actor is in the same movie with the given actor (exluding the given actor)
            if list(actor_db[actor_name])[i] in actor_db[actor] and actor != actor_name:
                #add the actor to the list of actors
                actors.append(actor)
    #use the set() to avoid duplicate names, return a list of actors
    return list(set(actors))


def get_common_movie(actor1, actor2, actor_db):
    '''take in two actor names and return a list of movies where
    both actors were cast, returns an empty list if they never
    worked together'''

    #declare an empty list to store the movies
    movies = []
    #iterate through all the movies that actor1 is in
    for i in range(len(actor_db[actor1])):
        #if there are any movie that actor2 is also in
        if list(actor_db[actor1])[i] in actor_db[actor2]:
            #add that movie to the movie list
            movies.append(list(actor_db[actor1])[i])
    #return the movies list
    return movies



def good_movies(ratingsdb):
    '''given a dictionary of movies, return the set of 
    movies that both critics and the audience have rated above
    85 (greater than or equal to 85)'''
    
    #get the movies that have critic ratings higher or equal to 85
    good_movies_critic = select_where_rating_is('>',85,True,ratingsdb)
    good_movies_critic = good_movies_critic + select_where_rating_is('=',85,True,ratingsdb)
    #get the movies that have audience ratings higher or equal to 85
    good_movies_audience = select_where_rating_is('>',85,False,ratingsdb)
    good_movies_audience = good_movies_audience + select_where_rating_is('=',85,False,ratingsdb)
    #add the movie to good_movies if both its critic and audience ratings are higher or equal to 85
    good_movies = [movie for movie in good_movies_critic if movie in good_movies_audience]

    #return the good_movies list
    return set(good_movies)



def get_common_actors(movie1, movie2, actor_db):
    '''given two movie names, return a list of actors that acted in both movies'''

    #declare an empty list to store the actors
    actors = []
    #iterate through all the actors
    for actor in actor_db:
        #find if movie1 and movie2 are in this actor's movie list
        if movie1 in actor_db[actor] and movie2 in actor_db[actor]:
            #if yes, add that actor to the actor list
            actors.append(actor)
    #return the actors list
    return actors


def change_to_lower(name,dictionary):
    '''change the input actor or movie name to match
    the ones in dictionary'''

    #change name to all lower cases
    name = name.lower()
    #match the movie or actor name in ratings_DB or actor_DB 
    for the_name in dictionary:
        if name == the_name.lower():
            #change the all lowercase name to the ones in database
            name = the_name
    #return the changed name
    return name



def main():
    '''tell the user what info my database has and answer their simple questions'''

    #read in moviedata and create actor info database
    actor_DB = create_actors_DB('moviedata.txt')
    #read in movieratings and create movie ratings database
    ratings_DB = create_ratings_DB('movieratings.csv')
    
    #Print a couple of welcome info and guidelines to asking questions
    print("\nWelcome to Daizhen's movie database\n")
    print("We have infomation about actors info and movie ratings\n")
    #ask the user for an input
    question = input("Press 1 for recommandatin of good movies\n\
Press 2 to inquiry the actor info\n\
Press 3 to inquity the movie ratings\n\
Press 4 for actors who's ever been in the same movie with your favorite actor\n")
    #if the user choose question 1
    if question == '1':
        #tell them the good movies based on our specification
        print(good_movies(ratings_DB))
    #if the user choose question 2
    elif question == '2':
        #ask who is the actor they wanna know
        actor = input('Who is the actor you want to know about?')
        #user change to lower function to help match with the name in database
        actor = change_to_lower(actor, actor_DB)
        #tell the user the name is not present if it's not in database
        if actor not in actor_DB:
            print('not present')
        #if the actor is in the database, print the movies he has benn in
        else:
            print(select_where_actor_is(actor,actor_DB))
    #if the user choose question 3
    elif question == '3':
        #ask what movie they want
        movie = input('What movie do you have in mind?')
        #match the movie name to the ones in our database
        movie = change_to_lower(movie, ratings_DB)
        #if the movie is not in our database, print error message
        if movie not in ratings_DB:
            print('not present')
        #otherwise give the ratings of the movie
        else:
            print("The critic's rating is %s and the audiences' rating is %s"\
             % (ratings_DB[movie][0],ratings_DB[movie][1]))
    #if the user choose question 4
    elif question == '4':
        #ask what actor is their favourite
        actor = input("Who's your favorite actor?")
        #match the actor name to our database
        actor = change_to_lower(actor, actor_DB)
        #print error message if the name is not in our databse
        if actor not in actor_DB:
            print('not present')
        #otherwise give the co-actor list if the user's favourite actor
        else:
            print(get_co_actors(actor,actor_DB))
    #if the user input something not specified, print error message
    else:
        print('Option Invalid')






if __name__ == '__main__':
    main()