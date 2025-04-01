# myedu
这是一个很简单的在线教育平台的项目，只是用来作为学习参考，先需要搭建好自己的k8s集群和镜像仓库，我的是harbor私有仓库
git clone https://github.com/xxf666888/myedu.git
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
此时你的项目还没有会话粘性，由于service可以负载均衡他会将你每次的请求随机分发给不同的pod，这样会导致会话中断
# 设置会话粘性
1. 简单方法：由service通过clientip的方式将请求分发给指定pod
   直接将service里的那几行注释取消掉
   kubectl replace --force -f k8s/service.yaml
   再次访问，就可以了
3. 复杂方法：由ingress控制器通过识别cookie的方式将请求分发给pod
    kubectl get ingess 看看你有没有ingress控制器，如果有，看看名字是不是nginx，如果不是去ingress.ymal里的ingressClassName改成你的名字
    # 如果没有ingress控制器，在k8s/有一个ingress.tar.xz的控制器的镜像tar包
   ]cd k8s
   ]docker load -i ingress.tar.xz
   ]docker images|while read i t _;do
      [[ "${t}" == "TAG" ]] && continue
      [[ "${i}" =~ ^"harbor:443/".+ ]] && continue
      docker tag ${i}:${t} harbor:443/plugins/${i##*/}:${t}
      docker push harbor:443/plugins/${i##*/}:${t}
      docker rmi ${i}:${t} harbor:443/plugins/${i##*/}:${t}
   done #自动push到harbor:443/plugins项目下，也可以手动上传到镜像仓库
   ]sed -ri 's,^(\s*image: )(.*/)?(.+),\1harbor:443/plugins/\3,' deploy.yaml #批量修改Kubernetes部署文件中的镜像地址，将镜像指向私有仓库
   ]kubectl apply -f deploy.yaml  #至此，控制器安装完成
   ]kubectl apply -f k8s/ingress.yaml
   # ingress也配置好了后，再用kubectl get ingress查看分配的address
   ]vim /etc/hosts
     192.168.1.19  edu.cn    #将刚刚查看的address和host添加到域名解析的文件,这里的host是ingress.yaml里面设置的，如果没改就是edu.cn
   这样就可以通过在网页输入edu.cn访问这个项目，并且也配置了会话粘性
   如果用的是windows系统远程linux，还需要一步
   讲这个文件 C:\Windows\System32\drivers\etc\hosts  添加address和host，跟上面的一样
   现在就可以在windows的浏览器里输入edu.cn访问到项目了
   
