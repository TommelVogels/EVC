
difference()
{
translate([0.75,-3,-4])
{
    cube([37,64,3]);
}

translate([20.5,9,-4.5])
{
cylinder(2,1.25,1.25);
}

translate([20.5,9,-2.75])
{
cylinder(3,4,4);
}

translate([0.5,55,-2.25])
{
    rotate([90,0,90])
    {
    cylinder(15.5,3.5,3.5);
    }
}

}


translate([0.75,60,-27])
{
    cube([37,3,50]);
}

difference()
{
translate([0.5,50,-7])
{
    cube([15,10,10]);
}

translate([0.5,55,-2.25])
{
    rotate([90,0,90])
    {
    cylinder(15.5,3.5,3.5);
    }
}


}

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


translate([0,0,14])
{
    rotate([-90,0,0])
    {
    //import("servo.stl");
    }
}