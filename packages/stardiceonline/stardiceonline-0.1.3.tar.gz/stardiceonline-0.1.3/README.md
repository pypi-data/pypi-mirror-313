# stardiceonline

Data reduction package for the stardice experiment. The package features:
- An image processing library "imageproc"
- A batch processing tool to handle the data archive and its reduction
- An interactive web interface (build upon bokeh) to manage observations and data reduction

## Installation for developpers

We recommend installation within a virtual environment although this step is optionnal:

```bash
python3 -m venv online
source online/bin/activate
```

Afterward you can install the package from sources:
```
git clone git@gitlab.in2p3.fr:stardice/stardiceonline.git
cd stardiceonline
pip install -e .
```

### Activation of bash/zsh completion

Optionnally, you can activate bash completion making the use of the
stardiceonline main script much more convenient and less error
prone. The completion is provided by the argcomplete module which
supports natively bash and zsh. The following command will add the
necessary configuration lines to your environment:

```
activate-global-python-argcomplete
```

Of course you need completion to be active in your shell, for zsh on
macos the .zshrc files must contain:

```
autoload -Uz compinit
compinit
```

### Activation of astrometry.net

For the moment, the initial astrometric solution relies on
astrometry.net. You need a working installation with suitable index
files for that to work. For example in debian:

```
sudo apt install astrometry.net astrometry-data-tycho2
```

Given the depth of StarDICE images, there should be no points in
downloading more substantial catalogs. The astrometry is latter
refined using subsamples of gaia downloaded on demand.

## Setup

You need to provide a local storage point to reduce the StarDICE images. The provided path must be an existing directory on your local disk. If you want to dedicate a directory "ohparchive" in your home directory to this task enter: 
```
mkdir ~/ohp_archive
stardiceonline config archive.local ~/ohp_archive
```

You then need to setup ssh connection to the host machine, in order to
be able to retrieve the data and talk to the scheduler. The host
machine is only reachable through a proxy which you need to
specify. If you have key-based access to CC-IN2P3 compute farm, you
can use it for this purpose. The default proxy value is thus
cca.in2p3.fr. You also need to specify the username that you are using
to connect to the proxy.

```
stardiceonline config ssh.proxy cca.in2p3.fr
stardiceonline config ssh.proxyuser username
```

The tool relies on an ssh agent to manage connections. SSH keys to
access to the ssh proxy and the stardice host machine must be set up
approprietly.

The rest of the configuration should be correct by default. If you
want to see the rest of the configuration type:
```
stardiceonline config show
```

## Offline usage

Browse the archive. If ssh connections are setup properly the following command should display a list of the nights available in the archive, with nights already available in the local archive displayed in green:
```
stardiceonline archive list 
```

Retrieve one of the available nights of data:
```
stardiceonline archive retrieve 2024_07_11
```

Optionnally you can retrieve all available data (this is very long):
```
stardiceonline archive retrieve all
```

Process one night of data:
```
stardiceonline process 2024_07_11
```

Stop the processing server:
```
stardiceonline process stop
```

## Online usage

Start the web interface to browse the data and monitor the data taking:
```
stardiceonline webapp serve
```
The default port is 5006
Watch it in your browser at localhost:5006/online

Start the automatic processing of incoming live data:
```
stardiceonline process live
```

Once done you can stop everything with:
```
stardiceonline process stop
```
and Ctrl-C the server of the web application

## Support

Submit issues and ideas to the issue page:

https://gitlab.in2p3.fr/stardice/stardiceonline/-/issues

## Roadmap

Known bugs:
- [ ] Led catalog is not properly presented (because it lacks astrometry...)
- [ ] Display of Skylevels and other sensors no longer work

In development:
- [ ] Presentation of meteo station data in the monitoring page of the web interface
- [ ] Target selection page
- [ ] Focus adjustment
- [ ] Live reduction of spectra (big chunk)


## Authors and acknowledgment

StarDICEonline is currently developed by Marc Betoule and Sébastien
Bongard. New contributors are welcome.

## License

StarDICEonline is licensed under the terms of GPL V2

