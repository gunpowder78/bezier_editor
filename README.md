# Bezier editor
This project was done for academic course "Mathematical methods of computer graphics" at University of Wrocław.

# Installation
1. clone repository: git clone https://github.com/jdzejdzej/bezier_editor.git
2. create virtualenv in bezier_editor: virtualenv --no-site-packages env
3. activate virtualenv: . env/bin/activate or for Windows  env\Scripts\activate
4. install dependencies: pip install -r requirements.txt
5. for Windows users: download precompiled dependencies from https://www.lfd.uci.edu/~gohlke/pythonlibs and install from wheel

# Run
python bezier_editor.py

# Types of curves:
- Bezier Curve
- Parametric Bezier Curve

# Operations on curves:
- add/delete/copy curve
- rotate/translate curve
- split/join curve (c0, c1)
- elevate/reduce degree of curve
- convex hull

# Operation on points:
- add/remove points
- change weight of point
- translate point

# Others:
- change colors of points, curve, convex hull
- save as image
- save as csv
- read from csv
