# Slurm in Docker

This is a test cluster that can be run in Docker.
For example, to build and launch the cluster run:
```sh
docker-compose up --build
```

Then you'll be able to ssh into the login node via,
```sh
ssh -F ssh_config xm-slurm
```

Some parts of this setup (mainly `docker-entrypoint.sh` and using `gosu`)
was taken from: [https://github.com/giovtorres/slurm-docker-cluster](https://github.com/giovtorres/slurm-docker-cluster)