# amonite
A simple game engine built around pyglet.</br>

PyPi page:</br>
https://pypi.org/project/amonite/

## Settings
You can change game settings by creating and manually editing a settings json file:</br>

### Debug
  * **debug** -> General debug setting, shows some useful features such as update time, render time and collisions.</br>
  * **show_collisions** -> Specific debug setting, shows collisions, but only if debug is true</br>
  * **show_tiles_grid** -> Specific debug setting, shows tilemap grid lines.</br>
  * **free_cam_bounds** -> Specific debug setting, allows the player to see beyond camera bounds.</br>

### Texts
  * **title** -> Game title: defines the title of the game window.</br>
  * **font_name** -> Game font; if you don't have the font installed, then an error will occur.</br>

### Rendering
  * **view_width** -> Base view width, defines the amount of pixels you can see horizontally</br>
  * **view_height** -> Base view height, defines the amount of pixels you can see vertically</br>
  * **pixel_perfect** -> Unused.</br>
  * **window_width** -> Actual window width in pixels (only used if not fullscreen).</br>
  * **window_height** -> Actual window height in pixels (only used if not fullscreen).</br>
  * **fullscreen** -> Fullscreen mode toggle.</br>

### Misc
  * **target_fps** -> Target FPS; keep this value high if you don't want any lags.</br>
  * **camera_speed** -> The speed at which the camera follows the player, the higher the speed, the closer it will be to the player.</br>
  * **layers_z_spacing** -> Distance between rendered layers on the Z axis.</br>
  * **tilemap_buffer** -> Width (in tiles number) of tilemap buffer, a higher tilemap buffer will reduce room size.</br>

### Sound
  * **sound** -> General sound setting, defines whether the game plays audio or not.</br>
  * **music** -> Specific sound setting, defines whether the game plays music or not.</br>
  * **sfx** -> Specific sound setting, defines whether the game plays sound effects or not.</br>

## Animations
All animations can be defined via a simple json definition file.</br>
Animation files are defined as follows:</br>
  * **name[string]**: name of the animation.</br>
  * **path[string]**: path to the animation file (starting from the application-defined assets directory).</br>
  * **anchor_x[int][optional]**: the x component of the animation anchor point.</br>
  * **anchor_y[int][optional]**: the y component of the animation anchor point.</br>
  * **center_x[bool][optional]**: whether the animation should be centered on the x axis. If present, this overrides the "anchor_x" parameter.</br>
  * **center_y[bool][optional]**: whether the animation should be centered on the y axis. If present, this overrides the "anchor_y" parameter.</br>
  * **duration[float][optional]**: the duration of each animation frame.</br>
  * **loop[bool][optional]**: whether the animation should loop or not.</br>

[Examples](/assets/sprites/iryo/animations)</br>

## Inventory
The inventory structure (sections, sizes etc) is defined by a json file made up as follows:
  * **sections[array]**: array of all inventory sections, each defined as follows:</br>
    * **size[string]**: string representation of the section size (in slots count), encoded as "[width],[height]".</br>
    * **name[string]**: name of the section, used to section to section linkage.</br>
    * **overflows[object]**: links to other sections upon overflow: tells which section the cursor should go to when overflowing in each direction. The go to for each overflow can be the name of another section or the "wrap" keyword, which means wrapping around itself keeping the other index unchanged.</br>
      * **top[string]**: section to go to when overflowing to the top.</br>
      * **bottom[string]**: section to go to when overflowing to the bottom.</br>
      * **left[string]**: section to go to when overflowing to the left.</br>
      * **right[string]**: section to go to when overflowing to the right.</br>