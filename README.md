# translation-api

本项目汇总市面上翻译服务，统一接口并构建为 docker 镜像方便使用。

## 支持的 API 供应商

- 百度翻译（`baidu`)：https://fanyi.baidu.com/
- 搜狗翻译（`sogou`）：https://fanyi.sogou.com/
- 小牛翻译（`niutrans`）：https://niutrans.vip/
- Bing 翻译（`bing`）：https://cn.bing.com/translator/
- 金山爱词霸翻译（`iciba`）：http://fy.iciba.com/


## API 使用方法

所有 API 使用 `POST` 访问，body 参数包含：

- `vendor`：api 供应商，可选值见上节
- `from`：待翻译文本语言，支持 `zh`, `en`
- `to`：翻译结果语言，支持 `zh`, `en`
- `query`：待翻译文本内容

返回结果除了保留请求参数，还包括：

- `status`：状态码，请求成功返回 0，否则返回 1
- `target`：翻译结果文本内容，只在 `status=0` 时返回
- `error`：错误详情，一般为 HTTP 链接错误或内容解析错误（如页面改版），只在 `status=1` 时返回

示例：

    $ curl -X POST 'http://10.202.81.49:8001/v1/trans' -H 'Content-Type:application/json' -d \ '   
    {
        "vendor": "baidu",
        "from": "zh",
        "to": "en",
        "query": "外国嘉宾参观互联网之光博览会上的黑科技。"
    }'

结果如下：

```json
{
    "status": 0,
    "target": "Foreign guests visit black technology at the Internet Light Expo.",
    "vendor": "baidu",
    "from": "zh",
    "to": "en",
    "query": "外国嘉宾参观互联网之光博览会上的黑科技。"
}
```


## Docker 镜像使用

使用 Docker：

- 构建

        $ docker build -t pyfreyr/trans:v0.0.1 .
        
- 运行

        $ docker run -d -p 8001:8888 --name trans pyfreyr/trans:v0.0.1

或者，使用 Compose：

- 构建

        $ docker-compose build
    
- 运行

        $ docker-compose up -d

## CHANGELOG
### 2018-11-9 18:22:41
- 修复 baidu 和 niutrans API 错误，感谢 @672399809(xstring) 反馈


