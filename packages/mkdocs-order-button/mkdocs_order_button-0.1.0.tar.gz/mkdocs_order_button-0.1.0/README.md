# mkdocs order button

MKDocs plugin for order electric parts.

[Demo](https://ouxt-polaris.github.io/mkdocs_order_button/)

## How to use
1. install this plugin from pypi

e.g
```sh
pip3 install mkdocs_order_button
```

1. add this plugin to your mkdocs.yaml

```yaml
plugins:
  - akizukidenshi_order_button
```

2. Just write these line in your markdown file.

```
@akizuki_denshi_order_button(./kibot_output/bom/miniv_motor_controller_board-bom.xml)
```

./kibot_output/bom/miniv_motor_controller_board-bom.xml is a relative path to the KiCAD XML BOM file.

I export this file by using [KiBot.](https://kibot.readthedocs.io/en/latest/configuration/outputs/kibom.html)
