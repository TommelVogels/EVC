{

difference()
{
sphere(47);

translate([-50,-50,-1])
{    
    cube(100);
}

translate([-50,-5,-50])
{    
    cube([100,10,15]);
}

sphere(45);

translate([-6.5,-39,-41])
{
cube([13,19,23]);
}

}

difference()
{
    
translate([-12.5,-42.5,-13])
{
cube([25,27.6,5]);
}

translate([0,-13,-11])
{
rotate([90,0,0])
{
cylinder(4,1.5,1.5);
}
}

}


difference()
{
    
translate([-11,-22.5,-41.5])
{
cube([21,7,3.5]);
}

translate([0,-15,-40])
{
rotate([90,0,0])
{
cylinder(4,1.5,1.5);
}
}

}

translate([-11,-23.5,-38.5])
{
cube([4,8,26]);
}

translate([6,-23.5,-38.5])
{
cube([4,8,26]);
}

}

translate([-12.5,-20,-11])
{
cube([25,3,10]);
}

translate([-5,-45,-4])
{
cube([10,30,3]);
}


difference()
{
translate([-20,-20,-5.5])
{
cube([40,30,4.5]);
}

translate([-17.5,-3.75,-4])
{
cube([36,7.5,4]);
}
}

difference()
{
translate([-7,-40,-42])
{
cube([14,20,30]);
}

translate([-6.5,-39,-41])
{
cube([13,19,28]);
}
}

translate([8,-30,-5])
{

    rotate([0,90,90])
    {
    import("servo.stl");
    }

}

translate([-25,8.4,30])
{

    rotate([180,0,0])
    {
    import("servo.stl");
    }

}


