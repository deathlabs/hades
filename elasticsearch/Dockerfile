# Set Dockerfile metadata for the first build.
FROM elasticsearch:8.12.0 AS first_build
LABEL image.authors="Victor Fernandez III, @cyberphor" 

# Copy Elasticsearch configuration files.
COPY app/elasticsearch.yml config/elasticsearch.yml

# Expose the TCP port used by Elasticsearch.
EXPOSE 9200

# Switch to a non-root user.
USER elasticsearch