# SSH Keygen (Password-less Server Login)

Using SSH keys for authentication is a secure and convenient way to log into a remote server without needing to enter a password every time. Below are the steps to set up password-less SSH login using RSA keys.

## Step 1: Generate an SSH Key Pair

First, generate an SSH key pair on your local machine. This command will create a public-private key pair.

```bash
ssh-keygen -t rsa -b 2048
```

You'll be prompted to specify a location to save the key and optionally enter a passphrase. If you choose to enter a passphrase, you'll add an extra layer of security, but you'll need to enter the passphrase each time you use the key.

## Step 2: Copy the Public Key to the Server

Use the `ssh-copy-id` command to copy your public key to the remote server. Replace `user` with your username and `server` with the remote server's address.

```bash
ssh-copy-id user@server
```

You'll be prompted to enter the remote user's password. This is the last time you should need to use the password to log in to the server.

## Step 3: Log into the Server

Now, you can log into the remote server without being prompted for a password.

```bash
ssh user@server
```

## Using a Custom Port

If your SSH server listens on a port other than the default port (22), you can specify the custom port using the `-p` option.

```bash
ssh-copy-id -p 8129 user@host
```

**Note:** When specifying a custom port, the port number must be placed before the `user@host` portion of the command.

## References

- [SSH Copy-ID Documentation](https://www.ssh.com/ssh/copy-id)
- [Using SSH-Copy-ID on a Different Port](https://unix.stackexchange.com/a/66074)
- [Source for Custom Port Usage](http://it-ride.blogspot.com/2009/11/use-ssh-copy-id-on-different-port.html)

By following these steps, you can set up password-less SSH login, which enhances security and convenience for accessing your remote servers.
