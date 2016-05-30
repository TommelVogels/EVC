
difference()
{
translate([0.75,-3,-4])
{
    cube([37,64,3]);
}

translate([20.5,9,-2.75])
{
cylinder(2,1.25,1.25);
}

translate([20.5,9,-4.5])
{
cylinder(3,4,4);
}

translate([0.5,55,-2.25])
{
    rotate([90,0,90])
    {
    cylinder(35.5,3.5,3.5);
    }
}

translate([10.5,-13,-8.25])
{
    rotate([0,0,60])
    {
    cube([10,20,10]);
    }
}

translate([25.5,-3,-8.25])
{
    rotate([0,0,-65])
    {
    cube([10,20,10]);
    }
}

translate([3.75,48,-15])
{
    rotate([0,0,0])
    {
    cylinder(25,1.25,1.25);
    }
}

}



translate([0.75,60,-12])
{
    cube([37,3,20]);
}

difference()
{
translate([0.5,40,-7])
{
    cube([35,20,10]);
}

translate([0.5,55,-2.25])
{
    rotate([90,0,90])
    {
    cylinder(35.5,3.5,3.5);
    }
}

translate([3.75,48,-15])
{
    rotate([0,0,0])
    {
    cylinder(25,1.25,1.25);
    }
}


}

difference()
{
translate([2.75,-3,-1])
{
cube([15,8,2.75]);
}

translate([10.5,-13,-8.25])
{
    rotate([0,0,60])
    {
    cube([10,20,10]);
    }
}}

translate([2.75,13,-1])
{
cube([15,8,2.75]);
}


difference()
{
translate([22.75,-3,-1])
{
cube([15,8,2.75]);
}

translate([25.5,-3,-8.25])
{
    rotate([0,0,-65])
    {
    cube([10,20,10]);
    }
}}

translate([22.75,13,-1])
{
cube([15,8,2.75]);
}

translate([28.75,40,4.25])
{
cube([6,20,1.5]);
}

difference()
{
translate([0.75,40,4.25])
{
cube([6,20,1.5]);
}

translate([3.75,48,-15])
{
    rotate([0,0,0])
    {
    cylinder(25,1.25,1.25);
    }
}
}

difference()
{
    
translate([0.75,40,-10.0])
{
cube([6,20,1.5]);
}

translate([3.75,48,-15])
{
    rotate([0,0,0])
    {
    cylinder(25,1.25,1.25);
    }
}
}

translate([28.75,40,-10.0])
{
cube([6,20,1.5]);
}

    
translate([39.5,57.25,-12])
{
    cube([3,5.75,20]);
}

translate([37.5,60,-12])
{
    cube([3,3,5.75]);
}



translate([0,0,14])
{
    rotate([-90,0,0])
    {
    //import("servo.stl");
    }
}