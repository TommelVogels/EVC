
difference()
{
translate([3.75,-2,-1])
{
    cube([5,16,14]);
}

translate([6.25,14,5.5])
{
    rotate([90,0,0])
    {
    cylinder(8,1.25,1.25);
    }
}

}

difference()
{
translate([0.75,-3,-4])
{
    cube([37,20,3]);
}

translate([20.5,9,-4.5])
{
cylinder(2,1.25,1.25);
}

translate([20.5,9,-2.75])
{
cylinder(3,4,4);
}


}

/*
translate([2.75,-3,-6.75])
{
cube([15,8,2.75]);
}

translate([2.75,13,-6.75])
{
cube([15,8,2.75]);
}

translate([22.75,-3,-6.75])
{
cube([15,8,2.75]);
}

translate([22.75,13,-6.75])
{
cube([15,8,2.75]);
}
*/

translate([32.75,-2,-1])
{
    cube([3,5,14]);
}

difference()
{
translate([-16.25,-3,-14])
{
    cube([72,1,37]);
}

translate([-10.25,-3,-10])
{
    cube([2,1,30]);
}


translate([48,-3,-10])
{
    cube([2,1,30]);
}

}




translate([39.5,-3,-4])
{
    cube([3,20,3]);
}

translate([37.5,-3,-4])
{
    cube([3,3,3]);
}


difference()
{
    
translate([32.75,7,-1])
{
    cube([5,7,14]);
}

translate([35,14,5.5])
{
    rotate([90,0,0])
    {
    cylinder(8,1.25,1.25);
    }
}

}

translate([0,0,14])
{
    rotate([-90,0,0])
    {
    //import("servo.stl");
    }
}