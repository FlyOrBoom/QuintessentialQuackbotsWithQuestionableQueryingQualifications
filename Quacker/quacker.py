from dotenv import load_dotenv
load_dotenv()

import os
import discord
from random import randint, random
import asyncio
import json

client = discord.Client()
latest_message_id = {}
dict = [
	"abstraction","accessibility","accessibilitytree","aom","adobeflash","ajax","algorithm","alignmentcontainer","alignmentsubject","alpha","alphachannel","alpn","api","applesafari","applicationcontext","argument","aria","arpa","arpanet","array","ascii","asynchronous","atag","attribute","bandwidth","base64","baseline","beacon","béziercurve","bidi","bigint","blink","block","css","block","scripting","blockciphermodeofoperation","boolean","boot2gecko","bootstrap","boundingbox","breadcrumb","brotli","browser","browsingcontext","buffer","cache","cacheable","caldav","callstack","callbackfunction","canonicalorder","canvas","cardsorting","carddav","caret","cdn","certificateauthority","certified","challengeresponseauthentication","character","characterencoding","characterset","chrome","cia","cipher","ciphersuite","ciphertext","class","clienthints","closure","cms","codesplitting","codec","compile","compiletime","computerprogramming","conditional","constant","constructor","continuousmedia","controlflow","cookie","copyleft","cors","corssafelistedrequestheader","corssafelistedresponseheader","crawler","crlf","crossaxis","crosssitescripting","crud","cryptanalysis","cryptographichashfunction","cryptography","csp","csrf","css","cssobjectmodel","cssom","csspixel","csspreprocessor","datastructure","decryption","denialofservice","descriptor","css","deserialization","developertools","dhtml","digest","digitalcertificate","distributeddenialofservice","dmz","dns","doctype","documentdirective","documentenvironment","dom","documentobjectmodel","domain","domainname","domainsharding","dominator","dosattack","dtls","datagramtransportlayersecurity","dtmf","dualtonemultifrequencysignaling","dynamicprogramminglanguage","dynamictyping","ecma","ecmascript","effectiveconnectiontype","element","emptyelement","encapsulation","encryption","endianness","engine","entity","entityheader","event","exception","expando","fallbackalignment","falsy","favicon","fetchdirective","fetchmetadatarequestheader","firefoxos","firewall","firstcontentfulpaint","firstcpuidle","firstinputdelay","firstinteractive","firstmeaningfulpaint","firstpaint","firstclassfunction","flex","flexcontainer","flexitem","flexbox","forbiddenheadername","forbiddenresponseheadername","fork","fragmentainer","framerate","fps","ftp","ftu","function","fuzztesting","gaia","garbagecollection","gecko","generalheader","gif","gij","git","globalobject","globalscope","globalvariable","glyph","gonk","googlechrome","gpl","gpu","gracefuldegradation","grid","gridareas","gridaxis","gridcell","gridcolumn","gridcontainer","gridlines","gridrow","gridtracks","guard","gutters","gzipcompression","hash","head","highlevelprogramminglanguage","hmac","hoisting","host","hotlink","houdini","hpkp","hsts","html","html5","http","httpheader","http/2","http/3","https","hyperlink","hypertext","i18n","iana","icann","ice","ide","idempotent","identifier","idl","ietf","iife","imap","immutable","index","indexeddb","informationarchitecture","inheritance","inputmethodeditor","instance","internationalization","internet","intrinsicsize","ipaddress","ipv4","ipv6","irc","iso","isp","itu","jank","java","javascript","jpeg","jquery","json","key","keyword","latency","layoutviewport","lazyload","lgpl","ligature","localscope","localvariable","locale","localization","longtask","loop","losslesscompression","lossycompression","ltr","lefttoright","mainaxis","mainthread","markup","mathml","media","media","audiovisualpresentation","media","css","metadata","method","microsoftedge","microsoftinternetexplorer","middleware","mime","mimetype","minification","mitm","mixin","mobilefirst","modem","modernwebapps","modularity","mozillafirefox","mutable","mvc","namespace","nan","nat","native","navigationdirective","netscapenavigator","networkthrottling","nntp","node","node","dom","node","networking","node.js","nonnormative","normative","null","nullishvalue","number","object","objectreference","oop","opengl","openssl","operabrowser","operand","operator","origin","ota","owasp","p2p","pac","packet","pageloadtime","pageprediction","parameter","parentobject","parse","parser","pdf","perceivedperformance","percentencoding","php","pixel","placeholdernames","plaintext","png","polyfill","polymorphism","pop3","port","prefetch","preflightrequest","prerender","presto","primitive","privileged","privilegedcode","progressiveenhancement","progressivewebapps","promise","property","property","css","property","javascript","protocol","prototype","prototypebasedprogramming","proxyserver","pseudoclass","pseudoelement","pseudocode","publickeycryptography","python","qualityvalues","quaternion","quic","rail","randomnumbergenerator","rasterimage","rdf","realusermonitoring","rum","recursion","reference","reflow","regularexpression","renderingengine","repo","reportingdirective","requestheader","resourcetiming","responseheader","responsivewebdesign","rest","rgb","ril","robots.txt","roundtriptime","rtt","routers","rss","rtcp","rtpcontrolprotocol","rtf","rtl","righttoleft","rtp","realtimetransportprotocol)andsrtp(securertp","rtsp:realtimestreamingprotocol","ruby","safe","sameoriginpolicy","scm","scope","screenreader","scriptsupportingelement","scrollcontainer","scrollport","sctp","sdp","searchengine","secondleveldomain","securesocketslayer","ssl","selector","css","selfexecutinganonymousfunction","semantics","seo","serialization","server","servertiming","sessionhijacking","sgml","shadowtree","shim","signature","signature","functions","signature","security","simd","simpleheader","simpleresponseheader","sisd","site","sitemap","sld","sloppymode","slug","smoketest","smpte","societyofmotionpictureandtelevisionengineers","smtp","snappositions","soap","spa","singlepageapplication","specification","speculativeparsing","speedindex","sql","sqlinjection","sri","stackingcontext","statemachine","statement","staticmethod","statictyping","strictmode","string","stun","styleorigin","stylesheet","svg","svn","symbol","symmetrickeycryptography","synchronous","syntax","syntaxerror","syntheticmonitoring","tag","tcp","tcphandshake","tcpslowstart","telnet","texel","thread","threejs","timetofirstbyte","timetointeractive","tld","tofu","transmissioncontrolprotocol","tcp","transportlayersecurity","tls","treeshaking","trident","truthy","ttl","turn","type","typecoercion","typeconversion","udp","userdatagramprotocol","ui","undefined","unicode","uri","url","urn","usenet","useragent","utf8","ux","validator","value","variable","vendorprefix","viewport","visualviewport","voip","w3c","wai","wcag","webperformance","webserver","webstandards","webdav","webextensions","webgl","webidl","webkit","webm","webp","webrtc","websockets","webvtt","whatwg","whitespace","worldwideweb","wrapper","xforms","xhr","xmlhttprequest","xhtml","xinclude","xlink","xml","xpath","xquery","xslt","404","502"
]


@client.event
async def on_ready():
	print('Logged in as ' + str(client.user))

@client.event
async def on_message(message):
	channel = message.channel
	if (
		message.author != client.user
		and any(trigger in channel.name for trigger in ['duck','bot','spam'])
	):
		latest_message_id[str(channel.id)] = message.id
		await asyncio.sleep(random()*4) #Pause and ponder
		async with channel.typing():
			for i in range(1,8):
				await asyncio.sleep(random())
				cancel = latest_message_id[str(channel.id)] != message.id #Stops typing if there's a new message
				if cancel: break
			if not cancel:
				await channel.send(
					( 'quack' if randint(0,36) else 'honk' ) * randint(1,5)
					+ ( dict[randint(0,len(dict))] if randint(0,3) else '')
					+ ( '!' if randint(0,1) else '?' )
				)

client.run(os.environ['TOKEN'])
