# EdgeCrafterFromScratch 
我的计划是从头开始写一个支持目标检测、实例分割等任务的视觉 Transformer 框架。它包含以下几个主要模块

+ 基于YAML的配置模块：这更接近Python系统开发，目的是学习一些Python语法特性和开发规范
+ 数据模块：数据集、数据管道
+ 模型模块：基于ViT的主干、FPN、基于Transformer的编解码器、任务头
+ 学习模块：评估、优化、训练
+ 日志模块：可视化、过程记录
+ 更多特性：AMP、EMA、LR调度、多GPU、权重、部署等

采用的方式是增量式的方式，一次写一点东西，逐步添加特性，最终实现一个可扩展的系统，包含一个

本项目基于的蓝本是[https://github.com/Intellindust-AI-Lab/EdgeCrafter](https://github.com/Intellindust-AI-Lab/EdgeCrafter)，它是DEIM系列的新作，整个视觉框架沿用继承了DEIM、DFINE、RT-DETR等系统。我们会拆解这个项目，用更简单的方法重构整个系统，使得你能尽可能清晰完整地理解它的每一块。