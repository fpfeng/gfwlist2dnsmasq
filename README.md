#here goes another gfwlist2dnsmasq script

##常用
举例，ipset名称为`gfw`，地址`127.0.0.1:1053`，输出文件`gfw_ipset.conf`                       
`gfwlist2dnsmasq.py -i gfw -d 127.0.0.1 -p 1053 -o gfw_ipset.conf`

##不常用          
`-l gfwlist.txt` 使用本地gfwlist.txt(必须为原始base64压缩格式)          
`-o -` 输出到STDOUT     
`-i -` 不生成ipset规则 

##感谢
9成代码复制以下项目，还有1成来自google。。。           
[https://github.com/JinnLynn/genpac](https://github.com/JinnLynn/genpac)             
[https://github.com/cokebar/gfwlist2dnsmasq](https://github.com/cokebar/gfwlist2dnsmasq)                     
