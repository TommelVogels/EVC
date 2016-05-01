
translate([2.75,-2,-1])
{
    cube([5,16,15]);
}

translate([2.75,-3,-6])
{
    cube([35,24,5]);
}

translate([32.75,-2,-1])
{
    cube([5,5,15]);
}

translate([2.75,-3,-1])
{
    cube([35,1,15]);
}

translate([32.75,7,-1])
{
    cube([5,7,15]);
}

translate([0,0,14])
{
    rotate([-90,0,0])
    {
    import("servo.stl");
    }
}