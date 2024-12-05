# Utils

Cloudflare utilities.
This utilities are meant to be used in CI/CD pipelines.

You can use it as a pre-commit.
Nb: No public hook is available since it would need to expose the repository => this must be defined locally

```yaml
- repo: local
  hooks:
  - id: cfutils-check
    name: cfutils-check
    description: check csv files containing DNS records
    entry: cfutils check
    language: python
    pass_filenames: false
    files: ^(.*/)?dns_records\.csv$
    args: ["-f", "dns_records.csv"]
    additional_dependencies: ["nagra_network_cloudflare_utils==0.2.1"]

  - id: cfutils-sort
    name: cfutils-sort
    description: sort csv files containing DNS records
    entry: cfutils sort
    language: python
    pass_filenames: false
    files: ^(.*/)?dns_records\.csv$
    args: ["-f", "dns_records.csv"]
    additional_dependencies: ["nagra_network_cloudflare_utils==0.2.1"]
```
