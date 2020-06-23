
# --------------------

wipe
model basic -ndm 3 -ndf 6

source fiberSections.tcl

set MCInfo [open MCInfo.txt r]
set var3 [split [read $MCInfo]]
set sectionName 		[lindex $var3 0]
set axialLoad  		[lindex $var3 1]
set moment		  	[lindex $var3 2]

if {$sectionName == "Pile2_0m"} {
set secTag 1
set   L1 	        2.0            ; #length of the outer rectangle section
set   a	        0.06           ; #the cover thickness of the concrete
set epsy 	[expr $HRB400(2)/$HRB400(4)];   # steel yield strain 
set Ky 	[expr $epsy/(0.7*($L1-2*$a))]; 	  # Estimated yield curvature

} elseif {$sectionName == "Pile1_5m"} {
set secTag 2
set   L1 	        1.5            ; #length of the outer rectangle section
set   a	        0.06           ; #the cover thickness of the concrete
set epsy 	[expr $HRB400(2)/$HRB400(4)];   # steel yield strain 
set Ky 	[expr $epsy/(0.7*($L1-2*$a))]; 	  # Estimated yield curvature

} elseif {$sectionName == "SidePier"} {
set secTag 3
set   L1 	        4.5            ; #length of the outer rectangle section
set   a	        0.04           ; #the cover thickness of the concrete
set epsy 	[expr $HRB400(2)/$HRB400(4)];   # steel yield strain 
set Ky 	[expr $epsy/(0.7*($L1-2*$a))]; 	  # Estimated yield curvature

} elseif {$sectionName == "Tower-1"} {
set secTag 4
set   L1 	        6.118            ; #length of the outer rectangle section
set   a	        0.06             ; #the cover thickness of the concrete
set epsy 	[expr $HRB400(2)/$HRB400(4)];   # steel yield strain 
set Ky 	[expr $epsy/(0.7*($L1-2*$a))]; 	  # Estimated yield curvature

} elseif {$sectionName == "Tower-2"} {
set secTag 5
set   L1 	        7.192            ; #length of the outer rectangle section
set   a	        0.06             ; #the cover thickness of the concrete
set epsy 	[expr $HRB400(2)/$HRB400(4)];   # steel yield strain 
set Ky 	[expr $epsy/(0.7*($L1-2*$a))]; 	  # Estimated yield curvature

} elseif {$sectionName == "Tower-3"} {
set secTag 6
set   L1 	        7.542            ; #length of the outer rectangle section
set   a	        0.06             ; #the cover thickness of the concrete
set epsy 	[expr $HRB400(2)/$HRB400(4)];   # steel yield strain 
set Ky 	[expr $epsy/(0.7*($L1-2*$a))]; 	  # Estimated yield curvature

} elseif {$sectionName == "Tower-4"} {
set secTag 7
set   L1 	        8.5            ; #length of the outer rectangle section
set   a	        0.06             ; #the cover thickness of the concrete
set epsy 	[expr $HRB400(2)/$HRB400(4)];   # steel yield strain 
set Ky 	[expr $epsy/(0.7*($L1-2*$a))]; 	  # Estimated yield curvature
}

set mu      40;			# Target ductility for analysis
set numIncr 8000;      		# Number of analysis increments
set maxK	[expr $mu*$Ky] 
set dK [expr $maxK/$numIncr]

# Define two nodes at (0,0)
node 1 0.0 0.0 0.0
node 2 0.0 0.0 0.0

# Fix all degrees of freedom except axial and bending. y is the longitudinal,z is the transverse
fix 1 1 1 1 1 1 1
fix 2 0 1 1 1 0 0
	
proc min {x1 x2} {
if {$x1>=$x2} {return $x2} elseif {$x1<$x2} {return $x1}
}
# Define element
element zeroLengthSection  1   1   2  $secTag -oirent 1 0 0 0 1 0
# Create recorder
recorder Node -file MomentCurvature.txt -time -node 2 -dof 6 disp

file mkdir	steelRecorder
file mkdir	coreRecorder
for {set i 1} {$i<= [min $barNum($secTag) 180]} {incr i 1} {
	set Yloc($i)       		[lindex $barFiber($secTag) [expr 3*($i-1)+0]]
	set Zloc($i)       		[lindex $barFiber($secTag) [expr 3*($i-1)+1]]
	recorder Element -file steelRecorder/steelFiberStressStrain$i.txt -time -ele 1 section fiber $Yloc($i) $Zloc($i) stressStrain
	}
for {set j 1} {$j<= [min $coreNum($secTag) 300]} {incr j 1} {
	set Yloc($j)       		[lindex $coreFiber($secTag) [expr 3*($j-1)+0]]
	set Zloc($j)       		[lindex $coreFiber($secTag) [expr 3*($j-1)+1]]
	recorder Element -file coreRecorder/coreFiberStressStrain$j.txt -time -ele 1 section fiber $Yloc($j) $Zloc($j) stressStrain
	}

proc min {x1 x2} {
if {$x1>=$x2} {return $x2} elseif {$x1<$x2} {return $x1}
}
# Define constant axial load
pattern Plain 1 "Constant" {
	load 2 [expr -$axialLoad] 0.0 0.0 0.0 $moment 0.0
}

integrator LoadControl 0.0
system SparseGeneral -piv;	# Overkill, but may need the pivoting!
test NormUnbalance 1.0e-8 1000
# the tolerance criteria used to check for convergence 
# the max number of iterations to check before returning failure condition  
	 
numberer Plain
constraints Plain
algorithm Newton
analysis Static
analyze 1

loadConst      -time 0.0

# Define reference moment
pattern Plain 2 "Linear" {
	load 2 0.0 0.0 0.0 0.0 0.0 1.0
}

# Compute curvature increment
set dK [expr $maxK/$numIncr]

# Use displacement control at node 2 for section analysis
integrator DisplacementControl 2 6 $dK 
# Do the section analysis
analyze $numIncr
puts "MomentCurvature IS OK!"


