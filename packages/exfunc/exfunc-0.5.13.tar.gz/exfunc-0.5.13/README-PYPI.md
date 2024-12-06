# Exfunc Python SDK

Developer-friendly & type-safe Python SDK specifically catered to leverage *exfunc* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=exfunc&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


<!-- Start Summary [summary] -->
## Summary

Exfunc Python SDK is a library that allows you to easily take web actions on websites from your Python codebase.

<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [Exfunc Python SDK](https://github.com/carvedai/exfunc-py/blob/master/#exfunc-python-sdk)
  * [SDK Installation](https://github.com/carvedai/exfunc-py/blob/master/#sdk-installation)
  * [IDE Support](https://github.com/carvedai/exfunc-py/blob/master/#ide-support)
  * [SDK Example Usage](https://github.com/carvedai/exfunc-py/blob/master/#sdk-example-usage)
  * [Available Resources and Operations](https://github.com/carvedai/exfunc-py/blob/master/#available-resources-and-operations)
  * [Retries](https://github.com/carvedai/exfunc-py/blob/master/#retries)
  * [Error Handling](https://github.com/carvedai/exfunc-py/blob/master/#error-handling)
  * [Server Selection](https://github.com/carvedai/exfunc-py/blob/master/#server-selection)
  * [Custom HTTP Client](https://github.com/carvedai/exfunc-py/blob/master/#custom-http-client)
  * [Authentication](https://github.com/carvedai/exfunc-py/blob/master/#authentication)
  * [Debugging](https://github.com/carvedai/exfunc-py/blob/master/#debugging)
* [Development](https://github.com/carvedai/exfunc-py/blob/master/#development)
  * [Maturity](https://github.com/carvedai/exfunc-py/blob/master/#maturity)
  * [Contributions](https://github.com/carvedai/exfunc-py/blob/master/#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install exfunc
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add exfunc
```
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from exfunc import Exfunc
import os

with Exfunc(
    api_key=os.getenv("EXFUNC_API_KEY", ""),
) as s:
    res = s.google.get_job_posting(request={
        "job_posting_id": "<id>",
    })

    if res is not None:
        # handle response
        pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from exfunc import Exfunc
import os

async def main():
    async with Exfunc(
        api_key=os.getenv("EXFUNC_API_KEY", ""),
    ) as s:
        res = await s.google.get_job_posting_async(request={
            "job_posting_id": "<id>",
        })

        if res is not None:
            # handle response
            pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>


### [google](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/google/README.md)

* [get_job_posting](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/google/README.md#get_job_posting) - Get job posting details from Google
* [get_product](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/google/README.md#get_product) - Get product details from Google
* [get_product_reviews](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/google/README.md#get_product_reviews) - Get product reviews from Google
* [search_job_postings](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/google/README.md#search_job_postings) - Search job postings on Google
* [search_news](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/google/README.md#search_news) - Search news articles on Google
* [search_products](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/google/README.md#search_products) - Search products on Google
* [search_web](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/google/README.md#search_web) - Search web on Google

### [linkedin](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/linkedin/README.md)

* [get_company](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/linkedin/README.md#get_company) - Get LinkedIn company info
* [get_job_posting](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/linkedin/README.md#get_job_posting) - Get LinkedIn job posting info
* [get_person](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/linkedin/README.md#get_person) - Get LinkedIn person profile info
* [search_companies](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/linkedin/README.md#search_companies) - Search for LinkedIn companies
* [search_job_postings](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/linkedin/README.md#search_job_postings) - Search for LinkedIn job postings
* [search_people](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/linkedin/README.md#search_people) - Search for LinkedIn people

### [navigator](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/navigator/README.md)

* [get_task](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/navigator/README.md#get_task) - Get web navigator task results
* [start_task](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/navigator/README.md#start_task) - Start a web navigator task
* [scrape](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/navigator/README.md#scrape) - Scrape a web page

### [skyscanner](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/skyscanner/README.md)

* [search_flights](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/skyscanner/README.md#search_flights) - Search flights on SkyScanner

### [twitter](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/twitter/README.md)

* [get_tweet](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/twitter/README.md#get_tweet) - Get a tweet by ID
* [get_user](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/twitter/README.md#get_user) - Get a Twitter user by either user ID or username
* [get_user_followers](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/twitter/README.md#get_user_followers) - Get a Twitter user's followers by username
* [get_user_followings](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/twitter/README.md#get_user_followings) - Get a Twitter user's followings by username
* [get_user_tweets](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/twitter/README.md#get_user_tweets) - Get a Twitter user's tweets by username
* [search_tweets](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/twitter/README.md#search_tweets) - Search Twitter for tweets
* [search_users](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/twitter/README.md#search_users) - Search Twitter for users

### [yelp](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/yelp/README.md)

* [get_business](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/yelp/README.md#get_business) - Get business details from Yelp
* [get_business_reviews](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/yelp/README.md#get_business_reviews) - Get Yelp reviews for a business
* [search_businesses](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/yelp/README.md#search_businesses) - Search for businesses on Yelp

### [zillow](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/zillow/README.md)

* [get_property](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/zillow/README.md#get_property) - Get property details from Zillow
* [search_properties](https://github.com/carvedai/exfunc-py/blob/master/docs/sdks/zillow/README.md#search_properties) - Search for properties on Zillow

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from exfunc import Exfunc
from exfunc.utils import BackoffStrategy, RetryConfig
import os

with Exfunc(
    api_key=os.getenv("EXFUNC_API_KEY", ""),
) as s:
    res = s.google.get_job_posting(request={
        "job_posting_id": "<id>",
    },
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    if res is not None:
        # handle response
        pass

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from exfunc import Exfunc
from exfunc.utils import BackoffStrategy, RetryConfig
import os

with Exfunc(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key=os.getenv("EXFUNC_API_KEY", ""),
) as s:
    res = s.google.get_job_posting(request={
        "job_posting_id": "<id>",
    })

    if res is not None:
        # handle response
        pass

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.SDKError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `get_job_posting_async` method may raise the following exceptions:

| Error Type         | Status Code | Content Type     |
| ------------------ | ----------- | ---------------- |
| models.UserError   | 400         | application/json |
| models.ServerError | 500         | application/json |
| models.SDKError    | 4XX, 5XX    | \*/\*            |

### Example

```python
from exfunc import Exfunc, models
import os

with Exfunc(
    api_key=os.getenv("EXFUNC_API_KEY", ""),
) as s:
    res = None
    try:
        res = s.google.get_job_posting(request={
            "job_posting_id": "<id>",
        })

        if res is not None:
            # handle response
            pass

    except models.UserError as e:
        # handle e.data: models.UserErrorData
        raise(e)
    except models.ServerError as e:
        # handle e.data: models.ServerErrorData
        raise(e)
    except models.SDKError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from exfunc import Exfunc
import os

with Exfunc(
    server_url="https://api.exfunc.com",
    api_key=os.getenv("EXFUNC_API_KEY", ""),
) as s:
    res = s.google.get_job_posting(request={
        "job_posting_id": "<id>",
    })

    if res is not None:
        # handle response
        pass

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from exfunc import Exfunc
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Exfunc(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from exfunc import Exfunc
from exfunc.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Exfunc(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name      | Type   | Scheme  | Environment Variable |
| --------- | ------ | ------- | -------------------- |
| `api_key` | apiKey | API key | `EXFUNC_API_KEY`     |

To authenticate with the API the `api_key` parameter must be set when initializing the SDK client instance. For example:
```python
from exfunc import Exfunc
import os

with Exfunc(
    api_key=os.getenv("EXFUNC_API_KEY", ""),
) as s:
    res = s.google.get_job_posting(request={
        "job_posting_id": "<id>",
    })

    if res is not None:
        # handle response
        pass

```
<!-- End Authentication [security] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from exfunc import Exfunc
import logging

logging.basicConfig(level=logging.DEBUG)
s = Exfunc(debug_logger=logging.getLogger("exfunc"))
```

You can also enable a default debug logger by setting an environment variable `EXFUNC_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=exfunc&utm_campaign=python)
