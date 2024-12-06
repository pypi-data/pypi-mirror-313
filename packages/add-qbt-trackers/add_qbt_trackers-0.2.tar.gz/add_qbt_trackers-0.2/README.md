# add-qbt-trackers

This program simply adds known working trackers to a qBittorrent instance. The tracker URLs are taken from the following lists:

``` shell
https://newtrackon.com/api/stable
https://trackerslist.com/best.txt
https://trackerslist.com/http.txt
https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt
```

I've also included my own tracker URLs:

``` shell
http://tracker.hyperreal.coffee/announce
udp://tracker.hyperreal.coffee:1337
```

## Installation

``` shell
pipx install add-qbt-trackers --include-deps
```

## Usage

``` shell
add-qbt-trackers HOSTNAME USERNAME PASSWORD
add-qbt-trackers -h
```

Example:

``` shell
add-qbt-trackers "http://localhost:8080" "admin" "password"
```

> Note: Be sure to use quotes around the HOSTNAME, USERNAME, and PASSWORD so that the shell parses them correctly.
