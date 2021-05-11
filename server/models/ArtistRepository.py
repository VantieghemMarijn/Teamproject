import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import functools
import operator
import logging

# ---- Repo to query the artists.csv data

class ArtistRepository():
    
    def __init__(self, dataset):
        self.dataset = dataset
        self.genres = {}
        self.countries = {}

        #self.get_sorted_genres()
    
    #Give a bar graph of most popular genres
    def get_sorted_genres(self):
        for i in range(100000):
            rec = self.dataset['tags_mb'][i]
        
            if type(rec) == str:

                rec_tags = rec.split(';')
                for tag in rec_tags:

                    self.check_tag(tag, int(self.dataset['listeners_lastfm'][i]) / 100)

        sorted_d = dict( sorted(self.genres.items(), key=operator.itemgetter(1),reverse=True))
        short_dict =list(sorted_d.items())[:10]
        
        return short_dict
    
    #Give a bar graph of most popular countries
    def get_sorted_countries(self):
        for i in range(100000):
            rec = self.dataset['country_mb'][i]
        
            if type(rec) == str:
                self.check_country(rec)

        sorted_d = dict( sorted(self.countries.items(), key=operator.itemgetter(1),reverse=True))
        short_dict =list(sorted_d.items())[:10]
        
        return short_dict
    
     
    def check_tag(self, tag, amount):
        amount = round(amount, 2)
        
        if tag in self.genres:
            self.genres[tag] += amount

        else:
            self.genres[tag] = amount
    
    def check_country(self, tag):
    
        if tag in self.countries:
            self.countries[tag] += 1
        else:
            self.countries[tag] = 1


    # Function that handles querie request
    def execute_query(self, query_number, param):
        print(query_number ,param)
        response_type = ""

        # Return correct info per query

        try:
            if query_number == "Q0":
                if type(param) == str:
                    temp = self.dataset.loc[self.dataset['artist_mb'] == param].tags_mb.values
                    data = pd.Series(temp[0].split(';'))
                    response_type = "text_response"
                    data = data.to_json(orient='values')
                    header = "Artists Genres"
            
            elif query_number == "Q1":
                if type(param) == str:
                    data = self.dataset.loc[self.dataset['country_mb'] == param].artist_mb[:50]
                    response_type = "text_response"
                    data = data.to_json(orient='values')
                    header = f"Top 50 from {param}"

            elif query_number == "Q2":
                if type(param) == str:
                    data = self.dataset.loc[self.dataset['tags_mb'].str.contains(param, na=False)].artist_mb[:50]
                    response_type = "text_response"
                    data = data.to_json(orient='values')
                    header = f"Top 50 from genre {param}"

            elif query_number == "Q3":
                data = self.get_sorted_genres()
                response_type = "plot_response"
                header = f"Top 10 genres"

            elif query_number == "Q4":
                data = self.get_sorted_countries()
                response_type = "plot_response"
                header = f"Top 10 countries"

            else:
                raise Exception('Unkonw Querey number')
            print(data)

            return response_type, data, header

        except Exception as e:
            logging.error(e)
            
        
        

if __name__ == '__main__':
    repo = ArtistRepository()

    print(repo.execute_query('Q0', "Eminem"))
            
