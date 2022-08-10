
> Testing Restore

```bash

## Create a New Pod

kubectl run busybox --image=busybox -n default -- sleep 600

## Snapshot DB on initial instance

etcdctl --endpoints https://$ETCD_IP_0:2379 snapshot save /root/snapshot.db

## Write-out status to validate that snapshot db looks good

etcdctl snapshot status /root/snapshot.db --write-out=table

## Delete Pod

kubectl delete po busybox -n default

## Restore Database

etcdctl snapshot restore /root/snapshot.db --skip-hash-check=true --data-dir="/var/lib/etcd-from-backup"

## Modify /etc/kubernetes/manifests/etcd.yaml

  - hostPath:
      path: /var/lib/etcd-from-backup
      type: DirectoryOrCreate

## Wait for restart - watch docker
watch "docker ps | grep etcd"

```