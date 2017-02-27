# regis

Docker Registry (API v2) Web UI.

Up to the moment the projects is a simple web UI for the Docker private registry.

It lets inspect images and tags. Also allows the logical deletion of tags.

## Screenshot

![Regis](/regis/static/img/regis.png)

## Usage

The project contains a Dockerfile to create an image.

### Building the image

    docker build -t regis .

### Running a container

Before you start the Regis container, you must have a Docker Registry v2 running on a Docker container:

    docker run -d -p 5000:5000 --restart always -e REGISTRY_STORAGE_DELETE_ENABLED=true --name registry registry:2.6

The REGISTRY_STORAGE_DELETE_ENABLED=true environment variable makes Docker Registry to honor the image deletion method.

Having a Registry then you could execute the following command to start a Regis container:

    docker run -d -p 4000:4000 --link <registry_name>:registry --name regis regis

The previous command is the simplest way to configure Regis. The link parameters do the trick you only have to complete with your <registry_name>.

If more complex configuration is needed you can mount the regis.cfg config file with the following command:

    docker run -d -p 4000:4000 -v /path/to/regis.cfg:/usr/src/app/regis.cfg --name regis regis

### Configuration file

The file is called **regis.cfg** and it contains the following properties to configure:

    # ip and port where the registry is listening
    [registry]
    host = registry
    port = 5000

    # username and password if configured, leave them empty if auth is not enabled.
    # ignore_ssl is to tell http client that don't check ssl certificate (not recommended for production!)
    [security]
    username =
    password =
    ignore_ssl = True

## Contact

This project is under development. Any problems don't doubt contacting me at [lea.beretta@gmail.com](mailto:lea.beretta@gmail.com).