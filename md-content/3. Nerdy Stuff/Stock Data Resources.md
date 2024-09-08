# Free Stock Data Resources for Research and Archiving

These resources are listed for **research purposes only**, and I’m still exploring their capabilities. All options are **free**, and many seem to support bulk requests for efficient data retrieval and archiving, though further investigation is needed.

## Company Logos

### Clearbit Logo API

Clearbit provides a free API to access logos for public companies. From what I’ve gathered, you can use the domain name of the company (e.g., `apple.com`) to retrieve the logo. It appears to support bulk requests and may be useful for archiving, but I haven't tested this extensively.

- **URL**: [https://clearbit.com/logo](https://clearbit.com/logo)
- **Usage**: Simply use a URL like `https://logo.clearbit.com/{domain}` to fetch the logo.

```html
<img src="https://logo.clearbit.com/apple.com" alt="Apple Logo" />
```

## Fundamentals

Although I haven't fully explored it, **SEC-Edgar** seems to simplify the process of obtaining filings for multiple companies at once. It allows for bulk downloads of a company’s periodic reports, filings, and forms, which could be valuable for archival purposes.

- **GitHub Repository**: [sec-edgar](https://github.com/sec-edgar/sec-edgar)
