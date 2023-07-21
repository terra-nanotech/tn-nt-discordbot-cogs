# Terra Nanotech Discordbot Cogs

A collection of cogs for
[AA-Discordbot](https://github.com/pvyParts/allianceauth-discordbot)


---

<!-- TOC -->
* [Terra Nanotech Discordbot Cogs](#terra-nanotech-discordbot-cogs)
  * [Important Information](#important-information)
  * [Install](#install)
<!-- TOC -->

---


## Important Information

These Discord bot COGs are specially tailored for the corporation Terra Nanotech.
They COGs of apps we use, so they fit our needs.

> **Note**
>
> If you install this app, you need to be aware that there will be
no support for any kind of issues you might encounter, and you have to figure it out
on your own.

## Install

```shell
pip install tnnt-discordbot-cogs
```

In `local.py` right after `INSTALLED_APPS`:

```python
# Terra Nanotech Discordbot Cogs
INSTALLED_APPS += ["eveuniverse", "tnnt_discordbot_cogs"]
```

Run DB migrations and restart supervisor.
