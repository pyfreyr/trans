from tornado import httpclient


async def get_content(request, **kwargs):
    client = httpclient.AsyncHTTPClient()

    res = {}
    try:
        response = await client.fetch(request, **kwargs)
    except httpclient.HTTPError as e:
        res.update(status=1, error=e)
    else:
        res.update(status=0, data=response.body.decode(errors='ignore'))
    return res
