import gmsh
import math
import os
import sys

gmsh.initialize()

path = os.path.dirname(os.path.abspath(__file__))
gmsh.merge(os.path.join(path, 'bottle.stl'))

# Модель бутылки получилась не очень удачно: не учел, что мешеру будет тяжело справиться с геометрией горлышка, и при
# запуске край получается неаккуратным. При заданных параметрах сетка будет наиболее качественная. Можно поставить
# funny = False и сильно сократить время мешинга, но качество сетки ухудшится.

angle = 60
forceParametrizablePatches = True
includeBoundary = True
curveAngle = 180
gmsh.model.mesh.classifySurfaces(angle * math.pi / 180., includeBoundary, forceParametrizablePatches,
                                 curveAngle * math.pi / 180.)
gmsh.model.mesh.createGeometry()

e = gmsh.model.getEntities(2)
v = gmsh.model.geo.addSurfaceLoop([e[i][1] for i in range(len(e))])
gmsh.model.geo.addVolume([v])

gmsh.model.geo.synchronize()

funny = True
f = gmsh.model.mesh.field.add("MathEval")
if funny:
    gmsh.model.mesh.field.setString(f, "F", "2*Sin((x+y)/5) + 3")
else:
    gmsh.model.mesh.field.setString(f, "F", "4")
gmsh.model.mesh.field.setAsBackgroundMesh(f)

gmsh.model.mesh.generate(3)
gmsh.write('bottle_stl.msh')

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
