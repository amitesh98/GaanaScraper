from selenium import webdriver
import requests
import bs4
import os
from pandas.core.dtypes.missing import isnull

# radio, top, track, artist scraper from Gaana.com
radio_mirchi = "https://gaana.com/radiomirchi"
gaana_radio= "https://gaana.com/gaanaradio"
top_album= "https://gaana.com/browse/albums"
top_songs="https://gaana.com/browse/songs"
track_artist_url = "https://gaana.com/search/"

# create the selenium browser
# Selenium driver must be on the same folder as the Gaana_Scraper.py file
browser = webdriver.Chrome()
browser.get("https://gaana.com/")

# main menu
print()
print(">>> Welcome to the Python Gaana.com Scraper!")
print(">>> Explore the Top / New & Hot Charts for all Genres")
print(">>> Search for tracks, artists, and mixes")
print()

while True:
    print(">>> Menu")
    print(">>> 1 - Search for Top Songs")
    print(">>> 2 - Search for Top Albums")
    print(">>> 3 - Listen to Mirchi Radio")
    print(">>> 4 - Listen to Gaana Radio")
    print(">>> 5 - Search for Songs/Artist/Playlist")
    print(">>> 0 - Exit")
    print()

    choice = int(input(">>> Your choice: "))
	#Logic for exiting the program
    if choice == 0:
        browser.quit()
        break
    print()

    # search for top Songs
    if choice == 1:
        request = requests.get(top_songs)
        soup = bs4.BeautifulSoup(request.text, "lxml")
        while True:
            print(">>> Songs Available: ")
            print()
            songs = soup.select("a[href*=song]")[4:]
            song_name=[]
            song_links = []

            # list out all of the available songs
            count=0
            for index, song in enumerate(songs):
                #album_available=genre.text.strip()
                if len(song.text.strip())>0:
                    print(str(count) + ": " + song.text)
                    count+=1
                    song_name.append(song.text)
                    song_links.append(song.get("href"))

            print()
            choice = input(">>> Your choice (x to go back to the main menu): ")
            print()

            if choice == "x":
                break
            else:
                choice = int(choice)

            url = song_links[choice]
			#Below logic will play the selected song from the list

            print("Now playing: " + song_name[choice])
            request = requests.get(url)
            browser.get(url)
            play=browser.find_element_by_xpath('//*[@id="p-list-play_all"]')
            play.click()
            choice = input(">>> press 'x' to go back to the main menu: ")
            print()
            if choice == "x":
                break

    # search for top albums
    if choice == 2:
        request = requests.get(top_album)
        soup = bs4.BeautifulSoup(request.text, "lxml")
        while True:
            print(">>> Albums Available: ")
            print()
            albums = soup.select("a[href*=album]")[6:]
            #print((genres.text()))
            album_name=[]
            album_links = []

            # list out all of the available albums
            count=0
            for index, album in enumerate(albums):

                if len(album.text.strip())>0:
                    print(str(count) + ": " + album.text)
                    count+=1
                    album_name.append(album.text)
                    album_links.append(album.get("href"))

            print()
            choice = input(">>> Your choice (x to go back to the main menu): ")
            print()

            if choice == "x":
                break
            else:
                choice = int(choice)
				
			#Below logic will play the selected album from the list
            url = "https://gaana.com" + album_links[choice]

            print("Now playing: " + album_name[choice])
            request = requests.get(url)
            browser.get(url)
            play=browser.find_element_by_xpath('//*[@id="p-list-play_all"]')
            play.click()
            choice = input(">>> press 'x' to go back to the main menu: ")
            print()
            if choice == "x":
                break


    # Listen to mirchi Radio
    if choice == 3:
        request = requests.get(radio_mirchi)
        soup = bs4.BeautifulSoup(request.text, "lxml")
        while True:
            print(">>> Radio Available: ")
            print()
            genres = soup.select("a[href*=radio]")[3::3]
            genre_links = []

            # list out all the available mirchi radio
            for index, genre in enumerate(genres):
                radio_available=genre.text.strip()
                if isnull(radio_available):
                    continue
                print(str(index) + ": " + radio_available)
                genre_links.append(genre.get("href"))

            print()
            choice = input(">>> Your choice (x to go back to the main menu): ")
            print()

            if choice == "x":
                break
            else:
                choice = int(choice)
			
			# Logic to play the selected Mirchi Radio from the list
            url = "https://gaana.com" + genre_links[choice]

            request = requests.get(url)
            browser.get(url)
            play=browser.find_element_by_xpath('//*[@id="p-list-play_all"]')
            play.click()
            choice = input(">>> press 'x' to go back to the main menu: ")
            print()
            if choice == "x":
                break
	# Listen to Gaana Radio
    if choice == 4:
        request = requests.get(gaana_radio)
        soup = bs4.BeautifulSoup(request.text, "lxml")
        while True:
            print(">>> Category Available: ")
            print()
            category = soup.select("h2")[4:-1]
            category_links = []
            category_names = []
			
			# List out the category avaliable in Gaana Radio
            for index, categ in enumerate(category):
                category_links.append(categ.a.get("href"))
                category_names.append(categ.text[:-13])
                print(str(index + 1) + ": " + categ.text[:-13])
				
            while True:
                choice = input(">>> Your choice (x to re-select a new genre): ")
                print()

                if choice == "x":
                    break
                else:
                    choice = int(choice) - 1
                
                url = "https://gaana.com" + category_links[choice]
                request = requests.get(url)
                soup = bs4.BeautifulSoup(request.text, "lxml")
                print(">>> Radio Available: ")
                print()
                genres = soup.select("a[href*=gaanaradio]")[3::3]
                genre_links = []
    
                # List out all of the available Ganna Radio from the selected category
                for index, genre in enumerate(genres):
                    radio_available=genre.text.strip()
                    if isnull(radio_available):
                        continue
                    print(str(index) + ": " + radio_available)
                    genre_links.append(genre.get("href"))
    
                print()
                choice = input(">>> Your choice (x to go back to the main menu): ")
                print()
    
                if choice == "x":
                    break
                else:
                    choice = int(choice)
				
				# Logic to play the selected radio from the list
                url = "https://gaana.com" + genre_links[choice]
				
                request = requests.get(url)
                browser.get(url)
                play=browser.find_element_by_xpath('//*[@id="main_middle_content"]/div[4]/div[1]/div[2]/div/div[1]/ul/li/div/div[1]/img')
                play.click()
                choice = input(">>> press 'x' to go back to main menu: ")
                print()
                if choice == "x":
                    break
            break
			
    # Search for an Artist/Song/Playlist
    if choice == 5:
        name = input("Name of the Song/Artist/Playlist: ")
        print()
        "%20".join(name.split(" "))
        browser.get(track_artist_url + name)
        continue

print()
print("Goodbye!")
print()