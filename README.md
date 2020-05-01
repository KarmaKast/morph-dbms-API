# node web API

## Setup: tested on linux. [On windows probably use bash instead of cmd. But its not tested]

- clone repo
- rum following commands in order at the cloned dir

``` bash
npm install
npm run build
npm run serve
```

notes:
- the api currently runs at http://localhost:3000 . If anything is running at that port it kills that process and starts this. This was to kill previous instances of nodeAPI server that were not closed properly. If you have anything else running at that port I suggest you manually edit the port in [serve.ts](./src/serve.ts#L4)
