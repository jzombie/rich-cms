# SSH Auditing

## Test sshd configuration validity

```bash
sudo /usr/sbin/sshd -t
```

- If there's **no output**, your config is syntactically correct.
- Any errors will be printed (missing parameters, bad indentation, etc.).

## Dump effective config

```bash
sudo /usr/sbin/sshd -T
```

This shows the **fully-resolved sshd configuration**, including defaults and overrides.

## Filter for Critical Options

To audit just the key security settings:

```bash
sudo /usr/sbin/sshd -T | grep -E \
'port|permitrootlogin|passwordauthentication|pubkeyauthentication|allowusers|challengeresponseauthentication'
```

### Recommended Output Should Look Like:

```text
port 2222
permitrootlogin no
passwordauthentication no
pubkeyauthentication yes
challengeresponseauthentication no
allowusers administrator
```

If `passwordauthentication` is `yes`, it's still vulnerable to password-based brute force.

## Optional: Test From a Remote Machine

To verify what auth methods the server offers:

```bash
ssh -vvv -p 2222 youruser@your.ip
```

Look for a line like:

```text
debug1: Authentications that can continue: publickey
```

If you see `password`, your config **still allows it**.
