import unittest
import re
from os_tests.libs import utils_lib
import time
import os
import json
import tempfile
import string
from urllib.parse import urlparse
from datetime import datetime

class TestImageMode(unittest.TestCase):
    def setUp(self):
        utils_lib.init_case(self)
        self.dmesg_cursor = utils_lib.get_cmd_cursor(self, cmd='sudo dmesg -T')
        utils_lib.collect_basic_info(self)

    def _podman_login(self,io_user, io_pw, io_name):
        cmd = "sudo podman login -u='{}' -p='{}' {}".format(io_user, io_pw, io_name)
        utils_lib.run_cmd(self, cmd, is_log_cmd=False, expect_ret=0)

    def test_create_bootc_disk_image(self):
        """
        case_name:
            test_create_bootc_disk_image
        case_tags:
            image_mode
        case_status:
            approved
        title:
            TestImageMode.test_create_bootc_disk_image
        importance:
            critical
        subsystem_team:
            rhel-sst-virtualization-cloud
        automation_drop_down:
            automated
        linked_work_items:
            n/a
        automation_field:
            https://github.com/virt-s1/os-tests/tree/master/os_tests/tests/test_image_mode.py
        setup_teardown:
            n/a
        environment:
            n/a
        component:
            system
        bug_id:
            n/a
        is_customer_case:
            False
        testplan:
            n/a
        test_type:
            functional
        test_level:
            component
        maintainer:
            linl@redhat.com
        description: |
            Build different formats disk images for testing RHEL in image mode.
        key_steps: |
            1. Pull base bootc image and build custom bootc container image with test packages installed.
            2. Convert the custom bootc container image to bootable disk image with reqired format for testing.
        expected_result: |
            The converted bootable disk image can be deployed and tested in corrosponding platforms.
        debug_want: |
            n/a
        """
        #product_id = utils_lib.get_product_id(self)
        #if float(product_id) < 9.4:
        #    self.fail("Image Mode was supported from rhel 9.4.")
        if self.params.get('subscription_username') and self.params.get('subscription_password'):
            utils_lib.rhsm_register(self, cancel_case=True)
        utils_lib.is_pkg_installed(self, pkg_name='container-tools', is_install=True, cancel_case=True)
        #prepare containerfile
        disk_image_format = self.params.get('disk_image_format')
        bootc_base_image_url = self.params.get('bootc_base_image_url')
        if not ':' in bootc_base_image_url:
            bootc_base_image_url = bootc_base_image_url + ":latest"
        arch = utils_lib.run_cmd(self, 'uname -m', expect_ret=0, msg="Check the architechure")
        pkgs = self.params.get('pkgs')
        if pkgs:
            pkgs = pkgs.replace(",", " ")
        containerfile = self.params.get('containerfile')
        current_time = datetime.now().strftime("%y%m%d%S")
        if containerfile and containerfile.startswith("http"):
            container_url = urlparse(containerfile)
            image_mode_dir = "image_mode_" + os.path.basename(container_url.path) + "_{}_{}".format(disk_image_format, current_time)
            cmd = "sudo rm {} -rf && sudo mkdir {}".format(image_mode_dir, image_mode_dir)
            utils_lib.run_cmd(self, cmd, expect_ret=0, msg="create image_mode_dir")
            utils_lib.is_pkg_installed(self, pkg_name='curl', is_install=True, cancel_case=True)
            cmd = "sudo curl -o {}/Containerfile {}".format(image_mode_dir, containerfile)
            utils_lib.run_cmd(self, cmd, expect_ret=0, msg="download {}".format(containerfile))
        else:
            if containerfile and containerfile.startswith("/"):
                image_mode_dir = "image_mode_" + os.path.basename(containerfile) + "_{}_{}".format(disk_image_format, current_time)
                cmd = "sudo rm {} -rf && sudo mkdir {}".format(image_mode_dir, image_mode_dir)
                utils_lib.run_cmd(self, cmd, expect_ret=0, msg="create image_mode_dir")
                utils_lib.copy_file(self, local_file=containerfile, target_file_dir=image_mode_dir, target_file_name='Containerfile')
            if not containerfile:
                if not bootc_base_image_url:
                    self.skipTest("Please sepcify the base bootc container image url.")
                image_mode_dir = "image_mode_" + bootc_base_image_url.split(':')[1].replace('.','u') + "_{}_{}".format(disk_image_format, current_time)
                cmd = "sudo rm {} -rf && sudo mkdir {}".format(image_mode_dir, image_mode_dir)
                utils_lib.run_cmd(self, cmd, expect_ret=0, msg="create image_mode_dir")
                cmd = 'echo "#Containerfile" > {}/Containerfile'.format(image_mode_dir)
                utils_lib.run_cmd(self, "sudo bash -c '{}'".format(cmd), expect_ret=0, msg="create an empty Containerfile")
                default_pkgs = "cloud-init virt-what"
                if disk_image_format == 'iso':
                    default_pkgs = default_pkgs + " " + "hyperv-daemons open-vm-tools"
                if disk_image_format == 'vmdk':
                    default_pkgs = default_pkgs + " " + "open-vm-tools"
                if disk_image_format == 'vhdx':
                    default_pkgs = default_pkgs + " " + "hyperv-daemons"
                if disk_image_format == 'vhd':
                    default_pkgs = default_pkgs + " " + "hyperv-daemons"
                if pkgs:
                    pkgs = default_pkgs + " " + pkgs
                else:
                    pkgs = default_pkgs
        cmd = "sudo cat {}/Containerfile".format(image_mode_dir)
        utils_lib.run_cmd(self, cmd, expect_ret=0, msg="check Containerfile")
        if bootc_base_image_url:
            cmd = "cd {} && sudo grep -q '^FROM' Containerfile && \
sudo sed -i 's#^FROM.*#FROM {}#' Containerfile || \
sudo sed -i '1iFROM {}' Containerfile && sudo cat Containerfile".format(image_mode_dir, bootc_base_image_url, bootc_base_image_url)
            utils_lib.run_cmd(self, cmd, expect_ret=0, msg="Update the bootc base image repo to the test url")
        
        #Prepare repo file
        dnf_repo_url = self.params.get('dnf_repo_url')
        if dnf_repo_url:
            utils_lib.configure_repo(self, repo_type='dnf_repo', repo_url_param=dnf_repo_url)
            cmd = "cd {} && sudo sed -i '2iADD ./dnf.repo /etc/yum.repos.d/dnf.repo' Containerfile && sudo cat Containerfile".format(image_mode_dir)
            utils_lib.run_cmd(self, cmd, expect_ret=0, msg="Configure repo file in containerfile.")
            #if disk_image_format == 'iso':
                #utils_lib.rhsm_unregister(self, cancel_case=True)
                #self.log.info('unregister rhsm to aviod bug when creating iso disk, please register again after this case if you need.')
        cmd = "sudo cp /etc/yum.repos.d/dnf.repo ./{}/dnf.repo".format(image_mode_dir)
        utils_lib.run_cmd(self, cmd, expect_ret=0, msg="Create dnf.repo for packages installation in building custom image")
        if pkgs:
            cmd = "cd {} && sudo sed -i '3iRUN dnf install -y {} && dnf clean all' Containerfile && sudo cat Containerfile".format(image_mode_dir, pkgs)
            utils_lib.run_cmd(self, cmd, expect_ret=0, msg="Add installed pkgs to Containerfile.")

        #Prepare 05-cloud-kargs.toml file
        cmd = "cd {} && sudo grep -q '05-cloud-kargs.toml' Containerfile".format(image_mode_dir)
        ret = utils_lib.run_cmd(self, cmd, ret_status=True, msg="check if there is 05-cloud-kargs.toml in Containerfile")
        if ret == 0:
            utils_lib.run_cmd(self, """
sudo cat << EOF | sudo tee {}/05-cloud-kargs.toml
[install]
kargs = ["console=tty0", "console=ttyS0,115200n8"]
EOF
""".format(image_mode_dir), msg='create 05-cloud-kargs.toml file')

        #login container repo
        quay_io_data = self.params.get('quay_io_data')
        bootc_io_data = self.params.get('bootc_io_data')
        for io_data in [quay_io_data, bootc_io_data]:
            if io_data is not None:
                io_user = io_data.split(',')[0]
                io_pw = io_data.split(',')[1]
                io_name = io_data.split(',')[2]
                self.log.info('Login {}'.format(io_name))
                self._podman_login(io_user, io_pw, io_name)
        
        cmd = "sudo grep ^FROM {}/Containerfile | awk '{{print $(2)}}'| tr -d '\n'".format(image_mode_dir)
        bootc_base_image = utils_lib.run_cmd(self, cmd, expect_ret=0, msg='Fetch bootc base image repo')
        cmd = "sudo podman rmi {} -f".format(bootc_base_image)
        utils_lib.run_cmd(self, cmd, expect_ret=0, msg="remove old bootc base image")
        cmd = "sudo podman pull {} --arch {}".format(bootc_base_image, arch)
        utils_lib.run_cmd(self, cmd, expect_ret=0, timeout = 1200, msg="pull bootc base image")
        cmd = "sudo podman images"
        utils_lib.run_cmd(self, cmd, expect_ret=0, msg="Check all container images")
        cmd = "sudo podman inspect {} --format '{{{{.ID}}}}' | tr -d '\n'".format(bootc_base_image)
        bootc_base_image_id = utils_lib.run_cmd(self, cmd, expect_ret=0, msg="check bootc base image ID")
        cmd = "sudo podman inspect {} --format '{{{{.Digest}}}}' | tr -d '\n'".format(bootc_base_image)
        bootc_base_image_digest = utils_lib.run_cmd(self, cmd, expect_ret=0, msg="check bootc base image Digest")
        bootc_base_image_digest = bootc_base_image_digest.split(':')[1]
        bootc_base_image_name = bootc_base_image.split('/')[2].split(':')[0]
        if ':' in bootc_base_image:
            bootc_base_image_tag = bootc_base_image.split(':')[1].replace('.', 'u')
        else:
            bootc_base_image_tag = 'latest'
        inspect_json_name = "{}_{}_inspect.json".format(image_mode_dir, bootc_base_image_name, bootc_base_image_tag)
        cmd = "sudo bash -c 'podman inspect {} > {}/{}'".format(bootc_base_image, image_mode_dir, inspect_json_name)
        utils_lib.run_cmd(self, cmd, expect_ret=0, msg="check bootc base image info")
        cmd = "sudo podman inspect {} --format '{{{{.Architecture}}}}' | tr -d '\n'".format(bootc_base_image)
        bootc_image_arch = utils_lib.run_cmd(self, cmd, expect_ret=0, msg="check bootc base image Architecture")
        if bootc_image_arch == 'amd64':
            bootc_image_arch = 'x86_64'
        cmd = "sudo jq -r .[].Config.Labels.\\\"redhat.compose-id\\\" {}/{} | tr -d '\n'".format(image_mode_dir, inspect_json_name)
        bootc_base_image_compose_id = utils_lib.run_cmd(self, cmd, expect_ret=0, msg="check bootc base image compose-id")
        if not bootc_base_image_compose_id:
            bootc_base_image_compose_id = 'other'
        bootc_custom_image_name = '{}_{}_{}_{}_{}'.format(bootc_base_image_name,
                                                       bootc_base_image_tag,
                                                       disk_image_format,
                                                       bootc_image_arch,
                                                       current_time)

        #Check if the bootc image is built
        built_digest = self.params.get('bootc_base_image_digest')
        if built_digest and len(bootc_base_image_digest) >= 10:
            if bootc_base_image_digest == built_digest or bootc_base_image_digest[-10:]== built_digest:
                self.skipTest("Custom bootc image based bootc image {} Digest:{} was already built. Skip this case."
                              .format(bootc_base_image_name, bootc_base_image_digest))
        bootc_custom_image_tag = bootc_base_image_digest[-10:]

        if quay_io_data:
            bootc_custom_image = "quay.io/{}/{}:{}".format(quay_io_data.split(',')[0], bootc_custom_image_name, bootc_custom_image_tag)
        else:
            bootc_custom_image = "localhost/{}:{}".format(bootc_custom_image_name, bootc_custom_image_tag)
        cmd = "cd {} && sudo podman build -t {} . --arch {}".format(image_mode_dir, bootc_custom_image, arch)
        utils_lib.run_cmd(self, cmd, expect_ret=0, timeout = 1200, msg="Build bootc custom image")
    
        #Create bootable disks with custom bootc images
        image_name_string = image_mode_dir.split('_')
        image_name_string = image_name_string[:-2]
        pre_image_name = '_'.join(image_name_string)
        bootc_image_builder = self.params.get('bootc_image_builder')
        if not bootc_image_builder:
            if 'rhel' in bootc_base_image:
                bootc_image_builder = bootc_base_image.replace('rhel-bootc','bootc-image-builder')
            else:
                self.skipTest("Please sepcify the bootc_image_builder.")

        if disk_image_format == 'ami':
            utils_lib.is_pkg_installed(self, pkg_name='awscli2', is_install=True, cancel_case=True)
            ami_name = '{}_{}_{}_{}'.format(pre_image_name, bootc_custom_image_name, bootc_custom_image_tag, bootc_base_image_compose_id)
            aws_info = self.params.get('aws_info')
            if aws_info and aws_info.split(',')[2]:
                aws_region = aws_info.split(',')[2]
            if aws_info and aws_info.split(',')[3]:
                aws_bucket = aws_info.split(',')[3]
            else:
                aws_bucket = 'rh-image-files'
            if aws_info and aws_info.split(',')[0] and aws_info.split(',')[1]:
                cmd = "sudo podman run --rm -it --privileged --pull=newer --tls-verify=false \
--security-opt label=type:unconfined_t -v /var/lib/containers/storage:/var/lib/containers/storage \
--env AWS_ACCESS_KEY_ID={} --env AWS_SECRET_ACCESS_KEY={} {} --type ami --target-arch {} --local --aws-ami-name {} \
--aws-region {} --aws-bucket {} {}".format(
                                         aws_info.split(',')[0], 
                                         aws_info.split(',')[1], 
                                         bootc_image_builder,
                                         bootc_image_arch,
                                         ami_name,
                                         aws_region,
                                         aws_bucket,
                                         bootc_custom_image)
                utils_lib.run_cmd(self, cmd, timeout=3600, is_log_cmd=False, msg='Create ami for image mode testing based on {}'.format(bootc_base_image_compose_id))

            else:
                cmd = "sudo grep region .aws/config | awk '{print $(3)}'| tr -d '\n'"
                aws_region = utils_lib.run_cmd(self, cmd, msg='Check aws region')
                if not aws_region:
                    self.FailTest('Please configure awscli')
                else:
                    cmd = "sudo podman run --rm -it --privileged --pull=newer -v ./.aws:/root/.aws:ro \
--env AWS_PROFILE=default -v /var/lib/containers/storage:/var/lib/containers/storage {} --local --type ami \
--target-arch {} --aws-ami-name {} --aws-region {} --aws-bucket {} {}".format(
                                                                      bootc_image_builder,
                                                                      bootc_image_arch,
                                                                      ami_name,
                                                                      aws_region,
                                                                      aws_bucket,
                                                                      bootc_custom_image)
                    utils_lib.run_cmd(self, cmd, timeout=3600, msg='Create ami for image mode testing based on {}'.format(bootc_base_image_compose_id))
            cmd = "aws ec2 describe-images --filters 'Name=name,Values={}' --query 'Images[*].ImageId' --output text | tr -d '\n'".format(ami_name)
            ami_id = utils_lib.run_cmd(self, cmd, msg='check ami id')
            if ami_id:
                self.log.info("AMI name:{} ID:{} based on bootc image {} compose-id:{} Digest:{} is uploaded \
to AWS {}".format(ami_name, ami_id, bootc_base_image, bootc_base_image_compose_id, bootc_base_image_digest, aws_region))
            else:
                self.FailTest('Failed to upload AMI')
        else:
            config_toml_file = self.params.get('config_toml_file')
            config_toml_info = self.params.get('config_toml_info')
            if config_toml_file:
                utils_lib.copy_file(self, local_file=config_toml_file, target_file_dir=image_mode_dir, target_file_name='config.toml')
            elif config_toml_info:
                #Note the key will display in the disk convert log if you specify it.
                utils_lib.run_cmd(self, """
sudo cat << EOF | sudo tee {}/config.toml
[[customizations.user]]
name = "{}"
password = "{}"
key = "ssh-rsa {}"
groups = ["wheel"]
EOF
""".format(image_mode_dir, config_toml_info.split(',')[0], config_toml_info.split(',')[1], config_toml_info.split(',')[2]),
           is_log_cmd=False,
           msg='create config_toml file')
 
            #Create directory for converted disk images
            output_dir_name = 'output_{}_{}'.format(bootc_custom_image_name, bootc_custom_image_tag)
            output_dir = "{}/{}".format(image_mode_dir, output_dir_name)
            cmd = "sudo rm {} -rf && sudo mkdir {}".format(output_dir, output_dir)
            utils_lib.run_cmd(self, cmd, expect_ret=0, msg="Create output directory")

            #Convert custom bootc container image to disk image
            disk_image_type = disk_image_format
            if disk_image_format in ['vhdx', 'vhd']:
                disk_image_type = 'qcow2'   
            cmd = "cd {} && sudo podman run --rm -it --privileged --pull=newer --security-opt \
label=type:unconfined_t -v ./config.toml:/config.toml -v ./{}:/output -v \
/var/lib/containers/storage:/var/lib/containers/storage {} --type {} --target-arch {} \
--config /config.toml --local {}".format(image_mode_dir, 
                                         output_dir_name, 
                                         bootc_image_builder, 
                                         disk_image_type, 
                                         bootc_image_arch, 
                                         bootc_custom_image)
            utils_lib.run_cmd(self,
                            cmd,
                            expect_ret=0,
                            timeout = 3600,
                            msg="Create container disk image {} for image mode testing based on {}".format(bootc_custom_image, bootc_base_image_compose_id))

            manifest_file = 'manifest{}'.format(output_dir_name.replace('output',''))
            cmd = "sudo mv {}/manifest-{}.json {}/{}".format(output_dir, disk_image_type, image_mode_dir, manifest_file)
            utils_lib.run_cmd(self, cmd, expect_ret=0, msg='move manifest-{}.json to {}'.format(disk_image_type, manifest_file))
            utils_lib.is_cmd_exist(self,"qemu-img")
            if disk_image_format == 'vhdx':
                cmd = "sudo qemu-img convert -O vhdx {}/qcow2/disk.qcow2 {}/qcow2/disk.vhdx".format(output_dir, output_dir)
                utils_lib.run_cmd(self, cmd, expect_ret=0, msg='convert qcow2 disk to vhdx disk')
            if disk_image_format == 'vhd':
                cmd = "sudo qemu-img convert -f qcow2 -o subformat=fixed,force_size -O vpc {}/qcow2/disk.qcow2 {}/qcow2/disk.vhd".format(output_dir, output_dir)
                utils_lib.run_cmd(self, cmd, expect_ret=0, msg='convert qcow2 disk to vhd disk')
            disk_dir = disk_image_type
            disk_file = 'disk.{}'.format(disk_image_format)
            if disk_image_type == 'iso':
                disk_file = 'install.iso'
                disk_dir = 'bootiso'
            disk_image_name = "{}_{}".format(pre_image_name, output_dir_name.replace('output_',''))
            cmd = "sudo mv {}/{}/{} {}/{}.{}".format(output_dir, disk_dir, disk_file, image_mode_dir, disk_image_name, disk_file.split('.')[1])
            utils_lib.run_cmd(self, cmd, expect_ret=0, msg='move {} to {}'.format(disk_file, image_mode_dir))
            #uploade the output to attachment
            utils_lib.save_file(self, file_dir=image_mode_dir, file_name="Containerfile")
            utils_lib.save_file(self, file_dir=image_mode_dir, file_name=inspect_json_name)
            utils_lib.save_file(self, file_dir=image_mode_dir, file_name=manifest_file)
            #Save the created bootable bootc image/disk to attachments in log and delete the image_mode_dir.
            #Or if you'd like to copy the disk file to your test environment by manual,
            #please specify --upload_image to no.
            upload_image = str(self.params.get('upload_image'))
            if upload_image:
                upload_image = upload_image.strip().lower()
                if upload_image in ["no", "n", "false"]:
                    self.log.info("Please copy Disk image {}/{}.{} based on bootc image {} \
compose-id:{} Digest:{} to your test environment.".format(image_mode_dir,
                                                          disk_image_name, 
                                                          disk_image_format,
                                                          bootc_base_image,
                                                          bootc_base_image_compose_id,
                                                          bootc_base_image_digest))
            else:
                utils_lib.save_file(self, file_dir=image_mode_dir, file_name='{}.{}'.format(disk_image_name, disk_image_format))
                cmd = "sudo rm -rf {}".format(image_mode_dir)
                utils_lib.run_cmd(self, cmd, expect_ret=0, msg="delete the {}".format(image_mode_dir))

        #delete container images
        for image in [bootc_base_image, bootc_custom_image, bootc_image_builder]:
            cmd = "sudo podman rmi {} -f".format(image)
            utils_lib.run_cmd(self, cmd, expect_ret=0, msg='remove container image {}'.format(image))
   
    def tearDown(self):
        utils_lib.finish_case(self)
        pass

if __name__ == '__main__':
    unittest.main()
