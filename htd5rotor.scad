use <../UniversalTools/CADLIB/base.scad>;
use <../UniversalTools/CADLIB/htd.scad>;
use <../UniversalTools/MCAD/Bolts/nuts_and_bolts_v1.95.scad>;

module big_rotor()
{
    rotor_h = 16;
    border_h = 2;
    layer_h = 3;
    inside_h = 8;
    difference() {
        union() {
            htd5gear_teeth(width = rotor_h, n_teeth = 120, hole_d = 0);
            echo(r_out = 5.0 * 120 / (2 * PI) - 0.55);
            //translate([0,0,-rotor_h/2-border_h/2])
            //cylinder(d = 200, h = border_h, center = true);
            //translate([0,0,-rotor_h/2-layer_h/2-border_h])
            //cylinder(d = 170, h = layer_h, center = true);
            //translate([0,0,-rotor_h/2-layer_h - inside_h/2-border_h])
            //cylinder(d = 145, h = inside_h, center = true);
            translate([0,0,rotor_h/2+border_h/2])
            cylinder(d = 200, h = border_h, center = true);
        }
        union() {
            mirrorcp([1, 0, 0])
            translate([158/2, 0, 0])
            cylinder(d = 5, h = 100, center = true);
            mirrorcp([0, 1, 0])
            translate([0, 158/2, 0])
            cylinder(d = 5, h = 100, center = true);
        }
    }
}

module ant_hdr()
{
    difference()
    {
        union() {
            cube([58, 20.2, 34], center = true);
        }
        mirrorcp([1,0,0])
        translate([15, 0, 17-10])
        rotate([90,0,0])
        cylinder(d = 6.2, h = 100, center = true);
        mirrorcp([1,0,0])
        translate([15, 0, 17-26])
        rotate([90,0,0])
        cylinder(d = 6.2, h = 100, center = true);
        cylinder(d=10.2, h = 100, center = true);
        translate([0,0,-17])
        rotate([0,0,30])
        prism(54)
        hexagon(17.2);
    }
}

module ant_screw()
{
    difference()
    {
        union() {
            intersection() {
                hex_nut(height = 6, 
                    thread_d = 10,
                    size = 15,
                    tolerance = 0,
                    quality = 64,
                    bool_cut = 0, thread = "metric",
                    pitch = 1.5);
                translate([0, 0, 3])
                cylinder(h = 6, d = 15, center = true);
            }  
            translate([0, 0, 6+6])
            cylinder(h = 12, d = 15, center = true);
        }
        translate([0,0,0])
        prism(100)
        hexagon(6);
    }
}

$fn = 64;
scale([1.006,1.006,1])
big_rotor();
//ant_hdr();
//ant_screw();

