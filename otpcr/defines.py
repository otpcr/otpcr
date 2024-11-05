# This file is placed in the Public Domain.
# pylint: disable=C,W0105,W0611,W0718


"defines"


TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%ss

[Install]
WantedBy=multi-user.target"""
