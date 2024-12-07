# DCI UMB

DCI UMB is a tool that listen on an amqps broker, filter on a specific topic and propagate any event via http post request.

## TLDR

```console
$ sudo yum -y install https://packages.distributed-ci.io/dci-release.el7.noarch.rpm
$ sudo yum -y install dci-umb
$ dci-umb \
  --key ./broker.key \
  --crt ./broker.crt \
  --ca ./broker.ca \
  --broker amqps://example.org:5671 \
  --source topic://VirtualTopic.eng \
  --destination http://localhost:5000/events
```

## Run as a service

If you want to run dci-umb as a systemd service, you can edit `/etc/dci-umb/config` file and modify the config.
Then you can run `systemctl start dci-umb`

## Example

Create a python virtual environment

    python3 -m venv venv
    source venv/bin/activate

Install dependencies

    pip install -r sandbox/requirements.txt
    pip install -r requirements.txt

Start the sandbox server:

    python sandbox/server.py

In another terminal start dci-umb with parameters

    source venv/bin/activate
    PYTHONPATH=. python dci_umb/main.py \
        --key ./broker.key \
        --crt ./broker.crt \
        --ca ./broker.ca \
        --broker amqps://example.org:5671 \
        --source topic://VirtualTopic.eng \
        --destination http://localhost:5000/events
