# TLS REQUESTS
**A powerful and lightweight Python library for making secure and reliable HTTP/TLS Fingerprint requests.**

* * *

**Installation**
----------------

To install the library, you can choose between two methods:

#### **1\. Install via PyPI:**

```shell
pip install wrapper-tls-requests
```

#### **2\. Install via GitHub Repository:**

```shell
pip install git+https://github.com/thewebscraping/tls-requests.git
```

**Quick Start**
---------------

Start using TLS Requests with just a few lines of code:

```pycon
>>> import tls_requests
>>> r = tls_requests.get("https://httpbin.org/get")
>>> r
<Response [200 OK]>
>>> r.status_code
200
```

**Introduction**
----------------

**TLS Requests** is a cutting-edge HTTP client for Python, offering a feature-rich,
highly configurable alternative to the popular [`requests`](https://github.com/psf/requests) library.

Built on top of [`tls-client`](https://github.com/bogdanfinn/tls-client),
it combines ease of use with advanced functionality for secure networking.

**Acknowledgment**: A big thank you to all contributors for their support!

### **Key Benefits**

*   **Bypass TLS Fingerprinting:** Mimic browser-like behaviors to navigate sophisticated anti-bot systems.
*   **Customizable TLS Clients:** Select specific TLS fingerprints to meet your needs.
*   **Ideal for Developers:** Build scrapers, API clients, or other custom networking tools effortlessly.


**Why Use TLS Requests?**
-------------------------

Modern websites increasingly use **TLS Fingerprinting** and anti-bot tools like Cloudflare Bot Fight Mode to block web crawlers.

**TLS Requests** bypass these obstacles by mimicking browser-like TLS behaviors,
making it easy to scrape data or interact with websites that use sophisticated anti-bot measures.

### Unlocking Cloudflare Bot Fight Mode
![coingecko.png](https://raw.githubusercontent.com/thewebscraping/tls-requests/refs/heads/main/docs/static/coingecko.png)

**Example Code:**

```pycon
>>> import tls_requests
>>> r = tls_requests.get('https://www.coingecko.com/')
>>> r
<Response [200]>
```

**Key Features**
----------------

### **Enhanced Capabilities**

*   **Browser-like TLS Fingerprinting**: Enables secure and reliable browser-mimicking connections.
*   **High-Performance Backend**: Built on a Go-based HTTP backend for speed and efficiency.
*   **Synchronous & Asynchronous Support**: Seamlessly switch between synchronous and asynchronous requests.
*   **Protocol Support**: Fully compatible with HTTP/1.1 and HTTP/2.
*   **Strict Timeouts**: Reliable timeout management for precise control over request durations.

### **Additional Features**

*   **Internationalized Domain & URL Support**: Handles non-ASCII URLs effortlessly.
*   **Cookie Management**: Ensures session-based cookie persistence.
*   **Authentication**: Native support for Basic and Function authentication.
*   **Content Decoding**: Automatic handling of gzip and brotli-encoded responses.
*   **Hooks**: Perfect for logging, monitoring, tracing, or pre/post-processing requests and responses.
*   **Unicode Support**: Effortlessly process Unicode response bodies.
*   **File Uploads**: Simplified multipart file upload support.
*   **Proxy Configuration**: Supports Socks5, HTTP, and HTTPS proxies for enhanced privacy.


**Documentation**
-----------------

Explore the full capabilities of TLS Requests in the documentation:

*   **[Quickstart Guide](https://thewebscraping.github.io/tls-requests/quickstart/)**: A beginner-friendly guide.
*   **[Advanced Topics](https://thewebscraping.github.io/tls-requests/advanced/client/)**: Learn to leverage specialized features.
*   **[Async Support](https://thewebscraping.github.io/tls-requests/advanced/async_client/)**: Handle high-concurrency scenarios.
*   **Custom TLS Configurations**:
    *   **[Wrapper TLS Client](https://thewebscraping.github.io/tls-requests/tls/)**
    *   **[TLS Client Profiles](https://thewebscraping.github.io/tls-requests/tls/profiles/)**
    *   **[Custom TLS Configurations](https://thewebscraping.github.io/tls-requests/tls/configuration/)**


Read the documentation: [**thewebscraping.github.io/tls-requests/**](https://thewebscraping.github.io/tls-requests/)
