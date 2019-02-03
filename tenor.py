import discord
import asyncio
import aiohttp
import requests
import configparser
import datetime
import sqlite3

config = configparser.ConfigParser()
config.read('keys.ini')

client = discord.Client()
apikey = config['Tenor']['key']

@client.event
async def on_ready():
	await client.change_presence(game=discord.Game(name="If you need help, type tenor.help"))
	print("Tenor Bot is ready to work")

@client.event
async def on_guild_join(guild):
	print("Joined")

@client.event
async def on_guild_remove(guild):
	print("Removed")

@client.event
async def on_message(message):

	#search gifs from tenor
	if message.content.startswith("tenor.search"):
		message_content = message.content
		split_message = message_content.split()
		len_message = int(len(split_message)) - 1
		datetime_now = datetime.datetime.now()
		time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
		try:
			int(split_message[len_message])
			check = True
		except:
			check = False
		if check == False:
			search = "https://api.tenor.com/v1/search?q={}&key={}&limit=1&media_filter=basic".format(split_message[1:], apikey)
			get = requests.get(search)
			if get.status_code == 200:
				json_search = get.json()
				json_check = json_search['next']
				if json_check == "0":
					await message.channel.send("{} I didn't found any gifs".format(message.author.mention))
				else:
					json_s = json_search['results']
					table = json_s[0]
					title = table["title"]
					ID = table['id']
					url = json_search['results']
					url = url[0]
					url = url['url']
					shares = json_search['results']
					shares = shares[0]
					shares = shares['shares']
					table = table.get("media")
					table = table[0]
					table = table.get("gif")
					table = table.get("url")
					if title == "":
						title = "None"
					search_embed = discord.Embed(title="Search Results", colour=discord.Color.blue(), image="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
					search_embed.add_field(name="Title: ", value=title, inline=False)
					search_embed.add_field(name="ID: ", value=ID, inline=False)
					search_embed.add_field(name="Link: ", value=url, inline=True)
					search_embed.set_image(url=table)
					search_embed.set_footer(text="You sent requests at {}".format(time), icon_url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
					search_embed.set_thumbnail(url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
					await message.channel.send(embed=search_embed)
			elif get.status_code == 404:
				await message.channel.send("{} Tenor is working at the moments now!".format(message.author.mention))	
		elif check == True:
			search_limit = split_message[len_message]
			split_message.pop()
			search = "https://api.tenor.com/v1/search?q={}&key={}&limit={}&media_filter=basic".format(split_message[1:], apikey, search_limit)
			get = requests.get(search)
			if get.status_code == 200:
				json_s = get.json()
				json_check = json_s["next"]
				if json_check == "0":
					await message.channel.send("{} I didn't found any gifs".format(message.author.mention))
				elif json_check < search_limit:
					await message.channel.send("{} The maximum of this search is {}!".format(message.author.mention, json_check))
				else:
					json_s = json_s["results"]	
					i = 0
					while i <= int(search_limit):
						table = json_s[i]
						title = table['title']
						ID = table['id']
						url = json_s[i]
						url = url['url']
						table = table.get("media")
						table = table[0]
						table = table.get("gif")
						table = table.get("url")
						#await message.channel.send("{}".format(table))
						if title == "":
							title = "None"
						i += 1
						search_embed = discord.Embed(title="Search Results", colour=discord.Color.blue(), image="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
						search_embed.add_field(name="Title: ", value=title, inline=False)
						search_embed.add_field(name="ID: ", value=ID, inline=False)
						search_embed.add_field(name="Link: ", value=url, inline=True)
						search_embed.set_image(url=table)
						search_embed.set_footer(text="You sent requests at {}".format(time), icon_url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
						search_embed.set_thumbnail(url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
						await message.channel.send(embed=search_embed)
						if i == int(search_limit):
							break
						else:
							continue			
			elif get.status_code == 404:
				await message.channel.send("{} Tenor is working at the problems now!".format(message.author.mention))
		elif split_message[len_message] == 50:
			await message.channel.send("{} It's to much gifs in 1 time!".format(message.author.mention))
	
	# trending gifs from tenor
	if message.content.startswith("tenor.trending"):
		message_trend = message.content
		join_message = message_trend.split()
		datetime_now = datetime.datetime.now()
		time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
		if len(join_message) == 1:
			trend = "https://api.tenor.com/v1/search?key={}&limit=1&media_filter=basic".format(apikey)
			get_trend = requests.get(trend)
			if get_trend.status_code == 200:
				json_trend = get_trend.json()["results"]
				ID = json_trend[0]
				ID = ID['id']
				title = json_trend[0]
				title = title['title']
				url = json_trend
				url = url[0]
				url = url["url"]
				json_trend = json_trend[0]
				json_trend = json_trend.get("media")
				json_trend = json_trend[0]
				json_trend = json_trend.get("gif")
				json_trend = json_trend.get("url")
				trending_embed = discord.Embed(title="Trending Results", colour=discord.Colour.blue())
				trending_embed.add_field(name="Title: ", value=title, inline=True)
				trending_embed.add_field(name="ID: ", value=ID, inline=True)
				trending_embed.add_field(name="Link: ", value=url, inline=True)
				trending_embed.set_image(url="{}".format(json_trend))
				trending_embed.set_footer(text="You sent requests at {}".format(time), icon_url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
				trending_embed.set_thumbnail(url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
				await message.channel.send(embed=trending_embed)

		elif len(join_message) == 2 and join_message[len_message] <= 49:
			trend = "https://api.tenor.com/v1/search?key={}&limit={}&media_filter=basic".format(apikey, join_message[1])
			get_trend = requests.get(trend)
			trending_embed = discord.Embed(title="Trending Results", colour=discord.Colour.blue())	
			if get_trend.status_code == 200:
				counter_trend = 0
				while counter_trend <= int(join_message[1]):
					json_trend = get_trend.json()["results"]
					ID = json_trend[0]
					ID = ID['id']
					title = json_trend[counter_trend]
					title = title['title']
					url = json_trend[counter_trend]
					url = url['url']
					json_trend = json_trend[counter_trend]
					json_trend = json_trend.get("media")
					json_trend = json_trend[0]
					json_trend = json_trend.get("gif")
					json_trend = json_trend.get("url")
					counter_trend += 1
					trending_embed.add_field(name="Title: ", value=title, inline=True)
					trending_embed.add_field(name="Link: ", value=url, inline=False)
					trending_embed.add_field(name="ID: ", value=ID, inline=True)
					trending_embed.set_image(url=json_trend)
					trending_embed.set_footer(text="You sent requests at {}".format(time), icon_url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
					trending_embed.set_thumbnail(url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
					await message.channel.send(embed=trending_embed)
					if counter_trend == int(join_message[1]):
						break	
					else:
						continue   
					

	# Random gifs from tenor					
	if message.content.startswith("tenor.random"):
		message_random = message.content
		split_random = message_random.split()
		datetime_now = datetime.datetime.now()
		time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
		if len(split_random) == 1:
			await message.channel.send("{} You must add a question".format(message.author.mention))
		elif len(split_random) >= 2:
			search_random = "https://api.tenor.com/v1/random?key={}&q={}&limit=1&media_filter=basic".format(apikey, split_random[1:])
			random_request = requests.get(search_random)
			if random_request.status_code == 200:
				try:
					json_random = random_request.json()['results']
					gif = json_random[0]
					title = gif['title']
					ID = gif['id']
					url = gif['url']
					gif = gif.get("media")
					gif = gif[0]
					gif = gif.get("gif")
					gif = gif.get("url")
					if title == "":
						title = "None" 
					random_embed = discord.Embed(title="Random Results", colour=discord.Colour.blue())
					random_embed.add_field(name="Title: ", value=title, inline=False)
					random_embed.add_field(name="ID: ", value=ID, inline=False)
					random_embed.add_field(name="Link: ", value=url, inline=False)
					random_embed.set_image(url=gif)
					random_embed.set_footer(text="You sent requests at {}".format(time), icon_url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
					random_embed.set_thumbnail(url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
					await message.channel.send(embed=random_embed)
				except:
					await message.channel.send("{} Sorry, but I hasn't found any gif!".format(message.author.mention))

	# A trending gifs from another categories
	if message.content.startswith("tenor.categories"):
		message_categories = message.content
		split_categories = message_categories.split()
		datetime_now = datetime.datetime.now()
		time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
		if len(split_categories) == 1 or split_categories[1] == "trending":
			categories = "https://api.tenor.com/v1/categories?key={}&media_filter=basic&type=trending".format(apikey)
			requests_categories = requests.get(categories)
			if requests_categories.status_code == 200:
				json_categories = requests_categories.json()["tags"]
				path = json_categories[0]
				print(type(path))
				path = path.get('path')
				categories = json_categories[0]
				categories = categories.get('image')
				path_url = path
				path_requests = requests.get(path_url)
				if path_requests.status_code == 200:
					path_json = path_requests.json()["results"]
					title = path_json[0]
					title = title["title"]
					ID = path_json[0]
					ID = ID["id"]
					url = path_json[0]
					url = url['url']
					categories_embed = discord.Embed(title="Random Results", colour=discord.Colour.blue())
					categories_embed.add_field(name="Title: ", value=title, inline=False)
					categories_embed.add_field(name="ID: ", value=ID, inline=False)
					categories_embed.add_field(name="Link: ", value=url, inline=False)
					categories_embed.set_image(url=categories)
					categories_embed.set_footer(text="You sent requests at {}".format(time), icon_url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
					categories_embed.set_thumbnail(url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
					await message.channel.send(embed=categories_embed)
		elif split_categories[1] == "emoji":
				await message.channel.send("{} The Tenor api is broken to show trending emoji, try another!".format(message.author.mention))
		elif split_categories[1] == "featured":
			categories = "https://api.tenor.com/v1/categories?key={}&media_filter=basic&type=featured".format(apikey)
			requests_categories = requests.get(categories)
			if requests_categories.status_code == 200:
				json_categories = requests_categories.json()["tags"]
				path = json_categories[0]
				print(type(path))
				path = path.get('path')
				categories = json_categories[0]
				categories = categories.get('image')
				path_url = path
				path_requests = requests.get(path_url)
				if path_requests.status_code == 200:
					path_json = path_requests.json()["results"]
					title = path_json[0]
					title = title["title"]
					ID = path_json[0]
					ID = ID["id"]
					url = path_json[0]
					url = url['url']
					if title == "":
						title = "None"
					categories_embed = discord.Embed(title="Random Results", colour=discord.Colour.blue())
					categories_embed.add_field(name="Title: ", value=title, inline=False)
					categories_embed.add_field(name="ID: ", value=ID, inline=False)
					categories_embed.add_field(name="Link: ", value=url, inline=False)
					categories_embed.set_image(url=categories)
					categories_embed.set_footer(text="You sent requests at {}".format(time), icon_url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
					categories_embed.set_thumbnail(url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
					await message.channel.send(embed=categories_embed)

	if message.content.lower() == "tenor.top":
		trendings = "https://api.tenor.com/v1/trending_terms?key={}&limit=3".format(apikey)
		requests_trendings = requests.get(trendings)
		datetime_now = datetime.datetime.now()
		time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
		if requests_trendings.status_code == 200:
			json_trendings = requests_trendings.json()["results"]
			get_1 = json_trendings[0]
			get_2 = json_trendings[1]
			get_3 = json_trendings[2]
			trendings_embed = discord.Embed(title="Top Trending searches", color=discord.Colour.blue())
			trendings_embed.add_field(name="Top Searches today: ", value="1.{}\n2.{}\n3.{}".format(get_1, get_2, get_3), inline=False)
			trendings_embed.set_footer(text="You sent requests at {}".format(time), icon_url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
			trendings_embed.set_thumbnail(url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
			await message.channel.send(embed=trendings_embed)

	# Sending a help commands
	if message.content.lower() == "tenor.help":
		datetime_now = datetime.datetime.now()
		time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
		help_embed = discord.Embed(title="Tenor Bot Help", colour=discord.Colour.blue())
		help_embed.add_field(name="Commands: ",
		value="`t.search [question] [limit|50]` - searching gif using name or name and limit, default limit is 1\n"
		"`tenor.trending [limit|50]` - send a daily gif trend from Tenor\n"
		"`tenor.categories [trending, emoji, featured]` - send a top from categories trending, emoji and featured, default is trending\n"
		"`tenor.random [question]` - gives you a one random gif\n"
		"`tenor.top` - send a top searched from this day\n"
		"`tenor.help` - shows all commands on this bot\n"
		"`tenor.about` - showing information about this bot\n"
		"`tenor.version` - showing current version of this bot"
		,inline=False)
		help_embed.set_thumbnail(url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
		help_embed.set_footer(text="You sent requests at {}".format(time), icon_url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
		await message.channel.send(embed=help_embed)

	# Information about Tenor Bot
	if message.content.lower() == "tenor.about":
		about_embed = discord.Embed(title="Tenot Bot About", colour=discord.Colour.blue())
		about_embed.add_field(name="About this bot",
		value="This bot is searching and showing information about gifs from tenor.com", inline=False)
		about_embed.add_field(name="Links", value="Bot website: https://discordbots.org/bot/529054239570264084\n"
		"github repo: https://github.com/MRmlik12/Tenor-Bot-Discord")
		await message.channel.send(embed=about_embed)
	
	if message.content.lower() == "tenor.version":
		version_embed = discord.Embed(title="Tenor Bot Version", colour=discord.Colour.blue())
		version_embed.add_field(name="Current Version", value="v1.5", inline=True)
		version_embed.add_field(name="Update Date", value="3/02/2019", inline=True)
		version_embed.add_field(name="Changes", value="- Added a new line of description `tenor.about`", inline=True)
		await message.channel.send(embed=version_embed)


# A discord bot token in keys.ini
client.run(config['Discord']['key'])