import sys
import gmsh

gmsh.initialize()

gmsh.model.add('Simple Tokamak')
# объем
gmsh.model.occ.addTorus(0, 0, 0, 2, 1, 1)
gmsh.model.occ.addTorus(0, 0, 0, 2, 0.5, 2)
gmsh.model.occ.cut([(3, 1)], [(3, 2)], 10)
# сетка 3D
gmsh.model.occ.synchronize()
gmsh.option.setNumber("Mesh.MeshSizeMax", 0.2)
gmsh.model.mesh.generate(3)
gmsh.write("simple_tokamak.msh")
gmsh.write("simple_tokamak.geo_unrolled")
# отображение
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()
gmsh.finalize()
