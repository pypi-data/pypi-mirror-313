# `stevent-management`

**Usage**:

```console
$ stevent-management [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `add_event`: Add an event
* `update_event`: Make changes to an existing event
* `delete_event`
* `add_profile` : Add a guest
* `list_profiles`: list all guest profiles created by event manager
* `get_profile`
* `update_profile`
* `delete_profile`
* `delete_all_profiles`
* `search_profiles`
* `export_profiles`
* `register_manager`: Register a new event manager.
* `login_manager`: Authenticate an event manager.
* `delete_manager`: Delete a specific event manager by username.
* `delete_all_managers`: Delete all event managers from the database.


>Note: TEXT after options below, are the input values we want to send along with the options. Where options are not included with
command, you will be prompted.

## `stevent-management add_event`

**Usage**:

```console
$ stevent-management add_event [OPTIONS]
$ stevent-management add_event
```

**Options**:

* `--event-name TEXT`: [required]
* `--description TEXT`: [required]
* `--event-date TEXT`: [required]
* `--age-range TEXT`: [required]
* `--token TEXT`: [required]
* `--help`: Show this message and exit.

## `stevent-management update_event`

**Usage**:

```console
$ stevent-management update_event [OPTIONS]
```

**Options**:

* `--event-name TEXT`: [required]
* `--description TEXT`
* `--event-date TEXT`
* `--age-range TEXT`
* `--token TEXT`
* `--help`: Show this message and exit.

## `stevent-management delete_event`

**Usage**:

```console
$ stevent-management delete_event [OPTIONS]
```

**Options**:

* `--event-name TEXT`: [required]
* `--token TEXT`: [required]
* `--help`: Show this message and exit.

## `stevent-management add_profile`

**Usage**:

```console
$ stevent-management add_profile [OPTIONS]
```

**Options**:

* `--username TEXT`: [required]
* `--age INTEGER`: [required]
* `--ticket TEXT`: [required]
* `--gender TEXT`: [required]
* `--event-name TEXT`: [required]
* `--token TEXT`: [required]
* `--help`: Show this message and exit.

## `stevent-management list_profiles`

**Usage**:

```console
$ stevent-management list_profiles [OPTIONS]
```

**Options**:

* `--token TEXT`
* `--help`: Show this message and exit.

## `stevent-management get_profile`

**Usage**:

```console
$ stevent-management get_profile [OPTIONS] ID
```

**Arguments**:

* `ID`: [required]

**Options**:

* `--token TEXT`
* `--help`: Show this message and exit.

## `stevent-management update_profile`

**Usage**:

```console
$ stevent-management update_profile [OPTIONS]
```

**Options**:

* `--id INTEGER`: [required]
* `--username TEXT`
* `--ticket TEXT`
* `--gender TEXT`
* `--age INTEGER`
* `--token TEXT`
* `--help`: Show this message and exit.

## `stevent-management delete_profile`

**Usage**:

```console
$ stevent-management delete_profile [OPTIONS] ID
```

**Arguments**:

* `ID`: [required]

**Options**:

* `--token TEXT`
* `--help`: Show this message and exit.

## `stevent-management delete_all_profiles`

**Usage**:

```console
$ stevent-management delete_all_profiles [OPTIONS]
```

**Options**:

* `--token TEXT`
* `--help`: Show this message and exit.

## `stevent-management search_profiles`

**Usage**:

```console
$ stevent-management search_profiles [OPTIONS]
```

**Options**:

* `--id INTEGER`
* `--username TEXT`
* `--age INTEGER`
* `--ticket TEXT`
* `--gender TEXT`
* `--token TEXT`
* `--help`: Show this message and exit.

## `stevent-management export_profiles`

**Usage**:

```console
$ stevent-management export_profiles [OPTIONS]
```

**Options**:

* `--file-path TEXT`: [required]
* `--token TEXT`
* `--help`: Show this message and exit.

## `stevent-management register_manager`

Register a new Event Manager.

**Usage**:

```console
$ stevent-management register_manager [OPTIONS]
```

**Options**:

* `--username TEXT`: [required]
* `--password TEXT`: [required]
* `--help`: Show this message and exit.

## `stevent-management login_manager`

Authenticate an Event Manager.

**Usage**:

```console
$ stevent-management login_manager [OPTIONS]
```

**Options**:

* `--username TEXT`: [required]
* `--password TEXT`: [required]
* `--help`: Show this message and exit.

## `stevent-management delete_manager`

Delete a specific Event Manager by username.

**Usage**:

```console
$ stevent-management delete_manager [OPTIONS]
```

**Options**:

* `--username TEXT`: [required]
* `--help`: Show this message and exit.

## `stevent-management delete_all_managers`

Delete all Event Managers from the database.

**Usage**:

```console
$ stevent-management delete_all_managers [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
