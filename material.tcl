model basic -ndm 3 -ndf 6

#===========�������������������ѹӦ��==============================

set f [open ./ecu.txt w+]


#============================================================

#HRB400�ֽ���ϣ�������ǿ��

set HRB400(1)      1;             
set HRB400(2)      400.0e3;         # ����Ӧ��
set HRB400(3)      510.0e3;         # ����Ӧ��
set HRB400(4)      2.0e8;           # ����ģ��
set HRB400(5)      2.0e6;           # ǿ���γ�ʼ�ն�
set HRB400(6)      0.045;           # ǿ���ο�ʼӦ��
set HRB400(7)      0.100;             # ����Ӧ��

uniaxialMaterial ReinforcingSteel $HRB400(1) $HRB400(2) $HRB400(3) $HRB400(4) $HRB400(5) $HRB400(6) $HRB400(7)
#************************************************************

#�����������C35��Manderģ��

set C35_Cover(1)      11;
set C35_Cover(2)     -23800;        #��ѹǿ�ȱ�׼ֵ
set C35_Cover(3)     -0.0020;       #��ֵӦ��
set C35_Cover(4)     -0.004;        #ѹ��Ӧ�� 

uniaxialMaterial Concrete04 $C35_Cover(1)  $C35_Cover(2)    $C35_Cover(3)     $C35_Cover(4)     [expr sqrt(-1*$C35_Cover(2)/1000)*(5e6)]    
#************************************************************

#�����������C50��Manderģ��

set C50_Cover(1)      12;
set C50_Cover(2)     -32400;        #��ѹǿ�ȱ�׼ֵ
set C50_Cover(3)     -0.0020;       #��ֵӦ��
set C50_Cover(4)     -0.004;        #ѹ��Ӧ�� 

uniaxialMaterial Concrete04 $C50_Cover(1)  $C50_Cover(2)    $C50_Cover(3)     $C50_Cover(4)     [expr sqrt(-1*$C50_Cover(2)/1000)*5e6]    
#************************************************************


#Pile2.0������������C35��Manderģ��
set name			    "Pile2_0m"
set C35_Core_Pile2_0(1)      21;
set C35_Core_Pile2_0(2)     -26667;        #��ѹǿ��
set C35_Core_Pile2_0(3)     -0.0034;       #��ֵӦ��
set C35_Core_Pile2_0(4)     -0.0087;       #ѹ��Ӧ�� 
puts $f  $name
puts $f  $C35_Core_Pile2_0(4)
uniaxialMaterial Concrete04 $C35_Core_Pile2_0(1)  $C35_Core_Pile2_0(2)    $C35_Core_Pile2_0(3)     $C35_Core_Pile2_0(4)     [expr sqrt(-1*$C35_Core_Pile2_0(2)/1000)*5e6]   


#Pile1.5������������C35��Manderģ��
set name			    "Pile1_5m"
set C35_Core_Pile1_5(1)      22;
set C35_Core_Pile1_5(2)     -25642;        #��ѹǿ��
set C35_Core_Pile1_5(3)     -0.0030;       #��ֵӦ��
set C35_Core_Pile1_5(4)     -0.0074;       #ѹ��Ӧ�� 
puts $f  $name
puts $f  $C35_Core_Pile1_5(4)
uniaxialMaterial Concrete04 $C35_Core_Pile1_5(1)  $C35_Core_Pile1_5(2)    $C35_Core_Pile1_5(3)     $C35_Core_Pile1_5(4)     [expr sqrt(-1*$C35_Core_Pile1_5(2)/1000)*5e6] 


#SidePier������������C50��Manderģ��
set name			    "SidePier"
set C50_Core_SidePier(1)      23;
set C50_Core_SidePier(2)     -38177;        #��ѹǿ��
set C50_Core_SidePier(3)     -0.0038;       #��ֵӦ��
set C50_Core_SidePier(4)     -0.0208;       #ѹ��Ӧ�� 
puts $f  $name
puts $f  $C50_Core_SidePier(4)
uniaxialMaterial Concrete04 $C50_Core_SidePier(1)  $C50_Core_SidePier(2)    $C50_Core_SidePier(3)     $C50_Core_SidePier(4)     [expr sqrt(-1*$C50_Core_SidePier(2)/1000)*5e6] 


#Tower1������������C50��Manderģ��
set name			    "Tower-1"
set C50_Core_Tower1(1)      24;
set C50_Core_Tower1(2)     -62151;        #��ѹǿ��
set C50_Core_Tower1(3)     -0.0112;       #��ֵӦ��
set C50_Core_Tower1(4)     -0.01115;       #ѹ��Ӧ�� 
puts $f  $name
puts $f  $C50_Core_Tower1(4)
uniaxialMaterial Concrete04 $C50_Core_Tower1(1)  $C50_Core_Tower1(2)    $C50_Core_Tower1(3)     $C50_Core_Tower1(4)     [expr sqrt(-1*$C50_Core_Tower1(2)/1000)*5e6]

#Tower2������������C50��Manderģ��
set name			    "Tower-2"
set C50_Core_Tower2(1)      25;
set C50_Core_Tower2(2)     -60047;        #��ѹǿ��
set C50_Core_Tower2(3)     -0.0105;       #��ֵӦ��
set C50_Core_Tower2(4)     -0.0118;       #ѹ��Ӧ�� 
puts $f  $name
puts $f  $C50_Core_Tower2(4)
uniaxialMaterial Concrete04 $C50_Core_Tower2(1)  $C50_Core_Tower2(2)    $C50_Core_Tower2(3)     $C50_Core_Tower2(4)     [expr sqrt(-1*$C50_Core_Tower2(2)/1000)*5e6]



#Tower3������������C50��Manderģ��
set name			    "Tower-3"
set C50_Core_Tower3(1)      26;
set C50_Core_Tower3(2)     -59340;        #��ѹǿ��
set C50_Core_Tower3(3)     -0.0103;       #��ֵӦ��
set C50_Core_Tower3(4)     -0.0119;       #ѹ��Ӧ�� 
puts $f  $name
puts $f  $C50_Core_Tower3(4)
uniaxialMaterial Concrete04 $C50_Core_Tower3(1)  $C50_Core_Tower3(2)    $C50_Core_Tower3(3)     $C50_Core_Tower3(4)     [expr sqrt(-1*$C50_Core_Tower3(2)/1000)*5e6] 


#Tower4������������C50��Manderģ��
set name			    "Tower-4"
set C50_Core_Tower4(1)      27;
set C50_Core_Tower4(2)     -55856;        #��ѹǿ��
set C50_Core_Tower4(3)     -0.0092;       #��ֵӦ��
set C50_Core_Tower4(4)     -0.0124;       #ѹ��Ӧ�� 
puts $f  $name
puts $f  $C50_Core_Tower4(4)
uniaxialMaterial Concrete04 $C50_Core_Tower4(1)  $C50_Core_Tower4(2)    $C50_Core_Tower4(3)     $C50_Core_Tower4(4)     [expr sqrt(-1*$C50_Core_Tower4(2)/1000)*5e6]






   