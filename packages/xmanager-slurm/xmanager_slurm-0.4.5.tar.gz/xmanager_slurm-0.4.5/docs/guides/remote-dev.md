# Developing on a Slurm Cluster


We'll outline the typical development flow for xm-slurm using vscode.
It's probably safe to assume most Slurm clusters don't have Docker installed
in order to perform the remote build.
You have two options:

1) Use the GCP cloud builder included in xm-slurm. This is quite involved and requires you set up
    your own GCP project.
2) Forward your local Docker socket to the remote machine via SSH so you can perform your Docker
    builds using the remote machine.
3) Use the Docker cloud builder on the Slurm Cluster.

(1) will be out of the scope of this guide, but we'll detail (2) and (3) in detail.
For both (2) and (3) we'll need to install the Docker client on the Slurm cluster.
Luckily, there are package binaries which should run on most clusters.

To install the Docker binaries you can,

```sh
mkdir -p $HOME/.local/bin $HOME/.docker/cli-plugins

export DOCKER_VERSION=25.0.2
export DOCKER_BUILDX_VERSION=0.12.1

curl -fsSL https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VERSION}.tgz | 
    tar zxvf - --strip 1 -C $HOME/.local/bin docker/docker
curl -fsSL "https://github.com/docker/buildx-desktop/releases/download/v${DOCKER_BUILDX_VERSION}-desktop.4/buildx-v${DOCKER_BUILDX_VERSION}-desktop.4.linux-amd64" -o $HOME/.docker/cli-plugins/docker-buildx

chmod +x $HOME/.local/bin/docker $HOME/.docker/cli-plugins/docker-buildx
```

You can check everything is working as expected by running: `docker buildx version`.


## Forwarding your Docker Socket

In order to forward your local Docker socket we'll need to modify our SSH config.
We'll give an example config but this will need to be modified for your use-case.
For your SSH host you'll need to `RemoteForward` the local socket at `/var/run/docker.sock`
to the remote host. In most cases forwarding the socket to a unix socket is desirable:

```ssh-config
Host my-slurm-cluster 
  RemoteForward $HOME/.docker/docker.sock  /var/run/docker.sock
```

If you can't do this then you can forward the socket to a remote port as such:
```ssh-config
Host my-slurm-cluster 
  RemoteForward 2375 /var/run/docker.sock
```

In either case on the remote machine you'll need to export `DOCKER_HOST` as either
`DOCKER_HOST=$HOME/.docker/docker.sock` or `DOCKER_HOST=tcp://127.0.0.1:2375`
depending on which of the above methods you used.


With this now complete you should be able to run `docker ps` on the remote host and it'll
return with any running containers on your local host.
Now when running xm-slurm it'll pick up the Docker client on the remote machine that'll build
your containers using the local host.


## Docker Cloud Builder

For the [Docker cloud builder](https://docs.docker.com/build/cloud/) you'll still need the docker & buildx
binary we installed above. You'll first need to set up your cloud builder (there is a free tier) at
[https://build.docker.com](https://build.docker.com).

Once this is complete you'll need to login to your docker account locally with `docker login`. Finally,
you'll need to create the cloud builder with:

```sh
docker buildx create --driver cloud ORG/BUILDER_NAME
```

where `ORG/BUILDER_NAME` comes from the setup process. Now you can set the cloud builder as your default builder with

```sh
docker buildx use cloud-ORG-BUILDER_NAME --global
```

Now xm-slurm will pick up your cloud builder and build all your images remotely using Docker's cloud build service.