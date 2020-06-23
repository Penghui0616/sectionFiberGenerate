model basic -ndm 3 -ndf 6

#===========保存核心区混凝土极限压应变==============================

set f [open ./ecu.txt w+]


#============================================================

#HRB400钢筋材料，抛物线强化

set HRB400(1)      1;             
set HRB400(2)      400.0e3;         # 屈服应力
set HRB400(3)      510.0e3;         # 极限应力
set HRB400(4)      2.0e8;           # 弹性模量
set HRB400(5)      2.0e6;           # 强化段初始刚度
set HRB400(6)      0.045;           # 强化段开始应变
set HRB400(7)      0.100;             # 极限应变

uniaxialMaterial ReinforcingSteel $HRB400(1) $HRB400(2) $HRB400(3) $HRB400(4) $HRB400(5) $HRB400(6) $HRB400(7)
#************************************************************

#保护层混凝土C35，Mander模型

set C35_Cover(1)      11;
set C35_Cover(2)     -23800;        #抗压强度标准值
set C35_Cover(3)     -0.0020;       #峰值应变
set C35_Cover(4)     -0.004;        #压溃应变 

uniaxialMaterial Concrete04 $C35_Cover(1)  $C35_Cover(2)    $C35_Cover(3)     $C35_Cover(4)     [expr sqrt(-1*$C35_Cover(2)/1000)*(5e6)]    
#************************************************************

#保护层混凝土C50，Mander模型

set C50_Cover(1)      12;
set C50_Cover(2)     -32400;        #抗压强度标准值
set C50_Cover(3)     -0.0020;       #峰值应变
set C50_Cover(4)     -0.004;        #压溃应变 

uniaxialMaterial Concrete04 $C50_Cover(1)  $C50_Cover(2)    $C50_Cover(3)     $C50_Cover(4)     [expr sqrt(-1*$C50_Cover(2)/1000)*5e6]    
#************************************************************


#Pile2.0核心区混凝土C35，Mander模型
set name			    "Pile2_0m"
set C35_Core_Pile2_0(1)      21;
set C35_Core_Pile2_0(2)     -26667;        #抗压强度
set C35_Core_Pile2_0(3)     -0.0034;       #峰值应变
set C35_Core_Pile2_0(4)     -0.0087;       #压溃应变 
puts $f  $name
puts $f  $C35_Core_Pile2_0(4)
uniaxialMaterial Concrete04 $C35_Core_Pile2_0(1)  $C35_Core_Pile2_0(2)    $C35_Core_Pile2_0(3)     $C35_Core_Pile2_0(4)     [expr sqrt(-1*$C35_Core_Pile2_0(2)/1000)*5e6]   


#Pile1.5核心区混凝土C35，Mander模型
set name			    "Pile1_5m"
set C35_Core_Pile1_5(1)      22;
set C35_Core_Pile1_5(2)     -25642;        #抗压强度
set C35_Core_Pile1_5(3)     -0.0030;       #峰值应变
set C35_Core_Pile1_5(4)     -0.0074;       #压溃应变 
puts $f  $name
puts $f  $C35_Core_Pile1_5(4)
uniaxialMaterial Concrete04 $C35_Core_Pile1_5(1)  $C35_Core_Pile1_5(2)    $C35_Core_Pile1_5(3)     $C35_Core_Pile1_5(4)     [expr sqrt(-1*$C35_Core_Pile1_5(2)/1000)*5e6] 


#SidePier核心区混凝土C50，Mander模型
set name			    "SidePier"
set C50_Core_SidePier(1)      23;
set C50_Core_SidePier(2)     -38177;        #抗压强度
set C50_Core_SidePier(3)     -0.0038;       #峰值应变
set C50_Core_SidePier(4)     -0.0208;       #压溃应变 
puts $f  $name
puts $f  $C50_Core_SidePier(4)
uniaxialMaterial Concrete04 $C50_Core_SidePier(1)  $C50_Core_SidePier(2)    $C50_Core_SidePier(3)     $C50_Core_SidePier(4)     [expr sqrt(-1*$C50_Core_SidePier(2)/1000)*5e6] 


#Tower1核心区混凝土C50，Mander模型
set name			    "Tower-1"
set C50_Core_Tower1(1)      24;
set C50_Core_Tower1(2)     -62151;        #抗压强度
set C50_Core_Tower1(3)     -0.0112;       #峰值应变
set C50_Core_Tower1(4)     -0.01115;       #压溃应变 
puts $f  $name
puts $f  $C50_Core_Tower1(4)
uniaxialMaterial Concrete04 $C50_Core_Tower1(1)  $C50_Core_Tower1(2)    $C50_Core_Tower1(3)     $C50_Core_Tower1(4)     [expr sqrt(-1*$C50_Core_Tower1(2)/1000)*5e6]

#Tower2核心区混凝土C50，Mander模型
set name			    "Tower-2"
set C50_Core_Tower2(1)      25;
set C50_Core_Tower2(2)     -60047;        #抗压强度
set C50_Core_Tower2(3)     -0.0105;       #峰值应变
set C50_Core_Tower2(4)     -0.0118;       #压溃应变 
puts $f  $name
puts $f  $C50_Core_Tower2(4)
uniaxialMaterial Concrete04 $C50_Core_Tower2(1)  $C50_Core_Tower2(2)    $C50_Core_Tower2(3)     $C50_Core_Tower2(4)     [expr sqrt(-1*$C50_Core_Tower2(2)/1000)*5e6]



#Tower3核心区混凝土C50，Mander模型
set name			    "Tower-3"
set C50_Core_Tower3(1)      26;
set C50_Core_Tower3(2)     -59340;        #抗压强度
set C50_Core_Tower3(3)     -0.0103;       #峰值应变
set C50_Core_Tower3(4)     -0.0119;       #压溃应变 
puts $f  $name
puts $f  $C50_Core_Tower3(4)
uniaxialMaterial Concrete04 $C50_Core_Tower3(1)  $C50_Core_Tower3(2)    $C50_Core_Tower3(3)     $C50_Core_Tower3(4)     [expr sqrt(-1*$C50_Core_Tower3(2)/1000)*5e6] 


#Tower4核心区混凝土C50，Mander模型
set name			    "Tower-4"
set C50_Core_Tower4(1)      27;
set C50_Core_Tower4(2)     -55856;        #抗压强度
set C50_Core_Tower4(3)     -0.0092;       #峰值应变
set C50_Core_Tower4(4)     -0.0124;       #压溃应变 
puts $f  $name
puts $f  $C50_Core_Tower4(4)
uniaxialMaterial Concrete04 $C50_Core_Tower4(1)  $C50_Core_Tower4(2)    $C50_Core_Tower4(3)     $C50_Core_Tower4(4)     [expr sqrt(-1*$C50_Core_Tower4(2)/1000)*5e6]






   