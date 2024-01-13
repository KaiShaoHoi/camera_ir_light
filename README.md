# Home Assistant HACS 集成：红外光传感器

该 Home Assistant 集成添加了对红外光传感器的支持。它通过检查红外摄像头的日志来确定室外光照条件，并允许您根据光照条件自动执行操作。

## 安装

1. 如果尚未安装 [HACS](https://hacs.xyz/)，请先安装。

2. 在 HACS 仪表板中，转到“Integrations”（集成）部分。

3. 点击 + 按钮以添加新的集成。

4. 搜索“IR Light Sensor”，并从列表中选择。

5. 点击 Install 并按照屏幕上的说明操作。

6. 通过提供主机 IP 地址和轮询间隔等必需信息来配置集成。

## 配置

在您的 Home Assistant `configuration.yaml` 文件中，您可以使用以下示例配置添加红外光传感器集成：

```yaml
sensor:
  - platform: ir_light
    host: 192.168.1.25
    polling_interval: 60
```

请确保根据您的设置调整 `host` 和 `polling_interval` 值。

## 注意事项

- 确保指定的主机 IP 地址是正确的，并且从您的 Home Assistant 实例可以访问。

- 轮询间隔确定集成检查红外摄像头日志的频率。请注意频率以避免不必要的网络流量。

- 如果遇到任何问题或有疑问，请查看 [GitHub 仓库](https://github.com/yourusername/your-repo) 进行故障排除和额外信息。

## 贡献

如果您有改进意见或发现错误，请在 [GitHub 仓库](https://github.com/yourusername/your-repo) 上提出问题。

## 许可证

此集成根据 MIT 许可证授权 - 详细信息请参阅 [LICENSE](LICENSE) 文件。

