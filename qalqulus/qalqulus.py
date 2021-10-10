import os,asyncio,discord # discord stuff

import argparse, cv2 # image recognition stuff

from dotenv import load_dotenv # configuration stuff
import re # regex

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as ' + str(client.user))

@client.event
async def on_message(message):
	channel = message.channel
	id = message.id

	if message.author != client.user:
		# match messages in the form of "!textbook_name page_# optional_problem_#"
		match = re.match(r'\!betaleithold (\d+) ?(\d+)?', message.content.lower())

		if match:
			page, problem = match.groups()
			page = int(page)

			# try:

			if problem:
				problem = int(problem)

				a = problem_loc(problem - 1, page) or (0,0)
				b = problem_loc(problem + 0, page) or (0,0)
				c = problem_loc(problem + 1, page) or (1500, 2000)

				top = min(a[1], b[1] + 64)
				bottom = max(b[1] + 200, c[1])

				left = min(a[0], b[0])
				right = max(b[0] + 700, c[0])

				page_image = cv2.imread(page_name(page))[top:bottom, left:right]

				cropped_name = 'cache/'+str(message.id)+'.jpg'
				cv2.imwrite(cropped_name, page_image)
				await channel.send(file=discord.File(cropped_name))

			else:
				await channel.send(file=discord.File(page_name(page)))

			# except Exception:
			# 	print(Exception)
			# 	await channel.send("I don't have that page!")

def page_name(page):
	return f'resources/leithold-{page}.jpg'

def problem_name(problem):
	return f'resources/leithold-n-{problem}.png'

def cv_image(file_name):
	return cv2.cvtColor(cv2.imread(file_name), cv2.COLOR_BGR2GRAY)

def problem_loc(problem, page):

	# load the input image and convert it to grayscale
	page_image = cv_image(page_name(page))
	problem_template = cv_image(problem_name(problem))

	# euclidean distance function for similarity score
	method = cv2.TM_SQDIFF_NORMED

	# apply template matching
	match = cv2.matchTemplate(page_image, problem_template, method)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

	if min_val < 0.02: #threshold
		return min_loc
	else:
		return None

client.run(os.environ['TOKEN'])
