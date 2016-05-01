


{

difference()
{
sphere(48);

translate([-50,-50,0])
{    
    cube(100);
}

translate([-50,-5,-50])
{    
    cube([100,10,15]);
}

sphere(45);
}

difference()
{
    
translate([-12.5,-43.5,-15])
{
cube([25,28.6,5]);
}

translate([0,-13,-12])
{
rotate([90,0,0])
{
cylinder(4,1.5,1.5);
}
}

}


difference()
{
    
translate([-12.5,-22.5,-40.5])
{
cube([25,7,4.5]);
}

translate([0,-15,-39])
{
rotate([90,0,0])
{
cylinder(4,1.5,1.5);
}
}

}

translate([-12,-23.5,-39.5])
{
cube([5,8,25]);
}

translate([7,-23.5,-39.5])
{
cube([5,8,25]);
}

}

difference()
{
    
translate([7,-10,-5])
{
cube([39,20,5]);
}

translate([9,0,-5])
{
rotate([0,0,0])
{
cylinder(6,1.5,1.5);
}
}


}

difference()
{
    
translate([-46,-10,-5])
{
cube([29,20,5]);
}

translate([-19,0,-5])
{
rotate([0,0,0])
{
cylinder(5,1.5,1.5);
}
}


}

translate([-17,-10,-10])
{
cube([25,3,10]);
}

translate([-17,7,-10])
{
cube([25,3,10]);
}

translate([-12.5,-20,-10])
{
cube([25,3,10]);
}

translate([-12.5,-20,-5])
{
cube([25,10,5]);
}



translate([8,-30,-7])
{

    rotate([0,90,90])
    {
    import("servo.stl");
    }

}

translate([-25,-8.4,-22])
{

    rotate([0,0,0])
    {
    import("servo.stl");
    }

}


