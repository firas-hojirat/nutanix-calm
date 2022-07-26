
## Verify Nvidia Grid Host Drivers are Installed

Login to CVM via SSH and run following command

```bash
## Verify Driver RPMs are installed
$ hostssh 'rpm -qa | grep nvidia'
============= 10.38.38.25 ============
nvidia-vgpu-450.102-2.20201105.1.14.el7.x86_64
============= 10.38.38.26 ============
nvidia-vgpu-450.102-2.20201105.1.14.el7.x86_64
============= 10.38.38.27 ============
nvidia-vgpu-450.102-2.20201105.1.14.el7.x86_64
============= 10.38.38.28 ============
nvidia-vgpu-450.102-2.20201105.1.14.el7.x86_64

## Verify Cards are detected
$ hostssh 'nvidia-smi -a | grep "Product Name"'
============= 10.38.38.25 ============
    Product Name                          : Tesla T4
    Product Name                          : Tesla T4
============= 10.38.38.26 ============
    Product Name                          : Tesla T4
    Product Name                          : Tesla T4
============= 10.38.38.27 ============
    Product Name                          : Tesla T4
    Product Name                          : Tesla T4
============= 10.38.38.28 ============
    Product Name                          : Tesla T4
    Product Name                          : Tesla T4

```

The first thing you'll need to do is to Assign a vGPU profile to the VM. When you're creating the VM, you'll be able to add GPU. Select an appropriate NVIDIA Virtual GPU License and then select a vGPU Profile to assign to the VM. Once this is done, create the VM and it's time to install some drivers.

It is very important to select a guest driver that matches the host-drivers that are installed. You can use the table below to determine which drivers you should use for Windows and Linux guests:

https://www.nutanix.dev/2022/02/16/getting-started-with-gpu-on-nutanix-karbon/


./karbon/karbonctl cluster gpu-inventory list --cluster-name ml-cluster

./karbon/karbonctl cluster node-pool add --cluster-name ml-cluster --count 2 --memory 12 --gpu-count 1 --gpu-name "Tesla T4 compute" --node-pool-name gpu


