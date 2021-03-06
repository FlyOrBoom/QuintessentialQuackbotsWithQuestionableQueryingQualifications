from print_fancy import *
print_time('Starting Qlassroom...')
import base64, re, random, os, sys, time, asyncio, socket
import dotenv, config, cache
import gmail, discord
print_time('Imported everything.')

async def background(discord_client):

	await discord_client.wait_until_ready()
	print_success('Logged in as',str(discord_client.user))
	while True:
		last_refresh = time.time()
		await handler()
		await asyncio.sleep(
			 last_refresh - time.time() + config.read('refresh interval')
		)

async def handler():	

	email_ids = gmail.fetch_email_ids()

	print_time(
		'\033[90mNew emails:\033[0m',
		str(len(email_ids))
	)

	if not email_ids: return False 

	### Get channels	
	try:
		channel_ids = config.read('channel ids')	
	except TypeError:
		print_error('No channels specified')
		return False


	channels = {
		discord_client.get_channel(int(channel_id))
		for channel_id
		in channel_ids 
		if channel_id
	}

	if not channels:
		print_warning('No valid channels found.')
		print(channel_ids)
		return False

	return await asyncio.gather(*[
		send_email_to_channels(email_id,channels)
		for email_id
		in email_ids
	])

async def send_email_to_channels(email_id,channels):

	### Fetch email
	email_full = gmail.fetch_email(email_id)

	try:
		email_b64 = email_full['payload']['parts'][0]['body']['data']
	except KeyError:
		print_warning(f'Body data not found in email {email_id}.')
		print(email_full)
		return False

	### Decode email
	
	try:
		email_text = base64.urlsafe_b64decode(
			email_b64
		).decode('utf-8').replace('\r','')
	except AttributeError:
		print_warning(f'Cannot decode email {email_id}.')
		print(email_b64)
		return False

	### Find matches in email body
	
	try:
		pattern = config.read('email pattern')
		matches = re.search(
			pattern,
			email_text
		).groups()
	except AttributeError:
		print_warning(f'Email {email_id} does not match pattern.')
		print(pattern,email_text)
		return True

	### Format matches

	try:
		post = {
			'teacher': matches[0].replace('\n',''),
			'type':	matches[1].capitalize(),
			'class': matches[2].replace('\n',''),
			'class_url': matches[3].replace('\n',''),
			'due': matches[4].replace('\n',''),
			'document': matches[5].replace('\n',''),
			'description': matches[6],
			'url': matches[7].replace('\n','')
		}
	except IndexError:
		print_warning('Insufficient matches in pattern.')
		print(matches)
		return False

	### Create embed

	embed = discord.Embed(
		color = 0x11aa77,
		title = f'📪 '+post['type']+(': '+post['document'] if post['document'] else ''),
		description = post['description'],
		url = post['url']
	).set_author(
		name = post['class'],
		url = post['class_url']
	).set_footer(
		text = post['teacher']
	)

	if post['due']:
		embed.add_field(
			name = 'Due',
			value = post['due'],
			inline = False
		)

	### Send embed

	[	
		print(
			' '.join([
				color_ribbon(str(id)) for id in [
					''.join([str(ord(c)).zfill(2)[:2] for c in str(embed)[-17:-1]]),
					message.id,
					message.guild.id,
					message.channel.id,
				]
			]),
			'\033[0mSent post to '
			f'\033[0mserver \033[1m{message.guild.name}',
			f'\033[0mchannel \033[1m{message.channel.name}\033[0m'
		)
		for message in await asyncio.gather(*[
			channel.send(embed=embed)
			for channel
			in channels
		])
	]
	
	cache.write(cache.read().union({email_id}))

	return True

try:
	dotenv.load_dotenv()
	discord_client = discord.Client()	
	discord_client.loop.create_task(background(discord_client))
	print_time('Bot ready.')

	discord_client.run(os.environ['discord_token'])
except KeyboardInterrupt:
	print_time('\033[91mStopping...')
	sys.exit(0)
except Exception as e:
	print_error(e)
	pass

