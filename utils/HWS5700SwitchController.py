#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import re
import os
try:
    from .utils.NSRSSH import *
except Exception:
    ABS_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
    sys.path.append(ABS_PATH)
    from utils.NSRSSH import *



class HWS5700SwitchController(NSRSSH):
    # def __init__(self, login_info, logged_in_symbol='<Quidway>', is_debug_mode=False,
    #              timeout=30, try_login_max_times=3, acl_number_shift=1000):
    #     super().__init__(login_info=login_info, logged_in_symbol=logged_in_symbol, is_debug_mode=is_debug_mode,
    #                      timeout=timeout, try_login_max_times=try_login_max_times)
    #     self.__acl_number_shift = acl_number_shift

    def __init__(self, timeout=30, acl_number_shift=1000):
        super(self.__class__, self).__init__(timeout=timeout)
        self.__acl_number_shift = acl_number_shift

    def get_vlan_list(self):
        vlan_list = []
        if self._cmd_exec_result == 0:
            each_pair = ['display vlan', '\[Quidway\]']
            self._print_debug_info(each_pair)
            self._child.sendline(each_pair[0])

            while True:
                j = self._child.expect([pexpect.TIMEOUT, pexpect.EOF, each_pair[1], 'More'],
                                 timeout=30)

                if 0 == j:
                    self._print_error()
                    self._cmd_exec_result = -1
                    break
                elif 1 == j:
                    self._print_error()
                    self._cmd_exec_result = -2
                    break
                elif 2 == j:
                    for vlan_id in re.findall(r'[0-9]+\s+common', self._child.before.decode("utf-8")):
                        pattern = r'\s*(?P<vlan_id>[0-9]+)\s+\S*'
                        vlan_list.append(re.search(pattern, vlan_id).group('vlan_id'))
                    break
                elif 3 == j:
                    for vlan_id in re.findall(r'[0-9]+\s+common', self._child.before.decode("utf-8")):
                        pattern = r'\s*(?P<vlan_id>[0-9]+)\s+\S*'
                        vlan_list.append(re.search(pattern, vlan_id).group('vlan_id'))
                    # vlan_list.remove('1')

                    self._child.sendline(' ')

            vlan_list = list(set(vlan_list))
        else:
            log_hw_s5700.info('SSH Error!')
        return vlan_list

    def enter_system_view(self):
        input_expect_pairs_list = [
                             ['system-view', '\[Quidway\]'],
        ]

        self._exec_command_sequence(input_expect_pairs_list)
        return self

    def save_config(self):
        input_expect_pairs_list = [
                                  ['quit', '<Quidway>'],
                                  ['save', 'continue?'],
                                  ['Y', '<Quidway>'],
        ]

        self._exec_command_sequence(input_expect_pairs_list)
        return self

    def vlan_add(self, vlan_id):
        '''
        创建vlan
        :param child: ssh实例
        :param vlan_id: vlan_id
        :return:
        '''
        #1.命令序列设置
        input_expect_pairs_list = [
                                  ['vlan %s' % vlan_id, '\[Quidway-vlan%s\]' % vlan_id],
                                  # ['vlan ' + vlan_id, '\[Quidway-vlan' + vlan_id + '\]'],
                                  ['quit', '\[Quidway\]'],

        ]
        self._exec_command_sequence(input_expect_pairs_list)  # 2.执行命令序列
        return self

    def vlan_add_batch(self, vlan_id_list):
        '''
        创建vlan
        :param child: ssh实例
        :param vlan_id: vlan_id
        :return:
        '''
        #1.命令序列设置
        input_expect_pairs_list = [
                             ['vlan batch ' + ' '.join([str(vlan_id) for vlan_id in vlan_id_list]), '\[Quidway\]'],#1.1创建对应id的vlan
        ]
        self._exec_command_sequence(input_expect_pairs_list)  # 2.执行命令序列
        return self

    def vlan_remove(self, vlan_id):
        '''
        删除vlan
        :param child:
        :param vlan_id:
        :return:
        '''
        #1.命令序列设置
        input_expect_pairs_list = [
                             ['undo interface vlanif %s' % vlan_id, '\[Quidway\]'],#1.1删除对应id的vlanif
                             ['undo vlan %s' % vlan_id, '\[Quidway\]'], #1.2删除对应id的vlan
        ]
        self._exec_command_sequence(input_expect_pairs_list)#2.执行命令序列
        return self

    def vlanif_gateway_add(self, vlan_id, vlanif_info):
        '''
        添加vlanif网关
        :param child:
        :param vlan_id:
        :param vlanif_info:
        :return:
        '''
        if 'sub' not in vlanif_info['type']:
            vlanif_info['type'] = ''
        #1.命令序列设置
        input_expect_pairs_list = [

                                  ['interface vlanif ' + vlan_id, '\[Quidway-Vlanif' + vlan_id + '\]'],#1.1进入对应id的vlanif
                                  ['ip address ' + vlanif_info['gateway'] + ' ' + vlanif_info['type'], '\[Quidway-Vlanif' + vlan_id + '\]'],#1.2添加网关ip
                                  ['quit', '\[Quidway\]'],#1.3退出vlanif

        ]
        self._exec_command_sequence(input_expect_pairs_list)#2.执行命令序列
        return self

    def vlanif_gateway_remove(self, vlan_id, vlanif_info):
        '''
        删除vlanif网关
        :param child:
        :param vlan_id:
        :param vlanif_info:
        :return:
        '''
        if 'sub' not in vlanif_info['type']:
            vlanif_info['type'] = ''
        #1.命令序列设置
        input_expect_pairs_list = [

                                  ['interface vlanif ' + vlan_id, '\[Quidway-Vlanif' + vlan_id + '\]'],#1.1进入对应id的vlanif
                                  ['undo ip address ' + vlanif_info['gateway'] + ' ' + vlanif_info['type'], '\[Quidway-Vlanif' + vlan_id + '\]'],#1.2删除网关ip
                                  ['quit', '\[Quidway\]'],#1.3退出vlanif

        ]
        self._exec_command_sequence(input_expect_pairs_list)#2.执行命令序列
        return self

    def vlanif_remove(self, vlan_id):
        '''
        删除vlanif
        :param child:
        :param vlan_id:
        :return:
        '''
        #1.命令序列设置
        input_expect_pairs_list = [
                                  ['undo interface vlanif ' + vlan_id, '\[Quidway\]'],#1.1删除对应id的vlanif
        ]

        self._exec_command_sequence(input_expect_pairs_list)#2.执行命令序列

        return self

    def eth_port_init(self, port_group):
        '''
        初始化物理端口
        :param child:
        :param port_group:
        :return:
        '''
        #1.命令序列设置
        input_expect_pairs_list = [
                                  ['undo port-group all', '\[Quidway\]'],#1.1删除所有端口组
                                  ['port-group vlan_group_tmp', '\[Quidway-port-group-vlan_group_tmp\]'],#1.2创建临时端口组
                                  ['group-member ' + ' '.join(['G0/0/'+str(port) for port in port_group]), '\[Quidway-port-group-vlan_group_tmp\]'],#1.3将对应id的vlan加入临时端口组

                                  ['undo port trunk allow-pass vlan 2 to 4094', '\[Quidway-port-group-vlan_group_tmp\]'],#1.4删除端口组内vlan的trunk信息
                                  ['undo port default vlan', '\[Quidway-port-group-vlan_group_tmp\]'],#1.5删除端口组内vlan的access信息
                                  ['undo port link-type', '\[Quidway-port-group-vlan_group_tmp\]'],#1.6删除端口组内vlan的配置类型
                                  ['quit', '\[Quidway\]'],#1.7退出临时端口组

        ]

        self._exec_command_sequence(input_expect_pairs_list)#2.执行命令序列
        return self

    def eth_port_config_access(self, vlan_id, port_group):
        '''
        配置物理端口为access类型
        :param child:
        :param vlan_id:
        :param port_group:
        :return:
        '''
        #1.命令序列设置
        input_expect_pairs_list = [
                                  ['undo port-group all', '\[Quidway\]'],#1.1删除所有端口组
                                  ['port-group vlan_group_tmp', '\[Quidway-port-group-vlan_group_tmp\]'],#1.2创建临时端口组
                                  ['group-member ' + ' '.join(['G0/0/'+str(port) for port in port_group]), '\[Quidway-port-group-vlan_group_tmp\]'],#1.3将对应id的vlan加入临时端口组
                                  ['port link-type access',  '\[Quidway-port-group-vlan_group_tmp\]'],#1.4将端口组内端口配置为access类型
                                  ['port default vlan ' + vlan_id, '\[Quidway-port-group-vlan_group_tmp\]'],#1.5配置为access的vlan信息
                                  ['quit', '\[Quidway\]'],#1.6退出临时端口组
        ]

        self._exec_command_sequence(input_expect_pairs_list)#2.执行命令序列
        return self

    def eth_port_config_trunk(self, vlan_id_group, port_group):
        '''
        配置物理端口为trunk
        :param child:
        :param vlan_id_group:
        :param port_group:
        :return:
        '''
        #1.命令序列设置
        input_expect_pairs_list = [
                                  ['undo port-group all', '\[Quidway\]'],#1.1删除所有端口组
                                  ['port-group vlan_group_tmp', '\[Quidway-port-group-vlan_group_tmp\]'],#1.2创建临时端口组
                                  ['group-member ' + ' '.join(['G0/0/'+str(port) for port in port_group]), '\[Quidway-port-group-vlan_group_tmp\]'],#1.3将对应id的vlan加入临时端口组
                                  ['port link-type trunk',  '\[Quidway-port-group-vlan_group_tmp\]'],#1.4将端口组内端口配置为trunk类型
                                  ['port trunk allow-pass vlan ' + ' '.join([str(vlan_id_tmp) for vlan_id_tmp in vlan_id_group]), '\[Quidway-port-group-vlan_group_tmp\]'],#1.5配置允许通过vlan信息
                                  ['quit', '\[Quidway\]'],#1.6退出临时端口组
        ]

        self._exec_command_sequence(input_expect_pairs_list)#2.执行命令序列

        return self

    def eth_port_config_trunk_vlan_allowpass_all(self, port_group):

        input_expect_pairs_list = [
                                  ['undo port-group all', '\[Quidway\]'],
                                  ['port-group vlan_group_tmp', '\[Quidway-port-group-vlan_group_tmp\]'],
                                  ['group-member ' + ' '.join(['G0/0/'+str(port) for port in port_group]), '\[Quidway-port-group-vlan_group_tmp\]'],
                                  ['port link-type trunk',  '\[Quidway-port-group-vlan_group_tmp\]'],
                                  ['port trunk allow-pass vlan all', '\[Quidway-port-group-vlan_group_tmp\]'],
                                  ['quit', '\[Quidway\]'],
        ]

        self._exec_command_sequence(input_expect_pairs_list)

        return self

    def acl_add(self, vlan_id):
        '''
        创建acl
        :param child:
        :param vlan_id:
        :return:
        '''

        acl_number = str(int(vlan_id) + self.__acl_number_shift)
        #1.命令序列设置
        input_expect_pairs_list = [
                                  #['undo acl ' + acl_number, '\[Quidway\]'],
                                  ['acl ' + acl_number, '\[Quidway-acl-adv-' + acl_number + '\]'],#1.1创建对应acl_number的acl
                                  #['rule 4294967294 deny ip', '\[Quidway-acl-adv-' + acl_number + '\]'],
                                  #['display this', 'rule 4294967294 deny ip'],
                                  ['quit', '\[Quidway\]'],#1.1退出对应acl_number的acl

        ]

        self._exec_command_sequence(input_expect_pairs_list)#2.执行命令序列
        return self

    def acl_remove(self, vlan_id):
        '''
        移除acl
        :param child:
        :param vlan_id:
        :return:
        '''
        acl_number = str(int(vlan_id) + self.__acl_number_shift)

        #1.命令序列设置
        input_expect_pairs_list = [
                                  ['undo acl ' + acl_number, '\[Quidway\]'],#1.1移除对应acl_number的acl
        ]

        self._exec_command_sequence(input_expect_pairs_list)#2.执行命令序列

        return self

    def acl_add_deny_any(self):
        '''
        创建拒绝所有ip流量的acl规则
        :param child:
        :return:
        '''
        #1.命令序列设置
        input_expect_pairs_list = [
                                  ['acl 2000', '\[Quidway-acl-basic-2000\]'],#1.1创建acl_number为2000的acl
                                  ['rule deny', '\[Quidway-acl-basic-2000\]'],#1.2规则设置为拒绝所有ip流量
                                  #['display this', 'rule 4294967294 deny ip'],
                                  ['quit', '\[Quidway\]'],#1.3退出acl
        ]

        #2.执行命令序列
        self._exec_command_sequence(input_expect_pairs_list)

        return self

    def acl_rule_add(self, vlan_id,  rule_info):
        '''
        添加acl规则
        :param child:
        :param vlan_id:
        :param rule_info:
        :return:
        '''
        acl_number = str(int(vlan_id) + self.__acl_number_shift)

        #1.命令序列设置
        input_expect_pairs_list = [
                                  ['acl ' + acl_number, '\[Quidway-acl-adv-' + acl_number + '\]'],#1.1进入对应acl_number的acl
                                  #['undo rule 4294967294', '\[Quidway-acl-adv-' + acl_number + '\]'],
                                  ['rule ' + ' permit ip source ' + rule_info['src_ip_with_mask'] + ' destination ' + rule_info['dst_ip_with_mask'],#1.2允许对应源ip和目的ip的流量通过
                                   '\[Quidway-acl-adv-' + acl_number + '\]'],
                                  #['rule ' + rule_info['rule_num'] + ' permit ip source ' + rule_info['src_ip_with_mask'] + ' destination ' + rule_info['dst_ip_with_mask'],
                                  #'\[Quidway-acl-adv-' + acl_number + '\]'],
                                  #['rule 4294967294 deny ip', '\[Quidway-acl-adv-' + acl_number + '\]'],
                                  ['quit', '\[Quidway\]'],#1.3退出acl
        ]

        #2.执行命令序列
        self._exec_command_sequence(input_expect_pairs_list)

        return self

    def acl_rule_remove(self, vlan_id, rule_info):

        acl_number = str(int(vlan_id) + self.__acl_number_shift)

        input_expect_pairs_list = [
                                  ['acl ' + acl_number, '\[Quidway-acl-adv-' + acl_number + '\]'],
                                  ['undo rule ' + rule_info['rule_num'], '\[Quidway-acl-adv-' + acl_number + '\]'],
                                  ['quit', '\[Quidway\]'],
        ]

        self._exec_command_sequence(input_expect_pairs_list)

        return self

    def traffic_add(self, vlan_id):
        '''
        创建对应vlan的流策略 流行为 流分类
        :param child:
        :param vlan_id:
        :return:
        '''
        traffic_classifier_name = 'c_vlan_' + vlan_id
        traffic_behavior_name = 'b_vlan_' + vlan_id
        traffic_policy_name = 'p_vlan_' + vlan_id
        acl_number = str(int(vlan_id) + self.__acl_number_shift)

        #1.命令序列设置
        input_expect_pairs_list = [
                                  ['traffic classifier ' + traffic_classifier_name, '\[Quidway-classifier-' + traffic_classifier_name + '\]'],#1.1创建流分类
                                  ['if-match ' + 'acl ' + acl_number, '\[Quidway-classifier-' + traffic_classifier_name + '\]'],#1.2绑定acl
                                  ['if-match ' + 'acl 2000', '\[Quidway-classifier-' + traffic_classifier_name + '\]'],#1.3绑定acl_number为 2000的acl
                                  #['display this', 'if-match ' + 'acl ' + acl_number],
                                  ['quit', '\[Quidway\]'],#1.4退出acl

                                  ['traffic behavior ' + traffic_behavior_name, '\[Quidway-behavior-' + traffic_behavior_name + '\]'],#1.5创建流行为
                                  ['quit', '\[Quidway\]'],#1.6退出流行为

                                  ['traffic policy ' + traffic_policy_name, '\[Quidway-trafficpolicy-' + traffic_policy_name + '\]'],#1.6创建流策略
                                  ['classifier ' + traffic_classifier_name + ' behavior ' + traffic_behavior_name,'\[Quidway-trafficpolicy-' + traffic_policy_name + '\]'],#1.7绑定流分类和流行为
                                  #['display this', 'classifier ' + traffic_classifier_name + ' behavior ' + traffic_behavior_name],
                                  ['quit', '\[Quidway\]'],#1.8退出流策略

                                  ['vlan ' + vlan_id, '\[Quidway-vlan' + vlan_id + '\]'],#1.9进入对应id的vlan
                                  ['traffic-policy ' + traffic_policy_name + ' inbound', '\[Quidway-vlan' + vlan_id + '\]'],#1.10绑定流策略
                                  #['display this', 'traffic-policy ' + traffic_policy_name + ' inbound'],
                                  ['quit', '\[Quidway\]'],#1.11退出vlan
        ]

        #2.执行命令序列
        self._exec_command_sequence(input_expect_pairs_list)

        return self

    def traffic_remove(self, vlan_id):
        '''
        清除对应vlan的流策略 流行为 流分类
        :param child:
        :param vlan_id:
        :return:
        '''
        traffic_classifier_name = 'c_vlan_' + vlan_id
        traffic_behavior_name = 'b_vlan_' + vlan_id
        traffic_policy_name = 'p_vlan_' + vlan_id
        acl_number = str(int(vlan_id) + self.__acl_number_shift)
        #1.命令序列设置
        input_expect_pairs_list = [
                                  ['vlan ' + vlan_id, '\[Quidway-vlan' + vlan_id + '\]'],#1.1进入对应id的vlan
                                  ['undo traffic-policy ' + traffic_policy_name + ' inbound', '\[Quidway-vlan' + vlan_id + '\]'],#1.2取消vlan与流策略的绑定
                                  ['quit', '\[Quidway\]'],#1.3退出vlan

                                  ['undo traffic policy ' + traffic_policy_name, '\[Quidway\]'],#1.4清除流策略

                                  ['undo traffic classifier ' + traffic_classifier_name, '\[Quidway\]'],#1.4清除流分类

                                  ['undo traffic behavior ' + traffic_behavior_name, '\[Quidway\]'],#1.4清除流行为

        ]
        #2.执行命令序列
        self._exec_command_sequence(input_expect_pairs_list)

        return self

