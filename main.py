#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import cgi, cgitb
import urllib2
import json
import os

ip = os.environ['REMOTE_ADDR']
cheker = ip.split('.')
if cheker[0] == '10':
	server = 'http://10.1.1.21/~chyngyz'
else:
	server = 'http://212.112.98.181:22080/~chyngyz'

print "Content-type:text/html\r\n\r\n"
beg = '''<html>
<head>
<meta charset=utf-8 />
<title>Kraken Music App</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link href="%s/skin/blue.monday/jplayer.blue.monday.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
<script type="text/javascript" src="%s/js/jquery.jplayer.min.js"></script>
<script type="text/javascript" src="%s/js/jplayer.playlist.min.js"></script>
<script type="text/javascript">
//<![CDATA[
$(document).ready(function(){

	new jPlayerPlaylist({
		jPlayer: "#jquery_jplayer_1",
		cssSelectorAncestor: "#jp_container_1"
	}, [''' % (server, server, server)
center = '''], {
		swfPath: "js",
		supplied: "oga, mp3",
		wmode: "window",
		smoothPlayBar: true,
		keyEnabled: true
	});
});
//]]>
</script>
</head>
<body>
	<center>'''

end = '''<div class = "form">
	<form>
		Search: <input class="form-field" type="text" name="search"><br>
		<input class="button" type="submit" value="Submit"></form>
	</div>
		<div id="jquery_jplayer_1" class="jp-jplayer"></div>

		<div id="jp_container_1" class="jp-audio">
			<div class="jp-type-playlist">
				<div class="jp-gui jp-interface">
					<ul class="jp-controls">
						<li><a href="javascript:;" class="jp-previous" tabindex="1">previous</a></li>
						<li><a href="javascript:;" class="jp-play" tabindex="1">play</a></li>
						<li><a href="javascript:;" class="jp-pause" tabindex="1">pause</a></li>
						<li><a href="javascript:;" class="jp-next" tabindex="1">next</a></li>
						<li><a href="javascript:;" class="jp-stop" tabindex="1">stop</a></li>
						<li><a href="javascript:;" class="jp-mute" tabindex="1" title="mute">mute</a></li>
						<li><a href="javascript:;" class="jp-unmute" tabindex="1" title="unmute">unmute</a></li>
						<li><a href="javascript:;" class="jp-volume-max" tabindex="1" title="max volume">max volume</a></li>
					</ul>
					<div class="jp-progress">
						<div class="jp-seek-bar">
							<div class="jp-play-bar"></div>
						</div>
					</div>
					<div class="jp-volume-bar">
						<div class="jp-volume-bar-value"></div>
					</div>
					<div class="jp-time-holder">
						<div class="jp-current-time"></div>
						<div class="jp-duration"></div>
					</div>
					<ul class="jp-toggles">
						<li><a href="javascript:;" class="jp-shuffle" tabindex="1" title="shuffle">shuffle</a></li>
						<li><a href="javascript:;" class="jp-shuffle-off" tabindex="1" title="shuffle off">shuffle off</a></li>
						<li><a href="javascript:;" class="jp-repeat" tabindex="1" title="repeat">repeat</a></li>
						<li><a href="javascript:;" class="jp-repeat-off" tabindex="1" title="repeat off">repeat off</a></li>
					</ul>
				</div>
				<div class="jp-playlist">
					<ul>
						<li></li>
					</ul>
				</div>
			</div>
		</div>
</center>
</body>
</html>'''

def search(query, num):
	query = query.replace(" ","%20")
	search_url = 'http://ex.fm/api/v3/song/search/%s?start=0&results=%s' %(query , str(num))
	html = urllib2.urlopen(search_url)
	songs = html.read()
	songs = json.loads(songs)
	result = {}
	count = 1
	for i in songs['songs']:
		result[count] = {}
		result[count]['title'] = i['title']
		result[count]['artist'] = i['artist']
		result[count]['thumbnail'] = i['image']['large']
		result[count]['url'] = i['url'] 
		count += 1
	return result

form = cgi.FieldStorage()
query = form.getvalue('search')
if query == None:
	query='zomboy'

num = '20'
results = search(query,num)
schet = int(len(results))

print beg
try:
	for x in range(1,schet+1):
		url = results[x]['url']
		title = results[x]['title']
		artist = results[x]['artist']
		check = url.split('/')
		if check[2] == 'api.soundcloud.com':
			url = url+'?client_id=0557caec313ae36a9d6a21841293da11'
		print'{'
		print '	title:"%s - %s",' % (artist, title)
		print '	mp3:"%s"' % url
		if x < schet:
			print '},'
		else:
			print '}'
	print center
	print '<h2><a href="%s/cgi-bin/last.py?artist=%s">Get same artists</a></h2>' % (server, query)
	print end
except Exception, e:
	print e
