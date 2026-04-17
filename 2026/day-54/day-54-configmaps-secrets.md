# What ConfigMaps and Secrets are and when to use each
### A conifgmap is an API object used to store non-confidential data in key-value pairs. Pods can consume ConfigMaps as environment variables, command-line arguments, or as configuration files in a volume.
### ConfigMap does not provide secrecy or encryption. If the data you want to store are confidential, use a Secret rather than a ConfigMap.

# The difference between environment variables and volume mounts
### Use Environment Variables When:
#### Configuration data is small (< 1MB total)
#### Values are simple key-value pairs
#### Application expects standard environment variables
#### Configuration is truly static during pod lifetime
#### You need maximum portability across platforms

### Use Volume Mounts When:
#### Configuration files are large or complex
#### You need structured data (JSON, YAML, XML)
#### Configuration might change during runtime
#### You have binary data or certificates
#### File permissions and ownership matter
#### You need atomic updates to multiple files

# Why base64 is encoding, not encryption
### Base64 is an encoding scheme, not encryption, because it is a reversible, keyless transformation designed solely for data format compatibility rather than security

# How ConfigMap updates propagate to volumes but not env vars
### Volumes: When a ConfigMap is mounted as a volume, the kubelet eventually updates the files in the container (delay depends on sync period and cache strategy). The application must detect and reload the file changes. 
### Environment Variables: Values are injected once at pod startup. Updates do not propagate; a pod restart (e.g., via kubectl rollout restart) is required for changes to take effect. 

