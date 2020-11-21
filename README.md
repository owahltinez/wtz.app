# wlinks
Simple implementation of a self-hosted service for the creation of short links.

## Instructions
1. Fork this repo
1. Create a publicly available CSV file containing `path` and `redirect` fields
1. Change the values in [config.json](./config.json) to match your desired configuration
1. Setup GitHub Pages to be served from your custom (apex) domain name

For an example CSV file, see the link in [config.json](./config.json) which uses Google Sheets. If
you want to keep the list of short URLs private, you can also use a free service like
[Cloudflare Workers](https://workers.cloudflare.com/) to hide the URL of the CSV file, and
only return a single record when the requested path matches a short link:

```js
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

// Source of data
const CSV_URL = 'your-secret-csv-file-url';

/**
 * Respond to the request with a CSV formatted body output.
 * @param {Request} request
 */
async function handleRequest(request) {
  const headers = {'Access-Control-Allow-Origin': '*'}
  const rows = (await (await fetch(CSV_URL)).text()).split('\n');
  const header = rows.shift();
  const searchPath = new URL(request.url).searchParams.get('path');
  for (let row of rows.reverse()) {
    const [path, redirect] = row.split(',', 3).slice(0, 2);
    if (path === searchPath) return new Response([header, row].join('\n'), {status: 200, headers: headers});
  }
  return new Response(null, {status: 404, headers: headers});
}
```