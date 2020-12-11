# MocaCommands
Run commands on the server side and get the response via HTTP protocol.
MocaCommands based on the [Sanic](https://github.com/huge-success/sanic) web framework, Sanic is a higher performance web framework.

### Requirements
- python3.7 or higher (recommended python3.8)
- Linux or macOS (Don't support windows)

### Install
```
git clone https://github.com/el-ideal-ideas/MocaCommands.git
cd MocaCommands
python3 -m pip install --upgrade -r requirements.txt
```

### HTTP Usage
You can use this system via HTTP or HTTPS protocol.
If you want to send some parameter such as api-key.
You can use `URL parameter` or `Form parameter` or `json body`

- `http://<your-ip>:<your-port>/moca-commands/commands/run`
    - This URI can executed registered commands.
    - parameters
        - api_key (string | max-length: 1024 | required) your API key.
        - cmd_name (string | max-length: 64 | required) the name of the command.
        - password (string | max-length: 1024 | optional) the password of this command.
        - root_pass (string | max-length: 1024 | optional) if you have a valid root password, you can run any command without command-pass.
        - arguments (string | max-length: 8192 | optional) you can pass any arguments as string to the command. (can't contains single-quotes, backslash, semicolon)
        
        
- `http://<your-ip>:<your-port>/moca-commands/dynamic/py/<filename>`
    - This UIR can run files in the `dynamic_scripts/python` as a dynamic route.
    - When you changed the source code of these files, the file will be reload automatically.
    - The usage please look the sample files under the dynamic_scripts directory.
    

- `http://<your-ip>:<your-port>/moca-commands/dynamic/js/<filename>`
    - This UIR can run files in the `dynamic_scripts/javascript` as a dynamic route.
    - When you changed the source code of these files, the file will be reload automatically.
    - The usage please look the sample files under the dynamic_scripts directory.   
 
        
- `http://<your-ip>:<your-port>/moca-commands/commands/run-any`
    - This URI can executed any shell commands (required root password).
    - If you think this URI is dangerous you can disable this URI in the API-KEY configs.
    - parameters
        - api_key (string | max-length: 1024 | required) your API key.
        - root_pass (string | max-length: 1024 | required) the root password of MocaCommands.
        - command (string | max-length: 16384 | required) the shell command you want to execute.
        
        
- `http://<your-ip>:<your-port>/moca-commands/commands/run-any-py`
    - This URI can executed any python3 code (required root password).
    - If you think this URI is dangerous you can disable this URI in the API-KEY configs.
    - parameters
        - api_key (string | max-length: 1024 | required) your API key.
        - root_pass (string | max-length: 1024 | required) the root password of MocaCommands.
        - code (string | max-length: 16384 | required) the python3 code you want to execute.
        

- `http://<your-ip>:<your-port>/status`
    - This URI can checking the server status.
    - parameter
        - don't need any parameters, don't need api-key.


### Console Usage
- `python3 moca.py version`
    - Show the version of this system.
- `python3 moca.py update`
    - Update modules via pip
- `python3 moca.py update-system`
    - Get the latest version of code from github and update system.
- `python3 moca.py reset-system`
    - Reset all data and update system.
- `python3 moca.py run`
    - Run this system.
- `python3 moca.py start`
    - Run this system on background.
- `python3 moca.py stop`
    - Stop background process.
- `python3 moca.py restart`
    - Restart background process.
- `python3 moca.py status`
    - Show the status of this system.
- `python3 moca.py turn-on`
    - Stop maintenance mode.
- `python3 moca.py turn-off`
    - Start maintenance mode.
- `python3 moca.py clear-logs`
    - Clear logs
- `python3 moca.py run-cmd <command name>`
    - Run registered commands from console.

### For example
All commands will be saved to `commands/commands.json`
If you want to add a new command just append it to `commands/commands.json`

#### example1
```
"hello": {
    "status": true,
    "cmd": "echo 'Hello World!'",
    "pass": null,
    "ip": ["127.0.0.1"],
    "rate": "64 per second",
    "rate_per_ip": "1 per second"
}
```
When you access to `http://127.0.0.1:5990/moca-commands/commands/run?cmd_name=hello&api_key=mochimochi`

The response will be `Hello World!`

#### example2
```
"hello-py": {
    "status": true,
    "cmd_path": "hello.py",
    "pass": null,
    "ip": ["127.0.0.1"],
    "rate": "64 per second",
    "rate_per_ip": "1 per second"
}
```
- hello.py
```python
#!/usr/bin/env python3

# Please make sure this file can be executed.
# chmod +x hello.py

print('Hello World!!')

```

When you access to `http://127.0.0.1:5990/moca-commands/commands/run?cmd_name=hello-py&api_key=mochimochi`

System will execute hello.py and return the output as response.

#### example3
```
"show-my-request": {
    "status": true,
    "cmd": "[moca]show_my_request",
    "pass": null,
    "ip": "*",
    "rate": "64 per second",
    "rate_per_ip": "1 per second"
}
```

When you access to `http://127.0.0.1:5990/moca-commands/commands/run?cmd_name=show-my-request&api_key=mochimochi`

System will call `show_my_request` function and return the response.

### Command format
```
"name of this command": {
    "status": true or false  // when this value is false, you can't use this command via HTTP.
    "cmd": string // The shell command to execute. If this value is starts with `[moca]` system will call the function.
    "cmd_path": string  // The path to the executable file, If this value is not starts with `/` the path will be starts from the commands folder.
    "pass": null or a string // If this value is not null, when you run this command you should send this password from the client.
    "ip": * or a list of string  // If this value is * this command can be used from anywhere, If this value is a list this command can be used from registered IPs.
    "rate": string  // the rate limit of this command.
    "rate_per_ip": string  // the rate limit of this command per ip address.
}
```
#### After your changed `commands/commands.json` will be reload automatically.

### API-KEY format
```
{
    "key": string  // The value of api-key.
    "status": true or false  // If the value is false, This api-key will be blocked.
    "allowed_path": a list of string  // A list of allowed paths
    "required": {
      "headers": dict,  // When you use this api-key, All required must contains these headers.
      "args": dict  // When you use this api-key, All required must contains these arguments.
    },
    "ip": * or a list of string  // This api-key can be used from these ip addresses.
    "rate": string  // The rate limit of this api-key.
    "delay": 0  // If this value is not 0, the response will be waiting `delay` seconds.
    "info": string // You can write any information.
}
```

#### After your changed `configs/api_key.json` will be reload automatically.

### server.json
```
{
  "address": {
    "host": "0.0.0.0",  // The host address of your server.
    "port": 5990,  // The port number of your server.
    "unix": null,  // Unix socket
    "use_ipv6": false  // If you want to use IPv6, Please set a true.
  },
  "ssl": {  // HTTPS configuration.
    "cert": null,
    "key": null
  },
  "debug": false,  // Show debug information.
  "access_log": false,  // Save access log.
  "log_level": 20,  // The logging level of sanic server.
  "workers": 0,  // the number of workers, If this value is 0, the number of workers will be same as the number of cpu cores.
  "auto_reload": false,  // when you changed the source code, reload sanic server.
  "backlog": 100,  // a number of unaccepted connections that the system will allow before refusing new connections.
  "headers": {},  // You can set some headers to all response.
  "access_control_allowed_credentials": true,
  "access_control_allowed_origins": ["https://localhost", "http://localhost", "https://127.0.0.1", "http://127.0.0.1"],
  "access_control_allowed_methods": ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
  "access_control_allow_headers": "*",
  "access_control_max_age": 600,
  "access_control_expose_headers": "*",
  "stream_large_files": false,  // a parameter of sanic static route.
  "rate_limiter_redis_storage": null,  // you can use redis to save the rate limiting data. (When you are using multiple workers, in-memory storage can't share between workers.)
  "pyjs_secret": null, // AES encryption, If the request contains Moca-Encryption header, Middleware will try decrypt the request body.
}
```

### system.json
```
{
  "maintenance_mode": false,  // If the value is true, all requests will get 503 response.
  "maintenance_mode_whitelist": ["127.0.0.1"],  // a ip whitelist of maintenance mode.
  "referer": {  // allowed referer
    "allowed_referer": [
      "https:\/\/localhost",
      "https:\/\/127.0.0.1",
      "http:\/\/localhost",
      "http:\/\/127.0.0.1"
    ],
    "force": false  // If this value is true, all requests must have referer header.
  },
  "force_headers": {  // All requests must have these headers.

  },
  "dos_detect": 5000,  // If the access rate is higher than `dos_detect/seconds`, the target ip will be blocked.
  "root_pass": "mochimochi"  // The root password, If valid root password is in your request, You can use all commands without command-pass checking.
}
```
#### After your changed `configs/system.json` will be reload automatically.

### Sanic server configuration.

For more details, you can see https://sanic.readthedocs.io/en/latest/sanic/config.html

| Variable | Default | Description |
| -------- | ------- | ----------- |
| REQUEST_MAX_SIZE | 100000000 | How big a request may be (bytes) |
| REQUEST_BUFFER_QUEUE_SIZE | 100 | Request streaming buffer queue size |
| REQUEST_TIMEOUT | 60 | How long a request can take to arrive (sec) | 
| RESPONSE_TIMEOUT | 60 | How long a response can take to process (sec) |
| KEEP_ALIVE | True | Disables keep-alive when False |
| KEEP_ALIVE_TIMEOUT | 5 | How long to hold a TCP connection open (sec)|
| WEBSOCKET_MAX_SIZE | 2^20 | Maximum size for incoming messages (bytes)|
| WEBSOCKET_MAX_QUEUE | 32 | Maximum length of the queue that holds incoming messages |
| WEBSOCKET_READ_LIMIT | 2^16 | High-water limit of the buffer for incoming bytes |
| WEBSOCKET_WRITE_LIMIT | 2^16 | High-water limit of the buffer for outgoing bytes |
| WEBSOCKET_PING_INTERVAL | 20 | A Ping frame is sent every ping_interval seconds. |
| WEBSOCKET_PING_TIMEOUT | 20 | Connection is closed when Pong is not received after ping_timeout seconds |
| GRACEFUL_SHUTDOWN_TIMEOUT | 15.0 | How long to wait to force close non-idle connection (sec) |
| ACCESS_LOG | True | Disable or enable access log |
| FORWARDED_SECRET | None | Used to securely identify a specific proxy server (see below) |
| PROXIES_COUNT | None | The number of proxy servers in front of the app (e.g. nginx; see below) |
| FORWARDED_FOR_HEADER | "X-Forwarded-For" | The name of "X-Forwarded-For" HTTP header that contains client and proxy ip |
| REAL_IP_HEADER | None | The name of “X-Real-IP” HTTP header that contains real client ip |

#### For reference:
- Apache httpd server default keepalive timeout = 5 seconds
- Nginx server default keepalive timeout = 75 seconds
- Nginx performance tuning guidelines uses keepalive = 15 seconds
- IE (5-9) client hard keepalive limit = 60 seconds
- Firefox client hard keepalive limit = 115 seconds
- Opera 11 client hard keepalive limit = 120 seconds
- Chrome 13+ client keepalive limit > 300+ seconds

### static directory
The files under the static directory, You can access from http://127.0.0.1:5990/moca-commands/static/  
You can put any static files under this directory.

### storage directory
MocaCommands will don't use this directory, you can use it for your own commands.

### startup, atexit
`startup.py` `startup.sh` will be executed before the api-server started.
`atexit.py` `atexit.sh` will be executed after the api-server stopped.
You can add any code to these files.

### Update
If you want to update your MocaCommands system.  
Just download the latest source code from this repository, and replace the src directory.  
(Maybe you need to check the latest configs format)

### License (MIT)
MIT License

Copyright 2020.1.17 <el.ideal-ideas: https://www.el-ideal-ideas.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
