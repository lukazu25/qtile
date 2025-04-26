If you use a display manager
```bash
sudo cp qtile.desktop /usr/share/xsessions/
```
If you don't
```bash
echo "exec qtile start >> ~/.xinitrc
```
dunst config 
```bash
sudo cp dunstrc ~/.config/dconf/
```
copy autostart to qtile directory
```bash
sudo cp autostart.sh ~/.config/qtile/
```
 make it executable 
```bash
sudo chmod +x autostart.sh
```
