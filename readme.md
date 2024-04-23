# Alpakka 3D-print

*Alpakka controller 3D-printed case and buttons (reference designs)*

## Project links
- [Alpakka Manual](https://inputlabs.io/devices/alpakka/manual).
- [Alpakka Firmware](https://github.com/inputlabs/alpakka_firmware).
- [Alpakka PCB](https://github.com/inputlabs/alpakka_pcb).
- [Alpakka 3D-print](https://github.com/inputlabs/alpakka_case). _(you are here)_
- [Input Labs Roadmap](https://github.com/orgs/inputlabs/projects/2/views/2).

## Previews
<span><img width='250px' src='./preview/print_A.png'/></span>
<span><img width='250px' src='./preview/print_B.png'/></span>
<span><img width='250px' src='./preview/print_C.png'/></span>
<span><img width='250px' src='./preview/print_D.png'/></span>
<span><img width='250px' src='./preview/print_E.png'/></span>
<span><img width='250px' src='./preview/print_F.png'/></span>

## LFS and file download
If you only want to download the Blender and STL files `DO NOT USE download ZIP` GitHub button, since it is not compatible with LFS (Large File Storage), but instead get the files from the [latest release](https://github.com/inputlabs/alpakka_case/releases/latest) package.

To use Git with this project it is required to install Git [Large File Storage](https://git-lfs.github.com).


## Parts hierarchy

### Main assembly
- `alpakka.blend` - Alpakka controller assembly.

### Case
- `case_front.blend` - Front case + cutouts.
- `case_back.blend` - Back case + cutouts.
- `case_cover.blend` - Rear bay cover.
- `anchor.blend` - Anchors holding the cases together.
- `lock.blend` - Screws holding the cases together.

### Buttons
- `button_dpad.blend` - Dpad buttons.
- `button_abxy.blend` - ABXY buttons.
- `button_select.blend` - Select/start buttons.
- `button_home.blend` - Home button.

### Triggers
- `trigger_R1.py (build123d)` - L1 and R1 shoulder triggers.
- `trigger_R2.blend` - L2 and R2 triggers.
- `trigger_R4.blend` - L4 and R4 triggers.

### Control widgets
- `hexagon.blend` - Touch sensitive surface.
- `thumbstick.blend` - Thumbstick cap.
- `dhat.blend` - 8-directional switch hat.
- `scrollwheel.py (build123d)` - Scrollwheel, core, and holder.

### Additional
- `soldering_stand.blend` - Tool to hold the PCB while soldering.
- `pcb.blend` - Reference model of the PCB.
- `shared.blend` - Common geometry nodes / modifiers shared by all parts.


## Exported filename labels
- `primary`: Primary color or material according to Alpakka reference design color pattern.
- `secondary`: Primary color or material according to Alpakka reference design color pattern.
- `any`: Non visible part or tool that can be printed in any material, even recycled ;)
- `015mm`: 0.15mm layer height, default for most prints.
- `007mm`: 0.07mm layer height, for parts that require extra finesse.
- `020mm`: 0.20mm layer height, for tools that we want to print fast.
- `2x`, `4x`: To be printed multiple times.

Except for the colors (which is up to you how to combine), it is very recommended to follow these indications, and to check the [Manual](https://inputlabs.io/devices/alpakka/manual/diy_case) for more details.


## Migration to Build123d
We are in the process of migrating 3D modelling from Blender to [Build123D](https://build123d.readthedocs.io), we decided to make the migration gradually, one part at a time.

The original Blender parts are still located in `blender/` folder.

While parts that are already ported into Build123D are located in `build123d/` folder.

The export script will create `STL` for all Blender and Build123D parts, and `STEP` only for Build123d parts.


## Developer commands
- `make release` - Create `blender.zip`, `stl.zip` and `step.zip`.
- `make clean` - Remove all export files and leftovers.
