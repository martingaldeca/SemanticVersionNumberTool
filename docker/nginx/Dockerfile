# Get the last version of nginx
FROM nginx

# Clean the default config and set a custom config
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf-final /etc/nginx/conf.d
RUN mv /etc/nginx/conf.d/nginx.conf-final /etc/nginx/conf.d/nginx.conf

# Add extra configs for the project
#COPY nginx.conf /etc/nginx/sites-enabled/
