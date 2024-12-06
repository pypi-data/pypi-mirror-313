

简介
=======

本工具提供给客户在已有集群的情况下在新节点加入集群后自动安装驱动的功能，支持在集群条件下华为NPU的驱动与固件的安装。

快速指南
===========

本工具主要支持存在已使用ascend-deployer的环境安装的集群的场景，如果遇到问题，请参考\ `ascend-deployer用户指南 <https://www.hiascend.com/document/detail/zh/ascend-deployer>`__\。

安装内容
-------------

工具支持安装的内容为驱动以及固件

使用样例
-------------

以下以Ubuntu_20.04_aarch64系统，服务器上插Atlas 300I Pro推理卡为例快速展示工具的使用方式。

1. 准备好驱动固件的run文件（可通过ascend-deployer下载，也可自行官方下载解压）Ascend-hdk-310P-npu-driver_23.0.rc1_linux-x86-64.run和Ascend-hdk-310P-npu-firmware_6.3.0.1.241.run，。
和驱动的依赖文件，在ascend-deployer下载中的Ubuntu_20.04_aarch64文件夹下，也可根据操作系统自己准备，这里是net-tools和pciutils的deb文件

2. 将上述文件与工具中的driver-install.sh dockerfile文件放置于同一文件夹下进行镜像构建，构建出的镜像名为arm-310p-installer:v1（也可以自己指定），
上传进节点可以拉取到的镜像仓中，可以为本地仓。

   ::

      docker build -t arm-310p-installer:v1 .
      文件如下
      .
      |- dockerfile
      |- driver-install.sh
      |- Ubuntu_20.04_aarch64
      |  |- net-tools_1.60_arm64.deb
      |  |- pciutils_5.30_arm64.deb
      |_ run_from_a310_zip
         |- Ascend-hdk-310P-npu-driver_23.0.rc1_linux-x86-64.run
         |- Ascend-hdk-310P-firmware_6.3.0.1.241.run
         |_ install.sh


3. 将工具中的kubernetes的yaml进行apply(主节点)，重点关注containers里的镜像是否和上面构建出的镜像正确对应，以及nodeselector字段是否为筛选arm和300p的标签
部署后查看daemonset判断是否创建成功

   ::

      kubectl apply -f 310-arm-installer.yaml

4. 将节点使用kubeadm join命令加入到集群中，在主节点上给节点打上相应标签，然后等待驱动安装完毕

   ::

      kubectl label node [worker] --overwrite host-arch=huawei-arm
      kubectl label node [worker] --overwrite accelerator=huawei-Ascend310P

   执行以上命令后，然后等待驱动安装完毕