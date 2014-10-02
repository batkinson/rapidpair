# Rapid Pair

A simple flask application for creating randomized pairs of active hacker school
batch members. It was initially intended to make the process of finding a
pairing partner a little less socially awkward. However, in the process of
developing the initial prototype I discovered that despite having considerable
experience developing servlet-based web applications, I was somewhat stumped by
the simple task of safely using a refresh token for a user without server-side
sessions.

Now that hacker school is essentially building/has built their own solution for
this, I doubt this will ever be fully developed. However, it provided an
excellent motif for digging into the internals of Flask and Werkzeug and
learning the assumptions that web application frameworks make in the Python tool
chain.

![Front Page Screenshot](screenshots/front-page.png?raw=true)
![Match Page Screenshot](screenshots/match-page.png?raw=true)

## Requirements

In the unlikely event that you want to (and are capable of) running this, you
will need:

   * A working Python 3 environment

## Setup

To run the program, first install the dependencies. This is as simple as running
the following:

```
pip install -r requirements.txt
```

You then need to create an authorized oauth application through your hacker
school account settings. Take the application id and secret and create a bash
script named keys.sh (it's already ignored in the git repo so you don't
accidentally commit it):

```
CONSUMER_KEY=<application-id from hackerschool.com>
CONSUMER_SECRET=<application-secret from hackerschool.com>
export CONSUMER_KEY CONSUMER_SECRET
```

## Running

Starting the application is as simple as running:

```
cd $RAPIDPAIR_HOME
source ./keys.sh
./app.py
```

By default, the application starts on tcp port 5000. Note that you will have to
access the application by your machine's remotely accessible hostname for the
oauth exchange with hacker school to work. This means that rather than using
http://localhost:5000, you need to use something like http://10.X.X.X:5000,
where 10.X.X.X is the public ip of the machine running rapid pair.

