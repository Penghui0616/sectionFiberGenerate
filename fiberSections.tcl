
source material.tcl
set GJ 1e10
#################################Pile2.0m##########################################
section Fiber 1 -GJ $GJ {
		set Data [open Pile2.0m/coreDivide.txt r]
		set coreFiber(1) [split [read $Data]]
		set coreNum(1) [expr  [llength $coreFiber(1)]/3]
		for {set i1 1} {$i1<=$coreNum(1)} {incr i1 1} {
			set yloc($i1) 	[lindex $coreFiber(1) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coreFiber(1) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coreFiber(1) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C35_Core_Pile2_0(1)
		}
		set Data [open Pile2.0m/coverDivide.txt r]
		set coverFiber(1) [split [read $Data]]
		set coverNum(1) [expr  [llength $coverFiber(1)]/3]
		for {set i1 1} {$i1<=$coverNum(1)} {incr i1 1} {
			set yloc($i1) 	[lindex $coverFiber(1) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coverFiber(1) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coverFiber(1) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C35_Cover(1)
		}
		set Data [open Pile2.0m/barDivide.txt r]
		set barFiber(1) [split [read $Data]]
		set barNum(1) [expr  [llength $barFiber(1)]/3]
		for {set i1 1} {$i1<=$barNum(1)} {incr i1 1} {
			set yloc($i1) 	[lindex $barFiber(1) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $barFiber(1) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $barFiber(1) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $HRB400(1)
		}
	       	
	} 


############################Pile1.5m#########################################
section Fiber 2 -GJ $GJ {
		set Data [open Pile1.5m/coreDivide.txt r]
		set coreFiber(2) [split [read $Data]]
		set coreNum(2) [expr  [llength $coreFiber(2)]/3]
		for {set i1 1} {$i1<=$coreNum(2)} {incr i1 1} {
			set yloc($i1) 	[lindex $coreFiber(2) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coreFiber(2) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coreFiber(2) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C35_Core_Pile1_5(1)
		}
		set Data [open Pile1.5m/coverDivide.txt r]
		set coverFiber(2) [split [read $Data]]
		set coverNum(2) [expr  [llength $coverFiber(2)]/3]
		for {set i1 1} {$i1<=$coverNum(2)} {incr i1 1} {
			set yloc($i1) 	[lindex $coverFiber(2) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coverFiber(2) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coverFiber(2) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C35_Cover(1)
		}
		set Data [open Pile1.5m/barDivide.txt r]
		set barFiber(2) [split [read $Data]]
		set barNum(2) [expr  [llength $barFiber(2)]/3]
		for {set i1 1} {$i1<=$barNum(2)} {incr i1 1} {
			set yloc($i1) 	[lindex $barFiber(2) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $barFiber(2) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $barFiber(2) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $HRB400(1)
		}
	       	
	} 

############################SidePier#########################################
section Fiber 3 -GJ $GJ {
		set Data [open SidePier/coreDivide.txt r]
		set coreFiber(3) [split [read $Data]]
		set coreNum(3) [expr  [llength $coreFiber(3)]/3]
		for {set i1 1} {$i1<=$coreNum(3)} {incr i1 1} {
			set yloc($i1) 	[lindex $coreFiber(3) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coreFiber(3) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coreFiber(3) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C50_Core_SidePier(1)
		}
		set Data [open SidePier/coverDivide.txt r]
		set coverFiber(3) [split [read $Data]]
		set coverNum(3) [expr  [llength $coverFiber(3)]/3]
		for {set i1 1} {$i1<=$coverNum(3)} {incr i1 1} {
			set yloc($i1) 	[lindex $coverFiber(3) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coverFiber(3) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coverFiber(3) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C50_Cover(1)
		}
		set Data [open SidePier/barDivide.txt r]
		set barFiber(3) [split [read $Data]]
		set barNum(3) [expr  [llength $barFiber(3)]/3]
		for {set i1 1} {$i1<=$barNum(3)} {incr i1 1} {
			set yloc($i1) 	[lindex $barFiber(3) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $barFiber(3) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $barFiber(3) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $HRB400(1)
		}
	       	
	} 

############################Tower-1#########################################
section Fiber 4 -GJ $GJ {
		set Data [open Tower-1/coreDivide.txt r]
		set coreFiber(4) [split [read $Data]]
		set coreNum(4) [expr  [llength $coreFiber(4)]/3]
		for {set i1 1} {$i1<=$coreNum(4)} {incr i1 1} {
			set yloc($i1) 	[lindex $coreFiber(4) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coreFiber(4) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coreFiber(4) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C50_Core_Tower1(1)
		}
		set Data [open Tower-1/coverDivide.txt r]
		set coverFiber(4) [split [read $Data]]
		set coverNum(4) [expr  [llength $coverFiber(4)]/3]
		for {set i1 1} {$i1<=$coverNum(4)} {incr i1 1} {
			set yloc($i1) 	[lindex $coverFiber(4) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coverFiber(4) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coverFiber(4) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C50_Cover(1)
		}
		set Data [open Tower-1/barDivide.txt r]
		set barFiber(4) [split [read $Data]]
		set barNum(4) [expr  [llength $barFiber(4)]/3]
		for {set i1 1} {$i1<=$barNum(4)} {incr i1 1} {
			set yloc($i1) 	[lindex $barFiber(4) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $barFiber(4) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $barFiber(4) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $HRB400(1)
		}
	       	
	} 


############################Tower-2#########################################
section Fiber 5 -GJ $GJ {
		set Data [open Tower-2/coreDivide.txt r]
		set coreFiber(5) [split [read $Data]]
		set coreNum(5) [expr  [llength $coreFiber(5)]/3]
		for {set i1 1} {$i1<=$coreNum(5)} {incr i1 1} {
			set yloc($i1) 	[lindex $coreFiber(5) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coreFiber(5) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coreFiber(5) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C50_Core_Tower2(1)
		}
		set Data [open Tower-2/coverDivide.txt r]
		set coverFiber(5) [split [read $Data]]
		set coverNum(5) [expr  [llength $coverFiber(5)]/3]
		for {set i1 1} {$i1<=$coverNum(5)} {incr i1 1} {
			set yloc($i1) 	[lindex $coverFiber(5) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coverFiber(5) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coverFiber(5) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C50_Cover(1)
		}
		set Data [open Tower-2/barDivide.txt r]
		set barFiber(5) [split [read $Data]]
		set barNum(5) [expr  [llength $barFiber(5)]/3]
		for {set i1 1} {$i1<=$barNum(5)} {incr i1 1} {
			set yloc($i1) 	[lindex $barFiber(5) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $barFiber(5) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $barFiber(5) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $HRB400(1)
		}
	       	
	} 

############################Tower-3#########################################
section Fiber 6 -GJ $GJ {
		set Data [open Tower-3/coreDivide.txt r]
		set coreFiber(6) [split [read $Data]]
		set coreNum(6) [expr  [llength $coreFiber(6)]/3]
		for {set i1 1} {$i1<=$coreNum(6)} {incr i1 1} {
			set yloc($i1) 	[lindex $coreFiber(6) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coreFiber(6) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coreFiber(6) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C50_Core_Tower3(1)
		}
		set Data [open Tower-3/coverDivide.txt r]
		set coverFiber(6) [split [read $Data]]
		set coverNum(6) [expr  [llength $coverFiber(6)]/3]
		for {set i1 1} {$i1<=$coverNum(6)} {incr i1 1} {
			set yloc($i1) 	[lindex $coverFiber(6) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coverFiber(6) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coverFiber(6) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C50_Cover(1)
		}
		set Data [open Tower-3/barDivide.txt r]
		set barFiber(6) [split [read $Data]]
		set barNum(6) [expr  [llength $barFiber(6)]/3]
		for {set i1 1} {$i1<=$barNum(6)} {incr i1 1} {
			set yloc($i1) 	[lindex $barFiber(6) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $barFiber(6) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $barFiber(6) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $HRB400(1)
		}
	       	
	} 

############################Tower-4#########################################
section Fiber 7 -GJ $GJ {
		set Data [open Tower-4/coreDivide.txt r]
		set coreFiber(7) [split [read $Data]]
		set coreNum(7) [expr  [llength $coreFiber(7)]/3]
		for {set i1 1} {$i1<=$coreNum(7)} {incr i1 1} {
			set yloc($i1) 	[lindex $coreFiber(7) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coreFiber(7) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coreFiber(7) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C50_Core_Tower4(1)
		}
		set Data [open Tower-4/coverDivide.txt r]
		set coverFiber(7) [split [read $Data]]
		set coverNum(7) [expr  [llength $coverFiber(7)]/3]
		for {set i1 1} {$i1<=$coverNum(7)} {incr i1 1} {
			set yloc($i1) 	[lindex $coverFiber(7) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $coverFiber(7) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $coverFiber(7) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $C50_Cover(1)
		}
		set Data [open Tower-4/barDivide.txt r]
		set barFiber(7) [split [read $Data]]
		set barNum(7) [expr  [llength $barFiber(7)]/3]
		for {set i1 1} {$i1<=$barNum(7)} {incr i1 1} {
			set yloc($i1) 	[lindex $barFiber(7) [expr 3*($i1-1)]]
			set zloc($i1)  	[lindex $barFiber(7) [expr 3*($i1-1)+1]]
			set A($i1)  	[lindex $barFiber(7) [expr 3*($i1-1)+2]]
			fiber $yloc($i1) $zloc($i1) $A($i1) $HRB400(1)
		}
	       	
	} 