# Flask Demo

## Requires
- SQLAlchemy
- Flask
- Flask-SQLAlchemy
- Flask-Cors


## TailwindCSS Notes

To build a new version of the CSS use:

```shell script
npx tailwindcss-cli@latest build ./static/src/styles.css -o ./static/css/styles.css
```

## Debugging Shell/Batch Files

The client will run on port 5000 and the server on port 5050.

### Linux systems
Enable execute for the user:
```shell script
chmod u+x client.sh server.sh
```
You will require TWO shells to run the server and client on one system

To run the Server file use:
```shell script
./server.sh
```

To run the Client file use:
```shell script
./client.sh
```

### Windows systems

You will require TWO shells to run the server and client on one system

To run the Server file use:
```shell script
server
```

To run the Client file use:
```shell script
client
```


## Other General Items for Linux CLI

| Command/Keys      | Explanation                                      |
|-------------------|--------------------------------------------------|
| `CTRL`+`Z`        | pauses the current executing application         |
| `CTRL`+`C`        | stops the current executing application          |
| `jobs`            | lists the jobs / apps that are 'paused'          |
| `fg x`            | brings the job number x into the foreground, eg `fg 1` |
