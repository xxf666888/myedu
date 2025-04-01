# myedu
首先需要搭建好自己的k8s集群和镜像仓库
git clone 项目链接 
cd myedu
docker build -t myapp:v1 .  如果太慢可以在dockerfiel里加清华源RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
将k8s下的deployment.yaml的镜像路径替换成你自己的路径
# 应用配置文件
kubectl apply -f deployment.yaml -f service.yaml
# 查看service暴露的端口
kubectl get service
本机Ip+service暴露的端口访问项目
