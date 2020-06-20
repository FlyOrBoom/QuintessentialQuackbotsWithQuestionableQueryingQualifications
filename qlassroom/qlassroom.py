from print_fancy import *
print_time('Starting Qlassroom...')
import base64, re, random, os, sys, time, asyncio, socket
import dotenv, config, cache
import gmail, discord
print_time('Imported everything.')

async def background(discord_client):

	await discord_client.wait_until_ready()
	print_time('\033[92mLogged in as',str(discord_client.user))
	while True:
		last_refresh = time.time()
		await handler()
		await asyncio.sleep(
			 last_refresh - time.time() + config.read('refresh interval')
		)

async def handler():	

	email_ids = gmail.fetch_email_ids()

	print_time(
		'\033[93m'+
		str(len(email_ids)),
		'\033[94mnew emails'
	)

	if not email_ids: return True

	### Get channels	
	
	channels = {
		discord_client.get_channel(int(channel_id))
		for channel_id
		in config.read('channel ids')
		if channel_id
	}

	if not channels:
		print_warning('No channels specified.')
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
		return False

	### Decode email
	
	try:
		email_text = base64.urlsafe_b64decode(
			email_b64
		).decode('utf-8').replace('\r','')
	except AttributeError:
		print_warning(f'Cannot decode email {email_id}.')
		return False

	### Find matches in email body
	
	try:
		matches = re.search(
			config.read('email pattern'),
			email_text
		).groups()
	except AttributeError:
		print_warning(f'Email {email_id} does not match pattern.')
		return False

	### Format matches

	try:
		post = {
			'teacher': matches[0],
			'type':	matches[1].capitalize(),
			'class': matches[2],
			'class_url': matches[3],
			'due': matches[4],
			'document': matches[5],
			'description': matches[6].replace('\n',' '),
			'url': matches[7]
		}
	except IndexError:
		print_warning('Insufficient matches in pattern.')
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
				color_ribbon(id) for id in(
					''.join([str(ord(c)).zfill(2)[:2] for c in str(embed)[-17:-1]]),
					message.id,
					message.guild.id,
					message.channel.id,
				)
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
	
	cache.write(cache.read().union(email_id))

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