# python
# "{'methip':'172.19.40.150','user':'nsr','password':'nsr12345'}"
# 10
# del
# "{'rule_num':'333','src_ip':'192.168.10.0','src_mask':'0.0.0.255' ,'dst_ip':'192.168.20.0','dst_mask':'0.0.0.255'}"

if __name__ == "__main__":


    #tnodedatanet = db.read_records(ACL, dict_where= dict(id=tnodedatanet_id))

    #switch_login_info ="{'methip':'" + methip + "','user':'" + user + "','password':'" + password + "'}"


    #assert len(sys.argv) == 4




#vlan: "{'methip':'172.19.40.200','user':'nsr','password':'nsr12345'}" "[2040]" vlan add
#vlan: "{'methip':'172.19.40.200','user':'nsr','password':'nsr12345'}" "[2030]" vlan del
#access: "{'methip':'172.19.40.200','user':'nsr','password':'nsr12345'}" 2001 access add "[10,11]"
#trunk: "{'methip':'172.19.40.200','user':'nsr','password':'nsr12345'}" "[8,9,11]" trunk add "[1, 2, 5, 16, 19]"
#trunk: "{'methip':'172.19.40.200','user':'nsr','password':'nsr12345'}" "[8,9,11]" trunk del "[1, 2, 5, 16, 19]"
#vlanif: "{'methip':'172.19.40.200','user':'nsr','password':'nsr12345'}" "[40]" vlanif add "[{'type': 'sub', 'gateway': '192.222.1.1 255.255.255.0'}]"
#acl: "{'methip':'172.19.40.200','user':'nsr','password':'nsr12345'}" "[40]" acl add
#clear all: "{'methip':'172.19.40.200','user':'nsr','password':'nsr12345'}" all clear
#rule: "{'methip':'172.19.40.200','user':'nsr','password':'nsr12345'}" "[10]" rule add "[{'rule_num':'355','src_ip_with_mask':'192.168.30.0 0.0.0.255' ,'dst_ip_with_mask':'192.168.20.0 0.0.0.255'},{'rule_num':'366','src_ip':'192.168.40.0','src_mask':'0.0.0.255' ,'dst_ip':'192.168.20.0','dst_mask':'0.0.0.255'}]"
#traffic: "{'methip':'172.19.40.200','user':'nsr','password':'nsr12345'}" 2001 traffic add

    switch_login_info = eval(sys.argv[1])

    # switch_login_info = {'methip':'172.19.40.200','user':'nsr','password':'nsr12345'}
    # vlan_id_list = [333,444,555]
    hw_s5700 = HWS5700SwitchController().connect(login_info=switch_login_info, logged_in_symbol='<Quidway>').enter_system_view()
    # hw_s5700.vlan_create_batch(vlan_id_list)

    vlan_id = sys.argv[2]


    if 'vlan' == sys.argv[3]:
    #1.命令类型为vlan
        vlan_id_list = eval(vlan_id)
        if 'add' == sys.argv[4]:
        #1.1命令操作为add
            hw_s5700.acl_add_deny_any()
            #1.1.1取出每一个vlan_id进行创建
            for vlan in vlan_id_list:
                vlan = str(vlan)
                hw_s5700.vlan_add(vlan)
                hw_s5700.acl_add(vlan)
                hw_s5700.traffic_add(vlan)
        elif 'del' == sys.argv[4]:
        #1.2命令操作为del
            #1.2.1取出每一个vlan_id进行删除
            for vlan in vlan_id_list:
                vlan = str(vlan)
                hw_s5700.traffic_remove(vlan)
                hw_s5700.acl_remove(vlan)
                hw_s5700.vlan_remove(vlan)
    elif 'vlanif' == sys.argv[3]:
    #2.命令类型为vlanif
        vlan_id_list = eval(vlan_id)
        vlanif_info_list = eval(sys.argv[5])
        if 'add' == sys.argv[4]:
        #2.1命令操作为add
            for vlan, vlanif_info in zip(vlan_id_list, vlanif_info_list):
            #2.1.1取出每一个vlan_id进行创建
                vlan = str(vlan)
                hw_s5700.vlanif_gateway_add(vlan, vlanif_info)
        elif 'del' == sys.argv[4]:
        #2.2命令操作为add
            for vlan, vlanif_info in zip(vlan_id_list, vlanif_info_list):
                #2.2.1取出每一个vlan_id进行删除
                vlan = str(vlan)
                hw_s5700.vlanif_gateway_remove(vlan, vlanif_info)
    elif 'traffic' == sys.argv[3]:
    #3.命令类型为traffic
        if 'add' == sys.argv[4]:
        #3.1命令操作为add
            hw_s5700.traffic_add(vlan_id)
        elif 'del' == sys.argv[4]:
        #3.2命令操作为del
            hw_s5700.traffic_remove(vlan_id)
    elif 'acl' == sys.argv[3]:
    #4.命令类型为traffic
        if 'add' == sys.argv[4]:
        #4.1命令操作为add
            hw_s5700.acl_add(vlan_id)
        elif 'del' == sys.argv[4]:
        #4.2命令操作为del
            hw_s5700.acl_remove(vlan_id)
    elif 'rule' == sys.argv[3]:
    #5.命令类型为rule
        vlan_id_list = eval(vlan_id)
        acl_rule_info = eval(sys.argv[5])
        if 'add' == sys.argv[4]:
        #5.1命令操作为add
            for vlan, rule in zip(vlan_id_list, acl_rule_info):
                vlan = str(vlan)
                hw_s5700.acl_rule_add(vlan, rule)
        elif 'del' == sys.argv[4]:
        #5.2命令操作为del
            for vlan, rule in zip(vlan_id_list, acl_rule_info):
                vlan = str(vlan)
                hw_s5700.acl_rule_remove(vlan, rule)
    # elif 'rule' == sys.argv[3]:
    #     vlan_id_list = eval(vlan_id)
    #     acl_rule_info = eval(sys.argv[5])
    #     if 'add' == sys.argv[4]:
    #         for rule in acl_rule_info:
    #             acl_rule_add(rule)
    #     elif 'del' == sys.argv[4]:
    #         for rule in acl_rule_info:
    #             acl_rule_remove(rule)
    elif 'access' == sys.argv[3]:
        vlan = str(vlan_id)
        if 'add' == sys.argv[4]:
        #1.1命令操作为add
            hw_s5700.acl_add_deny_any()
            #1.1.1取出每一个vlan_id进行创建
            port_group = eval(sys.argv[5])
            hw_s5700.vlan_add(vlan)
            hw_s5700.eth_port_init(port_group)
            hw_s5700.eth_port_config_access(vlan, port_group)
        elif 'del' == sys.argv[4]:
        #1.2命令操作为del
            #1.2.1取出每一个vlan_id进行删除
            port_group = eval(sys.argv[5])
            hw_s5700.eth_port_init(port_group)
            hw_s5700.vlan_remove(vlan)
    elif 'trunk' == sys.argv[3]:
    #6.命令类型为trunk
        port_group = eval(sys.argv[5])
        if 'add' == sys.argv[4]:
        #6.1命令操作为add
            if 'all' == vlan_id:
                hw_s5700.eth_port_init(port_group)
                hw_s5700.eth_port_config_trunk_vlan_allowpass_all(port_group)
            else:
                vlan_id = eval(vlan_id)
                hw_s5700.eth_port_init(port_group)
                hw_s5700.eth_port_config_trunk(vlan_id, port_group)
        elif 'del' == sys.argv[4]:
        #6.2命令操作为del
            hw_s5700.eth_port_init(port_group)
    elif 'clear' == sys.argv[3]:
        vlan_list = hw_s5700.get_vlan_list()
        port_group = []
        for i in range(1, 49):
            port_group.append(i)
        # hw_s5700.eth_port_init(port_group)
        # print.info(vlan_list)
        for vlan in vlan_list:
            vlan = str(vlan)
            hw_s5700.traffic_remove(vlan)
            hw_s5700.acl_remove(vlan)
            hw_s5700.vlan_remove(vlan)

    hw_s5700.save_config()
    hw_s5700.disconnect()

    if 0 == hw_s5700.get_cmd_exec_result():
        print("Success")
    elif -1 == hw_s5700.get_cmd_exec_result():
        print("SSH Error: Timeout")
    elif -2 == hw_s5700.get_cmd_exec_result():
        print("SSH Error: Connection Broken")
