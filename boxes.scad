use <../UniversalTools/CADLIB/base.scad>;
use <../UniversalTools/CADLIB/mechanic.scad>;

module bat_box()
{
    difference()
    {
        union() {
            box(internal = [117, 70, 34], shell = [2,2,2]);
            translate([117/2+11.001,0,0])
            //cube([22,3,36], center = true);
            box(internal = [18, 70, 34], shell = [2,2,2]);
            translate([10, 0, 0])
            mirrorcp([1, 0, 0])
            translate([117/2 + 1, 0, -34/2])
            cube([22, 70 + 4 + 30, 2.01], center = true);
        }
        translate([117/2 + 12, 70/2 + 0.5, 1])
        cube([12, 10, 29], center = true);
        translate([10.5, 0, 0])
        mirrorcp([1,0,0]) mirrorcp([0,1,0])
        translate([117/2 + 0.5, (70 + 4 + 30)/2 - 5, 0])
        cylinder(d = 4, h = 100, center = true);
        mirrorcp([1,0,0])
        translate([117/2, 0, 8])
        rotate([0,90,0])
        cylinder(d=6,h=100,center=true);
    }
}

$fn = 100;
bat_box();
