# UniSwap新池监控脚本，支持GoPlus SDK检测
![image](https://github.com/user-attachments/assets/b1d306f2-bfad-4b42-8515-e97cab7a185f)

## 安装依赖
```
pip install web3 goplus requests
```

## 克隆仓库
```
git clone https://github.com/singosol/New-pair-monitoring.git
```

## 进入刚克隆仓库的文件夹
```
cd New-pair-monitoring
```

## 配置脚本
### 第9行和第13行须替换成你自己的infura key和discord webhook链接，第14行可以根据自己的需求修改
```
nano uninewpair.py
```
![image](https://github.com/user-attachments/assets/3b566f15-c1bc-4b42-889f-41d6c55ed473)


## 运行脚本
```
python3 uninewpair.py
```
