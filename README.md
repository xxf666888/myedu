# myedu
先需要搭建好自己的k8s集群和镜像仓库，我的是harbor私有仓库
git clone 项目链接 
cd myedu
docker build -t myapp:v1 .  如果太慢可以在dockerfiel里加清华源RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# 上传到私有仓库
docker tag myedu:v1 harbor:443/edu/myedu:v1  （将harbor:443/edu/myedu:v1替换成你的仓库路径）
docker push harbor:443/edu/myedu:v1  （名字同上）
# 配置secret
由于搭建的harbor仓库是https的私有仓库，所以Kubernetes 需要凭证才能从Harbor 仓库拉取镜像。
kubectl create secret docker-registry myedu-registry-secret --docker-server=harbor:443 --docker-username=xxf --docker-password=Xxf1201. --docker-email=198703473@qq.com（创建了一个名为myedu-registry-scret的imagePullSecrets密钥，自定义账号密码邮箱）
# 编辑deployment文件
vim k8s/deployment.yaml
将containers下的image：harbor:443/edu/myedu:v1  改成你自己的仓库路径
# 应用配置文件
kubectl apply -f deployment.yaml -f service.yaml
# 查看service暴露的端口
kubectl get service
本机Ip+service暴露的端口访问项目
