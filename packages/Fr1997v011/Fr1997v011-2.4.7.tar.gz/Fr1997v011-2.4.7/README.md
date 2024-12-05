# Fr1997 python私有包

## 介绍
    私人包，所有方法需要配置参数，没有配置参数无法使用

### 项目代码打包成一个可执行文件

```sh
python setup.py build
```

### 将源文件进行打包操作

```sh
python setup.py sdist
```

### （本地）安装包

```sh
pip install dist/Fr1997v011-2.4.6.tar.gz
```

### 下载包

```sh
pip install Fr1997v011
```

### 清空pip缓存

```sh
pip cache purge
```

### 升级包

```sh
pip install --upgrade Fr1997v011
```

### 上传pypi  (pip install twine)
 
```sh
twine upload dist/*      
```
      

### 卸载包

```sh
pip uninstall Fr1997v011
```

pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Fr1997v011==1.1.2




