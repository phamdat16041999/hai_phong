from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from .models import Album, Cart, Category, Music, Group_music
from django.db.models import F
from django.db import connection
# Create your views here.
from django.http import HttpResponse
def login(request):
	return render(request, 'login.html')
def index(request):
	if request.user.is_authenticated:
		return render(request, 'user/index.html', DataIndex())
	else:
		if request.method == 'POST':
		    username = request.POST.get('username','')
		    password = request.POST.get('password','')
		    user = authenticate(username=username, password=password)
		    if(user is not None):
		    	request.session.set_expiry(86400)
		    	auth_login(request, user)
		    	return redirect('/')
		    else:
		    	return render(request, 'login.html')
		else:
			return render(request, 'index.html', DataIndex())
def logout_view(request):
    logout(request)
    return render(request, 'index.html', DataIndex())
def ViewAlbum(request):
	album = Album.objects.filter(Public = True)
	AllAlbum = {'album' : album}
	return render(request, 'Album.html', AllAlbum)
def ViewMusic(request):
	music = Music.objects.all().order_by(F('id').asc())
	music = {'music' : music}
	return render(request, 'music.html', music)
def viewMusicInAlbum(request, id):
	music = []
	with connection.cursor() as cursor:
		cursor.execute(
			"SELECT user_music.Image, user_music.Name, user_music.Singer, user_music.Price, user_music.Like, user_music.Description, user_music.Music, user_music.id FROM user_music INNER JOIN user_group_music on user_group_music.Music_ID_id = user_music.id INNER JOIN user_album ON user_album.id = user_group_music.AlbumID_id WHERE user_album.id = '%s'" ,
			[id]
		)
		music.append(cursor.fetchall())
	Allmusic = {'music' : music[0]}
	return render(request, 'viewMusicInAlbum.html', Allmusic)
def LikeMusic(request, id):
	if request.user.is_authenticated:
		music = []
		with connection.cursor() as cursor:
			cursor.execute(
				"SELECT COUNT(user_rate_music.id) FROM user_rate_music WHERE user_rate_music.Music_ID_id = '%s' AND user_rate_music.UserID_id = '%s'" ,
				[id, request.user.id]
			)
			music.append(cursor.fetchall())
		if(len(music) > 0):
			Music.objects.Create(UserID = request.user.id, Music_ID = id)
			response = HttpResponse()
			response.writelines('Like')
			return response
		else:
			Music.objects.filter(UserID = request.user.id, Music_ID = id).delete()
			response = HttpResponse()
			response.writelines('Dislike')
			return response
	else:
		response = HttpResponse()
		response.writelines('login')
		return response








def DataIndex():
	newAlbum = Album.objects.all().order_by(F('id').asc())
	with connection.cursor() as cursor:
		cursor.execute(
			"SELECT user_album.id FROM user_album WHERE user_album.Public = 1 ORDER BY RAND() LIMIT 1" ,
		)
		randomAlbumID = cursor.fetchall()[0][0]
	randomAlbum = Album.objects.filter(id = randomAlbumID)
	music = []
	with connection.cursor() as cursor:
		cursor.execute(
			"SELECT * FROM user_music INNER JOIN user_group_music on user_music.id = user_group_music.Music_ID_id INNER JOIN user_album on user_album.id = user_group_music.AlbumID_id WHERE user_album.id = '%s' AND user_album.Public = 1" ,
			[randomAlbumID]
		)
		music.append(cursor.fetchall())
	Allmusic = {'newAlbum': newAlbum, 'music' : music[0], 'randomAlbum':randomAlbum}
	return Allmusic