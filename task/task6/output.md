安装过程中遇到了一个错误，指出 `jwtSecretKey.txt` 文件中的内容无法被解析为 JSON。这可能是因为该文件的内容是一个字符串而不是 JSON 格式的数据。

为了修复这个问题，我们需要确保 `jwtSecretKey.txt` 包含的是有效的 JSON 格式。通常，对于 JWT 密钥，它应该是一个简单的字符串值，但是 Helm 期望它是一个键值对的形式。例如：

```json
{
  "appmanager": {
    "server": {
      "jwtSecretKey": "your-actual-jwt-secret-key"
    }
  }
}
```

请检查 `jwtSecretKey.txt` 文件的内容，并按照上述格式进行修改。如果你不确定如何修改，请提供文件的内容，我将帮助你转换成正确的格式。如果文件内容已经是正确的 JSON 格式，请确认是否有任何拼写或语法错误。