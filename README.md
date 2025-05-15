Check Virtualization Extension
Run this command to make sure you’ve enabled virtualization in on your computer. It should be above 0
```bash
egrep -c '(vmx|svm)' /proc/cpuinfo
```
If the output is zero then go to bios settings and enable VT-x (Virtualization Technology Extension) for Intel processor and AMD-V for AMD processor.

Install QEMU and Virtual Machine Manager
```bash
sudo apt install qemu-kvm qemu-system qemu-utils python3 python3-pip libvirt-clients libvirt-daemon-system bridge-utils virtinst libvirt-daemon virt-manager -y
```
Verify that Libvirtd service is started
```bash
sudo systemctl status libvirtd.service
```
Start Default Network for Networking 
```bash
sudo virsh net-start default
sudo virsh net-autostart default
sudo virsh net-list --all
```
Add User to libvirt to Allow Access to VMs
```bash
sudo usermod -aG libvirt $USER
sudo usermod -aG libvirt-qemu $USER
sudo usermod -aG kvm $USER
sudo usermod -aG input $USER
sudo usermod -aG disk $USER
```
