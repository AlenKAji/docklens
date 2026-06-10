# Reverse Proxy Auth

DockLens reads Docker metadata, so do not expose it directly to the public internet. Put it behind a private network, VPN, or reverse proxy authentication.

## Caddy

1. Edit `deploy/reverse-proxy/Caddyfile`.
2. Replace `docklens.example.com`.
3. Generate a real password hash:

```bash
caddy hash-password --plaintext 'your-password'
```

4. Replace the sample hash in the `basicauth` block.

## Nginx

Generate an htpasswd file:

```bash
htpasswd -c .htpasswd admin
```

Mount `nginx.conf` and `.htpasswd` into your Nginx container or host-level Nginx installation.

For HTTPS, pair this with Certbot, Caddy automatic TLS, or your cloud load balancer's managed certificates.
