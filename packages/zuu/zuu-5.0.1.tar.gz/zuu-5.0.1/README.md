# zuu


## Supported Sub Packages
- va (vision and automation)
- app (app configs and automation)
- cli (command line interface)
- doc (documents)
- ext1 
- alpha (for testing purposes)

## install
for plain package
```bash
pip install zuu
```
install with features
```bash
pip install zuu[io]
```

for package with additional supports
```bash
pip install git+https://github.com/zwtil/zuu2.git#subdirectory=PYTHON_PKG/std
```

to install sub packages

pip method
```bash
pip install git+https://github.com/zwtil/zuu2.git#subdirectory=PYTHON_PKG/{sub_pkg}
```

rye method
```bash
rye add zuu[{sub packages}] --git https://github.com/zwtil/zuu2.git#subdirectory=PYTHON_PKG/std
```

## Project Layout
| pkg  |    uses     | reserved |
| ---- | ----------- | -------- |
| std  | common, pkg | io       |
| app  | app         |          |
| cli  | common      |          |
| doc  | app, common |          |
| ext1 | pkg         |          |
| va   | pkg, common |          |
