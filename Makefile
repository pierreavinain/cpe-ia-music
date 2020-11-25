usage:
	# usage: make deploy

deploy:
	heroku container:login
	heroku container:push --app=cpe-ia-music web
	heroku container:release --app=cpe-ia-music web

logs:
	heroku logs --app=cpe-ia-music --tail